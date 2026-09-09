---
reference_id: scope-filters-entities
verified_on: 2026-09-09
rgs_version: "3.8 definitive (2025-12-10); 3.9 alfa where stated"
---

# RGS scope: filters, entity types, and sectors

**Load this when:** you must decide which part of RGS an entity uses (a new
BV, a ZZP'er, an eenmanszaak or VOF, a stichting, a woningcorporatie, a care
institution), build a right-sized chart, or place an entity in a legal size
class.

**Do not load this when:** the code for one account is already known and the
question is its mechanics (`references/structure-and-codes.md`), or the
question is a filing (`references/reporting-compliance.md`).

## Contents

- [How the workbook subsets](#how-the-workbook-subsets)
- [Measured subset sizes](#measured-subset-sizes)
- [Recipe: a chart for a micro or small BV](#recipe-a-chart-for-a-micro-or-small-bv)
- [Recipe: ZZP, eenmanszaak, VOF](#recipe-zzp-eenmanszaak-vof)
- [RGS MKB and its decimal numbers](#rgs-mkb-and-its-decimal-numbers)
- [Sectors](#sectors)
- [Legal size classes](#legal-size-classes)
- [Sources](#sources)

## How the workbook subsets

Filters exist since RGS 3.0; a filter either suppresses codes ("te vervallen
bij") or selects them [S1]. The 3.8 Recap tab documents the two column groups
of the main sheet and how to combine them [S2]:

- **Choose by nature** (columns I-M): `Basis` 3,101 codes, `Uitgebreid` 4,039,
  `EZ/VOF` 2,421, `ZZP` 261, `WoCo` 1,875. Start from one of these.
- **Then eliminate** (columns N onward): `Inactief` 42, `BB` beginbalans
  posts 371, `Agro` 124, `WKR` werkkostenregeling 133, `EZ/VOF`-specific 194,
  **`BV`-specific 613**, `WoCo`-specific 858, `Bank` 96, `OZW-Coop-Sticht-FWO`
  197 (split into `OZW` 49, `Coop` 39, `Stichting` 19, `FWO` 90),
  `Afrek syst` 65, `Nivo5` 3,162, `Uitbr5` 616.

The Recap's own worked examples: Basis minus inactive minus level 5 leaves
1,331 codes; the whole sheet minus inactive, minus WoCo, minus the columns a
BV does not need (`Agro`, `WKR`, `Bank`, `OZW-Coop-Sticht-FWO`), minus level 5
leaves 1,373 [S2]. The 3.9 alfa adds a `Zorg` choose column (2,473) and a
`Zorg`-specific drop column (294) [S3].

Two consequences for an agent reading the sheet:

- The `BV` column is a drop column that marks the 613 codes *specific to* a
  BV (all of `BEivGok` aandelenkapitaal among them); an eenmanszaak or VOF
  removes it, a BV keeps it. Removing it for a BV deletes the share capital.
  The same holds for the second `EZ/VOF` column (194 codes specific to
  natural persons, the `BEivKap` family), which a BV removes [S2] [S4].
- The `MKB-RGS3.8-def` sheet is the owner's MKB selection (3,705 rows, 1,155
  at niveau 4) and already omits `Agro`, `WoCo`, `Bank` and the OZW columns
  [S4].

## Measured subset sizes

Counted on `Totaal-RGS3.8-def`, active codes only [S4]:

| Selection at niveau 4 | Codes |
|---|---|
| all active niveau-4 codes | 1,458 |
| `Basis` | 1,091 |
| `Uitgebreid` | 1,246 |
| `Basis`, minus the `EZ/VOF`-specific, `Agro`, `WKR`, `Bank`, `OZW-Coop-Sticht-FWO` and `WoCo`-specific drop columns (a BV) | 1,042 |
| `EZ/VOF` choose column, minus the `BV`-specific and sector drop columns | 928 |
| `ZZP` choose column, minus the `BV`-specific column | 173 |
| `WoCo` choose column | 722 |

GBNED's dashboard reports 124 agro codes, 861 wonen (WoCo) codes and 0 bouw
codes in 3.8 [S5]. Earlier editions of this skill put a BV chart at "500-600
codes"; the workbook does not support that number, and a working chart is
smaller than the selection only because a business uses a fraction of the
codes it is allowed to.

## Recipe: a chart for a micro or small BV

1. Start from `MKB-RGS3.8-def` (or `Totaal` with `Basis` = 1), niveau 4 only,
   `Inactief` empty [S2] [S4].
2. Drop the `EZ/VOF`-specific column (privé equity of natural persons) and
   the sector columns you do not need (`Agro`, `WKR` if no werkkostenregeling
   bookkeeping, `Bank`, `OZW-Coop-Sticht-FWO`, `WoCo`); keep the `BV`
   column [S2].
3. Keep equity under `BEivGok` (aandelenkapitaal), `BEivAgi`, `BEivWer`,
   `BEivStr`, `BEivOvr`, `BEivOre`; the `BEivKap…` family is for natural
   persons [S4].
4. Add `Uitgebreid`-only codes when the business needs them (financial
   instruments, specific reserves), one at a time.
5. Give every own account exactly one code and keep the omslag pairs
   together (`references/structure-and-codes.md`).

For a brand-new BV the cheapest path is to use the codes as the chart from day
one; in MoneyBird the standard collections attach the code automatically
(`references/software-and-moneybird.md`).

## Recipe: ZZP, eenmanszaak, VOF

Use the `ZZP` or `EZ/VOF` choose column (173 and 928 niveau-4 codes after
dropping the BV-specific and sector columns) [S4].
Equity is `BEivKap` (ondernemingsvermogen, privé-stortingen, privé-opnamen,
privé-belastingen) and, for a VOF, `BEivKa2` to `BEivKa5` for the second to
fifth firmant [S4]. Drop the `BV`-specific column [S2].

## RGS MKB and its decimal numbers

GBNED's RGS MKB targets ZZP, eenmanszaak/VOF, BV micro and klein, and small
stichtingen and verenigingen, keeps codes through niveau 4, leaves out
woningcorporatie codes, and gives every code a 5-digit decimal account number
because the official referentienummer "blijkt niet consequent bijgehouden":
`BVorDebHad` Debiteuren is `13011`; own sub-accounts get a sixth digit
(`130110`, `130111` Debiteuren binnenland) that still map to the one code
[S6] [S7]. The standard owner describes RGS MKB as the subset of codes with
the MKB filter, with examples and documentation, and encourages such filters
[S8]. Use it as a starting chart; it is not a version of the standard.

## Sectors

| Sector | In RGS 3.8 | Governance and route |
|---|---|---|
| Woningcorporaties | `WoCo` choose column (1,875) and a `WoCo-RGS3.8-def` sheet; excluded from RGS MKB | tab credited to the RGS Beheergroep WoCo; SBR Wonen dVi entrypoints in the RGS Taxonomie [S2] [S9] |
| Zorg | `Zorg-RGS3.8-beta` sheet; a `Zorg` column in the 3.9 alfa main sheet | werkgroep RGS Zorg (SureSync-led); vendor adoption pending [S3] [S10] |
| Agrarisch | `Agro` drop column, 124 codes | filter only [S2] [S5] |
| Banken (credit reporting) | `Bank` drop column, 96 codes; RGS Taxonomie maps to three FRC jaarrekening entrypoints | SBR Nexus / FT taxonomy [S2] [S9] |
| Stichting, vereniging, coöperatie, fondsenwervend, OZW | `OZW-Coop-Sticht-FWO` and its four split columns | KvK NT20 has separate entrypoints for stichtingen, coöperaties, OZW and fondsenwervende organisaties [S2] [S11] |
| Onderwijs, pensioenfondsen, gemeenten | no RGS column or tab; KvK NT20 has entrypoints for pensioenfondsen and premiepensioeninstellingen that the RGS Taxonomie does not map | out of RGS scope [S9] [S11] |

## Legal size classes

Titel 9 Boek 2 BW sizes an entity by balance total, net turnover and
employees; it falls in a class when it meets two of the three for two
consecutive financial years [S12] [S13]. The amounts were raised 25 percent
for inflation by the Implementatiebesluit Richtlijn verhoging grensbedragen
(Stb. 2024, 52), mandatory for financial years starting on or after
2024-01-01 and optional for 2023 [S13]:

| Class | Balance total | Net turnover | Employees | Before 2024 |
|---|---|---|---|---|
| Micro (art. 2:395a) | ≤ €450,000 | ≤ €900,000 | < 10 | €350,000 / €700,000 |
| Klein (art. 2:396) | ≤ €7.5 million | ≤ €15 million | < 50 | €6 million / €12 million |
| Middelgroot (art. 2:397) | ≤ €25 million | ≤ €50 million | < 250 | €20 million / €40 million |
| Groot | above those | above those | ≥ 250 | |

KvK's own table prints "> €51 mln" for groot turnover; the Besluit says €50
million [S12] [S13]. The class selects the KvK entrypoint
(`references/reporting-compliance.md`); RGS itself has no size column.

## Sources

- **[S1]** Filterfunctionaliteit toegevoegd. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/24/Filterfunctionaliteit_toegevoegd.htm> [viewed 2026-09-09]. Tier 2.
- **[S2]** RGS 3.8-def.xlsx, sheet `Recap` (filter columns, counts, worked examples). Taakgroep RGS, 2025-12-10. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx> [viewed 2026-09-09]. Tier 1.
- **[S3]** RGS 3.9-alfa.xlsx, sheets `Recap` and `Totaal-RGS3.9-alfa`. Taakgroep RGS, 2026-07-28. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.9-alfa.xlsx> [viewed 2026-09-09]. Tier 1.
- **[S4]** RGS 3.8-def.xlsx, sheets `Totaal-RGS3.8-def` and `MKB-RGS3.8-def`. Taakgroep RGS, 2025-12-10. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx>; counts measured with `scripts/rgs_lookup.py` [viewed 2026-09-09]. Tier 1.
- **[S5]** RGS Dashboard (Bouw, Agrarisch, Wonen counts). Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/cmm/rgs/rgs_dashboard.php> [viewed 2026-09-09]. Tier 2.
- **[S6]** Wat is RGS MKB. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/pag_epa/137/RGS_MKB.php> [viewed 2026-09-09]. Tier 2.
- **[S7]** RGS MKB als decimaal rekeningschema gebruiken binnen je eigen organisatie. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/40/RGS_MKB_decimaal_rekeningschema_toegelicht.htm> [viewed 2026-09-09]. Tier 2.
- **[S8]** RGS en RGS mkb: wat is het verschil? 2025-05-20. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/Actueel/rgs-en-rgs-mkb-wat-het-verschil> [viewed 2026-09-09]. Tier 1.
- **[S9]** NT20_RGS_20251210.zip, directory `www.nltaxonomie.nl/rgs/nt20/rgs/20251210/entrypoints/` (25 entrypoint schemas: 4 bd, 6 bzk, 3 frc, 12 kvk). Taakgroep RGS. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/NT20_RGS_20251210.zip> [viewed 2026-09-09]. Tier 1.
- **[S10]** RGS Zorg: een structuur die bruikbaar is voor het gehele zorgdomein, 2026-04-17. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/Actueel/rgs-zorg-een-structuur-die-bruikbaar-voor-het-gehele-zorgdomein> [viewed 2026-09-09]. Tier 1.
- **[S11]** Index of /nt20/kvk/20251210/entrypoints/ (27 KvK entrypoints). Logius, nltaxonomie.nl. Available from: <http://www.nltaxonomie.nl/nt20/kvk/20251210/entrypoints/> [viewed 2026-09-09]. Tier 1.
- **[S12]** In welke bedrijfsklasse valt je bedrijf? (updated 2026-01-14). KVK. Available from: <https://www.kvk.nl/deponeren/in-welke-bedrijfsklasse-valt-je-bedrijf/> [viewed 2026-09-09]. Tier 1.
- **[S13]** Staatsblad 2024, 52: Besluit van 5 maart 2024 tot verhoging van de grensbedragen, genoemd in de artikelen 395a, 396 en 397 van Boek 2 BW (Implementatiebesluit Richtlijn verhoging grensbedragen). Overheid.nl. Available from: <https://zoek.officielebekendmakingen.nl/stb-2024-52.html> [viewed 2026-09-09]. Tier 1.
