#!/usr/bin/env python3
"""Look up, validate, and search RGS (Referentie GrootboekSchema) codes.

Reads the official RGS workbook (.xlsx) with the standard library only, a
CSV/TSV export (official layout or GBNED/boekhoudplaza layout), or a small
built-in seed. Understands the official filter columns: the "te kiezen bij
aard" group selects (Basis, Uitgebr, EZ/VOF, ZZP, WoCo, Zorg) and the
"te vervallen" group drops (Inactief, BB, Agro, WKR, EZ/VOF, BV, WoCo, Zorg,
Bank, OZW-Coop-Sticht-FWO, ...). The BV drop column marks codes specific to a
BV; an entity that is not a BV removes them, a BV keeps them.

    python3 rgs_lookup.py --fetch 3.8                # download the official workbook
    python3 rgs_lookup.py --validate WBedKanKoa      # exit 0 valid, 1 unknown, 2 inactive
    python3 rgs_lookup.py --search hosting --entity bv --nivo 4
    python3 rgs_lookup.py --lookup BLimBanRba        # shows the omslag partner
    python3 rgs_lookup.py --children WBedKan         # the next level down

Without --file the cached official workbook is used when present, otherwise
the seed. The seed holds a few dozen codes verified against RGS 3.8; it is a
convenience, not the standard. Exit codes: 0 ok, 1 not found / no match,
2 found but inactive, 3 usage or input error.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

# Official download URLs, verified 2026-09-09 (Kennisbank items
# /definitieve-versie-rgs-38 and /alfaversie-rgs-39). They can rot; --fetch
# reports the URL it tried so a failure is diagnosable.
OFFICIAL_URLS = {
    "3.8": "https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx",
    "3.9a": "https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.9-alfa.xlsx",
}
CACHE_DIR = Path(os.environ.get("RGS_CACHE_DIR", Path.home() / ".cache" / "rgs"))

# Column aliases, lower-cased. The official workbook and GBNED exports differ.
HEADER_ALIASES: dict[str, list[str]] = {
    "code": ["referentiecode", "rgs-code", "rgs code", "rgscode", "refcode", "code"],
    "omslag": ["referentieomslagcode", "omslagcode", "omslag", "omslagrekening"],
    "sortering": ["sortering", "sorteercode", "sortering bw2"],
    "nummer": ["referentienummer", "refnr", "rgs-nr", "rgs nr", "referentiegrootboeknummer", "nummer", "rgsnr"],
    "desc_short": ["omschrijving (verkort)", "omschrijving kort", "omschrijvingkort"],
    "desc": ["omschrijving", "grootboekomschrijving", "standaardomschrijving", "omschrijving (lang)", "naam", "description"],
    "dc": ["d/c", "dc", "debet/credit", "debet credit", "indicatie d/c"],
    "nivo": ["nivo", "niveau", "nv", "level"],
    "inactief": ["inactief", "status", "actief", "vervallen"],
    "reknr": ["reknr", "rekeningnummer", "rgs-rekeningnummer"],
}
CHOOSE_COLUMNS = {"basis", "uitgebr", "uitgebreid", "ez/vof", "zzp", "woco", "zorg"}
GBNED_ENTITY_COLUMNS = {"zzp", "ez", "bv", "sv", "svc"}
ENTITY_HELP = "bv, ez (eenmanszaak/VOF), zzp, sv (stichting/vereniging), woco, zorg"
# Sector drop columns removed for every entity unless --keep names them.
SECTOR_DROPS = ("agro", "wkr", "bank", "ozw-coop-sticht-fwo", "woco", "zorg")


@dataclass
class RgsAccount:
    code: str
    desc: str = ""
    desc_short: str = ""
    nummer: str = ""
    nivo: str = ""
    dc: str = ""
    omslag: str = ""
    sortering: str = ""
    inactive: bool = False
    choose: dict[str, bool] = field(default_factory=dict)  # official "te kiezen" columns
    drop: dict[str, bool] = field(default_factory=dict)  # official "te vervallen" columns
    gbned: dict[str, str] = field(default_factory=dict)  # GBNED ZZP/EZ/BV/SV -> J / J+ / P / N

    @property
    def parent(self) -> str:
        if len(self.code) <= 1:
            return ""
        return self.code[:-3] if len(self.code) > 4 else self.code[0]

    def as_dict(self) -> dict:
        return {
            "code": self.code, "desc": self.desc, "desc_short": self.desc_short,
            "nummer": self.nummer, "nivo": self.nivo, "dc": self.dc, "omslag": self.omslag,
            "sortering": self.sortering, "inactive": self.inactive,
            "choose": sorted(k for k, v in self.choose.items() if v),
            "drop": sorted(k for k, v in self.drop.items() if v),
            "gbned": {k: v for k, v in self.gbned.items() if v},
        }

    def fmt(self, db: dict[str, RgsAccount] | None = None) -> str:
        head = [self.code]
        if self.nivo:
            head.append(f"niveau {self.nivo}")
        if self.dc:
            head.append(self.dc)
        if self.nummer:
            head.append(f"nr {self.nummer}")
        out = ["  ".join(head), f"    {self.desc or self.desc_short}"]
        if self.omslag:
            partner = db.get(self.omslag) if db else None
            out.append(f"    omslagcode -> {self.omslag}" + (f"  ({partner.desc})" if partner else ""))
        flags = [k for k, v in self.choose.items() if v]
        drops = [k for k, v in self.drop.items() if v]
        if flags or drops:
            out.append(f"    kiezen: {', '.join(flags) or '-'}   vervallen bij: {', '.join(drops) or '-'}")
        if self.gbned:
            out.append("    " + "  ".join(f"{k.upper()}={v or '-'}" for k, v in self.gbned.items()))
        if self.inactive:
            out.append("    INACTIEF: retired code, do not book to it")
        return "\n".join(out)


# --- seed: codes verified against RGS 3.8-def.xlsx on 2026-09-09 --------------
# (code, description, nivo, D/C, omslagcode). Grouping levels are not bookable.
_SEED_ROWS = [
    ("B", "Balans", "1", "", ""), ("W", "Winst-en-verliesrekening", "1", "", ""),
    ("BIva", "Immateriële vaste activa", "2", "D", ""), ("BMva", "Materiële vaste activa", "2", "D", ""),
    ("BVas", "Vastgoedbeleggingen", "2", "D", ""), ("BFva", "Financiële vaste activa", "2", "D", ""),
    ("BEff", "Effecten (kortlopend)", "2", "D", ""), ("BVrd", "Voorraden", "2", "D", ""),
    ("BPro", "Onderhanden projecten (activa)", "2", "D", ""), ("BVor", "Vorderingen", "2", "D", ""),
    ("BLim", "Liquide middelen", "2", "D", ""), ("BEiv", "Groepsvermogen - Eigen vermogen - Kapitaal", "2", "C", ""),
    ("BEga", "Egalisatierekening", "2", "C", ""), ("BVrz", "Voorzieningen", "2", "C", ""),
    ("BLas", "Langlopende schulden", "2", "C", ""), ("BSch", "Kortlopende schulden", "2", "C", ""),
    ("WOmz", "Netto-omzet", "2", "C", ""), ("WWiv", "Wijziging voorraden", "2", "C", ""),
    ("WOvb", "Overige bedrijfsopbrengsten", "2", "C", ""), ("WKpr", "Kostprijs van de omzet", "2", "D", ""),
    ("WPer", "Lasten uit hoofde van personeelsbeloningen", "2", "D", ""),
    ("WAfs", "Afschrijvingen op immateriële en materiële vaste activa", "2", "D", ""),
    ("WBed", "Overige bedrijfskosten", "2", "D", ""), ("WFbe", "Financiële baten en lasten", "2", "C", ""),
    ("WBel", "Belastingen", "2", "D", ""), ("WNer", "Nettoresultaat", "2", "C", ""),
    ("BMvaBeg", "Bedrijfsgebouwen", "3", "D", ""), ("BVorDeb", "Vorderingen op handelsdebiteuren", "3", "D", ""),
    ("BVorOva", "Overlopende activa", "3", "D", ""), ("BLimKas", "Kasmiddelen", "3", "D", ""),
    ("BEivGok", "Aandelenkapitaal", "3", "C", ""), ("BEivKap", "Eigen vermogen onderneming natuurlijke personen", "3", "C", ""),
    ("BEivAvd", "Aandeel van derden", "3", "C", ""), ("BSchOpa", "Overlopende passiva", "3", "C", ""),
    ("WBedAut", "Autokosten en andere vervoermiddelen", "3", "D", ""), ("WBedKan", "Kantoorkosten", "3", "D", ""),
    ("WBedAlk", "Andere kosten", "3", "D", ""),
    ("BMvaBegVvp", "Verkrijgings- of vervaardigingsprijs bedrijfsgebouwen", "4", "D", ""),
    ("BVorDebHad", "Handelsdebiteuren nominaal", "4", "D", ""),
    ("BLimKasKas", "Kas kasmiddelen", "4", "D", ""),
    ("BLimBanRba", "Rekening-courant bank tegoeden bij banken", "4", "D", "BSchSakRba"),
    ("BEivGokGea", "Normale aandelen aandelenkapitaal", "4", "C", ""),
    ("BEivKapPrs", "Privé-stortingen", "4", "C", ""), ("BEivKapPro", "Privé-opnamen", "4", "D", ""),
    ("BSchCreHac", "Handelscrediteuren nominaal schulden aan leveranciers en handelskredieten", "4", "C", ""),
    ("WBedAutOak", "Overige autokosten autokosten en andere vervoermiddelen", "4", "D", ""),
    ("WBedKanKoa", "Kosten automatisering kantoorkosten", "4", "D", ""),
    ("WBedKanSof", "Kosten software abonnementen", "4", "D", ""),
    ("WBedAlkOal", "Algemene kosten andere kosten", "4", "D", ""),
    ("WFbeRlmRgi", "Rentebaten vorderingen groepsmaatschappijen binnenland", "4", "C", "WFbeRlsRgi"),
    ("WFbeRlmRgu", "Rentebaten vorderingen groepsmaatschappijen buitenland", "4", "C", "WFbeRlsRgu"),
    ("WMfoBelMfo", "Mutatie fiscale oudedagsreserve belastingen over de winst of het verlies", "4", "D", ""),
    ("BMvaBegVvpBeg", "Beginbalans (overname eindsaldo vorig jaar) bedrijfsgebouwen", "5", "D", ""),
    ("BMvaBegVvpLie", "Investeringen bedrijfsgebouwen", "5", "D", ""),
]


def load_seed() -> dict[str, RgsAccount]:
    return {c: RgsAccount(code=c, desc=d, nivo=n, dc=dc, omslag=o, choose={"basis": True})
            for c, d, n, dc, o in _SEED_ROWS}


# --- minimal .xlsx reader (standard library only) -----------------------------
_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
       "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}


def _col_index(ref: str) -> int:
    n = 0
    for ch in ref:
        if ch.isalpha():
            n = n * 26 + (ord(ch.upper()) - 64)
        else:
            break
    return n - 1


def xlsx_sheet_names(path: str) -> list[str]:
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
    return [s.get("name", "") for s in wb.find("m:sheets", _NS)]


def _sheet_part(z: zipfile.ZipFile, sheet: str | None) -> tuple[str, str]:
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {r.get("Id"): r.get("Target", "") for r in rels}
    sheets = wb.find("m:sheets", _NS)
    chosen = None
    for s in sheets:
        name = s.get("name", "")
        if sheet is None and name.lower().startswith("totaal"):
            chosen = s
            break
        if sheet is not None and name == sheet:
            chosen = s
            break
    if chosen is None:
        if sheet is not None:
            raise SystemExit(f"Sheet {sheet!r} not found; sheets: {[s.get('name') for s in sheets]}")
        chosen = sheets[0]
    target = rid_to_target[chosen.get(f"{{{_NS['r']}}}id")]
    target = target.lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target
    return chosen.get("name", ""), target


def read_xlsx_rows(path: str, sheet: str | None = None):
    """Yield (sheet_name, rows) where rows is an iterator of lists of strings."""
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(f"{{{_NS['m']}}}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{_NS['m']}}}t")))
        name, part = _sheet_part(z, sheet)
        data = z.read(part)

    def rows():
        tag_row = f"{{{_NS['m']}}}row"
        tag_c = f"{{{_NS['m']}}}c"
        tag_v = f"{{{_NS['m']}}}v"
        tag_is = f"{{{_NS['m']}}}is"
        for _, el in ET.iterparse(io.BytesIO(data), events=("end",)):
            if el.tag != tag_row:
                continue
            row: list[str] = []
            for c in el.findall(tag_c):
                idx = _col_index(c.get("r", ""))
                t = c.get("t", "")
                if t == "s":
                    v = c.find(tag_v)
                    val = shared[int(v.text)] if v is not None and v.text else ""
                elif t == "inlineStr":
                    is_ = c.find(tag_is)
                    val = "".join(x.text or "" for x in is_.iter(f"{{{_NS['m']}}}t")) if is_ is not None else ""
                else:
                    v = c.find(tag_v)
                    val = v.text if v is not None and v.text is not None else ""
                    if val.endswith(".0"):
                        val = val[:-2]
                while len(row) <= idx:
                    row.append("")
                row[idx] = val.strip()
            el.clear()
            yield row

    return name, rows()


# --- header resolution and row parsing --------------------------------------
def _find_header(rows) -> tuple[list[str], list[list[str]]]:
    buffered: list[list[str]] = []
    for row in rows:
        lowered = [c.lower() for c in row]
        if any(h in HEADER_ALIASES["code"] for h in lowered):
            return row, list(rows)
        buffered.append(row)
        if len(buffered) > 10:
            break
    raise SystemExit("No header row with a referentiecode column found in the first 10 rows.")


def _resolve(header: list[str], overrides: dict[str, str]) -> dict:
    lowered = [h.strip().lower() for h in header]
    idx: dict[str, int] = {}
    for name, aliases in HEADER_ALIASES.items():
        want = (overrides.get(name) or "").strip().lower()
        if want and want in lowered:
            idx[name] = lowered.index(want)
            continue
        for alias in aliases:
            if alias in lowered:
                idx[name] = lowered.index(alias)
                break
    if "code" not in idx:
        raise SystemExit(f"No referentiecode column. Headers: {header}. Use --col-code.")
    # Official layout: choose columns sit before "Inactief", drop columns after it.
    inactief = lowered.index("inactief") if "inactief" in lowered else None
    choose: dict[str, int] = {}
    drop: dict[str, int] = {}
    gbned: dict[str, int] = {}
    for i, h in enumerate(lowered):
        if not h or i == idx["code"]:
            continue
        if inactief is not None:
            if i < inactief and h in CHOOSE_COLUMNS:
                choose["uitgebr" if h == "uitgebreid" else h] = i
            elif i > inactief and h not in HEADER_ALIASES["desc"]:
                drop[h] = i
        elif h in GBNED_ENTITY_COLUMNS:
            gbned["sv" if h == "svc" else h] = i
    return {"idx": idx, "choose": choose, "drop": drop, "gbned": gbned, "official": inactief is not None}


def _truthy(v: str) -> bool:
    return v.strip().lower() in {"1", "j", "ja", "x", "true", "y"}


def _row_to_account(row: list[str], res: dict) -> RgsAccount | None:
    idx = res["idx"]

    def get(name: str) -> str:
        i = idx.get(name)
        return row[i].strip() if i is not None and i < len(row) else ""

    def cell(i: int) -> str:
        return row[i].strip() if i < len(row) else ""

    code = get("code")
    # The official workbook holds a few irregular codes (`BLimBanRbaBg10`,
    # `BIvaAIk`, `BproOnpPrp`); accept any B/W token rather than a strict
    # Xxx grammar, so no real code is silently dropped.
    if not code or not re.fullmatch(r"[BW][A-Za-z0-9]*", code):
        return None
    status = get("inactief").strip().lower()
    inactive = _truthy(status) or any(w in status for w in ("inactief", "vervallen", "expired"))
    acc = RgsAccount(
        code=code, desc=get("desc"), desc_short=get("desc_short"), nummer=get("nummer"),
        nivo=get("nivo"), dc=get("dc").upper(), omslag=get("omslag"), sortering=get("sortering"),
        inactive=inactive,
        choose={k: _truthy(cell(i)) for k, i in res["choose"].items()},
        drop={k: _truthy(cell(i)) for k, i in res["drop"].items()},
        gbned={k: cell(i).upper() for k, i in res["gbned"].items()},
    )
    if not acc.nivo and acc.code:
        acc.nivo = str(1 + (len(acc.code) - 1) // 3)
    return acc


def load_csv(path: str, overrides: dict[str, str]) -> dict[str, RgsAccount]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        delim = ";" if sample.count(";") >= sample.count(",") else ","
        if sample.count("\t") > max(sample.count(";"), sample.count(",")):
            delim = "\t"
        rows = list(csv.reader(fh, delimiter=delim))
    header, body = _find_header(iter(rows))
    res = _resolve(header, overrides)
    out: dict[str, RgsAccount] = {}
    for row in body:
        acc = _row_to_account(row, res)
        if acc:
            out[acc.code] = acc
    return out


def load_xlsx(path: str, overrides: dict[str, str], sheet: str | None) -> tuple[str, dict[str, RgsAccount]]:
    name, rows = read_xlsx_rows(path, sheet)
    header, body = _find_header(rows)
    res = _resolve(header, overrides)
    out: dict[str, RgsAccount] = {}
    for row in body:
        acc = _row_to_account(row, res)
        if acc:
            out[acc.code] = acc
    return name, out


def cached_workbook() -> Path | None:
    for version in ("3.8", "3.9a"):
        p = CACHE_DIR / f"RGS-{version}.xlsx"
        if p.is_file():
            return p
    return None


def load_rgs(path: str | None, overrides: dict[str, str], sheet: str | None) -> tuple[dict[str, RgsAccount], str]:
    """Return (accounts_by_code, source_label)."""
    if not path:
        cached = cached_workbook()
        if cached:
            path = str(cached)
        else:
            return load_seed(), "seed"
    if path.lower().endswith((".xlsx", ".xlsm")):
        name, db = load_xlsx(path, overrides, sheet)
        return db, f"{path} [{name}]"
    return load_csv(path, overrides), path


def fetch(version: str) -> Path:
    url = OFFICIAL_URLS.get(version)
    if not url:
        raise SystemExit(f"Unknown version {version!r}; known: {', '.join(OFFICIAL_URLS)}")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    dest = CACHE_DIR / f"RGS-{version}.xlsx"
    req = urllib.request.Request(url, headers={"User-Agent": "rgs-skill lookup/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
            fh.write(resp.read())
    except Exception as exc:  # noqa: BLE001 - report the URL, whatever failed
        raise SystemExit(f"Download failed for {url}: {exc}") from exc
    if not zipfile.is_zipfile(dest):
        dest.unlink(missing_ok=True)
        raise SystemExit(f"{url} did not return an .xlsx file; check the Kennisbank at https://www.referentiegrootboekschema.nl/kbase")
    return dest


# --- entity filtering ---------------------------------------------------------
def applies(acc: RgsAccount, entity: str | None, basis: bool, keep: set[str]) -> bool:
    if acc.inactive:
        return False
    if not entity and not acc.choose and not acc.gbned:
        return True
    if acc.gbned:  # GBNED layout: J / J+ / P mean applicable
        if not entity:
            return True
        e = entity.lower()
        if e not in acc.gbned:
            raise SystemExit(f"Unknown entity {entity!r}; choose from {ENTITY_HELP}")
        return acc.gbned[e].upper() in {"J", "J+", "P"}
    if not acc.choose and not acc.drop:
        return True
    e = (entity or "").lower()
    if e in ("", "bv", "sv"):
        selected = acc.choose.get("basis", False) if basis else acc.choose.get("uitgebr", False)
    elif e == "ez":
        selected = acc.choose.get("ez/vof", False)
    elif e == "zzp":
        selected = acc.choose.get("zzp", False)
    elif e == "woco":
        selected = acc.choose.get("woco", False)
    elif e == "zorg":
        selected = acc.choose.get("zorg", False)
    else:
        raise SystemExit(f"Unknown entity {entity!r}; choose from {ENTITY_HELP}")
    if not selected:
        return False
    if not e:
        return True
    drops = set(SECTOR_DROPS) - keep
    if e == "woco":
        drops.discard("woco")
    if e == "zorg":
        drops.discard("zorg")
    if e == "bv":
        drops.add("ez/vof")
    elif e in ("ez", "zzp"):
        drops.add("bv")
    elif e == "sv":
        drops |= {"ez/vof", "bv"}
        drops.discard("ozw-coop-sticht-fwo")
    return not any(acc.drop.get(d, False) for d in drops)


# --- operations ---------------------------------------------------------------
def op_validate(db: dict[str, RgsAccount], code: str, as_json: bool) -> int:
    acc = db.get(code)
    if not acc:
        print(json.dumps({"code": code, "found": False}) if as_json else f"NOT FOUND: {code} is not in this dataset. Do not book to it; look it up in the official workbook.")
        return 1
    if acc.inactive:
        print(json.dumps({**acc.as_dict(), "found": True, "valid": False}) if as_json else f"INACTIVE: {code} is retired.\n{acc.fmt(db)}")
        return 2
    print(json.dumps({**acc.as_dict(), "found": True, "valid": True}) if as_json else f"VALID: {code}\n{acc.fmt(db)}")
    return 0


def op_lookup(db: dict[str, RgsAccount], code: str, as_json: bool) -> int:
    acc = db.get(code) or next((v for k, v in db.items() if k.lower() == code.lower()), None)
    if not acc:
        print(json.dumps({"code": code, "found": False}) if as_json else f"NOT FOUND: {code}")
        return 1
    print(json.dumps(acc.as_dict()) if as_json else acc.fmt(db))
    return 0


def op_children(db: dict[str, RgsAccount], code: str, as_json: bool) -> int:
    kids = sorted((a for a in db.values() if a.parent == code), key=lambda a: a.code)
    if not kids:
        print(json.dumps([]) if as_json else f"No children of {code} in this dataset.")
        return 1
    if as_json:
        print(json.dumps([a.as_dict() for a in kids]))
    else:
        for a in kids:
            print(a.fmt(db))
    return 0


def op_search(db: dict[str, RgsAccount], term: str, entity: str | None, nivo: str | None,
              basis: bool, keep: set[str], limit: int, as_json: bool) -> int:
    needles = [t.lower() for t in term.split()]
    hits = []
    for acc in db.values():
        hay = f"{acc.desc} {acc.desc_short} {acc.code}".lower()
        if not all(n in hay for n in needles):
            continue
        if nivo and acc.nivo and acc.nivo != nivo:
            continue
        if not applies(acc, entity, basis, keep):
            continue
        hits.append(acc)
    hits.sort(key=lambda a: (a.nivo or "9", a.code))
    if not hits:
        print(json.dumps([]) if as_json else f"No matches for {term!r}" + (f" (entity={entity})" if entity else "") + (f" (nivo={nivo})" if nivo else "") + ".")
        return 1
    if as_json:
        print(json.dumps([a.as_dict() for a in hits[:limit]]))
    else:
        for acc in hits[:limit]:
            print(acc.fmt(db))
            print()
        if len(hits) > limit:
            print(f"... {len(hits) - limit} more; raise --limit.")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", help="Official workbook (.xlsx) or a CSV/TSV export. Default: the cached workbook, else the seed.")
    p.add_argument("--sheet", help="Worksheet for .xlsx (default: the sheet whose name starts with 'Totaal').")
    p.add_argument("--list-sheets", action="store_true", help="Print the sheet names of --file and exit.")
    p.add_argument("--fetch", metavar="VERSION", help=f"Download the official workbook into {CACHE_DIR} ({', '.join(OFFICIAL_URLS)}).")
    p.add_argument("--validate", metavar="CODE", help="Exit 0 if CODE exists and is active, 1 if unknown, 2 if inactive.")
    p.add_argument("--lookup", metavar="CODE", help="Show one code.")
    p.add_argument("--children", metavar="CODE", help="List the codes one level below CODE.")
    p.add_argument("--search", metavar="TERMS", help="All terms must occur in the description or code.")
    p.add_argument("--entity", help=f"Filter to codes applicable to an entity: {ENTITY_HELP}.")
    p.add_argument("--uitgebreid", action="store_true", help="Select from the Uitgebreid column instead of Basis (official layout).")
    p.add_argument("--keep", default="", help="Comma-separated sector drop columns to keep despite --entity (e.g. agro,wkr).")
    p.add_argument("--nivo", help="Restrict to a level (4 = grootboekrekening).")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--json", action="store_true", help="Machine-readable output.")
    for f in ("code", "desc", "nummer", "nivo", "dc", "omslag", "inactief"):
        p.add_argument(f"--col-{f}", help=f"Override the header used for '{f}'.")
    args = p.parse_args(argv)

    if args.fetch:
        dest = fetch(args.fetch)
        print(f"Saved {dest} ({dest.stat().st_size} bytes) from {OFFICIAL_URLS[args.fetch]}", file=sys.stderr)
        if not (args.validate or args.lookup or args.search or args.children):
            return 0
        if not args.file:
            args.file = str(dest)
    if args.list_sheets:
        if not args.file:
            return _usage(p, "--list-sheets needs --file")
        print("\n".join(xlsx_sheet_names(args.file)))
        return 0

    overrides = {f: getattr(args, f"col_{f}") for f in ("code", "desc", "nummer", "nivo", "dc", "omslag", "inactief")}
    db, source = load_rgs(args.file, overrides, args.sheet)
    if source == "seed":
        print("(i) Using the built-in seed (a few dozen codes verified against RGS 3.8). Not the standard: run --fetch 3.8 for real work.", file=sys.stderr)
    else:
        print(f"Loaded {len(db)} codes from {source}.", file=sys.stderr)
    keep = {k.strip().lower() for k in args.keep.split(",") if k.strip()}
    basis = not args.uitgebreid

    if args.validate:
        return op_validate(db, args.validate, args.json)
    if args.lookup:
        return op_lookup(db, args.lookup, args.json)
    if args.children:
        return op_children(db, args.children, args.json)
    if args.search:
        return op_search(db, args.search, args.entity, args.nivo, basis, keep, args.limit, args.json)
    p.print_help()
    return 0


def _usage(p: argparse.ArgumentParser, msg: str) -> int:
    print(f"error: {msg}", file=sys.stderr)
    p.print_usage(sys.stderr)
    return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
