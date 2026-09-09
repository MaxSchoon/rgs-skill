---
reference_id: versions-governance
verified_on: 2026-09-09
rgs_version: "3.8 definitive (2025-12-10); 3.9 alfa (2026-07-28)"
---

# RGS versions, artifacts, and governance

**Load this when:** you must say which RGS version is current or authoritative,
where the workbook or taxonomy is published, who governs RGS, what RGS MKB or
RGS Ready are, or how to re-verify any of that.

**Do not load this when:** the question is which code to book to
(`references/structure-and-codes.md`) or which taxonomy a filing needs
(`references/reporting-compliance.md`); those files carry the version facts
they depend on.

## Contents

- [What RGS is](#what-rgs-is)
- [Current version and release calendar](#current-version-and-release-calendar)
- [Version history](#version-history)
- [The artifacts and where they live](#the-artifacts-and-where-they-live)
- [Governance](#governance)
- [RGS MKB, sector tabs, and RGS Ready](#rgs-mkb-sector-tabs-and-rgs-ready)
- [Re-verifying freshness](#re-verifying-freshness)
- [Sources](#sources)

## What RGS is

RGS (Referentie GrootboekSchema) is a reference classification of ledger
accounts: a fixed set of alphabetic reference codes, each with an example
number, a standard description, and where needed an omslagcode, that an
organisation maps its own ledger accounts onto. The official English page
positions it "explicitly as a reference classification and not as a mandatory
standard", says it contains all the ledgers required to report to the Dutch
government plus most used for internal reporting, and states that RGS "is
currently only available in Dutch" [S1]. It is one of the four SBR
taakgroep domains; the SBR governance document notes that no international
standard exists for it, so the Taakgroep RGS maintains a semantic standard
rather than an exchange format [S2]. The Belastingdienst supports RGS because
an RGS-coded administration lets it compare returns and run standard analyses
automatically when preparing an audit [S3].

## Current version and release calendar

| Item | Value | Source |
|---|---|---|
| Definitive standard | **RGS 3.8**, workbook `RGS 3.8-def.xlsx`, released 2025-12-10; based on NT20 and FT20 | [S4] [S5] |
| Matching taxonomy | `NT20_RGS_20251210.zip` (RGS Taxonomie 3.8), on the Kennisbank | [S6] |
| Review version | **RGS 3.9 alfa**, `RGS 3.9-alfa.xlsx`, released 2026-07-28, based on NT21 and FT21; described as small corrections with the core since 3.0 intact | [S7] [S8] |
| RGS 3.9 calendar | alfa 2026-07-17; bèta 2026-10-09; definitive 2026-12-11; RGS Taxonomie 3.9.b 2026-11-06; RGS Taxonomie 3.9 2027-01-15 (FT21 planning unknown when set, so subject to change) | [S9] |
| Cadence | one alfa, bèta and definitive version per year, following the yearly NT and bankentaxonomie changes | [S10] |

The 3.9 alfa news lists the changes as mostly descriptions, 17 omslagcodes
adjusted or removed, 4 sorteercodes and 1 referentienummer changed, D/C changed
on 6 codes, 8 new general codes (resultaatbestemming for bestemmingsfondsen and
bestemmingsreserves, schulden aan aandeelhouders), woningcorporatie changes, and
a split of the OZW-Coop-Sticht-FWO filters [S7]. The alfa workbook's own Recap
tab counts 50 new codes in total, 18 omslagcode changes, 81 text changes, and
42 inactive codes; its main sheet holds 5,307 rows against 4,980 in 3.8, mainly
because the RGS Zorg codes now sit in the main sheet with their own filter
column [S8].

## Version history

Cumulative code counts per definitive version, from the GBNED RGS Dashboard
[S11]; the 3.8 workbook's main sheet counts 4,980 rows including the two
niveau-1 roots [S5].

| Year | Version | Codes | Note |
|---|---|---|---|
| 2016 | 2.0 | 2,528 | |
| 2017 | 3.0 | 3,009 | core stable from here; the referentienummer stops being the sort key [S12] |
| 2018 | 3.1 | 3,754 | |
| 2019 | 3.2 | 3,858 | |
| 2020 | 3.3 | 4,574 | basis of the English-label dataset [S1] |
| 2021 | 3.4 | 4,641 | |
| 2022 | 3.5 | 4,740 | the version MoneyBird's API accepts (`references/software-and-moneybird.md`) |
| 2023 | 3.6 | 4,779 | |
| 2024 | 3.7 | 4,963 | |
| 2025 | 3.8 | 4,977 | current definitive; 14 new codes, 42 inactive, 16 omslag changes versus 3.7 [S5] |

Because the core has not changed since 3.0, everyday codes such as
`WBedAlkOal` or `BLimKasKas` resolve in 3.5 and 3.8 alike; what moves between
versions is descriptions, omslagcodes, filters, sector codes, and the
`Inactief` flag [S5] [S7].

## The artifacts and where they live

- **Kennisbank** (`https://www.referentiegrootboekschema.nl/kbase`): every
  alfa, bèta and definitive workbook since 3.0, the RGS Taxonomie zips, the
  mapping documents, and the explanatory pages [S13]. Files sit under
  `/sites/default/files/kennisbank/`; the 3.8 workbook is
  `RGS%203.8-def.xlsx` and the 3.9 alfa `RGS%203.9-alfa.xlsx` [S4] [S7].
- **Workbook layout** (3.8): sheets `Recap` (release notes and filter
  semantics), `Totaal-RGS3.8-def`, `RGS3.8-versus-RGS3.7` (the audit trail
  with one column per version 3.0 to 3.8), `MKB-RGS3.8-def`,
  `WoCo-RGS3.8-def`, `Zorg-RGS3.8-beta` [S5]. Column details are in
  `references/structure-and-codes.md`.
- **RGS Taxonomie**: XBRL, published on nltaxonomie.nl under `/rgs/`, which
  holds `nt11/` through `nt20/` and no `nt21/` yet [S14]; the zip and its
  toelichting are on the Kennisbank [S6] [S10].
- **English labels**: one dataset, `20210913 RGS NL en EN labels.xlsx`, based
  on RGS 3.3 and the NT15/FT15 labels, with the site's own disclaimer that it
  is not an official product and will not be periodically updated [S1] [S15].

## Governance

Since the SBR governance reorganisation, RGS is run by the **Taakgroep RGS**,
which sets the course, releases versions, and steers three werkgroepen:
**Semantiek** (content; assesses change requests and prepares versions),
**Techniek** (implementation and technical documentation), and
**Implementatie en Communicatie** (adoption and the website) [S16]. The SBR
governance document gives the taakgroep the publication of both forms of the
standard, the spreadsheet and the XBRL taxonomy, and says taakgroepen decide
by unanimity where possible and otherwise by a three-quarters qualified
majority with at least five voting participants [S2]. The SBR website's own
Taakgroep RGS page, by contrast, says the taakgroep is expressly not
responsible for producing the RGS taxonomie, which it treats as a separate
artefact domain; the two SBR texts disagree and both are cited here [S2]. Change requests go
through the RGS meldingsformulier; the 3.9 calendar page confirms the routing
(Werkgroep Semantiek prepares, the taakgroep decides on publication) [S9].

Two wordings persist on official pages and are not errors to "correct":
the RGS Taxonomie page still says the taxonomy "wordt onderhouden door de RGS
Beheergroep" [S10], and the workbook Recap credits the WoCo and Zorg tabs to
an "RGS Beheergroep WoCo" and "RGS Beheergroep Zorg" [S8]. Read "beheergroep"
as the working group under the taakgroep for that domain.

## RGS MKB, sector tabs, and RGS Ready

- **RGS MKB** is a derivative of RGS for micro and small entities: only the
  codes with the MKB filter, with examples and documentation, described by the
  standard owner as a subset that makes RGS easier to apply [S17]. The
  practitioner product of that name is maintained by Onderzoeksbureau GBNED on
  boekhoudplaza.nl: codes through niveau 4 only (no mutaties), woningcorporatie
  codes left out, a 5-digit decimal account number per code, documentation per
  account, and target groups ZZP, eenmanszaak/VOF, BV (micro and klein per the
  KvK classes), and small stichtingen and verenigingen; NOAB reviews its
  proposals [S18]. The official workbook also ships an `MKB-RGS3.8-def` sheet
  [S5]. Neither is a version number: there is no "RGS 4.0".
- **Sector tabs** in the official workbook: `WoCo` (woningcorporaties) and
  `Zorg` (RGS Zorg, a bèta in 3.8, in the main sheet from 3.9 alfa) [S5] [S8].
  RGS Zorg was developed by a werkgroep led from SureSync to give the care
  sector one future-proof chart; adoption depends on care-sector software
  vendors supporting it [S19].
- **RGS Ready** is not certification by the standard owner. It is a GBNED
  yardstick of eight functions (RGS schema available in the package, automatic
  updates, manual coupling, an automatic coupling proposal, propagation across
  administrations, RGS code and version in the XAF audit file, an overview per
  RGS code with unmapped-account control, and RGS codes in the package's API or
  koppelvlak), adopted as a normenkader by the former RGS Taskforce
  implementatie; vendors are tested by GBNED and listed with a test report
  [S20]. The official English page points to rgsready.nl for implementing
  software [S1].

## Re-verifying freshness

1. Read `https://www.referentiegrootboekschema.nl/actueel`; the newest item
   names the newest artifact [S21].
2. Confirm the file on the Kennisbank and, for the taxonomy, the directory
   under `https://www.nltaxonomie.nl/rgs/` [S13] [S14].
3. Read the SBR release calendar for the NT generation the version maps to
   (`references/reporting-compliance.md`).
4. Update the `rgs_version` front matter of every reference you touched and
   the `verified_on` date, with the URL viewed.

The next expected changes on 2026-09-09: RGS 3.9 bèta (2026-10-09), RGS 3.9
definitive (2026-12-11), RGS Taxonomie 3.9 (2027-01-15) [S9], and NT21 in
production (2026-12-09, `references/reporting-compliance.md`).

## Sources

- **[S1]** English. Referentie GrootboekSchema (Taakgroep RGS). Available from: <https://www.referentiegrootboekschema.nl/english> [viewed 2026-09-09]. Tier 1.
- **[S2]** SBR Afsprakenstelsel, deel 2: Governance, v1 (§ 2.3 Taakgroepen, § 2.3.4 Taakgroep RGS). SBR Nederland / Logius. Available from: <https://www.sbr-nl.nl/sites/default/files/bestanden/SBR_afsprakenstelsel_deel_2_governance_v1.pdf>; summary page <https://www.sbr-nl.nl/governance-overleggen/taakgroepen/taakgroep-rgs> [viewed 2026-09-09]. Tier 1.
- **[S3]** Referentie Grootboekschema: iets voor u? Belastingdienst. Available from: <https://www.belastingdienst.nl/wps/wcm/connect/nl/intermediairs/content/referentie-grootboekschema-iets-voor-u> [viewed 2026-09-09]. Tier 1.
- **[S4]** Definitieve versie RGS 3.8 (Kennisbank item, file `RGS 3.8-def.xlsx`, 2.39 MB) and the news item "Definitieve versie RGS 3.8 gepubliceerd", 2025-12-10. Available from: <https://www.referentiegrootboekschema.nl/definitieve-versie-rgs-38>, <https://www.referentiegrootboekschema.nl/Actueel/definitieve-versie-rgs-38-gepubliceerd> [viewed 2026-09-09]. Tier 1.
- **[S5]** RGS 3.8-def.xlsx, sheets `Recap` and `Totaal-RGS3.8-def`. Taakgroep RGS, 2025-12-10. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx> and measured with `scripts/rgs_lookup.py` [viewed 2026-09-09]. Tier 1.
- **[S6]** NT20_RGS_20251210 (Kennisbank item, zip 12.12 MB). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/nt20rgs20251210> [viewed 2026-09-09]. Tier 1.
- **[S7]** Alfaversie RGS 3.9 gepubliceerd, 2026-07-28, and the Kennisbank item `RGS 3.9-alfa.xlsx`. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/Actueel/alfaversie-rgs-39-gepubliceerd>, <https://www.referentiegrootboekschema.nl/alfaversie-rgs-39> [viewed 2026-09-09]. Tier 1.
- **[S8]** RGS 3.9-alfa.xlsx, sheets `Recap` and `Totaal-RGS3.9-alfa`. Taakgroep RGS, 2026-07-28. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.9-alfa.xlsx> and measured [viewed 2026-09-09]. Tier 1.
- **[S9]** Releasekalender RGS 3.9 (page) and the news item of 2026-08-24. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/releasekalender-rgs>, <https://www.referentiegrootboekschema.nl/Actueel/releasekalender-rgs-39-gepubliceerd> [viewed 2026-09-09]. Tier 1.
- **[S10]** RGS Taxonomie (softwareontwikkelaars). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/softwareontwikkelaars/rgs-taxonomie> [viewed 2026-09-09]. Tier 1.
- **[S11]** RGS Dashboard, "Versieverloop SBR RGS". Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/cmm/rgs/rgs_dashboard.php> [viewed 2026-09-09]. Tier 2.
- **[S12]** RGS (Grootboek) Referentienummer toegelicht (quotes the beheergroep on the sortering field since 3.0). GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/21/RGS_Grootboek_Referentienummer_toegelicht.htm> [viewed 2026-09-09]. Tier 2.
- **[S13]** Kennisbank. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/kbase> [viewed 2026-09-09]. Tier 1.
- **[S14]** Index of /rgs/ (directory listing nt11 to nt20). Logius, nltaxonomie.nl. Available from: <http://www.nltaxonomie.nl/rgs/> [viewed 2026-09-09]. Tier 1.
- **[S15]** Dataset Engelse labels (file `20210913 RGS NL en EN labels.xlsx`). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/dataset-engelse-labels> [viewed 2026-09-09]. Tier 1.
- **[S16]** Over RGS (governance: Taakgroep RGS and the werkgroepen Semantiek, Techniek, Implementatie en Communicatie). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/over-rgs> [viewed 2026-09-09]. Tier 1.
- **[S17]** RGS en RGS mkb: wat is het verschil? 2025-05-20. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/Actueel/rgs-en-rgs-mkb-wat-het-verschil> [viewed 2026-09-09]. Tier 1.
- **[S18]** Wat is RGS MKB. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/pag_epa/137/RGS_MKB.php> [viewed 2026-09-09]. Tier 2.
- **[S19]** RGS Zorg: een structuur die bruikbaar is voor het gehele zorgdomein, 2026-04-17. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/Actueel/rgs-zorg-een-structuur-die-bruikbaar-voor-het-gehele-zorgdomein> [viewed 2026-09-09]. Tier 1.
- **[S20]** RGS Ready boekhoudsoftware (normenkader versie 2019-04). Onderzoeksbureau GBNED, softwarepakketten.nl. Available from: <https://www.softwarepakketten.nl/pag_reg/81/RGS_Ready.htm> [viewed 2026-09-09]. Tier 2.
- **[S21]** Actueel (news index; newest items 2026-08-24 and 2026-07-28 on the viewing date). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/actueel> [viewed 2026-09-09]. Tier 1.
