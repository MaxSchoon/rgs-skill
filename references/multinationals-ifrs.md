# RGS for multinationals, IFRS, consolidation & ESEF

> Read this when a task involves foreign entities, group reporting, IFRS, or listed-
> company filing. The honest bottom line: **RGS is a Dutch-GAAP / MKB instrument. It
> does not do IFRS or consolidation.** Knowing where its scope ends prevents expensive
> mistakes.

## Bottom line up front

RGS is a **reference classification for the Dutch SBR reporting chain** (Belastingdienst,
KvK, CBS, banks), anchored in **Dutch law and Dutch GAAP** (Besluit modellen jaarrekening,
RJ Richtlijnen, Nederlandse Taxonomie). It was **founded with an explicit MKB focus**
("focus primair op MKB", based on SME audit files averaging ~220 ledger accounts). For a
Dutch BV in an international group, RGS is useful **only at the Dutch local/statutory
ledger level**. Group-level IFRS consolidation and listed-company ESEF reporting live in
an **entirely separate XBRL world** (the IFRS Accounting Taxonomy / ESEF / the KvK IFRS
extension taxonomy).

## RGS ↔ IFRS — what exists, what doesn't

- **There is no IFRS-oriented RGS and no RGS→IFRS taxonomy mapping.** The RGS Taxonomie
  bridges RGS codes only to Dutch SBR reports. No entrypoint maps RGS to the IFRS
  Accounting Taxonomy.
- **An IFRS taxonomy exists in NL — but separately, inside the KvK/SBR Business Register
  taxonomy, not inside RGS.** The KvK taxonomy "is a concatenation of the IFRS accounting
  taxonomy as published by the IFRS Foundation and the associated labels … as published
  by ESMA" (it imports all IFRS elements via `kvk-annual-report-ifrs-ext.xsd`). That is
  how a Dutch entity filing IFRS accounts tags them at the KvK — unrelated to RGS.
- **RGS's English capability is thin.** Officially, "RGS is currently only available in
  Dutch." A *dataset of English labels* (based on NT15/FT15) exists as a translation aid,
  with the caveat that one reference code can map to multiple taxonomy concepts. It is
  **not** an international schema and unsuitable as a group-wide CoA standard for
  non-Dutch entities.
- **NL GAAP vs IFRS is a measurement/recognition gap, not a coding gap.** A ledger
  classification cannot bridge it (hence EY's and Deloitte's annual "IFRS vs NL GAAP"
  comparison guides). Conversion to IFRS is an accounting exercise, typically at group level.

## Consolidation & foreign subsidiaries

- RGS has **some** group/foreign codes — e.g. domestic/foreign splits like
  `WFbeRlmRgi` (rentebaten groepsmaatschappijen *binnenland*) vs `WFbeRlmRgu`
  (*buitenland*), and `BEivAvd` "Aandeel van derden" (minority interest) — but the latter
  is explicitly "niet in de boekhouding zelf opgenomen … alleen bedoeld voor een
  geconsolideerde balans".
- **Consolidation mechanics live outside RGS**, on a consolidatiestaat (elimination of
  participations and intercompany transactions; integral vs proportional methods). RGS
  provides classification codes only — **no consolidation logic, no elimination
  automation, no minority-interest computation.**
- **Multi-currency / foreign-operation translation** is an RJ (or IFRS) topic — RJ 122
  (vreemde valuta, functional vs presentation currency), RJ 217 (consolidatie), RJ 260
  (intercompany). **RGS has no currency dimension**; it is a single-currency ledger
  classification. Foreign subsidiaries in another functional currency must be translated
  by accounting rules outside RGS.
- **The standard two-track pattern** (per OrangeTax, Baker Tilly): keep **Dutch-GAAP local
  books on RGS**, then **convert/translate to IFRS at group level** for consolidation.
  Subsidiaries of IFRS groups may still keep Dutch GAAP for their local statutory filings.

## Extensibility — there is no "RGS Expander"

There is **no official product called "RGS Expander."** The sanctioned extensibility
mechanism is **"extensies" (extensions)**:
- The reference *number*'s 9th position carries an extension type: `0`=standaard,
  `1`=Fiscaal, `2`=Branche, **`3`=Concern**, **`4`=Onderneming**, `5–9`=vrij. (`3`/`4`
  exist precisely for group- and entity-specific accounts.)
- The reference *code* can be extended after a separator: `.` for object identification
  (e.g. an IBAN per bank account), `:` for codification.
- **Compliance rule:** while citing RGS as the standard you may *append* extensions but
  **not alter standard codes**; structural additions go to the beheerorganisatie.
- **Extensions are self-managed and outside central governance** — so they are **not
  mapped to SBR/IFRS** and break cross-company comparability. GBNED candidly advises
  against them ("verre van duidelijk en raden we dan ook af").
- **Implication for groups:** you *can* use `3`(Concern)/`4`(Onderneming) extensions or
  `.`-suffixed codes for intercompany/foreign accounts where standard codes don't suffice
  — but you buy internal structure, not external interoperability.

## ESEF / iXBRL for listed companies (separate from RGS)

- **ESEF and RGS are separate worlds.** ESEF requires EU-listed issuers to file the annual
  financial report in XHTML and tag the **consolidated IFRS statements** with the **ESEF
  taxonomy** (IFRS Foundation taxonomy extended by ESMA), with issuer extensions
  "anchored" into it. RGS plays no role. AFM: tagging is mandatory only for IFRS
  consolidated statements — "bij andere verslaggevingsstelsels is tagging niet toegestaan."
- **KvK is converging on ESEF for large entities** — but still via the IFRS/NL-GAAP
  taxonomy, **not RGS**: a mandatory ESD (entity-specific disclosure) extension taxonomy,
  Report Package, ESEF-style anchoring. IFRS-EU consolidated accounts must be filed in
  iXBRL at KvK.
- **Where RGS sits:** upstream, in the *bookkeeping ledger* of (mainly smaller) Dutch
  entities feeding *Dutch SBR* filings. ESEF/iXBRL is downstream *external reporting* of
  IFRS consolidated statements by large/listed entities. **They do not connect.**

## Practical recommendation — Dutch BV in an international group

1. **Use RGS only for the Dutch statutory/local ledger.** It genuinely helps there:
   standardizes the chart, auto-feeds VPB/IB/BTW and KvK SME filings, enables
   benchmarking, widely supported by Dutch software. Prefer **RGS MKB** if micro/klein.
2. **Don't expect RGS to do group reporting.** IFRS consolidation is a separate accounting
   + tooling layer (group reporting / consolidation software).
3. **Adopt the two-track model:** Dutch-GAAP local books on RGS → convert to IFRS at group
   level for consolidation.
4. **If the BV itself must file IFRS with KvK** (elected IFRS, or it's the listed parent),
   it files **iXBRL using the KvK IFRS / ESD extension taxonomy** (and, if listed, **ESEF**
   with AFM) — *not* RGS.
5. **For intercompany/foreign tracking in the ledger,** use RGS's existing binnenland/
   buitenland group codes; resort to self-managed Concern/Onderneming extensions only
   where standard codes don't suffice, accepting the comparability cost.
6. **English/multilingual:** the English-label dataset is a convenience only; RGS proper
   is Dutch-only.

## Honest limitations of this analysis

- "RGS Expander" was **not found as a named product** — the standard's extensibility is
  "extensies", documented above. Not invented to match the brief's term.
- No single official "RGS is not for multinationals" pronouncement was located; the scope
  conclusion is **well-evidenced inference** from RGS's governance/mapping (Dutch SBR
  only), its MKB-focused founding record, and the fact that IFRS/ESEF run through entirely
  separate taxonomies. NBA co-developed RGS but published no scope-limiting paper.
