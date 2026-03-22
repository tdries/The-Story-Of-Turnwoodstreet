# 05 — Gated Progression System
## Turnhoutsebaan RPG — Full Narrative & Systems Design

---

## OVERVIEW

The Turnhoutsebaan is not a linear street you simply walk down.
It is a living community that only opens to you as you earn its trust,
understand its music, and navigate its bureaucracy.

Four distinct **Capabilities** act as keys. Five **Zones** act as locks.
Progress is never arbitrary — every gate has a narrative justification
rooted in the real culture and history of Borgerhout.

---

## 1. THE FOUR CORE CAPABILITIES

### CAPABILITY 1 — VERTROUWEN VAN DE BUURT
**"The Community Trusts You"**

- **Verb:** *Vertrouwen wekken* — earning trust through help, presence, listening.
- **Acquired by:** Completing Fatima's Fabric Quest (delivering fabric_bolt from
  Stunt Solderie to Fatima). Trust is not given — it is earned through action.
- **Sets flag:** `has_community_trust = true`
- **Gate it opens:** Zone 1 → Zone 2 (Reuzenpoort, nos. 110)
- **Narrative logic:** Beyond the Reuzenpoort, shopkeepers and residents have seen
  too many outsiders arrive with plans and promises. Only someone vouched for by
  Fatima — a 22-year resident — is welcomed past the old stone gate.
- **In combat:** Unlocks *Solidariteitsroep* — the street backs you up.

---

### CAPABILITY 2 — MUZIEK VAN DE STRAAT
**"You Understand the Street's Language"**

- **Verb:** *Spelen* — play Reza's oud to move people emotionally and open guarded hearts.
- **Acquired by:** Completing Reza's Oud String Quest (finding `oud_string` at Oxfam
  Wereldwinkel and returning it to Reza near De Roma).
- **Sets flag:** `reza_quest_done = true`
- **Gate it opens:** Zone 2 → Zone 3 (De Roma entrance, nos. ~200)
- **Narrative logic:** De Roma's spirit only permits entry to those who understand
  that the street communicates through music. The bouncer — an Art Deco geest —
  asks: "Heb je ooit geluisterd naar de straat?" Those who helped Reza have.
- **In combat:** Unlocks *Muziek van de Straat* — demoralises all enemies.

---

### CAPABILITY 3 — DE VERGUNNING
**"You Have Official Standing"**

- **Verb:** *Voorleggen* — present your papers at bureaucratic checkpoints.
- **Acquired by:** Defeating the Bureau-Bulldozer enemy in Act 2 (the property
  speculator who threatens evictions). The permit drops as a key item.
- **Sets flag:** `has_permit_doc = true` + adds `permit_doc` to inventory
- **Gate it opens:** Zone 3 → Zone 4 (Deurne tram junction checkpoint, nos. ~300)
- **Narrative logic:** The boundary between Borgerhout and Deurne is patrolled by
  bureaucratic inertia. Without official documentation of your community standing,
  the checkpoint guard (an NPC echoing the old anti-Borgerhout attitude) refuses
  passage. The permit — seized from the speculator himself — is ironic proof of belonging.
- **In combat:** Unlocks *Vergunningsschild* — use legal paperwork as armour.

---

### CAPABILITY 4 — SAMEN AAN TAFEL
**"You Can Unite the Street"**

- **Verb:** *Uitnodigen* — invite all seven factions to the 2-kilometre table.
- **Acquired by:** Collecting 7 faction commitments (samen_tafel_faction_N ≥ 7).
  Each faction requires a separate trust-building sub-quest.
- **Sets flag:** `samen_tafel_faction_N = 7` → triggers ending
- **Gate it opens:** Zone 4 → Zone 5 (The Groot Feest / final celebration zone)
- **Narrative logic:** The 2km Samen Aan Tafel event (Easter + Iftar, April 2024,
  7000 people) was only possible because of years of trust built across cultural lines.
  You cannot organise it by force — every faction must genuinely want to come.
- **In combat:** Unlocks *Samen Aan Tafel* — pacify enemies by sharing food.

---

## 2. THE FIVE ZONES

### ZONE 1 — BORGERHOUT WEST
**"De Aankomst" (nos. 1–110)**

| Property | Value |
|----------|-------|
| Entry gate | None — open to all |
| Acquired capability | Vertrouwen van de Buurt |
| Narrative theme | Arrival. Learning the rhythms. Meeting your neighbours. |
| Key locations | La Cosa (no.11), Le Sud (café + save point), Reuzenpoort (locked gate at no.110), Stunt Solderie (no.74) |
| Tone | Welcoming but unfamiliar. The player doesn't know anyone yet. |

**Available quests in Zone 1:**
- `q_starter_delivery` — Help Yusuf the courier with 3 parcels
- `q_fabric_quest` — Fatima's fabric (earns Vertrouwen)
- `q_flour_shortage` — Omar needs flour (earns harira + goodwill)

---

### ZONE 2 — BORGERHOUT CENTRAL
**"De Wortels" (nos. 110–200)**

| Property | Value |
|----------|-------|
| Entry gate | `has_community_trust` — vouched for by Fatima |
| Acquired capability | Muziek van de Straat |
| Narrative theme | Taking root. Finding the street's hidden culture. |
| Key locations | Old Town Hall (no.110), Reza's corner, Aziz (#239) |
| Tone | Deeper. The street reveals its history. The speculator's first threats emerge. |

**Available quests in Zone 2:**
- `q_oud_string` — Reza's broken string → get from Aziz (#239) (earns Muziek van de Straat)
- `q_signatures` — Collect 5 signatures against eviction (Reza only signs after oud quest done)

---

### ZONE 3 — BORGERHOUT EAST / DE ROMA
**"De Ziel" (nos. 200–300)**

| Property | Value |
|----------|-------|
| Entry gate | `reza_quest_done` — you understand the music |
| Acquired capability | De Vergunning |
| Narrative theme | The heart of the street. Art, history, confrontation. |
| Key locations | De Roma (no.286), Snack Roma (nos.285–295), Mosque (no.315), Bureau-Bulldozer encounter |
| Tone | Dramatic. The speculator is defeated here. Geest van '88 appears. |

**Available quests in Zone 3:**
- `q_bulldozer_fight` — Confront and defeat Bureau-Bulldozer (earns permit_doc)
- `q_geest_88` — Defeat Geest van '88 using Samen Aan Tafel (earns kracht_van_gemeenschap)
- `q_de_roma_concert` — Unlock the De Roma concert cutscene (requires visited_de_roma)
- `q_mayor_meeting` — Meet El Osri (sets met_mayor, begins Act 4)

---

### ZONE 4 — DEURNE
**"De Verbinding" (nos. 300–471)**

| Property | Value |
|----------|-------|
| Entry gate | `has_permit_doc` — official standing required |
| Acquired capability | Samen Aan Tafel (full unlock — all 7 factions) |
| Narrative theme | Connection. The wider city. Gathering the last threads. |
| Key locations | Cogelsplein tram junction, Apotheek Praats, Costermans Wielersport, Te Boelaerpark (peaceful optional zone) |
| Tone | Quieter. More suburban. The player feels the contrast with Borgerhout's density. |

**Available quests in Zone 4 (faction quests for the Table):**
- `q_faction_moroccan` — Moroccan Association (requires met_fatima)
- `q_faction_turkish` — Turkish Social Club (requires tine dialogue)
- `q_faction_flemish` — Bar Leon Flemish café (requires met_baert_twice)
- `q_faction_art` — Borgerhub art space (requires visited_de_roma)
- `q_faction_school` — Local school (requires kid_marbles dialogue)
- `q_faction_mosque` — De-Koepel Mosque (requires met_imam)
- `q_faction_frituur` — Frituur de Tram (requires delivery_done)

---

### ZONE 5 — THE 2KM TABLE
**"De Grote Tafel" (nos. 471+ / Feestzone)**

| Property | Value |
|----------|-------|
| Entry gate | `samen_tafel_faction_N >= 7` |
| Acquired capability | N/A — this is the ending |
| Narrative theme | Celebration. Unity. The real historical event made playable. |
| Key locations | The entire Turnhoutsebaan transforms: 2km of tables, 7000 people, every faction represented |
| Tone | Joyful, multilingual, triumphant. |

**Win condition:** All 7 factions seated → ending cutscene triggers.

---

## 3. THE DEPENDENCY GRAPH (CRITICAL PATH)

```
START → Zone 1 (Borgerhout West)
  │
  ├─ Meet Fatima (met_fatima = true)
  ├─ Complete q_starter_delivery (tram_ticket earned)
  ├─ Complete q_fabric_quest → fabric_bolt delivered to Fatima
  │     └─ EARN: has_community_trust = true
  │
  ▼
[GATE: Reuzenpoort, no.110 — needs has_community_trust]
  │
  ▼
Zone 2 (Borgerhout Central)
  │
  ├─ Find oud_string at Oxfam (no.94)
  ├─ Give to Reza
  │     └─ EARN: reza_quest_done = true, music_of_the_street skill
  │
  ├─ Collect 5 signatures (sets speculator_threatened = true)
  ├─ Get bakfiets repaired at Beno (bakfiets_charge skill)
  │
  ▼
[GATE: De Roma entrance, no.200 — needs reza_quest_done]
  │
  ▼
Zone 3 (Borgerhout East / De Roma)
  │
  ├─ Visit De Roma (visited_de_roma = true, lore unlocked)
  ├─ Defeat Bureau-Bulldozer
  │     └─ EARN: has_permit_doc = true, permit_doc item, bureaucratic_shield skill
  │
  ├─ Defeat Geest van '88 using Samen Aan Tafel skill
  │     └─ EARN: kracht_van_gemeenschap = true
  │
  ├─ Meet El Osri (met_mayor = true) → Act 4 begins
  │
  ▼
[GATE: Deurne checkpoint, no.300 — needs has_permit_doc]
  │
  ▼
Zone 4 (Deurne)
  │
  ├─ q_faction_moroccan  (samen_tafel_faction_N++)
  ├─ q_faction_turkish   (samen_tafel_faction_N++)
  ├─ q_faction_flemish   (samen_tafel_faction_N++)
  ├─ q_faction_art       (samen_tafel_faction_N++)
  ├─ q_faction_school    (samen_tafel_faction_N++)
  ├─ q_faction_mosque    (samen_tafel_faction_N++)
  ├─ q_faction_frituur   (samen_tafel_faction_N++)
  │     └─ EARN: samen_tafel_faction_N = 7
  │
  ▼
[GATE: De Grote Tafel — needs samen_tafel_faction_N >= 7]
  │
  ▼
Zone 5 — ENDING: 2km Table cutscene, credits
```

**Backtracking moments (deliberate design):**
- Aziz (#239) is at x=1060 (Zone 1 with current boundaries) — oud_string is obtained
  there after the oud quest is accepted from Reza (x=880, also Zone 1).
- After earning has_community_trust, Fatima also reveals Omar's flour shortage
  quest (q_flour_shortage) back in Zone 1 — pulling player back.
- The `q_faction_flemish` quest requires visiting Bar Leon on Krugerplein (side street
  off Zone 2) — a return trip even from Zone 3.

---

## 4. NARRATIVE WRAPPER

### THE STORY IN ONE PARAGRAPH

You arrive on the Turnhoutsebaan as a newcomer — young, on a bicycle, carrying nothing
but curiosity. The street is alive: bakers, musicians, shopkeepers, elders. But the
street has layers. Behind the Reuzenpoort's stone arch lies a world that doesn't open
to strangers. A property speculator has bought three buildings and plans to hollow out
the community. A ghost from 1988 still haunts the side streets, muttering old slurs.
And somewhere along 2 kilometres of asphalt, 7000 chairs are waiting to be filled.
To place every one of them, you must earn something that cannot be bought: *vertrouwen*.

### WHY THE CAPABILITIES MAKE SENSE IN THE LORE

| Capability | Why it works narratively |
|-----------|-------------------------|
| Vertrouwen | Borgerhout's multicultural community is built on 50 years of trust across difference. An outsider earns it one act at a time. The Reuzenpoort — a real 1713 gate — is the perfect physical metaphor. |
| Muziek van de Straat | De Roma (real, Art Deco, 1927) has always been the street's cultural heart. Music is how the street communicates across language barriers. Reza is a real archetype — the Afghan-Belgian musician who belongs everywhere and nowhere until you help him. |
| De Vergunning | The speculator used bureaucracy as a weapon. Taking his permit reverses that power. The Deurne checkpoint echoes the real administrative boundary between postcodes 2140 and 2100 — a line that matters to residents. |
| Samen Aan Tafel | The 2024 Samen Aan Tafel event (real: 7000 people, 2km, Easter + Iftar) is the street's greatest achievement. It cannot be organised by one person alone — it requires every voice. The game makes you earn every seat. |

### THE EMOTIONAL ARC

```
Arrival (curious, uncertain)
  → Trust (you belong here)
    → Culture (you understand here)
      → Power (you can defend here)
        → Community (you can unite here)
          → CELEBRATION
```

---

## 5. GATE HINT MESSAGES (SHOWN TO PLAYER AT BLOCKED ZONES)

| Gate | x=  | Dutch hint message |
|------|-----|--------------------|
| Zone 1→2 | 1152 | *"De poort blijft gesloten voor vreemden. Spreek eerst met Fatima aan het begin van de straat."* |
| Zone 2→3 | 2304 | *"De deur van De Roma opent alleen voor wie de taal van de straat begrijpt. Zoek Reza's oud-snaar."* |
| Zone 3→4 | 3456 | *"De grenswachter vraagt naar uw papieren. Versla de Bulldozer-bureaucraat en draag zijn vergunning."* |
| Zone 4→5 | 4608 | *"Je hebt nog [N] facties nodig. De tafel is pas compleet als iedereen zit."* |

---

## 6. IMPLEMENTATION NOTES

### Zone Boundaries (world pixel x-coordinates)
WORLD_W = GAME_WIDTH × 12 = **5760 px** (street extended to cover Borgerhout → Deurne → Wijnegem).
```
Zone 1:  x =    0 – 1152  (nos.   1–110)   no gate
Zone 2:  x = 1152 – 2304  (nos. 110–200)   gate: has_community_trust
Zone 3:  x = 2304 – 3456  (nos. 200–300)   gate: reza_quest_done
Zone 4:  x = 3456 – 4608  (nos. 300–400)   gate: has_permit_doc
Zone 5:  x = 4608 – 5760  (nos. 400–471+)  gate: 7 factions
```
> ⚠️ Updated 2026-03-22. All NPC x-positions (210–1664) and story triggers (1728–1920) fall in Zones 1–2.
> Zones 3–5 (x > 2304) are the extended Deurne/Wijnegem area — building tiles only, no story NPCs yet.

### Key File Locations
- Quest definitions:     `src/data/quests.json`
- Quest logic:           `src/systems/QuestSystem.ts`
- Gate logic:            `src/systems/GateSystem.ts`
- Zone triggers:         `src/scenes/OverworldScene.ts → setupZoneTriggers()`
- State:                 `src/core/StateManager.ts → questFlags`
- Dialogue branches:     `src/data/dialogue.json` (choice arrays)
- Skill unlock checks:   `src/systems/SkillSystem.ts → isUnlocked(id)`

### Rules
- A gate **never** blocks backward travel (player can always return west).
- Gate hint is shown in the DialogueBox using speaker `"Turnhoutsebaan"`.
- Faction count `samen_tafel_faction_N` is a **number** flag, not boolean.
- `QuestSystem.checkCompletion()` is called after every dialogue end and battle end.
- `StateManager.save()` is called every time a quest completes.
