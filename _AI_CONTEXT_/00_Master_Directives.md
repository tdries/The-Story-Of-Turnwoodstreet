# 00 — Master Directives

These directives govern all AI contributions to this project.
Every file generated, every NPC written, every mechanic designed must follow them.

---

## The Game

**Title:** Turnhoutsebaan RPG
**Tagline:** "Live and let live — de straat is van iedereen."
**Engine:** Phaser.js 3.87 + TypeScript + Vite
**Platform:** Browser (desktop + mobile)
**Genre:** 2D top-down oblique RPG / walking sim with turn-based combat

---

## Core Directives

### 1. AUTHENTICITY OVER FANTASY
Every location, shop name, house number, street name, and cultural reference must be grounded in real Borgerhout. We are making a love letter to a real place. Do not invent generic "fantasy" content when a real Borgerhout equivalent exists.

### 2. COMMUNITY OVER CONFLICT
The game's central theme is **coexistence and solidarity**. Combat is rare and thematically motivated (vs. bureaucrats, speculators, historical prejudice). The dominant game mechanic is *dialogue, exploration, and quest chains built on trust*.

### 3. MULTILINGUAL BY DESIGN
NPC dialogue should reflect the real linguistic texture of the Turnhoutsebaan:
- Dutch (standard + Antwerp dialect)
- Moroccan Darija phrases (romanised, with in-game subtitle)
- Berber/Tamazight greetings
- Turkish phrases for Turkish-heritage NPCs
- French for administrative contexts
Youth NPCs code-switch Dutch/Darija naturally.

### 4. PIXEL ART STANDARDS
- 32-colour master palette (see palette.json)
- NW light source (top-left)
- 4× game pixels (SCALE=4 in SVGSheet)
- PNG export at 2× game resolution
- crispEdges rendering always
- No anti-aliasing, no gradients inside sprites

### 5. ARCHITECTURE RULES
- **No logic in scenes** — scenes orchestrate, systems process
- **No Phaser imports in systems** — CombatSystem, InventorySystem etc. are pure TypeScript
- **State lives in StateManager** — never in scene local vars that can be lost on restart
- **Data lives in JSON** — items, enemies, dialogue, skills are all in src/data/
- **All strings go through dialogue.json** — no hardcoded NPC dialogue in TypeScript

### 6. PERFORMANCE BUDGET
- Target: 60fps on a mid-range laptop
- Max 200 active physics bodies at once
- Tilemap + Y-sorted entity depth = painter's algorithm
- Background art is static graphics objects; foreground entities use physics sprites

---

## File Ownership Map

| Directory               | Owns                                      |
|------------------------|-------------------------------------------|
| `src/core/`            | GameConfig, StateManager, InputHandler    |
| `src/scenes/`          | Scene lifecycle and orchestration only    |
| `src/entities/`        | Sprite wrappers + animation definitions   |
| `src/systems/`         | Pure game logic (no Phaser deps)          |
| `src/ui/`              | Camera-fixed overlay components           |
| `src/data/`            | JSON data files (items, enemies, etc.)    |
| `assets/Sprites/`      | Generated PNG spritesheets                |
| `assets/maps/`         | Tiled/LDtk JSON tilemaps                  |
| `_AI_CONTEXT_/`        | These docs — context for AI sessions      |
| `skills/`              | AI skill prompt files                     |
