#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — NPC Portrait Sprites  (HIGH-DETAIL dedicated art)
=======================================================================
Purpose-built close-up portraits for the dialogue inlay.
Each function is NOT a re-use of the walking-sprite code — it is fully
dedicated portrait art with:
  - 4-tone skin gradients (highlight / base / shadow / deep-shadow)
  - 3-segment brow arches
  - Detailed eyes: whites, iris outer-ring + inner, pupil, sparkle
  - Nose: bridge highlight, ala shadows, distinct nostrils
  - Lips: Cupid's-bow upper, lower lip highlight, philtrum, corner shadows
  - Talking variant: open mouth with teeth
  - Character accessories: glasses, earrings, helmet visor, beard,
    AirPod, oud-peg, scarf, tracksuit logos …

Canvas  : 64×96 game-pixels (SVGSheet at scale=4)
Crop    : game x = 6..58, y = 0..52  →  52×52 game-pixel portrait area
Upscale : NEAREST  →  512×512 px per frame
Sheet   : 1024×512 px  (frame 0 = neutral, frame 1 = talking)
"""

import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from generate_sprites import SVGSheet

try:
    from PIL import Image, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Pillow not installed — run: pip3 install Pillow")

# ── constants ─────────────────────────────────────────────────────────────────

INTERMEDIATE_SCALE = 4
PORTRAIT_PX        = 512

CROP_GX1, CROP_GY1 = 6,  0
CROP_GX2, CROP_GY2 = 58, 52

OUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "assets", "Sprites", "characters", "npcs", "portraits"
)

# Canvas x-offset (crop left edge) — add to all local x-coords
C = 6

# ── SVG → PIL renderer ────────────────────────────────────────────────────────

def render_sheet(sheet: SVGSheet) -> "Image.Image":
    s  = sheet.SCALE
    ow = sheet.w * INTERMEDIATE_SCALE
    oh = sheet.h * INTERMEDIATE_SCALE
    img  = Image.new("RGBA", (ow, oh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r in sheet.rects:
        if not r.startswith('<rect'):
            continue
        m = re.search(
            r'x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="(#[0-9A-Fa-f]{6})"', r
        )
        if not m:
            continue
        x, y, w, h, fill = int(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5]
        gx, gy, gw, gh = x // s, y // s, w // s, h // s
        rv = int(fill[1:3], 16)
        gv = int(fill[3:5], 16)
        bv = int(fill[5:7], 16)
        px1 = max(0, gx * INTERMEDIATE_SCALE)
        py1 = max(0, gy * INTERMEDIATE_SCALE)
        px2 = min(ow - 1, (gx + gw) * INTERMEDIATE_SCALE - 1)
        py2 = min(oh - 1, (gy + gh) * INTERMEDIATE_SCALE - 1)
        if px2 >= px1 and py2 >= py1:
            draw.rectangle([px1, py1, px2, py2], fill=(rv, gv, bv, 255))
    return img


def crop_to_portrait(full_img: "Image.Image") -> "Image.Image":
    px1 = CROP_GX1 * INTERMEDIATE_SCALE
    py1 = CROP_GY1 * INTERMEDIATE_SCALE
    px2 = CROP_GX2 * INTERMEDIATE_SCALE
    py2 = CROP_GY2 * INTERMEDIATE_SCALE
    cropped = full_img.crop((px1, py1, px2, py2))
    return cropped.resize((PORTRAIT_PX, PORTRAIT_PX), Image.NEAREST)


# ── shared portrait helpers ────────────────────────────────────────────────────
#
# All coordinates are CANVAS coordinates (x includes the C=6 offset).
# Portrait face layout (canvas coords):
#   Near eye center : cx = C+31 = 37,  cy = 18
#   Far  eye center : cx = C+15 = 21,  cy = 18
#   Nose bridge top : nx = C+25 = 31,  ny = 22
#   Mouth center    : lx = C+25 = 31,  ly = 33
#   Face block      : y = 5..38,  x = C+8..C+44  (14..50)
#   Neck            : y = 38..46, x = C+18..C+34 (24..40)
#   Collar band     : y = 44..51, full portrait width

def p_bg(s):
    """Dark vignette background."""
    s.put(C,    0, "night",        52, 52)
    s.put(C+6,  3, "asphalt_dark", 40, 42)  # slightly lighter centre


def p_near_eye(s, cx, cy, iris, iris_dk, brow_col, skin_lt, skin_shd):
    """
    High-detail near (right) eye.
    cx, cy = canvas coords of iris centre.
    Eye is ~10 px wide; brow is ~10 px wide above it.
    """
    # ── brow arch (3 segments, tapers outward) ─────────────────────────────
    s.put(cx-6, cy-7, brow_col, 3, 2)   # inner head (thickest)
    s.put(cx-3, cy-8, brow_col, 5, 1)   # arch peak
    s.put(cx+2, cy-7, brow_col, 4, 1)   # outer tail (thin)
    s.put(cx-6, cy-6, brow_col, 2, 1)   # inner underside hairs
    # ── brow-ridge shadow ─────────────────────────────────────────────────
    s.put(cx-6, cy-4, skin_shd, 10, 1)
    # ── upper lid line ─────────────────────────────────────────────────────
    s.put(cx-6, cy-3, "black",  10, 1)
    # ── eye white ──────────────────────────────────────────────────────────
    s.put(cx-6, cy-2, "white",  10, 5)
    # ── iris outer ring ────────────────────────────────────────────────────
    s.put(cx-3, cy-2, iris,      5, 5)
    # ── iris inner (limbal ring) ───────────────────────────────────────────
    s.put(cx-2, cy-1, iris_dk,   3, 3)
    # ── pupil ──────────────────────────────────────────────────────────────
    s.put(cx-1, cy,   "black",   1, 1)
    # ── sparkle highlight (top-left of iris) ──────────────────────────────
    s.put(cx-3, cy-2, "white",   1, 1)
    s.put(cx-2, cy-1, skin_lt,   1, 1)   # secondary micro-glint
    # ── lower lash row ─────────────────────────────────────────────────────
    s.put(cx-6, cy+3, "black",  10, 1)
    # ── inner / outer corner shadows ──────────────────────────────────────
    s.put(cx-6, cy-2, skin_shd,  2, 5)
    s.put(cx+4, cy-2, skin_shd,  1, 5)
    # ── under-eye shadow ───────────────────────────────────────────────────
    s.put(cx-6, cy+4, skin_shd, 10, 2)


def p_far_eye(s, cx, cy, iris, iris_dk, brow_col, skin_shd):
    """
    High-detail far (left) eye — 7 px wide, perspective-foreshortened.
    cx, cy = canvas coords of iris centre.
    """
    # ── brow (shorter, in facial shadow) ───────────────────────────────────
    s.put(cx-1, cy-7, brow_col, 4, 1)
    s.put(cx+3, cy-6, brow_col, 2, 1)
    s.put(cx-1, cy-6, brow_col, 2, 1)
    # ── brow-ridge shadow ────────────────────────────────────���────────────
    s.put(cx-1, cy-4, skin_shd, 7, 1)
    # ── upper lid line ─────────────────────────────────────────────────────
    s.put(cx-1, cy-3, "black",  7, 1)
    # ── eye white (narrower due to perspective) ────────────────────────────
    s.put(cx-1, cy-2, "white",  7, 4)
    # ── iris outer ─────────────────────────────────────────────────────────
    s.put(cx+1, cy-2, iris,     3, 4)
    # ── iris inner ─────────────────────────────────────────────────────────
    s.put(cx+1, cy-1, iris_dk,  2, 2)
    # ── pupil ──────────────────────────────────────────────────────────────
    s.put(cx+2, cy,   "black",  1, 1)
    # ── sparkle ────────────────────────────────────────────────────────────
    s.put(cx+1, cy-2, "white",  1, 1)
    # ── lower lash ─────────────────────────────────────────────────────────
    s.put(cx-1, cy+2, "black",  7, 1)
    # ── inner corner / under-eye ──────────────────────────────────────────
    s.put(cx-1, cy-2, skin_shd, 2, 4)
    s.put(cx-1, cy+3, skin_shd, 7, 2)


def p_nose(s, nx, ny, skin_lt, skin_shd, skin_deep):
    """
    Portrait nose.  nx, ny = top of nose bridge (canvas coords).
    Bridge height ~8 game-px; total nose height ~10 px.
    """
    s.put(nx-1, ny,     skin_lt,   2, 7)   # bridge highlight (NW light)
    s.put(nx+2, ny,     skin_shd,  2, 6)   # bridge right shadow
    s.put(nx-2, ny+7,   skin_lt,   4, 2)   # nose tip plateau
    s.put(nx-3, ny+8,   skin_deep, 2, 2)   # nostril L shadow
    s.put(nx+3, ny+8,   skin_deep, 2, 2)   # nostril R shadow
    s.put(nx,   ny+9,   skin_lt,   2, 1)   # nostril base highlight
    s.put(nx-3, ny+5,   skin_shd,  2, 4)   # ala L wing
    s.put(nx+3, ny+5,   skin_shd,  2, 4)   # ala R wing


def p_lips(s, lx, ly, skin, skin_lt, skin_shd, lip_col, lip_lt, talking=False):
    """
    Portrait mouth.  lx, ly = centre of mouth seam (canvas coords).
    Span ~12 px wide, 6-7 px tall (neutral) / 10 px tall (talking).
    """
    # philtrum groove
    s.put(lx-1, ly-4, skin_shd, 2, 2)
    if talking:
        # ── upper lip (Cupid's bow) ──────────────────────────────────────
        s.put(lx-6, ly-2, lip_col, 2, 2)
        s.put(lx-4, ly-3, lip_col, 2, 1)
        s.put(lx-2, ly-2, lip_col, 2, 2)
        s.put(lx,   ly-3, lip_col, 2, 1)
        s.put(lx+2, ly-2, lip_col, 2, 2)
        # ── open mouth interior ──────────────────────────────────────────
        s.put(lx-5, ly,   "night",  10, 4)
        # ── upper teeth ──────────────────────────────────────────────────
        s.put(lx-4, ly,   "white",   8, 2)
        s.put(lx-2, ly,   skin_shd,  1, 2)   # tooth gap
        s.put(lx+1, ly,   skin_shd,  1, 2)   # tooth gap
        # ── lower lip ────────────────────────────────────────────────────
        s.put(lx-5, ly+4, lip_col,  10, 2)
        s.put(lx-4, ly+4, lip_lt,    8, 1)
    else:
        # ── upper lip (Cupid's bow, closed) ──────────────────────────────
        s.put(lx-6, ly-2, lip_col, 2, 2)
        s.put(lx-4, ly-3, lip_col, 2, 1)
        s.put(lx-2, ly-2, lip_col, 2, 2)
        s.put(lx,   ly-3, lip_col, 2, 1)
        s.put(lx+2, ly-2, lip_col, 2, 2)
        # ── mouth seam ───────────────────────────────────────────────────
        s.put(lx-7, ly,   skin_shd,  1, 1)
        s.put(lx-6, ly,   "black",  12, 1)
        s.put(lx+6, ly,   skin_shd,  1, 1)
        # ── lower lip ────────────────────────────────────────────────────
        s.put(lx-6, ly+1, skin,      2, 2)
        s.put(lx-4, ly+1, lip_col,   8, 2)
        s.put(lx-3, ly+1, lip_lt,    6, 1)
        s.put(lx+4, ly+1, skin,      2, 2)
    # corner shadows
    s.put(lx-8, ly-1, skin_shd, 1, 5)
    s.put(lx+7, ly-1, skin_shd, 1, 5)
    # chin shadow
    s.put(lx-5, ly+4, skin_shd, 10, 2)


# ── 01. Fatima ────────────────────────────────────────────────────────────────

def draw_portrait_fatima(s, talking=False):
    """Cream/beige hijab, warm olive skin, dark-brown eyes, rose coat collar."""
    SKIN   = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"; SKINDP = "wood_light"
    HIJ    = "cream_mid";  HIJL  = "white";     HIJS  = "cream_dark"
    BROW   = "ochre"

    p_bg(s)

    # ── hijab dome ────────────────────────────────────────────────────────────
    s.put(C+2,   0, HIJ,   48, 34)           # main volume
    s.put(C+2,  30, HIJS,  48, 10)           # lower fold shadow
    # highlight (NW quadrant of dome)
    s.put(C+4,   0, HIJL,  14,  4)
    s.put(C+2,   4, HIJL,   4, 12)
    s.put(C+20,  2, HIJL,   6,  2)           # crown gloss streak
    # fold texture lines
    s.put(C+4,  20, HIJS,   8,  1)
    s.put(C+38, 22, HIJS,   8,  1)
    s.put(C+4,  28, HIJS,  10,  1)
    # side drapes
    s.put(C,    12, HIJS,   4, 28)           # left drape shadow
    s.put(C+48, 12, HIJS,   4, 28)           # right drape shadow
    s.put(C+2,  34, HIJS,  48,  2)           # chin fold line

    # ── face (4-tone warm olive) ──────────────────────────────────────────────
    s.put(C+10,  5, SKIN,   32, 34)          # base flesh
    # NW forehead highlight
    s.put(C+10,  5, SKINL,  16,  6)
    s.put(C+10, 11, SKINL,   4, 12)
    # left cheek extension
    s.put(C+8,  14, SKIN,    2, 16)
    # right cheek shadow gradient
    s.put(C+36, 10, SKIND,   6, 22)
    s.put(C+40, 12, SKINDP,  2, 18)
    # cheekbone highlight (near side, under eye)
    s.put(C+28, 20, SKINL,   6,  4)
    # far cheek subtle shadow
    s.put(C+10, 18, SKIND,   2,  6)
    # chin underside
    s.put(C+10, 35, SKIND,  32,  4)
    # blush
    s.put(C+32, 22, "brick_light",  4,  3)
    s.put(C+12, 22, "brick_light",  2,  2)   # far-side blush

    # ── right ear (near, peeking from hijab edge) ─────────────────────────────
    s.put(C+41, 14, SKIN,    4,  9)
    s.put(C+42, 16, SKIND,   2,  5)
    s.put(C+44, 14, SKINDP,  1,  7)

    # ── eyes ──────────────────────────────────────────────────────────────────
    p_near_eye(s, C+31, 18, "stone_dark", "night", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "stone_dark", "night", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth ─────────────────────────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "brick_mid", "mortar", talking)

    # ── hijab framing face sides ──────────────────────────────────────────────
    s.put(C+8,  33, HIJS,   4,  8)           # hijab shadow on left cheek
    s.put(C+40, 33, HIJS,   4,  8)           # hijab shadow on right cheek

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 37, SKIN,   16, 10)
    s.put(C+28, 37, SKIND,   6, 10)

    # ── rose coat collar (bottom strip) ──────────────────────────────────────
    s.put(C,    44, "brick_light", 52,  8)   # coat body
    s.put(C,    44, "brick_mid",    6,  8)   # left shadow
    s.put(C+46, 44, "brick_mid",    6,  8)   # right shadow
    s.put(C+14, 42, "mortar",      24,  2)   # collar band
    s.put(C+22, 40, "brick_light",  8,  4)   # collar centre open
    s.put(C+26, 38, "brick_mid",    4,  6)   # collar seam


# ── 02. Omar ──────────────────────────────────────────────────────────────────

def draw_portrait_omar(s, talking=False):
    """Black wavy hair, warm olive skin, dark tired eyes, baker's apron."""
    SKIN   = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"; SKINDP = "wood_light"
    HAIR   = "black";      HAIRL = "stone_dark"; HAIRM = "stone_mid"
    BROW   = "black"

    p_bg(s)

    # ── black hair (wavy, slightly messy) ─────────────────────────────────────
    s.put(C+8,   0, HAIR,   36,  8)           # crown dome
    s.put(C+6,   6, HAIR,    4, 16)           # left side
    s.put(C+42,  6, HAIR,    4, 16)           # right side
    # hair highlights (NW gloss)
    s.put(C+12,  0, HAIRL,  14,  3)
    s.put(C+10,  3, HAIRL,   4,  6)
    s.put(C+22,  1, HAIRM,   6,  2)           # second gloss band
    # wave texture
    s.put(C+18,  6, HAIRL,   4,  2)
    s.put(C+28,  4, HAIRL,   4,  2)
    s.put(C+36,  6, HAIRL,   4,  2)

    # ── face (broad, weary baker) ─────────────────────────────────────────────
    s.put(C+8,   6, SKIN,   36, 34)
    # NW forehead highlight
    s.put(C+8,   6, SKINL,  18,  6)
    s.put(C+8,  12, SKINL,   4, 12)
    # cheekbones
    s.put(C+28, 18, SKINL,   8,  4)           # near cheekbone highlight
    # right shadow
    s.put(C+36,  9, SKIND,   8, 24)
    s.put(C+41, 11, SKINDP,  3, 20)
    # far cheek
    s.put(C+8,  18, SKIND,   2,  8)
    # under-eye fatigue lines
    s.put(C+22, 22, SKIND,  10,  1)           # near under-eye crease
    s.put(C+10, 22, SKIND,   4,  1)           # far under-eye crease
    # chin shadow
    s.put(C+8,  36, SKIND,  36,  4)

    # ── right ear ─────────────────────────────────────────────────────────────
    s.put(C+43, 14, SKIN,    3,  9)
    s.put(C+44, 16, SKIND,   2,  5)

    # ── eyes (warm brown, slightly tired) ────────────────────────────────────
    p_near_eye(s, C+31, 18, "wood_light", "wood_dark", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "wood_light", "wood_dark", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth ─────────────────────────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "cream_dark", "cream_mid", talking)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 38, SKIN,   14, 10)
    s.put(C+26, 38, SKIND,   6, 10)

    # ── white apron bib (with flour stain) ────────────────────────────────────
    s.put(C,    44, "white",       52, 10)   # apron
    s.put(C,    44, "stone_pale",   6, 10)   # left shading
    s.put(C+44, 44, "stone_mid",    8, 10)   # right shadow
    s.put(C+16, 42, "stone_pale",  24,  2)   # collar/bib top hem
    s.put(C+24, 40, "white",        8,  4)   # bib centre open
    # Flour stains on apron
    s.put(C+8,  46, "mortar",       6,  4)
    s.put(C+28, 47, "mortar",       4,  3)
    s.put(C+40, 45, "mortar",       6,  4)
    # Dark shirt collar visible above apron
    s.put(C+20, 40, "stone_dark",  12,  4)


# ── 03. Mevrouw Baert ─────────────────────────────────────────────────────────

def draw_portrait_baert(s, talking=False):
    """Silver-grey hair bun, pale Flemish skin, detailed reading glasses, blue-grey eyes."""
    SKIN   = "cream_light"; SKINL = "white";     SKIND = "cream_mid"; SKINDP = "cream_dark"
    HAIR   = "stone_mid";   HAIRL = "stone_light"; HAIRP = "stone_pale"
    BROW   = "stone_mid"

    p_bg(s)

    # ── grey hair bun ─────────────────────────────────────────────────────────
    s.put(C+8,   0, HAIR,   36, 10)           # dome
    s.put(C+6,   8, HAIR,    4, 18)           # left side
    s.put(C+42,  8, HAIR,    4, 18)           # right side
    # highlights
    s.put(C+12,  0, HAIRL,  14,  4)
    s.put(C+10,  4, HAIRL,   4,  8)
    s.put(C+24,  2, HAIRP,   6,  2)           # crown gloss
    # bun knot at back (peeking right)
    s.put(C+42,  4, HAIRL,   4,  6)
    # grey strand lines
    s.put(C+14,  8, HAIRP,   4,  2)
    s.put(C+26,  6, HAIRP,   4,  2)
    s.put(C+36,  8, HAIRP,   4,  2)

    # ── face (pale, soft age lines) ───────────────────────────────────────────
    s.put(C+8,   8, SKIN,   36, 32)
    # NW highlight
    s.put(C+8,   8, SKINL,  18,  6)
    s.put(C+8,  14, SKINL,   4, 10)
    # cheekbone highlight
    s.put(C+26, 20, SKINL,   8,  4)
    # right side shadow
    s.put(C+36, 12, SKIND,   6, 20)
    s.put(C+40, 14, SKINDP,  3, 16)
    # far cheek
    s.put(C+8,  20, SKIND,   2,  8)
    # nasolabial folds (age detail)
    s.put(C+18, 28, SKIND,   2,  6)           # fold near
    s.put(C+36, 28, SKIND,   2,  6)           # fold far
    # crow's-feet hint
    s.put(C+38, 20, SKIND,   3,  2)
    s.put(C+11, 20, SKIND,   2,  2)
    # chin shadow
    s.put(C+8,  36, SKIND,  36,  4)

    # ── right ear ───────���─────────────────────────────────────────────────────
    s.put(C+43, 14, SKIN,    3,  9)
    s.put(C+44, 16, SKIND,   2,  5)

    # ── reading glasses (full frames) ─────────────────────────────────────────
    # Left lens frame (far side)
    s.put(C+9,  14, "stone_dark",  8,  1)   # top rail L
    s.put(C+9,  14, "stone_dark",  1,  8)   # side L
    s.put(C+16, 14, "stone_dark",  1,  8)   # side inner L
    s.put(C+9,  22, "stone_dark",  8,  1)   # bottom rail L
    # Right lens frame (near side, larger)
    s.put(C+21, 12, "stone_dark", 12,  1)   # top rail R
    s.put(C+21, 12, "stone_dark",  1,  8)   # outer side R
    s.put(C+32, 12, "stone_dark",  1,  8)   # inner side R
    s.put(C+21, 20, "stone_dark", 12,  1)   # bottom rail R
    # Nose bridge bar
    s.put(C+17, 17, "stone_dark",  4,  1)
    # Lens fills (glass effect — slightly lighter than face bg)
    s.put(C+10, 15, "stone_pale",  6,  7)   # left lens interior
    s.put(C+22, 13, "stone_pale", 10,  7)   # right lens interior
    # Lens reflections (glint highlights)
    s.put(C+10, 15, "white",       2,  1)
    s.put(C+22, 13, "white",       3,  1)
    s.put(C+25, 15, "white",       1,  1)
    # Temple arms
    s.put(C+9,  17, "stone_dark",  1,  1)   # left arm hint
    s.put(C+43, 15, "stone_dark",  1,  6)   # right arm behind ear

    # ── eyes (behind lenses, blue-grey) ───────────────────────────────────────
    # Near eye (simplified slightly for glasses-behind look)
    s.put(C+24, 14, BROW,    6,  1)          # near brow (above frame)
    s.put(C+23, 15, "white", 8,  4)          # near white
    s.put(C+26, 15, "stone_mid", 3, 4)       # near iris (blue-grey)
    s.put(C+27, 17, "black",  1,  2)         # near pupil
    s.put(C+23, 14, "black",  8,  1)         # near upper lid
    s.put(C+23, 19, SKIND,    8,  1)         # near lower lid
    # Far eye
    s.put(C+11, 14, BROW,    4,  1)          # far brow
    s.put(C+11, 15, "white", 5,  4)          # far white
    s.put(C+13, 15, "stone_mid",2, 4)        # far iris
    s.put(C+14, 17, "black",  1,  2)         # far pupil
    s.put(C+11, 14, "black",  5,  1)         # far upper lid

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 24, SKINL, SKIND, SKINDP)

    # ── mouth (thinner with age) ───────────────────────────────────────────────
    p_lips(s, C+25, 35, SKIN, SKINL, SKIND, "cream_mid", "cream_light", talking)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 38, SKIN,   14, 10)
    s.put(C+26, 38, SKIND,   6, 10)

    # ── grey cardigan collar + blouse ─────────────────────────────────────────
    s.put(C,    44, "stone_mid",   52, 10)   # cardigan body
    s.put(C,    44, "stone_dark",   6, 10)   # shadow left
    s.put(C+46, 44, "stone_dark",   6, 10)   # shadow right
    s.put(C+20, 42, "night",       12,  2)   # collar gap
    s.put(C+20, 44, "cream_light", 12,  6)   # blouse visible
    s.put(C+20, 42, "stone_mid",    4,  6)   # left lapel
    s.put(C+28, 42, "stone_mid",    4,  6)   # right lapel
    # Cardigan button
    s.put(C+25, 49, "stone_dark",   2,  2)
    s.put(C+25, 49, "stone_light",  1,  1)


# ── 04. Reza ──────────────────────────────────────────────────────────────────

def draw_portrait_reza(s, talking=False):
    """Black hair, sharp olive features, 5-o'clock shadow, oud peg-box top-right."""
    SKIN   = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"; SKINDP = "wood_light"
    HAIR   = "black";      HAIRL = "stone_dark"; HAIRM = "stone_mid"
    BROW   = "black"

    p_bg(s)

    # ── oud peg-box (peeking top-right corner, distinctive) ───────────────────
    s.put(C+42,  0, "wood_light", 10, 16)    # oud neck/peg-box
    s.put(C+42,  0, "wood_dark",   2, 16)    # shadow
    s.put(C+50,  0, "wood_dark",   2, 16)
    s.put(C+44,  0, "cream_mid",   4,  2)    # peg-box top highlight
    # Tuning pegs
    s.put(C+43,  4, "wood_dark",   2,  2)
    s.put(C+43,  8, "wood_dark",   2,  2)
    s.put(C+43, 12, "wood_dark",   2,  2)
    s.put(C+49,  4, "wood_dark",   2,  2)

    # ── black hair (slightly wavy, neat) ──────────────────────────────────────
    s.put(C+6,   0, HAIR,   36,  8)
    s.put(C+6,   6, HAIR,    4, 18)
    s.put(C+40,  6, HAIR,    4, 18)
    # hair gloss
    s.put(C+10,  0, HAIRL,  16,  3)
    s.put(C+8,   3, HAIRL,   4,  8)
    s.put(C+20,  2, HAIRM,   6,  2)
    # strand texture
    s.put(C+18,  5, HAIRL,   4,  2)
    s.put(C+30,  3, HAIRL,   4,  2)

    # ── face (sharp olive features) ───────────────────────────────────────────
    s.put(C+8,   6, SKIN,   34, 34)
    # NW highlight
    s.put(C+8,   6, SKINL,  16,  6)
    s.put(C+8,  12, SKINL,   4, 12)
    # cheekbone highlight (strong)
    s.put(C+26, 18, SKINL,   8,  4)
    # right shadow
    s.put(C+36,  9, SKIND,   6, 22)
    s.put(C+40, 11, SKINDP,  2, 18)
    # angular jaw definition
    s.put(C+8,  28, SKIND,   4,  8)           # far jaw
    s.put(C+36, 28, SKINDP,  6,  8)           # near jaw
    # chin shadow
    s.put(C+8,  36, SKIND,  34,  4)

    # ── right ear ─────────────────────────────────────────────────────────────
    s.put(C+42, 14, SKIN,    3,  9)
    s.put(C+43, 16, SKIND,   2,  5)

    # ── 5-o'clock shadow (stippled stubble) ──────────────────────────────────
    s.put(C+10, 28, SKIND,  32,  8)           # stubble zone base
    s.put(C+12, 28, "stone_dark", 2,  6)      # stubble speckle L
    s.put(C+16, 30, "stone_dark", 2,  4)
    s.put(C+20, 28, "stone_dark", 2,  6)
    s.put(C+24, 29, "stone_dark", 2,  4)
    s.put(C+28, 28, "stone_dark", 2,  6)
    s.put(C+32, 30, "stone_dark", 2,  4)
    s.put(C+36, 28, "stone_dark", 2,  6)

    # ── eyes (deep brown, expressive) ─────────────────────────────────────────
    p_near_eye(s, C+31, 18, "stone_dark", "night", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "stone_dark", "night", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth ─────────────────────────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "cream_dark", "cream_mid", talking)

    # ── neck ────────────────────────��─────────────────────────────────────────
    s.put(C+16, 38, SKIN,   14, 10)
    s.put(C+26, 38, SKIND,   6, 10)

    # ── white shirt collar + dark waistcoat ───────────────────────────────────
    s.put(C,    44, "stone_dark",  52, 10)   # waistcoat
    s.put(C,    44, "night",        6, 10)   # deep shadow left
    s.put(C+46, 44, "night",        6, 10)
    # Vest pocket highlight
    s.put(C+8,  44, "stone_mid",    6,  2)
    # White shirt between lapels
    s.put(C+20, 42, "white",       12,  8)
    s.put(C+22, 42, "stone_pale",   2,  2)   # shirt highlight
    # Lapels
    s.put(C+18, 42, "stone_dark",   4,  8)
    s.put(C+30, 42, "stone_dark",   4,  8)


# ── 05. El Osri ───────────────────────────────────────────────────────────────

def draw_portrait_el_osri(s, talking=False):
    """Black hijab, dark-olive skin, gold earrings, kohl eyes, green blazer."""
    SKIN   = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"; SKINDP = "wood_light"
    HIJ    = "night";      HIJL  = "stone_dark"; HIJS  = "black"
    BROW   = "black"

    p_bg(s)

    # ── black hijab dome ──────────────────────────────────────────────────────
    s.put(C+2,   0, HIJ,   48, 34)
    s.put(C+2,  30, HIJS,  48, 10)
    # highlight (subtle, dark fabric)
    s.put(C+6,   0, HIJL,  12,  3)
    s.put(C+4,   3, HIJL,   3, 10)
    s.put(C+22,  1, HIJL,   4,  2)
    # fold lines
    s.put(C+4,  18, HIJS,   8,  1)
    s.put(C+40, 20, HIJS,   8,  1)
    s.put(C+4,  26, HIJS,   8,  1)
    # side drapes
    s.put(C,    12, HIJS,   4, 28)
    s.put(C+48, 12, HIJS,   4, 28)

    # ── face ──────────────────────────────────────────────────────────────────
    s.put(C+10,  5, SKIN,   32, 34)
    s.put(C+10,  5, SKINL,  14,  6)
    s.put(C+10, 11, SKINL,   4, 10)
    # cheekbone highlight
    s.put(C+28, 18, SKINL,   6,  4)
    # right shadow
    s.put(C+36, 10, SKIND,   6, 22)
    s.put(C+40, 12, SKINDP,  2, 18)
    # far cheek
    s.put(C+10, 18, SKIND,   2,  6)
    # chin
    s.put(C+10, 35, SKIND,  32,  4)

    # ── gold earrings (visible below hijab on right side) ─────────────────────
    s.put(C+40, 26, "gold",   2,  6)          # earring stem R
    s.put(C+39, 30, "gold",   4,  4)          # earring drop R
    s.put(C+40, 30, "ochre",  2,  2)          # gold inner darker
    # hint of left earring
    s.put(C+10, 26, "gold",   2,  4)

    # ── right ear ─────────────────────────────────────────────────────────────
    s.put(C+41, 14, SKIN,    4,  9)
    s.put(C+42, 16, SKIND,   2,  5)

    # ── eyes (kohl-lined, intense) ─────────────────────────────────────────────
    p_near_eye(s, C+31, 18, "stone_dark", "night", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "stone_dark", "night", BROW, SKIND)
    # kohl upper liner extension (dramatic)
    s.put(C+37,  15, "night",  4,  1)          # near kohl outer extend
    s.put(C+14,  15, "night",  2,  1)          # far kohl inner extend

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth ─────────────────────────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "brick_light", "mortar", talking)

    # ── hijab framing ──────────────────────────────────────────────────────────
    s.put(C+8,  33, HIJS,   4,  8)
    s.put(C+40, 33, HIJS,   4,  8)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 37, SKIN,   16, 10)
    s.put(C+28, 37, SKIND,   6, 10)

    # ── green blazer collar ───────────────────────────────────────────────────
    s.put(C,    44, "grass",       52, 10)
    s.put(C,    44, "stone_dark",   6, 10)
    s.put(C+46, 44, "stone_dark",   6, 10)
    s.put(C+14, 44, "stone_pale",   8,  2)    # NW highlight
    s.put(C+20, 42, "night",       12,  4)    # collar gap
    s.put(C+20, 44, "white",       12,  6)    # blouse
    s.put(C+18, 42, "grass",        4,  8)    # left lapel
    s.put(C+30, 42, "grass",        4,  8)    # right lapel
    # gold button
    s.put(C+24, 49, "gold",         2,  2)


# ── 06. Yusuf ─────────────────────────────────────────────────────────────────

def draw_portrait_yusuf(s, talking=False):
    """Orange delivery helmet with glass visor, brown skin, safety-vest."""
    SKIN   = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"; SKINDP = "wood_light"
    BROW   = "stone_dark"

    p_bg(s)

    # ── helmet shell ──────────────────────────────────────────────────────────
    s.put(C+4,   0, "stone_dark",  44, 16)    # helmet body
    s.put(C+2,   6, "stone_dark",   4, 12)    # left flare
    s.put(C+46,  6, "stone_dark",   4, 12)    # right flare
    # gloss highlights (NW)
    s.put(C+8,   0, "stone_light", 18,  3)
    s.put(C+6,   3, "stone_light",  4,  8)
    s.put(C+20,  0, "stone_mid",    8,  2)    # secondary gloss band
    # ventilation slots
    for vx in [C+16, C+22, C+28, C+34]:
        s.put(vx,  2, "night",      2,  5)
    # helmet brim shadow
    s.put(C+4,  14, "stone_dark",  44,  2)
    s.put(C+2,  16, "stone_dark",  48,  2)    # brim projection

    # ── glass visor strip ─────────────────────────────────────────────────────
    s.put(C+4,  18, "glass",       44,  6)
    s.put(C+4,  18, "sky_pale",    16,  3)    # visor glint left
    s.put(C+30, 18, "sky_light",   10,  2)    # visor glint right
    # Visor frame (dark edge)
    s.put(C+4,  18, "stone_dark",  44,  1)
    s.put(C+4,  23, "stone_dark",  44,  1)

    # ── face below visor ──────────────────────────────────────────────────────
    s.put(C+8,  24, SKIN,   36, 18)
    # NW highlight
    s.put(C+8,  24, SKINL,  14,  6)
    s.put(C+8,  30, SKINL,   4,  8)
    # cheekbone
    s.put(C+26, 28, SKINL,   8,  4)
    # right shadow
    s.put(C+36, 26, SKIND,   6, 14)
    s.put(C+40, 27, SKINDP,  2, 11)
    # chin
    s.put(C+8,  38, SKIND,  36,  4)

    # ── ears ──────────────────────────────────────────────────────────────────
    s.put(C+43, 22, SKIN,    3,  8)
    s.put(C+44, 24, SKIND,   2,  4)
    s.put(C+6,  22, SKIN,    3,  8)

    # ── eyes (shifted down due to visor, just below visor line) ──────────────
    p_near_eye(s, C+31, 28, "stone_dark", "night", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 28, "stone_dark", "night", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 32, SKINL, SKIND, SKINDP)

    # ── mouth ─────────────────────────────────────────────────────────────────
    p_lips(s, C+25, 40, SKIN, SKINL, SKIND, "cream_dark", "cream_mid", talking)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 44, SKIN,   14,  6)
    s.put(C+26, 44, SKIND,   6,  6)

    # ── orange safety vest (bottom strip) ─────────────────────────────────────
    s.put(C,    46, "ochre",       52,  6)
    s.put(C,    46, "cream_dark",   6,  6)
    s.put(C+46, 46, "cream_dark",   6,  6)
    s.put(C+8,  46, "cream_light",  8,  2)   # NW highlight
    # reflective strip
    s.put(C,    48, "white",       52,  2)
    s.put(C,    48, "stone_pale",  52,  1)


# ── 07. Aziz ──────────────────────────────────────────────────────────────────

def draw_portrait_aziz(s, talking=False):
    """White taqiyah, warm ochre skin, layered white beard, djellaba folds."""
    SKIN   = "ochre";  SKINL = "cream_dark"; SKIND = "wood_dark"
    BROW   = "stone_dark"

    p_bg(s)

    # ── taqiyah (white embroidered skullcap) ──────────────────────────────────
    s.put(C+8,   0, "white",       36,  8)
    s.put(C+6,   6, "white",        4,  8)
    s.put(C+42,  6, "white",        4,  8)
    # cap highlights
    s.put(C+12,  0, "stone_pale",  12,  3)
    s.put(C+10,  3, "stone_pale",   4,  6)
    # embroidery dots
    for ex in [C+12, C+18, C+24, C+30, C+36]:
        s.put(ex, 5, "stone_mid",  2,  2)
    s.put(C+14,  7, "stone_mid",   2,  1)
    s.put(C+34,  7, "stone_mid",   2,  1)

    # ── face (warm ochre, weathered) ──────────────────────────────────────────
    s.put(C+8,   7, SKIN,   36, 30)
    # NW highlight
    s.put(C+8,   7, SKINL,  14,  6)
    s.put(C+8,  13, SKINL,   4, 10)
    # cheekbone
    s.put(C+26, 18, SKINL,   6,  4)
    # right shadow
    s.put(C+36,  9, SKIND,   6, 20)
    s.put(C+40, 11, SKIND,   2, 16)          # deep shadow
    # far cheek
    s.put(C+8,  18, SKIND,   2,  8)
    # age creases
    s.put(C+10, 20, SKIND,   2,  4)          # near outer eye crease
    s.put(C+38, 20, SKIND,   4,  3)
    s.put(C+16, 28, SKIND,   2,  5)          # nasolabial L
    s.put(C+34, 28, SKIND,   2,  5)          # nasolabial R
    # chin shadow (into beard)
    s.put(C+8,  33, SKIND,  36,  4)

    # ── right ear ─────────────────────────────────────────────────────────────
    s.put(C+42, 14, SKIN,    3,  9)
    s.put(C+43, 16, SKIND,   2,  5)

    # ── eyes (kind, elder, droopy lower lid) ──────────────────────────────────
    p_near_eye(s, C+31, 18, "stone_dark", "night", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "stone_dark", "night", BROW, SKIND)
    # droopy lower lid (age)
    s.put(C+25,  22, SKIND,  12,  1)         # near lower lid droop
    s.put(C+14,  22, SKIND,   7,  1)         # far lower lid droop

    # ── nose (strong, large) ──────────────────────────────────────────────────
    p_nose(s, C+24, 22, SKINL, SKIND, "wood_dark")
    # widened nostrils
    s.put(C+20, 29, SKIND,   3,  3)
    s.put(C+30, 29, SKIND,   3,  3)

    # ── layered white beard (fills lower half) ────────────────────────────────
    # Base mass
    s.put(C+6,  30, "stone_pale",  40, 22)
    # Lighter centre
    s.put(C+10, 32, "white",       24, 18)
    # Darker outer
    s.put(C+6,  30, "stone_mid",    4, 22)
    s.put(C+42, 30, "stone_mid",    4, 22)
    # Beard texture lines (strand directions)
    s.put(C+14, 34, "stone_mid",    6,  1)
    s.put(C+22, 36, "stone_mid",    8,  1)
    s.put(C+30, 34, "stone_mid",    6,  1)
    s.put(C+14, 40, "stone_pale",   8,  1)
    s.put(C+26, 42, "stone_pale",   8,  1)
    s.put(C+18, 44, "stone_pale",  12,  1)
    # Moustache (slightly darker than beard)
    s.put(C+14, 30, "stone_light",  6,  3)
    s.put(C+32, 30, "stone_light",  6,  3)
    # Beard highlight (centre glow)
    s.put(C+18, 38, "white",       12,  3)

    # ── neck (hidden behind beard) ────────────────────────────────────────────
    s.put(C+16, 36, SKIN,   12,  4)

    # ── djellaba collar (white, with fold lines) ──────────────────────────────
    s.put(C,    46, "stone_light",  52,  6)
    s.put(C,    46, "stone_mid",     6,  6)
    s.put(C+46, 46, "stone_mid",     6,  6)
    s.put(C+8,  46, "white",         8,  2)   # NW highlight
    # neckline V-opening
    s.put(C+20, 44, "stone_mid",    12,  4)
    s.put(C+22, 44, "night",         8,  4)   # collar shadow
    # fold lines
    s.put(C+12, 47, "stone_mid",     4,  3)
    s.put(C+38, 47, "stone_mid",     4,  3)
    s.put(C+24, 48, "stone_light",   6,  2)


# ── 08. Sofia ─────────────────────────────────────────────────────────────────

def draw_portrait_sofia(s, talking=False):
    """Warm brown hair with reddish streak, pale Belgian skin, AirPod, hazel eyes."""
    SKIN   = "cream_light"; SKINL = "white";      SKIND = "cream_mid"; SKINDP = "cream_dark"
    HAIR   = "wood_dark";   HAIRL = "wood_light";  HAIRR = "ochre"
    BROW   = "wood_dark"

    p_bg(s)

    # ── warm brown hair ───────────────────────────────────────────────────────
    s.put(C+8,   0, HAIR,   36, 10)
    s.put(C+6,   8, HAIR,    4, 20)           # left side, falls to shoulder
    s.put(C+42,  8, HAIR,    4, 20)           # right side
    # Main highlights (NW)
    s.put(C+12,  0, HAIRL,  16,  4)
    s.put(C+10,  4, HAIRL,   4,  8)
    s.put(C+24,  2, HAIRL,   6,  2)           # crown gloss streak
    # Reddish-brown highlight streak
    s.put(C+20,  0, HAIRR,   8,  3)
    s.put(C+28,  2, HAIRR,   4,  2)
    # Strand details
    s.put(C+14,  8, HAIRL,   4,  3)
    s.put(C+28,  6, HAIRL,   4,  2)
    s.put(C+36,  8, HAIRL,   4,  3)
    # Hair falls past collar
    s.put(C+6,  26, HAIR,    4,  8)
    s.put(C+42, 26, HAIR,    4,  8)

    # ── face (pale, slightly rosy) ────────────────────────────��───────────────
    s.put(C+8,   8, SKIN,   36, 30)
    # NW highlight
    s.put(C+8,   8, SKINL,  18,  6)
    s.put(C+8,  14, SKINL,   4, 12)
    # cheekbone highlight
    s.put(C+28, 18, SKINL,   8,  4)
    # right shadow
    s.put(C+36, 12, SKIND,   6, 18)
    s.put(C+40, 14, SKINDP,  2, 14)
    # far cheek
    s.put(C+8,  18, SKIND,   2,  6)
    # rosy cheeks (subtle blush)
    s.put(C+32, 22, "brick_light",  4,  3)
    s.put(C+12, 22, "brick_light",  2,  2)
    # freckles (2-3 dots near nose)
    s.put(C+22, 22, SKINDP,  1,  1)
    s.put(C+28, 21, SKINDP,  1,  1)
    s.put(C+30, 23, SKINDP,  1,  1)
    # chin shadow
    s.put(C+8,  34, SKIND,  36,  4)

    # ── right ear with AirPod ──────────────────────────────────────────────────
    s.put(C+42, 14, SKIN,    4,  9)           # ear
    s.put(C+43, 16, SKIND,   2,  5)
    s.put(C+42, 16, "white",  2,  4)          # AirPod body (in ear canal)
    s.put(C+42, 20, "white",  2,  6)          # AirPod stem (hangs below)
    s.put(C+42, 20, "stone_pale",1, 6)        # stem highlight

    # ── left ear hint ─────────────────────────────────────────────────────────
    s.put(C+8,  14, SKIN,    3,  8)

    # ── eyes (hazel, bright) ──────────────────────────────────────────────────
    p_near_eye(s, C+31, 18, "wood_light", "wood_dark", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "wood_light", "wood_dark", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth (pink lips) ─────────────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "brick_light", "mortar", talking)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 36, SKIN,   14, 10)
    s.put(C+26, 36, SKIND,   6, 10)

    # ── olive vintage jacket ──────────────────────────────────────────────────
    s.put(C,    44, "grass",       52, 10)
    s.put(C,    44, "stone_dark",   6, 10)
    s.put(C+46, 44, "stone_dark",   6, 10)
    s.put(C+8,  44, "stone_pale",   8,  2)    # NW highlight
    # Open collar
    s.put(C+20, 42, "night",       12,  6)    # collar gap
    s.put(C+20, 44, "stone_pale",  12,  6)    # cream-coloured top visible
    s.put(C+18, 42, "grass",        4,  8)    # left lapel
    s.put(C+30, 42, "grass",        4,  8)    # right lapel
    # Brass button
    s.put(C+26, 49, "ochre",        2,  2)
    s.put(C+26, 49, "gold",         1,  1)
    # Elbow-patch hint at left edge
    s.put(C,    47, "wood_dark",    4,  4)


# ── 09. Hamza ─────────────────────────────────────────────────────────────────

def draw_portrait_hamza(s, talking=False):
    """Crisp fade haircut, darker olive skin, bright eyes, tracksuit with side stripes."""
    SKIN   = "cream_dark"; SKINL = "cream_mid"; SKIND = "ochre"; SKINDP = "wood_light"
    HAIR   = "black";      HAIRL = "stone_dark"
    BROW   = "black"

    p_bg(s)

    # ── fade haircut (very close-cropped top, sharp taper at sides) ───────────
    # Crown (close-cropped, dark)
    s.put(C+8,   0, HAIR,   36,  6)
    # NW sheen on crown
    s.put(C+12,  0, HAIRL,  14,  2)
    s.put(C+10,  2, HAIRL,   4,  4)
    # Fade line — very clean taper (dark → skin, top to bottom)
    s.put(C+6,   4, HAIR,    4, 14)           # left fade band
    s.put(C+42,  4, HAIR,    4, 14)           # right fade band
    s.put(C+6,  12, HAIRL,   4,  6)           # lighter mid-fade
    s.put(C+42, 12, HAIRL,   4,  6)
    s.put(C+6,  18, SKIND,   4,  4)           # fade-to-skin zone

    # ── face (darker olive, young / smooth skin) ──────────────────────────────
    s.put(C+8,   5, SKIN,   36, 35)
    # NW highlight (more defined on younger skin)
    s.put(C+8,   5, SKINL,  18,  7)
    s.put(C+8,  12, SKINL,   4, 14)
    # strong cheekbone highlight (youth)
    s.put(C+26, 18, SKINL,  10,  5)
    # right shadow
    s.put(C+36,  8, SKIND,   6, 24)
    s.put(C+40, 10, SKINDP,  2, 20)
    # jaw definition
    s.put(C+8,  32, SKIND,   4, 8)
    s.put(C+36, 32, SKINDP,  6, 8)
    # chin shadow
    s.put(C+8,  36, SKIND,  36,  4)

    # ── right ear ─────────────────────────────────────────────────────────────
    s.put(C+42, 14, SKIN,    4,  9)
    s.put(C+43, 16, SKIND,   2,  5)

    # ── eyes (bright, youthful) ────────────────────────────────────────────────
    p_near_eye(s, C+31, 18, "stone_dark", "night", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "stone_dark", "night", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth ─────────────────────────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "cream_dark", "cream_mid", talking)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 38, SKIN,   14, 10)
    s.put(C+26, 38, SKIND,   6, 10)

    # ── tracksuit collar + side stripes ───────────────────────────────────────
    s.put(C,    44, "de_lijn_blue", 52, 10)   # tracksuit body
    s.put(C,    44, "night",         6, 10)   # shadow left
    s.put(C+46, 44, "night",         6, 10)   # shadow right
    s.put(C+8,  44, "sky_pale",      8,  2)   # NW highlight
    # White side stripes (iconic detail)
    s.put(C,    44, "white",         3, 10)   # left stripe
    s.put(C+49, 44, "white",         3, 10)   # right stripe
    # Zip centre
    s.put(C+24, 42, "white",         4,  8)
    s.put(C+25, 42, "stone_light",   2,  2)   # zip pull
    # Brand embroidered logo (right chest)
    s.put(C+36, 45, "white",         6,  5)
    s.put(C+37, 46, "de_lijn_blue",  4,  3)   # logo interior


# ── 10. Tine ──────────────────────────────────────────────────────────────────

def draw_portrait_tine(s, talking=False):
    """Golden-blonde hair, pale skin, blue-grey eyes, colourful scarf, tunic embroidery."""
    SKIN   = "cream_light"; SKINL = "white";      SKIND = "cream_mid"; SKINDP = "cream_dark"
    HAIR   = "cream_dark";  HAIRL = "cream_mid";   HAIRG = "ochre";    HAIRH = "mortar"
    BROW   = "ochre"

    p_bg(s)

    # ── golden-blonde hair ────────────────────────────────────────────────────
    s.put(C+8,   0, HAIR,   36, 10)
    s.put(C+6,   8, HAIR,    4, 22)           # left side
    s.put(C+42,  8, HAIR,    4, 22)           # right side
    # Golden highlights (NW)
    s.put(C+12,  0, HAIRL,  16,  4)
    s.put(C+10,  4, HAIRL,   4,  8)
    s.put(C+24,  2, "cream_light", 6, 2)      # lightest crown gloss
    # Warm golden streak
    s.put(C+20,  0, HAIRG,   8,  4)
    s.put(C+28,  2, HAIRG,   4,  2)
    # Lowlight (darker strand)
    s.put(C+16,  6, HAIRH,   4,  2)
    s.put(C+34,  6, HAIRH,   4,  2)
    # Strand details
    s.put(C+14,  8, HAIRL,   4,  3)
    s.put(C+28,  6, HAIRL,   4,  2)
    s.put(C+36,  8, HAIRL,   4,  3)
    # Hair falling past collar
    s.put(C+6,  26, HAIR,    4, 10)
    s.put(C+42, 26, HAIR,    4, 10)

    # ── face (pale Belgian) ───────────────────────────────────────────────────
    s.put(C+8,   8, SKIN,   36, 30)
    # NW highlight
    s.put(C+8,   8, SKINL,  18,  6)
    s.put(C+8,  14, SKINL,   4, 12)
    # cheekbone
    s.put(C+28, 18, SKINL,   8,  4)
    # right shadow
    s.put(C+36, 12, SKIND,   6, 18)
    s.put(C+40, 14, SKINDP,  2, 14)
    # far cheek
    s.put(C+8,  18, SKIND,   2,  6)
    # blush (warm cheeks)
    s.put(C+32, 22, "brick_light",  4,  2)
    s.put(C+12, 22, "brick_light",  2,  2)
    # chin shadow
    s.put(C+8,  34, SKIND,  36,  4)

    # ── right ear ─────────────────────────────────────────────────────────────
    s.put(C+42, 14, SKIN,    3,  9)
    s.put(C+43, 16, SKIND,   2,  5)

    # ── eyes (blue-grey) ──────────────────────────────────────────────────────
    p_near_eye(s, C+31, 18, "de_lijn_blue", "stone_dark", BROW, SKINL, SKIND)
    p_far_eye (s, C+15, 18, "de_lijn_blue", "stone_dark", BROW, SKIND)

    # ── nose ──────────────────────────────────────────────────────────────────
    p_nose(s, C+25, 22, SKINL, SKIND, SKINDP)

    # ── mouth (warm natural lips) ──────────────────────────────────────────────
    p_lips(s, C+25, 33, SKIN, SKINL, SKIND, "brick_light", "mortar", talking)

    # ── neck ──────────────────────────────────────────────────────────────────
    s.put(C+16, 36, SKIN,   14, 10)
    s.put(C+26, 36, SKIND,   6, 10)

    # ── colourful scarf with gold dots ────────────────────────────────────────
    s.put(C,    42, "brick_mid",    52, 12)   # scarf base (warm red)
    s.put(C,    42, "brick_dark",    6, 12)   # left shadow
    s.put(C+46, 42, "brick_dark",    6, 12)   # right shadow
    s.put(C+8,  42, "brick_light",   8,  2)   # NW highlight
    # Gold dot pattern on scarf
    for dx in [C+10, C+16, C+22, C+28, C+34, C+40]:
        s.put(dx, 44, "gold",   2,  2)
        s.put(dx+3, 48, "gold", 2,  2)
    # Tunic embroidery visible at neckline
    s.put(C+18, 40, "gold",    16,  2)        # embroidery band
    s.put(C+18, 40, "ochre",    2,  2)        # embroidery detail L
    s.put(C+30, 40, "ochre",    2,  2)        # embroidery detail R
    for ex in [C+20, C+24, C+28]:
        s.put(ex, 40, "brick_light", 2, 2)


# ── NPCS list ─────────────────────────────────────────────────────────────────

NPCS = [
    ("fatima",  draw_portrait_fatima,  True),
    ("omar",    draw_portrait_omar,    True),
    ("baert",   draw_portrait_baert,   True),
    ("reza",    draw_portrait_reza,    True),
    ("el_osri", draw_portrait_el_osri, True),
    ("yusuf",   draw_portrait_yusuf,   True),
    ("aziz",    draw_portrait_aziz,    False),   # beard hides mouth
    ("sofia",   draw_portrait_sofia,   True),
    ("hamza",   draw_portrait_hamza,   True),
    ("tine",    draw_portrait_tine,    True),
]


# ── generator ─────────────────────────────────────────────────────────────────

def generate_portrait(npc_id: str, draw_fn, has_talking: bool) -> None:
    if not HAS_PIL:
        print("  ✗ Pillow unavailable — skipping")
        return

    # ── frame 0: neutral ──────────────────────────────────────────────────────
    s0 = SVGSheet(64, 96, f"{npc_id}_neutral")
    draw_fn(s0, talking=False)
    frame0 = crop_to_portrait(render_sheet(s0))

    # ── frame 1: talking ──────────────────────────────────────────────────────
    s1 = SVGSheet(64, 96, f"{npc_id}_talking")
    draw_fn(s1, talking=has_talking)
    frame1 = crop_to_portrait(render_sheet(s1))

    # ── stitch 2-frame sheet ──────────────────────────────────────────────────
    sheet = Image.new("RGBA", (PORTRAIT_PX * 2, PORTRAIT_PX), (0, 0, 0, 0))
    sheet.paste(frame0, (0,          0))
    sheet.paste(frame1, (PORTRAIT_PX, 0))

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{npc_id}_portrait.png")
    sheet.save(out_path)
    print(f"  PNG → {out_path}  ({PORTRAIT_PX * 2}×{PORTRAIT_PX} px)")


def main() -> None:
    print("=" * 60)
    print("Turnhoutsebaan NPC Portrait Generator  (high-detail dedicated art)")
    print(f"  Crop : game x={CROP_GX1}..{CROP_GX2}, y={CROP_GY1}..{CROP_GY2}")
    print(f"  Frame: {PORTRAIT_PX}×{PORTRAIT_PX} px")
    print("=" * 60)
    for npc_id, draw_fn, has_talking in NPCS:
        print(f"\n● {npc_id}")
        generate_portrait(npc_id, draw_fn, has_talking)
    print(f"\n✓ All portraits → {OUT_DIR}")


if __name__ == "__main__":
    main()
