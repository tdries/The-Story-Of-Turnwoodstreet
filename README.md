# Turnhoutsebaan RPG

> A 2D pixel-art RPG set on the real Turnhoutsebaan in Borgerhout, Antwerp — one of Belgium's most vibrant, densely populated, and culturally layered urban streets.

**Play it live:** [turnhoutsebaan.be](#) *(coming soon via Railway)*

---

## What is this?

You play as a young woman on a cargo bike navigating the Turnhoutsebaan, Borgerhout's central spine (postcode 2140). This is a real street — and almost everything in the game is real: the shops, the history, the community events, the people.

The game is set slightly in the future (year 2140, postal code becoming the year). The street's history, demographic layers, and cultural tensions are directly woven into the gameplay. The final boss is not a dragon — it is a property speculator. The hardest enemy is not defeated by combat but by sharing a meal.

The game culminates in a re-enactment of the **April 2024 "Samen Aan Tafel" event**: a 2-kilometre table on the Turnhoutsebaan, simultaneously celebrating Easter and Iftar, attended by 7,000 people of every background. That event is real. This game is its pixel-art archive.

---

## The Story (4 Acts)

### Act 1 — Aankomen (Arriving)
You arrive on the Turnhoutsebaan as a new resident. Fatima — 22 years on the street — shows you around. Omar the baker is short on flour. Yusuf the courier has a flat tyre and needs help with three deliveries. You learn how the street works.

### Act 2 — Wortels Schieten (Taking Root)
A **vastgoedspeculant** (property speculator) has bought three buildings and plans to evict the residents. You must gather signatures, collect a Vergunning document, and confront the **Bureau-Bulldozer** — a bureaucratic enemy who fights with permits and loopholes — at the district house.

Parallel: Reza's oud has a broken string. Find it → unlock the *Muziek van de Straat* skill. Visit De Roma concert hall and hear its ghost speak.

### Act 3 — Geesten van '88 (Ghosts of 1988)
A *Geest van '88* appears on the street — the spirit of the era when the Vlaams Blok used "Borgerokko" as a slur and won 40% of Borgerhout's votes. It cannot be defeated by combat. The only way to win is to use the **Samen Aan Tafel** skill: sit down and share food with your adversary. Defeating it gives you *Kracht van Gemeenschap* — the Strength of Community.

### Act 4 — 2 Kilometer Tafel (The Two-Kilometre Table)
Organise the real event. Convince 7 neighbourhood factions to join the table: the Moroccan community association, the Turkish social club, the Flemish regulars of Bar Leon, the Borgerhub art collective, the neighbourhood school, the De-Koepel Mosque, and Frituur de Tram (7,000 portions of fries). Each faction requires a different trust-building quest chain. If all 7 join, the ending triggers: a joyful, multilingual celebration.

---

## The Real History (accessible in-game as lore)

| Year | Event |
|------|-------|
| 1214 | First mention of "Borgerholt" in a Duke of Brabant act |
| 1833 | New town hall built at no. 110 |
| 1927–28 | De Roma built (Art Deco, 2,000 seats) |
| 1972 | Paul McCartney (Wings) plays De Roma, Aug 22 |
| 1972–74 | Moroccan/Turkish gastarbeiders peak; families arrive |
| 1983 | Borgerhout merged into Greater Antwerp |
| 1988 | Vlaams Blok begins "Borgerokko" slur campaign |
| 1990s | Far-right wins 40% in Borgerhout elections |
| 2003 | De Roma saved by 400 volunteers after years of decay |
| 2016 | De Roma wins inaugural Flemish Onroerenderfgoedprijs |
| Apr 2024 | 7,000-person, 2km Samen Aan Tafel (Easter + Iftar) |
| Sep 2025 | Time Out names Borgerhout world's 2nd coolest neighbourhood |

---

## Key NPCs

| Character | Background | Quest |
|-----------|-----------|-------|
| **Fatima** | Moroccan-Belgian, 45, second generation. Father arrived as gastarbeider, 1972. | The Fabric Quest — get cloth from Indian Boutique for her niece's celebration dress |
| **Omar de Bakker** | Moroccan, 38. Family bakery, open from 5am. Bakes khobz, msemmen, baklava. | Bakker Zonder Meel — flour shortage, source from Budget Market |
| **Mevrouw Baert** | Flemish, 67. Opened her shop in 1985. Watched the entire demographic transformation. *"Mijn beste klanten zijn de Marokkaanse vrouwen. Ze kennen stoffen beter dan wie ook."* | Fabric delivery item; Act 4 bridge between communities |
| **Reza** | Afghan-Belgian, 28. Oud musician. Lives near De Roma. | Find oud_string → Muziek van de Straat skill → De Roma concert cutscene |
| **Yusuf** | Moroccan courier, 31. Flat tyre, three parcels to deliver. | Starter delivery quest — introduces the street layout |
| **Aziz** | Elder, 72. Knows everyone, remembers 1972. Has a signature for the petition. | Gives lore, signs petition |
| **El Osri** | Based on real district mayor Mariam El Osri (Groen/Green). Central to Act 4. *"We willen mensen van verschillende achtergronden samenbrengen."* | Triggers the final quest chain |
| **Hamza** | Kid, 10. Plays marbles outside Bakkerij Charif. His school needs convincing. | School faction quest |
| **Sofia** | Young, phone-first. Knows everything happening on the street via group chats. | Information broker |
| **Tine** | Regular at Bar Leon. Bridge to the Flemish regulars and the Turkish social club. | Two faction quests |

---

## Locations (all real addresses)

| Address | Name | In-game |
|---------|------|---------|
| no. 137 | Indian Boutique | Quest item source (fabric bolt) |
| no. 170 | Patisserie Aladdin | Delivery stop; buy baklava |
| no. 189 | Bakkerij Charif | Omar's bakery; flour quest |
| no. 215 | Theehuys Amal | Rest point; tea consumable |
| no. 239 | Mimoun | Oud string source |
| no. 260 | Hammam Borgerhout | Buff location (recover HP) |
| no. 284 | Borger Hub | Act 3 final confrontation |
| no. 326 | Budget Market | Buy flour; general supplies |
| no. 332 | Costermans Wielersport | Repair bakfiets; unlock Bakfiets skill |
| Krugerplein | Bar Leon | Flemish faction; evening events |
| Stenenbrug 11 | De-Koepel Mosque | Mosque faction quest |

---

## Transport

- **Tram 10 (De Lijn):** Runs along the Turnhoutsebaan every 10 minutes. Use a `tram_ticket` item at any stop for fast travel between zones. Goes underground at Zegel, resurfaces at Astrid.
- **Bakfiets (cargo bike):** Player's main vehicle. Repair at Costermans Wielersport (no. 332) if broken. Unlocks the *Bakfiets-aanval* combat skill.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Game engine | [Phaser 3.87](https://phaser.io/) |
| Language | TypeScript 5.4 |
| Build tool | Vite 5.4 |
| Sprites | Python (SVG → PIL pipeline), pixel-art drawn programmatically at 64×96 game-px |
| State | `localStorage` via `StateManager` singleton |
| Dialogue | JSON trees with flag-setting, branching, and item grants |
| Quests | JSON definitions with flag-based objective checking |
| Hosting | Railway (static site) |

---

## Run Locally

```bash
git clone https://github.com/tdries/The-Story-Of-Turnwoodstreet
cd turnhoutsebaan-rpg
npm install
npm run dev
```

Open `http://localhost:5173`.

To rebuild sprites (requires Python + Pillow):

```bash
pip install Pillow cairosvg
python3 Sprites/generate_npcs.py
python3 Sprites/generate_sprites.py
```

To build for production:

```bash
npm run build
# Output: dist/
```

---

## Deploy to Railway

1. Fork this repository
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set the build command to `npm run build`
4. Set the start command to `npx serve dist`
5. Done — Railway handles the rest

---

## File Structure

```
turnhoutsebaan-rpg/
├── src/
│   ├── core/
│   │   ├── GameConfig.ts        # Resolution, scene keys, constants
│   │   ├── InputHandler.ts      # Keyboard abstraction
│   │   └── StateManager.ts      # All game state + localStorage save/load
│   ├── scenes/
│   │   ├── BootScene.ts         # Asset loading + progress bar
│   │   ├── MainMenuScene.ts     # Title screen, DOORGAAN / NIEUW SPEL
│   │   ├── OverworldScene.ts    # Main exploration scene (world, NPCs, music)
│   │   └── BattleScene.ts       # Turn-based combat overlay
│   ├── entities/
│   │   ├── Player.ts            # Bakfiets player + animation
│   │   └── NPC.ts               # Named NPCs with wander AI
│   ├── systems/
│   │   ├── DialogueSystem.ts    # Branching dialogue engine
│   │   ├── QuestSystem.ts       # Flag-based quest tracking + rewards
│   │   ├── CombatSystem.ts      # Turn-based combat logic
│   │   ├── InventorySystem.ts   # Item management
│   │   ├── SkillSystem.ts       # Skill unlock + use
│   │   └── GateSystem.ts        # Zone unlock logic
│   ├── ui/
│   │   ├── DialogueBox.ts       # Typewriter dialogue panel (bottom of screen)
│   │   ├── HUD.ts               # HP, coins, XP bar
│   │   └── InventoryMenu.ts     # In-game inventory overlay
│   └── data/
│       ├── dialogue.json        # All NPC dialogue trees
│       ├── quests.json          # Quest definitions + objectives + rewards
│       ├── items.json           # Item definitions
│       ├── skills.json          # Skill definitions
│       └── enemies.json         # Enemy stats
├── assets/
│   ├── Sprites/
│   │   ├── characters/          # Player + 10 NPC spritesheets
│   │   ├── buildings/           # Building tile atlas
│   │   ├── bikes/               # 16 bike variants
│   │   ├── vehicles/            # 7 vehicle types
│   │   ├── tram/                # Tram 10 (De Lijn)
│   │   └── characters/crowd/    # 20 pedestrian variants
│   └── audio/
│       ├── bgm/                 # Background music tracks
│       └── sfx/                 # Sound effects
├── Sprites/
│   ├── generate_npcs.py         # NPC spritesheet generator
│   └── generate_sprites.py      # SVGSheet base engine
├── _AI_CONTEXT_/                # Game design documents (for AI contributors)
│   ├── 01_Game_Design_Document.md
│   ├── 02_Architecture_State_Machine.md
│   └── 03_Asset_Manifest.md
└── Streetdata.md                # Real street data (shops, addresses)
```

---

## Open Source — Three Ways to Contribute

This game is designed to be **crowdsourced**. The street is real, the history is real, the people are real — and the more people contribute, the more accurate, beautiful, and playable it becomes.

There are three contribution tracks. You do not need to be a developer to contribute.

---

### Track A — Visuals

**What needs doing:**
- Draw new NPC sprites (Python, SVGSheet system — see `Sprites/generate_npcs.py`)
- Add building facades along the street (tile atlas: `assets/Sprites/buildings/`)
- Design new items, UI elements, or animations
- Improve the pixel-art palette and consistency
- Create crowd pedestrian variants (currently 20 — more needed)

**Files you'll touch:**
- `Sprites/generate_npcs.py` — the NPC drawing engine
- `Sprites/generate_sprites.py` — the SVGSheet base class
- `assets/Sprites/` — the PNG output directory
- `src/scenes/BootScene.ts` — to register new textures

**The palette:**
The game uses a fixed colour palette defined in `Sprites/generate_sprites.py` under `PAL`. All new sprites must use palette colours only. Key colours: `FFD700` (gold), `0A0A12` (night), `F0EAD6` (cream), `FF6633` (orange), and skin tones `cream_light` through `ochre`.

---

### Track B — Information Accuracy

**What needs doing:**
- Verify NPC dialogue against real history (`src/data/dialogue.json`)
- Check that house numbers in quests match actual shops on the street (`src/data/quests.json`)
- Add real historical events to the in-game lore system
- Correct or expand NPC backstories against real community demographics
- Add real quotes, opening hours, cultural details
- Translate dialogue (Dutch → French, Arabic, Turkish, English)

**Files you'll touch:**
- `src/data/dialogue.json` — all NPC dialogue trees
- `src/data/quests.json` — quest descriptions and objective text
- `Streetdata.md` — the street address ground truth
- `_AI_CONTEXT_/01_Game_Design_Document.md` — the GDD

**How to verify:**
The `Streetdata.md` file is the source of truth for addresses. Cross-reference against Google Maps street view, VLIZ historical records, or your own local knowledge. If you live on or near the Turnhoutsebaan — your knowledge is gold.

---

### Track C — Gameplay

**What needs doing:**
- Add new quest chains (`src/data/quests.json` + `src/data/dialogue.json`)
- Balance combat (enemy stats in `src/data/enemies.json`)
- Design new skills (`src/data/skills.json` + `src/systems/SkillSystem.ts`)
- Add new items (`src/data/items.json`)
- Improve the zone gate system (`src/systems/GateSystem.ts`)
- Build out Act 4 faction quest chains (currently stubbed)
- Add the Deurne and Wijnegem zones (currently not implemented)
- Build the time-of-day system (designed in the GDD, not yet coded)
- Create the ending cutscene (the 2km table celebration)

**Files you'll touch:**
- `src/data/` — all JSON data files
- `src/systems/` — game logic systems
- `src/scenes/OverworldScene.ts` — world layout, NPC placement

---

## Claude Code Dev Mode (In-Browser)

> This is what makes this project different.

The game will have a **Dev Mode** accessible directly from the hosted website. You bring your own Claude API key — no installation required, no local setup. Everything runs in the browser.

### How it works

1. Open the game at [turnhoutsebaan.be](#)
2. Press a hidden key combination on the main menu (to be published when ready)
3. A sidebar opens: enter your **Anthropic Claude API key** (stored only in your browser's sessionStorage — never sent anywhere except Anthropic's own API)
4. Choose your contribution track: **Visuals**, **Information**, or **Gameplay**
5. Claude Code opens a focused interface for that track:
   - **Visuals:** Edit the Python sprite generator and preview renders in real time
   - **Information:** Edit dialogue.json and quests.json with inline fact-checking
   - **Gameplay:** Edit quest and skill JSON with live validation
6. When you're happy with your changes, click **Submit as Pull Request**
7. The system opens a pre-filled GitHub PR against this repository — with your changes, a description of what you did, and which track it belongs to
8. The project owner reviews the PR, asks questions if needed, and merges or requests changes

### What this means

You do not need Git. You do not need a code editor. You do not need to understand Phaser or TypeScript. You need to know the street, care about the story, or want to make it more beautiful — and have a Claude API key.

The project owner controls the master branch. All changes go through PR review. Nothing appears in the live game without human approval.

---

## Contributing Without Dev Mode

If you prefer the traditional route:

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-contribution`
3. Make your changes
4. Open a PR with a clear description of:
   - Which track (A/B/C)
   - What you changed and why
   - Any sources for factual claims (Track B)

### PR Labels

| Label | Meaning |
|-------|---------|
| `track-A: visuals` | Sprite or art change |
| `track-B: accuracy` | Dialogue, quest text, historical fact |
| `track-C: gameplay` | Quest, combat, skill, or system change |
| `needs-review` | Waiting for owner review |
| `good-first-issue` | Suitable for first-time contributors |

---

## What Makes a Good Contribution

**Track A:**
- Stays within the established palette
- Sprites are generated via the Python pipeline (not hand-edited PNGs)
- NPC designs respect the cultural backgrounds described in the GDD

**Track B:**
- Changes are sourced (cite your source in the PR description)
- Dutch text should be checked by a Dutch speaker
- Real people (El Osri, etc.) should be represented respectfully and accurately

**Track C:**
- New quests should fit the four-act structure
- New skills should have a narrative reason to exist
- Balance changes should include a brief justification

---

## What We Will Not Merge

- Dialogue that stereotypes or demeans any community
- Quests that misrepresent real historical events
- Sprites that do not follow the palette and pipeline
- Gameplay mechanics that contradict the non-violent resolution themes
- Changes to the core message: **the street's strength is its coexistence**

---

## A Note on the Real Street

The Turnhoutsebaan is not a backdrop. It is the subject. The shops in this game are real shops. The historical events in this game happened. The 2km table in April 2024 was real, with 7,000 attendees.

If you know someone who lives or works there — ask them. Their answer might become the next quest.

In September 2025, Time Out magazine named Borgerhout the **second coolest neighbourhood in the world**. This game is being built at that moment. It is a pixel-art portrait of a street that the world just started paying attention to — made by the people who already knew.

---

## License

MIT — fork it, remix it, deploy it. If you build something based on this, tell us about it.

---

## Maintainer

Built and maintained by Tim Dries. Questions, ideas, and long messages about Borgerhout are welcome.

*Samen Aan Tafel.*
