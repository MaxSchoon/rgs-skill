"""Unit tests for scripts/rgs_lookup.py, with a generated workbook fixture.

The fixture reproduces the official layout (title row, header row with the
"te kiezen" and "te vervallen" column groups, duplicate EZ/VOF and WoCo
headers) so the filter semantics the references describe are what the script
implements. Standard library only.
"""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import rgs_lookup  # noqa: E402

HEADER = ["Referentiecode", "ReferentieOmslagcode", "Sortering", "Referentienummer",
          "Omschrijving (verkort)", "Omschrijving", "D/C", "Nivo",
          "Basis", "Uitgebr", "EZ/VOF", "ZZP", "WoCo",
          "Inactief", "BB", "Agro", "WKR", "EZ/VOF", "BV", "WoCo", "Bank",
          "OZW-Coop-Sticht-FWO", "Afrek syst", "Nivo5", "Uitbr5"]

# code, omslag, sort, nr, short, desc, dc, nivo, basis, uitg, ezvof, zzp, woco, inact, bb, agro, wkr, ezvof-drop, bv-drop, woco-drop, bank, ozw, afrek, nivo5, uitbr5
ROWS = [
    ["B", "", "", "", "BALANS", "BALANS", "", 1, 1, 1, 1, 1, 1, "", "", "", "", "", "", "", "", "", "", "", ""],
    ["BEiv", "", "A", "05", "Eigen vermogen", "Groepsvermogen - Eigen vermogen - Kapitaal", "C", 2, 1, 1, 1, 1, 1, "", "", "", "", "", "", "", "", "", "", "", ""],
    ["BEivGok", "", "A", "0501000", "Aandelenkapitaal", "Aandelenkapitaal", "C", 3, 1, 1, "", "", "", "", "", "", "", "", 1, "", "", "", "", "", ""],
    ["BEivGokGea", "", "A", "0501010", "Normale aandelen", "Normale aandelen aandelenkapitaal", "C", 4, 1, 1, "", "", "", "", "", "", "", "", 1, "", "", "", "", "", ""],
    ["BEivKap", "", "A", "509000", "Kapitaal NP", "Eigen vermogen onderneming natuurlijke personen", "C", 3, 1, 1, 1, 1, "", "", "", "", "", 1, "", "", "", "", "", "", ""],
    ["BEivKapPrs", "", "A", "0509010", "Privé-stortingen", "Privé-stortingen", "C", 4, 1, 1, 1, 1, "", "", "", "", "", 1, "", "", "", "", "", "", ""],
    ["BLimBanRba", "BSchSakRba", "B", "1002010", "RC bank", "Rekening-courant bank tegoeden bij banken", "D", 4, 1, 1, 1, 1, 1, "", "", "", "", "", "", "", "", "", 1, "", ""],
    ["BSchSakRba", "BLimBanRba", "C", "1206010", "RC kredietinst.", "Rekening-courant bij kredietinstellingen", "C", 4, 1, 1, 1, 1, 1, "", "", "", "", "", "", "", "", "", "", "", ""],
    ["WBedKanKoa", "", "K", "4206110", "Automatisering", "Kosten automatisering kantoorkosten", "D", 4, 1, 1, 1, "", 1, "", "", "", "", "", "", "", "", "", "", "", ""],
    ["WBedAgrOve", "", "K", "4299010", "Agro overig", "Overige agrarische kosten", "D", 4, "", 1, 1, "", "", "", "", 1, "", "", "", "", "", "", "", "", ""],
    ["BIvaKouCuh", "", "A", "0101030", "Cum. herwaard.", "Cumulatieve herwaarderingen kosten van oprichting", "D", 4, 1, 1, "", "", "", 1, "", "", "", "", 1, "", "", "", "", "", ""],
    ["BLimBanRbaBeg", "", "B", "1002010.01", "Beginbalans", "Beginbalans RC bank", "D", 5, 1, 1, 1, 1, 1, "", 1, "", "", "", "", "", "", "", "", 1, ""],
]


def _cell(ref: str, value, shared: list[str]) -> str:
    if value == "" or value is None:
        return ""
    if isinstance(value, (int, float)):
        return f'<c r="{ref}"><v>{value}</v></c>'
    if value not in shared:
        shared.append(value)
    return f'<c r="{ref}" t="s"><v>{shared.index(value)}</v></c>'


def _col(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def build_xlsx(path: Path, sheet_name: str = "Totaal-RGS3.8-def") -> None:
    shared: list[str] = []
    rows_xml = []
    all_rows = [["RGS3.8"] + [""] * 7 + ["Filter  - te kiezen bij aard"] + [""] * 4 + ["Filters - te vervallen c.q. "]] + [HEADER] + ROWS
    for r_i, row in enumerate(all_rows, start=1):
        cells = "".join(_cell(f"{_col(c_i)}{r_i}", v, shared) for c_i, v in enumerate(row))
        rows_xml.append(f'<row r="{r_i}">{cells}</row>')
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    sheet = f'<?xml version="1.0" encoding="UTF-8"?><worksheet {ns}><sheetData>{"".join(rows_xml)}</sheetData></worksheet>'
    sst = f'<?xml version="1.0" encoding="UTF-8"?><sst {ns} count="{len(shared)}" uniqueCount="{len(shared)}">' + "".join(f"<si><t>{s}</t></si>" for s in shared) + "</sst>"
    workbook = (f'<?xml version="1.0" encoding="UTF-8"?><workbook {ns} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f'<sheets><sheet name="Recap" sheetId="1" r:id="rId1"/><sheet name="{sheet_name}" sheetId="2" r:id="rId2"/></sheets></workbook>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>')
    recap = f'<?xml version="1.0" encoding="UTF-8"?><worksheet {ns}><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>Bijgaand de definitieve versie</t></is></c></row></sheetData></worksheet>'
    content_types = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                     '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/></Types>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", rels)
        z.writestr("xl/sharedStrings.xml", sst)
        z.writestr("xl/worksheets/sheet1.xml", recap)
        z.writestr("xl/worksheets/sheet2.xml", sheet)


def run(argv: list[str]) -> tuple[int, str]:
    out = io.StringIO()
    with redirect_stdout(out), redirect_stderr(io.StringIO()):
        code = rgs_lookup.main(argv)
    return code, out.getvalue()


class WorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.xlsx = Path(cls.tmp.name) / "fixture.xlsx"
        build_xlsx(cls.xlsx)
        cls.db = rgs_lookup.load_xlsx(str(cls.xlsx), {}, None)[1]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_reads_official_layout(self) -> None:
        self.assertEqual(rgs_lookup.xlsx_sheet_names(str(self.xlsx)), ["Recap", "Totaal-RGS3.8-def"])
        acc = self.db["BLimBanRba"]
        self.assertEqual(acc.nivo, "4")
        self.assertEqual(acc.dc, "D")
        self.assertEqual(acc.omslag, "BSchSakRba")
        self.assertEqual(acc.nummer, "1002010")
        self.assertEqual(self.db["BLimBanRbaBeg"].nummer, "1002010.01")
        self.assertTrue(acc.choose["basis"] and acc.choose["zzp"])
        self.assertTrue(acc.drop["afrek syst"])

    def test_duplicate_headers_split_into_choose_and_drop(self) -> None:
        kap = self.db["BEivKapPrs"]
        self.assertTrue(kap.choose["ez/vof"])       # first EZ/VOF column: selected for EZ/VOF
        self.assertTrue(kap.drop["ez/vof"])         # second EZ/VOF column: specific to EZ/VOF
        gok = self.db["BEivGokGea"]
        self.assertFalse(gok.choose["ez/vof"])
        self.assertTrue(gok.drop["bv"])             # specific to a BV

    def test_bv_keeps_share_capital_and_drops_prive(self) -> None:
        keep: set[str] = set()
        self.assertTrue(rgs_lookup.applies(self.db["BEivGokGea"], "bv", True, keep))
        self.assertFalse(rgs_lookup.applies(self.db["BEivKapPrs"], "bv", True, keep))
        self.assertFalse(rgs_lookup.applies(self.db["BEivGokGea"], "ez", True, keep))
        self.assertTrue(rgs_lookup.applies(self.db["BEivKapPrs"], "ez", True, keep))
        self.assertTrue(rgs_lookup.applies(self.db["BEivKapPrs"], "zzp", True, keep))

    def test_sector_drops_and_keep(self) -> None:
        agro = self.db["WBedAgrOve"]
        self.assertFalse(rgs_lookup.applies(agro, "bv", True, set()))          # not Basis
        self.assertFalse(rgs_lookup.applies(agro, "bv", False, set()))         # Uitgebreid but agro dropped
        self.assertTrue(rgs_lookup.applies(agro, "bv", False, {"agro"}))       # --keep agro

    def test_inactive_is_column_not_text(self) -> None:
        self.assertTrue(self.db["BIvaKouCuh"].inactive)
        self.assertFalse(self.db["BEivGokGea"].inactive)
        code, out = run(["--file", str(self.xlsx), "--validate", "BIvaKouCuh"])
        self.assertEqual(code, 2)
        self.assertIn("INACTIVE", out)

    def test_validate_exit_codes(self) -> None:
        self.assertEqual(run(["--file", str(self.xlsx), "--validate", "WBedKanKoa"])[0], 0)
        self.assertEqual(run(["--file", str(self.xlsx), "--validate", "WBedKanXyz"])[0], 1)

    def test_search_entity_and_level(self) -> None:
        code, out = run(["--file", str(self.xlsx), "--search", "rekening-courant", "--nivo", "4", "--entity", "bv", "--json"])
        self.assertEqual(code, 0)
        self.assertIn("BLimBanRba", out)
        self.assertIn("BSchSakRba", out)
        self.assertNotIn("BLimBanRbaBeg", out)

    def test_children_and_omslag_partner(self) -> None:
        code, out = run(["--file", str(self.xlsx), "--children", "BEivGok"])
        self.assertEqual(code, 0)
        self.assertIn("BEivGokGea", out)
        code, out = run(["--file", str(self.xlsx), "--lookup", "BLimBanRba"])
        self.assertIn("BSchSakRba", out)
        self.assertIn("kredietinstellingen", out)


class CsvAndSeedTests(unittest.TestCase):
    def test_gbned_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "mkb.csv"
            p.write_text("RGS-code;Omschrijving;Nivo;D/C;Omslagcode;ZZP;EZ;BV;SVC;RekNr\n"
                         "BVorDebHad;Debiteuren;4;D;;J;J;J;J;13011\n"
                         "BEivGokGea;Aandelenkapitaal;4;C;;N;N;J;N;05011\n", encoding="utf-8")
            db = rgs_lookup.load_csv(str(p), {})
            self.assertEqual(db["BVorDebHad"].gbned["bv"], "J")
            self.assertTrue(rgs_lookup.applies(db["BEivGokGea"], "bv", True, set()))
            self.assertTrue(rgs_lookup.applies(db["BEivGokGea"], "BV", True, set()))
            self.assertFalse(rgs_lookup.applies(db["BEivGokGea"], "zzp", True, set()))
            with self.assertRaises(SystemExit):
                rgs_lookup.applies(db["BEivGokGea"], "nv", True, set())

    def test_seed_is_used_without_cache(self) -> None:
        old = rgs_lookup.CACHE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            rgs_lookup.CACHE_DIR = Path(tmp)
            try:
                db, label = rgs_lookup.load_rgs(None, {}, None)
            finally:
                rgs_lookup.CACHE_DIR = old
        self.assertEqual(label, "seed")
        self.assertIn("WBedKanKoa", db)
        self.assertNotIn("BEivAan", db)
        self.assertEqual(db["BLimBanRba"].omslag, "BSchSakRba")

    def test_seed_codes_are_well_formed(self) -> None:
        for code, _, nivo, _, _ in rgs_lookup._SEED_ROWS:
            self.assertEqual(int(nivo), 1 + (len(code) - 1) // 3, code)

    def test_fetch_then_lookup_uses_downloaded_workbook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "RGS-3.9a.xlsx"
            build_xlsx(dest)
            old_fetch = rgs_lookup.fetch
            old_cache = rgs_lookup.CACHE_DIR
            rgs_lookup.CACHE_DIR = Path(tmp) / "cache"
            rgs_lookup.CACHE_DIR.mkdir()
            rgs_lookup.fetch = lambda _version: dest
            try:
                code, out = run(["--fetch", "3.9a", "--lookup", "BIvaKouCuh"])
            finally:
                rgs_lookup.fetch = old_fetch
                rgs_lookup.CACHE_DIR = old_cache
        self.assertEqual(code, 0)
        self.assertIn("BIvaKouCuh", out)


if __name__ == "__main__":
    unittest.main()
