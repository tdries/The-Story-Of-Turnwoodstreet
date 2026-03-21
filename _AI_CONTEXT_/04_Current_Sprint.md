# 04 — Current Sprint & Known Issues

**Last updated:** 2026-03-20
**Sprint goal:** First playable build — walk the Turnhoutsebaan, talk to NPCs, run one battle.

---

## Status: DONE ✓

- [x] Project structure (Vite + TypeScript + Phaser)
- [x] `index.html` — Phaser entry point
- [x] `src/main.ts` — scene registry
- [x] `src/core/GameConfig.ts` — constants, palette, scene keys
- [x] `src/core/StateManager.ts` — global state + localStorage save
- [x] `src/core/InputHandler.ts` — keyboard abstraction
- [x] `src/scenes/BootScene.ts` — asset loading + progress bar
- [x] `src/scenes/MainMenuScene.ts` — title screen
- [x] `src/scenes/OverworldScene.ts` — street + NPC wander + dialogue trigger
- [x] `src/scenes/BattleScene.ts` — turn-based combat UI
- [x] `src/entities/Player.ts` — physics sprite + walk animations
- [x] `src/entities/NPC.ts` — wander AI + Y-sorting
- [x] `src/entities/Enemy.ts` — stat block
- [x] `src/systems/CombatSystem.ts` — pure combat logic
- [x] `src/systems/InventorySystem.ts` — item use + data lookup
- [x] `src/systems/DialogueSystem.ts` — dialogue tree runner
- [x] `src/systems/SkillSystem.ts` — skill unlock + use
- [x] `src/ui/HUD.ts` — HP bar, coins, level
- [x] `src/ui/DialogueBox.ts` — typewriter dialogue panel
- [x] `src/ui/InventoryMenu.ts` — full-screen inventory overlay
- [x] `src/data/items.json` — 11 items (food, keys, misc)
- [x] `src/data/enemies.json` — 6 enemies (street, bosses, ghosts)
- [x] `src/data/dialogue.json` — 8 dialogue trees
- [x] `src/data/skills.json` — 5 skills
- [x] Sprite sheets generated (13 sheets, SCALE=4)
- [x] `_AI_CONTEXT_/` docs (GDD, Architecture, Asset Manifest)
- [x] `Streetdata.md` — all real addresses for 3 postal codes

---

## TODO — Next Sprint

### Critical (game won't run without these)
- [ ] Run `npm install` in project root
- [ ] Fix TypeScript errors (run `tsc --noEmit`)
- [ ] Verify all `@data/` JSON imports resolve correctly

### High Priority
- [ ] Create `assets/maps/borgerhout_main.json` tilemap (Tiled)
- [ ] Wire tilemap into OverworldScene (replace placeholder graphics)
- [ ] Animate NPCs with proper walk frames from npc_extended_sheet
- [ ] Add Y-sort update loop for all entities in OverworldScene
- [ ] Add tram sprite that travels across the screen periodically
- [ ] Implement InventoryMenu in OverworldScene (currently stubbed)

### Medium Priority
- [ ] Add time-of-day system (morning/afternoon/evening/night)
- [ ] BGM: ambient street audio loop
- [ ] Shop interiors (enter La Cosa, Le Sud, Omar's bakery)
- [ ] Implement Tram 10 fast-travel between zones
- [ ] Quest tracking UI (top-right quest dot from ui_sheet)
- [ ] NPC interaction indicator (press Z icon over nearby NPC)

### Low Priority / Polish
- [ ] Screen shake on battle hit
- [ ] Coin pickup FX animation (fx_sheet, coin_sparkle frames)
- [ ] Dust FX when player starts walking
- [ ] Mobile touch controls overlay
- [ ] Save/load from Main Menu (currently "LADEN" does nothing)
- [ ] Settings screen (language, sound volume)

---

## Known Bugs

| # | Description | Priority |
|---|-------------|----------|
| 1 | `CombatSystem.ts` uses a local `Phaser.Math` namespace shim — may conflict if Phaser is imported in the same module | Medium |
| 2 | `OverworldScene` NPC name tags are not camera-fixed — they scroll with the world but may overlap at zoom | Low |
| 3 | `BattleScene` menu wraps but does not visually cap at 4 items if skill/item subtypes are added later | Low |
| 4 | `DialogueBox` typewriter timer is not stopped on scene destroy — potential memory leak | Medium |

---

## Architecture Decisions Log

**2026-03-20** — Chose Phaser.js 3.87 over Godot/Unity WebExport for faster iteration and zero install requirement for players.

**2026-03-20** — StateManager as a singleton (not a Phaser plugin) so it survives scene restarts without re-creation.

**2026-03-20** — Systems have no Phaser imports to enable unit-testing without a browser environment.

**2026-03-20** — Dialogue stored in JSON (not TypeScript) so translators and community contributors can edit it without touching code.
