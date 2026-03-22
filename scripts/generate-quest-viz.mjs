#!/usr/bin/env node
/**
 * generate-quest-viz.mjs
 * Regenerates _AI_CONTEXT_/quest_state_machine.md from the known GameMachine structure.
 * Run with: npm run viz
 *
 * This script is intentionally self-contained (no TS compilation needed).
 * Update this file whenever GameMachine.ts states or events change.
 */

import { writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, '..', '_AI_CONTEXT_', 'quest_state_machine.md');

mkdirSync(dirname(OUT), { recursive: true });

const content = `# Quest State Machine — Turnhoutsebaan RPG

Auto-generated from \`src/systems/GameMachine.ts\`.
Regenerate with: \`npm run viz\`

> **How to read this diagram**
> - Each arc runs in **parallel** — all arcs progress independently.
> - Transitions are triggered by XState events (e.g. \`MET_YUSUF\`).
> - \`[*]\` = entry/exit point. \`✓\` = final state.
> - Grey boxes inside \`accepted\`/\`collecting\` are **nested parallel** sub-states.

---

## Full Machine — Parallel Arcs Overview

\`\`\`mermaid
flowchart LR
    delivery["🚴 Delivery\\nAct 1"]
    fabric["🧵 Fabric\\nAct 1→2"]
    flour["🌾 Flour\\nAct 2"]
    oud["🎸 Oud\\nAct 2"]
    signatures["✍️ Signatures\\nAct 2"]
    bulldozer["🏗️ Bulldozer\\nAct 3"]
    geest["👻 Geest\\nAct 3"]
    mayor["🏛️ Mayor\\nAct 3→4"]
    factions["🤝 Factions\\nAct 4"]

    delivery -.->|community trust| fabric
    fabric -.->|trust unlocks| signatures
    flour -.->|samen tafel| geest
    signatures -.->|speculator| bulldozer
    bulldozer -.->|permit| mayor
    mayor -.->|briefed| factions
\`\`\`

---

## Act 1 — Delivery Arc

\`\`\`mermaid
flowchart TD
    D_START([idle])
    D1([met])
    D_ACC([accepted])
    D_ALL([all_delivered])
    D_DONE(["rewarded ✓"])

    D_START -->|MET_YUSUF| D1
    D1 -->|DELIVERY_ACCEPTED| D_ACC

    D_ACC --> P137
    D_ACC --> P170
    D_ACC --> P284

    subgraph parallel["parallel packages"]
        P137["📦 #137\\npending"] -->|DELIVERED_137| P137D["#137 ✓"]
        P170["📦 #170\\npending"] -->|DELIVERED_170| P170D["#170 ✓"]
        P284["📦 #284\\npending"] -->|DELIVERED_284| P284D["#284 ✓"]
    end

    P137D & P170D & P284D -->|all done| D_ALL
    D_ALL -->|DELIVERY_REWARDED| D_DONE
\`\`\`

**Flags set:** \`met_yusuf\` · \`delivery_accepted\` · \`delivered_137/170/284\` · \`delivery_done\`

---

## Act 1→2 — Fabric Arc (Fatima's Wedding)

\`\`\`mermaid
flowchart LR
    F0([idle]) -->|MET_FATIMA| F1([met])
    F1 -->|FABRIC_ACCEPTED| F2([accepted])
    F2 -->|FABRIC_PICKED_UP| F3([picked_up])
    F3 -->|FABRIC_DELIVERED| F4(["completed ✓"])
\`\`\`

**Flags set:** \`met_fatima\` · \`fabric_quest_accepted\` · \`stunt_quest_active\` · \`stunt_quest_done\` · \`has_community_trust\`

---

## Act 2 — Flour Arc (Omar's Bakery)

\`\`\`mermaid
flowchart LR
    FL0([idle]) -->|FLOUR_ACCEPTED| FL1([accepted])
    FL1 -->|FLOUR_PICKED_UP| FL2([picked_up])
    FL2 -->|FLOUR_DELIVERED| FL3(["completed ✓"])
\`\`\`

**Flags set:** \`flour_quest_accepted\` · \`has_flour\` · \`omar_flour_done\` · \`knows_samen_tafel\`

---

## Act 2 — Oud Arc (Reza's String)

\`\`\`mermaid
flowchart LR
    O0([idle]) -->|OUD_ACCEPTED| O1([accepted])
    O1 -->|OUD_FOUND| O2([found])
    O2 -->|OUD_DELIVERED| O3(["completed ✓"])
\`\`\`

**Flags set:** \`oud_quest_accepted\` · \`has_oud_string_item\` · \`reza_quest_done\`

---

## Act 2 — Signatures Arc (Petition)

\`\`\`mermaid
flowchart TD
    S0([idle])
    S_COL([collecting])
    S_COMP([completed])
    S_DONE(["rewarded ✓"])

    S0 -->|any SIG_* event| S_COL

    S_COL --> SF
    S_COL --> SO
    S_COL --> SR
    S_COL --> SB
    S_COL --> SA

    subgraph sigs["parallel signatures"]
        SF["Fatima\\npending"] -->|SIG_FATIMA| SFD["Fatima ✓"]
        SO["Omar\\npending"]   -->|SIG_OMAR|   SOD["Omar ✓"]
        SR["Reza\\npending"]   -->|SIG_REZA|   SRD["Reza ✓"]
        SB["Baert\\npending"]  -->|SIG_BAERT|  SBD["Baert ✓"]
        SA["Aziz\\npending"]   -->|SIG_AZIZ|   SAD["Aziz ✓"]
    end

    SFD & SOD & SRD & SBD & SAD -->|all signed| S_COMP
    S_COMP -->|SIGNATURES_DONE\\nspeculator threatened| S_DONE
\`\`\`

**Flags set:** \`sig_fatima\` · \`sig_omar\` · \`sig_reza\` · \`sig_baert\` · \`sig_aziz\` · \`speculator_threatened\`

---

## Act 3 — Bulldozer Arc (De Roma)

\`\`\`mermaid
flowchart LR
    B0([idle]) -->|VISITED_DE_ROMA| B1([de_roma_visited])
    B1 -->|BULLDOZER_DEFEATED| B2(["completed ✓"])
\`\`\`

**Flags set:** \`visited_de_roma\` · \`has_permit_doc\`

---

## Act 3 — Geest Arc (Ghost of '88)

\`\`\`mermaid
flowchart LR
    G0([idle]) -->|GEEST_ENCOUNTERED| G1([encountered])
    G1 -->|GEEST_DEFEATED| G2(["completed ✓"])
\`\`\`

**Flags set:** \`geest_encountered\` · \`kracht_van_gemeenschap\`

---

## Act 3→4 — Mayor Arc

\`\`\`mermaid
flowchart LR
    M0([idle]) -->|MET_MAYOR| M1([met])
    M1 -->|MAYOR_BRIEFED| M2(["briefed ✓"])
\`\`\`

**Flags set:** \`met_mayor\` · \`act4_briefed\` · \`act4_started\`

---

## Act 4 — Factions (7 parallel)

\`\`\`mermaid
flowchart TD
    subgraph factions["factions — all run in parallel"]
        direction LR
        MOR_I([moroccan\\nidle]) -->|FACTION_MOROCCAN| MOR_D(["moroccan ✓"])
        TUR_I([turkish\\nidle])  -->|FACTION_TURKISH|  TUR_D(["turkish ✓"])
        FLE_I([flemish\\nidle])  -->|FACTION_FLEMISH|  FLE_D(["flemish ✓"])
        ART_I([art\\nidle])      -->|FACTION_ART|      ART_D(["art ✓"])
        SCH_I([school\\nidle])   -->|FACTION_SCHOOL|   SCH_D(["school ✓"])
        MOS_I([mosque\\nidle])   -->|FACTION_MOSQUE|   MOS_D(["mosque ✓"])
        FRI_I([frituur\\nidle])  -->|FACTION_FRITUUR|  FRI_D(["frituur ✓"])
    end

    MOR_D & TUR_D & FLE_D & ART_D & SCH_D & MOS_D & FRI_D -->|all 7 done| FINALE["🎉 Grote 2km Tafel"]
\`\`\`

**Flags set:** \`fatima_convinced\` · \`tine_faction_convinced\` · \`baert_faction_convinced\` · \`art_faction_convinced\` · \`school_faction_convinced\` · \`mosque_faction_convinced\` · \`frituur_faction_convinced\`

---

## Event → Flag Bridge

| XState Event | Flag(s) Set |
|---|---|
| \`MET_YUSUF\` | \`met_yusuf\` |
| \`DELIVERY_ACCEPTED\` | \`delivery_accepted\`, \`delivery_packages_received\` |
| \`DELIVERED_137/170/284\` | \`delivered_137/170/284\` |
| \`DELIVERY_REWARDED\` | \`delivery_done\` |
| \`MET_FATIMA\` | \`met_fatima\` |
| \`FABRIC_ACCEPTED\` | \`fabric_quest_accepted\`, \`knows_stunt_location\` |
| \`FABRIC_PICKED_UP\` | \`stunt_quest_active\` |
| \`FABRIC_DELIVERED\` | \`stunt_quest_done\`, \`has_community_trust\` |
| \`FLOUR_ACCEPTED\` | \`omar_flour_asked\`, \`flour_quest_accepted\` |
| \`FLOUR_PICKED_UP\` | \`has_flour\` |
| \`FLOUR_DELIVERED\` | \`omar_flour_done\`, \`knows_samen_tafel\` |
| \`OUD_ACCEPTED\` | \`oud_quest_accepted\` |
| \`OUD_FOUND\` | \`has_oud_string_item\` |
| \`OUD_DELIVERED\` | \`reza_quest_done\` |
| \`SIG_FATIMA/OMAR/REZA/BAERT/AZIZ\` | \`sig_fatima/omar/reza/baert/aziz\` |
| \`SIGNATURES_DONE\` | \`speculator_threatened\` |
| \`VISITED_DE_ROMA\` | \`visited_de_roma\` |
| \`BULLDOZER_DEFEATED\` | \`has_permit_doc\` |
| \`GEEST_ENCOUNTERED\` | \`geest_encountered\` |
| \`GEEST_DEFEATED\` | \`kracht_van_gemeenschap\` |
| \`MET_MAYOR\` | \`met_mayor\`, \`act4_briefed\` |
| \`MAYOR_BRIEFED\` | \`act4_started\` |
| \`FACTION_MOROCCAN\` | \`fatima_convinced\`, \`samen_tafel_faction_1\` |
| \`FACTION_TURKISH\` | \`tine_faction_convinced\`, \`samen_tafel_faction_2\` |
| \`FACTION_FLEMISH\` | \`baert_faction_convinced\`, \`samen_tafel_faction_3\` |
| \`FACTION_ART\` | \`art_faction_convinced\`, \`samen_tafel_faction_4\` |
| \`FACTION_SCHOOL\` | \`school_faction_convinced\`, \`samen_tafel_faction_5\` |
| \`FACTION_MOSQUE\` | \`mosque_faction_convinced\`, \`met_imam\`, \`samen_tafel_faction_6\` |
| \`FACTION_FRITUUR\` | \`frituur_faction_convinced\`, \`samen_tafel_faction_7\` |

---

## Dialogue Priority Rules

When adding new dialogue nodes, follow these guards to avoid blocking active quests:

| Situation | Required condition |
|---|---|
| Post-quest node after Fatima wedding | \`"sig_fatima": true\` if priority > 95 |
| Post-quest node after Reza concert | \`"sig_reza": true\` if priority > 95 |
| Post-quest node after Omar flour | \`"sig_omar": true\` if priority > 80 |
| Any "memory" dialogue after delivery | \`"delivery_done": true\` |
| Faction dialogue | \`"has_community_trust": true\` |
`;

writeFileSync(OUT, content, 'utf8');
console.log(`✅ Quest state machine diagram written to:\n   ${OUT}`);
