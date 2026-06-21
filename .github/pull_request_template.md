<!--
Thanks for contributing to the RGS skill! Keep PRs focused — one logical
change each. Cite a primary source (URL + version/date) for every factual
claim you add or change. See CONTRIBUTING.md.
-->

## What this changes

<!-- A short summary. Link any related issue (e.g. "Closes #12"). -->

## Type of change

- [ ] Source correction (skill said X, the RGS master / SBR says Y)
- [ ] Version update (new RGS / NT version)
- [ ] Software behaviour (MoneyBird/Exact/etc. changed)
- [ ] Trigger fix (skill fires when it shouldn't / misses when it should)
- [ ] Script change (`scripts/rgs_lookup.py`)
- [ ] Docs / structure
- [ ] Other:

## Source citations

<!--
For every technical/factual claim added or changed, cite the authoritative
URL you actually fetched, with its version/date. Add or update the matching
row in references/sources.md.
-->

-

## Checklist

- [ ] One logical change; focused diff
- [ ] Primary-source citation (URL + version/date) for every new/changed claim
- [ ] `references/sources.md` updated (new rows added; superseded rows marked)
- [ ] Language stays vendor-/harness-neutral (product behaviour labelled as such)
- [ ] `SKILL.md` still under 32 KiB and the frontmatter `description` under 1024 chars
- [ ] Script still compiles and the seed smoke tests pass:
      `python3 -m py_compile scripts/rgs_lookup.py`
      `python3 scripts/rgs_lookup.py --validate WBedAlkOal`
- [ ] Honest-gap notes preserved or added where a claim couldn't be verified

## Notes for the reviewer

<!-- Anything that helps review: a tricky citation, an intentional gap, a
     multi-agent review you ran, etc. -->
