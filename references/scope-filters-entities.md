# RGS scope: filters, entity types & right-sizing ("RGS op maat")

> Full RGS is ~4,977 codes. You never use all of it. This file is how you pick the
> relevant subset for a given entity — for a typical Dutch BV that means the
> **BV (micro/klein)** selection at niveau 4.

## Why subset, and the three mechanisms

Full RGS is huge; RGS MKB (the practitioner subset) is roughly **20%** of it so you
"don't lose the forest for the trees." Subsetting works three ways:

1. **Hierarchy level** — small entities only need through **niveau 4** (~800 lines at
   the simplest granularity). Skip niveau-5 mutaties.
2. **Filters (kolommen)** — the master Excel has filter columns that either *include*
   ("Nieuw te kiezen bij") or *suppress* ("Te vervallen bij") codes per group/branche.
   This is the primary subsetting mechanism in the official schema.
3. **Extensions** (extensiecode at pos 9) — in practice branche extensions are almost
   never used; the standard added sector codes (e.g. WoCo's ~800) directly instead.

## Two parallel filter systems — don't conflate them

- **Official SBR RGS filters** (referentiegrootboekschema.nl) — driven by SBR reporting
  **entrypoints**. One filter per reporting endpoint: Micro/Klein/Middelgroot/Groot
  (each "inrichting" + "publicatie"), Belastingdienst (OB/ICP/IB/VpB), Banken
  ("Inrichting" / "Inrichting Beperkt NP"), Woningcorporaties, SBR Wonen, and (since
  3.7) split filters for Fondsenwervende organisaties / Stichtingen / Coöperaties /
  Organisaties zonder winststreven (OZW). RGS 3.7 logged 38 filter changes — filters are
  actively versioned.
- **RGS MKB entity columns** (GBNED/boekhoudplaza) — a curated practitioner selection
  with simple ZZP/EZ/BV/SV columns and a decimal account number. **RGS MKB is not the
  formal standard** — it's a documented subset by Onderzoeksbureau GBNED (now with NOAB).

### RGS MKB entity-type columns (values: `J` basis, `P`/`J+` uitgebreid, `N` not assigned)

| Column | Entity meaning |
|---|---|
| **ZZP** | Zelfstandige zonder personeel (sole trader, no staff) |
| **EZ** | Eenmanszaak + VOF / Maatschap |
| **BV** | Besloten Vennootschap (and NV) — scoped to **Micro + Klein** |
| **SV** | Stichting / Vereniging (+ Coöperatie), small |
| **Branche** | Marks an account specific to one branche |
| **Uitgebreid** | Optional/less-common account within the entity's set |

Example: "Bank" is `J` for all entity types; "Aandelen beursgenoteerd" is BV + uitgebreid
(`J+`) because it's less common.

## Sector / branche schemas (governance)

| Sector | Governing body | In RGS | Status |
|---|---|---|---|
| **Woningcorporaties (WoCo)** | Aedes + SBR Wonen (BZK) / Aw / WSW | ~654–800 codes added into standard RGS (since 3.1); WoCo filter (3.3); dedicated tab; **excluded from RGS MKB** | Mature |
| **Banken / bancair** | SBR Nexus (ex-FRC: ABN/ING/Rabo) | Banken filters; maps to Bankentaxonomie **FT20**; delivered via BIV (not Digipoort) | Mature |
| **Onderwijs** | OCW / DUO | Via OCW Taxonomie (NT20) entrypoints, not a single RGS filter | Mature (separate domain) |
| **Agrarisch / Agro** | Historically VLB + LEI/WUR ("GRAS" 1987) | Agro filter + ~125 codes branche-flagged (~90 also in RGS MKB) | Maintained via filter |
| **Zorg** | Werkgroep RGS Zorg (+ VWS, ZiN, NZa, CBS) | New **RGS 3.8 Zorg** beta (Nov 2025); vendor adoption pending | New / emerging |
| **Gemeenten** | — (use BBV/IV3, separate) | **No dedicated RGS schema** | Out of scope |
| **Pensioenfondsen** | — (report to DNB separately) | **No dedicated RGS schema** | Out of scope |
| **Bouw / Horeca / Detailhandel** | — | Decimal ranges reserved in RGS MKB but largely unfilled | Reserved only |

Be precise: Onderwijs and Zorg are reporting *domains* (NT entrypoints), not simple
filter columns like WoCo. Gemeenten and pensioenfondsen have **no** RGS sector schema —
don't invent one.

## The practical subset for a Dutch MKB BV

Use **RGS MKB, filter = "BV (Micro en klein)", through niveau 4, excluding branche/WoCo
codes and level-5 mutaties.**

- Start from the `J` (basis) BV accounts; add `J+` (uitgebreid) accounts only as the
  business actually needs them (e.g. specific financial instruments).
- Size is on the order of ~500–600 codes — manageable as a working chart of accounts.
- **Exclude** WoCo (~800), Agro (~125), other branche-flagged codes (use the "Alleen
  standaard RGS codes" branche filter); skip niveau-5 mutaties.
- **Couple at niveau 4** even where some reports only need level 2–3 — future-proofs
  benchmarking/kengetallen.
- **Equity:** a BV uses `BEiv` share capital + reserves (`BEivAan…`), **not** the
  `BEivKap…` privé accounts (those are EZ/VOF/maatschap). See `structure-and-codes.md`.
- Core hoofdrubrieken a BV touches — Balans: `BIva BMva BFva BVrd BVor BLim` (assets),
  `BEiv BVrz BLas BSch` (equity/liabilities). W&V: `WOmz WKpr WPer WAfs WBed WFbe WBel WNer`.

For a brand-new BV, the cleanest route is to **use RGS codes directly as the chart of
accounts** from day one — uniform and benchmark-ready with zero migration. In MoneyBird
that means adding categories from the standard collections (which auto-attach the RGS
code) rather than inventing custom categories. See `software-and-moneybird.md`.

## Legal size categories (micro / klein / middelgroot / groot)

Size classes come from **Titel 9, Boek 2 BW** (micro 2:395a, klein 2:396, middelgroot
2:397, groot above). A rechtspersoon falls in a class when it meets **≥2 of 3 criteria**
on **two consecutive balance dates**. RGS connects via the SBR entrypoints (each KvK/NT
entrypoint is per class, "inrichting" + "publicatie").

**Current thresholds** (raised ~25% for inflation; mandatory for boekjaren starting on/
after 1 Jan 2024; Staatsblad 2024,52):

| Regime | Balanstotaal | Netto-omzet | Werknemers (fte) | Consequence |
|---|---|---|---|---|
| **Micro** | ≤ €450k | ≤ €900k | < 10 | Minimal balance; no audit/bestuursverslag |
| **Klein** | ≤ €7.5m | ≤ €15m | < 50 | Verkorte balans + beperkte toelichting; W&V not published; no audit |
| **Middelgroot** | ≤ €25m | ≤ €50m | < 250 | Fuller balance + W&V + bestuursverslag; **audit required** |
| **Groot** | > €25m | > €50m | ≥ 250 | Full jaarrekening; audit required |

(Pre-2024 thresholds — micro €350k/€700k, klein €6m/€12m, middelgroot €20m/€40m — still
appear in older sources; don't use them for boekjaar 2024+.) RGS MKB's BV column targets
**micro + klein**; a middelgroot/groot BV needs standard-RGS codes beyond the MKB subset.
Size categories apply under **Dutch GAAP only**, not IFRS.

> KvK filing note: since **boekjaar 2025**, even **groot** entities must file the
> jaarrekening via SBR/iXBRL (the old large-company exception lapsed). See
> `reporting-compliance.md`.

## Tooling for right-sizing

- **boekhoudplaza "Decimaal rekeningschema RGS MKB"** — interactive selector (Filter:
  ZZP / EZ-VOF / BV micro+klein / SV / MKB alles / ALLE RGS; Branche: standaard / Agro /
  Bouw / WoCo) producing a right-sized decimal chart + CSV/Excel/JSON.
- **boekhoudplaza "RGS SBR rapportages"** — same filters mapped to specific SBR reports.
- **RGS Brugstaat** — export your own ledger with RGS codes to check conformity.
- **rgsready.nl / softwarepakketten.nl** — check a package's RGS support/readiness.
- The official master **Excel** ships ready-made MKB and WoCo tabs.
