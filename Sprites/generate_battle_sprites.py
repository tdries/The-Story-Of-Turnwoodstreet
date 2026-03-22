#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — Battle Character Sprites
=============================================
Horizontal sheet: 7 frames × 48×64 game-px.

Frame index:
  0 = player_youssef   (faces right, setFlipX in BattleScene → faces left)
  1 = straatvechter    (faces left,  setFlipX in BattleScene → faces right)
  2 = pickpocket       (faces left,  setFlipX in BattleScene → faces right)
  3 = bulldozer_bureau (faces left,  setFlipX in BattleScene → faces right)
  4 = speculant        (faces left,  setFlipX in BattleScene → faces right)
  5 = tram_geest       (faces left,  setFlipX in BattleScene → faces right)
  6 = vlok_geest       (faces left,  setFlipX in BattleScene → faces right)

Sheet: 336×64 game-px → PNG at out_scale=8: 2688×512 px.
Phaser: frameWidth=384, frameHeight=512.
Display in BattleScene: setDisplaySize(44, 56) enemies, setDisplaySize(36, 48) player.
"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generate_sprites import SVGSheet

OUT_SCALE  = 8
FW, FH     = 48, 64
NUM_FRAMES = 7
SHEET_W    = FW * NUM_FRAMES  # 336
SHEET_H    = FH               # 64

OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Sprites', 'battle')
SVG_PATH = os.path.join(OUT_DIR, 'battle_sprites.svg')
PNG_PATH = os.path.join(OUT_DIR, 'battle_sprites.png')

os.makedirs(OUT_DIR, exist_ok=True)


def q(s: SVGSheet, ox: int, x: int, y: int, col: str, w: int = 1, h: int = 1):
    """Place pixel at frame-local (x,y) offset by ox."""
    s.put(ox + x, y, col, w, h)


# ── Frame 0: Player Youssef — battle stance, fists raised ────────────────────
def draw_player(s: SVGSheet, ox: int = 0):
    """White hoodie w/ blue hood, dark pants, Moroccan skin. Faces right."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    SKIN    = "cream_dark"
    SKIN_LT = "cream_mid"
    SKIN_SH = "ochre"
    HAIR    = "black"
    JACKET  = "white"
    JAC_SH  = "stone_light"
    HOOD    = "de_lijn_blue"
    PANTS   = "stone_dark"
    SHOE    = "white"
    SHOE_S  = "de_lijn_blue"
    SOLE    = "asphalt_dark"

    # ── Hood
    p(16,  7, HOOD, 16,  5)   # hood top dome
    p(14, 10, HOOD,  3, 14)   # hood left drape
    p(31, 10, HOOD,  3, 14)   # hood right drape
    p(16,  7, JACKET, 2, 12)  # hood face-opening left rim
    p(30,  7, JACKET, 2, 12)  # hood face-opening right rim

    # ── Hair
    p(19,  8, HAIR, 10,  3)   # hair top
    p(18, 10, HAIR, 12,  5)   # hair bulk

    # ── Face (y=11..23)
    p(19, 11, SKIN,   10, 12) # face
    p(19, 11, SKIN_LT, 5,  3) # forehead highlight
    p(27, 13, SKIN_SH, 2,  6) # right cheek shadow
    # Eyes
    p(20, 15, HAIR, 3, 1)     # left eye brow+eye
    p(24, 15, HAIR, 3, 1)     # right eye
    p(20, 16, HAIR, 2, 1)     # pupils
    p(25, 16, HAIR, 2, 1)
    # Determined mouth
    p(21, 21, SKIN_SH, 6, 1)
    p(21, 20, SKIN_SH, 2, 1)  # left grimace
    p(25, 20, SKIN_SH, 2, 1)  # right grimace
    # Nose
    p(23, 18, SKIN_SH, 3, 3)
    # Ears
    p(17, 15, SKIN, 2, 5)
    p(29, 15, SKIN, 2, 5)
    # Neck
    p(21, 23, SKIN, 6, 4)
    p(24, 24, SKIN_SH, 2, 3)

    # ── Torso (y=27..44)
    p(17, 27, JACKET, 14, 18)
    p(17, 27, JAC_SH,  2, 18)  # left edge shadow
    p(29, 27, JAC_SH,  2, 18)  # right edge shadow

    # ── Left arm raised (fist up, near side at left of frame)
    p(11, 25, JACKET, 6, 13)   # upper arm
    p( 9, 19, JACKET, 6,  8)   # forearm raised
    # Left fist
    p( 9, 13, SKIN,   5,  7)
    p( 9, 13, SKIN_SH,1,  6)   # fist left shadow
    p(13, 13, SKIN_SH,1,  6)   # fist right shadow

    # ── Right arm raised (fist up, far side at right of frame)
    p(31, 25, JACKET, 6, 13)
    p(33, 19, JACKET, 6,  8)
    # Right fist
    p(34, 13, SKIN,   5,  7)
    p(33, 13, SKIN_SH,1,  6)
    p(38, 13, SKIN_SH,1,  6)

    # ── Pants (y=45..57)
    p(18, 45, PANTS, 12, 13)
    p(24, 45, SOLE,   1, 13)   # centre seam
    p(29, 46, SOLE,   2, 11)   # right shadow

    # ── Shoes (y=58..63)
    p(17, 58, SHOE, 7, 5)
    p(24, 58, SHOE, 7, 5)
    p(17, 59, SHOE_S, 7, 1)
    p(24, 59, SHOE_S, 7, 1)
    p(16, 61, SOLE, 8, 3)
    p(24, 61, SOLE, 8, 3)


# ── Frame 1: Straatvechter — dark hoodie, aggressive stance ──────────────────
def draw_straatvechter(s: SVGSheet, ox: int = FW):
    """Street thug: dark grey hoodie, white skin, menacing. Faces left."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    SKIN    = "cream_mid"
    SKIN_SH = "cream_dark"
    HAIR    = "asphalt_dark"
    HOOD    = "asphalt_mid"
    HOOD_SH = "asphalt_dark"
    HOOD_LT = "asphalt_light"
    PANTS   = "stone_dark"
    SHOE    = "asphalt_dark"
    SOLE    = "night"

    # ── Hood up (menacing, hood casts face in shadow)
    p(16,  7, HOOD, 16,  5)
    p(14, 10, HOOD,  3, 15)
    p(31, 10, HOOD,  3, 15)
    p(14, 10, HOOD_LT, 1, 14) # lit left edge (light from right)
    p(31, 10, HOOD_SH, 2, 14)
    p(16,  7, HOOD_LT, 5,  3) # hood dome highlight

    # ── Hair (barely visible under hood)
    p(19,  9, HAIR, 10,  3)
    p(18, 11, HAIR, 12,  4)

    # ── Face (shadowed, harsh)
    p(18, 12, SKIN,   12, 12)
    p(18, 12, SKIN_SH, 4,  8) # left shadow (facing left = light from right)
    p(28, 13, SKIN_SH, 2,  7) # right deep shadow
    # Heavy brows
    p(19, 14, HAIR,  4,  2)   # left brow
    p(25, 14, HAIR,  4,  2)   # right brow
    # Narrowed eyes
    p(19, 16, HAIR,  4,  2)   # left eye (squinting)
    p(25, 16, HAIR,  4,  2)   # right eye
    p(20, 17, SKIN_SH, 2, 1)  # eye shadow
    p(26, 17, SKIN_SH, 2, 1)
    # Snarl
    p(20, 21, HAIR,  8,  1)   # mouth line (tight/angry)
    p(19, 20, SKIN_SH, 2, 2)  # left jaw tension
    p(27, 20, SKIN_SH, 2, 2)
    # Nose
    p(23, 17, SKIN_SH, 3,  4)
    # Neck / jaw
    p(20, 23, SKIN, 8, 3)
    p(20, 24, SKIN_SH, 3, 2)

    # ── Torso (y=26..46, broad)
    p(15, 26, HOOD, 18, 21)
    p(15, 26, HOOD_LT, 2, 21)
    p(31, 26, HOOD_SH, 2, 21)

    # ── Right arm raised threatening (near side, faces left so right is near)
    p(31, 23, HOOD,  6, 15)
    p(35, 16, HOOD,  5,  9)
    # Right fist (raised, close to viewer)
    p(35, 11, SKIN,   5,  6)
    p(35, 11, SKIN_SH,1,  5)
    p(39, 11, SKIN_SH,1,  5)

    # ── Left arm at side (far side)
    p( 9, 26, HOOD,  6, 20)
    p( 9, 44, SKIN,  5,  4)   # left hand

    # ── Pants
    p(16, 47, PANTS, 16, 13)
    p(24, 47, SOLE,   1, 11)
    p(30, 48, SOLE,   2, 10)

    # ── Shoes
    p(15, 58, SHOE, 8,  6)
    p(24, 58, SHOE, 8,  6)
    p(14, 61, SOLE, 9,  3)
    p(24, 61, SOLE, 9,  3)


# ── Frame 2: Pickpocket (Zakkenroller) — nimble, hooded, reaching ─────────────
def draw_pickpocket(s: SVGSheet, ox: int = 2 * FW):
    """Smaller, hunched, grey hood up, one hand reaching. Faces left."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    SKIN    = "cream_mid"
    SKIN_SH = "cream_dark"
    HOOD    = "stone_mid"
    HOOD_SH = "stone_dark"
    HOOD_LT = "stone_light"
    PANTS   = "stone_dark"
    SHOE    = "stone_dark"
    SOLE    = "night"
    SHADOW  = "asphalt_dark"

    # Character is smaller/shorter: head starts at y=12, feet at y=60
    # ── Hood (fully up, shadowed face)
    p(17, 12, HOOD, 14, 12)    # hood dome
    p(15, 16, HOOD,  3, 14)    # left drape
    p(30, 16, HOOD,  2, 14)    # right drape
    p(17, 12, HOOD_LT, 5,  3)  # dome highlight
    p(27, 14, HOOD_SH, 4, 10)  # right shadow

    # ── Face (barely visible, shadowed under hood)
    p(18, 18, SHADOW, 10,  8)  # dark face shadow
    p(19, 19, SKIN_SH, 5,  5)  # faint skin
    # Glinting eyes in shadow
    p(20, 20, HOOD_LT, 2,  1)
    p(24, 20, HOOD_LT, 2,  1)

    # Neck
    p(21, 26, HOOD,  6,  3)

    # ── Body (hunched, slightly forward-leaning)
    p(16, 29, HOOD, 16, 17)
    p(16, 29, HOOD_LT, 2, 17)
    p(30, 29, HOOD_SH, 2, 17)

    # ── Right arm extended forward (reaching/stealing, near side, faces left)
    p(30, 28, HOOD,  7, 12)
    p(35, 21, HOOD,  6, 10)
    p(39, 17, SKIN,  4,  5)   # reaching hand
    p(38, 17, SKIN_SH,1, 4)
    p(42, 18, SKIN_SH,1, 3)   # extended finger

    # ── Left arm (far side, tucked in body)
    p( 9, 29, HOOD,  7, 18)

    # ── Pants (shorter legs)
    p(17, 46, PANTS, 14, 13)
    p(24, 46, SOLE,   1, 11)
    p(29, 47, SOLE,   2, 10)

    # ── Shoes
    p(16, 57, SHOE, 8,  5)
    p(24, 57, SHOE, 8,  5)
    p(15, 60, SOLE, 9,  3)
    p(24, 60, SOLE, 9,  3)


# ── Frame 3: Bureau-Bulldozer — yellow hard hat, grey suit, clipboard ─────────
def draw_bulldozer_bureau(s: SVGSheet, ox: int = 3 * FW):
    """Bureaucrat boss: stocky, yellow hard hat, power suit, clipboard. Faces left."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    SKIN    = "cream_mid"
    SKIN_LT = "cream_light"
    SKIN_SH = "cream_dark"
    HAIR    = "stone_dark"
    HAT     = "de_lijn_yellow"  # bright construction hard hat
    HAT_SH  = "ochre"
    HAT_LT  = "gold"
    SUIT    = "stone_mid"
    SUIT_SH = "stone_dark"
    SUIT_LT = "stone_light"
    TIE     = "red_ui"
    SHIRT   = "white"
    CLIP    = "cream_light"     # clipboard
    CLIP_D  = "cream_dark"
    SHOE    = "asphalt_dark"
    SOLE    = "night"

    # ── Hard Hat (most iconic feature — large, imposing)
    p(13,  8, HAT,    22,  3)   # wide brim
    p(15,  4, HAT,    18,  6)   # dome
    p(15,  4, HAT_LT,  7,  2)   # shine
    p(30,  4, HAT_SH,  4,  6)   # right shadow
    p(13,  8, HAT_SH, 22,  2)   # brim underside

    # ── Face (stocky, ruddy, stern)
    p(17, 10, HAIR,   14,  4)   # hair under hat brim
    p(18, 12, SKIN,   12, 14)   # face
    p(18, 12, SKIN_LT, 5,  4)   # forehead highlight (left side, facing left = lit from right)
    p(28, 14, SKIN_SH, 3,  8)   # right shadow
    p(18, 14, SKIN_SH, 2,  6)   # left deep shadow (near side)
    # Heavy stern brows
    p(19, 15, HAIR,  4,  2)
    p(25, 15, HAIR,  4,  2)
    # Beady bureaucratic eyes
    p(19, 17, "asphalt_dark", 4, 3)
    p(25, 17, "asphalt_dark", 4, 3)
    p(20, 18, SKIN_LT, 1, 1)    # tiny glint
    p(26, 18, SKIN_LT, 1, 1)
    # Nose (bulbous authority figure)
    p(22, 21, SKIN_SH, 5,  4)
    p(22, 23, SKIN_SH, 6,  2)   # nostrils
    # Stern frown
    p(19, 24, SKIN_SH, 10, 1)
    p(19, 23, SKIN_SH,  2,  2)  # left frown crease
    p(27, 23, SKIN_SH,  2,  2)  # right frown crease
    # Double chin (authority/comfort)
    p(18, 25, SKIN,   12,  3)
    p(18, 27, SKIN_SH,12,  1)
    # Ears
    p(16, 15, SKIN,  2,  6)
    p(30, 15, SKIN,  2,  6)
    # Neck
    p(21, 28, SKIN,  6,  3)
    p(22, 28, SHIRT, 3,  4)     # collar

    # ── Suit (stocky, wide body, y=31..52)
    p(13, 31, SUIT,   22, 22)
    p(13, 31, SUIT_LT, 2, 22)
    p(33, 31, SUIT_SH, 2, 22)
    # Shirt front
    p(20, 31, SHIRT,   8,  8)
    # Power tie (red, thick)
    p(22, 31, TIE,     4, 15)
    p(23, 43, TIE,     2,  4)   # tie point
    # Lapels (wide, authoritative)
    p(14, 31, SUIT_SH, 6, 12)
    p(28, 31, SUIT_SH, 5, 12)
    # Pocket square
    p(28, 33, SHIRT,   3,  2)

    # ── Right arm: holds clipboard (near side, faces left)
    p(33, 31, SUIT,    6, 18)
    # Clipboard (beside right arm)
    p(37, 20, CLIP,    8, 16)   # board
    p(37, 20, CLIP_D,  1, 16)   # left shadow
    p(44, 20, SUIT_SH, 1, 16)   # right edge
    p(37, 20, HAT,     8,  2)   # clamp/clip (yellow = matches hard hat)
    # Paper lines
    p(38, 23, SUIT_SH, 6,  1)
    p(38, 25, SUIT_SH, 6,  1)
    p(38, 27, SUIT_SH, 6,  1)
    p(38, 29, SUIT_SH, 6,  1)
    p(38, 31, SUIT_SH, 6,  1)
    # Hand on clipboard
    p(38, 35, SKIN,    5,  4)

    # ── Left arm (far side, hanging at side)
    p( 7, 31, SUIT,    6, 20)
    p( 7, 49, SKIN,    5,  4)   # left fist (can punch paperwork)

    # ── Pants (y=53..58, wide trousers)
    p(14, 53, SUIT_SH, 20, 7)
    p(24, 53, SOLE,     1, 6)   # crease
    p(32, 54, SOLE,     2, 5)   # right shadow

    # ── Shoes (large, heavy)
    p(12, 58, SHOE, 11,  5)
    p(23, 58, SHOE, 11,  5)
    p(11, 61, SOLE, 12,  3)
    p(23, 61, SOLE, 12,  3)


# ── Frame 4: Speculant (Vastgoedspeculant) — sharp suit, smug, briefcase ──────
def draw_speculant(s: SVGSheet, ox: int = 4 * FW):
    """Real estate speculator: dark power suit, briefcase, slick hair. Faces left."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    SKIN    = "cream_light"     # well-fed pinkish
    SKIN_LT = "white"
    SKIN_SH = "cream_mid"
    HAIR    = "ochre"           # slicked-back blond/brown
    HAIR_SH = "cream_dark"
    SUIT    = "asphalt_mid"     # dark power suit
    SUIT_SH = "asphalt_dark"
    SUIT_LT = "asphalt_light"
    SHIRT   = "white"
    TIE     = "de_lijn_blue"
    BRIEF   = "wood_dark"       # leather briefcase
    BRIEF_H = "wood_light"
    SHOE    = "night"
    SOLE    = "asphalt_dark"

    # Tall, lean — weasel build
    # ── Slicked hair
    p(18,  6, HAIR,   12,  2)   # part / front
    p(17,  7, HAIR,   14,  7)   # hair bulk
    p(27,  8, HAIR_SH, 4,  5)   # right shadow
    p(18,  8, HAIR_SH, 4,  3)   # left part shadow

    # ── Face (y=12..24, smug/calculating)
    p(19, 12, SKIN,   10, 12)
    p(19, 12, SKIN_LT, 4,  3)   # forehead gloss
    p(28, 14, SKIN_SH, 2,  7)   # right shadow
    p(19, 14, SKIN_SH, 2,  6)   # left shadow (near side, faces left)
    # Beady calculating eyes
    p(20, 15, HAIR_SH, 4,  2)   # left brow
    p(25, 15, HAIR_SH, 4,  2)   # right brow
    p(21, 17, "night", 2,  2)   # left eye
    p(26, 17, "night", 2,  2)   # right eye
    p(21, 17, SKIN_LT, 1,  1)   # eye glint
    p(26, 17, SKIN_LT, 1,  1)
    # Nose (aquiline, sharp)
    p(23, 19, SKIN_SH, 3,  4)
    p(22, 22, SKIN_SH, 5,  1)   # nostril
    # Smug grin
    p(20, 23, SKIN_SH, 2,  1)   # left frown up
    p(26, 23, SKIN_SH, 2,  1)   # right (this is up = smug smirk)
    p(21, 24, SKIN_SH, 7,  1)
    # Ears
    p(17, 15, SKIN, 2,  6)
    p(29, 15, SKIN, 2,  6)
    # Neck
    p(21, 24, SKIN, 6,  4)

    # ── Suit (slim cut, y=28..50)
    p(17, 28, SUIT,   14, 23)
    p(17, 28, SUIT_LT, 2, 23)
    p(29, 28, SUIT_SH, 2, 23)
    # Shirt / tie
    p(21, 28, SHIRT,   6,  8)
    p(23, 28, TIE,     3, 16)
    p(24, 42, TIE,     1,  3)   # tie point
    # Lapels
    p(18, 28, SUIT_SH, 3, 11)
    p(28, 28, SUIT_SH, 3, 11)

    # ── Right arm: pointing/gesturing (near side, faces left)
    p(31, 28, SUIT,    5, 16)
    p(34, 20, SUIT,    5,  9)
    p(37, 14, SKIN,    4,  7)   # pointing hand
    p(36, 13, SKIN_SH, 1,  6)
    p(40, 15, SKIN_SH, 1,  4)
    p(38, 13, SKIN,    1,  3)   # pointing finger extended

    # ── Left arm: briefcase (far side)
    p(12, 28, SUIT,    5, 20)
    # Briefcase (dark leather)
    p( 6, 43, BRIEF,  12,  9)
    p( 6, 43, BRIEF_H, 2,  9)   # left highlight
    p(17, 43, SUIT_SH, 1,  9)   # right shadow
    p( 9, 41, BRIEF,   4,  3)   # handle
    p( 9, 41, BRIEF_H, 1,  2)   # handle highlight
    # Latches
    p( 8, 47, BRIEF_H, 2,  2)
    p(13, 47, BRIEF_H, 2,  2)
    # Left hand on handle
    p( 9, 50, SKIN,    6,  4)

    # ── Pants (y=51..58)
    p(18, 51, SUIT_SH, 12, 9)
    p(24, 51, SOLE,     1, 8)   # sharp crease
    p(29, 52, SOLE,     2, 7)

    # ── Shoes (narrow, polished)
    p(17, 58, SHOE,  8,  5)
    p(25, 58, SHOE,  7,  5)
    p(16, 61, SOLE,  9,  3)
    p(25, 61, SOLE,  8,  3)


# ── Frame 5: Tram Geest — spectral De Lijn conductor, glowing eyes ───────────
def draw_tram_geest(s: SVGSheet, ox: int = 5 * FW):
    """Ghostly conductor: De Lijn blue/yellow, fades at bottom. Faces left."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    GHOST   = "sky_pale"
    GHOST_D = "sky_mid"
    GHOST_L = "cloud"
    GLOW    = "sky_light"
    HAT_B   = "de_lijn_blue"
    HAT_LT  = "glass"
    BADGE   = "gold"
    UNIF    = "de_lijn_blue"
    UNIF_LT = "glass"
    UNIF_SH = "night"
    FACE    = "sky_pale"
    EYE_GL  = "white"           # glowing white eyes

    # ── Conductor Cap
    p(15,  9, HAT_B, 18,  3)    # wide brim
    p(17,  4, HAT_B, 14,  7)    # crown
    p(17,  4, HAT_LT, 5,  2)    # shine
    p(29,  4, GHOST_D, 4, 6)    # cap right shadow
    p(15,  9, UNIF_SH,18,  2)   # brim underside
    # Gold badge
    p(21,  6, BADGE,  6,  3)
    p(23,  7, GHOST_D,2,  1)    # badge detail

    # ── Ghostly face (y=12..28)
    p(17, 12, FACE,   14, 16)
    p(17, 12, GHOST_L, 6,  4)   # ectoplasmic glow top-left
    p(29, 14, GHOST_D, 3,  8)   # right shadow
    # Glowing eyes (haunting white orbs)
    p(18, 16, EYE_GL,  5,  4)
    p(25, 16, EYE_GL,  5,  4)
    p(19, 17, HAT_B,   3,  2)   # blue iris (ghostly tram colour)
    p(26, 17, HAT_B,   3,  2)
    p(20, 18, GHOST_D, 1,  1)   # pupil (very small)
    p(27, 18, GHOST_D, 1,  1)
    # Wailing open mouth
    p(19, 22, GHOST_D, 9,  5)
    p(20, 23, UNIF_SH, 7,  3)   # mouth darkness
    p(20, 22, GHOST,   2,  1)   # left lip
    p(26, 22, GHOST,   2,  1)   # right lip

    # Neck (ghostly, wispy)
    p(21, 28, GHOST, 6, 4)

    # ── Uniform (y=32..52)
    p(14, 32, UNIF,   20, 21)
    p(14, 32, UNIF_LT, 2, 21)   # left glow edge
    p(32, 32, UNIF_SH, 2, 21)   # right shadow
    # Uniform front / buttons
    p(21, 32, GHOST_L, 6,  8)   # ghostly shirt front
    # Gold buttons
    p(23, 36, BADGE,   1,  2)
    p(23, 39, BADGE,   1,  2)
    p(23, 42, BADGE,   1,  2)
    p(23, 45, BADGE,   1,  2)
    # Shoulder boards
    p(15, 32, BADGE,   6,  2)
    p(27, 32, BADGE,   6,  2)

    # ── Right arm: gesturing (near side, faces left)
    p(32, 32, UNIF_SH, 5, 16)
    p(35, 23, GHOST,   5, 11)   # ghostly forearm
    p(34, 18, GHOST_L, 5,  6)   # glowing hand / tram lantern gesture

    # ── Left arm (far side)
    p( 9, 32, UNIF_SH, 5, 16)
    p( 9, 46, GHOST,   5,  4)   # spectral hand

    # ── Ghost tail — fades to nothing (no legs/shoes)
    p(16, 53, GLOW,   16,  6)   # fade zone 1
    p(18, 59, GHOST_L,12,  4)   # fade zone 2
    p(21, 63, GHOST,   6,  1)   # wisp tail


# ── Frame 6: Vlok Geest — sinister ghost of racist '88 era ───────────────────
def draw_vlok_geest(s: SVGSheet, ox: int = 6 * FW):
    """Ghost from Vlaams Blok '88: pale, red eyes, dark aura, old suit. Faces left."""
    def p(x, y, c, w=1, h=1): q(s, ox, x, y, c, w, h)

    SKIN    = "cream_light"     # sickly pale
    SKIN_SH = "cream_mid"
    SKIN_DK = "cream_dark"
    HAIR    = "stone_light"     # greying
    HAIR_SH = "stone_mid"
    SUIT    = "stone_dark"      # dark 80s suit
    SUIT_SH = "night"
    SUIT_LT = "stone_mid"
    SHIRT   = "cream_light"
    TIE     = "red_ui"          # Flemish red
    EYE     = "red_ui"          # glowing red eyes (sinister)
    AURA    = "brick_dark"      # dark aura
    SHOE    = "night"
    SOLE    = "asphalt_dark"

    # ── Sinister aura (drawn first, behind character)
    p(13,  7, AURA,  2, 55)    # left aura pillar
    p(33,  7, AURA,  2, 55)    # right aura pillar
    p(13,  6, AURA, 22,  2)    # top aura
    p(13, 62, AURA, 22,  2)    # bottom aura

    # ── Hair (greased-back 80s style)
    p(18,  7, HAIR,   12,  3)
    p(17,  9, HAIR,   14,  6)
    p(18,  8, HAIR_SH, 3,  4)  # left parting shadow
    p(28,  9, HAIR_SH, 3,  5)  # right shadow

    # ── Face (y=13..25, pale, gaunt)
    p(18, 13, SKIN,   12, 13)
    p(18, 13, SKIN_SH, 3,  7)  # left shadow (near side, faces left)
    p(28, 15, SKIN_SH, 2,  7)  # right shadow
    # Sinister eyebrows (thick, arched evilly)
    p(19, 14, SUIT_SH, 5,  2)
    p(25, 14, SUIT_SH, 5,  2)
    # Glowing red eyes
    p(19, 16, EYE,     4,  3)
    p(25, 16, EYE,     4,  3)
    p(20, 17, "brick_mid", 2, 1)
    p(26, 17, "brick_mid", 2, 1)
    # Gaunt nose
    p(23, 19, SKIN_SH, 3,  4)
    p(22, 22, SKIN_DK, 5,  1)
    # Thin grim mouth
    p(20, 23, SKIN_DK, 8,  1)
    p(19, 22, SKIN_DK, 2,  2)  # left jowl
    p(27, 22, SKIN_DK, 2,  2)  # right jowl
    # Sideburns (70s/80s)
    p(16, 15, HAIR_SH, 3, 10)
    p(29, 15, HAIR_SH, 3, 10)
    # Ears
    p(16, 16, SKIN,  2,  6)
    p(30, 16, SKIN,  2,  6)
    # Neck
    p(21, 25, SKIN,  6,  4)
    p(22, 26, SHIRT, 3,  3)    # collar

    # ── Suit (wide 80s lapels, y=29..52)
    p(14, 29, SUIT,   20, 24)
    p(14, 29, SUIT_LT, 2, 24)  # left highlight
    p(32, 29, SUIT_SH, 2, 24)  # right shadow
    # Wide 80s lapels
    p(15, 29, SUIT_LT, 6, 14)  # left lapel
    p(27, 29, SUIT_SH, 6, 14)  # right lapel
    # Shirt front / tie
    p(21, 29, SHIRT,   6,  7)
    p(23, 29, TIE,     3, 17)  # red tie
    p(24, 43, TIE,     1,  4)  # tie point
    # Pocket square (red, like the aura)
    p(28, 31, TIE,     3,  2)

    # ── Right arm: accusing point (near side, faces left)
    p(32, 29, SUIT,    5, 16)
    p(35, 21, SUIT,    5,  9)
    p(38, 16, SKIN,    4,  6)  # pointing hand
    p(37, 15, SKIN_SH, 1,  5)
    p(41, 17, SKIN_SH, 1,  4)
    p(39, 15, SKIN,    1,  3)  # accusing index finger

    # ── Left arm (far side)
    p( 9, 29, SUIT,    5, 22)
    p( 9, 49, SKIN,    5,  4)  # left hand (clenched)

    # ── Pants (y=53..59, wide 80s cut)
    p(15, 53, SUIT_SH, 18, 8)
    p(24, 53, SUIT_SH,  1, 7)  # crease
    p(31, 54, SOLE,     2, 6)  # right shadow

    # ── Shoes (pointed 80s style)
    p(14, 59, SHOE,  9,  5)
    p(24, 59, SHOE,  9,  5)
    p(13, 62, SOLE, 10,  2)
    p(24, 62, SOLE, 10,  2)

    # ── Red aura at feet
    p(13, 63, AURA, 22,  1)


# ── Main ──────────────────────────────────────────────────────────────────────
def generate():
    s = SVGSheet(SHEET_W, SHEET_H, 'Battle Character Sprites — Turnhoutsebaan RPG')

    draw_player(s, ox=0 * FW)
    draw_straatvechter(s, ox=1 * FW)
    draw_pickpocket(s, ox=2 * FW)
    draw_bulldozer_bureau(s, ox=3 * FW)
    draw_speculant(s, ox=4 * FW)
    draw_tram_geest(s, ox=5 * FW)
    draw_vlok_geest(s, ox=6 * FW)

    s.save(SVG_PATH)
    s.to_pil(PNG_PATH, out_scale=OUT_SCALE)
    print(f"\nBattle sprites: {NUM_FRAMES} frames, {FW}×{FH} game-px each")
    print(f"PNG: {SHEET_W * OUT_SCALE}×{SHEET_H * OUT_SCALE} px → {PNG_PATH}")


if __name__ == '__main__':
    generate()
