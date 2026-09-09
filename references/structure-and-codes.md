---
reference_id: structure-and-codes
verified_on: 2026-09-09
rgs_version: "3.8 definitive (2025-12-10); column layout also checked on 3.9 alfa"
---

# RGS structure, codes, and the workbook data model

*Part of the RGS Skill by Ontos B.V. (Max Schoon, Doc2iXBRL) — <https://github.com/MaxSchoon/rgs-skill>. Licensed CC BY 4.0. If you use this material, you must credit Ontos B.V. (see `ATTRIBUTION.md`).*

**Load this when:** you must choose or validate a code for an account or a
transaction, map an own chart of accounts to RGS, read the official workbook,
or explain levels, the referentiecode, the referentienummer, D/C, omslag, or
extensions.

**Do not load this when:** the question is which subset of codes an entity or
sector uses (`references/scope-filters-entities.md`), or how a package stores
the code (`references/software-and-moneybird.md`).

## Contents

- [The workbook: columns that matter](#the-workbook-columns-that-matter)
- [Five levels; book at niveau 4](#five-levels-book-at-niveau-4)
- [The referentiecode](#the-referentiecode)
- [The referentienummer is an example](#the-referentienummer-is-an-example)
- [D/C and omslag](#dc-and-omslag)
- [Inactive codes](#inactive-codes)
- [Extensions](#extensions)
- [Assign a code to an account or transaction](#assign-a-code-to-an-account-or-transaction)
- [Map an own chart to RGS](#map-an-own-chart-to-rgs)
- [Mnemonic traps](#mnemonic-traps)
- [Sources](#sources)

## The workbook: columns that matter

The official standard is an Excel workbook; row 1 of each data sheet is a
title row and row 2 holds the headers [S1]. `Totaal-RGS3.8-def` has these
columns, in order:

| Column | Meaning |
|---|---|
| `Referentiecode` | the key |
| `ReferentieOmslagcode` | the counterpart code for a balance that flips sign |
| `Sortering` | the sort key for balans and W&V (since 3.0, replaces the number as sort key [S2]) |
| `Referentienummer` | the example decimal number |
| `Omschrijving (verkort)`, `Omschrijving` | short and full description |
| `D/C` | normal side; blank only on the two niveau-1 roots `B` and `W` |
| `Nivo` | level 1-5 |
| `Basis`, `Uitgebr`, `EZ/VOF`, `ZZP`, `WoCo` | "Filter - te kiezen bij aard": selection columns |
| `Inactief` | the code is retired; 42 rows in 3.8 |
| `BB`, `Agro`, `WKR`, `EZ/VOF`, `BV`, `WoCo`, `Bank`, `OZW-Coop-Sticht-FWO`, `Afrek syst`, `Nivo5`, `Uitbr5`, `Stichting`, `OZW`, `FWO`, `Coop` | "Filters - te vervallen": drop columns |

The 3.9 alfa adds a `Zorg` column to both groups [S3]. Two headers (`EZ/VOF`,
`WoCo`) occur once in each group; the position decides the meaning. Filter
semantics and counts are in `references/scope-filters-entities.md`.

## Five levels; book at niveau 4

| Niveau | Name | Example (official) | Bookable |
|---|---|---|---|
| 1 | Balans / Winst-en-verliesrekening | `B` | no |
| 2 | Hoofdrubriek | `BMva` Materiële vaste activa | no |
| 3 | Rubriek | `BMvaBeg` Bedrijfsgebouwen | no |
| 4 | Grootboekrekening | `BMvaBegVvp` Verkrijgings- of vervaardigingsprijs bedrijfsgebouwen | **yes** |
| 5 | Mutatie | `BMvaBegVvpBeg` Beginbalans … bedrijfsgebouwen (the official page's example `BMvaBegVvpIna` is not in 3.8; the investment mutatie is `BMvaBegVvpLie`) | movement detail |

Levels and examples from the Opbouw page [S4], checked against the workbook
[S1]. RGS 3.8 has 2, 42, 295, 1,479 and 3,162 codes on levels 1 to 5 [S1].
Mutaties are defined for balance accounts only [S5]; a drop column `Nivo5`
removes all 3,162 of them in one step [S1]. The handleiding calls the first
four levels "level 1", sufficient for small entities at roughly 800 lines
[S6]. Map at niveau 4: a level-2 or level-3 code loses the split the reports
need, and a level-5 code turns a movement into an account.

## The referentiecode

A code is a source letter, `B` (Balans) or `W` (Winst-en-verliesrekening),
followed by one three-letter group per level in the form `Xxx` (one upper
case, two lower case): `SXxx` for a hoofdrubriek, `SXxxXxx` for a rubriek,
`SXxxXxxXxx` for a rekening, `SXxxXxxXxxXxx` for a mutatie, so at most 13
characters. The groups are derived from the Dutch description "as well as
possible". While RGS is cited as the standard, codes may not be changed or
extended; requests go to the beheersorganisatie [S5]. The code is unique per
level and is the durable key across versions; the number is not [S4] [S2].

## The referentienummer is an example

The velddefinities page describes a nine-digit number: positions 1-2
hoofdrubriek, 3-4 rubriek, 5-6 grootboekrekening, 7-8 mutatie, 9 the
extensiecode; the number "dient alleen als voorbeeld" and is renumbered when
accounts are inserted [S5]. The published workbook does not follow that
layout: niveau-4 numbers have seven digits (`BMvaBegVvp` = `0202010`) and
mutaties append `.NN` (`BIvaKouVvpBeg` = `0101010.01`), which is the layout
GBNED documents, with position 7 as the extensiecode [S1] [S2]. Since 3.0 the
number is no longer the sort key; the `Sortering` column is [S2]. Store the
code, print the number if a decimal chart is wanted, and expect the number to
change.

## D/C and omslag

`D/C` gives the normal side of every code below niveau 1 [S1]. Where a balance
can be debit or credit, the omslagcode is "de referentiecode van de
tegengestelde rekening" [S4]. In 3.8, 328 codes carry an omslagcode, 185 of
them at niveau 4 [S1]; GBNED counts about 180 niveau-4 accounts in roughly 90
pairs, among them bank and rekening-courant accounts, coöperatie member
accounts, tax receivable/payable pairs, tussenrekeningen, onderhanden
projecten, transitoria, and 14 rente baten/lasten pairs [S7]. Example:
`BLimBanRba` (rekening-courant bank, debit) has omslagcode `BSchSakRba` [S1].

The omslag is applied when a report is built (jaarrekening, winstaangifte),
separately for opening and closing balance; the same design explains the
duplicated tussenrekeningen under Vorderingen and Schulden. GBNED notes there
is no agreed moment for applying it in an XAF or RGS Brugstaat export, so the
receiving software may or may not expect it done [S7]. The standard owner's
own coupling guidance: when an account carries an omslagcode, make sure the
other code is coupled too [S8].

## Inactive codes

Retired codes stay in the workbook with `Inactief` = 1 ("Afgesproken is deze
niet in het RGS schema te verwijderen, maar wel te markeren"); 3.8 marks 42
[S1]. Only one description contains the word "vervallen"
(`WOmzNooOvv`, "Opbrengsten vervallen vouchers"), and it is an active code
[S1]. Test the column, never the text. One more irregularity to know: the 3.8
main sheet lists `WKprKvg` twice at niveau 3 with different descriptions
("Kosten van grond- en hulpstoffen / halffabrikaten" and "Kosten van
personeel"); the script keeps the last row, so treat that code as ambiguous
and check its children before using it [S1].

## Extensions

Extensions identify multiple objects behind one code (several bank accounts
by IBAN) or a codification by wetsartikel. On the code they are appended after
`.` (identification) or `:` (codification); on the number, position 9 (or 7 in
the published layout) marks the origin: 0 standard, 1 fiscaal, 2 branche,
3 concern, 4 onderneming, 5-9 free. Extensions are outside central governance
and must be managed by the user [S9]. GBNED finds the mechanism "verre van
duidelijk" and advises against it [S10]. Prefer a request for a new code over
an extension where the split is generally useful [S8].

## Assign a code to an account or transaction

1. Decide balans or W&V, then the hoofdrubriek and rubriek from the nature of
   the item (asset, liability, equity, revenue, cost type). This fixes the
   first seven characters.
2. List the niveau-4 candidates under that rubriek with
   `scripts/rgs_lookup.py --search <term> --nivo 4 --entity <bv|ez|zzp>`
   against the workbook version the receiver accepts.
3. Disambiguate by parent, not by description: the workbook holds many
   identical descriptions, and the owner's guidance is to look at the level
   above [S8]. "Overige …" can be read literally (the residual line) or
   indirectly (everything the parent did not name) [S6].
4. Confirm the code is not `Inactief`, note its `D/C`, and if it has an
   omslagcode, plan to couple the counterpart too [S1] [S8].
5. Book at niveau 4. Fix a wrong posting with a correcting entry.

## Map an own chart to RGS

Each own account gets exactly one code (the koppeltabel). The owner's
coupling guidance names the cases [S8]:

- **1:n** (one own account fits several codes): split the account and book
  separately from now on.
- **m:1** (own accounts finer than RGS): add an extension, expect to couple it
  manually in reporting software, and request the split if it is generally
  useful.
- **1:x** (no matching code): request a code; old fiscal schemes will not be
  added.
- **Omslag**: couple both codes.
- **Confusing descriptions**: decide by the level above.

Every account must be coupled; unmapped accounts produce report differences.
A new own account is coupled the day it is created.

## Mnemonic traps

The groups are Dutch abbreviations, not English ones. Verified in 3.8 [S1]:

| Looks like | Is | Use instead |
|---|---|---|
| `WBedAut` = automation | Autokosten en andere vervoermiddelen | `WBedKanKoa` Kosten automatisering, `WBedKanSof` Kosten software abonnementen, both under `WBedKan` Kantoorkosten |
| `BEivAan…` share capital | not a code | `BEivGok` Aandelenkapitaal (`BEivGokGea` normale aandelen, `…Pra` preferente, `…Eia` eigen aandelen) |
| `BEivKap…` for a BV | Eigen vermogen onderneming natuurlijke personen (privé-stortingen, -opnamen; `BEivKa2`-`BEivKa5` for firmanten 2-5) | EZ/VOF only |
| `WBedKau…` | not a code | look it up |
| `WBedAlkOal` | Algemene kosten andere kosten, under `WBedAlk` Andere kosten | fine for general costs, but check the parent |

Never complete a tail from the pattern; the grammar invites it, the standard
forbids it [S5], and the script exists to refuse it.

## Sources

- **[S1]** RGS 3.8-def.xlsx, sheet `Totaal-RGS3.8-def` (and `Recap`). Taakgroep RGS, 2025-12-10. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx>; counts and codes measured with `scripts/rgs_lookup.py` [viewed 2026-09-09]. Tier 1.
- **[S2]** RGS (Grootboek) Referentienummer toegelicht. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/21/RGS_Grootboek_Referentienummer_toegelicht.htm> [viewed 2026-09-09]. Tier 2.
- **[S3]** RGS 3.9-alfa.xlsx, sheet `Totaal-RGS3.9-alfa`. Taakgroep RGS, 2026-07-28. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.9-alfa.xlsx> [viewed 2026-09-09]. Tier 1.
- **[S4]** Opbouw RGS. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/opbouw-rgs> [viewed 2026-09-09]. Tier 1.
- **[S5]** Beschrijving velddefinities RGS. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/beschrijving-velddefinities-rgs> [viewed 2026-09-09]. Tier 1.
- **[S6]** Handleiding Referentie GrootboekSchema. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/handleiding-referentie-grootboekschema> [viewed 2026-09-09]. Tier 1.
- **[S7]** RGS Omslagcodes toegelicht. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/17/RGS_Omslagcodes_toegelicht.htm> [viewed 2026-09-09]. Tier 2.
- **[S8]** Aandachtspunten bij koppelen grootboekrekeningschema. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/over-rgs/aandachtspunten-bij-koppelen-grootboekrekeningschema> [viewed 2026-09-09]. Tier 1.
- **[S9]** Het werken met extensies. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/het-werken-met-extensies> [viewed 2026-09-09]. Tier 1.
- **[S10]** Extensies Referentie GrootboekSchema - RGS. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/25/Extensies_Referentie_GrootboekSchema_RGS.htm> [viewed 2026-09-09]. Tier 2.
