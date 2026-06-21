# Security Policy

This repository is an AI-agent skill: markdown reference material plus a
small, dependency-light Python lookup script. It executes no network calls
on its own and ships no secrets. The realistic risk surface is:

1. **Filing-integrity defects** — a code, rule, or instruction in the skill
   that would lead an agent (or a person) to produce a **non-compliant**
   Dutch SBR / jaarrekening / belastingaangifte, or to book to a wrong/
   superseded RGS code. We treat these with the same seriousness as a
   security bug, because the downstream consequence is regulatory.
2. **Script safety** — any way `scripts/rgs_lookup.py` could be made to do
   something unexpected with a crafted input file.
3. **Supply chain** — the GitHub Actions workflows and their pinned actions.

## Reporting a vulnerability

**Please do not open a public issue for a security or filing-integrity
problem.** Instead, use one of:

- **GitHub private vulnerability reporting** — the "Report a vulnerability"
  button under the repository's **Security** tab (preferred; keeps the
  report private until a fix ships).
- **Email** — **contact@doc2ixbrl.com**, subject line starting `SECURITY:`.

Include: what's wrong, the file/line or RGS code involved, the impact (e.g.
"would file an invalid OB-aangifte"), and a primary-source citation if the
issue is a correctness/compliance claim.

## What to expect

- Acknowledgement within a few working days.
- An assessment, and — for confirmed issues — a fix on a private branch,
  merged once verified.
- Credit in the release notes if you'd like it (tell us your preferred name).

## Scope notes

This skill is **not** legal, accounting, tax, or filing advice (see the
README disclaimer). A report that the skill is "not a substitute for an
accountant" is out of scope; a report that a specific code/rule/instruction
is **wrong** and would cause a non-compliant filing is firmly in scope.
