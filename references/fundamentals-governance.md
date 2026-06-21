# RGS fundamentals, governance & versioning

> Read this when you need to state *which RGS version is authoritative*, who governs
> it, or explain what RGS is and why it exists. For the day-to-day "which code do I
> book to" question, go straight to `structure-and-codes.md`.

## What RGS is

**RGS (Referentie GrootboekSchema)** is the Netherlands' standardized, uniform
reference chart of accounts. It is a fixed catalogue of reference *codes* (plus an
example reference account number and a standard description) that you map your own
ledger accounts onto **once**, after which the same bookkeeping can feed many
different reports — the "**boekhouden één keer, hergebruik voor meerdere
rapportages**" principle (book once, reuse for many reports).

RGS is the bookkeeping-side enabler of **SBR (Standard Business Reporting)**: by
tagging each grootboekrekening with an RGS code, the ledger can be rendered into
SBR/XBRL filings for the Belastingdienst, KvK, CBS and banks without re-keying.

RGS is a **reference classification, not a mandatory accounting standard**. The
official English page is explicit: it "is explicitly positioned as a reference
classification and not as a mandatory standard." You are never legally forced to use
RGS — but using it makes standardized reporting and benchmarking almost free, which
is exactly the user's goal here.

## Governance (current, post-Feb-2024 model)

RGS has been under **SBR governance since 2015**. After the 2024 SBR governance
reorganization the structure is:

- **Taakgroep RGS** — the central body that releases new versions and manages change
  requests (meldingen). Supported by three werkgroepen: **Semantiek** (content &
  mapping; assesses user change requests), **Techniek** (technical implementation &
  documentation), and **Implementatie & Communicatie**.
- **Logius** runs the SBR "Staf"/Stelselregie role and administers the taxonomy.
- Stakeholders / uitvragende partijen: **Belastingdienst, KvK, CBS, SBR Nexus**
  (banks/credit reporting), **SBR Wonen**, plus accountancy/bookkeeping bodies (e.g.
  **NOAB** collaborates on RGS MKB; **NBA** co-developed RGS).

**Change procedure:** users submit change requests via referentiegrootboekschema.nl;
Semantiek assesses, Techniek implements, the Taakgroep releases. SBR decisions use a
qualified (3/4) majority where unanimity isn't reached. **You may not change or
extend reference codes yourself while citing RGS as the standard** — structural
additions must be requested from the beheerorganisatie.

> ⚠️ **Terminology drift.** Older but still-online pages (e.g. fundamentvoor.nl 2017,
> rgs-wonen.nl 2019) describe an **Expertgroep RGS / Beheergroep RGS / Taskforce
> Implementatie** model. That is **superseded**. The Beheergroep's last formal act was
> the RGS Taxonomie 3.6 (19 Feb 2024); its work moved into the Taakgroep RGS. Use the
> Taakgroep model. "Beheergroep RGS" is still used colloquially, so don't be thrown by it.

## Versioning — the current authoritative version

**As of mid-2026 the current, authoritative, recommended version is RGS 3.8**
(definitive Excel released **10 December 2025**). The matching **RGS Taxonomie 3.8**,
mapping RGS 3.8 to **NT20** (KvK + Belastingdienst), **FT20** (SBR Nexus bank credit
reports) and **dVi2025-NT20** (SBR Wonen), went definitive **2 February 2026**
(artifact `NT20_RGS_20251210`). **RGS 3.7 and earlier are superseded.**

Version lineage (cumulative code counts, GBNED RGS Dashboard):

| Year | Version | ~Codes | Note |
|---|---|---|---|
| 2016 | 2.0 | 2,528 | |
| 2017 | 3.0 | 3,009 | Core ("kern") stable from here on |
| 2018–2021 | 3.1–3.4 | 3,754 → 4,641 | |
| 2022 | 3.5 | 4,740 | **The version MoneyBird currently maps to** |
| 2023 | 3.6 | 4,779 | |
| 2024 | 3.7 | 4,963 | Definitive Excel 3 Mar 2025; added MKB + woningcorporaties tabs |
| 2025 | **3.8** | **4,977** | **Current** — definitive Excel 10 Dec 2025 |

Because the **core has been stable since RGS 3.0**, the everyday balance/cost codes
are forward-compatible across 3.5 → 3.8. That matters for MoneyBird users: MoneyBird maps
to **RGS 3.5** (`taxonomy_version: "3.5"`, platform-controlled — you cannot force a newer
taxonomy via the API), but the codes you actually pick (e.g. `WBedAlkOal`) resolve to
the same accounts in 3.8, so reporting stays standard.

**Release cadence:** roughly one minor version per year, published Alfa → Bèta
(consultation, 4–6 weeks) → Definitief, with the definitive version landing around
December before the reporting year. Delivery is an **Excel workbook** (release notes on
the "Recap" tab) from the Kennisbank; the XBRL **RGS Taxonomie** ships separately and
slightly later.

> 🔄 **Re-verify after late 2026.** An RGS 3.9 cycle is plausible by late 2026 on the
> annual cadence. Before asserting "3.8 is latest" past that point, check
> referentiegrootboekschema.nl/actueel with Exa.

## Two things people confuse with "a new RGS version"

1. **RGS MKB** — *not* an official version and *not* a successor to the 3.x line. It
   is a derivative product of **Onderzoeksbureau GBNED (Gerard Bottemanne)** on
   boekhoudplaza.nl (launched 1 Oct 2023): a curated subset of standard RGS codes up to
   **niveau 4 only** (no niveau-5 mutaties, ~400–860 codes), re-numbered into a 5-digit
   decimal account scheme, with extra SME documentation (booking scenarios, KPIs).
   It uses standard RGS codes and stays compatible up to niveau 4. Note: official RGS
   *also* ships an "MKB" tab inside its Excel since 3.7 — that tab is separate from
   GBNED's RGS MKB product. **There is no "RGS 4.0."**
2. **The 2022 RGS Taxonomie architecture RfC** — a technical XBRL restructuring, not a
   content version bump.

## RGS Ready (software readiness)

There is **no official "RGS-certified" program**. The market term is **"RGS Ready,"**
a GBNED benchmark (criteria set with the former RGS Taskforce Implementatie): an
8-function yardstick for how well software supports RGS. Suppliers self-test for free;
results are published per supplier on **rgsready.nl** and **softwarepakketten.nl**.
There's a split: **RGS Ready for accountancy** (all 8 criteria, incl. auto-mapping
suggestions) vs **RGS Ready for entrepreneurs** (a few criteria relaxed). The official
RGS site endorses this as the de-facto check rather than running its own certification.
