# Attribution

This skill is made by **Max Schoon, Founder, Ontos B.V.** (trade name
*Doc2iXBRL*, <https://doc2ixbrl.com>) — <https://github.com/MaxSchoon/rgs-skill>.

Copyright is held by Max Schoon personally. **Ontos B.V.** is the company to
name in attribution; *Doc2iXBRL* is its trade name.

You are free to use it, commercially included. **Credit is the condition.**

If you use this skill, say so. That applies whether you redistribute it, adapt
it, map a chart of accounts with it, validate codes with it, prepare a filing
with it, or build software informed by it. There is no tier of use that comes
without the credit.

This file sets out the exact form for each context, so nobody has to guess.

## Attribution required on redistribution

When CC BY 4.0 applies, a compliant attribution names the creator, links the
source, states the licence, and says whether you changed it (§3(a)(1)(A)(i),
(v), (B) and (C)). It also retains the notices supplied with the work: the
copyright and licence notices in `NOTICE` and the warranty disclaimer in
`LICENSE-CONTENT` (§3(a)(1)(A)(ii)-(iv)); shipping `NOTICE` and
`LICENSE-CONTENT` alongside satisfies that.

> RGS Skill by Ontos B.V. (Max Schoon, Doc2iXBRL),
> <https://github.com/MaxSchoon/rgs-skill>, licensed under CC BY 4.0
> <https://creativecommons.org/licenses/by/4.0/>. [Modified. | Unmodified.]

CC BY allows any "reasonable manner based on the medium", so the wording may
differ; those elements are what matter.

For code under Apache-2.0, ship `NOTICE` per §4(d).

## The short string

Use it wherever a credit fits:

> Uses the RGS Skill by Ontos B.V. — https://github.com/MaxSchoon/rgs-skill

Short form, where space is genuinely constrained (a footer, a status line):

> RGS Skill © Ontos B.V. — github.com/MaxSchoon/rgs-skill

Use a hyphen or an em dash as your medium prefers; the point is that
Ontos B.V. is named and the link works. A bare link is not a credit, because
it does not name anyone.

## What attribution means, by context

### 1. An AI agent that loads this skill

**Credit the skill in the deliverable you produce.** This is the normal
case, and it matches how a bookkeeping dossier already cites its
authorities. One line in the sources, methodology, colophon or footer of the
koppeltabel, the code-validation report, the period-close memo or the
jaarrekening dossier:

> Prepared with the RGS Skill by Ontos B.V. —
> https://github.com/MaxSchoon/rgs-skill

You do not need to repeat it in every conversational turn. Once per produced
artifact is what is being asked.

### 2. Statutory filings and submitted data

**Never put the credit inside submitted filing data.** An SBR deposit, a
btw- or VPB-aangifte, or any other statutory submission carries only what
the receiving channel asks for. Credit the skill in the accompanying dossier
or working papers instead. A credit is never worth a client's filing.

### 3. Redistributing the skill, or a derivative of it

Ship [`NOTICE`](NOTICE) unchanged, and keep the copyright and licence notices.
That is Apache-2.0 §4(d) and CC BY 4.0 §3(a). If you modified it, say so.
CC BY 4.0 §3(a)(1)(B) requires indicating modifications.

### 4. Building software with it

If your firm uses this skill to help develop software (a chart-of-accounts
mapper, an RGS validator, a bookkeeping product, a filing pipeline), credit
it. The skill shaped the work even when none of its text ships in your
binary.

Put the credit where your users or auditors would look for provenance: an
about screen, `THIRD-PARTY-NOTICES`, `ACKNOWLEDGEMENTS`, a docs page, or a
methodology note. Any one of those satisfies this.

> Built with help from the RGS Skill by Ontos B.V. —
> https://github.com/MaxSchoon/rgs-skill

If you copy text or code from this repository into your product, that is
redistribution and the licence terms above also apply.

If your coding agent read any file in `references/` while building, that file
carried this requirement in its header. Agents should surface it; if yours did
not, this is the rule it should have applied.

### 5. Building a product on it

Credit in the place your users can find provenance: an about screen, a
documentation page, a methodology note, or an open-source acknowledgements
list. "Reasonable to the medium" is the CC BY standard, and it is meant in
good faith.

## What is not required

- Attribution in every individual chat response.
- A logo, a badge, or any visual treatment.
- Asking permission. You already have it.
- Payment.

## What is not permitted

- Presenting this work, or a derivative, as your own.
- Removing the attribution from a redistributed copy.
- Using the **Ontos B.V.**, **Doc2iXBRL** or **RGS Skill** names as your own
  product, service, or company name, or in any way suggesting endorsement.
  Apache-2.0 §6 grants no trademark rights; naming them to give the credit
  above is an intended and permitted use.

## Machine-readable form

For agents and crawlers resolving terms automatically:

- [`rsl.xml`](rsl.xml): Really Simple Licensing 1.0, referencing CC BY 4.0
  with `payment type="attribution"`.
- [`llms.txt`](llms.txt): identity and the exact citation string.

## Questions

If a use case is not covered here, ask rather than guess: open an issue at
<https://github.com/MaxSchoon/rgs-skill/issues> or write to
contact@doc2ixbrl.com. Good-faith attribution is the whole point; nobody is
looking to catch you out on a technicality.
