# RGS Skill

A practical, primary-source-validated skill for doing Dutch bookkeeping
the standardized way with **RGS — the Referentie GrootboekSchema**, the
Netherlands' national reference chart of accounts. Map your ledger to RGS
once and the same bookkeeping feeds your annual accounts (KvK), tax
returns (Belastingdienst IB / VPB / OB), CBS statistics, and bank
reporting through SBR — *boekhouden één keer, hergebruik voor meerdere
rapportages*.

Built for the people who actually keep the books: ZZP'ers and BV owners
doing their own administratie, bookkeepers and accountants, and the
engineers building agentic bookkeeping tools for the Dutch market.

## What this skill gives you

- **`SKILL.md`** — the 30-second model (book at niveau 4; the
  referentiecode is the durable key; current version RGS 3.8 ↔ NT20 =
  reporting year 2026; RGS is Dutch-GAAP/MKB), a decision-routing table,
  and the core workflow for assigning an RGS code to a transaction.
  Loaded automatically when the skill triggers.
- **`references/`** — load on demand:
  - `fundamentals-governance.md` — what RGS is, the Taakgroep RGS
    governance model, the version history, and how to tell which version
    is authoritative (and which are superseded).
  - `structure-and-codes.md` — the 5-level hierarchy, how a
    referentiecode is constructed, the full field/attribute dictionary,
    omslag / debet-credit mechanics, and the main rubriek tables.
  - `scope-filters-entities.md` — picking the right subset
    ("RGS op maat"): ZZP / eenmanszaak / BV / stichting filters, sector
    schemas (woningcorporaties, agro, zorg, banken), and the Title 9
    Book 2 BW size classes (micro / klein / middelgroot / groot).
  - `reporting-compliance.md` — the RGS → SBR → filing chain, the
    Nederlandse Taxonomie (NT) version trap (**NT20 = reporting year
    2026, not 2020**), KvK deponering, the IB/VPB/OB winstaangifte flow,
    and BW2 model alignment.
  - `software-and-moneybird.md` — how RGS lives in MoneyBird's API
    (and Exact, Twinfield, AFAS, e-Boekhouden, SnelStart, Yuki,
    Asperion), the setup workflow, the pitfalls that actually bite, and
    machine-readable RGS datasets.
  - `multinationals-ifrs.md` — the honest scope limits: RGS has **no
    IFRS mapping and no consolidation logic**. The two-track model for a
    Dutch BV in an international group, plus where ESEF / the KvK IFRS
    taxonomy sit.
  - `sources.md` — the validated source register (three authority
    tiers, plus the known-issues / superseded list).
- **`scripts/rgs_lookup.py`** — a pure-stdlib tool to validate, look up,
  and fuzzy-search RGS codes from the official Excel master (or any CSV
  export), with an entity filter and a small offline seed for quick
  checks.

## Source discipline

Every factual claim in this skill is tied to a primary source — the RGS
standard owner (referentiegrootboekschema.nl), SBR Nederland / Logius
(sbr-nl.nl, nltaxonomie.nl), the Belastingdienst, KvK, CBS and AFM — with
GBNED / boekhoudplaza.nl cited as the de-facto practitioner reference and
vendor docs as corroborating. `references/sources.md` lists every URL with
its authority tier, date/version, and whether it is current or superseded.
Versions and rule numbers were verified at the time of writing — **RGS is
versioned roughly annually, so re-check `referentiegrootboekschema.nl/actueel`
before relying on a specific version for a regulated filing** (an RGS 3.9 /
NT21 cycle is expected after late 2026).

## Install

This is an AI-agent skill — a self-contained directory of markdown and a
script that any agent harness supporting the
[skill convention](https://skills.sh) can load.

### Install via the skills CLI

`SKILL.md` lives at the root of this public repo, so any runtime with the
[`skills`](https://www.skills.sh) CLI can install it directly:

```bash
npx skills add MaxSchoon/rgs-skill
```

skills.sh has no separate submission step — its directory is populated
from CLI install telemetry, so the skill becomes discoverable (via
`npx skills find rgs`) and climbs the listing as people install it.

### Manual install

Drop the directory under your agent's skills root. Common locations
include `~/.<agent>/skills/rgs/` or a project-local
`.agents/skills/rgs/`. Most harnesses auto-discover the skill from the
`name` and `description` in the SKILL.md frontmatter.

## Using the lookup script

```bash
# Validate a code exists and is active (download the official RGS 3.8 Excel first):
python scripts/rgs_lookup.py --file RGS_3.8.xlsx --validate WBedAlkOal

# Fuzzy-search by Dutch description, restricted to the bookable level + a BV:
python scripts/rgs_lookup.py --file RGS_3.8.xlsx --search "afschrijving" --entity BV --nivo 4

# Inspect one account (shows the omslag pair and D/C side):
python scripts/rgs_lookup.py --file RGS_3.8.xlsx --lookup BVorOva
```

With no `--file` it falls back to a tiny built-in seed of common codes —
a convenience for quick checks, **not** authoritative. Download the
official master from referentiegrootboekschema.nl (Kennisbank →
"Download RGS") for real work. For MoneyBird's API (pinned to RGS 3.5),
feed it a dataset filtered to codes valid in 3.5.

## Compatibility

The skill is harness-agnostic. It works with any AI-agent runtime that
loads skills from a directory of markdown files with YAML frontmatter
(`name`, `description`), routes requests to skills by description, and
lets the agent read reference files on demand — terminal coding agents,
IDE-integrated agents, chat agents, and SDK-built custom agents alike.

`scripts/rgs_lookup.py` needs only Python 3.10+ for CSV input; reading the
official `.xlsx` master additionally needs `pip install openpyxl`. The
references work on their own without any dependencies.

## License

MIT — see [`LICENSE`](LICENSE). Third-party attribution notices are in
[`NOTICE`](NOTICE).

## Disclaimer

This skill is **not** legal, accounting, tax, or filing advice. Dutch
statutory and tax filings carry real consequence; always verify against
the live publisher source (referentiegrootboekschema.nl, sbr-nl.nl,
belastingdienst.nl, kvk.nl) and involve a qualified accountant or tax
adviser before relying on a specific code, rule, or treatment for a
regulated filing. The skill lowers the cost of getting to the right RGS
code and the right page of the right manual; it does not replace
professional judgement.

## Contributing

Issues and pull requests are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).
Two principles:

1. **Source discipline.** Every new factual claim must cite a primary
   authoritative URL the contributor has actually fetched, with its
   version/date.
2. **Generality.** This is a public, vendor-neutral skill. No
   organisation-specific naming or internal jargon presented as
   universal; product-specific behaviour (e.g. a bookkeeping package's
   quirks) must be labelled as such.

## Contact

Questions, collaboration, or corrections: **contact@doc2ixbrl.com**.
For anything that could affect filing integrity (e.g. a code or rule in
the skill that would produce a non-compliant filing), please email before
opening a public issue.
