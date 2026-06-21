---
name: rgs
description: >-
  Authoritative, source-validated guide to RGS (Referentie GrootboekSchema), the Dutch
  standardized reference chart of accounts, for bookkeeping the standardized way so annual
  reports and SBR filings (KvK, Belastingdienst IB/VPB/OB, CBS, banks) compile easily and
  stay compliant. USE THIS SKILL WHENEVER the task touches: choosing or validating an RGS
  code (referentiecode), mapping/koppelen a chart of accounts to RGS, picking the right
  account subset for an entity type (ZZP/eenmanszaak/BV) or sector (woningcorporaties,
  agro, zorg, banken), RGS levels (niveau 1-5), omslagcodes, debet/credit, the RGS
  Taxonomie / SBR / NT (Nederlandse Taxonomie) versions, jaarrekening/winstaangifte, or
  RGS for multinationals / IFRS / consolidation. Trigger EVEN when the user doesn't say
  "RGS" — e.g. "which ledger account should this go to", "standardize my chart of
  accounts", "wat is de juiste grootboekrekening", "boek dit volgens de standaard", or any
  standardized-Dutch-bookkeeping question. Covers MoneyBird's RGS API.
---

# RGS — Referentie GrootboekSchema

RGS is the Netherlands' standardized reference chart of accounts: a fixed catalogue of
**reference codes** you map your own ledger accounts onto **once**, after which the same
bookkeeping feeds many reports — "**boekhouden één keer, hergebruik voor meerdere
rapportages**". Using it is exactly how you get standardized books, an easy-to-compile
jaarrekening, and low-friction compliance — the goal of standardized bookkeeping for any
Dutch BV or MKB entity.

RGS is a **reference classification, not a mandatory standard** — you're never forced to
use it, but adopting it makes standardized reporting and benchmarking nearly free.

## The 30-second model (read before acting)

- **Book at niveau 4.** RGS is a 5-level tree; level 4 (`grootboekrekening`, e.g.
  `BLimKasKas`) is the bookable account. Levels 1–3 are grouping nodes; level 5
  (`mutatie`) exists only for some balance accounts and MKB software ignores it.
- **The referentiecode is the key, not the number.** Map on the alphabetic code
  (`B`/`W` + 3-letter groups). The decimal `referentienummer` is only an example and can
  change between versions.
- **Current version: RGS 3.8** (definitive 10 Dec 2025) → **RGS Taxonomie 3.8 ↔ NT20**
  (definitive 2 Feb 2026). **NT20 = reporting year 2026** (the number tracks the year, not
  2020). **MoneyBird's API is pinned to RGS 3.5** — codes you set via its API must be valid
  in 3.5 (the stable core means common codes are).
- **RGS is Dutch-GAAP / MKB.** It has no IFRS mapping and no consolidation logic. For a BV
  in an international group it covers only the Dutch local/statutory ledger.

## Decision routing — which reference to open

Keep SKILL.md in context and read **one** reference for the task at hand:

| Your task | Read |
|---|---|
| "Which code do I book this to?" / code structure, levels, fields, omslag, D/C | `references/structure-and-codes.md` |
| Pick the right account subset for an entity (BV/EZ/ZZP) or sector; size classes | `references/scope-filters-entities.md` |
| Filing: jaarrekening (KvK), IB/VPB/OB aangifte, SBR, taxonomy/NT versions, BW2 | `references/reporting-compliance.md` |
| Doing it in software / the MoneyBird API, setup workflow, pitfalls, datasets | `references/software-and-moneybird.md` |
| Foreign entities, IFRS, consolidation, ESEF, listed companies | `references/multinationals-ifrs.md` |
| Version/governance authority, "is this current?", RGS Ready, RGS MKB vs RGS | `references/fundamentals-governance.md` |
| Citing a source / re-validating freshness | `references/sources.md` |

Don't load all of them — that defeats the purpose. Route by the table.

## Core workflow: assign an RGS code to a transaction or account

1. **Identify the account's nature** — balance or P&V? asset/liability/equity or
   cost/revenue? This fixes the first letter (`B`/`W`) and hoofdrubriek.
2. **Find the candidate code at niveau 4.** Use the lookup script (below) or browse the
   official master. Disambiguate near-identical "Overige …" descriptions by their parent
   rubriek — "overige" is the single most error-prone term.
3. **Validate it exists and is active** (not `VERVALLEN`), in the version your software
   supports (RGS 3.5 for MoneyBird's API). Never invent a niveau-4 code tail — verify it.
4. **Check the entity fit** — is the code flagged for this entity type (BV)? A BV uses
   `BEiv` share capital + reserves, **not** the `BEivKap…` privé accounts (those are
   EZ/VOF). See `scope-filters-entities.md`.
5. **Handle omslag** — if the account can swing debit/credit (bank, RC, transitoria, tax),
   couple **both** the code and its `omslagcode` counterpart, or the balance reports under
   the wrong rubriek.
6. **Book it**, then confirm completeness — every account must be coupled. MoneyBird
   enforces this (it blocks the RGS Brugstaat export and blocks creating uncoded ledger
   accounts via the API).

For a **new** BV, the cleanest path is to use RGS codes as the chart of accounts from day
one (in MoneyBird: add categories from the **standard collections**, which auto-attach the
RGS code) rather than inventing custom categories and mapping later.

## The bundled lookup tool

`scripts/rgs_lookup.py` validates/looks up/searches RGS codes. It reads the **official RGS
Excel master** (download from referentiegrootboekschema.nl → Kennisbank) or any CSV export;
with no file it falls back to a tiny built-in seed of attested codes (convenience only —
**not authoritative**, verify against the master before booking).

```bash
# Validate a code exists and is active:
python scripts/rgs_lookup.py --file RGS_3.8.xlsx --validate WBedAlkOal
# Search by Dutch description, restricted to bookable level + BV:
python scripts/rgs_lookup.py --file RGS_3.8.xlsx --search "afschrijving" --entity BV --nivo 4
# Inspect one account (shows omslag pair, D/C):
python scripts/rgs_lookup.py --file RGS_3.8.xlsx --lookup BVorOva
```

It matches column headers case-insensitively against known aliases (official Excel and
GBNED exports differ); override with `--col-code` / `--col-desc` etc., and pick a tab with
`--sheet` (e.g. an MKB or Totaal tab). For MoneyBird compatibility, feed it a dataset
filtered to codes valid in RGS 3.5.

## Using this with MoneyBird (or any RGS-aware package)

If you book in **MoneyBird**, the key API fact validated here: MoneyBird exposes
`rgs_code` (RGS **3.5**) on `ledger_accounts`; on **POST/PATCH it's a top-level body field
— a sibling of `ledger_account`, not inside it — and required on create**; in responses
the link surfaces via the `taxonomy_item` object. Details, the setup workflow, and the
pitfalls are in `references/software-and-moneybird.md`, which also covers Exact Online,
Twinfield, AFAS, e-Boekhouden, SnelStart, Yuki and Asperion. Whatever the package, never
overwrite a booked period to "fix" a miscoding — post a **correcting entry** so the audit
trail stays intact.

## Source discipline (this matters)

Everything here was validated against primary sources on **2026-06-21** (see
`references/sources.md`). RGS is versioned ~annually, so **re-validate version-sensitive
claims after late 2026** (an RGS 3.9 / NT21 cycle is expected). The freshness check is
**referentiegrootboekschema.nl/actueel** (use whatever web search/fetch tools your agent
runtime provides). Treat referentiegrootboekschema.nl, sbr-nl.nl, logius.nl,
belastingdienst.nl and kvk.nl as authoritative; boekhoudplaza.nl / softwarepakketten.nl
(GBNED) as the de-facto practitioner reference (not the formal standard); vendor docs as
corroborating. When unsure whether a code or rule is still current, **look it up — don't
rely on memory.**
