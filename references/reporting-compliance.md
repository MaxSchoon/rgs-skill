---
reference_id: reporting-compliance
verified_on: 2026-09-09
rgs_version: "RGS Taxonomie 3.8 = NT20_RGS_20251210; NT20 in production, NT21 from 2026-12-09"
---

# RGS to SBR: taxonomies, filings, and exports

**Load this when:** the task is a filing or return fed from an RGS-coded
ledger (KvK jaarrekening, IB, VPB, OB, SBR Wonen, bank credit reporting), a
taxonomy generation or date (NT20, NT21, RGS Taxonomie), or an export that
carries RGS codes (XAF audit file, RGS Brugstaat).

**Do not load this when:** the question is iXBRL or XBRL mechanics of the
deposit itself (entry points, report packages, validator codes): that is the
sibling iXBRL skill, <https://github.com/MaxSchoon/ixbrl>, file
`references/jurisdictions/nl-sbr.md`. This file stops where the RGS code
leaves the ledger.

## Contents

- [The chain in one paragraph](#the-chain-in-one-paragraph)
- [Which taxonomy generation, and when](#which-taxonomy-generation-and-when)
- [What the RGS Taxonomie 3.8 actually maps](#what-the-rgs-taxonomie-38-actually-maps)
- [Mapping method](#mapping-method)
- [KvK annual accounts](#kvk-annual-accounts)
- [Belastingdienst returns](#belastingdienst-returns)
- [Exports that carry the code: XAF and RGS Brugstaat](#exports-that-carry-the-code-xaf-and-rgs-brugstaat)
- [Sources](#sources)

## The chain in one paragraph

Each own ledger account carries one referentiecode; the RGS Taxonomie, an XBRL
artifact built on the Nederlandse Taxonomie architecture, links each code to
the concepts of specific SBR reports (entrypoints), so reporting software can
fill a KvK, Belastingdienst, SBR Wonen or bank report from the ledger without
re-keying [S1] [S2]. The Belastingdienst promotes RGS because an RGS-coded
administration lets it compare BTW and income-tax returns and run standard
analyses automatically before an audit [S3].

## Which taxonomy generation, and when

The NT number is a generation, not a year. Read the entrypoint file names:
under NT20 the KvK entrypoints are `kvk-rpt-jaarverantwoording-2025-…` (annual
accounts for financial year 2025, deposited in 2026), while the Belastingdienst
entrypoints mix years: `bd-rpt-vpb-aangifte-2025`, `bd-rpt-ihz-aangifte-2025`,
`bd-rpt-ihz-via-2025`, `bd-rpt-ob-aangifte-2026`, `bd-rpt-ob-suppletie-2026`,
`bd-rpt-icp-opgaaf-2026`, `bd-rpt-vpb-sba-2026`,
`bd-rpt-vpb-verzoekwijzigingva-2026` [S4] [S5].

From the SBR release calendar (updated 2026-07-30) [S6]:

| Generation | Domain | Definitive | Production |
|---|---|---|---|
| NT20.2 | Belastingdienst (`NT20_BD_20260916`) | 2026-07-31 | 2026-09-16 |
| NT21 | KvK (`NT21_KVK_20261209`) | 2026-10-29 | 2026-12-09 |
| NT21 | Belastingdienst (`NT21_BD_20261209`) | 2026-11-05 | 2026-12-09 |
| NT21.1 | Belastingdienst | 2027-01-28 | 2027-02-17 |
| NT21 | OCW | 2027-01-05 | 2027-02-17 |

RGS 3.8 was built on NT20 and FT20; the 3.9 alfa on NT21 and FT21, with the
bank, tax and SBR Wonen entrypoints "nog niet beschikbaar" at alfa time
[S7] [S8]. RGS Taxonomie 3.9 is planned for 2027-01-15
(`references/versions-governance.md`). On nltaxonomie.nl the RGS tree ends at
`nt20/`; there is no `nt21/` yet [S9].

## What the RGS Taxonomie 3.8 actually maps

`NT20_RGS_20251210.zip` unpacks to `www.nltaxonomie.nl/rgs/nt20/rgs/20251210/`
with `dictionary/`, `entrypoints/`, `mapping/` and `presentation/`. The
`entrypoints/` directory holds 26 schemas: `rgs-rpt-reference-codes.xsd`
(the code list itself) and 25 `rgs-to-<domain>-…` schemas [S10]:

| Domain | Entrypoints mapped |
|---|---|
| Belastingdienst (`bd`) | `ihz-aangifte-2025`, `vpb-aangifte-2025`, `ob-aangifte-2026`, `ob-suppletie-2026` |
| KvK (`kvk`) | `jaarverantwoording-2025-nlgaap-` micro, klein, middelgroot, groot, each with `-publicatiestukken` and `-verticaal` variants where they exist (12 in total) |
| SBR Wonen (`bzk`) | six `de-verantwoordingsinformatie-2025-toegelaten-instellingen-volkshuisvesting-…` variants (administratieve, hybride, juridische scheiding, verlicht regime, and geconsolideerd) |
| Banks (`frc`) | `nt-sbr-jaarrekening-rechtspersoon-2025`, `-natuurlijk-persoon-2025`, `-beperkt-2025` |

The KvK NT20 directory itself lists 27 entrypoints, including sector ones
(banken, verzekeringsmaatschappijen, pensioenfondsen, zorginstellingen,
stichtingen, coöperaties, organisaties zonder winststreven, fondsenwervende
organisaties, toegelaten instellingen volkshuisvesting) that the RGS Taxonomie
does not map [S5] [S10]. The mapping linkbases are named `map-<domain>-…xml`
(for example `map-bd-vpb_bd-lr-hd_par_dec-vpb.xml`) [S10]. A human-readable
mapping and its toelichting are on the Kennisbank as "RGS 3.8 mapping naar SBR
NT20 concepten" [S11]. Earlier editions of this skill cited "32 entrypoints"
and linkbases named `rgs-mapping_…`; the zip shows neither.

## Mapping method

The owner's instruction defines mapping as coupling source elements (RGS) to
target elements (an SBR entrypoint). A sub-report is mapped **balanced** when
every level of the target stays in balance, which requires that no source
level is more condensed than the target (1:1 or 1:n, never n:1) and that
totals hold at every level; otherwise it is **unbalanced**. Mapping is
iterative per level, and unmapped elements stay untagged [S12]. The
handleiding adds that "Overige …" lines can be tagged **direct** (the literal
line) or **indirect** (everything the higher elements excluded), which is why
each level needs its own residual [S13].

## KvK annual accounts

All legal persons deposit electronically via SBR from financial year 2025:
micro and klein since financial year 2016, middelgroot since 2017, groot from
2025, after the Besluit elektronische deponering handelsregister was amended on
2024-12-18; XBRL and iXBRL are both permitted and post or e-mail deposit
lapses [S14] [S15]. Micro and klein entities may use software via SBR or,
for listed legal forms, the Zelf Deponeren portal; middelgroot and groot must
use software via SBR with a PKIoverheid certificate [S15]. The size class
selects the classic KvK entrypoint the RGS Taxonomie maps to
(`references/scope-filters-entities.md`); RTS, Reporting Manual and FAQ
editions for financial year 2026 are dated 2026-07-10 [S14]. Deposit
mechanics beyond the ledger are the iXBRL skill's domain.

## Belastingdienst returns

The RGS Taxonomie maps to the IB (`ihz`), VPB and OB entrypoints listed above,
so an RGS-coded ledger can feed the winstaangifte and the BTW return through
fiscal software [S10]. The Belastingdienst's own RGS page describes the
benefit as automatic comparison of BTW and IB returns and standard analyses
during audit preparation [S3]. Which point release applies to a given
berichtstroom (NT20, NT20.1, NT20.2) is on the release calendar [S6].

## Exports that carry the code: XAF and RGS Brugstaat

- **XAF (XML Auditfile Financieel).** The standard owner's note on the SBR
  coupling says two elements were added to `generalLedger/ledgerAccount`:
  `leadReference` for the RGS referentiecode and `leadCrossReference` for the
  RGS omslagcode, used for negative balances [S16]. GBNED documents that the
  2017 edition of XAF 3.2 instead specified a `taxoRef` element and marked
  `leadCode`, `leadDescription`, `leadReference` and `leadCrossReference` as
  "NIET gebruiken voor RGS", that vendors implemented both patterns, and that
  XAF 4.0 handles RGS codes uniformly [S17]. When reading a XAF, look in both
  places and record the RGS version separately; the file cannot name it in
  the 2014 layout [S17].
- **RGS Brugstaat.** A standard koppelvlak defined by GBNED with software
  vendors to move RGS-coded ledger balances from bookkeeping software to
  fiscal software for the IB and VPB winstaangifte [S18]. MoneyBird exports it
  once every category has an RGS 3.5 code, and cites the CBS questionnaire as
  a use [S19]. GBNED notes the brugstaat documentation (2.0, 2020) tells the
  producer to account for omslagcodes, and that there is no market-wide
  agreement on whether the producer or the consumer applies them [S20].

## Sources

- **[S1]** RGS Taxonomie (softwareontwikkelaars). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/softwareontwikkelaars/rgs-taxonomie> [viewed 2026-09-09]. Tier 1.
- **[S2]** English (RCSFI "is connected to XBRL-tags in the Dutch taxonomy"). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/english> [viewed 2026-09-09]. Tier 1.
- **[S3]** Referentie Grootboekschema: iets voor u? Belastingdienst. Available from: <https://www.belastingdienst.nl/wps/wcm/connect/nl/intermediairs/content/referentie-grootboekschema-iets-voor-u> [viewed 2026-09-09]. Tier 1.
- **[S4]** Index of /nt20/bd/20251210/entrypoints/ (8 files). Logius, nltaxonomie.nl. Available from: <http://www.nltaxonomie.nl/nt20/bd/20251210/entrypoints/> [viewed 2026-09-09]. Tier 1.
- **[S5]** Index of /nt20/kvk/20251210/entrypoints/ (27 files). Logius, nltaxonomie.nl. Available from: <http://www.nltaxonomie.nl/nt20/kvk/20251210/entrypoints/> [viewed 2026-09-09]. Tier 1.
- **[S6]** Releasekalender 2026-2027 (laatste update 30-07-2026). SBR Nederland. Available from: <https://www.sbr-nl.nl/werken-met-sbr/taxonomie/releasekalender> [viewed 2026-09-09]. Tier 1.
- **[S7]** RGS 3.8-def.xlsx, sheet `Recap` ("op basis van NT20-FT20"; entrypoints assessed). Taakgroep RGS, 2025-12-10. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx> [viewed 2026-09-09]. Tier 1.
- **[S8]** RGS 3.9-alfa.xlsx, sheet `Recap` ("op basis van NT21-FT21"). Taakgroep RGS, 2026-07-28. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.9-alfa.xlsx> [viewed 2026-09-09]. Tier 1.
- **[S9]** Index of /rgs/ (nt11 to nt20). Logius, nltaxonomie.nl. Available from: <http://www.nltaxonomie.nl/rgs/> [viewed 2026-09-09]. Tier 1.
- **[S10]** NT20_RGS_20251210.zip (RGS Taxonomie 3.8), directory listing of `entrypoints/` and `mapping/`. Taakgroep RGS. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/NT20_RGS_20251210.zip> via <https://www.referentiegrootboekschema.nl/nt20rgs20251210> [viewed 2026-09-09]. Tier 1.
- **[S11]** RGS 3.8 mapping naar SBR NT20 concepten, and its toelichting (Kennisbank items). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/rgs-38-mapping-naar-sbr-nt20-concepten>, <https://www.referentiegrootboekschema.nl/toelichting-rgs-38-mapping-naar-sbr-nt20-concepten> [viewed 2026-09-09]. Tier 1.
- **[S12]** Instructie mapping RGS en SBR. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/instructie-mapping-rgs-en-sbr> [viewed 2026-09-09]. Tier 1.
- **[S13]** Handleiding Referentie GrootboekSchema. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/handleiding-referentie-grootboekschema> [viewed 2026-09-09]. Tier 1.
- **[S14]** Uitbreiding elektronische deponering handelsregister (documents for financial year 2026 dated 2026-07-10). SBR Nederland. Available from: <https://www.sbr-nl.nl/sbr-domeinen/handelsregister/uitbreiding-elektronische-deponering-handelsregister> [viewed 2026-09-09]. Tier 1.
- **[S15]** Deponeren met SBR (updated 2026-03-05). KVK. Available from: <https://www.kvk.nl/deponeren/deponeren-met-sbr/> [viewed 2026-09-09]. Tier 1.
- **[S16]** RGS en de koppeling tussen SBR en Auditfile Financieel. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/rgs-en-de-koppeling-tussen-sbr-en-auditfile-financieel> [viewed 2026-09-09]. Tier 1.
- **[S17]** RGS in de Auditfile Financieel (XAF) (note of 2025-02-20 on XAF 4.0). Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/bericht/1453&bronw=1/RGS_in_de_Auditfile_FInancieel_XAF.htm> [viewed 2026-09-09]. Tier 2.
- **[S18]** RGS Ready boekhoudsoftware, section "RGS brugstaat". Onderzoeksbureau GBNED, softwarepakketten.nl. Available from: <https://www.softwarepakketten.nl/pag_reg/81/RGS_Ready.htm> [viewed 2026-09-09]. Tier 2.
- **[S19]** Voeg gemakkelijk categorieën toe met het RGS, 2024-07-25. Moneybird. Available from: <https://www.moneybird.nl/blog/categorieen-toevoegen-met-het-rgs/> [viewed 2026-09-09]. Tier 3.
- **[S20]** RGS Omslagcodes toegelicht. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/17/RGS_Omslagcodes_toegelicht.htm> [viewed 2026-09-09]. Tier 2.
