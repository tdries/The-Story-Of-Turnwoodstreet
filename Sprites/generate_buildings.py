#!/usr/bin/env python3
"""
Turnhoutsebaan Building Facade Generator
==========================================
Generates pixel-art building tiles based on the REAL shops along
Turnhoutsebaan / Borgerhout, Antwerp — as documented in Streetdata.md.

Tile order follows house-number sequence (Borgerhout existing game shops first,
then additional businesses from the street data).

Each tile: 48 game-px wide × 112 game-px tall
Scale:      4 px per game pixel  →  192×448 px per tile PNG
Tileset:   20 tiles side-by-side → building_tiles.png  (3840×448 px)

Tile index  House nr  Name                     ID (in game)
-----------  --------  ----------------------   -----------
 0           137       Indian Boutique          indian_boutique
 1           170       Patisserie Aladdin       aladdin
 2           180       Brasserie 't Center      brasserie_center
 3           189       Bakkerij Charif          charif
 4           200       Frituur de Tram          frituur
 5           215       Theehuys Amal            theehuys
 6           239       Mimoun                   mimoun
 7           240       Nacht Winkel             nachtw
 8           260       Hammam Borgerhout        hammam
 9           284       Borger Hub               borgerHub
10           317       Apotheek Praats          apotheek
11           326       Budget Market            budgetmkt
12           332       Costermans Wielersport   costermans
13           360       Basic-Fit                basic_fit
14           370       New Star Kebab           newstar
15           —         Carrefour Market         carrefour
16           (brick)   Woonhuis A               brick_a
17           (brick)   Woonhuis B               brick_b
18           (brick)   Woonhuis C               brick_c
19           (vacant)  Leegstand                vacant

Usage:
  python3 generate_buildings.py
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────────────────────────
SCALE      = 8          # px per game pixel  (doubled → crisper fonts, sharper sprites)
TW, TH     = 48, 112   # tile size in game pixels (unchanged — Phaser displays at 2× width)
PW, PH     = TW * SCALE, TH * SCALE   # 384 × 896 px per tile
NUM_TILES  = 20

OUT_DIR    = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Sprites', 'buildings')
OUT_FILE   = os.path.join(OUT_DIR, 'building_tiles.png')

# ── Font setup ────────────────────────────────────────────────────────────────
# Try macOS system fonts first, then Linux, then PIL default
def _load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/Arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                pass
    return ImageFont.load_default()

def fit_font(text: str, max_w_px: int, start_size: int = 60, min_size: int = 12) -> ImageFont.ImageFont:
    """Return the largest font that renders `text` within `max_w_px` pixels."""
    size = start_size
    while size >= min_size:
        fnt = _load_font(size)
        try:
            bb = fnt.getbbox(text)
            w  = bb[2] - bb[0]
        except Exception:
            # fallback: use textbbox via a throwaway draw
            import io
            tmp_img = Image.new('RGBA', (1, 1))
            tmp_d   = ImageDraw.Draw(tmp_img)
            bb      = tmp_d.textbbox((0, 0), text, font=fnt)
            w       = bb[2] - bb[0]
        if w <= max_w_px:
            return fnt
        size -= 4
    return _load_font(min_size)

FONT_LG = _load_font(16)   # legacy (sign_band now calls fit_font instead)
FONT_SM = _load_font(40)   # house numbers — large and readable

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    'sky_l':      (0x78, 0xAF, 0xE1),
    'sky_m':      (0xA8, 0xCB, 0xE8),
    # Brick (Flemish red-orange)
    'brick_d':    (0x6E, 0x2C, 0x18),
    'brick_m':    (0x98, 0x44, 0x28),
    'brick_l':    (0xC0, 0x70, 0x50),
    'mortar':     (0xD4, 0xB8, 0x98),
    # Stone / Render
    'stone_d':    (0x60, 0x60, 0x58),
    'stone_m':    (0x88, 0x88, 0x80),
    'stone_l':    (0xB4, 0xB0, 0xA8),
    'stone_p':    (0xD8, 0xD4, 0xCC),
    # Cream / Ochre render
    'cream_d':    (0xC8, 0xA8, 0x6C),
    'cream_m':    (0xE8, 0xCF, 0xA0),
    'cream_l':    (0xF4, 0xE8, 0xC8),
    'ochre':      (0xD4, 0xA0, 0x40),
    'terra':      (0xB8, 0x60, 0x30),   # terracotta
    'terra_l':    (0xD4, 0x88, 0x58),
    # Wood
    'wood_d':     (0x4A, 0x2C, 0x10),
    'wood_m':     (0x7A, 0x46, 0x20),
    'wood_l':     (0x8A, 0x5A, 0x28),
    # Glass
    'glass_d':    (0x18, 0x28, 0x38),
    'glass_m':    (0x28, 0x48, 0x68),
    'glass_l':    (0xA0, 0xC8, 0xE4),
    'glass_lit':  (0xF4, 0xE8, 0x88),
    # Roof
    'slate_d':    (0x28, 0x28, 0x30),
    'slate_m':    (0x44, 0x44, 0x50),
    # Sign / brand colours
    'white':      (0xF0, 0xEE, 0xE8),
    'off_white':  (0xE8, 0xE4, 0xD8),
    'black':      (0x14, 0x12, 0x10),
    'red':        (0xCC, 0x20, 0x10),
    'red_dk':     (0x88, 0x10, 0x08),
    'green_d':    (0x0C, 0x44, 0x1C),
    'green_m':    (0x18, 0x80, 0x38),
    'green_l':    (0x4C, 0xB8, 0x68),
    'yellow':     (0xDD, 0xB8, 0x00),
    'gold':       (0xFF, 0xD7, 0x00),
    'blue_d':     (0x0C, 0x2C, 0x68),
    'blue_m':     (0x1C, 0x58, 0x98),
    'blue_l':     (0x48, 0x90, 0xCC),
    'orange':     (0xD4, 0x6C, 0x14),
    'teal_d':     (0x0C, 0x44, 0x44),
    'teal_m':     (0x18, 0x80, 0x80),
    'teal_l':     (0x4C, 0xB0, 0xB0),
    'purple':     (0x70, 0x30, 0x80),
    'grey_d':     (0x28, 0x28, 0x28),
    'grey_m':     (0x48, 0x48, 0x48),
    'grey_l':     (0x88, 0x88, 0x88),
    'neon_g':     (0x20, 0xFF, 0x80),
    'neon_b':     (0x40, 0xC8, 0xFF),
    'sidewalk':   (0xB4, 0xAE, 0x9E),
    'night':      (0x0C, 0x0C, 0x18),
    'pink':       (0xD4, 0x5C, 0x88),
}


# ── Low-level drawing helpers ─────────────────────────────────────────────────
def S(x: int) -> int:
    """Convert game-pixels to PNG pixels."""
    return x * SCALE


def R(d: ImageDraw.Draw, x1: int, y1: int, x2: int, y2: int, col: tuple):
    """Filled rectangle in game-pixel coordinates (exclusive x2/y2)."""
    d.rectangle([S(x1), S(y1), S(x2) - 1, S(y2) - 1], fill=col + (255,) if len(col) == 3 else col)


def HL(d, x1, x2, y, col):
    """Horizontal line (1 game-px tall)."""
    R(d, x1, y, x2, y + 1, col)


def VL(d, x, y1, y2, col):
    """Vertical line (1 game-px wide)."""
    R(d, x, y1, x + 1, y2, col)


def PX(d, x, y, col):
    """Single game-pixel."""
    R(d, x, y, x + 1, y + 1, col)


def new_tile() -> tuple[Image.Image, ImageDraw.Draw]:
    """Create blank transparent tile.

    Sky background is intentionally left transparent so the scene's own sky
    gradient shows through — both in the trapgevel step gaps and above facades.
    This guarantees a perfect colour match regardless of camera position.
    """
    img = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    return img, d


def brick_fill(d, x1, y1, x2, y2, b_mid=None, b_lt=None, b_dk=None):
    """Flemish-bond brick pattern."""
    bm = b_mid or C['brick_m']
    bl = b_lt  or C['brick_l']
    bd = b_dk  or C['brick_d']
    mo = C['mortar']
    R(d, x1, y1, x2, y2, mo)
    bh, bw = 4, 8
    for row in range((y2 - y1) // bh + 2):
        by = y1 + row * bh
        if by >= y2: break
        offset = (bw // 2) if (row % 2) else 0
        for col in range(-1, (x2 - x1) // bw + 2):
            bx = x1 + col * bw + offset
            lx1 = max(bx, x1);   ly1 = by
            lx2 = min(bx + bw - 1, x2 - 1)
            ly2 = min(by + bh - 2, y2 - 1)
            if lx2 < lx1 or ly2 < ly1: continue
            c = bd if (row + col) % 5 == 0 else (bl if (row + col) % 3 == 0 else bm)
            R(d, lx1, ly1, lx2 + 1, ly2 + 1, c)


def stone_render(d, x1, y1, x2, y2, col_m=None, col_l=None, col_d=None):
    """Smooth cream / stone render with horizontal joints."""
    cm = col_m or C['cream_m']
    cl = col_l or C['cream_l']
    cd = col_d or C['cream_d']
    R(d, x1, y1, x2, y2, cm)
    HL(d, x1, x2, y1, cl)
    for y in range(y1 + 8, y2, 8):
        HL(d, x1, x2, y, cd)


def window_rect(d, x, y, w, h, lit=False):
    """Rectangular window with frame."""
    R(d, x, y, x + w, y + h, C['stone_d'])
    glass = C['glass_lit'] if lit else C['glass_d']
    R(d, x + 1, y + 1, x + w - 1, y + h - 1, glass)
    if lit:
        HL(d, x + 1, x + w - 1, y + 1, C['glass_l'])
    else:
        PX(d, x + 1, y + 1, C['glass_m'])


def arch_win(d, x, y, w, h, glass=None, frame=None):
    """Arched window (semicircle top)."""
    fc = frame or C['stone_d']
    gc = glass or C['glass_d']
    r  = w // 2
    ah = r  # arch height
    # Rectangle body
    R(d, x, y + ah, x + w, y + h, fc)
    R(d, x + 1, y + ah, x + w - 1, y + h - 1, gc)
    # Rasterised arch
    cx = x + r
    for dy in range(ah + 1):
        hw = int(math.sqrt(max(0, r * r - (ah - dy) ** 2)))
        if hw >= 1:
            R(d, cx - hw, y + dy, cx + hw, y + dy + 1, fc)
            if hw >= 2:
                R(d, cx - hw + 1, y + dy, cx + hw - 1, y + dy + 1, gc)


def awning_stripe(d, x1, x2, y, col1, col2, depth=5):
    """Striped awning."""
    for i in range(x2 - x1):
        c = col1 if (i % 4 < 2) else col2
        VL(d, x1 + i, y, y + depth, c)
    HL(d, x1, x2, y + depth, C['stone_d'])


def sign_band(d, img, x1: int, y1: int, x2: int, y2: int,
              bg: tuple, text: str, text_col: tuple = None,
              font: ImageFont.ImageFont = None, sub: str = ''):
    """
    Draw a sign band with auto-fitted readable text + large house number.
    Coordinates in GAME pixels; text drawn in PNG pixels for sharpness.

    Layout when sub (house number) is present:
      TOP HALF  — house number (FONT_SM ≈40px, auto-fit to half-band width)
      BOT HALF  — shop name   (auto-fit to full band width)
    Without sub: shop name centred in full band.
    """
    R(d, x1, y1, x2, y2, bg)
    HL(d, x1, x2, y1, (
        min(bg[0] + 40, 255),
        min(bg[1] + 40, 255),
        min(bg[2] + 40, 255),
    ))
    HL(d, x1, x2, y2 - 1, (
        max(bg[0] - 40, 0),
        max(bg[1] - 40, 0),
        max(bg[2] - 40, 0),
    ))

    tc   = text_col or C['white']
    px1, py1, px2, py2 = S(x1), S(y1), S(x2), S(y2)
    band_w = px2 - px1 - 4        # usable PNG-px width (2px padding each side)
    band_h = py2 - py1
    cx     = (px1 + px2) // 2

    def _draw_text(label, fnt, cx_, cy_):
        bb = d.textbbox((0, 0), label, font=fnt)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        tx = cx_ - tw // 2
        ty = cy_ - th // 2
        d.text((tx + 1, ty + 1), label, fill=(0, 0, 0, 180), font=fnt)
        d.text((tx, ty), label, fill=tc + (255,) if len(tc) == 3 else tc, font=fnt)

    if sub:
        # House number in top half — large font, auto-fit to half band width
        num_fnt = fit_font(sub,  band_w // 2, start_size=80, min_size=28)
        nam_fnt = fit_font(text, band_w,      start_size=112, min_size=20)
        cy_num = py1 + band_h // 4
        cy_nam = py1 + 3 * band_h // 4
        _draw_text(sub,  num_fnt, px1 + band_w // 4, cy_num)  # left-ish
        _draw_text(text, nam_fnt, cx,                cy_nam)
    else:
        nam_fnt = fit_font(text, band_w, start_size=112, min_size=20)
        _draw_text(text, nam_fnt, cx, (py1 + py2) // 2)


def plinth(d, ground_y=104):
    """Standard plinth + sidewalk at bottom of tile."""
    R(d, 0, ground_y, TW, ground_y + 4, C['stone_d'])
    HL(d, 0, TW, ground_y, C['stone_l'])
    R(d, 0, ground_y + 4, TW, TH, C['sidewalk'])
    HL(d, 0, TW, ground_y + 4, C['stone_m'])


def draw_trapgevel(d, body_col):
    """
    Classic Flemish stepped gable (trapgevel) painted at y=0..16 of the tile.
    Call LAST in each draw_* function so it overlays any sky background.
    body_col : main building material colour (3-tuple RGB).
    Sky shows through the gaps between wider and narrower steps, creating
    the authentic Antwerp roofline silhouette.
    """
    mc_l = tuple(min(c + 48, 255) for c in body_col[:3])
    mc_d = tuple(max(c - 36, 0)   for c in body_col[:3])
    CX   = TW // 2   # = 24
    # Each entry: (y_start, y_end, half_width_from_centre)
    # Sky shows in the "notch" between each step's wider base
    steps = [
        (0,  3,  4),    # tip:         x = 20–28  (8 px wide)
        (3,  6,  8),    # step 1:      x = 16–32  (16 px wide)
        (6,  9,  13),   # step 2:      x = 11–37  (26 px wide)
        (9,  12, 19),   # step 3:      x =  5–43  (38 px wide)
        (12, 16, 24),   # base cornice: full width (48 px)
    ]
    for y1, y2, hw in steps:
        x1, x2 = CX - hw, CX + hw
        R(d, x1, y1, x2, y2, body_col)
        HL(d, x1, x2, y1, mc_l)          # top-edge highlight
        VL(d, x1, y1 + 1, y2, mc_l)      # left-edge highlight
        VL(d, x2 - 1, y1 + 1, y2, mc_d)  # right-edge shadow


def door(d, x, y, w=12, h=18, col=None):
    dc = col or C['wood_d']
    R(d, x, y, x + w, y + h, dc)
    R(d, x + 1, y + 1, x + w - 1, y + h - 1, C['wood_l'])
    R(d, x + 2, y + 2, x + w - 2, y + h // 2, C['wood_m'])


# ── Individual building draw functions ────────────────────────────────────────

def draw_indian_boutique(img, d):
    """#137 Indian Boutique — Borgerhout — exotic products, colourful fabrics."""
    brick_fill(d, 0, 18, TW, 50)
    # Upper decorative band
    for x in range(0, TW, 3):
        cs = [C['orange'], C['red'], C['yellow'], C['teal_m'], C['purple']]
        R(d, x, 18, x + 3, 22, cs[(x // 3) % len(cs)])

    sign_band(d, img, 0, 50, TW, 64, C['orange'],
              'Indian Boutique', C['white'], FONT_LG, '#137')

    awning_stripe(d, 0, TW, 66, C['orange'], C['yellow'])

    # Display window
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_m'])
    # Fabric rolls (colourful)
    for i, fx in enumerate(range(3, TW - 4, 5)):
        fabrics = [C['red'], C['orange'], C['yellow'], C['teal_m'], C['purple'], C['pink']]
        R(d, fx, 76, fx + 4, 92, fabrics[i % len(fabrics)])
        HL(d, fx, fx + 4, 76, (255, 255, 255, 80))

    door(d, 18, 94, 12, 10)
    plinth(d)


def draw_patisserie_aladdin(img, d):
    """#170 Patisserie Aladdin — cream render, yellow awning, Arabic signage."""
    stone_render(d, 0, 14, TW, 50, C['cream_m'], C['cream_l'], C['cream_d'])
    # Ornate cornice
    R(d, 0, 14, TW, 18, C['ochre'])
    HL(d, 0, TW, 14, C['gold'])

    # Arched windows upper floor
    arch_win(d, 4, 20, 16, 28, C['glass_lit'])
    arch_win(d, 28, 20, 16, 28, C['glass_lit'])

    sign_band(d, img, 0, 50, TW, 64, C['yellow'],
              'Patisserie Aladdin', C['black'], FONT_LG, '#170')

    awning_stripe(d, 0, TW, 66, C['yellow'], C['cream_l'])

    # Shopfront
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_lit'])
    # Pastry display (golden blobs)
    for bx in range(3, TW - 4, 4):
        R(d, bx, 84, bx + 3, 92, C['ochre'])
        PX(d, bx + 1, 85, C['gold'])

    door(d, 18, 94)
    plinth(d)


def draw_brasserie_center(img, d):
    """#180 Brasserie 't Center — classic Antwerp café, red brick, brass fittings."""
    brick_fill(d, 0, 16, TW, 50)
    # Ornate cornice
    R(d, 0, 14, TW, 18, C['stone_d'])
    for sx in range(2, TW, 6):
        R(d, sx, 14, sx + 3, 18, C['stone_l'])

    window_rect(d, 2, 22, 14, 16, lit=True)
    window_rect(d, 32, 22, 14, 16, lit=True)

    sign_band(d, img, 0, 50, TW, 64, C['brick_d'],
              "Brasserie 't Center", C['gold'], FONT_LG, '#180')

    awning_stripe(d, 0, TW, 66, C['red_dk'], C['cream_l'])

    # Bar interior window
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_lit'])
    # Bar stools silhouette
    for bx in [4, 10, 18, 26, 34, 40]:
        VL(d, bx, 84, 93, C['stone_d'])
        R(d, bx - 1, 84, bx + 3, 87, C['stone_d'])

    door(d, 18, 94)
    plinth(d)


def draw_bakkerij_charif(img, d):
    """#189 Bakkerij Charif — cream render, yellow awning, bread in window."""
    stone_render(d, 0, 14, TW, 50, C['cream_m'], C['cream_l'])

    arch_win(d, 6, 20, 14, 26, C['glass_lit'])
    arch_win(d, 26, 20, 14, 26, C['glass_lit'])

    sign_band(d, img, 0, 50, TW, 64, C['yellow'],
              'Bakkerij Charif', C['black'], FONT_LG, '#189')

    awning_stripe(d, 0, TW, 66, C['yellow'], C['white'])

    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_lit'])
    # Bread loaves
    for bx in range(3, TW - 4, 5):
        R(d, bx, 84, bx + 4, 91, C['ochre'])
        R(d, bx + 1, 82, bx + 3, 85, C['cream_l'])
        HL(d, bx, bx + 4, 84, C['cream_m'])

    door(d, 18, 94)
    plinth(d)


def draw_frituur_de_tram(img, d):
    """#200 Frituur de Tram — white/red classic Belgian frituur, tram silhouette."""
    # White tiled facade
    R(d, 0, 14, TW, 50, C['white'])
    for y in range(14, 50, 4): HL(d, 0, TW, y, C['stone_l'])
    for x in range(0, TW, 4): VL(d, x, 14, 50, C['stone_l'])

    # Roof vent / chimney
    R(d, 34, 6, 40, 16, C['stone_m'])
    R(d, 33, 4, 41, 8, C['stone_l'])
    for sy in range(0, 4, 1):
        PX(d, 36 + sy % 2, sy, C['stone_l'])

    sign_band(d, img, 0, 50, TW, 64, C['red'],
              'Frituur de Tram', C['white'], FONT_LG, '#200')

    awning_stripe(d, 0, TW, 66, C['red'], C['yellow'])

    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_m'])
    # Fry baskets
    for bx in [4, 14, 24, 34]:
        R(d, bx, 80, bx + 8, 92, C['yellow'])
        for fy in range(82, 92, 2):
            HL(d, bx, bx + 8, fy, C['ochre'])

    door(d, 18, 94, 12, 10, C['stone_d'])
    plinth(d)


def draw_theehuys_amal(img, d):
    """#215 Theehuys Amal — ochre, teal shutters, Arabic + Dutch sign."""
    stone_render(d, 0, 14, TW, 50, C['ochre'], C['cream_l'], C['cream_d'])
    HL(d, 0, TW, 14, C['gold'])

    # Upper windows with teal shutters
    for wx in [3, 28]:
        window_rect(d, wx, 20, 16, 20, lit=True)
        # Shutters
        R(d, wx - 3, 20, wx, 40, C['teal_d'])
        R(d, wx + 16, 20, wx + 19, 40, C['teal_d'])
        for sy in range(22, 38, 3):
            HL(d, wx - 3, wx, sy, C['teal_m'])
            HL(d, wx + 16, wx + 19, sy, C['teal_m'])

    sign_band(d, img, 0, 50, TW, 64, C['teal_d'],
              'Theehuys Amal', C['gold'], FONT_LG, '#215')

    awning_stripe(d, 0, TW, 66, C['teal_d'], C['cream_l'])

    # Cosy interior view
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_lit'])
    # Small tables
    for tx in [5, 22, 36]:
        R(d, tx, 86, tx + 8, 88, C['wood_d'])
        VL(d, tx + 3, 88, 93, C['wood_m'])
        VL(d, tx + 6, 88, 93, C['wood_m'])
    # Teapot silhouette
    R(d, 18, 78, 28, 85, C['stone_d'])

    door(d, 18, 94)
    plinth(d)


def draw_mimoun(img, d):
    """#239 Mimoun — geschenken & huishoudartikelen, colourful window display."""
    brick_fill(d, 0, 16, TW, 50)
    window_rect(d, 2, 22, 14, 16)
    window_rect(d, 32, 22, 14, 16)

    sign_band(d, img, 0, 50, TW, 64, C['purple'],
              'Mimoun', C['white'], FONT_LG, '#239 · Geschenken')

    awning_stripe(d, 0, TW, 66, C['purple'], C['cream_l'])

    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_m'])
    # Gift items / pottery display
    items = [C['teal_m'], C['orange'], C['red'], C['yellow'], C['purple'], C['teal_l'], C['pink']]
    for i, ix in enumerate(range(3, TW - 4, 6)):
        R(d, ix, 80, ix + 4, 92, items[i % len(items)])
        PX(d, ix + 2, 80, C['gold'])

    door(d, 18, 94)
    plinth(d)


def draw_nacht_winkel(img, d):
    """#240 Nacht Winkel — dark grey, neon signage, always lit up."""
    # Dark grey facade — always open, night atmosphere
    R(d, 0, 12, TW, 50, C['grey_d'])
    for y in range(12, 50, 6): HL(d, 0, TW, y, C['grey_m'])
    brick_fill(d, 0, 12, TW, 30, C['grey_m'], C['grey_l'], C['grey_d'])

    # Neon sign (green)
    sign_band(d, img, 0, 50, TW, 66, C['grey_d'],
              'Nacht Winkel', C['neon_g'], FONT_LG, '#240 · OPEN 24U')

    # Neon border glow effect
    R(d, 0, 50, 2, 66, C['neon_g'])
    R(d, TW - 2, 50, TW, 66, C['neon_g'])

    # Lit shop window
    R(d, 1, 68, TW - 1, 94, C['stone_d'])
    R(d, 2, 69, TW - 2, 93, C['night'])
    # Products with neon glow
    for i, px_x in enumerate(range(3, TW - 4, 5)):
        c = [C['neon_g'], C['neon_b'], C['yellow'], C['red']][i % 4]
        R(d, px_x, 72, px_x + 4, 92, C['grey_d'])
        R(d, px_x + 1, 73, px_x + 3, 91, c)

    door(d, 18, 94, 12, 10, C['grey_m'])
    plinth(d)


def draw_hammam(img, d):
    """#260 Hammam Borgerhout — terracotta render, teal tiled arch, ornate."""
    stone_render(d, 0, 10, TW, 50, C['terra'], C['terra_l'], C['cream_d'])
    HL(d, 0, TW, 10, C['gold'])

    # Mosaic border at top
    tile_cs = [C['teal_m'], C['blue_m'], C['gold'], C['green_m'], C['teal_d']]
    for x in range(TW):
        R(d, x, 12, x + 1, 16, tile_cs[x % len(tile_cs)])
    for x in range(TW):
        R(d, x, 17, x + 1, 21, tile_cs[(x + 2) % len(tile_cs)])

    # Upper arched window
    arch_win(d, 14, 22, 20, 26, C['glass_lit'], C['teal_d'])

    sign_band(d, img, 0, 50, TW, 64, C['teal_d'],
              'Hammam Borgerhout', C['gold'], FONT_LG, '#260')

    # Mosaic band below sign
    for x in range(TW):
        R(d, x, 65, x + 1, 68, tile_cs[(x + 1) % len(tile_cs)])

    # Large horseshoe arch entrance
    arch_win(d, 4, 70, 40, 34, C['glass_lit'], C['teal_d'])
    # Inner reveal
    arch_win(d, 7, 72, 34, 30, C['glass_lit'], C['teal_m'])

    # Pilasters flanking
    R(d, 0, 70, 5, 104, C['terra'])
    VL(d, 1, 72, 102, C['terra_l'])
    R(d, TW - 5, 70, TW, 104, C['terra'])
    VL(d, TW - 2, 72, 102, C['terra_l'])

    plinth(d)


def draw_borger_hub(img, d):
    """#284 Borger Hub — renovated community space, grey, modern green accents."""
    # Modern renovated facade: smooth grey
    R(d, 0, 12, TW, 50, C['grey_m'])
    HL(d, 0, TW, 12, C['grey_l'])
    # Horizontal band accents
    HL(d, 0, TW, 18, C['green_m'])
    HL(d, 0, TW, 19, C['green_m'])

    # Large modern windows
    window_rect(d, 2, 22, 20, 22, lit=True)
    window_rect(d, 26, 22, 20, 22, lit=True)

    sign_band(d, img, 0, 50, TW, 65, C['green_d'],
              'Borger Hub', C['white'], FONT_LG, '#284 · Gemeenschapsruimte')

    # Green accent stripe
    R(d, 0, 67, TW, 70, C['green_m'])

    # Glass shopfront
    R(d, 1, 72, TW - 1, 94, C['grey_d'])
    R(d, 2, 73, TW - 2, 93, C['glass_l'])
    # Interior — community space: chairs, table
    R(d, 10, 82, 38, 84, C['wood_d'])
    for cx in [12, 18, 24, 30, 36]:
        R(d, cx - 1, 84, cx + 2, 92, C['stone_m'])

    door(d, 18, 94, 12, 10, C['grey_d'])
    plinth(d)


def draw_apotheek_praats(img, d):
    """Apotheek Praats — Wijnegem #317 — white render, green cross."""
    R(d, 0, 14, TW, 50, C['white'])
    for y in range(14, 50, 8): HL(d, 0, TW, y, C['stone_l'])

    # Green cross (iconic pharmacy symbol)
    cross_x, cross_y = 18, 18
    R(d, cross_x, cross_y, cross_x + 12, cross_y + 4, C['green_m'])
    R(d, cross_x + 4, cross_y - 4, cross_x + 8, cross_y + 8, C['green_m'])
    HL(d, cross_x, cross_x + 12, cross_y, C['green_l'])
    HL(d, cross_x + 4, cross_x + 8, cross_y - 4, C['green_l'])

    sign_band(d, img, 0, 50, TW, 64, C['green_d'],
              'Apotheek Praats', C['white'], FONT_LG, '#317 Wijnegem')

    awning_stripe(d, 0, TW, 66, C['green_d'], C['white'])

    # Window + medicine display
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_l'])
    for mx in [4, 14, 28, 38]:
        R(d, mx, 78, mx + 8, 92, C['green_d'])
        R(d, mx + 1, 79, mx + 7, 84, C['green_l'])
        VL(d, mx + 3, 80, 83, C['white'])
        HL(d, mx + 1, mx + 7, 81, C['white'])

    door(d, 18, 94)
    plinth(d)


def draw_budget_market(img, d):
    """#326 Budget Market — red brick, 4 stories, wide red awning."""
    brick_fill(d, 0, 8, TW, 50)
    # 4-storey facade — extra windows
    # Top storey
    window_rect(d, 2, 10, 12, 8)
    window_rect(d, 18, 10, 12, 8)
    window_rect(d, 34, 10, 12, 8)
    # 3rd floor
    window_rect(d, 2, 22, 12, 10, lit=True)
    window_rect(d, 18, 22, 12, 10)
    window_rect(d, 34, 22, 12, 10)
    # 2nd floor
    window_rect(d, 2, 36, 12, 10)
    window_rect(d, 18, 36, 12, 10, lit=True)
    window_rect(d, 34, 36, 12, 10)

    sign_band(d, img, 0, 50, TW, 64, C['red'],
              'Budget Market', C['white'], FONT_LG, '#326')

    awning_stripe(d, 0, TW, 66, C['red'], C['white'], depth=7)

    # Wide shopfront
    R(d, 1, 75, TW - 1, 94, C['stone_d'])
    R(d, 2, 76, TW - 2, 93, C['glass_m'])
    # Shelves visible through window
    for sy in range(78, 92, 4):
        HL(d, 2, TW - 2, sy, C['stone_d'])
        for sx in range(4, TW - 4, 4):
            R(d, sx, sy - 3, sx + 3, sy, [C['red'], C['yellow'], C['orange'],
                                           C['blue_m'], C['green_m']][(sx // 4) % 5])

    door(d, 19, 94, 10, 10, C['stone_d'])
    plinth(d)


def draw_costermans(img, d):
    """#332 Costermans Wielersport — fietsenwinkel, Wijnegem."""
    brick_fill(d, 0, 16, TW, 50)
    window_rect(d, 2, 22, 16, 18)
    window_rect(d, 30, 22, 16, 18)

    sign_band(d, img, 0, 50, TW, 64, C['blue_d'],
              'Costermans Wielersport', C['white'], FONT_LG, '#332 · Fietsen')

    awning_stripe(d, 0, TW, 66, C['blue_d'], C['blue_l'])

    # Bike display in window
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_l'])
    # Simplified bicycle silhouettes
    for bx in [4, 24]:
        # Wheels
        for wx in [bx + 2, bx + 12]:
            for dy in range(-4, 5):
                hw = int(math.sqrt(max(0, 16 - dy * dy)))
                if hw:
                    R(d, wx - hw, 86 + dy, wx + hw, 87 + dy, C['stone_d'])
            R(d, wx - 2, 84, wx + 2, 88, C['grey_l'])  # rim
        # Frame
        R(d, bx + 2, 82, bx + 14, 87, C['blue_m'])
        VL(d, bx + 8, 78, 87, C['blue_m'])

    door(d, 18, 94)
    plinth(d)


def draw_basic_fit(img, d):
    """#360 Basic-Fit — dark grey, large blue logo, gym."""
    R(d, 0, 10, TW, 50, C['grey_d'])
    HL(d, 0, TW, 10, C['grey_m'])
    # Concrete texture
    for y in range(12, 50, 8): HL(d, 0, TW, y, C['grey_m'])

    # Large logo area
    R(d, 4, 18, TW - 4, 48, C['blue_m'])
    R(d, 5, 19, TW - 5, 47, C['blue_d'])
    # "BF" pixel art
    for px_x in [8, 9, 10, 11]: VL(d, px_x, 22, 44, C['blue_l'])
    HL(d, 8, 18, 22, C['blue_l'])
    HL(d, 8, 16, 32, C['blue_l'])
    HL(d, 8, 18, 43, C['blue_l'])
    for px_x in [24, 25, 26, 27]: VL(d, px_x, 22, 44, C['blue_l'])
    HL(d, 24, 36, 22, C['blue_l'])
    HL(d, 24, 34, 32, C['blue_l'])

    sign_band(d, img, 0, 50, TW, 64, C['blue_m'],
              'Basic-Fit', C['white'], FONT_LG, '#360 · Fitness')

    # Glass entrance
    R(d, 0, 66, TW, 94, C['grey_d'])
    R(d, 2, 68, TW - 2, 93, C['glass_m'])
    HL(d, 2, TW - 2, 68, C['blue_l'])

    door(d, 16, 94, 16, 10, C['grey_m'])
    plinth(d)


def draw_new_star_kebab(img, d):
    """#370 New Star Kebab — terracotta, red awning, doner sign."""
    stone_render(d, 0, 14, TW, 50, C['terra'], C['terra_l'])
    HL(d, 0, TW, 14, C['cream_l'])

    # Upper windows
    arch_win(d, 4, 18, 16, 28, C['glass_lit'])
    arch_win(d, 28, 18, 16, 28, C['glass_lit'])

    # Doner rotating sign (vertical cylinder)
    R(d, 40, 16, 47, 46, C['stone_d'])
    for ry in range(18, 44, 4):
        cs = [C['red'], C['cream_m'], C['red'], C['ochre']]
        R(d, 41, ry, 46, ry + 3, cs[(ry // 4) % len(cs)])

    sign_band(d, img, 0, 50, TW, 64, C['red'],
              'New Star Kebab', C['white'], FONT_LG, '#370')

    awning_stripe(d, 0, TW, 66, C['red'], C['cream_l'])

    # Grill / counter visible through window
    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_lit'])
    R(d, 4, 84, TW - 4, 88, C['grey_d'])   # counter
    # Flames on grill
    for fx in range(5, TW - 5, 4):
        R(d, fx, 80, fx + 2, 84, C['orange'])
        PX(d, fx + 1, 79, C['yellow'])

    door(d, 18, 94)
    plinth(d)


def draw_carrefour(img, d):
    """Carrefour Market — supermarket, large white facade, blue/red logo."""
    R(d, 0, 12, TW, 50, C['white'])
    HL(d, 0, TW, 12, C['stone_l'])
    for y in range(14, 50, 8): HL(d, 0, TW, y, C['stone_p'])

    # Carrefour logo colours (blue / red arrows)
    R(d, 14, 20, 24, 44, C['blue_m'])
    R(d, 24, 20, 34, 44, C['red'])
    HL(d, 14, 34, 30, C['white'])
    HL(d, 14, 34, 31, C['white'])

    sign_band(d, img, 0, 50, TW, 64, C['blue_m'],
              'Carrefour Market', C['white'], FONT_LG, 'Supermarkt')

    awning_stripe(d, 0, TW, 66, C['blue_m'], C['red'])

    R(d, 1, 73, TW - 1, 94, C['stone_d'])
    R(d, 2, 74, TW - 2, 93, C['glass_l'])
    # Produce shelves
    for sy in range(76, 92, 4):
        HL(d, 2, TW - 2, sy, C['stone_d'])
        for sx in range(3, TW - 3, 4):
            R(d, sx, sy - 3, sx + 3, sy,
              [C['red'], C['yellow'], C['green_m'], C['orange'], C['teal_m']][(sx // 4) % 5])

    door(d, 18, 94, 12, 10, C['stone_d'])
    plinth(d)


def draw_brick_a(img, d):
    """Antwerp red-brick rowhouse — 3 upper floors + residential ground floor."""
    brick_fill(d, 0, 16, TW, 62)
    # 3rd floor windows
    window_rect(d, 2, 19, 14, 12)
    window_rect(d, 30, 19, 14, 12)
    # 2nd floor windows
    window_rect(d, 2, 35, 14, 12, lit=True)
    window_rect(d, 30, 35, 14, 12)
    # 1st floor windows
    window_rect(d, 2, 50, 14, 10)
    window_rect(d, 30, 50, 14, 10)
    # Stone belt course (divides upper brick from ground floor render)
    R(d, 0, 62, TW, 66, C['stone_d'])
    HL(d, 0, TW, 62, C['stone_l'])
    # Ground floor: rendered stone, residential entry
    stone_render(d, 0, 66, TW, 100, C['stone_m'], C['stone_l'], C['stone_d'])
    door(d, TW // 2 - 6, 70, 12, 30)
    window_rect(d, 2, 72, 10, 20)
    window_rect(d, 36, 72, 10, 20)
    # Stone step
    R(d, 0, 100, TW, 104, C['stone_d'])
    HL(d, 0, TW, 100, C['stone_l'])
    plinth(d, 104)


def draw_brick_b(img, d):
    """Antwerp brick rowhouse — 3 upper floors + commercial ground floor."""
    brick_fill(d, 0, 16, TW, 62)
    window_rect(d, 2, 19, 14, 14)
    window_rect(d, 30, 19, 14, 14, lit=True)
    window_rect(d, 2, 37, 14, 13, lit=True)
    window_rect(d, 30, 37, 14, 13)
    window_rect(d, 2, 53, 14, 7)
    window_rect(d, 30, 53, 14, 7)
    # Stone belt course
    R(d, 0, 62, TW, 66, C['stone_d'])
    HL(d, 0, TW, 62, C['stone_l'])
    # Commercial ground floor: large display window
    stone_render(d, 0, 66, TW, 100, C['cream_m'], C['cream_l'], C['cream_d'])
    R(d, 1, 70, TW - 1, 96, C['stone_d'])
    R(d, 2, 71, TW - 2, 95, C['glass_m'])
    door(d, TW // 2 - 6, 80, 12, 16)
    # Stone step
    R(d, 0, 100, TW, 104, C['stone_d'])
    HL(d, 0, TW, 100, C['stone_l'])
    plinth(d, 104)


def draw_brick_c(img, d):
    """Antwerp brick rowhouse with bay window (erker) — extended to y=104."""
    brick_fill(d, 0, 16, TW, 62)
    # 3rd floor windows
    window_rect(d, 2, 19, 14, 14)
    window_rect(d, 30, 19, 14, 14, lit=True)
    # Bay window (erker) on 2nd floor — projects slightly
    R(d, 8, 35, 40, 60, C['stone_m'])
    window_rect(d, 9, 38, 30, 20, lit=True)
    R(d, 6, 33, 42, 37, C['stone_d'])
    HL(d, 6, 42, 33, C['stone_l'])
    HL(d, 6, 42, 60, C['stone_d'])
    # Stone belt course
    R(d, 0, 62, TW, 66, C['stone_d'])
    HL(d, 0, TW, 62, C['stone_l'])
    # Ground floor: residential entry
    stone_render(d, 0, 66, TW, 100, C['stone_m'], C['stone_l'], C['stone_d'])
    door(d, TW // 2 - 6, 70, 12, 30)
    window_rect(d, 2, 72, 10, 18)
    window_rect(d, 36, 72, 10, 18)
    # Stone step
    R(d, 0, 100, TW, 104, C['stone_d'])
    HL(d, 0, TW, 100, C['stone_l'])
    plinth(d, 104)


def draw_vacant(img, d):
    """Leegstand — boarded-up vacant building, extended to plinth y=104."""
    brick_fill(d, 0, 16, TW, 104, b_mid=C['brick_d'], b_lt=C['brick_m'], b_dk=C['brick_d'])
    # Board over upper windows (2 rows × 2 cols)
    for wx, wy in [(2, 20), (28, 20), (2, 40), (28, 40)]:
        R(d, wx, wy, wx + 18, wy + 18, C['wood_d'])
        HL(d, wx, wx + 18, wy + 9, C['wood_l'])
        HL(d, wx, wx + 18, wy, C['wood_l'])
        HL(d, wx, wx + 18, wy + 17, C['wood_m'])
    # Board over lower windows
    for wx, wy in [(2, 60), (28, 60)]:
        R(d, wx, wy, wx + 18, wy + 16, C['wood_d'])
        HL(d, wx, wx + 18, wy + 8, C['wood_l'])
        HL(d, wx, wx + 18, wy, C['wood_l'])
    # Board over shopfront / ground floor
    R(d, 2, 80, TW - 2, 98, C['wood_d'])
    for hy in range(83, 98, 4):
        HL(d, 2, TW - 2, hy, C['wood_l'])
    VL(d, TW // 2, 80, 98, C['wood_l'])
    # Graffiti pixel marks
    for gx, gy, gc in [(5, 84, C['teal_m']), (7, 85, C['teal_m']),
                       (20, 90, C['red']),    (22, 89, C['red']),
                       (35, 83, C['green_m']), (36, 84, C['green_m'])]:
        PX(d, gx, gy, gc)
    # Stone step
    R(d, 0, 100, TW, 104, C['stone_d'])
    HL(d, 0, TW, 100, C['stone_l'])
    plinth(d, 104)


# ── Trapgevel color per tile (body colour for the stepped gable) ──────────────
# Index matches TILES list order below.
TRAPGEVEL_COL = [
    # 0–15 shops
    'brick_m',   # 0  indian_boutique
    'cream_m',   # 1  patisserie_aladdin
    'brick_m',   # 2  brasserie_center
    'cream_m',   # 3  bakkerij_charif
    'white',     # 4  frituur_de_tram
    'ochre',     # 5  theehuys_amal
    'brick_m',   # 6  mimoun
    'grey_d',    # 7  nacht_winkel
    'terra',     # 8  hammam
    'grey_m',    # 9  borger_hub
    'white',     # 10 apotheek_praats
    'brick_m',   # 11 budget_market
    'brick_m',   # 12 costermans
    'grey_d',    # 13 basic_fit
    'terra',     # 14 new_star_kebab
    'white',     # 15 carrefour
    # 16–19 residential / vacant
    'brick_m',   # 16 brick_a
    'brick_m',   # 17 brick_b
    'brick_m',   # 18 brick_c
    'brick_d',   # 19 vacant
]

# ── Tile registry (order = house-number sequence along street) ────────────────
TILES = [
    ('indian_boutique',   draw_indian_boutique),     # #137
    ('aladdin',           draw_patisserie_aladdin),  # #170
    ('brasserie_center',  draw_brasserie_center),    # #180
    ('charif',            draw_bakkerij_charif),     # #189
    ('frituur',           draw_frituur_de_tram),     # #200
    ('theehuys',          draw_theehuys_amal),       # #215
    ('mimoun',            draw_mimoun),              # #239
    ('nachtw',            draw_nacht_winkel),        # #240
    ('hammam',            draw_hammam),              # #260
    ('borgerHub',         draw_borger_hub),          # #284
    ('apotheek',          draw_apotheek_praats),     # #317 Wijnegem
    ('budgetmkt',         draw_budget_market),       # #326
    ('costermans',        draw_costermans),          # #332 Wijnegem
    ('basic_fit',         draw_basic_fit),           # #360
    ('newstar',           draw_new_star_kebab),      # #370
    ('carrefour',         draw_carrefour),           # Carrefour Market
    ('brick_a',           draw_brick_a),             # generic rowhouse A
    ('brick_b',           draw_brick_b),             # generic rowhouse B
    ('brick_c',           draw_brick_c),             # rowhouse with bay window
    ('vacant',            draw_vacant),              # vacant/boarded-up
]

assert len(TILES) == NUM_TILES, f"Expected {NUM_TILES} tiles, got {len(TILES)}"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    sheet = Image.new('RGBA', (PW * NUM_TILES, PH), (0, 0, 0, 0))
    print('=' * 68)
    print('Turnhoutsebaan Building Facade Generator')
    print(f'  Tile: {TW}×{TH} game-px  |  {PW}×{PH} PNG-px  |  {NUM_TILES} tiles')
    print(f'  Sheet: {PW * NUM_TILES}×{PH} px')
    print('=' * 68)

    for i, (name, draw_fn) in enumerate(TILES):
        img, d = new_tile()
        draw_fn(img, d)
        draw_trapgevel(d, C[TRAPGEVEL_COL[i]])   # Flemish stepped gable on top
        sheet.paste(img, (i * PW, 0))
        tile_path = os.path.join(OUT_DIR, f'tile_{i:02d}_{name}.png')
        img.save(tile_path)
        print(f'  {i:2d}  {name:<24}  → tile_{i:02d}_{name}.png')

    sheet.save(OUT_FILE)
    print()
    print(f'✓ Building tileset → {OUT_FILE}')
    print(f'  Tile size: {TW}×{TH} game-px  ({PW}×{PH} px each)')
    print(f'  Sheet:     {PW * NUM_TILES}×{PH} px')


if __name__ == '__main__':
    main()
