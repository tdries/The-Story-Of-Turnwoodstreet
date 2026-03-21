#!/usr/bin/env python3
"""
Item Icon Spritesheet Generator — Turnhoutsebaan RPG
=====================================================
13 quest/inventory icons, each 16×16 game-px.
Output: single horizontal PNG strip, 208×16 px (1x, 1px per game-px).

Frame order (matches ITEM_FRAME in ItemBar.ts):
  0  fabric_bolt        1  delivery_package   2  flour
  3  oud_string         4  tram_ticket        5  harira
  6  baklava            7  samen_flyer        8  permit_doc
  9  friet             10  reuzenpoort_key   11  mint_tea
 12  smoske
"""

import os
from PIL import Image, ImageDraw

SCALE    = 1          # 1px per game-px — Phaser loads at frameWidth=16
W, H     = 16, 16    # per icon, in game-px
N        = 13
PW       = W * N     # 208
PH       = H         # 16

OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Sprites', 'items')
OUT_FILE = os.path.join(OUT_DIR, 'items_sheet.png')
os.makedirs(OUT_DIR, exist_ok=True)

img  = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

def px(draw, ix, x, y, col):
    """Draw a single game-pixel at icon-local (x,y) for icon index ix."""
    gx = ix * W + x
    gy = y
    draw.rectangle([gx, gy, gx, gy], fill=col)

def rect(draw, ix, x1, y1, x2, y2, col):
    """Fill a rectangle [x1,y1..x2,y2] inclusive (game-px coords)."""
    draw.rectangle([ix*W+x1, y1, ix*W+x2, y2], fill=col)

# ── Colour palette ──────────────────────────────────────────────────────────
C = {
    # Neutrals
    'black':   (0x0A, 0x0A, 0x12, 255),
    'white':   (0xF0, 0xEA, 0xD6, 255),
    'gold':    (0xFF, 0xD7, 0x00, 255),
    'gold_d':  (0xC0, 0x90, 0x00, 255),
    'cream':   (0xF5, 0xF5, 0xDC, 255),
    'grey':    (0x88, 0x88, 0x88, 255),
    'dk_grey': (0x44, 0x44, 0x44, 255),
    # Browns
    'brown':   (0x8B, 0x45, 0x13, 255),
    'lt_brn':  (0xD4, 0xA8, 0x50, 255),
    'card':    (0xCC, 0xA0, 0x60, 255),
    'card_d':  (0x99, 0x70, 0x38, 255),
    # Fabric / cloth
    'fab_r':   (0xC0, 0x39, 0x2B, 255),
    'fab_b':   (0x1E, 0x5F, 0xA0, 255),
    'fab_g':   (0x27, 0xAE, 0x60, 255),
    # Food
    'soup_r':  (0xC0, 0x30, 0x20, 255),
    'soup_o':  (0xE0, 0x70, 0x20, 255),
    'honey':   (0xE8, 0xB8, 0x00, 255),
    'pastry':  (0xD4, 0xA8, 0x30, 255),
    'fry':     (0xFF, 0xE0, 0x80, 255),
    'cone_r':  (0xCC, 0x22, 0x22, 255),
    'cone_w':  (0xF0, 0xEA, 0xD6, 255),
    'bread':   (0xD4, 0xA0, 0x50, 255),
    'fill_g':  (0x27, 0xAE, 0x60, 255),
    'fill_r':  (0xC0, 0x39, 0x2B, 255),
    # Tea
    'tea_a':   (0xC0, 0x80, 0x20, 255),
    'tea_g':   (0x1A, 0x8A, 0x30, 255),
    'glass':   (0xA0, 0xD0, 0xE0, 180),
    # Flour
    'flour':   (0xF5, 0xF5, 0xF5, 255),
    'flour_t': (0xE0, 0xD8, 0xC8, 255),
    # Flyer
    'flyer_o': (0xE8, 0x70, 0x20, 255),
    'flyer_l': (0xF0, 0x90, 0x30, 255),
    # Ticket
    'tick_y':  (0xFF, 0xD7, 0x00, 255),
    'tick_d':  (0xC0, 0x90, 0x00, 255),
    'tick_bl': (0x1E, 0x5F, 0xA0, 255),
    # Key
    'key_g':   (0xFF, 0xD7, 0x00, 255),
    'key_d':   (0xA0, 0x78, 0x00, 255),
    # Document
    'doc_bg':  (0xF5, 0xF5, 0xDC, 255),
    'doc_rd':  (0xCC, 0x2B, 0x1A, 255),
    'doc_bl':  (0x1E, 0x5F, 0xA0, 255),
    # String
    'str_br':  (0xA0, 0x78, 0x30, 255),
    'str_lt':  (0xD4, 0xA8, 0x50, 255),
}

# ─────────────────────────────────────────────────────────────────────────────
# Icon 0: fabric_bolt — rolled scroll of colourful fabric
# ─────────────────────────────────────────────────────────────────────────────
i = 0
# Roll body (horizontal cylinder, cream)
rect(draw, i, 2, 5, 13, 11, C['cream'])
rect(draw, i, 2, 5, 13, 6,  C['lt_brn'])    # top shading
rect(draw, i, 2, 10, 13, 11, C['brown'])    # bottom shadow
# Left cap (end of roll)
rect(draw, i, 0, 4, 2, 12, C['lt_brn'])
rect(draw, i, 0, 4, 0, 12, C['brown'])
# Right cap
rect(draw, i, 13, 4, 15, 12, C['lt_brn'])
rect(draw, i, 15, 4, 15, 12, C['cream'])
# Fabric stripes on roll
rect(draw, i, 4, 6, 5, 10, C['fab_r'])
rect(draw, i, 7, 6, 8, 10, C['fab_b'])
rect(draw, i, 10, 6, 11, 10, C['fab_g'])
# Tie ribbon in centre
rect(draw, i, 7, 3, 8, 13, C['gold'])
rect(draw, i, 5, 7, 10, 9, C['gold'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 1: delivery_package — cardboard box with tape cross
# ─────────────────────────────────────────────────────────────────────────────
i = 1
# Box body
rect(draw, i, 2, 4, 13, 13, C['card'])
# Top flap (slightly lighter)
rect(draw, i, 2, 3, 13, 5, C['lt_brn'])
# Left side (darker)
rect(draw, i, 2, 4, 3, 13, C['card_d'])
# Bottom shadow
rect(draw, i, 2, 12, 13, 13, C['card_d'])
# Tape cross (horizontal + vertical lines)
rect(draw, i, 6, 4, 9, 13, C['tick_y'])     # vertical tape
rect(draw, i, 2, 7, 13, 9, C['tick_y'])     # horizontal tape
# Tape overlap
rect(draw, i, 6, 7, 9, 9, C['gold'])
# Outline
rect(draw, i, 2, 3, 13, 3, C['card_d'])
rect(draw, i, 2, 13, 13, 13, C['card_d'])
rect(draw, i, 2, 3, 2, 13, C['card_d'])
rect(draw, i, 13, 3, 13, 13, C['card_d'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 2: flour — flour sack, off-white with tie and label
# ─────────────────────────────────────────────────────────────────────────────
i = 2
# Sack body (rounded rectangle approximation)
rect(draw, i, 3, 4, 12, 13, C['flour'])
rect(draw, i, 2, 5, 13, 12, C['flour'])
# Shading
rect(draw, i, 2, 5, 2, 12, C['flour_t'])
rect(draw, i, 3, 4, 12, 5, C['flour_t'])
rect(draw, i, 12, 5, 13, 12, C['cream'])
rect(draw, i, 3, 12, 12, 13, C['flour_t'])
# Tie at top
rect(draw, i, 6, 2, 9, 4, C['brown'])
rect(draw, i, 5, 2, 10, 2, C['brown'])
# Label (small blue rectangle on front)
rect(draw, i, 5, 7, 10, 11, C['fab_b'])
rect(draw, i, 6, 8, 9, 10, C['white'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 3: oud_string — coiled string/wire
# ─────────────────────────────────────────────────────────────────────────────
i = 3
# Outer coil ring
rect(draw, i, 4, 3, 11, 4, C['str_br'])
rect(draw, i, 2, 5, 3, 10, C['str_br'])
rect(draw, i, 12, 5, 13, 10, C['str_br'])
rect(draw, i, 4, 11, 11, 12, C['str_br'])
# Inner coil
rect(draw, i, 5, 5, 10, 6, C['str_lt'])
rect(draw, i, 4, 6, 5, 9, C['str_lt'])
rect(draw, i, 10, 6, 11, 9, C['str_lt'])
rect(draw, i, 5, 9, 10, 10, C['str_lt'])
# Centre highlight
rect(draw, i, 6, 7, 9, 8, C['gold_d'])
# String tail
rect(draw, i, 12, 3, 14, 4, C['str_lt'])
rect(draw, i, 13, 4, 14, 6, C['str_lt'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 4: tram_ticket — yellow De Lijn transit ticket
# ─────────────────────────────────────────────────────────────────────────────
i = 4
# Ticket body
rect(draw, i, 1, 4, 14, 12, C['tick_y'])
# Blue stripe at top (De Lijn branding)
rect(draw, i, 1, 4, 14, 6, C['tick_bl'])
# Dark text lines
rect(draw, i, 3, 8, 12, 8, C['tick_d'])
rect(draw, i, 3, 10, 9, 10, C['tick_d'])
# Perforation holes on left
for y in [5, 7, 9, 11]:
    px(draw, i, 1, y, (0, 0, 0, 0))
# Outline
rect(draw, i, 1, 4, 14, 4, C['gold_d'])
rect(draw, i, 1, 12, 14, 12, C['gold_d'])
rect(draw, i, 1, 4, 1, 12, C['gold_d'])
rect(draw, i, 14, 4, 14, 12, C['gold_d'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 5: harira — bowl of Moroccan soup
# ─────────────────────────────────────────────────────────────────────────────
i = 5
# Bowl body (elliptical)
rect(draw, i, 2, 7, 13, 12, C['soup_r'])
rect(draw, i, 1, 8, 14, 11, C['soup_r'])
# Soup surface (top of liquid)
rect(draw, i, 2, 7, 13, 8, C['soup_o'])
rect(draw, i, 1, 8, 14, 8, C['soup_o'])
# Bowl rim
rect(draw, i, 1, 7, 14, 7, C['lt_brn'])
rect(draw, i, 2, 6, 13, 6, C['lt_brn'])
# Bowl bottom
rect(draw, i, 4, 12, 11, 13, C['brown'])
# Steam lines
for sx in [5, 8, 11]:
    rect(draw, i, sx, 3, sx, 5, C['white'])
    rect(draw, i, sx+1, 2, sx+1, 4, C['white'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 6: baklava — diamond-shaped golden pastry
# ─────────────────────────────────────────────────────────────────────────────
i = 6
# Diamond shape (layered)
rect(draw, i, 7, 2, 8, 3, C['pastry'])
rect(draw, i, 5, 4, 10, 5, C['pastry'])
rect(draw, i, 3, 6, 12, 7, C['pastry'])
rect(draw, i, 2, 8, 13, 9, C['pastry'])
rect(draw, i, 3, 10, 12, 11, C['pastry'])
rect(draw, i, 5, 12, 10, 13, C['pastry'])
rect(draw, i, 7, 13, 8, 14, C['pastry'])
# Honey glaze (top lighter)
rect(draw, i, 7, 2, 8, 2, C['honey'])
rect(draw, i, 6, 4, 9, 4, C['honey'])
rect(draw, i, 4, 6, 11, 6, C['honey'])
rect(draw, i, 3, 8, 12, 8, C['honey'])
# Walnut/pistachio dots
px(draw, i, 7, 7, C['fill_g'])
px(draw, i, 5, 9, C['fill_g'])
px(draw, i, 9, 9, C['fill_g'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 7: samen_flyer — orange event flyer
# ─────────────────────────────────────────────────────────────────────────────
i = 7
# Paper body (slight angle: 3px tab at top-right)
rect(draw, i, 2, 3, 13, 14, C['flyer_o'])
rect(draw, i, 11, 2, 13, 4, C['flyer_l'])   # folded corner
# Fold indicator
rect(draw, i, 11, 3, 13, 3, C['brown'])
# Text lines (white)
rect(draw, i, 4, 5, 11, 5, C['white'])
rect(draw, i, 4, 7, 11, 7, C['white'])
rect(draw, i, 4, 9, 8, 9, C['white'])
# Sub-detail lines
rect(draw, i, 4, 11, 10, 11, C['honey'])
rect(draw, i, 4, 12, 7, 12, C['honey'])
# Outline
rect(draw, i, 2, 3, 13, 3, C['brown'])
rect(draw, i, 2, 14, 13, 14, C['brown'])
rect(draw, i, 2, 3, 2, 14, C['brown'])
rect(draw, i, 13, 3, 13, 14, C['brown'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 8: permit_doc — official document with red stamp
# ─────────────────────────────────────────────────────────────────────────────
i = 8
# Paper
rect(draw, i, 2, 2, 13, 14, C['doc_bg'])
rect(draw, i, 2, 2, 2, 14, C['flour_t'])   # left shadow
# Folded corner top-right
rect(draw, i, 10, 2, 13, 5, C['flour_t'])
rect(draw, i, 10, 2, 13, 2, C['grey'])
# Red official stamp (circle)
rect(draw, i, 8, 9, 12, 13, C['doc_rd'])
rect(draw, i, 9, 8, 12, 14, C['doc_rd'])
rect(draw, i, 9, 9, 12, 13, (0xAA, 0x18, 0x0A, 255))  # inner
# Text lines
rect(draw, i, 3, 4, 9, 4, C['grey'])
rect(draw, i, 3, 6, 9, 6, C['grey'])
rect(draw, i, 3, 8, 7, 8, C['grey'])
# GOEDGEKEURD text (implied by blue box at bottom)
rect(draw, i, 3, 11, 7, 12, C['doc_bl'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 9: friet — paper cone of fries
# ─────────────────────────────────────────────────────────────────────────────
i = 9
# Cone (red and white stripes)
rect(draw, i, 4, 8, 11, 14, C['cone_r'])
rect(draw, i, 5, 8, 7, 14, C['cone_w'])
rect(draw, i, 9, 8, 10, 14, C['cone_w'])
# Cone point
rect(draw, i, 6, 13, 9, 15, C['cone_r'])
rect(draw, i, 7, 14, 8, 15, C['cone_r'])
# Fries sticking out
rect(draw, i, 4, 2, 5, 9, C['fry'])
rect(draw, i, 6, 3, 7, 8, C['fry'])
rect(draw, i, 8, 2, 9, 8, C['fry'])
rect(draw, i, 10, 3, 11, 9, C['fry'])
rect(draw, i, 12, 4, 13, 9, C['fry'])
# Fry tips (slightly browned)
rect(draw, i, 4, 2, 5, 2, C['lt_brn'])
rect(draw, i, 6, 3, 7, 3, C['lt_brn'])
rect(draw, i, 8, 2, 9, 2, C['lt_brn'])
rect(draw, i, 10, 3, 11, 3, C['lt_brn'])
rect(draw, i, 12, 4, 13, 4, C['lt_brn'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 10: reuzenpoort_key — ornate gold key
# ─────────────────────────────────────────────────────────────────────────────
i = 10
# Key bow (ring at top)
rect(draw, i, 5, 2, 10, 3, C['key_g'])
rect(draw, i, 4, 3, 11, 4, C['key_g'])
rect(draw, i, 3, 4, 4, 7, C['key_g'])
rect(draw, i, 11, 4, 12, 7, C['key_g'])
rect(draw, i, 4, 7, 5, 8, C['key_g'])
rect(draw, i, 10, 7, 11, 8, C['key_g'])
# Hollow centre of bow
rect(draw, i, 5, 4, 10, 7, (0,0,0,0))
# Key shaft
rect(draw, i, 7, 8, 9, 14, C['key_g'])
# Key bit (teeth)
rect(draw, i, 9, 10, 11, 11, C['key_g'])
rect(draw, i, 9, 12, 12, 13, C['key_g'])
# Shading
rect(draw, i, 7, 8, 7, 14, C['key_d'])
rect(draw, i, 5, 2, 5, 7, C['key_d'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 11: mint_tea — tea glass with amber tea and green mint
# ─────────────────────────────────────────────────────────────────────────────
i = 11
# Glass body
rect(draw, i, 4, 4, 11, 13, C['tea_a'])
rect(draw, i, 3, 5, 12, 12, C['tea_a'])
# Glass walls (transparent edges)
rect(draw, i, 3, 5, 3, 12, C['glass'])
rect(draw, i, 12, 5, 12, 12, C['glass'])
# Glass rim and base
rect(draw, i, 4, 4, 11, 4, C['grey'])
rect(draw, i, 3, 13, 12, 13, C['grey'])
# Highlight reflection
rect(draw, i, 4, 5, 5, 11, (0xFF, 0xFF, 0xFF, 80))
# Mint leaves (green)
rect(draw, i, 5, 2, 8, 5, C['tea_g'])
rect(draw, i, 8, 1, 11, 4, C['tea_g'])
# Steam
rect(draw, i, 6, 1, 6, 3, C['white'])
rect(draw, i, 9, 2, 9, 4, C['white'])

# ─────────────────────────────────────────────────────────────────────────────
# Icon 12: smoske — layered Antwerp sandwich
# ─────────────────────────────────────────────────────────────────────────────
i = 12
# Top bread
rect(draw, i, 1, 3, 14, 6, C['bread'])
rect(draw, i, 1, 3, 14, 4, C['lt_brn'])   # crust top
rect(draw, i, 1, 3, 1, 6, C['lt_brn'])    # crust left
rect(draw, i, 14, 3, 14, 6, C['lt_brn'])  # crust right
# Filling 1 (lettuce)
rect(draw, i, 1, 7, 14, 8, C['fill_g'])
# Filling 2 (tomato/meat)
rect(draw, i, 1, 9, 14, 10, C['fill_r'])
# Filling 3 (cheese/sauce - cream)
rect(draw, i, 1, 11, 14, 11, C['cream'])
# Bottom bread
rect(draw, i, 1, 12, 14, 14, C['bread'])
rect(draw, i, 1, 14, 14, 14, C['lt_brn'])  # crust bottom
rect(draw, i, 1, 12, 1, 14, C['lt_brn'])
rect(draw, i, 14, 12, 14, 14, C['lt_brn'])

# ── Save ─────────────────────────────────────────────────────────────────────
img.save(OUT_FILE)
print(f"Saved {PW}×{PH} px → {OUT_FILE}")
print(f"  13 icons × 16×16 px, frameWidth=16")
