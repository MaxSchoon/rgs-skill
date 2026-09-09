---
reference_id: multinationals-ifrs
verified_on: 2026-09-09
rgs_version: "3.8 definitive"
---

# RGS for groups, IFRS, consolidation, and ESEF

*Part of the RGS Skill by Ontos B.V. (Max Schoon, Doc2iXBRL) — <https://github.com/MaxSchoon/rgs-skill>. Licensed CC BY 4.0. If you use this material, you must credit Ontos B.V. (see `ATTRIBUTION.md`).*

**Load this when:** a Dutch entity sits in an international group, someone
wants RGS as a group chart of accounts, or the question mentions IFRS,
consolidation, foreign subsidiaries, or ESEF.

**Do not load this when:** the entity is a stand-alone Dutch business and the
question is a local booking or filing (`references/structure-and-codes.md`,
`references/reporting-compliance.md`).

## Contents

- [Where RGS stops](#where-rgs-stops)
- [What RGS does offer a group](#what-rgs-does-offer-a-group)
- [Recommendation](#recommendation)
- [Sources](#sources)

## Where RGS stops

- **Dutch reports only.** The RGS Taxonomie 3.8 maps to Belastingdienst,
  KvK NL-GAAP, SBR Wonen and bank entrypoints and to nothing else; there is
  no entrypoint to the IFRS Accounting Taxonomy [S1]. The KvK NT20 directory
  carries `nlgaap` entrypoints only; the KvK Inline XBRL taxonomy that
  imports the IFRS taxonomy for IFRS filers is a separate tree documented in
  the iXBRL skill (<https://github.com/MaxSchoon/ixbrl>,
  `references/jurisdictions/nl-sbr.md`) [S2].
- **Dutch only.** The standard "is currently only available in Dutch". The one
  English-label dataset is based on RGS 3.3 and the NT15/FT15 labels, is
  "not an official product that will be periodically updated", and a code can
  carry several translations because it maps to several concepts [S3] [S4].
- **No consolidation logic.** RGS is a classification of accounts; nothing in
  the workbook or the taxonomy eliminates intercompany balances or computes
  minority interests. `BEivAvd` "Aandeel van derden" exists as a rubriek for a
  consolidated balance, and rente codes distinguish groepsmaatschappijen
  binnenland from buitenland (`WFbeRlmRgi`, `WFbeRlmRgu`, with omslag pairs
  `WFbeRlsRgi`, `WFbeRlsRgu`) [S5].
- **ESEF is another world.** Listed issuers tag the consolidated IFRS
  statements with the ESEF taxonomy, an ESMA extension of the IFRS taxonomy,
  and file a report package with the AFM; RGS plays no part [S6].

## What RGS does offer a group

A Dutch subsidiary keeps its statutory ledger on RGS and gets the local SBR
filings, the BTW and VPB returns, and Dutch benchmarking from it
(`references/reporting-compliance.md`). For group-specific accounts the
sanctioned mechanism is an extension: the number's extensiecode `3` (concern)
or `4` (onderneming), or a `.`/`:` suffix on the code; extensions are
self-managed, outside central governance, and therefore not mapped to any SBR
report [S7]. GBNED advises against relying on them [S8].

## Recommendation

1. Use RGS for the Dutch statutory ledger only, at niveau 4.
2. Convert to IFRS and consolidate in the group's reporting layer; RGS has no
   currency dimension and no IFRS concepts.
3. If the Dutch entity itself files IFRS accounts with the KvK or is a listed
   issuer, that is an iXBRL question: hand over to the iXBRL skill.
4. Track intercompany positions with the existing binnenland/buitenland
   codes before reaching for extensions; where an extension is unavoidable,
   accept that it breaks comparability outside the group.

## Sources

- **[S1]** NT20_RGS_20251210.zip (RGS Taxonomie 3.8), `entrypoints/` listing: bd, bzk, frc, kvk only. Taakgroep RGS. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/NT20_RGS_20251210.zip> [viewed 2026-09-09]. Tier 1.
- **[S2]** Index of /nt20/kvk/20251210/entrypoints/ (all `nlgaap`). Logius, nltaxonomie.nl. Available from: <http://www.nltaxonomie.nl/nt20/kvk/20251210/entrypoints/> [viewed 2026-09-09]. Tier 1.
- **[S3]** English. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/english> [viewed 2026-09-09]. Tier 1.
- **[S4]** Dataset Engelse labels (`20210913 RGS NL en EN labels.xlsx`). Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/dataset-engelse-labels> [viewed 2026-09-09]. Tier 1.
- **[S5]** RGS 3.8-def.xlsx, sheet `Totaal-RGS3.8-def` (codes `BEivAvd`, `WFbeRlmRgi`, `WFbeRlmRgu` and their omslagcodes). Taakgroep RGS, 2025-12-10. Downloaded from <https://www.referentiegrootboekschema.nl/sites/default/files/kennisbank/RGS%203.8-def.xlsx> [viewed 2026-09-09]. Tier 1.
- **[S6]** Jaarlijkse verslaggeving in ESEF. AFM. Available from: <https://www.afm.nl/nl-nl/sector/effectenuitgevende-ondernemingen/financiele-en-duurzaamheidsverslaggeving/jaarlijkse-verslaggeving-in-esef> [viewed 2026-09-09]. Tier 1.
- **[S7]** Het werken met extensies. Taakgroep RGS. Available from: <https://www.referentiegrootboekschema.nl/het-werken-met-extensies> [viewed 2026-09-09]. Tier 1.
- **[S8]** Extensies Referentie GrootboekSchema - RGS. Onderzoeksbureau GBNED, boekhoudplaza.nl. Available from: <https://www.boekhoudplaza.nl/wiki_uitleg/25/Extensies_Referentie_GrootboekSchema_RGS.htm> [viewed 2026-09-09]. Tier 2.
