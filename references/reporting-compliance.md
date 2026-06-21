# RGS → statutory reporting & tax compliance

> This is *why* RGS is worth the effort: one RGS-coded ledger feeds KvK annual
> accounts, Belastingdienst returns (IB/VPB/OB), CBS and bank reports — without
> re-keying. Read this when the task is about filings, taxonomy versions, or the
> jaarrekening.

## The mechanism: RGS → SBR → filing

The principle is verified on Belastingdienst.nl: with SBR you record data once, in a
standard way, then reuse it for many reports. The chain has three layers:

1. **Grootboekrekening → RGS code.** Each ledger account is tagged with an RGS
   referentiecode. In the XML Auditfile Financieel (XAF) this is the `LeadReference`
   element on `ledgerAccount`; `LeadCrossReference` carries the omslagcode for negative
   balances.
2. **RGS code → SBR taxonomy concept.** The **RGS Taxonomie** (an XBRL artifact, built
   on the Nederlandse Taxonomie Architectuur) links each RGS code to a taxonomy element
   via Generic Link References. The current version (Toelichting v15) covers **32 SBR
   rapportages**, each a separate **entrypoint**. Historically ~85% of RGS elements map
   1:1 to taxonomy concepts; the rest need summation or breakdown.
3. **SBR concept → filing.** The tagged data is rendered as XBRL/iXBRL and submitted via
   **Digipoort** (government) or the **Bancaire Infrastructurele Voorziening** (banks).

A simpler, widely-used alternative to the full taxonomy is the **RGS Brugstaat** — a
standardized XML of RGS-based ledger balances handed to fiscal/reporting software (e.g.
for the winstaangifte IB/VPB). This is what most SME packages expose, MoneyBird included.

**Mapping types** (referentiegrootboekschema.nl "Instructie mapping RGS en SBR"):
*balanced* vs *unbalanced* mapping (whether the target sub-report stays in balance at
each level), and *direct* vs *indirect* (an "Overige …" post is mapped indirectly as
the level total minus the directly-mapped posts).

## ⚠️ The NT version trap: NT20 ≠ year 2020

The Nederlandse Taxonomie version number tracks the **reporting/tax year**, not the
calendar year:

- **NT20 = reporting year 2026** — the **current production taxonomy for filings made in
  2026.**
- NT19 = reporting year 2025 (superseded for new filings).
- NT21 = reporting year 2027 — in development; goes to production **9 December 2026**.

**For any 2026 compliance work, target NT20 and RGS 3.8 (`NT20_RGS_20251210`).** Concretely:
- **Belastingdienst** = NT20 (`NT20_BD_20251210`, with point releases NT20.1
  `20260218` / NT20.2 `20260916`, and corrected `NT20_20260126.zip` for ICP 2026). NT20
  covers: aangifte VPB 2025, voorlopige aanslag VPB 2026, aangifte IB 2025, aangifte OB
  2026, ICP 2026, suppletie OB 2026, VIA 2025.
- **KvK** jaarverantwoording for **boekjaar 2025** (filed in 2026) is under NT20.
- **RGS Taxonomie 3.8** (definitief 2 Feb 2026) maps RGS 3.8 to KvK (NT20),
  Belastingdienst (NT20), SBR Nexus (FT20), SBR Wonen (dVi2025-NT20).

> Note the boekjaar-vs-aangiftejaar mismatch *within* NT20: KvK covers boekjaar 2025
> while several BD streams cover belastingjaar 2026 (OB/ICP) and 2025 (VPB/IB). Don't
> assume one year per taxonomy generation. Always pick the sub-release matching the
> specific berichtstroom (the ICP correction is mandatory for ICP 2026).

## KvK annual accounts (deponering jaarrekening)

- **Legal basis:** art. **2:394 BW** requires depositing the jaarrekening with the
  Handelsregister; the *Besluit elektronische deponering* mandates **SBR**.
- **Mandatory SBR/XBRL by class:** micro & klein since boekjaar 2016; middelgroot since
  2017; **groot since boekjaar 2025** (the long-standing large-company exception lapsed
  via the 18 Dec 2024 amendment, for boekjaren starting on/after 1 Jan 2025). Only
  remaining exception: uitgevende instellingen (art. 5:25o Wft).
- **Formats:** classic SBR (XBRL instance) or European **XHTML/iXBRL** (available from
  boekjaar 2024; large companies now file iXBRL).
- **Routes:** micro/klein may use the free **Zelf Deponeren** portal or software via
  SBR; middelgroot/groot must use software via SBR with a **PKIoverheid certificate**.
  Deadline: within **12 months** of boekjaar end.
- **RGS → line items:** the RGS Taxonomie ships a per-class mapping linkbase
  (`rgs-mapping_jaarverantwoording-{year}-nlgaap-{class}.xml`) for each entrypoint
  (`...nlgaap-micro/-klein/-middelgroot/-groot`, plus `-publicatiestukken`), so the same
  RGS-coded ledger fills the right publication model.

## Belastingdienst (IB / VPB / OB)

SBR is **mandatory** for these via Digipoort (PKIoverheid certificate).

- **IB / VPB — the winstaangifte flow:** the RGS-coded bookkeeping produces an **RGS
  Brugstaat** (or feeds the RGS Taxonomie directly) into fiscal software, which maps to
  the `bd-rpt-ihz-aangifte-{year}` (IB) and `bd-rpt-vpb-aangifte-{year}` (VPB)
  entrypoints (linkbases `rgs-mapping_ihz-aangifte-{year}.xml` /
  `rgs-mapping_vpb-aangifte-{year}.xml`). This is where RGS pays off most.
- **OB / BTW:** `bd-rpt-ob-aangifte-{year}` (+ `ob-suppletie`, `icp-opgaaf`). Largely
  driven by RGS turnover/VAT codes; far simpler than the winstaangifte. (Reverse charge —
  *btw verlegd* — for foreign B2B services maps to OB rubriek 4a/4b with self-accounted
  BTW; pick the dedicated reverse-charge purchase rate, not plain 0%.)

## Title 9 Book 2 BW alignment

- **Title 9 of Book 2 BW** ("De jaarrekening en het bestuursverslag") sets the statutory
  requirements. The concrete line-item layouts come from the **Besluit modellen
  jaarrekening** (BWBR0003648): balans = model A/B (C/D if small), winst-en-verliesrekening
  = model E/F (I/J if small); micro (2:395a) is model-exempt; banks/insurers use K–S.
- **RGS rubrieken align to these models by construction** — RGS levels were derived from
  the NT/BT taxonomy concepts and aligned to the BW2 models, so the RGS hoofdrubrieken
  structurally mirror the statutory balans/W&V models *and* the SBR jaarverantwoording
  entrypoints at once. That is exactly why RGS standardization makes the annual report
  easier to compile (the user's stated goal).

## Mapping / koppeltabel resources

Official downloads (referentiegrootboekschema.nl Kennisbank, RGS 3.8 category):
- **`NT20_RGS_20251210`** — the RGS Taxonomie ZIP (RGS 3.8 → NT20), the XBRL koppeltabel.
- **"RGS 3.8 mapping naar SBR NT20 concepten"** — human-readable mapping (RGS code → SBR concept).
- **"Toelichting RGS 3.8 mapping naar SBR NT20 concepten"** + **"Toelichting RGS
  Taxonomie versie 15"** (method: Generic Link References, 32 entrypoints).
- **`http://nltaxonomie.nl/`** — publication root (`nt20/`, `nt21/`, `rgs/`).
- **Instructie mapping RGS en SBR** — the methodology (balanced/unbalanced, direct/indirect).

**Logius role:** via the Kenniscentrum XBRL, Logius beheert the Nederlandse Taxonomie and
the NTA, runs Digipoort, and supports the uitvragende partijen (Belastingdienst, DUO,
KVK, SBR-Wonen). In the taxonomy split Logius owns the generic "SBR" and BW2-specific
"VenJ" modules; the **RGS module is owned by RGS** and contains the mapping from RGS to
parts of the CBS, KvK, BD and FRC taxonomieën.

## Caveats

- **NT20 ≠ 2020** is the #1 trap — restated because the digits invite misreading.
- **Entrypoint count drifts by version** (v13.b cited 28, v15 cites 32) — confirm against
  the exact RGS Taxonomie version you deploy.
- **RGS Brugstaat** exact XML structure should be confirmed against the RGS spec, not a
  single vendor page.
- **wetten.overheid.nl** consolidated text for the Besluit modellen jaarrekening may lag;
  verify article numbers against the live version before quoting verbatim.
- **RJ (Richtlijnen voor de Jaarverslaggeving)** supplement BW2 for middelgroot/groot but
  are not free/online and not part of the statutory RGS↔taxonomy koppeltabel.
