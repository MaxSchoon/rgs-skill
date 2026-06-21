# RGS structure, codes & the data model

> The core of day-to-day RGS work: how an account code is built, which level you
> actually book to, and what every field means. When you need to *choose a code for a
> transaction*, this plus `scope-filters-entities.md` is what you want.

## The 5-level hierarchy (niveau / nivo)

RGS is a strict five-level tree. Only **niveau 4** is the normal posting (bookable)
account; levels 1–3 are grouping nodes, and level 5 exists only for some balance
accounts.

| Niveau | Name (NL) | Role | Example | Bookable? |
|---|---|---|---|---|
| 1 | Balans / Winst-en-verliesrekening | Report type | `B` (Balans) | No |
| 2 | Hoofdrubriek | Main category | `BMva` (Materiële vaste activa) | No |
| 3 | Rubriek | Sub-category | `BMvaBeg` (Bedrijfsgebouwen) | No |
| 4 | **Grootboekrekening** | **GL account — book here** | `BMvaBegVvp` (Verkrijgings-/vervaardigingsprijs) | **Yes** |
| 5 | Mutatie | Movement detail (balance accts only) | `BMvaBegVvpIna` (Investeringen nieuw) | Rarely |

Worked example with no level 5: `B` (Balans) → `BLim` (Liquide middelen) → `BLimKas`
(Kasmiddelen) → `BLimKasKas` (Kas — the bookable account).

**Book at niveau 4.** This is the single most important practical rule. Mapping at
level 2/3 throws away specificity (e.g. booking everything to "Salarisverwerking" at
level 3 loses the Netto lonen / Vakantiegeld / Gratificaties split at level 4). Level 5
mutaties exist only for balance-sheet accounts (to build the verloopstaat / movement
schedule for the jaarrekening) and are not used by MKB software — **MoneyBird and RGS
MKB both work at level 4 and ignore level 5.**

## The referentiecode — the durable key

The **referentiecode** (alphabetic, e.g. `WBedAutOak`) is the *true unique key* of
RGS. It encodes both identity and account type. Always map and store on the
referentiecode, never the number — see "Why the number is not the key" below.

Construction:
- Starts with a **source letter**: `B` = Balans, `W` = Winst-en-verliesrekening.
- Then **one 3-letter group per level** (notation `Xxx`: one uppercase + two lowercase),
  each mnemonically derived from that level's description.
  - Hoofdrubriek: `SXxx` → `BMva`
  - Rubriek: `SXxxXxx` → `BMvaBeg`
  - Rekening: `SXxxXxxXxx` → `BMvaBegVvp`
  - Mutatie: `SXxxXxxXxxXxx` → `BMvaBegVvpIna`
- **Max 13 characters** (`B`/`W` + up to four 3-letter groups).

Decode example — `WBedAutOak`: `W` (W&V) → `WBed` (Bedrijfskosten) → `WBedAut`
(Autokosten) → `WBedAutOak` (Overige autokosten). Useful 3-letter mnemonics you'll see
a lot: `Hui`=Huisvesting, `Vvp`=Verkrijgings-/vervaardigingsprijs, `Cae`=Cumulatieve
afschrijvingen, `Beg`=Beginbalans, `Des`=Desinvesteringen.

> You may **not change or extend** referentiecodes while citing RGS as the standard.
> Appended *extensions* are the only sanctioned addition (`.` for identification — e.g.
> an IBAN per bank account; `:` for codification) — and GBNED openly advises against
> using extensions because the spec is unclear. Structural additions go to the Taakgroep RGS.

> ⚠️ **Mnemonic false friends — never reverse-engineer a code from the 3-letter groups.**
> The mnemonics are derived from Dutch descriptions and are *not* English/abbreviation-
> intuitive. The classic trap: `WBedAut` is **Autokosten** (vehicle/car costs), **not**
> "automatisering" — so server/hosting/IT costs do **not** go to `WBedAut…`. (Automation/
> office-IT costs live elsewhere, e.g. the kantoorkosten family — look up the exact code,
> don't assume.) Likewise `WBedKan`=Kantoorkosten, `Aut`≠automation, `Hui`=Huisvesting.
> **Always confirm a niveau-4 code against the official master (or `scripts/rgs_lookup.py`)
> by its description and parent rubriek — never guess the tail from the letters.**

## The referentie(grootboek)nummer — example only

A parallel decimal number, provided **only as a suggestion** — you may keep your own
numbering. Two official descriptions disagree on length (boekhoudplaza flags this):

- referentiegrootboekschema.nl: **9 digits** — pos 1–2 hoofdrubriek, 3–4 rubriek, 5–6
  rekening, 7–8 mutatie, **pos 9 = extensiecode**.
- boekhoudplaza: **7 digits + `.NN`** for mutaties — pos 1–2 / 3–4 / 5–6 / pos 7 =
  extensiecode; mutaties as `…010.1`.

In the published data, mutaties appear as `202010.1` style (matching the 7+`.NN` form).
Extensiecode values: `0`=standaard, `1`=Fiscaal, `2`=Branche, `3`=Concern,
`4`=Onderneming, `5–9`=vrij.

**Why the number is not the key:** since RGS 3.0 the referentienummer is *no longer the
sort key* (a separate **Sortering** field handles ordering, because hoofdrubrieken
aren't consistently zero-padded). Numbers also shift when accounts are inserted between
versions. The **referentiecode is stable; the number is not.**

## Field / attribute dictionary

The official site formally names four velden (referentiecode, referentienummer,
grootboekomschrijving, omslagcode). The published Excel/master carries more:

| Field | Meaning | Example |
|---|---|---|
| **Referentiecode** | Unique alphabetic key; the durable mapping key | `BLimBanRba` |
| **Referentienummer** | Example decimal number (7/9-digit, `.NN` mutaties) | `202010` / `202010.1` |
| **Omschrijving** | Standard account name (some sources split kort/lang) | `Verkrijgings- of vervaardigingsprijs bedrijfsgebouwen` |
| **Niveau (Nv)** | Hierarchy level 1–5 | `4` |
| **D/C** | Normal posting side — **meaningful only at niveau 4–5** | `D` |
| **Omslagcode** | Referentiecode of the opposite account for sign-flips | (see below) |
| **Sortering** | Logical balans/W&V sort key (new since 3.0; also "Sortering BW2") | numeric |
| **Filters / branche** | Applicability columns: `ZZP`, `EZ`, `BV`, `SV`, branche flags | `J`, `J+`/`P`, blank |
| **Status** | Lifecycle — expired codes get **`VERVALLEN`** appended to omschrijving | `… VERVALLEN` |
| **Extensiecode** | Extension type at pos 9 (0=standaard … 4=onderneming) | `0` |

Filter values: `J` = basis account, `J+`/`P` = uitgebreid (less common, optional),
blank/`N` = not applicable.

## Main rubriek (niveau-2) reference table

First letter: **`B` = Balans**, **`W` = Winst-en-verliesrekening**.

**Balans (B):** `BIva` Immateriële VA · `BMva` Materiële VA · `BVas`
Vastgoedbeleggingen · `BFva` Financiële VA · `BEff` Effecten (kort) · `BVrd`
Voorraden · `BPro` Onderhanden projecten · `BVor` Vorderingen · `BLim` Liquide
middelen · `BEiv` Eigen vermogen / Kapitaal · `BEga` Egalisatierekening · `BVrz`
Voorzieningen · `BLas` Langlopende schulden · `BSch` Kortlopende schulden.

**W&V (W):** `WOmz` Netto-omzet · `WWiv` Wijziging voorraden · `WOvb` Overige
bedrijfsopbrengsten · `WKpr` Kostprijs van de omzet · `WPer` Personeelsbeloningen ·
`WAfs` Afschrijvingen (imm./mat. VA) · `WBed` Overige bedrijfskosten · `WFbe`
Financiële baten en lasten · `WBel` Belastingen · `WRed` Aandeel in resultaat
deelnemingen · `WNer` Nettoresultaat.

Common niveau-3 examples: under `BVor` → `BVorDeb` (Debiteuren), `BVorOva` (Overlopende
activa); under `BVrd` → `BVrdHan` (Handelsgoederen).

> ⚠️ **EZ/VOF vs BV equity.** A BV uses share capital + reserves under `BEiv`
> (`BEivAan…`), **not** the `BEivKap…` privé/ondernemersvermogen accounts (privé-stortingen/
> -onttrekkingen, per-vennoot capital) which are for eenmanszaak/VOF/maatschap. RGS models
> up to 5 vennoten by default. Picking the wrong equity family is a classic entity-type error.

## Omslag / debet-credit mechanics

**Omslag** = an account's balance switching sign and therefore needing to appear under a
*different* reporting rubriek. RGS handles this with the **omslagcode**, which holds the
referentiecode of the opposite (counter) account.

Canonical example — **Bank**: a debit (positive) saldo reports under *Liquide middelen*;
a credit (negative) saldo reports under *Kortlopende schulden*. The two RGS accounts
point at each other via omslagcode. Other pairs: rekening-courant, transitoria
(`BVorOva` Overlopende activa ↔ `BSchOpa` Overlopende passiva), te betalen vs terug te
vorderen belastingen, and ~14 rente baten/lasten pairs in the W&V.

Scale: ~180 niveau-4 accounts carry an omslagcode (~90 omslag situations), which is why
RGS contains deliberately **duplicated tussenrekeningen** (one under Vorderingen, one
under Schulden). The omslag is applied **during reporting** (jaarrekening, winstaangifte),
separately for begin- and eindbalans — **not** pre-applied in the XAF auditfile, and (per
GBNED) **not** implemented in the RGS XBRL Taxonomie. Practical takeaway: when you map an
account that can swing sign, couple **both** the account and its omslagcode counterpart, or
balances flip into the wrong rubriek.

## How your own ledger maps to RGS (the koppeling)

You keep your **own grootboekrekeningnummers and descriptions**; RGS is overlaid by
mapping each own account to **one referentiecode** (the koppeltabel). Relationship types:

- **1:1** — ideal, one own account ↔ one RGS code.
- **m:1** — you split finer than RGS → add an extensie, or accept the coarser RGS code.
- **1:n** — your one account spans several RGS codes → split the account going forward.

Because RGS links onward to SBR via the RGS Taxonomie, this single mapping lets the same
ledger feed KvK, Belastingdienst, CBS and bank reports. See `reporting-compliance.md`.

## Where to get the master file

- **Official:** referentiegrootboekschema.nl → Kennisbank → "Download RGS". Authoritative
  master is an **Excel workbook** (current **RGS 3.8**, 10 Dec 2025); release notes on the
  "Recap" tab; tabs include MKB-only and woningcorporatie sheets.
- **XBRL form:** the **RGS Taxonomie** on sbr-nl.nl / nltaxonomie.nl (machine-readable
  mapping to SBR entrypoints).
- **Browsable / filterable exports:** boekhoudplaza.nl/GBNED (CSV/PDF, filter by
  ZZP/EZ/BV/SV and branche) and the separate **RGS MKB decimaal** scheme.

Typical master columns mirror the field dictionary above: **Referentiecode | Omschrijving
| Referentienummer | Nivo | Omslagcode | D/C | ZZP | EZ | BV | SV | Branche | Sortering**,
plus extensiecode and inline `VERVALLEN` status.
