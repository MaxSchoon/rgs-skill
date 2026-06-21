# RGS sources — validated register

> Every claim in this skill traces to a source here. **Validated 2026-06-21** via Exa
> search + fetch: each was checked for accessibility, recency, and whether it is current
> or superseded. Re-validate (especially version-sensitive rows) if using this skill
> after **late 2026** — an RGS 3.9 / NT21 cycle is expected.

## How to re-validate

Use whatever web search/fetch tools your agent runtime provides. The canonical "is this
still current?" check is **referentiegrootboekschema.nl/actueel**.
Treat referentiegrootboekschema.nl / sbr-nl.nl / logius.nl / belastingdienst.nl / kvk.nl
as **authoritative**; boekhoudplaza.nl & softwarepakketten.nl (GBNED / Gerard Bottemanne)
as **the de-facto practitioner reference** (expert commentary, not the formal standard);
vendor pages as **corroborating**.

## Tier 1 — Official / authoritative

| Source | Covers | Authority | Status (2026-06-21) |
|---|---|---|---|
| referentiegrootboekschema.nl/actueel | Latest releases, taxonomy news | RGS (Taakgroep) | **Current** — primary freshness check |
| referentiegrootboekschema.nl/Actueel/definitieve-versie-rgs-38-gepubliceerd | RGS 3.8 definitive (10 Dec 2025) | RGS | **Current (latest version)** |
| referentiegrootboekschema.nl/over-rgs | What RGS is; governance | RGS | Current |
| referentiegrootboekschema.nl/opbouw-rgs | 5-level hierarchy | RGS | Current |
| referentiegrootboekschema.nl/beschrijving-velddefinities-rgs | Field definitions, extension codes | RGS | Current (stand okt 2021) |
| referentiegrootboekschema.nl/handleiding-referentie-grootboekschema | Levels, mapping principles | RGS | Current (some legacy text) |
| referentiegrootboekschema.nl/instructie-mapping-rgs-en-sbr | Mapping methodology | RGS | Current |
| referentiegrootboekschema.nl/het-werken-met-extensies | Extensions | RGS | Current |
| referentiegrootboekschema.nl/aandachtspunten-bij-koppelen-grootboekrekeningschema | Coupling pitfalls | RGS | Current |
| referentiegrootboekschema.nl/toelichting-releasenotes-...-rgs-37 | Filters/tabs detail (38 filter changes) | RGS | Superseded by 3.8 but most detailed on filters |
| referentiegrootboekschema.nl/english | English scope, limits | RGS | Current |
| referentiegrootboekschema.nl/.../Toelichting RGS Taxonomie versie 15.pdf | Taxonomy method, 32 entrypoints | RGS | Current |
| referentiegrootboekschema.nl/Actueel/rgs-en-rgs-mkb-wat-het-verschil | RGS vs RGS MKB | RGS | Current (20 May 2025) |
| referentiegrootboekschema.nl/Actueel/rgs-zorg-... | RGS Zorg (new domain) | RGS | Current (Apr 2026) |
| sbr-nl.nl/.../taakgroepen/taakgroep-rgs | Governance (current model) | SBR/Logius | Current |
| sbr-nl.nl/over-sbr/sbr-organisatie/sbr-governance | SBR governance, 3/4 majority | SBR/Logius | Current |
| sbr-nl.nl/werken-met-sbr/taxonomie/releasekalender | NT20/NT21 dates | SBR/Logius | Current (upd 28-04-2026) |
| sbr-nl.nl/.../documentatie-nederlandse-taxonomie | NT13…NT21 list | SBR/Logius | Current |
| sbr-nl.nl/.../architectuur-en-ontwikkelingen | Taxonomy module ownership | SBR/Logius | Current |
| sbr-nl.nl/.../uitbreiding-elektronische-deponering-handelsregister | Groot SBR mandate (boekjaar 2025) | SBR/Logius | Current |
| sbr-nl.nl/.../Reporting_Manual_...Business Register_iXBRL.pdf | KvK iXBRL regime | SBR/Logius | Current (Jul 2024) |
| sbr-nl.nl/.../SBR-domein-Handelsregister_taxonomy-documentation.pdf | KvK IFRS taxonomy concatenation | SBR/Logius | Current (Sep 2024) |
| sbr-nl.nl/.../20251031_RTS_2025_NL_SBR-domein_Handelsregister.pdf | KvK RTS 2025 | SBR/Logius | Current (latest) |
| logius.nl/diensten/xbrl + .../wie-doet-wat | Logius role, KvK/BD/DUO/SBR-Wonen | Logius | Current |
| nltaxonomie.nl/ | NT/RGS publication root | Logius | Current (rgs/ 2025-08-26) |
| belastingdienst.nl/.../wat_is_sbr + standard_business_reporting | SBR reuse principle, IB/VPB/OB | Belastingdienst | Current |
| belastingdienst.nl/.../referentie-grootboekschema-iets-voor-u | RGS for entrepreneurs | Belastingdienst | Current |
| kvk.nl/deponeren/deponeren-met-sbr/ | SBR deposit by class | KvK | Current (Mar 2026) |
| kvk.nl/deponeren/in-welke-bedrijfsklasse-valt-je-bedrijf/ | Size thresholds | KvK | Current (Jan 2026) |
| wetten.overheid.nl/BWBR0003648 | Besluit modellen jaarrekening | Overheid | In force (verify consolidated text) |
| zoek.officielebekendmakingen.nl/stb-2024-52.html | New size thresholds (boekjaar 2024+) | Overheid | Current law |
| afm.nl/.../jaarlijkse-verslaggeving-in-esef | ESEF for listed issuers | AFM | Current |
| developer.moneybird.com/api/ledger-accounts | `rgs_code` field, 3.5, required-on-POST | MoneyBird | Current |
| moneybird.nl/blog/categorieen-toevoegen-met-het-rgs/ | Categories ↔ RGS 3.5, Brugstaat | MoneyBird | Current (25 Jul 2024) |

## Tier 2 — GBNED practitioner reference (boekhoudplaza.nl / softwarepakketten.nl)

| Source | Covers | Status |
|---|---|---|
| boekhoudplaza.nl/cmm/rgs/rgs_dashboard.php | Version history, code counts, audittrail | Current (to 3.8) |
| boekhoudplaza.nl/wiki_uitleg/18/RGS_Referentiecode_toegelicht.htm | Code construction | Current |
| boekhoudplaza.nl/wiki_uitleg/21/RGS_Grootboek_Referentienummer_toegelicht.htm | Number (7 vs 9 digit discrepancy) | Current |
| boekhoudplaza.nl/wiki_uitleg/17/RGS_Omslagcodes_toegelicht.htm | Omslag mechanics | Current |
| boekhoudplaza.nl/wiki_uitleg/23/RGS_Indicatie_debet_credit_toegelicht.htm | D/C | Current |
| boekhoudplaza.nl/wiki_uitleg/24/Filterfunctionaliteit_toegevoegd.htm | Filter mechanics | Current-ish (3.2 examples) |
| boekhoudplaza.nl/cmm/rgs/decimaal_rekeningschema_rgs.php | RGS MKB selector (ZZP/EZ/BV/SV + branche) | Current (live tool) |
| boekhoudplaza.nl/pag_epa/137/RGS_MKB.php | What RGS MKB is (+ NOAB) | Current |
| boekhoudplaza.nl/wiki_uitleg/40/... | RGS MKB decimal numbering rationale | Current |
| boekhoudplaza.nl/wiki_uitleg/122/Woningcorporaties_in_standaard_RGS_schema.htm | WoCo | Current |
| boekhoudplaza.nl/wiki_uitleg/28/Agrarische_sector..._RGS.htm | Agro | Current |
| boekhoudplaza.nl/wiki_uitleg/134/RGS_Branchegericht... | Branche reserved ranges | Current |
| boekhoudplaza.nl/.../204,206/...eliminatie/intercompany | Consolidation example | Current |
| softwarepakketten.nl/pag_reg/81/RGS_Ready.htm | RGS Ready 8-criteria, vendor list | Current registry |
| boekhoudplaza.nl/cmm/rgs/referentiegrootboekschema_rgs_balans_winst_en_verlies.php | RGS ↔ BW2 models | Current |

## Tier 3 — Vendor & tooling (corroborating)

| Source | Covers | Status |
|---|---|---|
| help.afas.nl/.../Fin_Config_Ledger_RGS.htm | AFAS RGS + extensie | Current (3.7) |
| kennispleinweb.snelstart.nl/.../grootboekrekeningschema-koppelen-aan-rgs | SnelStart mapping | Current (3.1) |
| wolterskluwer.com/.../rgs-in-twinfield | Twinfield reporting structure | Current (3.2+) |
| cdn.e-boekhouden.nl/handleiding/Handleiding_Referentie_Grootboekschema.pdf | e-Boekhouden | Current |
| help.asperion.nl/.../referentie-grootboekschema-(rgs).aspx | Asperion auto-match | Current |
| fiba.nl/rgs_snelzoeker | Fuzzy code lookup, versions to 3.8 | Current tool |
| github.com/Vegter/RGS-API | Open-source RGS REST API | **Stale (v3.3, 2021)** — code ref only |
| ey.com / deloitte.com — IFRS vs NL GAAP 2025 | Measurement differences | Current commentary |
| orangetax.com / bakertilly.nl — Dutch GAAP vs IFRS | Two-track pattern | Current commentary |

## Known issues found during validation

- **Superseded but still online:** RGS 3.7/3.6 release pages (use 3.8); the older
  Expertgroep/Beheergroep governance model on fundamentvoor.nl (2017) & rgs-wonen.nl
  (2019) (use the Taakgroep model); pre-2024 size thresholds.
- **Did not fully render:** Exact Online support article `glaccmaprgst` (login/JS wall) —
  covered via third-party write-ups instead. Some MoneyBird Intercom help articles
  returned garbled bytes — substituted MoneyBird's own blog + developer docs.
- **Internal inconsistency:** referentienummer length (7 vs 9 digits) differs between
  referentiegrootboekschema.nl and boekhoudplaza — both documented in
  `structure-and-codes.md`.
- **Stale tooling:** Vegter/RGS-API (v3.3). For a current machine-readable dataset prefer
  the official Excel or GBNED's RGS MKB CSV/JSON.
- **No broken links** otherwise; all Tier-1 sources fetched successfully.
