<!--
Thanks for contributing to the RGS skill. Keep a PR to one logical change.
Every factual claim you add or change needs a primary source you fetched,
cited with an `[Sn]` marker and a `**[Sn]**` entry (URL, date, tier) in the
reference's Sources list. See CONTRIBUTING.md.
-->

## What this changes

<!-- A short summary. Link any related issue (e.g. "Closes #12"). -->

## Type of change

- [ ] Source correction (the skill said X; the RGS workbook, SBR or the law says Y)
- [ ] Version update (new RGS or NT version)
- [ ] Software behaviour (MoneyBird or another package changed)
- [ ] Trigger fix (skill fires when it should not, or misses when it should)
- [ ] Script change (`scripts/rgs_lookup.py`)
- [ ] Docs or structure
- [ ] Other:

## Sources

<!--
For every claim added or changed: the URL you fetched, the page or file
date or version, and the `[viewed YYYY-MM-DD]` date, as it appears in the
reference's Sources list.
-->

-

## Checks run

<!-- Paste the output of the local checks in CONTRIBUTING.md. -->

## Checklist

- [ ] One logical change; focused diff
- [ ] `[Sn]` marker on every new or changed claim, resolving to a Sources entry with URL and viewed date
- [ ] `verified_on` and `rgs_version` front matter updated on every reference touched
- [ ] Language stays vendor- and harness-neutral; product behaviour is labelled as that product's
- [ ] `python3 tests/check_skill.py`, `npx --yes markdownlint-cli2@0.18.1` and `python3 -m unittest discover -s tests` pass
- [ ] Gaps stated as gaps where a claim could not be verified

## Notes for the reviewer

<!-- A tricky citation, an intentional gap, a review you ran, etc. -->
