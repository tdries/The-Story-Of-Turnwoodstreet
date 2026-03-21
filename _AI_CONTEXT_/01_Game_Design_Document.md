# 01 — Game Design Document (GDD)
## Turnhoutsebaan RPG — Borgerhout, Antwerpen

---

## 1. LOGLINE

A 2D pixel-art RPG set on the real Turnhoutsebaan in Borgerhout, Antwerp (2140).
You play as a young woman navigating a multicultural urban neighbourhood: building trust with shopkeepers, running errands for neighbours, uncovering the street's layered history, and defending the community from gentrification forces and ghosts of past prejudice.

---

## 2. THE WORLD

### Geography
The Turnhoutsebaan is the central spine of **Borgerhout Intra Muros** — one of the most densely populated and diverse urban areas in Belgium. It runs east–west through Borgerhout (2140), continues into Deurne (2100), and ends at Wijnegem (2110).

**Key zones in the game:**
- **Zone 1 — Borgerhout West** (nos. 1–110): Start area. La Cosa, Le Sud, Reuzenhof, Reuzenpoort.
- **Zone 2 — Borgerhout Central** (nos. 110–200): Old Town Hall, Stunt Solderie, Beno Cycling, Oxfam.
- **Zone 3 — Borgerhout East / De Roma** (nos. 200–300): Beno Cycling, De Roma, Snack Roma, mosque.
- **Zone 4 — Deurne** (nos. 1–247): Cogelsplein tram junction, different architectural character.
- **Zone 5 — Wijnegem** (nos. 1–471): End-game area, Wijnegem Shopping, suburban character.

### The Two Borgerhouts
- **Intra Muros** (inside the old city walls): Dense, diverse, everything interesting. The game world.
- **Extra Muros** (outside): Te Boelaerpark (16 ha). Optional exploration zone. Peaceful.

---

## 3. STORY

### Act 1 — Aankomen (Arriving)
The player arrives on the Turnhoutsebaan as a new resident. Meets Fatima (22-year resident), Omar the baker, Mrs. Baert of Stunt Solderie. Learns the rhythms of the street. First quest: deliver a parcel for the overworked courier.

### Act 2 — Wortels Schieten (Taking Root)
A **vastgoedspeculant** (property speculator) has bought three buildings and wants to evict the residents. The player must gather signatures, find the Vergunning (permit) document, and confront the Bureau-Bulldozer enemy at the district house.

Parallel quest: Reza's broken oud string → find it → unlock "Muziek van de Straat" skill.

### Act 3 — Geesten van '88 (Ghosts of '88)
Historical mini-arc. A "Geest van '88" enemy appears — representing the Vlaams Blok era when anti-immigrant politicians won 40% of Borgerhout votes. Defeated not by combat but by the "Samen Aan Tafel" skill: sharing food with adversaries.

### Act 4 — 2 Kilometer Tafel (The 2km Table)
Final quest: Organise the real historical event. The player must convince 7 neighbourhood factions (Moroccan association, Turkish social club, Belgian Flemish café, art gallery, school, mosque, frituur) to all join the 2km iftar/Easter table. Each requires a different trust-building quest chain. If all 7 join, the "Samen Aan Tafel" ending triggers: a joyful, multilingual celebration scene.

---

## 4. KEY NPCS

### Fatima (Turnhoutsebaan ~120)
- Age: 45 | Background: Moroccan-Belgian, second generation
- Father came as gastarbeider 1972, textile industry
- Speaks: Dutch (fluent), Darija, French
- Quest: The Fabric Quest (get fabric from Stunt Solderie for her niece's celebration dress)
- Unlocks: Solidarity Shout skill

### Omar de Bakker (Turnhoutsebaan ~85)
- Age: 38 | Background: Moroccan, runs family bakery
- Bakes khobz, msemmen, baklava; open from 5am
- Quote: "Tijdens de Ramadan bak ik soms tot middernacht."
- Quest: "Bakker zonder meel" — flour shortage, player must source from the market
- Reward: Harira (consumable)

### Mevrouw Baert (Turnhoutsebaan 74 — Stunt Solderie)
- Age: 67 | Background: Flemish Belgian, opened Stunt Solderie in 1985
- Has watched the entire demographic transformation
- Quote: "Mijn beste klanten zijn de Marokkaanse vrouwen. Ze kennen stoffen beter dan wie ook."
- Quest: The Fabric Delivery quest (gives player fabric_bolt item)

### Reza (near De Roma)
- Age: 28 | Background: Afghan-Belgian, oud musician
- Quest: Find oud_string item → triggers "Muziek van de Straat" skill
- Unlocks the De Roma evening concert cutscene

### Districtsvoorzitter El Osri
- Based on real district mayor Mariam El Osri (Groen/Green)
- Central to Act 4 — organises the 2km table
- Quote: "We willen mensen van verschillende achtergronden samenbrengen."
- Triggers final quest chain

### De Roma Geest (Turnhoutsebaan 286)
- Friendly spirit of the concert hall, Art Deco aesthetic
- Gives lore: Paul McCartney (Wings, Aug 22, 1972), Yes (Jan 20, 1972)
- Saved in 2003 by 400 volunteers after years of decay

### Geest van '88 (enemy)
- Manifests from the years of Vlaams Blok dominance
- Shouts: "Borgerokko!" — a real slur used in that era
- Cannot be defeated by combat — only by "Samen Aan Tafel" skill
- Defeating it gives the "Kracht van Gemeenschap" quest flag

---

## 5. LANDMARKS (IN-GAME)

| Landmark | Address | In-game function |
|---------|---------|-----------------|
| La Cosa | no. 11 | Restaurant — buy food items, meet NPCs |
| Le Sud | no. 6 | Café — rest point, saves game |
| Reuzenpoort | no. 110 | Locked gate — requires reuzenpoort_key |
| Old Town Hall | no. 110 | Quest hub — permit documents |
| Oxfam Wereldwinkel | no. 94 | Buy fair-trade items; quest item source |
| Beno Cycling | nos. 203–205 | Repair bakfiets; unlock Bakfiets skill |
| De Roma | no. 286 | Major story location; concert cutscene |
| Snack Roma | no. 285–295 | Buy food, gossip with locals |
| Mosque | no. 315 | Community anchor; safe zone during combat |
| Baillien Toys | no. 330 | Buy marbles for kid NPCs; mini-game |
| Mirakeltje / de Vriendjes | nos. 337, 364 | Children's quest chain hub |
| Krugerplein | (side street) | Green park, only one in Intra Muros |
| Bar Leon | Krugerplein | Community café, evening events |
| TRIX | Noordersingel 28 | Side-area; music quest chain |
| Borgerhub | Former courthouse | Market — sell misc items |
| De-Koepel Mosque | Stenenbrug 11 | Dutch-language Islamic centre |
| Te Boelaerpark | Extra Muros | Optional exploration, peaceful |

---

## 6. TRANSPORT MECHANICS

**Tram 10 (De Lijn):**
- Runs every 10 minutes along the Turnhoutsebaan
- Player can board by using a `tram_ticket` item at any tram stop
- Fast-travel between zones (Borgerhout → Deurne → Wijnegem)
- Goes underground at Zegel → reappears at Astrid
- 32 stops in real life; game has 6 key stops

**Cycling:**
- Player can ride a bakfiets (cargo bike) to move faster on the overworld
- Beno Cycling at no. 203 repairs it if broken
- Unlocks "Bakfiets-aanval" combat skill

---

## 7. SENSORY BIBLE
*(Guides art direction and sound design)*

**Sounds:**
- Tram 10's metallic squeal on tracks every ~10 minutes (ambient loop)
- Arabic and Darija voices from shopfront interiors
- Call to prayer at dusk (from 2 mosques, slightly different timing)
- Turkish pop / raï from a shop radio
- Kids shouting in Dutch-Darija code-switch
- Frying hiss from the frituur snack bar
- At night during Ramadan: much louder, busier, joyful

**Smells (described in item/location text):**
- Cumin, ras el hanout from sacks on the pavement
- Mint and orange blossom from the tea house
- Grilling meat from the halal butcher
- Fresh bread at 7am from Omar's bakery
- During Ramadan evening: harira, dates, frying dough

**Time-of-day system:**
- Dawn (06:00–09:00): Bakers, market vendors setting up, quiet
- Morning (09:00–12:00): Commuters, school drop-off
- Midday (12:00–15:00): School rush, lunch spots busy, tram packed
- Afternoon (15:00–18:00): Elderly on Krugerplein benches, kids out
- Evening (18:00–21:00): Busy street, if Ramadan → packed and festive
- Night (21:00–03:00): Bars, TRIX shows, tram until 03:00

---

## 8. WORLD HISTORY (ACCESSIBLE IN-GAME)

Available through lore items, dialogue, and the "Historisch Museum" mini-zone at Turnhoutsebaan 110:

- **1214** — First mention of "Borgerholt" in a Duke of Brabant act
- **1713** — Reuzenhuis built; Reuzenpoort gateway erected
- **1833** — New town hall built at no. 110 (Josephus Hoefnagels)
- **1850–1853** — Street paved with cobblestones, sewage installed
- **1879** — Krugerplein opened
- **1886** — Moorkensplein district house built (Flemish neo-Renaissance)
- **1900** — Streets named for Boer War generals (Krugerplein, Bothastraat, etc.)
- **1927–1928** — De Roma built (Alphonse Pauwels, Art Deco, 2000 seats)
- **1972** — Paul McCartney (Wings) plays De Roma, Aug 22. Yes plays Jan 20.
- **1972–1974** — Moroccan/Turkish gastarbeiders peak; families begin arriving
- **1983** — Borgerhout merged into Greater Antwerp (was independent municipality)
- **1988** — Vlaams Blok begins using "Borgerokko" as anti-immigration slur
- **1990s** — Far-right wins 40% in Borgerhout; menacing street presence
- **2002** — De Roma listed as protected monument
- **2003** — De Roma saved by Paul Schyvens + 400 volunteers
- **2015** — De Roma restoration (€2.8M)
- **2016** — De Roma wins inaugural Flemish Onroerenderfgoedprijs
- **April 2024** — 7000-person 2km Samen Aan Tafel (Easter + Iftar)
- **September 2025** — Time Out names Borgerhout world's 2nd coolest neighbourhood
