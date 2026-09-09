---
reference_id: software-and-moneybird
verified_on: 2026-09-09
rgs_version: "MoneyBird API: RGS 3.5; AFAS Profit 7: RGS 3.7; standard: 3.8"
---

# RGS in bookkeeping software, with MoneyBird's API in detail

*Part of the RGS Skill by Ontos B.V. (Max Schoon, Doc2iXBRL) — <https://github.com/MaxSchoon/rgs-skill>. Licensed CC BY 4.0. If you use this material, you must credit Ontos B.V. (see `ATTRIBUTION.md`).*

**Load this when:** code or a person books through a package (MoneyBird first,
others by their RGS Ready status), an integration must create or read ledger
accounts with RGS codes, or a chart is being set up or checked for complete
coupling.

**Do not load this when:** the question is the meaning of a code or the
mapping rules themselves (`references/structure-and-codes.md`), or which
subset an entity uses (`references/scope-filters-entities.md`).

## Contents

- [MoneyBird: product behaviour](#moneybird-product-behaviour)
- [MoneyBird: the ledger-accounts API](#moneybird-the-ledger-accounts-api)
- [Other packages](#other-packages)
- [Setup and completeness](#setup-and-completeness)
- [Datasets for validation](#datasets-for-validation)
- [Sources](#sources)

## MoneyBird: product behaviour

In MoneyBird a ledger account is a *categorie*, and every category is linked
to an RGS 3.5 code. Categories added from a **standaard verzameling** get the
right code automatically; a **losse categorie** takes a code you choose, with
a top-five of smart suggestions based on the name and its place on the balans
or resultatenrekening. Legacy categories without a 3.5 code show as
*verouderd* under Instellingen > Categorieën. The **RGS Brugstaat** export
(the blog names a CBS questionnaire as a use) is only available when every
category in the administration has an RGS 3.5 code [S1].

## MoneyBird: the ledger-accounts API

From the developer documentation, viewed 2026-09-09 [S2]:

- **`rgs_code` is required on create** and described as an "Existing RGS
  version 3.5 code, e.g. 'WMfoBelMfo'". It is a **top-level body property,
  a sibling of the `ledger_account` object**, on both POST and PATCH:

  ```json
  { "rgs_code": "WMfoBelMfo", "ledger_account": { "name": "new name" } }
  ```

- The `ledger_account` object carries `name`, `account_type` and
  `account_id`. `account_type` is one of `non_current_assets`,
  `current_assets`, `equity`, `provisions`, `non_current_liabilities`,
  `current_liabilities`, `revenue`, `direct_costs`, `expenses`,
  `other_income_expenses`.
- Responses expose the link as a `taxonomy_item` object with
  `taxonomy_version` (`"3.5"`), `code`, `name`, `name_english` and
  `reference` (the referentienummer, for example `WBedAlkOal` /
  `4215010`, `BVorDebHad` / `1101010`, `BSchBepBtwAfo` / `1205010.13`).
  The examples show level-5 codes in use for BTW sub-accounts.
- Documented status codes: POST 201, 400, 404, 422; PATCH 200, 404, 422.
  Treat 404 on a syntactically valid code as "unknown in 3.5" and 422 as a
  payload problem; the documentation does not spell out which is which.
- GET and list return `taxonomy_item`; there is no endpoint that lists all
  valid codes, so validate against a 3.5-filtered dataset before posting.
- DELETE deactivates first and deletes only if that fails; it always returns
  204.

Because the RGS core is unchanged since 3.0, the everyday codes present in 3.8
are present in 3.5; codes added after 3.5 are not
(`references/versions-governance.md`).

## Other packages

RGS Ready is the market yardstick (eight functions; GBNED tests and publishes
a report per vendor) [S3]. The RGS Ready table on softwarepakketten.nl lists,
among others, AFAS Profit, Exact Online, Twinfield (via two partners), SnelStart
Accountant, Yuki (extra accounts get the code automatically; the standard
chart is always coupled), Minox, iMUIS Online, CASH, Informer, 7x24.nl,
Aareon Tobias, Ctac, Cegeka-dsa, ITRIS, Metacom, Stip.t, and Microsoft
Business Central via De Saak (ships RGS MKB as the standard chart). MoneyBird
is not in that table [S4]. Version pins differ per vendor: AFAS Profit 7
supports RGS 3.7 and records an RGS-referentiecode plus an optional
RGS-extensie per account; its 3.6 to 3.7 upgrade emptied seven removed codes
(`BVrdOweGet`, `WPerPenDpe`, `WPerPenDvb`, `WPerPenDvl`, `WPerPenVpv`,
`WPerPenVvb`, `WPerPenVvl`) [S5]. Always read the version the package states
and validate against that workbook.

## Setup and completeness

1. Check the package's RGS Ready report and stated version [S3] [S4].
2. Choose the route: use the codes as the chart (a new entity), let the
   package auto-couple, or map an existing chart by hand from the package's
   suggestions.
3. Map at niveau 4; handle 1:n by splitting, m:1 by extension or a change
   request, 1:x by a change request, and omslag by coupling both codes [S6].
4. Run the package's unmapped-accounts control (RGS Ready function 7) until
   it is empty; MoneyBird withholds the Brugstaat export until then [S1] [S3].
5. Couple every new account on creation; do not rewrite booked periods to
   repair a miscoding.

## Datasets for validation

- **Official workbook** (`RGS 3.8-def.xlsx`), authoritative;
  `scripts/rgs_lookup.py --fetch 3.8` downloads it.
- **RGS MKB** (GBNED): a niveau-4 subset with 5-digit decimal numbers and
  per-entity charts for ZZP, EZ/VOF, BV micro and klein, and small
  stichtingen and verenigingen, obtainable from boekhoudplaza.nl [S7].
- **Fiba RGS Snelzoeker**: a browser tool with an offline database, version
  selector and fuzzy search; no API [S8].
- **Vegter/RGS-API**: an MPL-2.0 REST API over RGS 3.3 with the GBNED MKB
  filters, last pushed 2021-04-19; code reference only [S9].

## Sources

- **[S1]** Voeg gemakkelijk categorieën toe met het RGS, 2024-07-25. Moneybird. Available from: <https://www.moneybird.nl/blog/categorieen-toevoegen-met-het-rgs/> [viewed 2026-09-09]. Tier 3.
- **[S2]** Moneybird API Documentation, Ledger accounts (create, update, get, list, delete). Moneybird. Available from: <https://developer.moneybird.com/api/ledger-accounts> [viewed 2026-09-09]. Tier 3.
- **[S3]** RGS Ready boekhoudsoftware (normenkader versie 2019-04). Onderzoeksbureau GBNED, softwarepakketten.nl. Available from: <https://www.softwarepakketten.nl/pag_reg/81/RGS_Ready.htm> [viewed 2026-09-09]. Tier 2.
- **[S4]** RGS functionaliteit in boekhoudsoftware (RGS Ready table with test reports). Onderzoeksbureau GBNED, softwarepakketten.nl. Available from: <https://www.softwarepakketten.nl/cmm/swp/raadplegen_eigenschappen_kort.php?bronw=1&slt=72> [viewed 2026-09-09]. Tier 2.
- **[S5]** Referentie GrootboekSchema (RGS) inrichten (Profit 7). AFAS Help Center. Available from: <https://help.afas.nl/help/NL/SE/Fin_Config_Ledger_RGS.htm> [viewed 2026-09-09]. Tier 3.
- **[S6]** Aandachtspunten bij koppelen grootboekrekeningschema. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/over-rgs/aandachtspunten-bij-koppelen-grootboekrekeningschema> [viewed 2026-09-09]. Tier 1.
- **[S7]** Wat is RGS MKB. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/pag_epa/137/RGS_MKB.php> [viewed 2026-09-09]. Tier 2.
- **[S8]** RGS Snelzoeker. Fiba.nl. Available from: <https://fiba.nl/rgs_snelzoeker> [viewed 2026-09-09]. Tier 3.
- **[S9]** Vegter/RGS-API (GitHub repository; last push 2021-04-19; MPL-2.0). Available from: <https://github.com/Vegter/RGS-API> [viewed 2026-09-09]. Tier 3.
