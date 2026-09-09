---
name: rgs
description: Use when a task touches RGS, the Dutch Referentie GrootboekSchema (the national reference chart of accounts) - choosing or validating a referentiecode, mapping (koppelen) a grootboekrekeningschema to RGS, picking the account subset for an entity (ZZP, eenmanszaak, VOF, BV, stichting) or sector (woningcorporaties, agro, zorg), RGS levels (niveau 1-5), omslagcodes, debet/credit, the RGS Taxonomie, SBR, the Nederlandse Taxonomie (NT20, NT21), a jaarrekening or winstaangifte fed from an RGS-coded ledger, MoneyBird's rgs_code API, or RGS versus IFRS and consolidation. Trigger even when RGS is not named - "which grootboekrekening for this cost", "standardize my chart of accounts", "boek dit volgens de standaard", "wat is de juiste RGS-code", or any standardized Dutch bookkeeping question.
license: MIT
metadata:
  author: MaxSchoon
  verified_on: "2026-09-09"
  rgs_version: "3.8 definitive; 3.9 alfa"
---

# RGS skill

RGS is a catalogue of reference codes (`referentiecodes`) for ledger accounts.
Map each own account to one code once, and the RGS Taxonomie carries the
ledger into SBR reports for the KvK, the Belastingdienst, SBR Wonen and the
banks. It is a reference classification, not a mandatory standard, and it is
Dutch-GAAP only. This file routes; the facts, each with its source, live in
`references/`.

## Start here: what is in front of you

Pick the row that matches the artifact you have, then read the references it
names in that order. Load one reference at a time.

| What you have | What the question is | Read first |
|---|---|---|
| A transaction, invoice, or journal line | which code it books to, at which level | `references/structure-and-codes.md` (Assign a code), then the package's section in `references/software-and-moneybird.md` if one is named |
| An own chart of accounts, or an existing koppeltabel | how to map it, or whether the mapping is right | `references/structure-and-codes.md` (Map an own chart), `references/scope-filters-entities.md` (the subset), `references/software-and-moneybird.md` (completeness) |
| An entity type or sector, and no chart yet | which part of RGS applies (new BV, ZZP, stichting, woningcorporatie, zorg) | `references/scope-filters-entities.md` |
| A filing, taxonomy, or version question | jaarrekening, IB/VPB/OB aangifte, SBR, NT20/NT21, RGS Taxonomie, RGS 3.8 versus 3.9 | `references/reporting-compliance.md`, then `references/versions-governance.md` |
| Code that reads or writes RGS codes through a package's API | what the integration must get right | `references/software-and-moneybird.md` |
| A group, a foreign subsidiary, IFRS, consolidation, or ESEF | whether RGS reaches that far | `references/multinationals-ifrs.md` |
| A bare question, no artifact | what RGS is, who governs it, which version is current, RGS versus RGS MKB | `references/versions-governance.md` |

## Before any judgment: pin three things

1. **The RGS version the receiver accepts.** The definitive standard is RGS
   3.8 (workbook of 2025-12-10); a 3.9 alfa is out for review; MoneyBird's
   API accepts RGS 3.5 codes only. A code is validated against the version
   the receiver runs, never against "the latest".
2. **The entity filter.** The official workbook subsets by columns, not by
   separate files: "te kiezen bij aard" columns select, "te vervallen"
   columns drop. The `BV` column marks codes *specific to* a BV (share
   capital among them) for other entities to drop; it is not a "use for a
   BV" selection, and a BV must not drop it.
3. **The level.** Book and map at niveau 4, the grootboekrekening. Levels
   1-3 group; level 5 mutaties exist for balance accounts only and are
   filtered out by most MKB software.

## Invariants that hold in every case

- **The referentiecode is the key.** The referentienummer is an example
  numbering that changes between versions; never map or store on it.
- **Never derive a code tail from its letters.** The 3-letter groups are
  Dutch mnemonics: `WBedAut` is *Autokosten* (vehicles), not automation;
  server, hosting and software costs sit under Kantoorkosten
  (`WBedKanKoa`, `WBedKanSof`). A BV's share capital is `BEivGok…`; the
  `BEivKap…` family is the privé equity of natural persons. Confirm every
  niveau-4 code by description and parent, with `scripts/rgs_lookup.py`
  against the official workbook.
- **Retired codes are flagged, not deleted.** The workbook keeps them with
  the `Inactief` column set; the text "VERVALLEN" appears in one description
  only. Check the column.
- **Omslag runs both ways.** An account that can swing debit/credit (bank,
  rekening-courant, BTW, transitoria) carries an omslagcode; couple both the
  code and its counterpart or the balance reports under the wrong rubriek.
- **"Overige …" has two readings**, the literal residual line and everything
  the parent did not name; disambiguate by the parent rubriek, and never pick
  an "overige" code by description alone.
- **NT20 is the taxonomy generation for filings made in 2026**, not the year
  2020; NT21 enters production on 2026-12-09.
- **Correct by correcting entry.** Never rewrite a booked period to fix a
  miscoding.

## Reference index

| Read when the question is about | File |
|---|---|
| Which version is current, the 3.9 release calendar, the workbook and taxonomy artifacts, who governs RGS, RGS versus RGS MKB, RGS Ready, how to re-verify freshness | `references/versions-governance.md` |
| The workbook's columns, the five levels, how a code and its number are built, D/C and omslag mechanics, extensions, the procedure to assign a code or map an own chart | `references/structure-and-codes.md` |
| Subsetting by entity (ZZP, EZ/VOF, BV, stichting) and sector (WoCo, agro, zorg, banks), the filter columns with measured counts, legal size classes | `references/scope-filters-entities.md` |
| The RGS to SBR chain, the RGS Taxonomie's entrypoints, NT20/NT21 dates, KvK deposit, Belastingdienst returns, the XAF audit file and the RGS Brugstaat | `references/reporting-compliance.md` |
| MoneyBird's ledger-accounts API, what other packages support, the setup workflow, the pitfalls the standard owner names | `references/software-and-moneybird.md` |
| Groups, foreign subsidiaries, IFRS, consolidation, ESEF, and where RGS stops | `references/multinationals-ifrs.md` |

## Scripts

- **`scripts/rgs_lookup.py`** validates, looks up, and searches codes in the
  official RGS workbook, a CSV export, or its built-in seed. It reads
  `.xlsx` with the standard library alone, understands the official filter
  columns (`--entity bv|ez|zzp|sv|woco|zorg`, `--uitgebreid`, `--nivo 4`), reports
  `Inactief` and the omslag pair, and fetches the official workbook with
  `--fetch 3.8` (URL verified 2026-09-09; the seed is a convenience only).
  Run it before asserting that any niveau-4 code exists.

```bash
python3 scripts/rgs_lookup.py --fetch 3.8                       # once; caches ~/.cache/rgs/
python3 scripts/rgs_lookup.py --validate WBedKanKoa             # exists, active, level, omslag
python3 scripts/rgs_lookup.py --search hosting --entity bv --nivo 4
python3 scripts/rgs_lookup.py --lookup BLimBanRba               # shows omslag -> BSchSakRba
```

## Evidence and authority

Tier 1: referentiegrootboekschema.nl (Kennisbank workbooks and the
`/actueel` news page), nltaxonomie.nl, sbr-nl.nl, kvk.nl, belastingdienst.nl,
wetten.overheid.nl and the Staatsblad. Tier 2: boekhoudplaza.nl and
softwarepakketten.nl (Onderzoeksbureau GBNED), the practitioner reference
behind RGS MKB and RGS Ready, not the standard. Tier 3: vendor documentation,
authoritative only for that product's behaviour. Every reference ends with a
`Sources` list; a claim's `[Sn]` marker resolves there, with the date the
page was viewed. The freshness check is `referentiegrootboekschema.nl/actueel`.
For iXBRL, ESEF, and KvK deposit mechanics, the sibling iXBRL skill
(<https://github.com/MaxSchoon/ixbrl>) is the reference; this skill stops at
the ledger.

## When this skill cannot answer

If a question concerns a code not in the workbook version at hand, a sector
schema this skill does not cover (gemeenten, pensioenfondsen), a version
newer than the references cite, or a package not documented here, say so and
point at the primary source. Do not invent a code tail, a version, a date,
or an entrypoint. The cost of a wrong code in a filed return is real.

## Editing this skill

Runtimes cap the frontmatter `description` at 1024 characters and load this
whole body on activation; keep it under 500 lines and about 5,000 tokens, and
put substance in `references/`. Every reference carries front matter, a
`Load this when` and `Do not load this when` line, a `Contents` list, `[Sn]`
markers, and a `Sources` section last. `tests/check_skill.py` enforces all of
it; `CONTRIBUTING.md` has the rules.
