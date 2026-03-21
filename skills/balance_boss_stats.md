# Skill: Balance Boss Stats

## Usage
"Balance the [enemy_id] boss for level [N] players."

## Tuning Formula

Given player level N:
- `player.atk` ≈ 5 + (N-1)*2
- `player.def` ≈ 2 + (N-1)*1
- `player.maxHp` ≈ 20 + (N-1)*5

Target fight duration: **4–6 player turns** for a close win.

### Boss HP
```
boss.hp = player.atk * 5   (dies in ~5 turns without def)
```

### Boss ATK
```
boss.atk = player.maxHp / 5   (player can take ~5 hits before dying)
```

### Boss DEF
```
boss.def = 1–4   (1 = glasscannon, 4 = tankier)
```

### XP / Coins Reward
```
xp    = 20 * N
coins = 5 * N
```

## Example: Vastgoedspeculant at level 3
- Player: atk=9, def=4, maxHp=30
- Boss hp: 9*5 = 45
- Boss atk: 30/5 = 6
- Boss def: 3 (medium tank)
- Reward: xp=60, coins=15

## Steps
1. Read `src/data/enemies.json`
2. Calculate with formula above
3. Edit the enemy entry — adjust hp, atk, def, xp, coins
4. Verify taunt strings are still thematically appropriate
5. If the boss drops a key item, ensure `loot` array is set

## Thematic Rule
Borgerhout bosses should feel *earned*, not frustrating. The "Samen Aan Tafel" skill should always offer a non-violent path for story-critical enemies.
