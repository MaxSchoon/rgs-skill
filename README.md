# RGS Skill

A primary-source-grounded skill for AI agents doing Dutch bookkeeping the
standardized way with **RGS, the Referentie GrootboekSchema**: the national
reference chart of accounts that the SBR chain maps onto KvK annual
accounts, Belastingdienst returns (IB, VPB, OB), SBR Wonen and bank reports.
Map each ledger account to one RGS code once and the same books feed every
report.

Built for the people who actually keep the books (ZZP'ers and BV owners,
bookkeepers, accountants) and the engineers building agentic bookkeeping
tools for the Dutch market.

## What this skill gives you

An agent that must pick, validate or map an RGS code has one job: be right,
and know when it cannot be. Everything here serves that.

### The entry point

`SKILL.md` loads when the skill triggers. It holds an intake table keyed on
what is in front of the agent (a transaction, an own chart, an entity, a
filing question, an API, a group question), the three things to pin before
any judgment (the version the receiver accepts, the entity filter, the
level), the invariants that hold in every case, and the reference index. It
holds no domain facts of its own; those live in `references/`, each with its
source.

### The references

Load one. Each opens with `Load this when` and `Do not load this when`, a
contents list, and ends with a `Sources` list that every `[Sn]` marker in
the body resolves to (URL, publisher, page or file date, `[viewed
YYYY-MM-DD]`, authority tier).

| Read this | When you need |
|---|---|
| `versions-governance.md` | Which version is current (3.8 definitive, 3.9 alfa and its calendar), the workbook and taxonomy artifacts, the Taakgroep RGS, RGS MKB, RGS Ready, how to re-verify |
| `structure-and-codes.md` | The workbook's columns, the five levels, how a code is built, D/C and omslag, inactive codes, extensions, the procedure to assign a code or map an own chart, the mnemonic traps |
| `scope-filters-entities.md` | The filter columns with measured counts, recipes for a BV and for ZZP/EZ/VOF, RGS MKB's decimal numbers, sectors, legal size classes |
| `reporting-compliance.md` | The RGS to SBR chain, what the RGS Taxonomie 3.8 maps (25 entrypoints, counted), NT20/NT21 dates, KvK deposit, Belastingdienst returns, XAF and the RGS Brugstaat |
| `software-and-moneybird.md` | MoneyBird's ledger-accounts API (`rgs_code` top-level and required, RGS 3.5), RGS Ready packages, setup and completeness, datasets |
| `multinationals-ifrs.md` | Where RGS stops: no IFRS mapping, no consolidation logic, Dutch only, ESEF is elsewhere |

### The script

`scripts/rgs_lookup.py` validates, looks up and searches codes in the
official RGS workbook, reading `.xlsx` with the standard library alone. It
understands the official filter columns, reports `Inactief` and the omslag
partner, lists children for disambiguation by parent, and fetches the
workbook:

```bash
python3 scripts/rgs_lookup.py --fetch 3.8                       # caches ~/.cache/rgs/RGS-3.8.xlsx
python3 scripts/rgs_lookup.py --validate WBedKanKoa             # exit 0 valid, 1 unknown, 2 inactive
python3 scripts/rgs_lookup.py --search hosting --entity bv --nivo 4 --json
python3 scripts/rgs_lookup.py --children WBedKan
```

Without `--file` and without a cached workbook it falls back to a seed of a
few dozen codes verified against RGS 3.8: a convenience, not the standard.

## Source discipline

Every claim in `references/` traces to a source fetched on the date its
entry states: the standard owner (referentiegrootboekschema.nl, including
the official workbooks and the RGS Taxonomie zip, both downloaded and
measured), Logius (nltaxonomie.nl), SBR Nederland, KVK, the Belastingdienst
and Dutch law as tier 1; GBNED's boekhoudplaza.nl and softwarepakketten.nl
as the practitioner reference (tier 2); vendor documentation as tier 3.
RGS is versioned yearly; the next expected changes are RGS 3.9 bèta
(2026-10-09), RGS 3.9 definitive (2026-12-11) and NT21 in production
(2026-12-09). Re-check `referentiegrootboekschema.nl/actueel` before relying
on a version for a regulated filing.

For iXBRL, ESEF and KvK deposit mechanics use the sibling
[iXBRL skill](https://github.com/MaxSchoon/ixbrl); this skill stops at the
ledger.

## Install

This is an AI-agent skill: a directory of Markdown and one script that any
harness supporting the [skill convention](https://agentskills.io) can load.

```bash
npx skills add MaxSchoon/rgs-skill
```

Or drop the directory under your agent's skills root
(`~/.<agent>/skills/rgs/` or a project-local `.agents/skills/rgs/`); the
`name` and `description` in the SKILL.md front matter are what harnesses
route on.

## Compatibility

Harness-agnostic: any runtime that loads skills from a directory with YAML
front matter, routes on the description, and lets the agent read reference
files on demand. The script needs Python 3.10+ and nothing else; `--fetch`
needs network access.

## License

MIT, see [`LICENSE`](LICENSE). Third-party notices are in [`NOTICE`](NOTICE).

## Disclaimer

This skill is not legal, accounting, tax or filing advice. Verify against
the live publisher source and involve a qualified accountant or tax adviser
before relying on a code, rule or treatment for a regulated filing. The
skill lowers the cost of reaching the right code and the right page of the
right source; it does not replace professional judgement.

## Contributing

Issues and pull requests are welcome; see [`CONTRIBUTING.md`](CONTRIBUTING.md).
Two rules govern every change: a primary source, fetched and dated, for every
claim; and vendor-neutral language, with product behaviour labelled as such.

## Contact

Questions, collaboration, or corrections: **contact@doc2ixbrl.com**. For
anything that could affect filing integrity, please email before opening a
public issue (see [`SECURITY.md`](SECURITY.md)).
