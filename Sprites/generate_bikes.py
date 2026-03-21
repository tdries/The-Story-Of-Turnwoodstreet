#!/usr/bin/env python3
"""
Turnhoutsebaan Biker Sprite Generator — v2
==========================================
16 biker types cycling along the Turnhoutsebaan.
Each frame: 36×30 game-px   SCALE=6 → 216×180 px per frame
Sheet: 3456×180 px  (16 frames side-by-side, all facing RIGHT)

Types:
  0  racing_red      — road frame red, drop bars, helmet, lycra
  1  racing_blue     — road frame blue, drop bars, helmet, lycra
  2  city_blue       — city teal-blue, flat bars, upright, basket
  3  city_red        — city red, upright, cap, pannier
  4  ebike_gray      — ebike metallic gray, battery, flat bars
  5  mountain_green  — mountain dark green, wide bars, helmet
  6  mountain_orange — mountain orange, wide bars, helmet
  7  cargo_yellow    — cargo/bakfiets yellow, long front, box
  8  cargo_child     — standard blue + child seat rear
  9  delivery_green  — city dark green, panniers, hi-vis vest
 10  grandma_blue    — step-through dusty blue, basket, flowers, hat
 11  hijab_teal      — step-through teal, teal hijab, long skirt
 12  hijab_purple    — step-through purple, purple hijab, coat
 13  fixie_black     — minimal black, flat bars, jersey
 14  dutch_beige     — classic Dutch, fenders, chain guard, basket, hat
 15  bmx_red         — small red frame, small wheels, standing rider
"""

import os
import math
from PIL import Image, ImageDraw

SCALE   = 6
FW, FH  = 36, 30          # game-px per frame
PW, PH  = FW * SCALE, FH * SCALE   # 216 × 180 px per frame
N_TYPES = 16

OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Sprites', 'bikes')
OUT_FILE = os.path.join(OUT_DIR, 'bikes_sheet.png')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    # Skin tones
    'skin_l':    (0xF5, 0xD0, 0xA9),
    'skin_m':    (0xC8, 0x96, 0x60),
    'skin_d':    (0x7A, 0x50, 0x30),
    'skin_dk':   (0x4A, 0x2A, 0x10),
    # Frame colours
    'red':       (0xCC, 0x22, 0x22),
    'red_dark':  (0x99, 0x11, 0x11),
    'blue':      (0x22, 0x44, 0xCC),
    'blue_dark': (0x11, 0x22, 0x88),
    'teal':      (0x22, 0xAA, 0x99),
    'teal_dark': (0x11, 0x77, 0x66),
    'green':     (0x22, 0x88, 0x22),
    'green_dk':  (0x11, 0x55, 0x11),
    'orange':    (0xDD, 0x66, 0x00),
    'orange_dk': (0xAA, 0x44, 0x00),
    'yellow':    (0xEE, 0xCC, 0x00),
    'yellow_dk': (0xAA, 0x99, 0x00),
    'purple':    (0x66, 0x22, 0xAA),
    'purple_dk': (0x44, 0x11, 0x77),
    'black':     (0x18, 0x18, 0x18),
    'gray':      (0x88, 0x88, 0x88),
    'lgray':     (0xCC, 0xCC, 0xCC),
    'dgray':     (0x44, 0x44, 0x44),
    'mgray':     (0x88, 0x88, 0x99),   # metallic gray
    'brown':     (0x88, 0x55, 0x22),
    'dbrown':    (0x55, 0x33, 0x11),
    'beige':     (0xDD, 0xCC, 0xAA),
    'cream':     (0xF0, 0xE8, 0xD0),
    'navy':      (0x11, 0x22, 0x55),
    'white':     (0xF0, 0xEA, 0xD6),
    'pink':      (0xEE, 0x44, 0x88),
    'hiviz':     (0xFF, 0xDD, 0x00),
    # Bike parts
    'chrome':    (0xCC, 0xCC, 0xDD),
    'silver':    (0xAA, 0xAA, 0xBB),
    'rubber':    (0x22, 0x22, 0x22),
    'rim':       (0xAA, 0xAA, 0xCC),
    'spoke':     (0x99, 0x99, 0xAA),
    'chain':     (0x55, 0x55, 0x33),
    'chain_hi':  (0x77, 0x77, 0x44),
    'saddle':    (0x33, 0x1A, 0x00),
    'saddle_hi': (0x55, 0x33, 0x11),
    'basket':    (0xAA, 0x88, 0x44),
    'basket_dk': (0x77, 0x55, 0x22),
    'box_wood':  (0xCC, 0xAA, 0x55),
    'box_dark':  (0x99, 0x77, 0x33),
    'lycra_w':   (0xEE, 0xEE, 0xEE),
    'lycra_y':   (0xEE, 0xCC, 0x00),
    'shadow':    (0x00, 0x00, 0x00, 0x40),
    'hijab_t':   (0x22, 0xAA, 0x99),
    'hijab_p':   (0x77, 0x33, 0xBB),
    'jacket_br': (0x88, 0x55, 0x22),
    'fender':    (0xCC, 0xCC, 0xAA),
}

# ── Core drawing helpers ──────────────────────────────────────────────────────

def S(v):
    """Scale a game-pixel value to PNG-pixel value."""
    return v * SCALE

def R(d, x1, y1, x2, y2, col):
    """Draw a filled rectangle in game-px coords (x2,y2 exclusive)."""
    if len(col) == 3:
        col = col + (255,)
    d.rectangle([S(x1), S(y1), S(x2) - 1, S(y2) - 1], fill=col)

def PX(d, x, y, col):
    """Draw a single game-pixel."""
    R(d, x, y, x + 1, y + 1, col)

def HL(d, x1, x2, y, col, t=1):
    """Horizontal line from x1 to x2 (inclusive) at game-row y, thickness t rows."""
    R(d, x1, y, x2 + 1, y + t, col)

def VL(d, x, y1, y2, col, t=1):
    """Vertical line from y1 to y2 (inclusive) at game-col x, thickness t cols."""
    R(d, x, y1, x + t, y2 + 1, col)

def line(d, x0, y0, x1, y1, col):
    """Bresenham line in game-px coords."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        PX(d, x0, y0, col)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def circle_outline(d, cx, cy, r, col, thickness=1):
    """
    Draw a circle outline at game-px centre (cx, cy) with given radius and thickness.
    Uses midpoint circle algorithm sampling all 8 octants.
    """
    if len(col) == 3:
        col = col + (255,)
    for t in range(thickness):
        cr = r - t
        if cr <= 0:
            break
        x = cr
        y = 0
        err = 0
        while x >= y:
            pts = [
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x),
            ]
            for px, py in pts:
                PX(d, px, py, col)
            y += 1
            err += 1 + 2 * y
            if 2 * (err - x) + 1 > 0:
                x -= 1
                err += 1 - 2 * x

# ── Wheel ─────────────────────────────────────────────────────────────────────

def wheel(d, cx, cy, r=5, tyre_col=None, rim_col=None, n_spokes=8):
    """
    Draw a detailed bicycle wheel with tyre, rim, spokes, hub and shadow.
    cx, cy, r all in game-px.
    """
    if tyre_col is None:
        tyre_col = C['rubber']
    if rim_col is None:
        rim_col = C['rim']

    # Drop shadow (slightly offset, semi-transparent)
    shadow_col = (0, 0, 0, 50)
    circle_outline(d, cx + 1, cy + 1, r, shadow_col, thickness=1)

    # Tyre — 2 px thick rubber ring
    circle_outline(d, cx, cy, r, tyre_col, thickness=2)

    # Rim — 1 px silver ring just inside tyre
    circle_outline(d, cx, cy, r - 2, rim_col, thickness=1)

    # Spokes — lines from hub to inner rim
    spoke_col = C['spoke']
    for i in range(n_spokes):
        angle = (2 * math.pi * i) / n_spokes
        # Spoke end at rim (r-3 to leave gap at tyre)
        sx = int(round(cx + (r - 3) * math.cos(angle)))
        sy = int(round(cy + (r - 3) * math.sin(angle)))
        line(d, cx, cy, sx, sy, spoke_col)

    # Hub — small 2×2 square at centre
    R(d, cx - 1, cy - 1, cx + 1, cy + 1, rim_col)

# ── Frame drawing ─────────────────────────────────────────────────────────────

def draw_frame(d, rw, fw, wy, r, col, style='road'):
    """
    Draw bicycle frame components.
    rw = rear wheel cx, fw = front wheel cx, wy = wheel cy (all game-px)
    r  = wheel radius
    col = frame colour (3-tuple)
    style: 'road','city','mountain','cargo','step_through','bmx','fixie','ebike'
    """
    bb_x = (rw + fw) // 2         # bottom bracket x
    seat_x = rw + (fw - rw) // 3  # seat tube top x (skewed toward rear)
    seat_top = wy - r - 8         # seat tube top y
    bb_y    = wy - 1              # bottom bracket y (at chain level)

    dark = tuple(max(0, c - 30) for c in col)  # shaded side of frame

    # ── Chain stay: rear axle → bottom bracket ────────────────────────────────
    HL(d, rw, bb_x, wy - 1, C['chain'])
    # thin frame lines alongside chain stay
    line(d, rw, wy - 2, bb_x, wy - 2, dark)

    # ── Seat tube (vertical) ──────────────────────────────────────────────────
    VL(d, seat_x, seat_top, bb_y, col)
    VL(d, seat_x + 1, seat_top, bb_y, dark)  # shaded edge

    if style == 'step_through':
        # Low, curved top tube — two low horizontal sections
        step_y = wy - r - 3
        HL(d, rw + 1, seat_x, step_y, col)
        HL(d, seat_x, fw - 2, step_y - 2, col)
        # second step-through tube lower
        HL(d, rw + 1, seat_x, step_y + 2, dark)

    elif style == 'cargo':
        # Extended front section + top tube high
        top_y = seat_top
        HL(d, seat_x, fw - 2, top_y, col)   # top tube (long)
        # down tube: diagonal from head tube to bb
        line(d, fw - 2, top_y + 1, bb_x, bb_y - 1, col)
        # extra lower cargo rail from bb forward to fw+6
        HL(d, bb_x, fw + 4, bb_y - 1, col)
        HL(d, bb_x, fw + 4, bb_y,     dark)
        # rear stay diagonal
        line(d, rw + 1, wy - 2, seat_x, seat_top + 1, col)

    elif style == 'bmx':
        # Short top tube, raised head tube
        top_y = wy - r - 6
        HL(d, seat_x, fw - 2, top_y, col)
        line(d, seat_x, top_y + 1, bb_x, bb_y - 1, col)
        line(d, rw + 1, wy - 2, seat_x, seat_top + 1, col)

    else:
        # Standard diamond frame (road/city/mountain/fixie/ebike)
        top_y = seat_top
        # Top tube
        HL(d, seat_x, fw - 2, top_y, col)
        # Down tube: diagonal from head tube crown to bb
        line(d, fw - 2, top_y + 2, bb_x, bb_y - 1, col)
        # Seat stay: rear axle → seat tube top
        line(d, rw + 1, wy - 2, seat_x, seat_top + 2, col)

    # ── Fork ──────────────────────────────────────────────────────────────────
    # Fork blades from crown (just below head tube) to front axle
    crown_y = seat_top + 2 if style not in ('step_through', 'bmx') else wy - r - 3
    line(d, fw - 2, crown_y, fw, wy - 1, col)
    line(d, fw - 1, crown_y, fw + 1, wy - 1, col)

    # ── Saddle ────────────────────────────────────────────────────────────────
    saddle_y = seat_top - 1
    saddle_x0 = seat_x - 2
    saddle_x1 = seat_x + 3
    HL(d, saddle_x0, saddle_x1, saddle_y,     C['saddle'])
    HL(d, saddle_x0 + 1, saddle_x1 - 1, saddle_y - 1, C['saddle_hi'])  # highlight

    # ── Handlebars ────────────────────────────────────────────────────────────
    hbar_x = fw - 1
    hbar_top = top_y if style not in ('step_through',) else wy - r - 4

    if style == 'road':
        # Drop bars: curved down
        VL(d, hbar_x, hbar_top - 2, hbar_top + 2, col)
        PX(d, hbar_x - 1, hbar_top + 2, col)   # drop curve
        PX(d, hbar_x + 1, hbar_top - 2, col)
    elif style in ('bmx',):
        # Wide, raised BMX bars
        VL(d, hbar_x, hbar_top - 3, hbar_top + 1, col)
        HL(d, hbar_x - 3, hbar_x + 3, hbar_top - 3, col)
    elif style == 'mountain':
        # Wide flat bars
        VL(d, hbar_x, hbar_top - 2, hbar_top + 1, col)
        HL(d, hbar_x - 3, hbar_x + 2, hbar_top - 2, col)
    else:
        # Flat city / upright bars
        VL(d, hbar_x, hbar_top - 2, hbar_top + 1, col)
        PX(d, hbar_x + 1, hbar_top - 2, col)
        PX(d, hbar_x - 1, hbar_top - 2, col)

    # ── E-bike battery ────────────────────────────────────────────────────────
    if style == 'ebike':
        bat_x = seat_x + 1
        bat_y = wy - r - 4
        R(d, bat_x, bat_y, bat_x + 3, bat_y + 5, C['black'])
        R(d, bat_x + 1, bat_y + 1, bat_x + 2, bat_y + 4, (0x00, 0xCC, 0x44))
        PX(d, bat_x + 1, bat_y - 1, C['silver'])  # terminal

    # Return key geometry
    return seat_x, seat_top, bb_x, bb_y

# ── Rider ─────────────────────────────────────────────────────────────────────

def draw_rider(d, rw, fw, wy, r, lean_fwd, body_col, head_col, skin_col, accessory):
    """
    Draw a seated cyclist rider.
    lean_fwd: 0 = upright, 1 = fully leaned forward
    accessory: None, 'helmet', 'hijab', 'cap', 'hat'
    """
    seat_x = rw + (fw - rw) // 3
    seat_top = wy - r - 8         # where saddle is
    rider_seat_y = seat_top - 1   # rider pelvis

    # Legs: crank at bb_x
    bb_x = (rw + fw) // 2
    # Left leg (down stroke) — extends toward rear axle level
    leg_down_x = seat_x - 1
    leg_down_y = wy - r - 2
    line(d, seat_x, rider_seat_y + 2, leg_down_x, leg_down_y, skin_col)
    # Shoe left
    R(d, leg_down_x - 1, leg_down_y, leg_down_x + 2, leg_down_y + 1, C['black'])

    # Right leg (up stroke) — knee raised
    leg_up_x = seat_x + 1
    leg_up_y = rider_seat_y + 2
    line(d, seat_x, rider_seat_y + 2, bb_x, leg_up_y - 1, skin_col)
    PX(d, bb_x, leg_up_y - 2, skin_col)
    # Shoe right
    R(d, bb_x - 1, leg_up_y - 1, bb_x + 2, leg_up_y, C['black'])

    if lean_fwd == 0:
        # Upright torso
        torso_top = rider_seat_y - 7
        torso_bot = rider_seat_y + 1
        R(d, seat_x - 1, torso_top, seat_x + 3, torso_bot, body_col)
        # Collar / highlight
        HL(d, seat_x - 1, seat_x + 2, torso_top, C['lgray'])
        # Head position
        head_y = torso_top - 3
        head_x = seat_x
        # Arms: from shoulder to handlebars (mostly horizontal)
        arm_y = torso_top + 2
        hbar_x = fw - 1
        hbar_top = wy - r - 8
        line(d, seat_x + 2, arm_y, hbar_x, hbar_top, skin_col)

    else:
        # Leaned forward torso (diagonal)
        lean = int(lean_fwd * 4)  # how many px forward
        torso_top_y = rider_seat_y - 5
        torso_top_x = seat_x + lean
        R(d, seat_x - 1, rider_seat_y - 1, seat_x + 3, rider_seat_y + 1, body_col)
        line(d, seat_x + 1, rider_seat_y, torso_top_x, torso_top_y, body_col)
        line(d, seat_x + 2, rider_seat_y, torso_top_x + 1, torso_top_y, body_col)
        line(d, seat_x,     rider_seat_y + 1, torso_top_x - 1, torso_top_y + 1, body_col)
        head_y = torso_top_y - 3
        head_x = torso_top_x + 1
        # Arms reaching to drop bars
        hbar_x = fw - 1
        hbar_top = wy - r - 8
        line(d, torso_top_x + 2, torso_top_y + 1, hbar_x, hbar_top + 2, skin_col)

    # Head (3×3 game-px skin)
    R(d, head_x, head_y, head_x + 3, head_y + 3, skin_col)
    # Eyes (2 px)
    PX(d, head_x + 1, head_y + 1, C['black'])
    PX(d, head_x + 2, head_y + 1, C['black'])

    # ── Accessories ───────────────────────────────────────────────────────────
    if accessory == 'helmet':
        # Rounded helmet: wider than head, darker tone + stripe
        R(d, head_x - 1, head_y - 2, head_x + 4, head_y + 1, head_col)
        # vent stripe highlight
        HL(d, head_x, head_x + 2, head_y - 2, C['lgray'])
        # chin strap
        PX(d, head_x, head_y + 2, C['lgray'])
        PX(d, head_x + 3, head_y + 2, C['lgray'])

    elif accessory == 'hijab':
        # Larger head covering + cloth flowing back
        R(d, head_x - 1, head_y - 1, head_x + 4, head_y + 3, head_col)
        # Cloth drape behind head
        R(d, head_x - 2, head_y + 1, head_x + 1, head_y + 5, head_col)
        # Under-chin wrap
        HL(d, head_x - 1, head_x + 3, head_y + 2, head_col)

    elif accessory == 'cap':
        # Flat cap: rectangle + brim
        R(d, head_x, head_y - 1, head_x + 3, head_y + 1, head_col)
        PX(d, head_x + 3, head_y, head_col)   # brim
        PX(d, head_x - 1, head_y, C['black']) # shadow under brim

    elif accessory == 'hat':
        # Classic hat: crown + brim
        R(d, head_x, head_y - 2, head_x + 3, head_y,     head_col)  # crown
        HL(d, head_x - 1, head_x + 3, head_y,             head_col)  # brim
        PX(d, head_x, head_y - 2, C['lgray'])  # highlight

    elif accessory == 'cap_sideways':
        # Sideways cap (BMX style)
        R(d, head_x - 1, head_y - 1, head_x + 3, head_y + 1, head_col)
        PX(d, head_x - 2, head_y, head_col)  # brim left

# ── Individual biker draw functions ──────────────────────────────────────────

def draw_biker(d, biker_spec):
    """
    Universal biker draw function.
    biker_spec dict keys:
      rw, fw, wy, r          — wheel geometry
      frame_col, style       — frame colour + style string
      tyre_col, rim_col      — wheel colours
      lean_fwd               — 0 = upright, 1 = fully forward
      body_col, head_col     — clothing / accessory colours
      skin_col               — rider skin tone
      accessory              — None/'helmet'/'hijab'/'cap'/'hat'/'cap_sideways'
      extras                 — list of callables: extra(d) for attachments
    """
    spec = biker_spec

    rw   = spec['rw']
    fw   = spec['fw']
    wy   = spec['wy']
    r    = spec['r']

    # Rear wheel
    wheel(d, rw, wy, r,
          tyre_col=spec.get('tyre_col', C['rubber']),
          rim_col=spec.get('rim_col', C['rim']),
          n_spokes=spec.get('n_spokes', 8))

    # Frame
    draw_frame(d, rw, fw, wy, r,
               col=spec['frame_col'],
               style=spec.get('style', 'road'))

    # Front wheel (drawn after frame so fork overlaps)
    wheel(d, fw, wy, r,
          tyre_col=spec.get('tyre_col', C['rubber']),
          rim_col=spec.get('rim_col', C['rim']),
          n_spokes=spec.get('n_spokes', 8))

    # Rider
    draw_rider(d, rw, fw, wy, r,
               lean_fwd=spec.get('lean_fwd', 0),
               body_col=spec['body_col'],
               head_col=spec['head_col'],
               skin_col=spec['skin_col'],
               accessory=spec.get('accessory', None))

    # Extras (attachments, baskets, cargo, fenders…)
    for extra_fn in spec.get('extras', []):
        extra_fn(d, rw, fw, wy, r, spec)


# ── Attachment helpers ────────────────────────────────────────────────────────

def attach_front_basket(d, rw, fw, wy, r, spec):
    """Wicker basket on front fork."""
    bx0 = fw - 1
    bx1 = fw + 4
    by0 = wy - r - 3
    by1 = wy - r + 1
    R(d, bx0, by0, bx1, by1, C['basket'])
    # Weave lines
    HL(d, bx0, bx1, by0,     C['basket_dk'])
    HL(d, bx0, bx1, by0 + 2, C['basket_dk'])
    VL(d, bx0 + 1, by0, by1, C['basket_dk'])
    VL(d, bx0 + 3, by0, by1, C['basket_dk'])

def attach_front_basket_flowers(d, rw, fw, wy, r, spec):
    """Wicker basket + flower dots."""
    attach_front_basket(d, rw, fw, wy, r, spec)
    bx0 = fw - 1
    by0 = wy - r - 3
    PX(d, bx0 + 1, by0 - 1, C['pink'])
    PX(d, bx0 + 2, by0 - 1, C['yellow'])
    PX(d, bx0 + 3, by0 - 1, C['pink'])

def attach_rear_pannier(d, rw, fw, wy, r, spec):
    """Single rear pannier bag."""
    px0 = rw - 3
    px1 = rw + 1
    py0 = wy - r + 1
    py1 = wy + 2
    R(d, px0, py0, px1, py1, C['dgray'])
    HL(d, px0, px1, py0, C['gray'])
    PX(d, px0 + 1, py0 + 1, C['lgray'])  # buckle

def attach_panniers_both(d, rw, fw, wy, r, spec):
    """Large panniers both sides (delivery)."""
    attach_rear_pannier(d, rw, fw, wy, r, spec)
    # Second pannier stacked
    px0 = rw - 3
    R(d, px0, wy - r - 1, rw + 1, wy - r + 2, C['green_dk'])
    HL(d, px0, rw + 1, wy - r - 1, C['green'])

def attach_cargo_box(d, rw, fw, wy, r, spec):
    """Cargo/bakfiets box at front."""
    bx0 = fw - 8
    bx1 = fw - 1
    by0 = wy - r - 3
    by1 = wy - r + 2
    R(d, bx0, by0, bx1, by1, C['box_wood'])
    # Box edges
    HL(d, bx0, bx1, by0,     C['box_dark'])
    HL(d, bx0, bx1, by1 - 1, C['box_dark'])
    VL(d, bx0, by0, by1,     C['box_dark'])
    VL(d, bx1 - 1, by0, by1, C['box_dark'])
    # Handle
    HL(d, bx0 + 2, bx1 - 2, by0 - 1, C['brown'])
    PX(d, bx0 + 2, by0 - 1, C['brown'])
    PX(d, bx1 - 2, by0 - 1, C['brown'])

def attach_child_seat(d, rw, fw, wy, r, spec):
    """Child seat on rear rack + tiny passenger silhouette."""
    # Seat
    cx0 = rw - 4
    cx1 = rw
    cy0 = wy - r - 6
    cy1 = wy - r - 1
    R(d, cx0, cy0, cx1, cy1, C['blue'])
    HL(d, cx0, cx1, cy0, C['lgray'])
    # Child silhouette (tiny)
    child_x = rw - 2
    child_y = cy0 - 4
    R(d, child_x, child_y, child_x + 2, child_y + 3, C['yellow'])   # body
    R(d, child_x, child_y - 2, child_x + 2, child_y,   C['skin_l']) # head

def attach_dutch_fenders(d, rw, fw, wy, r, spec):
    """Full fenders arcing over both wheels."""
    fender_col = spec.get('fender_col', C['beige'])
    # Rear fender arc
    circle_outline(d, rw, wy, r + 1, fender_col, thickness=1)
    # Front fender arc
    circle_outline(d, fw, wy, r + 1, fender_col, thickness=1)
    # Fender stays (small lines)
    VL(d, rw + r + 1, wy - 2, wy + 2, fender_col)
    VL(d, fw + r + 1, wy - 2, wy + 2, fender_col)

def attach_chain_guard(d, rw, fw, wy, r, spec):
    """Chain guard rectangle from rear axle to bb."""
    bb_x = (rw + fw) // 2
    R(d, rw, wy - 2, bb_x + 2, wy, C['cream'])
    HL(d, rw, bb_x + 2, wy - 2, C['beige'])

def attach_hiviz_vest(d, rw, fw, wy, r, spec):
    """Hi-viz yellow vest overlay on rider torso."""
    seat_x = rw + (fw - rw) // 3
    seat_top = wy - r - 8
    torso_top = seat_top - 7
    R(d, seat_x - 1, torso_top + 1, seat_x + 3, torso_top + 6, C['hiviz'])
    HL(d, seat_x, seat_x + 2, torso_top + 2, C['yellow'])  # reflective stripe

def attach_long_skirt(d, rw, fw, wy, r, spec):
    """Long skirt overlay over legs."""
    seat_x = rw + (fw - rw) // 3
    skirt_col = spec.get('skirt_col', C['teal'])
    seat_top = wy - r - 8
    R(d, seat_x - 2, seat_top - 2, seat_x + 3, wy - r, skirt_col)


# ── 16 BIKERS list ────────────────────────────────────────────────────────────
# All bikes fit in 36×30 game-px.
# Standard geometry: rw=8, fw=28, wy=22, r=5 (leaves 3px headroom, 3px ground)

def make_bikers():
    RW, FW_B, WY, R_STD = 8, 28, 22, 5

    def spec(overrides):
        base = dict(rw=RW, fw=FW_B, wy=WY, r=R_STD,
                    tyre_col=C['rubber'], rim_col=C['rim'],
                    n_spokes=8, lean_fwd=0, extras=[])
        base.update(overrides)
        return base

    bikers = [
        # 0 — racing_red
        spec(dict(
            frame_col=C['red'], style='road',
            rim_col=(0xDD, 0x33, 0x33),
            lean_fwd=1,
            body_col=C['red'], head_col=C['red'],
            skin_col=C['skin_m'],
            accessory='helmet',
            # Lycra white stripe drawn in extras
        )),
        # 1 — racing_blue
        spec(dict(
            frame_col=C['blue'], style='road',
            rim_col=(0x33, 0x44, 0xDD),
            lean_fwd=1,
            body_col=C['blue'], head_col=C['blue'],
            skin_col=C['skin_l'],
            accessory='helmet',
        )),
        # 2 — city_blue (teal, basket front)
        spec(dict(
            frame_col=C['teal'], style='city',
            lean_fwd=0,
            body_col=C['blue'], head_col=C['lgray'],
            skin_col=C['skin_l'],
            accessory=None,
            extras=[attach_front_basket],
        )),
        # 3 — city_red (pannier rear, cap)
        spec(dict(
            frame_col=C['red'], style='city',
            lean_fwd=0,
            body_col=C['jacket_br'], head_col=C['brown'],
            skin_col=C['skin_m'],
            accessory='cap',
            extras=[attach_rear_pannier],
        )),
        # 4 — ebike_gray
        spec(dict(
            frame_col=C['mgray'], style='ebike',
            lean_fwd=0,
            body_col=C['navy'], head_col=C['gray'],
            skin_col=C['skin_m'],
            accessory=None,
        )),
        # 5 — mountain_green
        spec(dict(
            frame_col=C['green_dk'], style='mountain',
            tyre_col=(0x1A, 0x1A, 0x1A),  # slightly knobbly look (dark)
            lean_fwd=0,
            body_col=C['green'], head_col=C['green'],
            skin_col=C['skin_d'],
            accessory='helmet',
        )),
        # 6 — mountain_orange
        spec(dict(
            frame_col=C['orange'], style='mountain',
            tyre_col=(0x1A, 0x1A, 0x1A),
            lean_fwd=0,
            body_col=C['orange_dk'], head_col=C['orange'],
            skin_col=C['skin_l'],
            accessory='helmet',
        )),
        # 7 — cargo_yellow (bakfiets)
        spec(dict(
            rw=10, fw=30, wy=WY, r=R_STD,
            frame_col=C['yellow'], style='cargo',
            lean_fwd=0,
            body_col=C['orange'], head_col=C['orange'],
            skin_col=C['skin_m'],
            accessory=None,
            extras=[attach_cargo_box],
        )),
        # 8 — cargo_child (child seat on rear)
        spec(dict(
            frame_col=C['blue'], style='city',
            lean_fwd=0,
            body_col=(0x55, 0x66, 0xAA), head_col=C['gray'],
            skin_col=C['skin_l'],
            accessory=None,
            extras=[attach_child_seat],
        )),
        # 9 — delivery_green (panniers + hiviz)
        spec(dict(
            frame_col=C['green_dk'], style='city',
            lean_fwd=0,
            body_col=C['hiviz'], head_col=C['lgray'],
            skin_col=C['skin_dk'],
            accessory='helmet',
            extras=[attach_panniers_both, attach_hiviz_vest],
        )),
        # 10 — grandma_blue (step-through, flowers, hat)
        spec(dict(
            frame_col=(0x88, 0xAA, 0xCC), style='step_through',
            lean_fwd=0,
            body_col=C['purple'], head_col=C['dgray'],
            skin_col=C['skin_l'],
            accessory='hat',
            extras=[attach_front_basket_flowers],
        )),
        # 11 — hijab_teal
        spec(dict(
            frame_col=C['teal'], style='step_through',
            lean_fwd=0,
            body_col=C['teal_dark'], head_col=C['hijab_t'],
            skin_col=C['skin_m'],
            accessory='hijab',
            skirt_col=C['teal'],
            extras=[attach_long_skirt],
        )),
        # 12 — hijab_purple
        spec(dict(
            frame_col=C['purple'], style='step_through',
            lean_fwd=0,
            body_col=C['purple_dk'], head_col=C['hijab_p'],
            skin_col=C['skin_m'],
            accessory='hijab',
            skirt_col=C['purple'],
            extras=[attach_long_skirt],
        )),
        # 13 — fixie_black
        spec(dict(
            frame_col=C['black'], style='fixie',
            rim_col=C['red'],   # coloured rim
            lean_fwd=0,
            body_col=C['red'], head_col=C['black'],
            skin_col=C['skin_l'],
            accessory='cap',
        )),
        # 14 — dutch_beige (fenders, chain guard, basket, hat)
        spec(dict(
            frame_col=C['beige'], style='city',
            lean_fwd=0,
            body_col=C['jacket_br'], head_col=C['dgray'],
            skin_col=C['skin_l'],
            accessory='hat',
            fender_col=C['beige'],
            extras=[attach_dutch_fenders, attach_chain_guard, attach_front_basket_flowers],
        )),
        # 15 — bmx_red (small wheels, upright, cap sideways)
        spec(dict(
            rw=9, fw=25, wy=22, r=4,
            frame_col=C['red'], style='bmx',
            lean_fwd=0,
            body_col=C['black'], head_col=C['red'],
            skin_col=C['skin_m'],
            accessory='cap_sideways',
        )),
    ]
    return bikers

BIKER_NAMES = [
    'racing_red',
    'racing_blue',
    'city_blue',
    'city_red',
    'ebike_gray',
    'mountain_green',
    'mountain_orange',
    'cargo_yellow',
    'cargo_child',
    'delivery_green',
    'grandma_blue',
    'hijab_teal',
    'hijab_purple',
    'fixie_black',
    'dutch_beige',
    'bmx_red',
]

# ── Main ──────────────────────────────────────────────────────────────────────

print('=' * 60)
print('Turnhoutsebaan Bike Sprite Generator v2')
print(f'  Frame: {FW}x{FH} game px | SCALE={SCALE} | {PW}x{PH} px per frame')
print(f'  Sheet: {N_TYPES * PW}x{PH} px  ({N_TYPES} types)')
print('=' * 60)

BIKERS = make_bikers()
assert len(BIKERS) == N_TYPES, f"Expected {N_TYPES} bikers, got {len(BIKERS)}"

sheet = Image.new('RGBA', (N_TYPES * PW, PH), (0, 0, 0, 0))

for i, (name, spec) in enumerate(zip(BIKER_NAMES, BIKERS)):
    frame = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    draw_biker(d, spec)
    sheet.paste(frame, (i * PW, 0))
    out_path = os.path.join(OUT_DIR, f'bike_{i:02d}_{name}.png')
    frame.save(out_path)
    print(f'  [{i:02d}] {name} → {PW}x{PH} px')

sheet.save(OUT_FILE)
print()
print(f'Saved spritesheet: {N_TYPES * PW}x{PH} px')
print(f'  → {OUT_FILE}')
print(f'  → {N_TYPES} individual frames in {OUT_DIR}')
