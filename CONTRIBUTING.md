# Contributing to the RGS Skill

This skill is read by AI agents and by people keeping real Dutch
administraties, so its accuracy reaches filed returns. Contributions are
welcome from bookkeepers, accountants, tax advisers, software vendors, RGS
and SBR insiders, and engineers building bookkeeping tools.

## What this project is

- `SKILL.md`: the agent entry point (intake, pins, invariants, index). No
  domain facts of its own.
- `references/`: one file per topic, each with sources.
- `scripts/rgs_lookup.py`: a standard-library validator over the official
  workbook.
- `tests/`: the structural gate and the script's unit tests.

No harness-specific assumptions: no "use tool X", no vendor-only
instructions presented as universal.

## Three rules

### 1. A primary source for every claim

Every factual statement in a reference carries an `[Sn]` marker that
resolves to a `**[Sn]**` entry in that file's `## Sources` list. An entry
gives the title, the publisher, the page or file date or version where the
page states one, `Available from: <URL>`, `[viewed YYYY-MM-DD]`, and the
tier. Dates are ISO 8601 (`YYYY-MM-DD`). Prefer the publisher's permalink
over a search result, and the workbook or zip itself over a page about it.

Authority, in order: referentiegrootboekschema.nl (Kennisbank workbooks,
taxonomy zips, explanatory pages, news), nltaxonomie.nl, sbr-nl.nl, kvk.nl,
belastingdienst.nl, wetten.overheid.nl and the Staatsblad (tier 1);
boekhoudplaza.nl and softwarepakketten.nl by Onderzoeksbureau GBNED
(tier 2, the practitioner reference, not the standard); vendor
documentation (tier 3, authoritative for that product only).

Cite the version you checked: RGS codes, filters and omslagcodes change
between versions. Where the workbook is the source, say which sheet and
that you measured it (the script is the instrument).

### 2. State gaps as gaps

If you could not verify something, say so in the text rather than smoothing
it over: "not found in the 3.8 workbook", "GBNED documents this; the owner's
pages are silent", "observed in the API; not in its documentation". A stated
gap is a contribution; a confident guess is a regression. When two sources
disagree (the 9-digit number in the velddefinities versus the 7-digit layout
in the workbook), keep both and say which one the data follows.

### 3. Vendor- and harness-neutral language

Do not name agent harnesses, IDEs or assistants, or hard-code one runtime's
tool names. Bookkeeping-software behaviour (MoneyBird, AFAS, and so on) is in
scope, labelled as that product's behaviour and dated.

## Reference shape (enforced)

Each `references/*.md` has:

1. Front matter with `reference_id` (equal to the file name), `verified_on`
   (`YYYY-MM-DD`) and `rgs_version`.
2. One H1, then a `**Load this when:**` line and a `**Do not load this
   when:**` line, decidable from the agent's situation.
3. `## Contents` as the first H2, listing every H2 that follows, with links
   that resolve.
4. Named sections, never numbered.
5. `## Sources` as the last H2, with `- **[Sn]** …` entries; every marker in
   the body resolves, every entry is cited, every entry has a URL and a
   viewed date.

`tests/check_skill.py` checks all of it, plus SKILL.md's size (under 32 KiB
and 500 lines) and description (under 1024 characters), and that every
reference is linked from SKILL.md.

## Freshness

RGS ships a new version each December (alfa in July, bèta in October) and
the RGS Taxonomie follows in January; the NT generation enters production
in December. Before changing a version-sensitive claim, read
`referentiegrootboekschema.nl/actueel` and the SBR release calendar, then
update the tables in `references/versions-governance.md` and
`references/reporting-compliance.md`, the pin in `SKILL.md`, and the
`rgs_version` and `verified_on` front matter of every reference you touched.

## Script

`scripts/rgs_lookup.py` must stay standard-library only and runnable on
Python 3.10+. Its behaviour on the official layout is pinned by
`tests/test_rgs_lookup.py`, which generates a workbook fixture with the real
header layout; a bug fix lands with a test that fails without it. Seed codes
are added only after checking them in the official workbook, with the
official description.

## Local checks

```bash
python3 tests/check_skill.py
npx --yes markdownlint-cli2@0.18.1
python3 -m py_compile scripts/rgs_lookup.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/rgs_lookup.py --validate WBedKanKoa      # seed smoke test
```

Paste the output into the pull request.

## How to contribute

1. Fork, then branch by change kind: `fix/omslag-count`,
   `update/rgs-39-definitive`, `docs/moneybird-status-codes`,
   `trigger/false-fire-on-belgian-pcmn`.
2. One logical change per pull request.
3. Run the local checks and paste the output.
4. Open the PR with the template; cite the sources you fetched.
5. Respond to review; a citation may be requested for anything uncited.

## Reporting bugs and gaps

Use the issue templates: source correction, version update, trigger or
bug, enhancement. For anything that could affect filing integrity, email
**contact@doc2ixbrl.com** before filing publicly (see `SECURITY.md`).

## License

By contributing you agree your contribution is licensed under the
repository's MIT License.
