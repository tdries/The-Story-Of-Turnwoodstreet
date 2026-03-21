# 02 — Architecture & State Machine

## Scene Graph

```
BootScene
  └─ preloads all assets → starts MainMenuScene

MainMenuScene
  └─ Z/Space/Enter → starts OverworldScene

OverworldScene  (runs persistently)
  ├─ pauses → launches BattleScene (enemy encounter)
  ├─ DialogueSystem (modal, blocks movement)
  └─ InventoryMenu (modal overlay)

BattleScene
  └─ on end → stops self, resumes OverworldScene
```

## Module Dependency Graph

```
main.ts
  ├─ GameConfig       (pure config, no deps)
  ├─ StateManager     (pure TS, localStorage)
  └─ Scenes
       ├─ BootScene        (Phaser)
       ├─ MainMenuScene    (Phaser, GameConfig, StateManager)
       ├─ OverworldScene   (Phaser, InputHandler, Player, NPC, HUD,
       │                    DialogueBox, DialogueSystem, StateManager)
       └─ BattleScene      (Phaser, InputHandler, CombatSystem,
                            StateManager, enemies.json)

Entities:
  Player     → InputHandler, Phaser.Physics.Arcade.Sprite
  NPC        → Phaser.Physics.Arcade.Sprite
  Enemy      → pure stats (no Phaser)

Systems (NO Phaser imports):
  CombatSystem      → Combatant interface
  InventorySystem   → StateManager, items.json
  DialogueSystem    → StateManager, DialogueBox, dialogue.json
  SkillSystem       → StateManager, skills.json

UI (camera-fixed, Phaser allowed):
  HUD           → Phaser, StateManager
  DialogueBox   → Phaser
  InventoryMenu → Phaser, InputHandler, InventorySystem
```

## State Machine — Quest Flags

All quest state lives in `StateManager.questFlags`. Never in scene variables.

### Key flags

| Flag | Type | Set by | Meaning |
|------|------|--------|---------|
| `met_fatima` | boolean | fatima_intro dialogue end | Unlocks Solidarity Shout skill |
| `knows_samen_tafel` | boolean | omar_bakker dialogue | Unlocks Samen Aan Tafel skill |
| `stunt_quest_active` | boolean | Mevrouw Baert dialogue | Fabric quest started |
| `stunt_quest_done` | boolean | delivering fabric to Fatima | Fabric quest complete |
| `reza_quest_done` | boolean | giving oud_string to Reza | Unlocks Music of the Street skill |
| `visited_de_roma` | boolean | entering De Roma building | Lore unlocked |
| `met_mayor` | boolean | talking to El Osri | Act 4 begins |
| `has_permit_doc` | boolean | defeating Bureau-Bulldozer | Unlocks Bureaucratic Shield |
| `kracht_van_gemeenschap` | boolean | defeating Geest van '88 | Story milestone |
| `samen_tafel_faction_N` | number (0–7) | completing each faction quest | Final table count |

### Win condition
`samen_tafel_faction_N >= 7` → trigger ending cutscene.

## Save / Load

`StateManager.save()` → writes full `GameState` to `localStorage['tbaan_save']`.
Called automatically after:
- Every battle end
- Every completed quest flag set
- On scene exit

## Physics Setup

- `Phaser.Physics.Arcade` with no gravity
- Player body: 10×10px at feet
- NPC bodies: 10×10px, immovable
- World bounds: locked to sidewalk Y-band (50%–80% of GAME_HEIGHT)
- Camera follows player with 8% lerp + 25% deadzone

## Y-Sorting (Painter's Algorithm)

All entities set `setDepth(this.sprite.y)` each frame.
Static tilemap layers:
- `depth: 0` — sky, ground
- `depth: 1` — building walls
- `depth: 2` — building details (windows, doors)
- `depth: 3` — props at ground level (bins, benches)
- `depth: 10` — player (base, adjusted by Y each frame)
- `depth: 100` — HUD elements (fixed to camera, always on top)
