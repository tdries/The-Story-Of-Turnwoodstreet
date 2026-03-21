#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — Crowd Sprite Sheet
=========================================
20 pedestrian silhouettes representing Borgerhout's multicultural street life.
Each person has 3 animation frames: idle, walk_A, walk_B.

Frame layout: 12×28 game pixels per frame, SCALE=6 → 72×168 px per frame
3 frames per person → 216×168 px per person strip
20 persons → horizontal sheet: 4320×168 px

Run: python3 generate_crowd.py
"""

import os
from PIL import Image, ImageDraw

# ── Config ────────────────────────────────────────────────────────────────────
SCALE       = 6          # px per game pixel
GW, GH      = 12, 28     # game frame size
FW          = GW * SCALE  # 72 px
FH          = GH * SCALE  # 168 px
NUM_FRAMES  = 3
NUM_PERSONS = 20

BASE_DIR    = os.path.join(os.path.dirname(__file__), "..", "assets", "Sprites", "characters", "crowd")

# ── Palette ───────────────────────────────────────────────────────────────────
SKIN_LIGHT  = (0xF4, 0xD0, 0xA8, 255)
SKIN_MED    = (0xD4, 0x9C, 0x6C, 255)
SKIN_DARK   = (0x88, 0x54, 0x2C, 255)
SKIN_DEEP   = (0x44, 0x28, 0x14, 255)
HAIR_BLK    = (0x18, 0x10, 0x08, 255)
HAIR_BRN    = (0x48, 0x28, 0x10, 255)
HAIR_GRY    = (0x88, 0x84, 0x80, 255)
WHITE       = (0xF0, 0xEE, 0xE8, 255)
BLACK_C     = (0x14, 0x12, 0x10, 255)
HIJAB_TL    = (0x18, 0x80, 0x80, 255)
HIJAB_BK    = (0x18, 0x10, 0x28, 255)
HIJAB_WH    = (0xE8, 0xE4, 0xD8, 255)
DJELL_BG    = (0xD8, 0xD0, 0xB8, 255)
DJELL_WH    = (0xF0, 0xEE, 0xE8, 255)
JACKET_BK   = (0x20, 0x1C, 0x18, 255)
JACKET_BL   = (0x24, 0x44, 0x6C, 255)
JACKET_GN   = (0x28, 0x50, 0x30, 255)
TRACK_BL    = (0x1C, 0x58, 0x98, 255)
TRACK_GR    = (0x30, 0x30, 0x30, 255)
COAT_BK     = (0x18, 0x14, 0x10, 255)
COAT_BN     = (0x6C, 0x44, 0x28, 255)
JEANS       = (0x2C, 0x44, 0x6C, 255)
JEANS_BK    = (0x18, 0x18, 0x20, 255)
TROUSERS_G  = (0x48, 0x48, 0x44, 255)
SHIRT_WH    = (0xEC, 0xE8, 0xE0, 255)
SHIRT_BL    = (0x28, 0x5C, 0xA0, 255)
VEST_OR     = (0xD4, 0x6C, 0x14, 255)
SHOES_BK    = (0x20, 0x18, 0x10, 255)
SHOES_WH    = (0xE0, 0xDC, 0xD4, 255)
BAG_BN      = (0x78, 0x4C, 0x28, 255)
CHILD_RED   = (0xCC, 0x20, 0x10, 255)
GOLD        = (0xFF, 0xD7, 0x00, 255)
SHADOW_C    = (0x10, 0x0C, 0x08, 180)
HELM_GR     = (0x60, 0x60, 0x58, 255)
HELM_YL     = (0xE8, 0xCC, 0x00, 255)
KUFI_WH     = (0xEC, 0xEA, 0xE0, 255)
APRON_WH    = (0xE8, 0xE4, 0xDC, 255)
HAT_DK      = (0x28, 0x20, 0x18, 255)
SKIN_LIGHT_SHD = (0xD8, 0xAC, 0x84, 255)
SKIN_MED_SHD   = (0xA8, 0x70, 0x44, 255)
SKIN_DARK_SHD  = (0x60, 0x38, 0x18, 255)
TRANSPARENT = (0, 0, 0, 0)


# ── Drawing helper ────────────────────────────────────────────────────────────
def px(d, gx, gy, gw, gh, color):
    """Draw a rectangle in game-pixel coordinates."""
    x1 = gx * SCALE
    y1 = gy * SCALE
    x2 = (gx + gw) * SCALE - 1
    y2 = (gy + gh) * SCALE - 1
    d.rectangle([x1, y1, x2, y2], fill=color)


def make_frame():
    return Image.new('RGBA', (FW, FH), (0, 0, 0, 0))


# ── Person drawing functions ──────────────────────────────────────────────────
# All figures are drawn in game-pixel space (0..11 x, 0..27 y).
# Head top at y=0, feet bottom at y=27.
# Frame 0 = idle, Frame 1 = walk_A, Frame 2 = walk_B

def draw_fatima_crowd(d, frame):
    """0. fatima_crowd — medium skin, teal hijab, long dark coat, dark jeans"""
    # Legs / animation
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
    else:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 21, 19

    # Teal hijab (covers head completely)
    px(d, 3, 0, 6, 1, HIJAB_TL)
    px(d, 2, 1, 8, 3, HIJAB_TL)
    px(d, 2, 4, 2, 2, HIJAB_TL)
    px(d, 8, 4, 2, 2, HIJAB_TL)
    # Face
    px(d, 4, 1, 4, 4, SKIN_MED)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 6, 2, 1, 1, BLACK_C)
    # Hijab shadow under chin
    px(d, 3, 5, 6, 1, (0x10, 0x60, 0x60, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_MED)
    # Long dark coat body
    px(d, 3, 6, 6, 14, COAT_BK)
    # Coat shadow right edge
    px(d, 8, 6, 1, 14, (0x10, 0x0C, 0x08, 255))
    # Left arm (upper)
    px(d, 2, 7, 1, 4, COAT_BK)
    # Left forearm
    px(d, 2, 11, 1, 3, COAT_BK)
    # Right arm upper
    px(d, 9, 7, 1, 4, COAT_BK)
    # Right forearm
    if frame == 1:
        px(d, 10, 10, 1, 3, COAT_BK)
    elif frame == 2:
        px(d, 9, 10, 1, 3, COAT_BK)
    else:
        px(d, 9, 11, 1, 3, COAT_BK)
    # Hands (skin)
    px(d, 2, 14, 1, 1, SKIN_MED)
    px(d, 9, 14, 1, 1, SKIN_MED)
    # Coat button seam
    px(d, 6, 7, 1, 12, (0x30, 0x28, 0x20, 255))
    # Dark jeans legs
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    # Jeans shadow on right
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_moroccan_man(d, frame):
    """1. moroccan_man — dark skin, white kufi cap, beige djellaba"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 21, 21
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 20, 22
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 22, 20

    # White kufi cap
    px(d, 3, 0, 6, 2, KUFI_WH)
    px(d, 2, 2, 8, 2, KUFI_WH)
    # Cap highlight
    px(d, 3, 0, 2, 1, (0xFF, 0xFF, 0xF8, 255))
    # Face (dark skin)
    px(d, 3, 2, 6, 4, SKIN_DARK)
    px(d, 2, 3, 1, 2, SKIN_DARK)
    px(d, 9, 3, 1, 2, SKIN_DARK)
    # Eyes
    px(d, 4, 3, 1, 1, BLACK_C)
    px(d, 7, 3, 1, 1, BLACK_C)
    # Nose hint
    px(d, 6, 4, 1, 1, SKIN_DARK_SHD)
    # Mouth
    px(d, 5, 5, 2, 1, (0x30, 0x18, 0x10, 255))
    # Neck
    px(d, 5, 6, 2, 1, SKIN_DARK)
    # Beige djellaba (wide, flowing)
    px(d, 2, 7, 8, 14, DJELL_BG)
    # Djellaba shadow
    px(d, 2, 7, 1, 14, (0xA0, 0x98, 0x80, 255))
    px(d, 9, 7, 1, 14, (0xA0, 0x98, 0x80, 255))
    # Djellaba highlight
    px(d, 3, 7, 2, 1, (0xE8, 0xE0, 0xC8, 255))
    # Djellaba fold lines
    px(d, 6, 9, 1, 10, (0xC0, 0xB8, 0xA0, 255))
    # Djellaba hood drape visible at neck
    px(d, 4, 7, 4, 2, DJELL_WH)
    # Left arm sleeve
    px(d, 1, 8, 2, 6, DJELL_BG)
    # Right arm sleeve
    px(d, 9, 8, 2, 6, DJELL_BG)
    # Hands
    px(d, 1, 13, 1, 2, SKIN_DARK)
    px(d, 10, 13, 1, 2, SKIN_DARK)
    # Legs below djellaba
    px(d, ll_x, ll_y, 2, 6, DJELL_BG)
    px(d, rl_x, rl_y, 2, 6, DJELL_BG)
    # Shoes (dark, peek below djellaba)
    px(d, ll_x, 26, 3, 2, SHOES_BK)
    px(d, rl_x, 26, 3, 2, SHOES_BK)


def draw_teen_boy(d, frame):
    """2. teen_boy — medium skin, black hair, blue tracksuit, white sneakers"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Hair (black, short)
    px(d, 3, 0, 6, 2, HAIR_BLK)
    px(d, 2, 2, 8, 1, HAIR_BLK)
    # Face
    px(d, 3, 1, 6, 4, SKIN_MED)
    px(d, 2, 2, 1, 2, SKIN_MED)
    px(d, 9, 2, 1, 2, SKIN_MED)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Nose
    px(d, 6, 3, 1, 1, SKIN_MED_SHD)
    # Mouth
    px(d, 5, 4, 2, 1, (0xA0, 0x68, 0x44, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_MED)
    # Tracksuit jacket (blue)
    px(d, 3, 6, 6, 8, TRACK_BL)
    # Jacket shadow
    px(d, 8, 6, 1, 8, (0x14, 0x40, 0x70, 255))
    # Jacket highlight
    px(d, 3, 6, 2, 1, (0x30, 0x6C, 0xB0, 255))
    # Zipper line
    px(d, 6, 6, 1, 8, (0x14, 0x40, 0x78, 255))
    # Side stripes (white)
    px(d, 3, 7, 1, 6, WHITE)
    px(d, 9, 7, 1, 6, WHITE)
    # Left arm (upper)
    px(d, 2, 6, 1, 4, TRACK_BL)
    px(d, 1, 10, 1, 3, TRACK_BL)  # forearm
    # Right arm
    px(d, 10, 6, 1, 4, TRACK_BL)
    px(d, 10, la_y-2, 1, 3, TRACK_BL)  # forearm moves with walk
    # Hands
    px(d, 1, 13, 1, 1, SKIN_MED)
    px(d, 10, ra_y+1, 1, 1, SKIN_MED)
    # Tracksuit pants (blue with white stripe)
    px(d, ll_x, ll_y, 2, 7, TRACK_BL)
    px(d, rl_x, rl_y, 2, 7, TRACK_BL)
    px(d, ll_x, ll_y+1, 1, 5, WHITE)
    px(d, rl_x, rl_y+1, 1, 5, WHITE)
    # Pants shadow
    px(d, ll_x+1, ll_y, 1, 7, (0x14, 0x40, 0x70, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x14, 0x40, 0x70, 255))
    # White sneakers
    px(d, ll_x-1, 26, 3, 2, SHOES_WH)
    px(d, rl_x-1, 26, 3, 2, SHOES_WH)
    # Sneaker stripe (blue)
    px(d, ll_x, 26, 1, 1, TRACK_BL)
    px(d, rl_x, 26, 1, 1, TRACK_BL)


def draw_elderly_man(d, frame):
    """3. elderly_man — light skin, grey hair, dark jacket, grey trousers, walking stick"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 19, 19
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 18, 20
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 20, 18

    # Grey hair (receding, sides only)
    px(d, 3, 0, 6, 1, HAIR_GRY)
    px(d, 2, 1, 2, 3, HAIR_GRY)
    px(d, 8, 1, 2, 3, HAIR_GRY)
    # Face (light, older)
    px(d, 3, 1, 6, 4, SKIN_LIGHT)
    px(d, 2, 2, 1, 2, SKIN_LIGHT)
    px(d, 9, 2, 1, 2, SKIN_LIGHT)
    # Eyes (slightly droopy)
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Grey eyebrows
    px(d, 4, 1, 2, 1, HAIR_GRY)
    px(d, 7, 1, 2, 1, HAIR_GRY)
    # Wrinkle lines (darker skin tone)
    px(d, 3, 3, 1, 1, SKIN_LIGHT_SHD)
    px(d, 9, 3, 1, 1, SKIN_LIGHT_SHD)
    # Mouth (thin)
    px(d, 5, 4, 2, 1, (0xCC, 0x98, 0x78, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_LIGHT)
    # Dark jacket
    px(d, 3, 6, 6, 9, JACKET_BK)
    # Jacket shadow right
    px(d, 8, 6, 1, 9, (0x10, 0x0C, 0x08, 255))
    # Jacket highlight left
    px(d, 3, 6, 1, 9, (0x30, 0x2C, 0x28, 255))
    # Lapel
    px(d, 5, 6, 2, 3, (0x18, 0x14, 0x10, 255))
    # White shirt collar
    px(d, 5, 6, 2, 1, SHIRT_WH)
    # Left arm (held close, elderly posture)
    px(d, 2, 7, 1, 4, JACKET_BK)
    px(d, 1, 11, 1, 3, JACKET_BK)
    # Right arm (holding stick)
    px(d, 9, 7, 1, 4, JACKET_BK)
    px(d, 9, 11, 1, 3, JACKET_BK)
    # Hands
    px(d, 1, 14, 1, 1, SKIN_LIGHT)
    px(d, 9, 14, 1, 1, SKIN_LIGHT)
    # Walking stick (1px rod from right hand down)
    px(d, 9, 14, 1, 13, HAIR_BRN)
    px(d, 8, 14, 1, 1, (0x70, 0x50, 0x30, 255))  # stick handle
    # Grey trousers
    px(d, ll_x, ll_y, 2, 8, TROUSERS_G)
    px(d, rl_x, rl_y, 2, 8, TROUSERS_G)
    px(d, ll_x+1, ll_y, 1, 8, (0x38, 0x38, 0x34, 255))
    px(d, rl_x+1, rl_y, 1, 8, (0x38, 0x38, 0x34, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_hijab_woman_b(d, frame):
    """4. hijab_woman_b — dark skin, dark purple hijab, black coat, black jeans"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19

    # Dark purple hijab
    px(d, 2, 0, 8, 2, HIJAB_BK)
    px(d, 1, 2, 10, 3, HIJAB_BK)
    px(d, 1, 5, 2, 2, HIJAB_BK)
    px(d, 9, 5, 2, 2, HIJAB_BK)
    # Hijab highlight
    px(d, 2, 0, 3, 1, (0x30, 0x20, 0x40, 255))
    # Face (dark skin)
    px(d, 3, 2, 6, 4, SKIN_DARK)
    px(d, 2, 3, 1, 2, SKIN_DARK)
    px(d, 9, 3, 1, 2, SKIN_DARK)
    # Eyes
    px(d, 4, 3, 1, 1, BLACK_C)
    px(d, 7, 3, 1, 1, BLACK_C)
    # Nose
    px(d, 6, 4, 1, 1, SKIN_DARK_SHD)
    # Mouth
    px(d, 5, 5, 2, 1, (0x60, 0x38, 0x20, 255))
    # Neck
    px(d, 5, 6, 2, 1, SKIN_DARK)
    # Black coat body
    px(d, 3, 7, 6, 13, COAT_BK)
    px(d, 9, 7, 1, 13, (0x10, 0x0C, 0x08, 255))
    # Coat highlight
    px(d, 3, 7, 1, 13, (0x28, 0x24, 0x20, 255))
    # Button seam
    px(d, 6, 8, 1, 11, (0x14, 0x10, 0x0C, 255))
    # Coat collar / hijab drape onto coat
    px(d, 3, 7, 6, 2, HIJAB_BK)
    # Left arm
    px(d, 2, 8, 1, 4, COAT_BK)
    px(d, 1, 12, 1, 3, COAT_BK)
    # Right arm
    px(d, 9, 8, 1, 4, COAT_BK)
    if frame == 1:
        px(d, 10, 11, 1, 3, COAT_BK)
    elif frame == 2:
        px(d, 9, 11, 1, 3, COAT_BK)
    else:
        px(d, 9, 12, 1, 3, COAT_BK)
    # Hands
    px(d, 1, 15, 1, 1, SKIN_DARK)
    px(d, 9, 15, 1, 1, SKIN_DARK)
    # Black jeans
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_business_man(d, frame):
    """5. business_man — light skin, brown hair, dark blue jacket, grey trousers, briefcase"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 19, 19
        la_y, ra_y = 13, 13
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 18, 20
        la_y, ra_y = 14, 12
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 20, 18
        la_y, ra_y = 12, 14

    # Hair (brown, neat, parted)
    px(d, 3, 0, 6, 2, HAIR_BRN)
    px(d, 2, 2, 8, 1, HAIR_BRN)
    # Hair part line
    px(d, 6, 0, 1, 2, (0x38, 0x20, 0x0C, 255))
    # Face (light skin)
    px(d, 3, 1, 6, 4, SKIN_LIGHT)
    px(d, 2, 2, 1, 2, SKIN_LIGHT)
    px(d, 9, 2, 1, 2, SKIN_LIGHT)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Brows
    px(d, 4, 1, 2, 1, HAIR_BRN)
    px(d, 7, 1, 2, 1, HAIR_BRN)
    # Nose
    px(d, 6, 3, 1, 1, SKIN_LIGHT_SHD)
    # Mouth
    px(d, 5, 4, 2, 1, (0xCC, 0x98, 0x78, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_LIGHT)
    # Dark blue jacket
    px(d, 3, 6, 6, 9, JACKET_BL)
    px(d, 8, 6, 1, 9, (0x18, 0x30, 0x50, 255))
    px(d, 3, 6, 1, 9, (0x30, 0x50, 0x80, 255))
    # Lapels
    px(d, 5, 6, 2, 3, (0x1C, 0x38, 0x5C, 255))
    # White shirt collar / tie
    px(d, 5, 6, 2, 1, SHIRT_WH)
    px(d, 6, 7, 1, 4, (0x80, 0x20, 0x10, 255))  # red tie
    # Left arm
    px(d, 2, 7, 1, 4, JACKET_BL)
    px(d, 2, 11, 1, 3, JACKET_BL)
    # Right arm (briefcase side)
    px(d, 9, 7, 1, 4, JACKET_BL)
    px(d, 9, 11, 1, 3, JACKET_BL)
    # Hands
    px(d, 2, 14, 1, 1, SKIN_LIGHT)
    # Briefcase (right hand)
    px(d, 9, la_y, 3, 4, (0x50, 0x38, 0x20, 255))
    px(d, 9, la_y, 3, 1, (0x70, 0x50, 0x30, 255))  # top edge
    px(d, 10, la_y-1, 1, 1, (0x70, 0x50, 0x30, 255))  # handle
    px(d, 9, la_y+2, 3, 1, (0x40, 0x2C, 0x18, 255))  # latch line
    # Grey trousers
    px(d, ll_x, ll_y, 2, 8, TROUSERS_G)
    px(d, rl_x, rl_y, 2, 8, TROUSERS_G)
    px(d, ll_x+1, ll_y, 1, 8, (0x38, 0x38, 0x34, 255))
    px(d, rl_x+1, rl_y, 1, 8, (0x38, 0x38, 0x34, 255))
    # Crease line on trousers
    px(d, ll_x, ll_y+2, 1, 4, (0x54, 0x54, 0x50, 255))
    # Shoes (dark leather, polished)
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)
    px(d, ll_x-1, 26, 1, 1, (0x38, 0x30, 0x28, 255))  # shine


def draw_kid_short(d, frame):
    """6. kid_short — medium skin, black hair, red coat, dark jeans (shorter figure)"""
    # Offset downward by 4 px to simulate shorter child
    oy = 4
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19

    # Hair (black, messy)
    px(d, 4, oy+0, 4, 2, HAIR_BLK)
    px(d, 3, oy+2, 6, 1, HAIR_BLK)
    # Face
    px(d, 4, oy+1, 4, 4, SKIN_MED)
    px(d, 3, oy+2, 1, 2, SKIN_MED)
    px(d, 8, oy+2, 1, 2, SKIN_MED)
    # Eyes (bigger, child-like)
    px(d, 4, oy+2, 1, 1, BLACK_C)
    px(d, 7, oy+2, 1, 1, BLACK_C)
    # Nose (small dot)
    px(d, 5, oy+3, 1, 1, SKIN_MED_SHD)
    # Mouth (slight smile)
    px(d, 5, oy+4, 2, 1, (0xA0, 0x68, 0x44, 255))
    # Neck
    px(d, 5, oy+5, 2, 1, SKIN_MED)
    # Red coat (short, childish)
    px(d, 3, oy+6, 6, 8, CHILD_RED)
    px(d, 8, oy+6, 1, 8, (0xA0, 0x18, 0x08, 255))
    px(d, 3, oy+6, 1, 8, (0xE0, 0x30, 0x18, 255))
    # Hood detail on collar
    px(d, 4, oy+6, 4, 1, (0xDD, 0x28, 0x18, 255))
    # Coat buttons
    px(d, 6, oy+7, 1, 1, WHITE)
    px(d, 6, oy+9, 1, 1, WHITE)
    # Left arm
    px(d, 2, oy+6, 1, 3, CHILD_RED)
    px(d, 2, oy+9, 1, 2, CHILD_RED)
    # Right arm
    px(d, 9, oy+6, 1, 3, CHILD_RED)
    px(d, 9, oy+9, 1, 2, CHILD_RED)
    # Hands
    px(d, 2, oy+11, 1, 1, SKIN_MED)
    px(d, 9, oy+11, 1, 1, SKIN_MED)
    # Dark jeans
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Shoes (small, rounded)
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_young_woman(d, frame):
    """7. young_woman — medium skin, brown hair, green jacket, blue jeans, tote bag"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19

    # Brown hair (medium length, flows past shoulders)
    px(d, 3, 0, 6, 2, HAIR_BRN)
    px(d, 2, 2, 8, 3, HAIR_BRN)
    px(d, 2, 5, 1, 4, HAIR_BRN)
    px(d, 9, 5, 1, 4, HAIR_BRN)
    # Face (medium skin)
    px(d, 3, 1, 6, 4, SKIN_MED)
    px(d, 2, 2, 1, 2, SKIN_MED)
    px(d, 9, 2, 1, 2, SKIN_MED)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Brows
    px(d, 4, 1, 2, 1, HAIR_BRN)
    px(d, 7, 1, 2, 1, HAIR_BRN)
    # Nose
    px(d, 6, 3, 1, 1, SKIN_MED_SHD)
    # Lips
    px(d, 5, 4, 2, 1, (0xC0, 0x60, 0x50, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_MED)
    # Green jacket
    px(d, 3, 6, 6, 9, JACKET_GN)
    px(d, 8, 6, 1, 9, (0x1C, 0x38, 0x20, 255))
    px(d, 3, 6, 1, 9, (0x34, 0x60, 0x3C, 255))
    # Jacket collar open
    px(d, 5, 6, 2, 2, (0x20, 0x48, 0x28, 255))
    # Shirt under jacket
    px(d, 5, 7, 2, 2, (0xE8, 0xD8, 0xC0, 255))
    # Left arm (with tote bag strap)
    px(d, 2, 7, 1, 4, JACKET_GN)
    px(d, 1, 11, 1, 3, JACKET_GN)
    # Right arm
    px(d, 9, 7, 1, 4, JACKET_GN)
    if frame == 1:
        px(d, 10, 10, 1, 3, JACKET_GN)
    elif frame == 2:
        px(d, 9, 10, 1, 3, JACKET_GN)
    else:
        px(d, 9, 11, 1, 3, JACKET_GN)
    # Hands
    px(d, 1, 14, 1, 1, SKIN_MED)
    px(d, 9, 14, 1, 1, SKIN_MED)
    # Tote bag (hanging at left hip)
    px(d, 1, 13, 2, 5, BAG_BN)
    px(d, 1, 13, 1, 5, (0x58, 0x34, 0x18, 255))  # bag shadow
    px(d, 1, 13, 2, 1, (0x90, 0x60, 0x38, 255))  # top edge
    # Bag strap over shoulder
    px(d, 3, 7, 1, 6, (0x90, 0x60, 0x38, 255))
    # Blue jeans
    px(d, ll_x, ll_y, 2, 7, JEANS)
    px(d, rl_x, rl_y, 2, 7, JEANS)
    px(d, ll_x+1, ll_y, 1, 7, (0x20, 0x34, 0x58, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x20, 0x34, 0x58, 255))
    # Jeans pocket stitching hint
    px(d, ll_x, ll_y+2, 1, 1, (0x40, 0x60, 0x90, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_delivery_man(d, frame):
    """8. delivery_man — dark skin, helmet (grey dome), orange vest, dark jeans"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Grey helmet dome
    px(d, 2, 0, 8, 3, HELM_GR)
    px(d, 1, 3, 10, 2, HELM_GR)
    # Helmet highlight
    px(d, 2, 0, 3, 1, (0x80, 0x80, 0x78, 255))
    # Helmet visor strip
    px(d, 1, 5, 10, 1, (0x30, 0x30, 0x28, 255))
    # Face (dark skin below visor)
    px(d, 3, 5, 6, 3, SKIN_DARK)
    px(d, 2, 6, 1, 1, SKIN_DARK)
    px(d, 9, 6, 1, 1, SKIN_DARK)
    # Eyes
    px(d, 4, 6, 1, 1, BLACK_C)
    px(d, 7, 6, 1, 1, BLACK_C)
    # Chin strap
    px(d, 2, 7, 1, 1, HELM_GR)
    px(d, 9, 7, 1, 1, HELM_GR)
    # Neck
    px(d, 5, 8, 2, 1, SKIN_DARK)
    # Orange safety vest
    px(d, 3, 9, 6, 8, VEST_OR)
    px(d, 8, 9, 1, 8, (0xA0, 0x50, 0x08, 255))
    px(d, 3, 9, 1, 8, (0xE0, 0x80, 0x20, 255))
    # Reflective strips
    px(d, 3, 12, 6, 1, (0xF0, 0xEC, 0xE0, 255))
    px(d, 3, 15, 6, 1, (0xF0, 0xEC, 0xE0, 255))
    # Vest zipper
    px(d, 6, 9, 1, 7, (0xB0, 0x58, 0x10, 255))
    # Left arm
    px(d, 2, 9, 1, 4, VEST_OR)
    px(d, 1, 13, 1, 3, (0x1C, 0x14, 0x10, 255))  # dark glove
    # Right arm
    px(d, 9, 9, 1, 4, VEST_OR)
    px(d, 9, ra_y, 1, 3, (0x1C, 0x14, 0x10, 255))
    # Dark delivery backpack (visible on left side)
    px(d, 1, 9, 2, 8, (0x20, 0x20, 0x18, 255))
    px(d, 1, 9, 2, 1, (0x38, 0x38, 0x30, 255))
    # Jeans
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Boots (dark, heavy)
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_elderly_woman(d, frame):
    """9. elderly_woman — light skin, grey hair, white hijab, brown coat"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 21, 21
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 20, 22
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 22, 20

    # White hijab (with grey hair visible at edges)
    px(d, 2, 0, 8, 2, HIJAB_WH)
    px(d, 1, 2, 10, 3, HIJAB_WH)
    px(d, 1, 5, 2, 3, HIJAB_WH)
    px(d, 9, 5, 2, 3, HIJAB_WH)
    # Grey hair peeking out at forehead
    px(d, 3, 1, 6, 1, HAIR_GRY)
    # Hijab highlight
    px(d, 2, 0, 3, 1, (0xFF, 0xFF, 0xFF, 255))
    # Face (light, older)
    px(d, 3, 2, 6, 4, SKIN_LIGHT)
    px(d, 2, 3, 1, 2, SKIN_LIGHT)
    px(d, 9, 3, 1, 2, SKIN_LIGHT)
    # Eyes (slightly squinting)
    px(d, 4, 3, 1, 1, BLACK_C)
    px(d, 7, 3, 1, 1, BLACK_C)
    # Wrinkles
    px(d, 3, 4, 1, 1, SKIN_LIGHT_SHD)
    px(d, 9, 4, 1, 1, SKIN_LIGHT_SHD)
    # Mouth
    px(d, 5, 5, 2, 1, (0xCC, 0x98, 0x78, 255))
    # Hijab under chin
    px(d, 4, 6, 4, 1, HIJAB_WH)
    # Neck area under hijab
    px(d, 5, 6, 2, 1, SKIN_LIGHT)
    # Brown coat (wide, older woman)
    px(d, 2, 7, 8, 14, COAT_BN)
    px(d, 9, 7, 1, 14, (0x50, 0x30, 0x18, 255))
    px(d, 2, 7, 1, 14, (0x80, 0x58, 0x34, 255))
    # Coat highlight top
    px(d, 3, 7, 3, 1, (0x80, 0x58, 0x38, 255))
    # Coat button
    px(d, 6, 10, 1, 1, (0x40, 0x28, 0x10, 255))
    px(d, 6, 13, 1, 1, (0x40, 0x28, 0x10, 255))
    # Left arm (wide sleeve)
    px(d, 1, 8, 2, 6, COAT_BN)
    # Right arm
    px(d, 9, 8, 2, 6, COAT_BN)
    # Hands
    px(d, 1, 14, 1, 1, SKIN_LIGHT)
    px(d, 10, 14, 1, 1, SKIN_LIGHT)
    # Legs (hidden by coat)
    px(d, ll_x, ll_y, 2, 6, COAT_BN)
    px(d, rl_x, rl_y, 2, 6, COAT_BN)
    # Shoes (flat, dark)
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_white_hijab(d, frame):
    """10. white_hijab — light skin, white hijab, dark coat"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19

    # White hijab
    px(d, 3, 0, 6, 1, HIJAB_WH)
    px(d, 2, 1, 8, 3, HIJAB_WH)
    px(d, 1, 4, 2, 3, HIJAB_WH)
    px(d, 9, 4, 2, 3, HIJAB_WH)
    # Hijab drape onto shoulders
    px(d, 2, 7, 8, 2, HIJAB_WH)
    # Hijab shine/highlight
    px(d, 3, 0, 3, 1, (0xFF, 0xFF, 0xFF, 255))
    # Hijab shadow
    px(d, 2, 6, 8, 1, (0xC8, 0xC4, 0xBC, 255))
    # Face (light skin)
    px(d, 3, 2, 6, 4, SKIN_LIGHT)
    px(d, 2, 3, 1, 2, SKIN_LIGHT)
    px(d, 9, 3, 1, 2, SKIN_LIGHT)
    # Eyes
    px(d, 4, 3, 1, 1, BLACK_C)
    px(d, 7, 3, 1, 1, BLACK_C)
    # Nose
    px(d, 6, 4, 1, 1, SKIN_LIGHT_SHD)
    # Mouth
    px(d, 5, 5, 2, 1, (0xCC, 0x98, 0x78, 255))
    # Dark coat
    px(d, 3, 9, 6, 11, COAT_BK)
    px(d, 8, 9, 1, 11, (0x10, 0x0C, 0x08, 255))
    px(d, 3, 9, 1, 11, (0x28, 0x24, 0x20, 255))
    # Button seam
    px(d, 6, 10, 1, 9, (0x14, 0x10, 0x0C, 255))
    # Button detail
    px(d, 6, 10, 1, 1, (0x40, 0x38, 0x30, 255))
    px(d, 6, 13, 1, 1, (0x40, 0x38, 0x30, 255))
    # Left arm
    px(d, 2, 9, 1, 4, COAT_BK)
    px(d, 1, 13, 1, 3, COAT_BK)
    # Right arm
    px(d, 9, 9, 1, 4, COAT_BK)
    if frame == 1:
        px(d, 10, 12, 1, 3, COAT_BK)
    elif frame == 2:
        px(d, 9, 12, 1, 3, COAT_BK)
    else:
        px(d, 9, 13, 1, 3, COAT_BK)
    # Hands
    px(d, 1, 16, 1, 1, SKIN_LIGHT)
    px(d, 9, 16, 1, 1, SKIN_LIGHT)
    # Dark jeans
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_teen_girl(d, frame):
    """11. teen_girl — medium skin, black hair ponytail, grey tracksuit, black jeans"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Black hair with ponytail
    px(d, 3, 0, 6, 2, HAIR_BLK)
    px(d, 2, 2, 8, 2, HAIR_BLK)
    # Ponytail (sticks up/back)
    px(d, 8, 0, 2, 4, HAIR_BLK)
    px(d, 9, 4, 1, 3, HAIR_BLK)
    # Ponytail tie
    px(d, 8, 3, 2, 1, (0xCC, 0x20, 0x10, 255))
    # Face
    px(d, 3, 1, 6, 4, SKIN_MED)
    px(d, 2, 2, 1, 2, SKIN_MED)
    px(d, 9, 2, 1, 1, SKIN_MED)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Eyelashes hint
    px(d, 4, 1, 2, 1, HAIR_BLK)
    px(d, 7, 1, 2, 1, HAIR_BLK)
    # Mouth
    px(d, 5, 4, 2, 1, (0xA0, 0x68, 0x44, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_MED)
    # Grey tracksuit jacket
    px(d, 3, 6, 6, 8, TRACK_GR)
    px(d, 8, 6, 1, 8, (0x20, 0x20, 0x20, 255))
    px(d, 3, 6, 1, 8, (0x44, 0x44, 0x44, 255))
    # Hoodie hood detail at neck
    px(d, 4, 6, 4, 1, (0x40, 0x40, 0x40, 255))
    # Zipper
    px(d, 6, 7, 1, 6, (0x28, 0x28, 0x28, 255))
    # Kangaroo pocket
    px(d, 4, 10, 4, 3, (0x28, 0x28, 0x28, 255))
    px(d, 4, 10, 4, 1, (0x38, 0x38, 0x38, 255))
    # Left arm
    px(d, 2, 6, 1, 4, TRACK_GR)
    px(d, 1, la_y-2, 1, 3, TRACK_GR)
    # Right arm
    px(d, 9, 6, 1, 4, TRACK_GR)
    px(d, 9, ra_y-2, 1, 3, TRACK_GR)
    # Hands
    px(d, 1, la_y+1, 1, 1, SKIN_MED)
    px(d, 9, ra_y+1, 1, 1, SKIN_MED)
    # Black jeans
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Sneakers (white)
    px(d, ll_x-1, 26, 3, 2, SHOES_WH)
    px(d, rl_x-1, 26, 3, 2, SHOES_WH)
    px(d, ll_x, 26, 1, 1, TRACK_GR)


def draw_market_vendor(d, frame):
    """12. market_vendor — dark skin, white apron, dark shirt, dark trousers"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Hair (black, close-cropped)
    px(d, 3, 0, 6, 2, HAIR_BLK)
    px(d, 2, 2, 8, 1, HAIR_BLK)
    # Face (dark skin)
    px(d, 3, 1, 6, 4, SKIN_DARK)
    px(d, 2, 2, 1, 2, SKIN_DARK)
    px(d, 9, 2, 1, 2, SKIN_DARK)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Nose
    px(d, 6, 3, 1, 1, SKIN_DARK_SHD)
    # Mouth (smile — market vendor is cheery)
    px(d, 5, 4, 2, 1, (0x50, 0x28, 0x14, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_DARK)
    # Dark shirt
    px(d, 3, 6, 6, 9, (0x1C, 0x1C, 0x18, 255))
    px(d, 8, 6, 1, 9, (0x10, 0x10, 0x0C, 255))
    # White apron over shirt
    px(d, 4, 7, 4, 8, APRON_WH)
    px(d, 4, 7, 4, 1, (0xC8, 0xC4, 0xBC, 255))  # apron top edge shadow
    # Apron strings at waist
    px(d, 3, 12, 1, 1, (0xC8, 0xC4, 0xBC, 255))
    px(d, 8, 12, 1, 1, (0xC8, 0xC4, 0xBC, 255))
    # Pocket on apron
    px(d, 5, 10, 2, 3, (0xD8, 0xD4, 0xCC, 255))
    px(d, 5, 10, 2, 1, (0xC0, 0xBC, 0xB4, 255))
    # Left arm
    px(d, 2, 7, 1, 4, (0x1C, 0x1C, 0x18, 255))
    px(d, 1, la_y-2, 1, 3, (0x1C, 0x1C, 0x18, 255))
    # Right arm
    px(d, 9, 7, 1, 4, (0x1C, 0x1C, 0x18, 255))
    px(d, 9, ra_y-2, 1, 3, (0x1C, 0x1C, 0x18, 255))
    # Hands
    px(d, 1, la_y+1, 1, 2, SKIN_DARK)
    px(d, 9, ra_y+1, 1, 2, SKIN_DARK)
    # Dark trousers
    px(d, ll_x, ll_y, 2, 7, (0x20, 0x20, 0x1C, 255))
    px(d, rl_x, rl_y, 2, 7, (0x20, 0x20, 0x1C, 255))
    px(d, ll_x+1, ll_y, 1, 7, (0x14, 0x14, 0x10, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x14, 0x14, 0x10, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_kapper_man(d, frame):
    """13. kapper_man — medium skin, black hair, white shirt, black jeans"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Black hair (styled, slight quiff)
    px(d, 3, 0, 6, 2, HAIR_BLK)
    px(d, 2, 2, 8, 1, HAIR_BLK)
    px(d, 3, 0, 4, 1, (0x28, 0x18, 0x08, 255))  # quiff highlight
    # Face (medium skin)
    px(d, 3, 1, 6, 4, SKIN_MED)
    px(d, 2, 2, 1, 2, SKIN_MED)
    px(d, 9, 2, 1, 2, SKIN_MED)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Brows
    px(d, 4, 1, 2, 1, HAIR_BLK)
    px(d, 7, 1, 2, 1, HAIR_BLK)
    # Stubble
    px(d, 3, 4, 6, 1, SKIN_MED_SHD)
    px(d, 3, 3, 1, 2, SKIN_MED_SHD)
    px(d, 8, 3, 1, 2, SKIN_MED_SHD)
    # Mouth
    px(d, 5, 4, 2, 1, (0xA0, 0x68, 0x44, 255))
    # Neck
    px(d, 5, 5, 2, 2, SKIN_MED)
    # White shirt (neat, barber attire)
    px(d, 3, 7, 6, 8, SHIRT_WH)
    px(d, 8, 7, 1, 8, (0xC8, 0xC4, 0xBC, 255))
    px(d, 3, 7, 1, 8, (0xEC, 0xE8, 0xE0, 255))
    # Shirt collar
    px(d, 5, 7, 2, 2, (0xD8, 0xD4, 0xCC, 255))
    # Shirt buttons
    for by in range(8, 15, 2):
        px(d, 6, by, 1, 1, (0xA0, 0x9C, 0x94, 255))
    # Black belt
    px(d, 3, 15, 6, 1, HAIR_BLK)
    px(d, 6, 15, 1, 1, (0x50, 0x48, 0x40, 255))  # buckle
    # Left arm
    px(d, 2, 7, 1, 4, SHIRT_WH)
    px(d, 1, la_y-2, 1, 3, SKIN_MED)  # rolled sleeve
    # Right arm
    px(d, 9, 7, 1, 4, SHIRT_WH)
    px(d, 9, ra_y-2, 1, 3, SKIN_MED)
    # Hands
    px(d, 1, la_y+1, 1, 2, SKIN_MED)
    px(d, 9, ra_y+1, 1, 2, SKIN_MED)
    # Black jeans
    px(d, ll_x, ll_y, 2, 7, JEANS_BK)
    px(d, rl_x, rl_y, 2, 7, JEANS_BK)
    px(d, ll_x+1, ll_y, 1, 7, (0x10, 0x10, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x10, 0x10, 0x18, 255))
    # Shoes (white sneakers, clean — barber style)
    px(d, ll_x-1, 26, 3, 2, SHOES_WH)
    px(d, rl_x-1, 26, 3, 2, SHOES_WH)


def draw_student(d, frame):
    """14. student — light skin, brown hair, blue jacket, blue jeans, tote bag on back"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19

    # Brown hair (messy student hair)
    px(d, 3, 0, 6, 2, HAIR_BRN)
    px(d, 2, 2, 8, 2, HAIR_BRN)
    px(d, 2, 4, 1, 2, HAIR_BRN)
    # Messy texture
    px(d, 3, 0, 2, 1, (0x58, 0x34, 0x18, 255))
    px(d, 7, 0, 2, 1, (0x40, 0x24, 0x0C, 255))
    # Face (light skin)
    px(d, 3, 1, 6, 4, SKIN_LIGHT)
    px(d, 2, 2, 1, 2, SKIN_LIGHT)
    px(d, 9, 2, 1, 2, SKIN_LIGHT)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Glasses (thin frame)
    px(d, 3, 2, 3, 1, (0x50, 0x40, 0x30, 255))
    px(d, 7, 2, 3, 1, (0x50, 0x40, 0x30, 255))
    px(d, 6, 2, 1, 1, (0x50, 0x40, 0x30, 255))  # nose bridge
    # Brows
    px(d, 4, 1, 2, 1, HAIR_BRN)
    px(d, 7, 1, 2, 1, HAIR_BRN)
    # Mouth
    px(d, 5, 4, 2, 1, (0xCC, 0x98, 0x78, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_LIGHT)
    # Blue jacket (slightly oversized)
    px(d, 3, 6, 6, 9, JACKET_BL)
    px(d, 8, 6, 1, 9, (0x18, 0x30, 0x50, 255))
    px(d, 3, 6, 1, 9, (0x30, 0x50, 0x80, 255))
    # Open collar, hoodie underneath
    px(d, 5, 6, 2, 2, (0x1C, 0x38, 0x5C, 255))
    px(d, 5, 7, 2, 1, (0x60, 0x60, 0x58, 255))  # inner hoodie
    # Backpack visible on left side (canvas, tote)
    px(d, 1, 7, 2, 8, (0x60, 0x78, 0x50, 255))  # green tote/backpack
    px(d, 1, 7, 2, 1, (0x78, 0x90, 0x60, 255))  # top edge
    px(d, 1, 7, 1, 8, (0x48, 0x60, 0x38, 255))  # shadow
    # Backpack strap
    px(d, 3, 6, 1, 7, (0x50, 0x68, 0x40, 255))
    # Left arm
    px(d, 2, 7, 1, 4, JACKET_BL)
    px(d, 1, 11, 1, 3, JACKET_BL)
    # Right arm
    px(d, 9, 7, 1, 4, JACKET_BL)
    if frame == 1:
        px(d, 10, 10, 1, 3, JACKET_BL)
    elif frame == 2:
        px(d, 9, 10, 1, 3, JACKET_BL)
    else:
        px(d, 9, 11, 1, 3, JACKET_BL)
    # Hands
    px(d, 1, 14, 1, 1, SKIN_LIGHT)
    px(d, 9, 14, 1, 1, SKIN_LIGHT)
    # Blue jeans
    px(d, ll_x, ll_y, 2, 7, JEANS)
    px(d, rl_x, rl_y, 2, 7, JEANS)
    px(d, ll_x+1, ll_y, 1, 7, (0x20, 0x34, 0x58, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x20, 0x34, 0x58, 255))
    # Sneakers
    px(d, ll_x-1, 26, 3, 2, SHOES_WH)
    px(d, rl_x-1, 26, 3, 2, SHOES_WH)


def draw_turkish_man(d, frame):
    """15. turkish_man — medium skin, dark hair, grey jacket, dark trousers"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 13, 13
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 14, 12
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 12, 14

    # Dark hair (neat, combed)
    px(d, 3, 0, 6, 2, (0x22, 0x18, 0x0C, 255))
    px(d, 2, 2, 8, 1, (0x22, 0x18, 0x0C, 255))
    # Face (medium skin)
    px(d, 3, 1, 6, 4, SKIN_MED)
    px(d, 2, 2, 1, 2, SKIN_MED)
    px(d, 9, 2, 1, 2, SKIN_MED)
    # Eyes
    px(d, 4, 2, 1, 1, BLACK_C)
    px(d, 7, 2, 1, 1, BLACK_C)
    # Brows (dark, bushy)
    px(d, 4, 1, 3, 1, (0x28, 0x18, 0x0C, 255))
    px(d, 7, 1, 3, 1, (0x28, 0x18, 0x0C, 255))
    # Moustache
    px(d, 4, 4, 4, 1, (0x22, 0x18, 0x0C, 255))
    # Mouth
    px(d, 5, 5, 2, 1, (0xA0, 0x68, 0x44, 255))
    # Neck
    px(d, 5, 5, 2, 1, SKIN_MED)
    # Grey jacket (zip-up style)
    px(d, 3, 6, 6, 9, TROUSERS_G)
    px(d, 8, 6, 1, 9, (0x38, 0x38, 0x34, 255))
    px(d, 3, 6, 1, 9, (0x58, 0x58, 0x54, 255))
    # Zip line
    px(d, 6, 6, 1, 8, (0x40, 0x40, 0x3C, 255))
    # Collar
    px(d, 5, 6, 2, 2, (0x54, 0x54, 0x50, 255))
    # Left arm
    px(d, 2, 7, 1, 4, TROUSERS_G)
    px(d, 1, la_y-2, 1, 3, TROUSERS_G)
    # Right arm
    px(d, 9, 7, 1, 4, TROUSERS_G)
    px(d, 9, ra_y-2, 1, 3, TROUSERS_G)
    # Hands
    px(d, 1, la_y+1, 1, 2, SKIN_MED)
    px(d, 9, ra_y+1, 1, 2, SKIN_MED)
    # Dark trousers
    px(d, ll_x, ll_y, 2, 7, (0x28, 0x28, 0x24, 255))
    px(d, rl_x, rl_y, 2, 7, (0x28, 0x28, 0x24, 255))
    px(d, ll_x+1, ll_y, 1, 7, (0x1C, 0x1C, 0x18, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x1C, 0x1C, 0x18, 255))
    # Shoes
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)


def draw_imam(d, frame):
    """16. imam — dark skin, white djellaba, white kufi"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 21, 21
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 20, 22
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 22, 20

    # White kufi cap
    px(d, 3, 0, 6, 2, KUFI_WH)
    px(d, 2, 2, 8, 2, KUFI_WH)
    px(d, 3, 0, 2, 1, (0xFF, 0xFF, 0xFF, 255))  # cap shine
    # Face (dark skin)
    px(d, 3, 2, 6, 4, SKIN_DARK)
    px(d, 2, 3, 1, 2, SKIN_DARK)
    px(d, 9, 3, 1, 2, SKIN_DARK)
    # Eyes (warm, wise)
    px(d, 4, 3, 1, 1, BLACK_C)
    px(d, 7, 3, 1, 1, BLACK_C)
    # Beard (full, dark with grey)
    px(d, 3, 5, 6, 3, (0x28, 0x20, 0x18, 255))
    px(d, 4, 6, 4, 2, HAIR_GRY)
    # White djellaba (flowing, long)
    px(d, 1, 8, 10, 18, DJELL_WH)
    # Djellaba shadow left
    px(d, 1, 8, 1, 18, (0xD0, 0xCC, 0xC4, 255))
    # Djellaba shadow right
    px(d, 10, 8, 1, 18, (0xD0, 0xCC, 0xC4, 255))
    # Djellaba highlight
    px(d, 2, 8, 3, 1, (0xFF, 0xFF, 0xFF, 255))
    # Vertical fold lines
    px(d, 6, 9, 1, 15, (0xD8, 0xD4, 0xCC, 255))
    px(d, 4, 10, 1, 12, (0xE8, 0xE4, 0xDC, 255))
    # Djellaba hood neck area
    px(d, 4, 8, 4, 2, (0xD8, 0xD4, 0xCC, 255))
    # Wide sleeves
    px(d, 0, 9, 2, 6, DJELL_WH)
    px(d, 10, 9, 2, 6, DJELL_WH)
    # Hands (peeking from sleeves)
    px(d, 0, 14, 1, 2, SKIN_DARK)
    px(d, 11, 14, 1, 2, SKIN_DARK)
    # Legs under djellaba
    px(d, ll_x, ll_y, 2, 6, DJELL_WH)
    px(d, rl_x, rl_y, 2, 6, DJELL_WH)
    # Shoes (dark, peek below)
    px(d, ll_x, 26, 3, 2, SHOES_BK)
    px(d, rl_x, 26, 3, 2, SHOES_BK)


def draw_construction(d, frame):
    """17. construction — medium skin, hard hat (yellow), orange vest, dark trousers"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Yellow hard hat
    px(d, 2, 0, 8, 3, HELM_YL)
    px(d, 1, 3, 10, 2, HELM_YL)
    # Hard hat brim (extends a bit)
    px(d, 1, 5, 10, 1, (0xC8, 0xAC, 0x00, 255))
    # Hat highlight
    px(d, 2, 0, 3, 1, (0xFF, 0xE8, 0x40, 255))
    # Face (medium skin, stubble)
    px(d, 3, 5, 6, 3, SKIN_MED)
    px(d, 2, 6, 1, 1, SKIN_MED)
    px(d, 9, 6, 1, 1, SKIN_MED)
    # Eyes
    px(d, 4, 6, 1, 1, BLACK_C)
    px(d, 7, 6, 1, 1, BLACK_C)
    # Stubble
    px(d, 3, 7, 6, 1, SKIN_MED_SHD)
    # Neck
    px(d, 5, 8, 2, 1, SKIN_MED)
    # Orange safety vest over dark shirt
    px(d, 3, 9, 6, 8, VEST_OR)
    px(d, 8, 9, 1, 8, (0xA0, 0x50, 0x08, 255))
    px(d, 3, 9, 1, 8, (0xE0, 0x80, 0x20, 255))
    # Reflective strips (horizontal)
    px(d, 3, 12, 6, 1, (0xF0, 0xEC, 0xE0, 255))
    px(d, 3, 15, 6, 1, (0xF0, 0xEC, 0xE0, 255))
    # Vest zipper
    px(d, 6, 9, 1, 7, (0xB0, 0x58, 0x10, 255))
    # Dark shirt under vest at arms
    px(d, 2, 9, 1, 4, (0x20, 0x20, 0x18, 255))
    px(d, 2, la_y-2, 1, 3, (0x20, 0x20, 0x18, 255))
    px(d, 9, 9, 1, 4, VEST_OR)
    px(d, 9, ra_y-2, 1, 3, (0x20, 0x20, 0x18, 255))
    # Hands (work gloves)
    px(d, 1, la_y+1, 1, 2, (0x58, 0x44, 0x30, 255))
    px(d, 9, ra_y+1, 1, 2, (0x58, 0x44, 0x30, 255))
    # Dark work trousers
    px(d, ll_x, ll_y, 2, 7, (0x20, 0x20, 0x1C, 255))
    px(d, rl_x, rl_y, 2, 7, (0x20, 0x20, 0x1C, 255))
    px(d, ll_x+1, ll_y, 1, 7, (0x14, 0x14, 0x10, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x14, 0x14, 0x10, 255))
    # Work boots (heavy, dark with toe cap)
    px(d, ll_x-1, 26, 3, 2, (0x18, 0x14, 0x10, 255))
    px(d, rl_x-1, 26, 3, 2, (0x18, 0x14, 0x10, 255))
    px(d, ll_x-1, 26, 1, 1, (0x30, 0x28, 0x20, 255))  # toe cap shine
    px(d, rl_x-1, 26, 1, 1, (0x30, 0x28, 0x20, 255))


def draw_cyclist_walk(d, frame):
    """18. cyclist_walk — medium skin, helmet, dark jacket, jeans"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 20, 20
        la_y, ra_y = 12, 12
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 19, 21
        la_y, ra_y = 13, 11
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 21, 19
        la_y, ra_y = 11, 13

    # Cycling helmet (aerodynamic, vented)
    px(d, 2, 0, 8, 3, (0x60, 0xA0, 0x30, 255))  # green helmet
    px(d, 1, 3, 10, 2, (0x60, 0xA0, 0x30, 255))
    # Helmet vents (dark stripes)
    px(d, 3, 1, 1, 2, (0x20, 0x40, 0x10, 255))
    px(d, 5, 1, 1, 2, (0x20, 0x40, 0x10, 255))
    px(d, 7, 1, 1, 2, (0x20, 0x40, 0x10, 255))
    # Helmet highlight
    px(d, 2, 0, 2, 1, (0x80, 0xC0, 0x40, 255))
    # Sunglasses (dark wrap-around)
    px(d, 2, 5, 8, 1, (0x20, 0x20, 0x18, 255))
    # Face (medium skin)
    px(d, 3, 5, 6, 3, SKIN_MED)
    px(d, 2, 6, 1, 1, SKIN_MED)
    px(d, 9, 6, 1, 1, SKIN_MED)
    # Sunglasses over face
    px(d, 3, 5, 6, 1, (0x18, 0x18, 0x10, 255))
    # Nose/chin visible
    px(d, 5, 6, 2, 1, SKIN_MED_SHD)
    # Mouth
    px(d, 5, 7, 2, 1, SKIN_MED)
    # Chin strap
    px(d, 2, 7, 1, 1, (0x48, 0x78, 0x20, 255))
    px(d, 9, 7, 1, 1, (0x48, 0x78, 0x20, 255))
    # Neck
    px(d, 5, 8, 2, 1, SKIN_MED)
    # Dark jacket (cycling/casual)
    px(d, 3, 9, 6, 8, JACKET_BK)
    px(d, 8, 9, 1, 8, (0x10, 0x0C, 0x08, 255))
    px(d, 3, 9, 1, 8, (0x28, 0x24, 0x20, 255))
    # Jacket collar
    px(d, 5, 9, 2, 1, (0x18, 0x14, 0x10, 255))
    # Bright panel on jacket (cycling-style)
    px(d, 4, 10, 1, 5, (0x60, 0xA0, 0x30, 255))
    # Left arm
    px(d, 2, 9, 1, 4, JACKET_BK)
    px(d, 1, la_y-2, 1, 3, JACKET_BK)
    # Right arm
    px(d, 9, 9, 1, 4, JACKET_BK)
    px(d, 9, ra_y-2, 1, 3, JACKET_BK)
    # Hands
    px(d, 1, la_y+1, 1, 1, SKIN_MED)
    px(d, 9, ra_y+1, 1, 1, SKIN_MED)
    # Jeans
    px(d, ll_x, ll_y, 2, 7, JEANS)
    px(d, rl_x, rl_y, 2, 7, JEANS)
    px(d, ll_x+1, ll_y, 1, 7, (0x20, 0x34, 0x58, 255))
    px(d, rl_x+1, rl_y, 1, 7, (0x20, 0x34, 0x58, 255))
    # Shoes (bike shoes - slightly stiff)
    px(d, ll_x-1, 26, 3, 2, (0x20, 0x30, 0x18, 255))
    px(d, rl_x-1, 26, 3, 2, (0x20, 0x30, 0x18, 255))


def draw_old_man_suit(d, frame):
    """19. old_man_suit — light skin, grey hair, dark brown coat, grey trousers, hat"""
    if frame == 0:
        ll_x, rl_x, ll_y, rl_y = 3, 6, 19, 19
    elif frame == 1:
        ll_x, rl_x, ll_y, rl_y = 2, 7, 18, 20
    else:
        ll_x, rl_x, ll_y, rl_y = 4, 5, 20, 18

    # Felt hat (3px brim, dark)
    px(d, 2, 0, 8, 2, HAT_DK)   # hat crown
    px(d, 1, 2, 10, 1, HAT_DK)  # brim 1
    px(d, 1, 3, 10, 1, (0x1C, 0x16, 0x10, 255))  # brim underside shadow
    # Hat band
    px(d, 2, 2, 8, 1, (0x10, 0x0C, 0x08, 255))
    # Hat crown highlight
    px(d, 2, 0, 3, 1, (0x38, 0x30, 0x28, 255))
    # Grey hair at sides (under hat brim)
    px(d, 2, 3, 2, 2, HAIR_GRY)
    px(d, 8, 3, 2, 2, HAIR_GRY)
    # Face (light, older with lines)
    px(d, 3, 3, 6, 4, SKIN_LIGHT)
    px(d, 2, 4, 1, 2, SKIN_LIGHT)
    px(d, 9, 4, 1, 2, SKIN_LIGHT)
    # Eyes (slightly sunken)
    px(d, 4, 4, 1, 1, BLACK_C)
    px(d, 7, 4, 1, 1, BLACK_C)
    # Grey brows
    px(d, 4, 3, 2, 1, HAIR_GRY)
    px(d, 7, 3, 2, 1, HAIR_GRY)
    # Wrinkles (age lines)
    px(d, 3, 5, 1, 1, SKIN_LIGHT_SHD)
    px(d, 9, 5, 1, 1, SKIN_LIGHT_SHD)
    # Mouth (stern)
    px(d, 5, 6, 2, 1, (0xCC, 0x98, 0x78, 255))
    # Neck + collar
    px(d, 5, 7, 2, 1, SKIN_LIGHT)
    # White shirt collar visible
    px(d, 5, 8, 2, 1, SHIRT_WH)
    # Tie (dark, elegant)
    px(d, 6, 8, 1, 5, (0x40, 0x10, 0x10, 255))
    # Dark brown coat (dignified)
    px(d, 3, 8, 6, 11, COAT_BN)
    px(d, 8, 8, 1, 11, (0x50, 0x30, 0x18, 255))
    px(d, 3, 8, 1, 11, (0x80, 0x58, 0x38, 255))
    # Coat lapels
    px(d, 5, 8, 2, 3, (0x60, 0x40, 0x24, 255))
    # Coat buttons
    px(d, 6, 11, 1, 1, (0x40, 0x28, 0x10, 255))
    px(d, 6, 14, 1, 1, (0x40, 0x28, 0x10, 255))
    # Left arm (close to body, dignified posture)
    px(d, 2, 9, 1, 4, COAT_BN)
    px(d, 1, 13, 1, 3, COAT_BN)
    # Right arm
    px(d, 9, 9, 1, 4, COAT_BN)
    px(d, 9, 13, 1, 3, COAT_BN)
    # Hands (pale)
    px(d, 1, 16, 1, 1, SKIN_LIGHT)
    px(d, 9, 16, 1, 1, SKIN_LIGHT)
    # Grey trousers (pressed)
    px(d, ll_x, ll_y, 2, 8, TROUSERS_G)
    px(d, rl_x, rl_y, 2, 8, TROUSERS_G)
    px(d, ll_x+1, ll_y, 1, 8, (0x38, 0x38, 0x34, 255))
    px(d, rl_x+1, rl_y, 1, 8, (0x38, 0x38, 0x34, 255))
    # Trouser crease
    px(d, ll_x, ll_y+1, 1, 6, (0x58, 0x58, 0x54, 255))
    px(d, rl_x, rl_y+1, 1, 6, (0x58, 0x58, 0x54, 255))
    # Shoes (classic polished leather)
    px(d, ll_x-1, 26, 3, 2, SHOES_BK)
    px(d, rl_x-1, 26, 3, 2, SHOES_BK)
    px(d, ll_x-1, 26, 1, 1, (0x38, 0x30, 0x28, 255))  # shoe shine


# ── Person registry ───────────────────────────────────────────────────────────
PERSONS = [
    ("fatima_crowd",   draw_fatima_crowd),
    ("moroccan_man",   draw_moroccan_man),
    ("teen_boy",       draw_teen_boy),
    ("elderly_man",    draw_elderly_man),
    ("hijab_woman_b",  draw_hijab_woman_b),
    ("business_man",   draw_business_man),
    ("kid_short",      draw_kid_short),
    ("young_woman",    draw_young_woman),
    ("delivery_man",   draw_delivery_man),
    ("elderly_woman",  draw_elderly_woman),
    ("white_hijab",    draw_white_hijab),
    ("teen_girl",      draw_teen_girl),
    ("market_vendor",  draw_market_vendor),
    ("kapper_man",     draw_kapper_man),
    ("student",        draw_student),
    ("turkish_man",    draw_turkish_man),
    ("imam",           draw_imam),
    ("construction",   draw_construction),
    ("cyclist_walk",   draw_cyclist_walk),
    ("old_man_suit",   draw_old_man_suit),
]


def main():
    os.makedirs(BASE_DIR, exist_ok=True)

    sheet_w = FW * NUM_FRAMES * NUM_PERSONS  # 4320
    sheet = Image.new('RGBA', (sheet_w, FH), (0, 0, 0, 0))

    print("=" * 60)
    print("Turnhoutsebaan Crowd Sprite Generator")
    print(f"  Frame: {GW}x{GH} game px | SCALE={SCALE} | {FW}x{FH} px per frame")
    print(f"  Sheet: {sheet_w}x{FH} px")
    print("=" * 60)

    for i, (name, draw_fn) in enumerate(PERSONS):
        person_strip = Image.new('RGBA', (FW * NUM_FRAMES, FH), (0, 0, 0, 0))

        for frame in range(NUM_FRAMES):
            frame_img = make_frame()
            d = ImageDraw.Draw(frame_img)
            draw_fn(d, frame)
            person_strip.paste(frame_img, (frame * FW, 0))
            sheet.paste(frame_img, (i * FW * NUM_FRAMES + frame * FW, 0))

        strip_path = os.path.join(BASE_DIR, f"crowd_{i:02d}_{name}.png")
        person_strip.save(strip_path)
        print(f"  [{i:02d}] {name} — 3 frames")

    sheet_path = os.path.join(BASE_DIR, "crowd_sheet.png")
    sheet.save(sheet_path)
    print(f"\n✓ crowd_sheet.png ({sheet_w}x{FH} px)")
    print(f"  → {sheet_path}")


if __name__ == '__main__':
    main()
