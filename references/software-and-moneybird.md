# RGS in software & in practice — focus on MoneyBird

> The operational reference: how RGS lives in MoneyBird's API, the setup workflow, the
> pitfalls that actually bite, and machine-readable RGS datasets. MoneyBird is one of the
> most widely used Dutch MKB packages, so it's covered in depth here; the same patterns
> apply to the other packages in the table below.

## MoneyBird + RGS — the facts that matter

In MoneyBird, **grootboekrekeningen are called *categorieën* (categories), and since the
July 2024 update every category is linked to an RGS 3.5 code** — the live constraint for
anyone booking a Dutch BV on MoneyBird.

In the product:
- **Standaard verzamelingen** — adding a category from MoneyBird's standard collections
  auto-attaches the correct RGS code. **This is the recommended path** — no manual lookup,
  fewer coding errors. For a clean BV, build the chart from standard collections.
- **Losse categorieën** — for a custom category you choose the RGS code yourself;
  MoneyBird shows a **top-5 "slimme suggesties"** based on the name and its position on
  the P&V/balance.
- **Overstappen** — legacy categories without an RGS 3.5 code show as "verouderd";
  Instellingen > Categorieën migrates them with smart suggestions.
- **RGS Brugstaat export** — for category exports (e.g. a CBS questionnaire). **Only
  available once *every* category has an RGS 3.5 code.**

### API — `ledger_accounts`

Authoritative ref: `https://developer.moneybird.com/api/ledger-accounts` (RGS **3.5**).

- **An `rgs_code` field exists** — e.g. `"WMfoBelMfo"`, described as an "RGS version 3.5
  code".
- **Body placement is unusual:** on **POST** and **PATCH**, `rgs_code` is a **top-level
  body property — a sibling of the `ledger_account` object, NOT inside it**:
  ```json
  { "rgs_code": "WMfoBelMfo", "ledger_account": { "name": "new name" } }
  ```
- **On POST, `rgs_code` is `string · required`.** Since July 2024, **creating a ledger
  account without a valid RGS 3.5 code is blocked** — a missing/invalid code can return
  **404** (unknown code) or **400/422** (bad payload).
- In **responses**, the RGS link is surfaced via a **`taxonomy_item`** object on each
  ledger account (not a raw `rgs_code` string). To read/validate existing links, inspect
  `taxonomy_item` on GET/list responses.
- `account_type` enum (separate from RGS): `non_current_assets, current_assets, equity,
  provisions, non_current_liabilities, current_liabilities, revenue, direct_costs,
  expenses, other_income_expenses`. Parent/child trees need matching `account_type`.
- A **Rapportage (Reporting) API** (2025) can pull P&V/balance/cashflow directly — useful
  for RGS-aligned reporting without manual exports.

> **Integration action item.** If any code path *creates* ledger accounts via POST, it
> must pass a valid RGS 3.5 `rgs_code` as a **top-level** field or the call fails. A PATCH
> of only name/type doesn't require it, but you can pass `rgs_code` to (re)link. Get the
> top-level placement and the 3.5 validity right and most MoneyBird+RGS integration bugs
> disappear.

> **Version mismatch is the headline caveat:** MoneyBird's API is pinned to **RGS 3.5**
> while the live standard is **3.8**. Any code you set via the API must be **valid in
> 3.5**. Because the RGS core is stable since 3.0, the common codes (`WBedAlkOal`,
> `BLimKasKas`, etc.) are present in 3.5 — but validate against 3.5, not 3.8, before POSTing.

## Other Dutch packages — the universal pattern

Every package keeps its **own chart** and maps each account to an **RGS referentiecode**
(a koppeltabel); the code links onward to SBR for filings.

| Package | RGS version | How assigned | Notable |
|---|---|---|---|
| **MoneyBird** | 3.5, lvl 4 | Auto (standard collections) + top-5 suggestions; `rgs_code` required on API create | Categories ≈ ledgers; RGS Brugstaat needs full coverage |
| **Exact Online** | via Reporting Schemes (1.1→3.2) | "RGS suggesties" (~3/acct) | Queryable via Invantive SQL |
| **Twinfield** | 3.2+ | Reporting structure pre-linked at environment level | Auto-pushed to sub-administrations |
| **AFAS Profit** | up to 3.7 | Per account: RGS-referentie + optional extensie | Combined code+extension field |
| **e-Boekhouden.nl** | detailniveau 3 or 4 | Type-ahead per account | Choose detail level |
| **SnelStart** | 3.1, lvl 4 | "Vul met suggesties" (25 at a time) | Mapping stored per account, reused across admins |
| **Yuki** | standard scheme | Pre-coded; extra accounts auto-coded | Near-zero manual mapping |
| **Asperion** | up to lvl 5 | Auto-match + conversion templates | Hierarchical parent-branch guard |

## Practical setup workflow

1. **Check readiness** — package on softwarepakketten.nl, status on rgsready.nl.
2. **Choose a route** — (a) software auto-couples; (b) manual map; (c) partial auto-map
   you complete; (d) **use RGS codes directly as your chart** — ideal for a new BV.
3. **Pick the level** — map at **niveau 4** (10-char code like `BLimKasKas`). Don't map
   to level 2/3 (loses specificity) or level 5 (mutaties mix with accounts).
4. **Map (koppeltabel)** — attach a referentiecode per account; use auto-suggestions,
   then **review**.
5. **Handle edge cases** — splits, extensies, omslagcodes, "overige" (see Pitfalls).
6. **Validate completeness** — run the mapping-control report; **every** account must be
   coupled (MoneyBird blocks the Brugstaat until then).
7. **Propagate & maintain** — couple new accounts immediately; stay on the latest
   operational version your software supports.
8. **Export / report** — XAF with RGS codes, or RGS-aware exports → SBR filings.

## Common pitfalls (these actually bite)

1. **1:n ambiguity** — your account fits multiple RGS codes → split it going forward.
2. **m:1 too-detailed** — you split finer than RGS → add an extensie (or accept the
   coarser code). Extensions usually need manual coupling and break SBR comparability.
3. **No matching code** — submit a request to add one; don't force a wrong code.
4. **Omslagcode** — accounts that can go debit *or* credit must couple **both** sides or
   balances flip into the wrong rubriek.
5. **"Overige …"** — the single most error-prone term; disambiguate by the parent level.
6. **Wrong level** — map at niveau 4, not 2/3/5.
7. **Incomplete coupling** — the classic error → reporting discrepancies. MoneyBird
   enforces this (Brugstaat blocked; API blocks uncoded ledger creation).
8. **New accounts uncoupled / version drift** — couple immediately; mind the 3.5-vs-3.8
   API mismatch.
9. **Own sub-accounts in a decimal scheme** — reserve a trailing digit (use 6-digit
   numbers) so you can add sub-accounts without breaking the standard numbering.

## RGS Ready (the 8-point yardstick)

A GBNED keurmerk (norms set with the former RGS Taskforce); results on rgsready.nl /
softwarepakketten.nl. The 8 functions: (1) RGS scheme available in-software; (2) auto
updates; (3) manual coupling; (4) auto-coupling proposal; (5) auto-propagation across
administrations; (6) RGS code+version in the XAF at mutation level; (7) overview-by-RGS-
code with validation of unmapped accounts; (8) RGS codes passed through the package's
API/koppelvlak. **"RGS Ready voor accountancy"** = all 8; **"voor ondernemers"** drops #4
and #5. Certified packages include Minox (first), SnelStart, Exact Online, Twinfield,
Yuki, AFAS, e-Boekhouden, Asperion, CASH, and ~20 more. *(MoneyBird clearly supports RGS
3.5 but a dedicated MoneyBird RGS Ready test report wasn't confirmed — treat as
"supports RGS" rather than certified; verify on rgsready.nl if it matters.)*

## Machine-readable RGS datasets (for the bundled lookup script)

- **Official — referentiegrootboekschema.nl Kennisbank "Download RGS"** — the
  authoritative Excel master (current **3.8**). Best source of truth.
- **GBNED / boekhoudplaza RGS Dashboard** (`boekhoudplaza.nl/cmm/rgs/rgs_dashboard.php`)
  — browsable codes, decimal scheme, filters, RGS Audittrail of per-version changes.
- **RGS MKB schema (GBNED)** — curated subset to niveau 4, available as **CSV/Excel and
  JSON** on request (`rgs@gbned.nl`). Fields incl. Refcode, Omslagcode, Refnr,
  Branchecode, Status, Versie, RekNr, ZZP/EZ/BV/SVC flags. The most practical
  machine-readable dataset for a custom validator.
- **Vegter/RGS-API** (GitHub, MPL-2.0) — Node/TS REST API over RGS, but **v3.3, last push
  2021 — stale**; use as code reference only.
- **Fiba RGS Snelzoeker** (`fiba.nl/rgs_snelzoeker`) — fast fuzzy lookup UI, version
  selector up to 3.8. Manual lookups; not an API.
- **For MoneyBird:** validate a code by attempting to set `rgs_code` (an invalid 3.5 code
  → 404); read existing links via `taxonomy_item`. No public "list valid codes" endpoint.

See `scripts/rgs_lookup.py` for a self-contained validator/lookup built on the official
Excel master (with a 3.5-filter option for MoneyBird compatibility).
