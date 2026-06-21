# Contributing to the RGS Skill

Thanks for considering a contribution. This skill is read by AI agents and
by people doing their own bookkeeping, so its accuracy directly affects the
quality and compliance of real Dutch administraties and filings.
Contributions are welcome from anyone — bookkeepers, accountants, tax
advisers, software vendors, RGS/SBR insiders, and engineers building
bookkeeping tools.

## What this project is

A vendor-neutral skill for any AI-agent runtime that supports the standard
skill convention. It contains:

- `SKILL.md` — the agent entrypoint (model, routing, core workflow)
- `references/` — primary-source-cited notes on RGS fundamentals &
  governance, structure & codes, scope/filters/entities, reporting &
  compliance, software & MoneyBird, multinationals & IFRS, and the source
  register
- `scripts/rgs_lookup.py` — a pure-stdlib RGS code validator / lookup tool

There are no harness-specific assumptions in this repo. Do not introduce
them (no "use tool X", no vendor-only instructions presented as universal).

## Discipline

Three rules govern every change:

### 1. Primary-source validation

Every factual claim must trace to an authoritative source the contributor
has actually fetched. In order of authority:

- **Authoritative:** referentiegrootboekschema.nl (the RGS standard owner /
  Taakgroep RGS), sbr-nl.nl & logius.nl & nltaxonomie.nl (SBR / Nederlandse
  Taxonomie), belastingdienst.nl, kvk.nl, cbs.nl, afm.nl, and Dutch law
  (wetten.overheid.nl, Staatsblad).
- **Practitioner reference:** boekhoudplaza.nl / softwarepakketten.nl
  (GBNED / Gerard Bottemanne) — influential and detailed, but **not** the
  formal standard; label it as commentary.
- **Corroborating:** bookkeeping-software vendor docs (product-specific
  behaviour only).

Cite the URL with its **version/date**, and add or update the row in
`references/sources.md`. RGS reference codes change between versions —
prefer the durable referentiecode over the example referentienummer, and
say which RGS version a claim was checked against.

### 2. Honest-gap discipline

If you could not verify a claim, say so rather than papering over it:

- "Not verified against the RGS 3.8 master; included pending confirmation."
- "boekhoudplaza documents this, but the official velddefinities are silent."
- "Behaviour observed in MoneyBird's API; not stated in its public docs."

A documented gap is a contribution; a confident-sounding fabrication is a
regression. The skill already flags real ambiguities (e.g. the 7-vs-9-digit
referentienummer discrepancy, the omslag timing) — keep that habit.

### 3. Vendor-neutral language

The skill must be usable in any agent harness. Don't name specific
harnesses, IDEs, or assistants, and don't hard-code one runtime's tool
names — say "use your agent's web search/fetch tools". Product-specific
behaviour of *bookkeeping software* (MoneyBird, Exact, etc.) is in scope,
but must be clearly labelled as that product's behaviour, not RGS itself.

## Freshness discipline (RGS is versioned annually)

RGS ships a new minor version roughly every December, and the matching RGS
Taxonomie / NT version follows. Before changing any version-sensitive
claim, check **referentiegrootboekschema.nl/actueel** and update:

- the version statements in `SKILL.md` and `fundamentals-governance.md`,
- the NT/taxonomy mapping in `reporting-compliance.md` (mind the trap:
  **NTxx tracks the reporting year, not the calendar year**),
- the affected rows in `references/sources.md` (mark superseded entries).

## Size discipline (skill-runtime limits)

Skills load into runtimes that enforce real size limits. A bloated
`SKILL.md` is silently truncated by some runtimes and crowds out other
skills. Keep:

- **YAML frontmatter `description`** ≤ **1024 characters** (the runtime
  reads it to decide whether to load the skill at all).
- **`SKILL.md` body** ≤ **32 KiB** and aim for **< 500 lines**.

Prefer extending a file in `references/` over growing `SKILL.md` —
reference files load only when the body points the agent at them
(progressive disclosure). Before merging an edit that grows `SKILL.md`:

```bash
wc -c SKILL.md   # keep under 32768
```

## Script integrity

Every change to `scripts/rgs_lookup.py` must keep it runnable on a clean
Python 3.10+ with no third-party packages (the `.xlsx` path's `openpyxl`
import is optional and guarded). Before opening a PR:

```bash
python3 -m py_compile scripts/rgs_lookup.py
python3 scripts/rgs_lookup.py --validate WBedAlkOal     # seed smoke test
python3 scripts/rgs_lookup.py --search kas --nivo 4
```

If you add codes to the built-in seed, only add ones attested in a cited
source, and keep the "not authoritative — verify against the master"
notice intact. Never guess a niveau-4 code tail from the letters.

## How to contribute

1. **Fork** the repo on GitHub.
2. **Branch**, named for the change kind:
   - `fix/nt20-entrypoint-citation`
   - `update/rgs-39-release`
   - `docs/omslag-clarification`
   - `trigger/false-fire-on-non-dutch`
3. **Make focused changes.** One logical change per PR.
4. **Run the local checks** (above) and paste output into the PR.
5. **Open a PR** with a clear description, citing a primary source (URL +
   version/date) for every factual claim added or changed.
6. **Respond to review.** Source citations may be requested for claims that
   look right but are uncited.

## PR checklist

- Type of change identified
- Primary-source citation (URL + version/date) for every new/changed claim
- `references/sources.md` updated (new rows; superseded rows marked)
- Vendor-/harness-neutral language preserved
- `SKILL.md` still under 32 KiB
- Script still compiles and the smoke tests pass
- Honest-gap notes preserved or added where applicable

## Reporting bugs and gaps

Issues are most actionable when labelled by kind:

- **Source correction** — "the skill says X but the RGS master / SBR says Y"
- **Version update** — "RGS 3.9 / NTxx changed Z; update files A and B"
- **Software behaviour** — "MoneyBird/Exact now does this differently"
- **Trigger misfire** — "skill fires on X but shouldn't / misses Y"
- **Script bug** — anything in `rgs_lookup.py`
- **Enhancement** — proposals for new content or structure

For anything that could affect **filing integrity** (a code or rule in the
skill that would produce a non-compliant SBR/jaarrekening/aangifte), email
**contact@doc2ixbrl.com** before filing publicly.

## License

By contributing you agree your contribution is licensed under the
repository's MIT License.
