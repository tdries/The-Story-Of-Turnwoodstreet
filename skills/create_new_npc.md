# Skill: Create New NPC

## Usage
"Create an NPC named [name] who is [description]."

## Steps

1. **Read the GDD** (`_AI_CONTEXT_/01_Game_Design_Document.md`) for world tone.
2. **Add to `src/data/dialogue.json`:**
   ```json
   "[name]_intro": [
     { "speaker": "[Name]", "text": "..." },
     { "speaker": "[Name]", "text": "...", "flag": "[name]_met", "flagVal": true }
   ]
   ```
3. **Add to `OverworldScene.ts` `npcSeed` array:**
   ```typescript
   { id: '[name]', x: [X], y: [Y], dialogue: '[name]_intro', frame: [N] }
   ```
   - X: pick a house number range from Streetdata.md, convert to pixel offset (~3.2px per house number)
   - Y: 185–194 (sidewalk band)
   - frame: 0=hijab woman, 4=djellaba man, 8=child, 12=delivery worker

4. **Check dialogue rules:**
   - Speak in the NPC's natural language mix (see Master Directives §3)
   - Include at least one real Turnhoutsebaan reference (shop name, address, event)
   - Last line sets a quest flag if the NPC is quest-relevant

5. **If NPC gives an item:** Add a `choice` block with `item` field and add the item to `items.json`.

## NPC Frame Reference (npc_extended_sheet)
- Frame 0–3: Hijab woman, walk right
- Frame 4–7: Djellaba man, walk right
- Frame 8–11: Child, walk right
- Frame 12–15: Delivery worker, walk right
- Frame 16+: See npc_extra_sheet
