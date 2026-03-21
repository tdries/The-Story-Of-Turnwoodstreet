#!/usr/bin/env python3
"""
Antwerp De Lijn Tram Generator
================================
Single 2-section articulated Citadis tram, facing RIGHT.
TW=112, TH=24 game-px  |  SCALE=4  →  448×96 px

Livery: modern De Lijn — navy blue body, FFD700 stripe, large windows.
"""

import os, math
from PIL import Image, ImageDraw

SCALE    = 4
TW, TH   = 112, 24
PW, PH   = TW * SCALE, TH * SCALE   # 448 × 96 px

OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Sprites', 'tram')
OUT_FILE = os.path.join(OUT_DIR, 'tram.png')
os.makedirs(OUT_DIR, exist_ok=True)

C = {
    'body':      (0x0D, 0x20, 0x45),
    'body_l':    (0x15, 0x30, 0x60),
    'body_d':    (0x08, 0x14, 0x2E),
    'stripe':    (0xFF, 0xD7, 0x00),
    'stripe_l':  (0xFF, 0xE8, 0x55),
    'roof':      (0x22, 0x38, 0x60),
    'roof_eq':   (0x88, 0x88, 0x99),
    'glass':     (0x5A, 0x88, 0xBB),
    'glass_l':   (0x8A, 0xB8, 0xE0),
    'frame_c':   (0xCC, 0xD0, 0xD8),
    'door_bg':   (0x08, 0x18, 0x38),
    'door_edge': (0xAA, 0xAA, 0xBB),
    'skirt':     (0x06, 0x10, 0x25),
    'rubber':    (0x1A, 0x1A, 0x1A),
    'rim':       (0x88, 0x88, 0x99),
    'bogie':     (0x28, 0x28, 0x38),
    'pantograph':(0xAA, 0xAA, 0xBB),
    'headlight': (0xFF, 0xFF, 0xDD),
    'taillight': (0xCC, 0x22, 0x22),
    'dest_bg':   (0x0A, 0x0A, 0x18),
    'dest_txt':  (0xFF, 0xFF, 0xFF),
    'artic':     (0x1A, 0x30, 0x55),
    'shadow':    (0x00, 0x00, 0x00, 55),
}

def S(v): return int(v * SCALE)

def R(d, x1, y1, x2, y2, col):
    if x2 <= x1 or y2 <= y1: return
    c = col + (255,) if len(col) == 3 else col
    d.rectangle([S(x1), S(y1), S(x2)-1, S(y2)-1], fill=c)

def PX(d, x, y, col):
    R(d, x, y, x+1, y+1, col)

def HL(d, x1, x2, y, col):
    R(d, x1, y, x2, y+1, col)

def VL(d, x, y1, y2, col):
    R(d, x, y1, x+1, y2, col)

def circ(d, cx, cy, r, col):
    for dx in range(-r, r+1):
        for dy in range(-r, r+1):
            if dx*dx + dy*dy <= r*r:
                PX(d, cx+dx, cy+dy, col)

def window(d, x, y, w=8, h=9):
    R(d, x,   y,   x+w, y+h,   C['glass'])
    R(d, x+1, y+1, x+w-1, y+h-1, C['glass_l'])
    HL(d, x, x+w, y,     C['frame_c'])
    HL(d, x, x+w, y+h-1, C['frame_c'])
    VL(d, x,     y, y+h, C['frame_c'])
    VL(d, x+w-1, y, y+h, C['frame_c'])
    PX(d, x+1, y+1, (0xFF, 0xFF, 0xFF, 100))
    PX(d, x+2, y+1, (0xFF, 0xFF, 0xFF, 60))

def door(d, x, y=4, w=7, h=11):
    R(d, x, y, x+w, y+h, C['door_bg'])
    HL(d, x, x+w, y, C['door_edge'])
    VL(d, x,     y, y+h, C['door_edge'])
    VL(d, x+w-1, y, y+h, C['door_edge'])
    # door handle pixel
    PX(d, x+w-2, y+h//2, C['frame_c'])

def bogie(d, cx, wy=21):
    R(d, cx-4, wy-2, cx+4, wy, C['bogie'])
    HL(d, cx-4, cx+4, wy-2, C['rim'])
    circ(d, cx-2, wy+1, 2, C['rubber'])
    circ(d, cx+2, wy+1, 2, C['rubber'])
    PX(d, cx-2, wy+1, C['rim'])
    PX(d, cx+2, wy+1, C['rim'])

img = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
d   = ImageDraw.Draw(img)

# ── SECTION 1 (front, x=0–52) ──────────────────────────────────────────────
R(d,  1,  2, 52, 20, C['body'])
R(d,  0,  0, 52,  3, C['roof'])
# Roof equipment
R(d, 15,  0, 28,  1, C['roof_eq'])
# Body highlight panel (upper third)
R(d,  4,  2, 52,  5, C['body_l'])

# Front cab nose (slightly rounded)
R(d,  0,  3,  3, 20, C['body_d'])
R(d,  1,  3,  4, 20, C['body'])
PX(d, 2,  4, C['body_l'])

# Destination display
R(d,  2,  2, 11,  4, C['dest_bg'])
for px, py in [(3,2),(4,2),(5,2),(7,2),(8,2),(9,2),(5,3),(7,3),(8,3),(3,3),(4,3),(5,3)]:
    PX(d, px, py, C['dest_txt'])

# Cab windscreen
window(d, 3, 4, w=7, h=9)

# Section 1 windows
for wx in [12, 22, 32, 42]:
    window(d, wx, 4, w=8, h=9)

# Door 1 (section 1 front)
door(d, 17, y=4, w=7, h=11)

# Yellow stripe
R(d, 3,  15, 52, 19, C['stripe'])
HL(d, 3,  52, 15, C['stripe_l'])

# Headlights
R(d,  1, 14,  3, 16, C['headlight'])
R(d,  1, 16,  3, 17, (0xFF, 0xAA, 0x00))   # amber

# Lower skirt
R(d,  2, 19, 52, 22, C['skirt'])
HL(d, 2,  52, 19, C['body_d'])

# Bogies section 1
bogie(d, 9)
bogie(d, 40)

# ── ARTICULATION BELLOWS (x=52–56) ──────────────────────────────────────────
R(d, 52,  2, 56, 20, C['artic'])
for bx in range(52, 56, 2):
    VL(d, bx, 3, 19, C['body_l'])

# ── SECTION 2 (rear, x=56–112) ──────────────────────────────────────────────
R(d, 56,  2, 111, 20, C['body'])
R(d, 56,  0, 112,  3, C['roof'])
R(d, 65,  0,  78,  1, C['roof_eq'])
R(d, 85,  0,  98,  1, C['roof_eq'])
R(d, 56,  2, 112,  5, C['body_l'])

# Section 2 windows
for wx in [57, 67, 77, 87, 97]:
    window(d, wx, 4, w=8, h=9)

# Door 2 (section 2)
door(d, 72, y=4, w=7, h=11)

# Yellow stripe section 2
R(d, 56, 15, 111, 19, C['stripe'])
HL(d, 56, 111, 15, C['stripe_l'])

# Rear tail
R(d, 109,  3, 112, 20, C['body_d'])
R(d, 108,  3, 111, 20, C['body'])
# Taillights
R(d, 110, 14, 112, 16, C['taillight'])
R(d, 110, 16, 112, 17, (0xFF, 0x66, 0x00))

# Lower skirt section 2
R(d, 56, 19, 110, 22, C['skirt'])
HL(d, 56, 110, 19, C['body_d'])

# Bogies section 2
bogie(d, 70)
bogie(d, 103)

# ── PANTOGRAPH ───────────────────────────────────────────────────────────────
px0 = 24
R(d, px0-1, 0, px0+2, 1, C['pantograph'])
VL(d, px0,  -3, 0,       C['pantograph'])
HL(d, px0-3, px0+4, -4,  C['pantograph'])

# ── DROP SHADOW ───────────────────────────────────────────────────────────────
R(d, 5, 23, 109, 24, C['shadow'])

img.save(OUT_FILE)
print('=' * 60)
print('Antwerp De Lijn Tram Generator')
print(f'  Size: {TW}×{TH} game-px | SCALE={SCALE} | {PW}×{PH} px')
print(f'\n✓ tram.png → {OUT_FILE}')
