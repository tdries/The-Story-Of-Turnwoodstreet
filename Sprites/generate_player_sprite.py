#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — Player Character Sprite
============================================
Young Moroccan boy on a city bicycle — the main player character.

Frame layout (64×64 game pixels each, 5 frames):
  0 — Idle right        (neutral pedal, facing right)
  1 — Pedal A right     (right foot pushing down)
  2 — Pedal B right     (left foot pushing down)
  3 — Walk up           (back view: boy visible, bike partially)
  4 — Walk down         (front view: boy faces camera)

Left-facing: use Phaser flipX on frames 0–2 (no separate frames needed).
Sheet: 320 × 64 game pixels → PNG at out_scale=10 = 3200 × 640 px
All drawing functions use internal 32×32 coordinates; a local p() helper
doubles every coordinate and size to fill the 64×64 canvas (4× pixel area).
"""

import os
import sys
import math

sys.path.insert(0, os.path.dirname(__file__))
from generate_sprites import SVGSheet, PAL

# ── Config ────────────────────────────────────────────────────────────────────
FW, FH = 32, 32          # frame dimensions (game pixels)
NUM_FRAMES = 5
SHEET_W = FW * NUM_FRAMES   # 160
SHEET_H = FH               # 32

# ── Colour shortcuts for this sprite ─────────────────────────────────────────
SKIN_MID   = "cream_dark"    # medium-brown Moroccan skin
SKIN_LIGHT = "cream_mid"     # highlights on skin
SKIN_SHD   = "ochre"         # shadow areas
HAIR       = "black"         # dark curly hair
JACKET     = "white"         # white hoodie
HOOD       = "de_lijn_blue"  # blue hood accent
PANTS      = "stone_dark"    # dark jeans
SHOE       = "white"         # white Nike / Adidas
SHOE_STR   = "de_lijn_blue"  # shoe stripe
BIKE_FRAME = "stone_dark"    # dark grey frame
BIKE_SHD   = "night"         # frame shadow side
TIRE       = "asphalt_dark"  # black tyre
RIM        = "stone_light"   # chrome wheel rim
SPOKE      = "stone_mid"     # spokes
CHAIN      = "asphalt_mid"   # chain/crank

# Wheel geometry in 32-px internal space (doubled by p() helper at draw time)
WBX, WFX, WY, WR = 7, 25, 24, 5


# ── Right-facing frame (idle / pedal A / pedal B) ─────────────────────────────

def draw_frame_right(s: SVGSheet, ox: int, oy: int, phase: int = 0):
    """
    Assemble a right-facing riding frame at 4× pixel area.
    All coordinates are in the 32-px internal space; p() doubles them
    to fill the 64×64 canvas.
    """
    # ── Local helpers ─────────────────────────────────────────────────────────
    def p(x, y, color, w=1, h=1):
        s.put(ox + x, oy + y, color, w, h)

    def line(x1, y1, x2, y2, color, t=1):
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy), 1)
        for i in range(steps + 1):
            x = round(x1 + dx * i / steps)
            y = round(y1 + dy * i / steps)
            p(x, y, color, t, t)

    def wheel(cx, cy):
        r = WR
        for dy2 in range(-r, r + 1):
            for dx2 in range(-r, r + 1):
                if dx2 * dx2 + dy2 * dy2 <= r * r:
                    p(cx + dx2, cy + dy2, TIRE)
        for dy2 in range(-r, r + 1):
            for dx2 in range(-r, r + 1):
                d2 = dx2 * dx2 + dy2 * dy2
                if (r - 1) ** 2 <= d2 <= r * r:
                    p(cx + dx2, cy + dy2, RIM)
        for i in range(-r + 2, r - 1):
            p(cx + i, cy,     SPOKE)
            p(cx,     cy + i, SPOKE)
        p(cx - 1, cy - 1, RIM, 2, 2)

    # ── Wheels ────────────────────────────────────────────────────────────────
    wheel(WBX, WY)
    wheel(WFX, WY)

    # ── Bike frame ────────────────────────────────────────────────────────────
    bx, fx   = WBX, WFX
    ay       = WY
    bb_x, bb_y = 16, 21
    st_x, st_y = 13, 13

    line(bx, ay, bb_x, bb_y, BIKE_FRAME)          # chain stay
    line(bx, ay, st_x, st_y, BIKE_FRAME)          # seat stay
    p(st_x, st_y, BIKE_FRAME, 1, bb_y - st_y + 1) # seat tube
    p(st_x, st_y, BIKE_FRAME, fx - st_x, 1)       # top tube
    line(fx, st_y, bb_x, bb_y, BIKE_FRAME)        # down tube
    line(fx, st_y, fx,   ay,   BIKE_FRAME)        # front fork
    line(bx + 1, ay, bb_x + 1, bb_y, BIKE_SHD)   # chain-stay shadow
    line(st_x + 1, st_y, bb_x + 1, bb_y, BIKE_SHD) # down-tube shadow

    # Seat
    p(st_x - 3, st_y - 1, BIKE_FRAME, 8, 1)
    p(st_x - 2, st_y - 2, BIKE_SHD,   6, 1)
    p(st_x - 3, st_y - 2, RIM,        1, 1)

    # Handlebar
    p(fx,     st_y,     BIKE_FRAME, 1, 4)
    p(fx - 1, st_y + 1, BIKE_FRAME, 3, 1)
    p(fx - 1, st_y,     RIM,        1, 1)
    p(fx + 1, st_y,     RIM,        1, 1)

    # Bottom bracket
    p(bb_x, bb_y, CHAIN, 2, 2)

    # ── Boy ───────────────────────────────────────────────────────────────────
    # Head
    p(11, 1,  HAIR,       8, 1)   # crown
    p(10, 2,  HAIR,      10, 2)   # bulk hair
    p(10, 3,  HAIR,       2, 4)   # left sideburn
    p(18, 3,  HAIR,       2, 4)   # right sideburn
    p(12, 3,  SKIN_MID,   6, 5)   # face centre
    p(11, 4,  SKIN_MID,   1, 3)   # left cheek edge
    p(18, 4,  SKIN_MID,   1, 3)   # right cheek edge
    p(16, 5,  HAIR,       1, 1)   # eye
    p(15, 4,  HAIR,       2, 1)   # eyebrow
    p(13, 7,  SKIN_SHD,   4, 1)   # mouth
    p(18, 5,  SKIN_LIGHT, 1, 2)   # ear
    p(12, 3,  SKIN_LIGHT, 2, 1)   # forehead highlight

    # Torso
    p(10, 8,  HOOD,   9, 2)   # hood/collar
    p(10, 10, JACKET, 9, 5)   # jacket front panel
    p( 9,  9, JACKET, 1, 5)   # left sleeve
    p(19,  9, JACKET, 1, 5)   # right sleeve
    p(20, 12, SKIN_MID, 4, 2) # right forearm/hand
    p( 8, 11, JACKET, 2, 4)   # left arm
    p( 8, 15, SKIN_MID, 2, 2) # left hand
    p(10, 10, "cloud", 4, 1)  # NW jacket highlight
    p(10, 10, "cloud", 1, 4)

    # Legs (pedaling)
    cx, cy = 16, 21
    if phase == 0:
        # Right foot down
        p(14, 14, PANTS,    4, 5)
        p(16, 19, PANTS,    3, 4)
        p(16, 22, SHOE,     4, 2)
        p(17, 22, SHOE_STR, 2, 1)
        line(cx, cy, cx + 2, cy + 2, RIM)
        p(cx + 2, cy + 2, RIM, 2, 1)
        # Left foot up (shadowed)
        p(11, 14, BIKE_SHD, 3, 4)
        p(12, 18, BIKE_SHD, 2, 2)
        p(11, 18, SHOE,     2, 2)
        line(cx, cy, cx - 2, cy - 2, RIM)
        p(cx - 3, cy - 2, RIM, 2, 1)
    else:
        # Left foot down
        p(13, 14, PANTS,    4, 5)
        p(13, 19, PANTS,    3, 4)
        p(13, 22, SHOE,     4, 2)
        p(14, 22, SHOE_STR, 2, 1)
        line(cx, cy, cx - 2, cy + 2, RIM)
        p(cx - 3, cy + 2, RIM, 2, 1)
        # Right foot up
        p(14, 14, BIKE_SHD, 3, 4)
        p(15, 18, BIKE_SHD, 2, 2)
        p(16, 18, SHOE,     2, 2)
        line(cx, cy, cx + 2, cy - 2, RIM)
        p(cx + 2, cy - 2, RIM, 2, 1)


# ── Back view (moving up the screen) ─────────────────────────────────────────

def draw_frame_back(s: SVGSheet, ox: int, oy: int, step: int = 0):
    """Back view: boy from behind, pushing bike up the screen."""
    def p(x, y, color, w=1, h=1):
        s.put(ox + x, oy + y, color, w, h)

    def line(x1, y1, x2, y2, color, t=1):
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy), 1)
        for i in range(steps + 1):
            x = round(x1 + dx * i / steps)
            y = round(y1 + dy * i / steps)
            p(x, y, color, t, t)

    leg_phase = step

    # Rear wheel edge-on (centre-bottom)
    p(13, 19, TIRE,  6, 12)
    p(13, 19, RIM,   6,  1)
    p(13, 30, RIM,   6,  1)
    p(14, 24, SPOKE, 4,  1)
    p(14, 25, RIM,   4,  2)

    # Frame structure
    p(15, 14, BIKE_FRAME, 2, 8)   # seat tube
    p(16, 14, BIKE_SHD,   1, 8)
    line(14, 21, 13, 25, BIKE_FRAME)  # chain-stay L
    line(18, 21, 19, 25, BIKE_FRAME)  # chain-stay R

    # Saddle (wide, from rear)
    p(10, 13, BIKE_SHD,   12, 2)
    p( 9, 13, BIKE_FRAME,  1, 2)
    p(22, 13, BIKE_FRAME,  1, 2)
    p(10, 12, RIM,         5, 1)

    # Handlebar
    p( 3, 12, BIKE_FRAME, 26, 1)
    p( 3, 11, BIKE_SHD,   26, 1)
    p( 2, 11, RIM, 3, 3)
    p(27, 11, RIM, 3, 3)
    p( 3, 10, BIKE_FRAME, 2, 1)
    p(28, 10, BIKE_FRAME, 2, 1)

    # Head (back)
    p(11,  1, HAIR, 10, 2)
    p(10,  3, HAIR, 12, 3)
    p(10,  6, HAIR, 12, 2)

    # Neck
    p(13, 8, SKIN_MID, 6, 2)

    # Jacket back
    p( 9,  8, HOOD,    14, 2)
    p( 9, 10, JACKET,  14, 4)
    p( 9, 10, "cloud",  4, 1)
    p( 9, 10, "cloud",  1, 3)
    p( 5, 10, JACKET,   5, 3)   # left sleeve
    p(22, 10, JACKET,   5, 3)   # right sleeve
    p( 3, 12, SKIN_MID, 2, 2)   # left hand
    p(27, 12, SKIN_MID, 2, 2)   # right hand

    # Hips
    p(11, 14, PANTS, 10, 4)

    if leg_phase == 0:
        p(11, 18, PANTS,    4, 7)
        p(10, 25, SHOE,     6, 2)
        p(11, 25, SHOE_STR, 4, 1)
        p(17, 18, PANTS,    4, 5)
        p(17, 23, SHOE,     6, 2)
    else:
        p(17, 18, PANTS,    4, 7)
        p(17, 25, SHOE,     6, 2)
        p(18, 25, SHOE_STR, 4, 1)
        p(11, 18, PANTS,    4, 5)
        p(11, 23, SHOE,     6, 2)


# ── Front view (moving down the screen) ──────────────────────────────────────

def draw_frame_front(s: SVGSheet, ox: int, oy: int, step: int = 0):
    """Front view: boy faces the camera, riding towards the player."""
    def p(x, y, color, w=1, h=1):
        s.put(ox + x, oy + y, color, w, h)

    def line(x1, y1, x2, y2, color, t=1):
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy), 1)
        for i in range(steps + 1):
            x = round(x1 + dx * i / steps)
            y = round(y1 + dy * i / steps)
            p(x, y, color, t, t)

    leg_phase = step

    # Front wheel (edge-on, centre-bottom)
    p(13, 21, TIRE,  6, 10)
    p(13, 21, RIM,   6,  1)
    p(13, 30, RIM,   6,  1)
    p(14, 25, SPOKE, 4,  1)
    p(14, 26, RIM,   4,  2)

    # Front fork
    line(13, 15, 13, 21, BIKE_FRAME)
    line(18, 15, 18, 21, BIKE_FRAME)
    p(13, 14, BIKE_FRAME, 6, 2)   # fork crown
    p(14, 11, BIKE_FRAME, 4, 4)   # stem
    p(15, 11, BIKE_SHD,   2, 4)

    # Handlebar
    p( 3, 12, BIKE_FRAME, 26, 1)
    p( 3, 11, BIKE_SHD,   26, 1)
    p( 2, 11, RIM, 3, 3)
    p(27, 11, RIM, 3, 3)
    p( 3, 10, BIKE_FRAME, 2, 1)
    p(28, 10, BIKE_FRAME, 2, 1)

    # Head
    p(11,  1, HAIR,       10, 2)
    p(10,  3, HAIR,       12, 3)
    p(10,  3, HAIR,        2, 5)
    p(20,  3, HAIR,        2, 5)
    p(12,  3, SKIN_MID,    8, 6)
    p(12,  3, SKIN_LIGHT,  4, 1)
    p(13,  5, HAIR,        2, 1)   # left eye
    p(17,  5, HAIR,        2, 1)   # right eye
    p(13,  4, HAIR,        2, 1)   # left brow
    p(17,  4, HAIR,        2, 1)   # right brow
    p(15,  7, SKIN_SHD,    2, 1)   # nose
    p(13,  8, SKIN_SHD,    5, 1)   # smile
    p(11,  5, SKIN_LIGHT,  1, 2)   # left ear
    p(20,  5, SKIN_LIGHT,  1, 2)   # right ear

    # Jacket front
    p( 9,  8, HOOD,    14, 2)
    p(10, 10, JACKET,  12, 5)
    p(10, 10, "cloud",  4, 1)
    p(10, 10, "cloud",  1, 3)
    p(15, 10, BIKE_SHD, 2, 5)   # zip
    p( 5, 10, JACKET,   5, 3)
    p(22, 10, JACKET,   5, 3)
    p( 3, 12, SKIN_MID, 2, 2)
    p(27, 12, SKIN_MID, 2, 2)

    # Hips
    p(11, 15, PANTS, 10, 4)

    if leg_phase == 0:
        p( 8, 19, PANTS,    4, 6)
        p( 7, 25, SHOE,     6, 2)
        p( 8, 25, SHOE_STR, 4, 1)
        p(20, 19, PANTS,    4, 4)
        p(20, 23, SHOE,     6, 2)
    else:
        p(20, 19, PANTS,    4, 6)
        p(20, 25, SHOE,     6, 2)
        p(21, 25, SHOE_STR, 4, 1)
        p( 8, 19, PANTS,    4, 4)
        p( 8, 23, SHOE,     6, 2)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "Sprites", "characters", "player")
    os.makedirs(out_dir, exist_ok=True)

    sheet = SVGSheet(SHEET_W, SHEET_H, "Player — Moroccan Boy on Bicycle")

    # Frame 0 — Idle right
    draw_frame_right(sheet, FW * 0, 0, phase=0)

    # Frame 1 — Pedal A right (right foot down)
    draw_frame_right(sheet, FW * 1, 0, phase=0)

    # Frame 2 — Pedal B right (left foot down)
    draw_frame_right(sheet, FW * 2, 0, phase=1)

    # Frame 3 — Back view
    draw_frame_back(sheet, FW * 3, 0, step=0)

    # Frame 4 — Front view
    draw_frame_front(sheet, FW * 4, 0, step=0)

    svg_path = os.path.join(out_dir, "player_sheet.svg")
    png_path = os.path.join(out_dir, "player_sheet.png")

    sheet.save(svg_path)
    sheet.to_pil(png_path, out_scale=10)

    print("\n✓ Player sprite sheet generated!")
    print(f"  Frames:     {NUM_FRAMES} (idle, pedal_A, pedal_B, back, front)")
    print(f"  Frame size: {FW}×{FH} game pixels  (4× pixel area vs 32×32)")
    print(f"  PNG output: {FW * 10 * NUM_FRAMES}×{FH * 10} px  ({png_path})")


if __name__ == "__main__":
    main()
