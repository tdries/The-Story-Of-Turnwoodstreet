#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — NPC Character Sprites  (detailed redraw)
=============================================================
10 story NPCs, each drawn at 64×96 game pixels (native canvas).
All coordinates are in 64×96 space; S=2 comments show the old 32×48 origin.

Output PNG at out_scale=10: 1920×960 px per character (3 × 640×960).
Phaser loading: frameWidth=640, frameHeight=960.
In-game display: setDisplaySize(20, 30) — same on-screen size.
"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generate_sprites import SVGSheet, PAL

OUT_SCALE  = 10
FW, FH     = 64, 96
NUM_FRAMES = 3
BASE_DIR   = os.path.join(os.path.dirname(__file__), "..", "assets", "Sprites", "characters", "npcs")

# ── helpers ──────────────────────────────────────────────────────────────────

def line(s, x1, y1, x2, y2, col):
    dx, dy = x2-x1, y2-y1
    steps = max(abs(dx), abs(dy), 1)
    for i in range(steps+1):
        s.put(round(x1+dx*i/steps), round(y1+dy*i/steps), col)

def make_sheet(label):
    return SVGSheet(FW*NUM_FRAMES, FH, label)

def save(sheet, npc_id):
    d = os.path.join(BASE_DIR, npc_id)
    os.makedirs(d, exist_ok=True)
    sheet.save(os.path.join(d, f"{npc_id}_sheet.svg"))
    sheet.to_pil(os.path.join(d, f"{npc_id}_sheet.png"), out_scale=OUT_SCALE)


# ── shared head helpers ───────────────────────────────────────────────────────
# Canvas is 64×96; head occupies roughly y=4..28, neck y=28..32.
# eye_x is the absolute x of the right (visible) eye pupil.

def draw_head_bare(s, ox, oy, skin, skin_lt, skin_shd, hair, hair_lt, eye_x):
    """3/4 right-facing bare head with detailed face."""
    # ── hair ─────────────────────────────────────────────────────────────────
    s.put(ox+22, oy+ 4, hair,    18,  3)   # crown
    s.put(ox+20, oy+ 7, hair,    22,  8)   # bulk sides
    s.put(ox+20, oy+ 7, hair,     4, 12)   # left sideburn
    s.put(ox+38, oy+ 7, hair,     4, 12)   # right sideburn
    s.put(ox+22, oy+ 4, hair_lt,  6,  2)   # NW crown highlight
    s.put(ox+26, oy+ 6, hair_lt,  4,  1)   # glint
    # ── face ─────────────────────────────────────────────────────────────────
    s.put(ox+22, oy+ 8, skin,    18, 14)   # face block
    s.put(ox+20, oy+10, skin,     2,  8)   # left cheek
    s.put(ox+40, oy+10, skin,     2,  8)   # right cheek
    # forehead highlight strip
    s.put(ox+22, oy+ 8, skin_lt,  8,  2)
    # right cheek shadow (light source left)
    s.put(ox+36, oy+11, skin_shd, 4,  8)
    s.put(ox+22, oy+21, skin_shd,18,  2)   # chin underside shadow
    # ── brows ────────────────────────────────────────────────────────────────
    s.put(ox+24, oy+12, hair,     4,  1)   # left brow (barely visible)
    s.put(eye_x-2,oy+12,hair,     6,  2)   # right brow (prominent)
    # ── eyes ─────────────────────────────────────────────────────────────────
    # Right eye (facing right, this is the near eye)
    s.put(eye_x-2, oy+14, "black",   8,  1)   # upper eyelid line
    s.put(eye_x-2, oy+15, "white",   8,  4)   # eye white
    s.put(eye_x,   oy+15, "de_lijn_blue", 4, 4)  # iris
    s.put(eye_x+1, oy+16, "black",   2,  2)   # pupil
    s.put(eye_x-2, oy+18, hair,      8,  1)   # lower lash
    s.put(eye_x-2, oy+14, skin_shd,  2,  1)   # inner corner shadow
    # Left eye (far side, simplified)
    s.put(ox+24,   oy+14, hair,      2,  1)   # far eyelid hint
    s.put(ox+24,   oy+15, skin_shd,  2,  3)   # far eye in shadow
    # ── nose ─────────────────────────────────────────────────────────────────
    s.put(ox+29,   oy+18, skin_shd,  4,  4)   # nose bridge shadow
    s.put(ox+28,   oy+20, skin_shd,  6,  2)   # nostril area
    s.put(ox+28,   oy+18, skin_lt,   2,  2)   # nose bridge highlight
    # ── mouth ────────────────────────────────────────────────────────────────
    s.put(ox+25,   oy+22, skin,      8,  2)   # upper lip zone
    s.put(ox+26,   oy+22, skin_shd,  6,  1)   # mouth line
    s.put(ox+25,   oy+24, skin,      8,  2)   # lower lip zone
    s.put(ox+26,   oy+24, skin_lt,   4,  1)   # lower lip highlight
    # ── ears ─────────────────────────────────────────────────────────────────
    s.put(ox+20,   oy+13, skin,      2,  6)   # left ear (hidden)
    s.put(ox+40,   oy+13, skin,      2,  6)   # right ear
    s.put(ox+40,   oy+15, skin_shd,  2,  3)   # ear inner shadow
    s.put(ox+41,   oy+13, skin_shd,  1,  4)   # ear outer edge
    # ── neck (extended to bridge chin gap) ───────────────────────────────────
    s.put(ox+26,   oy+22, skin,     10, 10)   # neck from chin bottom to body top
    s.put(ox+34,   oy+22, skin_shd,  4,  9)   # neck right shadow


def draw_head_hijab(s, ox, oy, skin, skin_lt, skin_shd, hijab, hijab_lt, hijab_shd, eye_x):
    """Hijab-wearing head: fabric wraps and frames the face window."""
    # ── outer hijab shape ────────────────────────────────────────────────────
    s.put(ox+18, oy+ 4, hijab,    26, 20)  # top dome
    s.put(ox+16, oy+ 8, hijab,     4, 20)  # left drape
    s.put(ox+44, oy+ 8, hijab,     4, 20)  # right drape
    s.put(ox+18, oy+24, hijab,    26,  8)  # shoulder drape
    # Hijab highlight (upper-left of dome)
    s.put(ox+20, oy+ 4, hijab_lt,  8,  3)
    s.put(ox+18, oy+ 7, hijab_lt,  3,  6)
    # Hijab shadow underside / folds
    s.put(ox+18, oy+22, hijab_shd, 8,  3)
    s.put(ox+38, oy+22, hijab_shd, 6,  3)
    s.put(ox+16, oy+14, hijab_shd, 4, 10)  # left drape shadow
    # ── face window ──────────────────────────────────────────────────────────
    s.put(ox+22, oy+ 8, skin,     18, 18)  # face
    s.put(ox+22, oy+ 8, skin_lt,   8,  2)  # forehead highlight
    s.put(ox+36, oy+12, skin_shd,  4,  8)  # right cheek shadow
    s.put(ox+22, oy+24, skin_shd, 18,  2)  # chin shadow
    # ── brows ────────────────────────────────────────────────────────────────
    s.put(ox+24, oy+12, hijab_shd, 4,  2)  # left brow
    s.put(eye_x-2,oy+12,hijab_shd, 6,  2)  # right brow
    # ── eyes ─────────────────────────────────────────────────────────────────
    s.put(eye_x-2,oy+14, "black",   8,  1)
    s.put(eye_x-2,oy+15, "white",   8,  4)
    s.put(eye_x,  oy+15, "stone_dark",4, 4)  # dark iris (Moroccan/Turkish)
    s.put(eye_x+1,oy+16, "black",   2,  2)
    s.put(eye_x-2,oy+18, hijab_shd, 8,  1)
    s.put(ox+24,  oy+14, hijab_shd, 2,  1)
    s.put(ox+24,  oy+15, skin_shd,  2,  3)
    # ── nose & mouth (same as bare head) ─────────────────────────────────────
    s.put(ox+29,  oy+18, skin_shd,  4,  4)
    s.put(ox+28,  oy+20, skin_shd,  6,  2)
    s.put(ox+28,  oy+18, skin_lt,   2,  2)
    s.put(ox+25,  oy+22, skin,      8,  2)
    s.put(ox+26,  oy+22, skin_shd,  6,  1)
    s.put(ox+25,  oy+24, skin,      8,  2)
    s.put(ox+26,  oy+24, skin_lt,   4,  1)


def draw_head_cap(s, ox, oy, skin, skin_lt, skin_shd, cap, cap_lt, cap_shd, eye_x):
    """Cap / helmet / taqiyah."""
    # ── cap dome ─────────────────────────────────────────────────────────────
    s.put(ox+20, oy+ 2, cap,     22,  8)
    s.put(ox+18, oy+ 6, cap,      4,  6)
    s.put(ox+42, oy+ 6, cap,      4,  6)
    s.put(ox+20, oy+ 2, cap_lt,   8,  2)  # gloss
    s.put(ox+18, oy+ 4, cap_lt,   2,  4)
    s.put(ox+20, oy+ 9, cap_shd, 22,  2)  # brim shadow
    s.put(ox+16, oy+11, cap,     30,  2)  # brim/visor projection
    # ── face ─────────────────────────────────────────────────────────────────
    s.put(ox+22, oy+13, skin,    18, 12)
    s.put(ox+20, oy+15, skin,     2,  8)
    s.put(ox+40, oy+15, skin,     2,  8)
    s.put(ox+22, oy+13, skin_lt,  8,  2)
    s.put(ox+36, oy+16, skin_shd, 4,  6)
    s.put(ox+22, oy+24, skin_shd,18,  2)
    # ── brows (in cap shadow) ────────────────────────────────────────────────
    s.put(ox+24, oy+13, cap_shd,  4,  2)
    s.put(eye_x-2,oy+13,cap_shd,  6,  2)
    # ── eyes ─────────────────────────────────────────────────────────────────
    s.put(eye_x-2,oy+15, "black",  8,  1)
    s.put(eye_x-2,oy+16, "white",  8,  3)
    s.put(eye_x,  oy+16, "stone_dark",4,3)
    s.put(eye_x+1,oy+16, "black",  2,  2)
    s.put(eye_x-2,oy+18, cap_shd,  8,  1)
    s.put(ox+24,  oy+16, skin_shd, 2,  3)
    # ── nose & mouth ─────────────────────────────────────────────────────────
    s.put(ox+29,  oy+20, skin_shd, 4,  3)
    s.put(ox+28,  oy+21, skin_shd, 6,  2)
    s.put(ox+28,  oy+20, skin_lt,  2,  2)
    s.put(ox+25,  oy+23, skin,     8,  2)
    s.put(ox+26,  oy+23, skin_shd, 6,  1)
    s.put(ox+25,  oy+25, skin_lt,  4,  1)
    # ── ears & neck ──────────────────────────────────────────────────────────
    s.put(ox+40,  oy+16, skin,     2,  6)
    s.put(ox+40,  oy+17, skin_shd, 2,  3)
    s.put(ox+26,  oy+26, skin,    10,  6)
    s.put(ox+34,  oy+26, skin_shd, 4,  5)


# ── 01. Fatima ────────────────────────────────────────────────────────────────

def draw_fatima(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"
    draw_head_hijab(s, ox, oy, SKIN, SKINL, SKIND,
                    "cream_mid", "white", "cream_dark", eye_x=ox+34)

    # ── long dusty-rose coat ──────────────────────────────────────────────────
    # 3-tone: shadow left, base, highlight right
    s.put(ox+16, oy+32, "brick_mid",   2, 46)   # left shadow edge
    s.put(ox+18, oy+32, "brick_light", 26, 46)  # coat body
    s.put(ox+44, oy+32, "brick_mid",   2, 46)   # right shadow edge
    # Highlight strip (NW light)
    s.put(ox+18, oy+32, "mortar",       6,  2)  # shoulder highlight
    s.put(ox+18, oy+34, "mortar",       2, 18)  # left edge highlight
    # Coat front seam
    s.put(ox+30, oy+36, "brick_mid",    2, 42)
    # Buttons (3 evenly spaced)
    for by in [40, 50, 60]:
        s.put(ox+30, oy+by, "mortar",   2,  2)
        s.put(ox+31, oy+by, "white",    1,  1)  # button highlight
    # Coat fold lines (subtle)
    s.put(ox+22, oy+52, "brick_mid",   10,  1)
    s.put(ox+20, oy+62, "brick_mid",   14,  1)
    # Collar detail
    s.put(ox+22, oy+32, "mortar",      18,  2)  # collar band
    s.put(ox+24, oy+34, "brick_light",  8,  2)

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+12, oy+34, "brick_light",  6, 28)  # left sleeve
    s.put(ox+10, oy+34, "brick_mid",    2, 28)  # sleeve shadow
    s.put(ox+12, oy+34, "mortar",       2,  2)  # sleeve highlight top
    s.put(ox+44, oy+34, "brick_light",  4, 24)  # right sleeve
    s.put(ox+48, oy+34, "brick_mid",    2, 24)

    # ── wicker bag (left hand) ────────────────────────────────────────────────
    s.put(ox+ 8, oy+50, "wood_light",  10, 18)  # bag body
    s.put(ox+ 8, oy+50, "wood_dark",    2, 18)  # bag shadow left
    s.put(ox+ 8, oy+50, "cream_mid",   10,  2)  # bag rim top
    s.put(ox+10, oy+46, "wood_light",   4,  6)  # bag handle arc L
    s.put(ox+14, oy+44, "wood_light",   4,  4)  # handle top
    # Weave pattern on bag
    for hy in range(54, 66, 4):
        s.put(ox+ 9, oy+hy, "wood_dark", 8,  1)

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+10, oy+60, SKIN,  4,  6)   # left hand
    s.put(ox+11, oy+60, SKINL, 2,  2)   # knuckle highlight
    s.put(ox+44, oy+56, SKIN,  4,  6)   # right hand
    s.put(ox+45, oy+56, SKINL, 2,  2)

    # ── legs (glimpse below long coat) ───────────────────────────────────────
    s.put(ox+24, oy+76, "stone_dark",  8, 14)
    s.put(ox+24, oy+76, "stone_mid",   2, 14)   # leg highlight
    s.put(ox+30, oy+76, "night",       2, 14)   # leg split

    # ── feet ─────────────────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+22, oy+88-lf, "stone_dark", 10,  6)
    s.put(ox+22, oy+88-lf, "stone_mid",   4,  2)   # shoe highlight
    s.put(ox+32, oy+88+rf, "stone_dark", 10,  6)
    s.put(ox+32, oy+88+rf, "stone_mid",   4,  2)


# ── 02. Omar ─────────────────────────────────────────────────────────────────

def draw_omar(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"
    draw_head_bare(s, ox, oy, SKIN, SKINL, SKIND, "black", "stone_mid", eye_x=ox+34)

    # ── dark shirt underneath ─────────────────────────────────────────────────
    s.put(ox+18, oy+32, "stone_dark", 26, 30)
    s.put(ox+14, oy+34, "stone_dark",  6, 24)  # left sleeve
    s.put(ox+12, oy+34, "night",       2, 24)  # sleeve shadow
    s.put(ox+42, oy+34, "stone_dark",  6, 24)  # right sleeve
    s.put(ox+48, oy+34, "night",       2, 24)

    # ── white apron ──────────────────────────────────────────────────────────
    s.put(ox+20, oy+32, "white",      22, 50)  # apron body
    s.put(ox+20, oy+32, "stone_pale",  8,  2)  # NW apron highlight
    s.put(ox+20, oy+34, "stone_pale",  2, 18)  # left edge highlight
    s.put(ox+40, oy+34, "stone_mid",   2, 44)  # right apron shadow
    # Apron bib top stitching
    s.put(ox+21, oy+32, "stone_mid",  20,  1)  # top hem
    # Apron center seam
    s.put(ox+30, oy+36, "stone_pale",  2, 44)
    # Apron waist strings (sides)
    s.put(ox+18, oy+48, "stone_mid",   2,  2)
    s.put(ox+42, oy+48, "stone_mid",   2,  2)
    # Apron pocket
    s.put(ox+32, oy+54, "stone_pale", 10, 12)
    s.put(ox+32, oy+54, "stone_mid",   10,  1)  # pocket top
    s.put(ox+32, oy+54, "stone_mid",    1, 12)  # pocket left

    # ── flour stains ─────────────────────────────────────────────────────────
    s.put(ox+24, oy+38, "mortar",  6,  4)
    s.put(ox+34, oy+44, "mortar",  4,  4)
    s.put(ox+22, oy+54, "mortar",  8,  4)
    s.put(ox+36, oy+56, "mortar",  4,  2)

    # ── bread in right hand ───────────────────────────────────────────────────
    if frame < 2:
        s.put(ox+44, oy+42, "cream_mid",  10,  8)   # bread body
        s.put(ox+44, oy+42, "cream_dark", 10,  2)   # crust top
        s.put(ox+44, oy+44, "mortar",      2,  2)   # score L
        s.put(ox+50, oy+44, "mortar",      2,  2)   # score R
        s.put(ox+44, oy+42, "cream_light", 4,  1)   # crust highlight

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+14, oy+52, "cream_mid",  4,  8)   # left hand (flour-dusted)
    s.put(ox+15, oy+52, "white",      2,  2)   # knuckle
    s.put(ox+44, oy+50, "cream_mid",  4,  8)   # right hand

    # ── trousers ──────────────────────────────────────────────────────────────
    s.put(ox+20, oy+76, "stone_dark", 12, 14)
    s.put(ox+20, oy+76, "stone_mid",   2, 14)
    s.put(ox+30, oy+76, "night",       2, 14)
    s.put(ox+32, oy+76, "stone_dark", 10, 14)
    s.put(ox+40, oy+76, "night",       2, 14)

    # ── shoes ─────────────────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+20, oy+88-lf, "night",  10,  6)
    s.put(ox+20, oy+88-lf, "stone_dark", 4,  2)
    s.put(ox+32, oy+88+rf, "night",  10,  6)
    s.put(ox+32, oy+88+rf, "stone_dark", 4,  2)


# ── 03. Mevrouw Baert ─────────────────────────────────────────────────────────

def draw_baert(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_light"; SKINL = "white"; SKIND = "cream_mid"

    # ── grey hair bun ─────────────────────────────────────────────────────────
    s.put(ox+22, oy+ 4, "stone_mid",  18,  4)   # bun dome
    s.put(ox+20, oy+ 8, "stone_mid",  22,  8)   # sides
    s.put(ox+20, oy+ 8, "stone_light", 4, 10)   # left side lighter
    s.put(ox+38, oy+ 8, "stone_mid",   4, 10)
    s.put(ox+22, oy+ 4, "stone_light", 8,  2)   # bun highlight
    s.put(ox+26, oy+ 6, "stone_pale",  4,  1)   # bun gloss

    # ── face (pale Flemish) ───────────────────────────────────────────────────
    s.put(ox+22, oy+ 8, SKIN,        18, 16)
    s.put(ox+20, oy+10, SKIN,         2,  8)
    s.put(ox+40, oy+10, SKIN,         2,  8)
    s.put(ox+22, oy+ 8, SKINL,        8,  2)   # forehead highlight
    s.put(ox+36, oy+12, SKIND,        4,  8)   # cheek shadow
    s.put(ox+22, oy+22, SKIND,       18,  2)

    # ── reading glasses (on face) ─────────────────────────────────────────────
    s.put(ox+22, oy+12, "stone_dark",  18,  2)  # glasses bar
    s.put(ox+22, oy+12, "stone_light",  6,  1)  # left lens glint
    s.put(ox+34, oy+12, "stone_light",  6,  1)  # right lens glint
    s.put(ox+29, oy+12, "stone_dark",   2,  2)  # nose bridge

    # ── eyes (behind glasses) ─────────────────────────────────────────────────
    s.put(ox+24, oy+14, "white",      6,  3)
    s.put(ox+26, oy+14, "stone_mid",  2,  3)   # grey iris (blue-grey)
    s.put(ox+27, oy+15, "black",      1,  1)   # pupil
    s.put(ox+24, oy+13, "stone_dark", 6,  1)   # upper lid (glasses frame)

    # ── nose & mouth (older, slight lines) ───────────────────────────────────
    s.put(ox+29, oy+18, SKIND,  4,  4)
    s.put(ox+28, oy+20, SKIND,  6,  2)
    s.put(ox+28, oy+18, SKINL,  2,  2)
    s.put(ox+25, oy+22, SKIN,   8,  2)
    s.put(ox+26, oy+22, SKIND,  6,  1)   # thinner smile line (older)
    s.put(ox+23, oy+20, SKIND,  2,  3)   # nasolabial fold L
    s.put(ox+37, oy+20, SKIND,  2,  3)   # nasolabial fold R

    # ── ears & neck ───────────────────────────────────────────────────────────
    s.put(ox+40, oy+13, SKIN,  2,  6)
    s.put(ox+40, oy+15, SKIND, 2,  3)
    s.put(ox+26, oy+22, SKIN, 10, 10)   # neck extended from face bottom to cardigan top
    s.put(ox+34, oy+22, SKIND, 4,  9)   # neck shadow

    # ── grey cardigan ─────────────────────────────────────────────────────────
    s.put(ox+16, oy+32, "stone_mid",  30, 34)
    s.put(ox+14, oy+32, "stone_dark",  2, 34)  # left shadow
    s.put(ox+46, oy+32, "stone_dark",  2, 34)
    s.put(ox+16, oy+32, "stone_light", 8,  2)  # NW highlight
    s.put(ox+16, oy+34, "stone_light", 2, 16)

    # Cardigan front opening / lapels
    s.put(ox+28, oy+32, "night",       4,  8)   # dark collar gap
    s.put(ox+28, oy+32, "stone_mid",   2,  8)   # left lapel
    s.put(ox+32, oy+32, "stone_mid",   2,  8)   # right lapel

    # Blouse visible at collar (cream)
    s.put(ox+28, oy+34, "cream_light",  4, 8)

    # Cardigan buttons (3)
    for by in [42, 50, 58]:
        s.put(ox+28, oy+by, "stone_dark", 2, 2)
        s.put(ox+28, oy+by, "stone_light",1, 1)

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+12, oy+34, "stone_mid",   4, 22)
    s.put(ox+10, oy+34, "stone_dark",  2, 22)
    s.put(ox+12, oy+34, "stone_light", 2,  2)
    s.put(ox+46, oy+34, "stone_mid",   4, 22)
    s.put(ox+50, oy+34, "stone_dark",  2, 22)

    # ── hands (resting on hips) ───────────────────────────────────────────────
    s.put(ox+12, oy+54, SKINL, 4,  6)
    s.put(ox+46, oy+54, SKINL, 4,  6)

    # ── practical trousers ────────────────────────────────────────────────────
    s.put(ox+18, oy+66, "stone_pale", 26, 22)
    s.put(ox+16, oy+66, "stone_mid",   2, 22)
    s.put(ox+44, oy+66, "stone_mid",   2, 22)
    s.put(ox+30, oy+66, "stone_mid",   2, 22)   # trouser crease

    # ── flat shoes ────────────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+18, oy+86-lf, "stone_dark", 12,  6)
    s.put(ox+18, oy+86-lf, "stone_mid",   6,  2)
    s.put(ox+32, oy+86+rf, "stone_dark", 12,  6)
    s.put(ox+32, oy+86+rf, "stone_mid",   6,  2)


# ── 04. Reza ──────────────────────────────────────────────────────────────────

def draw_reza(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"
    draw_head_bare(s, ox, oy, SKIN, SKINL, SKIND, "black", "stone_mid", eye_x=ox+34)

    # stubble shadow
    s.put(ox+22, oy+20, SKIND, 18,  4)
    s.put(ox+22, oy+20, "stone_mid", 2, 4)  # stubble texture L
    s.put(ox+36, oy+20, "stone_mid", 2, 4)  # stubble texture R

    # ── white shirt ──────────────────────────────────────────────────────────
    s.put(ox+18, oy+32, "white",     26, 36)
    s.put(ox+16, oy+34, "white",      4, 26)  # left sleeve
    s.put(ox+14, oy+34, "stone_pale", 2, 26)  # sleeve shadow
    s.put(ox+42, oy+34, "white",      4, 26)
    s.put(ox+46, oy+34, "stone_pale", 2, 26)
    s.put(ox+18, oy+32, "stone_pale", 8,  2)  # shoulder highlight
    # Shirt collar
    s.put(ox+26, oy+32, "stone_pale", 4,  4)

    # ── dark waistcoat ────────────────────────────────────────────────────────
    s.put(ox+20, oy+32, "stone_dark", 22, 34)
    s.put(ox+20, oy+32, "stone_mid",   6,  2)  # waistcoat NW
    s.put(ox+20, oy+34, "stone_mid",   2, 18)  # left edge highlight
    s.put(ox+40, oy+34, "night",       2, 30)  # right shadow
    # Vest open front (white shirt visible between lapels)
    s.put(ox+27, oy+33, "white",       8, 28)
    # Vest pocket (left breast)
    s.put(ox+22, oy+38, "stone_mid",   6,  8)
    s.put(ox+22, oy+38, "stone_dark",  6,  1)
    # Vest buttons
    for by in [42, 50, 58]:
        s.put(ox+29, oy+by, "stone_light", 2, 2)
        s.put(ox+29, oy+by, "stone_pale",  1, 1)

    # ── oud on back (pear-shaped, poking over right shoulder) ─────────────────
    s.put(ox+40, oy+16, "wood_light", 14, 28)  # oud pear body
    s.put(ox+40, oy+16, "wood_dark",   2, 28)  # shadow left
    s.put(ox+52, oy+16, "wood_dark",   2, 28)  # shadow right
    s.put(ox+42, oy+14, "wood_light",  8,  4)  # oud shoulder curve
    s.put(ox+44, oy+10, "wood_light",  6,  6)  # oud neck (thinner)
    s.put(ox+45, oy+ 6, "wood_dark",   4,  5)  # peg box
    # Sound hole
    s.put(ox+44, oy+26, "night",       6, 10)
    s.put(ox+46, oy+28, "wood_dark",   2,  6)  # hole inner
    # Strings
    s.put(ox+42, oy+18, "stone_light", 1, 22)
    s.put(ox+44, oy+18, "stone_light", 1, 22)
    s.put(ox+46, oy+18, "stone_mid",   1, 22)
    # Oud body highlight
    s.put(ox+42, oy+18, "cream_mid",   4,  3)

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+14, oy+56, SKIN, 4, 8)
    s.put(ox+15, oy+56, SKINL,2, 2)
    s.put(ox+44, oy+56, SKIN, 4, 8)
    s.put(ox+45, oy+56, SKINL,2, 2)

    # ── dark jeans ────────────────────────────────────────────────────────────
    s.put(ox+18, oy+68, "night",      12, 22)
    s.put(ox+18, oy+68, "stone_dark",  2, 22)
    s.put(ox+28, oy+68, "stone_dark",  2, 22)  # crease
    s.put(ox+30, oy+68, "night",      12, 22)
    s.put(ox+40, oy+68, "black",       2, 22)

    # ── white sneakers ────────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+16, oy+88-lf, "white",        14,  6)
    s.put(ox+18, oy+88-lf, "de_lijn_blue",  6,  2)  # stripe
    s.put(ox+16, oy+92-lf, "stone_pale",   14,  2)  # sole
    s.put(ox+30, oy+88+rf, "white",        14,  6)
    s.put(ox+32, oy+88+rf, "de_lijn_blue",  6,  2)
    s.put(ox+30, oy+92+rf, "stone_pale",   14,  2)


# ── 05. El Osri ───────────────────────────────────────────────────────────────

def draw_el_osri(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"
    draw_head_hijab(s, ox, oy, SKIN, SKINL, SKIND,
                    "night", "stone_dark", "black", eye_x=ox+34)

    # gold earrings
    s.put(ox+20, oy+20, "gold", 2,  4)
    s.put(ox+40, oy+20, "gold", 2,  4)
    s.put(ox+20, oy+22, "ochre",2,  2)

    # ── green blazer ─────────────────────────────────────────────────────────
    s.put(ox+14, oy+32, "grass",      34, 38)
    s.put(ox+12, oy+32, "night",       2, 38)  # shadow left
    s.put(ox+48, oy+32, "night",       2, 38)
    s.put(ox+14, oy+32, "stone_pale",  8,  2)  # NW lapel highlight
    s.put(ox+14, oy+34, "stone_pale",  2, 16)
    s.put(ox+46, oy+34, "night",       2, 32)  # right shadow fold

    # Lapels (open collar)
    s.put(ox+26, oy+32, "night",       8,  8)  # collar gap
    s.put(ox+26, oy+32, "grass",       4,  8)  # left lapel
    s.put(ox+32, oy+32, "grass",       4,  8)  # right lapel

    # White blouse visible
    s.put(ox+28, oy+36, "white",       6, 16)
    s.put(ox+30, oy+36, "stone_pale",  2,  2)  # blouse highlight

    # Breast pocket (right side)
    s.put(ox+38, oy+36, "stone_pale",  8,  2)  # pocket flap
    s.put(ox+38, oy+36, "stone_dark",  8,  1)
    # Blazer buttons
    for by in [44, 54]:
        s.put(ox+28, oy+by, "stone_pale", 2, 2)
        s.put(ox+28, oy+by, "gold",       1, 1)

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+10, oy+34, "grass",       4, 28)
    s.put(ox+ 8, oy+34, "night",       2, 28)
    s.put(ox+10, oy+34, "stone_pale",  2,  2)
    s.put(ox+48, oy+34, "grass",       4, 28)
    s.put(ox+52, oy+34, "night",       2, 28)
    # Sleeve cuff detail
    s.put(ox+10, oy+60, "white",       4,  2)
    s.put(ox+48, oy+60, "white",       4,  2)

    # ── tablet under left arm ─────────────────────────────────────────────────
    s.put(ox+ 6, oy+48, "stone_dark",  6, 12)
    s.put(ox+ 6, oy+48, "glass",       6, 10)
    s.put(ox+ 7, oy+49, "sky_pale",    4,  4)  # screen reflection
    s.put(ox+ 9, oy+57, "gold",        2,  2)  # home button

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+ 8, oy+60, SKIN, 4, 6)
    if frame == 0:
        s.put(ox+48, oy+58, SKIN, 4, 6)
    else:
        s.put(ox+48, oy+50, SKIN, 4, 6)   # raised hand

    # ── dark trousers (start at oy+70 to close 2px gap with blazer) ──────────
    s.put(ox+18, oy+70, "stone_dark", 12, 22)
    s.put(ox+18, oy+70, "stone_mid",   2, 22)
    s.put(ox+28, oy+70, "night",       2, 22)
    s.put(ox+30, oy+70, "stone_dark", 12, 22)
    s.put(ox+40, oy+70, "night",       2, 22)

    # ── heeled shoes ──────────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+16, oy+90-lf, "night",  14,  4)
    s.put(ox+18, oy+90-lf, "stone_dark", 6,  2)
    s.put(ox+22, oy+93-lf, "night",   4,  2)  # heel block
    s.put(ox+30, oy+90+rf, "night",  14,  4)
    s.put(ox+32, oy+90+rf, "stone_dark", 6,  2)
    s.put(ox+36, oy+93+rf, "night",   4,  2)


# ── 06. Yusuf ─────────────────────────────────────────────────────────────────

def draw_yusuf(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"

    # ── helmet ────────────────────────────────────────────────────────────────
    s.put(ox+20, oy+ 2, "stone_dark",  22, 12)   # shell
    s.put(ox+18, oy+ 6, "stone_dark",   4,  8)   # left flare
    s.put(ox+42, oy+ 6, "stone_dark",   4,  8)
    s.put(ox+20, oy+ 2, "stone_light",  10,  2)   # NW gloss
    s.put(ox+20, oy+ 4, "stone_light",   2,  4)
    s.put(ox+28, oy+ 2, "stone_mid",     4,  2)   # second gloss band
    s.put(ox+20, oy+13, "stone_dark",   22,  2)   # brim shadow
    s.put(ox+18, oy+15, "glass",        26,  4)   # visor strip
    s.put(ox+18, oy+15, "sky_pale",      8,  2)   # visor glint
    # Ventilation slots
    for vx in range(26, 40, 4):
        s.put(ox+vx, oy+ 4, "night",    2,  4)

    # ── face below visor ─────────────────────────────────────────────────────
    s.put(ox+22, oy+19, SKIN,        18,  8)
    s.put(ox+22, oy+19, SKINL,        8,  2)
    s.put(ox+36, oy+20, SKIND,        4,  5)
    s.put(ox+34, oy+21, "black",      2,  2)   # eye
    s.put(ox+32, oy+20, "stone_dark", 4,  1)   # brow in shadow
    # Chin strap + throat bridge (face ends at oy+27, vest starts at oy+30)
    s.put(ox+22, oy+27, SKIN, 18,  3)         # throat bridge
    s.put(ox+20, oy+26, "stone_mid",  2,  4)
    s.put(ox+40, oy+26, "stone_mid",  2,  4)

    # ── orange safety vest ────────────────────────────────────────────────────
    s.put(ox+14, oy+30, "ochre",      34, 38)
    s.put(ox+12, oy+30, "cream_dark",  2, 38)  # shadow
    s.put(ox+48, oy+30, "cream_dark",  2, 38)
    s.put(ox+14, oy+30, "cream_light", 8,  2)  # NW highlight
    s.put(ox+14, oy+32, "cream_light", 2, 18)
    # Reflective strips (white horizontal bands)
    s.put(ox+14, oy+42, "white",      34,  2)
    s.put(ox+14, oy+54, "white",      34,  2)
    s.put(ox+14, oy+42, "stone_pale", 34,  1)  # strip top sheen
    # Vest logo area (fake brand mark)
    s.put(ox+30, oy+36, "cream_dark",  8,  6)
    s.put(ox+32, oy+37, "ochre",       4,  4)

    # ── delivery backpack (side) ───────────────────────────────────────────────
    s.put(ox+ 8, oy+30, "stone_dark",  6, 30)
    s.put(ox+ 8, oy+30, "stone_mid",   6,  2)  # pack top
    s.put(ox+ 8, oy+30, "stone_mid",   2, 28)  # pack left highlight
    s.put(ox+13, oy+30, "stone_dark",  1, 28)  # pack seam

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+10, oy+32, "ochre",       4, 22)
    s.put(ox+ 8, oy+32, "cream_dark",  2, 22)
    s.put(ox+48, oy+32, "ochre",       4, 22)
    s.put(ox+52, oy+32, "cream_dark",  2, 22)

    # ── gloved hands ──────────────────────────────────────────────────────────
    s.put(ox+ 8, oy+56, "black",  4,  8)
    s.put(ox+ 9, oy+56, "stone_dark",2,2)
    s.put(ox+48, oy+56, "black",  4,  8)
    s.put(ox+49, oy+56, "stone_dark",2,2)

    # ── trousers ──────────────────────────────────────────────────────────────
    s.put(ox+18, oy+68, "stone_dark", 12, 20)
    s.put(ox+18, oy+68, "stone_mid",   2, 20)
    s.put(ox+28, oy+68, "night",       2, 20)
    s.put(ox+30, oy+68, "stone_dark", 12, 20)
    s.put(ox+40, oy+68, "night",       2, 20)

    # ── heavy boots ───────────────────────────────────────────────────────────
    lf = 4 if stride == 1 else 0
    rf = 4 if stride == 2 else 0
    s.put(ox+16, oy+86-lf, "black",   14,  8)
    s.put(ox+16, oy+86-lf, "stone_mid", 6,  2)
    s.put(ox+16, oy+92-lf, "stone_dark",14, 2)  # sole
    s.put(ox+30, oy+86+rf, "black",   14,  8)
    s.put(ox+30, oy+86+rf, "stone_mid", 6,  2)
    s.put(ox+30, oy+92+rf, "stone_dark",14, 2)


# ── 07. Aziz ──────────────────────────────────────────────────────────────────

def draw_aziz(s, ox, oy, frame=0):
    stride = frame
    SKIN = "ochre"; SKINL = "cream_dark"; SKIND = "wood_dark"

    # ── taqiyah (white skullcap) ──────────────────────────────────────────────
    s.put(ox+22, oy+ 4, "white",      18,  6)
    s.put(ox+20, oy+ 6, "white",       4,  6)
    s.put(ox+40, oy+ 6, "white",       4,  6)
    s.put(ox+22, oy+ 4, "stone_pale",  6,  2)  # cap highlight
    s.put(ox+24, oy+ 4, "stone_pale",  2,  4)

    # ── face (older, weathered ochre skin) ───────────────────────────────────
    s.put(ox+22, oy+10, SKIN,        18, 16)
    s.put(ox+20, oy+12, SKIN,         2,  8)
    s.put(ox+40, oy+12, SKIN,         2,  8)
    s.put(ox+22, oy+10, SKINL,        8,  2)
    s.put(ox+36, oy+13, SKIND,        4,  8)
    s.put(ox+22, oy+24, SKIND,       18,  2)
    # Age lines
    s.put(ox+23, oy+18, SKIND,  2,  4)   # crow's foot L
    s.put(ox+37, oy+18, SKIND,  2,  4)   # crow's foot R
    s.put(ox+22, oy+21, SKIND, 18,  1)   # nasolabial line

    # ── eye ───────────────────────────────────────────────────────────────────
    s.put(ox+32, oy+14, "white",    6,  4)
    s.put(ox+34, oy+14, "stone_dark",2, 4)
    s.put(ox+34, oy+15, "black",    1,  2)
    s.put(ox+32, oy+13, "stone_dark",6,  1)
    s.put(ox+32, oy+17, "stone_mid", 6,  1)  # droopy lower lid
    s.put(ox+24, oy+14, SKIND,      2,  4)   # far eye in shadow

    # ── nose (larger, older) ──────────────────────────────────────────────────
    s.put(ox+29, oy+19, SKIND,  6,  5)
    s.put(ox+28, oy+21, SKIND,  8,  3)
    s.put(ox+28, oy+19, SKINL,  2,  2)

    # ── white beard ───────────────────────────────────────────────────────────
    s.put(ox+20, oy+22, "stone_pale", 22, 10)  # beard mass
    s.put(ox+22, oy+24, "white",      18,  8)  # beard lighter centre
    s.put(ox+24, oy+26, "stone_pale", 14,  2)  # beard texture line
    s.put(ox+26, oy+28, "stone_pale", 10,  2)

    # ── ears & neck ───────────────────────────────────────────────────────────
    s.put(ox+40, oy+13, SKIN,  2,  6)
    s.put(ox+40, oy+15, SKIND, 2,  3)
    s.put(ox+26, oy+28, SKIN, 10,  4)
    s.put(ox+34, oy+28, SKIND, 4,  3)

    # ── grey djellaba (wide, flowing) ─────────────────────────────────────────
    s.put(ox+10, oy+32, "stone_mid",  42, 56)   # main body (56→oy+88 = flush with feet)
    s.put(ox+ 8, oy+32, "stone_dark",  2, 56)   # shadow left
    s.put(ox+52, oy+32, "stone_dark",  2, 56)
    s.put(ox+10, oy+32, "stone_light", 8,  2)   # NW shoulder
    s.put(ox+10, oy+34, "stone_light", 2, 18)
    # Djellaba fold lines
    s.put(ox+20, oy+50, "stone_light",  4, 20)
    s.put(ox+38, oy+46, "stone_dark",   4, 24)
    s.put(ox+28, oy+54, "stone_light",  2, 18)
    # Hood drape at shoulders
    s.put(ox+16, oy+32, "stone_light",  4,  6)
    s.put(ox+42, oy+32, "stone_light",  4,  6)

    # ── prayer beads on wrist ─────────────────────────────────────────────────
    for by in range(58, 64, 2):
        s.put(ox+48, oy+by, "ochre",  2,  2)
        s.put(ox+48, oy+by, "wood_dark", 1, 1)

    # ── walking stick ─────────────────────────────────────────────────────────
    s.put(ox+12, oy+56, "wood_dark",  2, 36)   # shaft
    s.put(ox+10, oy+56, "wood_light", 4,  2)   # crook
    s.put(ox+12, oy+90, "stone_mid",  2,  2)   # rubber tip

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+10, oy+54, SKIN, 4,  6)
    s.put(ox+46, oy+54, SKIN, 4,  6)

    # ── feet (dark shoes below djellaba) ──────────────────────────────────────
    s.put(ox+20, oy+88, "stone_dark", 10,  6)
    s.put(ox+20, oy+88, "stone_mid",   4,  2)
    s.put(ox+34, oy+88, "stone_dark", 10,  6)
    s.put(ox+34, oy+88, "stone_mid",   4,  2)


# ── 08. Sofia ─────────────────────────────────────────────────────────────────

def draw_sofia(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_light"; SKINL = "white"; SKIND = "cream_mid"

    # ── warm brown hair ────────────────────────────────────────────────────────
    s.put(ox+22, oy+ 4, "wood_dark",  18,  4)   # crown
    s.put(ox+20, oy+ 8, "wood_dark",  22,  8)   # sides
    s.put(ox+20, oy+ 6, "wood_dark",   4, 12)   # left side hair
    s.put(ox+40, oy+ 6, "wood_dark",   4, 12)   # right side hair
    s.put(ox+20, oy+26, "wood_dark",   4,  8)   # hair falls to shoulder L
    s.put(ox+40, oy+26, "wood_dark",   4,  8)   # hair falls R
    # Hair highlights
    s.put(ox+24, oy+ 4, "wood_light",  8,  2)
    s.put(ox+26, oy+ 6, "wood_light",  4,  1)

    # ── face (pale Belgian) ───────────────────────────────────────────────────
    s.put(ox+22, oy+ 8, SKIN,        18, 16)
    s.put(ox+20, oy+10, SKIN,         2,  8)
    s.put(ox+40, oy+10, SKIN,         2,  8)
    s.put(ox+22, oy+ 8, SKINL,        8,  2)
    s.put(ox+36, oy+12, SKIND,        4,  8)
    s.put(ox+22, oy+22, SKIND,       18,  2)

    # eye
    s.put(ox+32, oy+13, "black",    6,  1)
    s.put(ox+32, oy+14, "white",    6,  4)
    s.put(ox+34, oy+14, "wood_dark",2,  4)  # hazel iris
    s.put(ox+35, oy+15, "black",    1,  2)
    s.put(ox+32, oy+17, SKIND,      6,  1)
    s.put(ox+24, oy+14, SKIND,      2,  4)

    # nose/mouth
    s.put(ox+29, oy+18, SKIND,  4,  4)
    s.put(ox+28, oy+19, SKIND,  6,  2)
    s.put(ox+28, oy+18, SKINL,  2,  2)
    s.put(ox+25, oy+22, SKIN,   8,  2)
    s.put(ox+26, oy+22, "brick_light", 5, 1)  # pink lips
    s.put(ox+25, oy+24, SKIN,   8,  2)
    s.put(ox+26, oy+24, SKINL,  4,  1)

    # AirPod right ear
    s.put(ox+40, oy+16, "white", 2,  4)
    s.put(ox+40, oy+13, SKIN,    2,  6)
    s.put(ox+40, oy+15, SKIND,   2,  3)

    # ── neck (missing in original — added to connect face to jacket) ──────────
    s.put(ox+26, oy+22, SKIN,  10, 10)   # neck from face bottom to jacket top
    s.put(ox+34, oy+22, SKIND,  4,  9)   # neck right shadow

    # ── olive vintage jacket ──────────────────────────────────────────────────
    s.put(ox+14, oy+32, "grass",      34, 38)
    s.put(ox+12, oy+32, "stone_dark",  2, 38)
    s.put(ox+48, oy+32, "stone_dark",  2, 38)
    s.put(ox+14, oy+32, "stone_pale",  8,  2)
    s.put(ox+14, oy+34, "stone_pale",  2, 18)
    s.put(ox+46, oy+34, "night",       2, 32)
    # Open collar
    s.put(ox+26, oy+32, "night",       8,  6)
    s.put(ox+26, oy+32, "grass",       4,  6)
    s.put(ox+32, oy+32, "grass",       4,  6)
    # Brass buttons
    for by in [42, 50, 58]:
        s.put(ox+29, oy+by, "ochre",   2, 2)
        s.put(ox+29, oy+by, "gold",    1, 1)
    # Jacket elbow patch hint
    s.put(ox+12, oy+50, "wood_dark",   4,  6)

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+10, oy+34, "grass",       4, 26)
    s.put(ox+ 8, oy+34, "stone_dark",  2, 26)
    s.put(ox+10, oy+34, "stone_pale",  2,  2)
    s.put(ox+48, oy+34, "grass",       4, 26)
    s.put(ox+52, oy+34, "stone_dark",  2, 26)

    # ── tote bag ──────────────────────────────────────────────────────────────
    s.put(ox+ 6, oy+44, "stone_pale",  8, 22)
    s.put(ox+ 6, oy+44, "stone_mid",   2, 22)
    s.put(ox+ 6, oy+44, "stone_dark",  8,  2)  # bag top
    # Bag strap
    s.put(ox+10, oy+32, "stone_mid",   2, 14)
    # Print on bag (abstract coloured square)
    s.put(ox+ 8, oy+50, "de_lijn_blue",4,  4)
    s.put(ox+ 9, oy+52, "gold",        2,  2)
    s.put(ox+ 8, oy+54, "grass",       2,  2)

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+ 8, oy+62, SKIN, 4, 6)
    s.put(ox+ 9, oy+62, SKINL,2, 2)
    s.put(ox+48, oy+60, SKIN, 4, 6)
    s.put(ox+49, oy+60, SKINL,2, 2)

    # ── jeans (blue with paint stains) ────────────────────────────────────────
    s.put(ox+18, oy+70, "de_lijn_blue", 12, 22)
    s.put(ox+16, oy+70, "night",         2, 22)
    s.put(ox+28, oy+70, "night",         2, 22)  # crease
    s.put(ox+30, oy+70, "de_lijn_blue", 12, 22)
    s.put(ox+40, oy+70, "night",         2, 22)
    # Paint stains
    s.put(ox+20, oy+74, "white",   2,  2)
    s.put(ox+34, oy+78, "ochre",   2,  2)
    s.put(ox+24, oy+76, "red_ui",  2,  2)
    s.put(ox+36, oy+72, "grass",   2,  2)

    # ── white sneakers ────────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+16, oy+90-lf, "white",      14,  6)
    s.put(ox+16, oy+94-lf, "stone_pale", 14,  2)
    s.put(ox+30, oy+90+rf, "white",      14,  6)
    s.put(ox+30, oy+94+rf, "stone_pale", 14,  2)


# ── 09. Hamza ─────────────────────────────────────────────────────────────────

def draw_hamza(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"
    # Hamza is shorter — head starts lower
    draw_head_bare(s, ox, oy+8, SKIN, SKINL, SKIND, "black", "stone_mid", eye_x=ox+34)

    # ── blue/white tracksuit top ───────────────────────────────────────────────
    s.put(ox+16, oy+40, "de_lijn_blue", 30, 28)
    s.put(ox+14, oy+40, "night",         2, 28)
    s.put(ox+46, oy+40, "night",         2, 28)
    s.put(ox+16, oy+40, "sky_pale",      8,  2)  # NW highlight
    s.put(ox+16, oy+42, "sky_pale",      2, 16)

    # White side stripes
    s.put(ox+14, oy+42, "white",  2, 24)
    s.put(ox+46, oy+42, "white",  2, 24)

    # Zipper line
    s.put(ox+30, oy+40, "white",       2, 24)
    s.put(ox+30, oy+40, "stone_light", 2,  2)  # zip pull

    # Brand logo (small embroidered mark)
    s.put(ox+38, oy+44, "white",  4,  4)
    s.put(ox+39, oy+45, "de_lijn_blue", 2, 2)

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+10, oy+42, "de_lijn_blue", 6, 20)
    s.put(ox+ 8, oy+42, "night",        2, 20)
    s.put(ox+10, oy+42, "sky_pale",     2,  2)
    s.put(ox+46, oy+42, "de_lijn_blue", 6, 20)
    s.put(ox+52, oy+42, "night",        2, 20)

    # ── phone in right hand ───────────────────────────────────────────────────
    s.put(ox+48, oy+54, "night",  4,  8)   # phone body
    s.put(ox+48, oy+54, "glass",  4,  6)   # screen
    s.put(ox+49, oy+55, "sky_pale",2, 3)   # screen content
    s.put(ox+48, oy+62, SKIN,     4,  6)   # hand holding phone
    s.put(ox+49, oy+62, SKINL,    2,  2)

    # ── left hand ─────────────────────────────────────────────────────────────
    s.put(ox+10, oy+58, SKIN, 4,  6)
    s.put(ox+11, oy+58, SKINL,2,  2)

    # ── tracksuit bottoms ─────────────────────────────────────────────────────
    s.put(ox+16, oy+68, "de_lijn_blue", 14, 24)
    s.put(ox+14, oy+68, "night",         2, 24)
    s.put(ox+14, oy+70, "white",         2, 20)  # left stripe
    s.put(ox+28, oy+68, "night",         2, 24)
    s.put(ox+30, oy+68, "de_lijn_blue", 14, 24)
    s.put(ox+44, oy+68, "night",         2, 24)
    s.put(ox+44, oy+70, "white",         2, 20)  # right stripe

    # ── chunky sneakers ────────────────────────────────────────────────────────
    lf = 4 if stride == 1 else 0
    rf = 4 if stride == 2 else 0
    s.put(ox+14, oy+90-lf, "white",       14,  6)
    s.put(ox+16, oy+90-lf, "de_lijn_blue", 6,  2)
    s.put(ox+14, oy+94-lf, "stone_mid",   14,  4)  # thick sole
    s.put(ox+28, oy+90+rf, "white",       14,  6)
    s.put(ox+30, oy+90+rf, "de_lijn_blue", 6,  2)
    s.put(ox+28, oy+94+rf, "stone_mid",   14,  4)


# ── 10. Tine ──────────────────────────────────────────────────────────────────

def draw_tine(s, ox, oy, frame=0):
    stride = frame
    SKIN = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"

    # ── printed cotton headscarf ───────────────────────────────────────────────
    s.put(ox+20, oy+ 4, "brick_light", 22, 14)  # scarf main
    s.put(ox+18, oy+ 8, "brick_light",  4, 12)  # left wrap
    s.put(ox+42, oy+ 8, "brick_light",  4, 12)
    # Scarf NW highlight
    s.put(ox+22, oy+ 4, "mortar",        8,  2)
    s.put(ox+20, oy+ 6, "mortar",        2,  8)
    # Scarf shadow folds
    s.put(ox+20, oy+16, "brick_mid",    22,  2)
    s.put(ox+18, oy+12, "brick_mid",     4,  6)
    # Gold dot pattern on scarf
    for sx, sy in [(24,6),(28,8),(22,10),(32,6),(26,12),(30,10),(34,8)]:
        s.put(ox+sx, oy+sy, "gold", 2, 2)
    # Front hair visible
    s.put(ox+22, oy+ 8, "stone_dark",  18,  2)

    # ── face ──────────────────────────────────────────────────────────────────
    s.put(ox+22, oy+10, SKIN,        18, 14)
    s.put(ox+20, oy+12, SKIN,         2,  8)
    s.put(ox+40, oy+12, SKIN,         2,  8)
    s.put(ox+22, oy+10, SKINL,        8,  2)
    s.put(ox+36, oy+13, SKIND,        4,  8)
    s.put(ox+22, oy+22, SKIND,       18,  2)

    # eye
    s.put(ox+32, oy+13, "black",    6,  1)
    s.put(ox+32, oy+14, "white",    6,  4)
    s.put(ox+34, oy+14, "stone_dark",2, 4)
    s.put(ox+34, oy+15, "black",    1,  2)
    s.put(ox+32, oy+17, SKIND,      6,  1)
    s.put(ox+24, oy+14, SKIND,      2,  4)

    s.put(ox+29, oy+18, SKIND,  4,  4)
    s.put(ox+28, oy+20, SKIND,  6,  2)
    s.put(ox+28, oy+18, SKINL,  2,  2)
    s.put(ox+25, oy+22, SKIN,   8,  2)
    s.put(ox+26, oy+22, "brick_light", 5, 1)  # warm pink lips
    s.put(ox+25, oy+24, SKIN,   8,  2)
    s.put(ox+26, oy+24, SKINL,  4,  1)

    s.put(ox+40, oy+13, SKIN,  2,  6)
    s.put(ox+40, oy+15, SKIND, 2,  3)
    s.put(ox+26, oy+24, SKIN, 10,  8)   # neck extended from oy+24 to close face-neck gap
    s.put(ox+34, oy+24, SKIND, 4,  7)   # neck shadow

    # ── teal tunic ────────────────────────────────────────────────────────────
    s.put(ox+14, oy+32, "de_lijn_blue", 34, 48)
    s.put(ox+12, oy+32, "night",         2, 48)
    s.put(ox+48, oy+32, "night",         2, 48)
    s.put(ox+14, oy+32, "sky_pale",      8,  2)
    s.put(ox+14, oy+34, "sky_pale",      2, 20)
    s.put(ox+46, oy+34, "night",         2, 36)
    # Embroidery at neckline (gold arc pattern)
    for ex in range(22, 40, 2):
        s.put(ox+ex, oy+34, "gold",  2,  2)
    s.put(ox+22, oy+36, "ochre",    18,  2)  # embroidery band
    # Tunic side seam / split detail
    s.put(ox+32, oy+52, "night",    2, 24)
    # Tunic fold lines
    s.put(ox+22, oy+56, "sky_pale", 6, 20)
    s.put(ox+38, oy+52, "night",    4, 22)

    # ── sleeves ───────────────────────────────────────────────────────────────
    s.put(ox+10, oy+34, "de_lijn_blue", 4, 26)
    s.put(ox+ 8, oy+34, "night",        2, 26)
    s.put(ox+10, oy+34, "sky_pale",     2,  2)
    s.put(ox+48, oy+34, "de_lijn_blue", 4, 26)
    s.put(ox+52, oy+34, "night",        2, 26)

    # ── hands ─────────────────────────────────────────────────────────────────
    s.put(ox+10, oy+58, SKIN, 4, 6)
    s.put(ox+11, oy+58, SKINL,2, 2)
    s.put(ox+48, oy+58, SKIN, 4, 6)
    s.put(ox+49, oy+58, SKINL,2, 2)

    # ── wide-leg trousers ─────────────────────────────────────────────────────
    s.put(ox+16, oy+80, "stone_dark", 14, 12)
    s.put(ox+14, oy+80, "night",       2, 12)
    s.put(ox+28, oy+80, "night",       2, 12)
    s.put(ox+30, oy+80, "stone_dark", 14, 12)
    s.put(ox+44, oy+80, "night",       2, 12)

    # ── traditional shoes ─────────────────────────────────────────────────────
    lf = 2 if stride == 1 else 0
    rf = 2 if stride == 2 else 0
    s.put(ox+14, oy+90-lf, "wood_dark",  14,  6)
    s.put(ox+14, oy+90-lf, "wood_light",  6,  2)
    s.put(ox+30, oy+90+rf, "wood_dark",  14,  6)
    s.put(ox+30, oy+90+rf, "wood_light",  6,  2)


# ── registry & runner ─────────────────────────────────────────────────────────

NPCS = [
    ("fatima",  draw_fatima,  "Fatima — Moroccan woman 45, long coat + hijab + wicker bag"),
    ("omar",    draw_omar,    "Omar — Moroccan baker 38, white apron, bread"),
    ("baert",   draw_baert,   "Mevrouw Baert — Flemish woman 67, Stunt Solderie"),
    ("reza",    draw_reza,    "Reza — Afghan-Belgian 28, waistcoat + oud on back"),
    ("el_osri", draw_el_osri, "El Osri — District mayor 42, green blazer + tablet"),
    ("yusuf",   draw_yusuf,   "Yusuf — Delivery rider 30, orange vest + helmet"),
    ("aziz",    draw_aziz,    "Aziz — Elderly Moroccan 72, grey djellaba + stick + tasbih"),
    ("sofia",   draw_sofia,   "Sofia — Flemish art student 24, olive jacket + tote"),
    ("hamza",   draw_hamza,   "Hamza — Moroccan-Belgian teen 14, blue tracksuit + phone"),
    ("tine",    draw_tine,    "Tine — Turkish-Belgian 50, teal tunic + embroidery"),
]


def generate_npc(npc_id, draw_fn, label):
    print(f"\n● {label}")
    sheet = make_sheet(label)
    for frame in range(NUM_FRAMES):
        draw_fn(sheet, FW * frame, 0, frame=frame)
    save(sheet, npc_id)


def main():
    print("=" * 60)
    print("Turnhoutsebaan NPC Sprite Generator  (detailed redraw)")
    print(f"  Frame: {FW}×{FH} game px  |  out_scale={OUT_SCALE}")
    print(f"  PNG per NPC: {FW*OUT_SCALE*NUM_FRAMES}×{FH*OUT_SCALE} px")
    print("=" * 60)
    for npc_id, draw_fn, label in NPCS:
        generate_npc(npc_id, draw_fn, label)
    print(f"\n✓ All NPCs generated → {BASE_DIR}")


if __name__ == "__main__":
    main()
