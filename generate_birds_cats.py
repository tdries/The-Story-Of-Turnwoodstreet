"""
Sprite sheet generator for pigeons and cats.
Outputs:
  assets/Sprites/birds/pigeons_sheet.png  — 384×32 (12 frames × 32×32)
  assets/Sprites/cats/cats_sheet.png      — 480×32 (15 frames × 32×32)
"""

import os
import math
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def new_frame():
    """Return a blank 32×32 RGBA frame (transparent)."""
    return Image.new("RGBA", (32, 32), (0, 0, 0, 0))


def ellipse(draw, cx, cy, rx, ry, fill, outline=None):
    """Draw a filled ellipse from centre + radii."""
    draw.ellipse(
        [cx - rx, cy - ry, cx + rx, cy + ry],
        fill=fill,
        outline=outline,
    )


def alpha(col, a=255):
    return col + (a,)


# ===========================================================================
# PIGEON SPRITE SHEET
# ===========================================================================

PIGEON_TYPES = [
    # (body, belly, neck_iridescence, wing_tip)
    ((90,  90, 100), (150, 155, 165), (70, 140, 80),  (55,  55,  65)),   # grey
    ((220, 220, 230), (240, 240, 250), (200, 180, 255), (170, 170, 190)),  # white dove
    ((115,  85,  55), (155, 125,  95), (90, 130, 70),  (75,  55,  35)),   # fat brown
]

BEAK_COL   = (220, 130, 30, 255)
EYE_COL    = (180,  30,  30, 255)
LEG_COL    = (220, 120, 100, 255)
TOE_COL    = (200, 100,  80, 255)


def draw_pigeon_sitting(body, belly, neck, wing_tip):
    img = new_frame()
    d   = ImageDraw.Draw(img)

    # Body — plump oval centred at (16,22)
    body_a = alpha(body)
    ellipse(d, 16, 22, 11, 8, body_a)

    # Belly — lighter lower half
    belly_a = alpha(belly)
    ellipse(d, 16, 25, 9, 5, belly_a)

    # Neck iridescence patch
    neck_a = alpha(neck)
    ellipse(d, 17, 17, 4, 3, neck_a)

    # Wing tips — dark polygons on sides
    wt = alpha(wing_tip)
    d.polygon([(5, 20), (10, 18), (9, 27), (4, 26)],  fill=wt)
    d.polygon([(23, 20), (27, 18), (28, 27), (22, 26)], fill=wt)

    # Head — small circle top-right of body
    ellipse(d, 21, 14, 5, 5, body_a)

    # Beak — tiny orange pointing right
    d.polygon([(26, 13), (30, 14), (26, 15)], fill=BEAK_COL)

    # Eye
    d.ellipse([22, 12, 24, 14], fill=EYE_COL)

    # Tail — small triangle at right
    d.polygon([(27, 21), (31, 20), (31, 25), (27, 26)], fill=wt)

    # Legs — two thin pink lines
    for lx in (13, 19):
        d.line([(lx, 29), (lx, 31)], fill=LEG_COL, width=1)
    # Toes
    for lx in (13, 19):
        d.line([(lx - 2, 31), (lx + 2, 31)], fill=TOE_COL, width=1)

    return img


def draw_pigeon_fly_up(body, belly, neck, wing_tip):
    img = new_frame()
    d   = ImageDraw.Draw(img)

    body_a = alpha(body)
    wt     = alpha(wing_tip)

    # Body horizontal ellipse
    ellipse(d, 14, 17, 9, 5, body_a)
    ellipse(d, 14, 18, 7, 4, alpha(belly))

    # Head — forward-right
    ellipse(d, 23, 13, 4, 4, body_a)
    d.polygon([(27, 12), (31, 13), (27, 14)], fill=BEAK_COL)
    d.ellipse([24, 11, 26, 13], fill=EYE_COL)

    # Neck iridescence
    ellipse(d, 20, 15, 3, 2, alpha(neck))

    # Wings swept HIGH — triangles pointing up
    d.polygon([(8, 16), (2, 4), (14, 12)],  fill=wt)   # left wing up
    d.polygon([(20, 14), (26, 3), (30, 12)], fill=wt)   # right wing up

    # Tail behind (left)
    d.polygon([(2, 16), (0, 20), (5, 22), (6, 17)], fill=wt)

    return img


def draw_pigeon_fly_level(body, belly, neck, wing_tip):
    img = new_frame()
    d   = ImageDraw.Draw(img)

    body_a = alpha(body)
    wt     = alpha(wing_tip)

    # Body
    ellipse(d, 14, 17, 9, 5, body_a)
    ellipse(d, 14, 18, 7, 4, alpha(belly))

    # Head
    ellipse(d, 23, 13, 4, 4, body_a)
    d.polygon([(27, 12), (31, 13), (27, 14)], fill=BEAK_COL)
    d.ellipse([24, 11, 26, 13], fill=EYE_COL)

    # Neck
    ellipse(d, 20, 15, 3, 2, alpha(neck))

    # Wings spread WIDE — flat rectangles with pointed tips
    d.polygon([(7, 15), (0, 14), (0, 18), (7, 19)],   fill=wt)   # left
    d.polygon([(21, 14), (31, 13), (31, 17), (21, 18)], fill=wt)  # right

    # Primary feathers (slightly darker shade implied by wing_tip colour)
    body_col = alpha(body)
    d.polygon([(7, 15), (3, 13), (3, 17), (7, 17)],  fill=body_col)
    d.polygon([(21, 14), (27, 12), (27, 16), (21, 16)], fill=body_col)

    # Tail
    d.polygon([(2, 16), (0, 20), (5, 22), (6, 17)], fill=wt)

    return img


def draw_pigeon_fly_down(body, belly, neck, wing_tip):
    img = new_frame()
    d   = ImageDraw.Draw(img)

    body_a = alpha(body)
    wt     = alpha(wing_tip)

    # Body
    ellipse(d, 14, 17, 9, 5, body_a)
    ellipse(d, 14, 18, 7, 4, alpha(belly))

    # Head
    ellipse(d, 23, 13, 4, 4, body_a)
    d.polygon([(27, 12), (31, 13), (27, 14)], fill=BEAK_COL)
    d.ellipse([24, 11, 26, 13], fill=EYE_COL)

    # Neck
    ellipse(d, 20, 15, 3, 2, alpha(neck))

    # Wings swept DOWN — triangles pointing down
    d.polygon([(8, 17), (2, 28), (14, 22)],   fill=wt)  # left
    d.polygon([(20, 17), (26, 29), (30, 22)],  fill=wt)  # right

    # Tail
    d.polygon([(2, 16), (0, 20), (5, 22), (6, 17)], fill=wt)

    return img


PIGEON_FRAME_FNS = [
    draw_pigeon_sitting,
    draw_pigeon_fly_up,
    draw_pigeon_fly_level,
    draw_pigeon_fly_down,
]


def build_pigeons_sheet():
    sheet = Image.new("RGBA", (384, 32), (0, 0, 0, 0))
    col = 0
    for (body, belly, neck, wing_tip) in PIGEON_TYPES:
        for fn in PIGEON_FRAME_FNS:
            frame = fn(body, belly, neck, wing_tip)
            sheet.paste(frame, (col * 32, 0))
            col += 1
    return sheet


# ===========================================================================
# CAT SPRITE SHEET
# ===========================================================================

CAT_TYPES = [
    # (body, belly, eye_col, has_stripes, stripe_col)
    ((210, 120,  40), (230, 180, 120), (80, 160, 80, 255),   True,  (160,  80, 20)),   # orange tabby
    (( 30,  30,  35), ( 45,  45,  50), (200, 230,  50, 255), False, None),             # black cat
    ((140, 140, 150), (190, 190, 200), (70, 160, 200, 255),  True,  (110, 110, 120)),  # grey cat
]

EAR_COL   = None   # will use body colour per type
NOSE_COL  = (220, 100, 120, 255)
WHISKER   = (240, 240, 240, 200)
PAW_COL   = None   # belly colour
TAIL_COL  = None   # body colour


def draw_cat_tail(d, body_col, tip_x=8, tip_y=4):
    """Draw an elegant curved tail arcing upward and to the left from body."""
    tail = alpha(body_col)
    # Bezier-style approximation using a polygon strip
    # Tail base starts around (10, 22), arcs up to (4, 8), curves right to (8, 4)
    points = [
        (12, 24), (10, 22),
        (8,  18), (6,  14),
        (5,  10), (5,   7),
        (6,   5), (8,   4),
        (10,  4), (11,   5),
        (10,  8), (9,  11),
        (9,  15), (10, 19),
        (12, 22), (13, 24),
    ]
    d.polygon(points, fill=tail)


def draw_cat_ears(d, cx, cy, body_col):
    """Two small triangular ears on the head circle."""
    bc = alpha(body_col)
    inner = (230, 160, 160, 255)
    # Left ear
    d.polygon([(cx - 4, cy - 3), (cx - 7, cy - 8), (cx - 1, cy - 7)], fill=bc)
    d.polygon([(cx - 4, cy - 4), (cx - 6, cy - 7), (cx - 2, cy - 6)], fill=inner)
    # Right ear
    d.polygon([(cx + 2, cy - 3), (cx + 5, cy - 8), (cx + 7, cy - 3)], fill=bc)
    d.polygon([(cx + 2, cy - 4), (cx + 5, cy - 7), (cx + 6, cy - 4)], fill=inner)


def draw_cat_face(d, cx, cy, body_col, belly_col, eye_col, has_stripes, stripe_col):
    bc = alpha(body_col)
    # Head
    ellipse(d, cx, cy, 6, 5, bc)
    # Ears
    draw_cat_ears(d, cx, cy, body_col)
    # Eyes — almond shaped
    d.ellipse([cx - 4, cy - 2, cx - 1, cy + 1], fill=eye_col)
    d.ellipse([cx + 1, cy - 2, cx + 4, cy + 1], fill=eye_col)
    # Pupils
    d.ellipse([cx - 3, cy - 1, cx - 2, cy],   fill=(10, 10, 10, 255))
    d.ellipse([cx + 2, cy - 1, cx + 3, cy],   fill=(10, 10, 10, 255))
    # Nose
    d.polygon([(cx - 1, cy + 1), (cx + 1, cy + 1), (cx, cy + 3)], fill=NOSE_COL)
    # Whiskers
    d.line([(cx - 6, cy + 1), (cx - 2, cy + 1)], fill=WHISKER, width=1)
    d.line([(cx + 2, cy + 1), (cx + 6, cy + 1)], fill=WHISKER, width=1)
    d.line([(cx - 6, cy + 2), (cx - 2, cy + 2)], fill=WHISKER, width=1)
    d.line([(cx + 2, cy + 2), (cx + 6, cy + 2)], fill=WHISKER, width=1)


def draw_cat_body(d, body_col, belly_col, bx, by, bw, bh, has_stripes, stripe_col):
    bc = alpha(body_col)
    bl = alpha(belly_col)
    ellipse(d, bx, by, bw, bh, bc)
    ellipse(d, bx, by + 1, bw - 2, bh - 1, bl)
    if has_stripes and stripe_col is not None:
        sc = alpha(stripe_col)
        for sx in range(bx - bw + 4, bx + bw - 2, 4):
            d.line([(sx, by - bh + 2), (sx, by + bh - 2)], fill=sc, width=1)


def draw_cat_paws(d, belly_col, positions):
    """Draw small rectangular paws at given (x,y) positions."""
    pc = alpha(belly_col)
    for (px, py) in positions:
        d.rectangle([px - 2, py, px + 2, py + 3], fill=pc)


# ---- Five walk-cycle frames per cat ----------------------------------------

def draw_cat_frame0(body_col, belly_col, eye_col, has_stripes, stripe_col):
    """NEUTRAL STAND"""
    img = new_frame()
    d   = ImageDraw.Draw(img)
    # Tail
    draw_cat_tail(d, body_col)
    # Body
    draw_cat_body(d, body_col, belly_col, 16, 20, 9, 5, has_stripes, stripe_col)
    # Paws — 4 below body
    draw_cat_paws(d, belly_col, [(10, 25), (14, 25), (19, 25), (23, 25)])
    # Head
    draw_cat_face(d, 24, 14, body_col, belly_col, eye_col, has_stripes, stripe_col)
    return img


def draw_cat_frame1(body_col, belly_col, eye_col, has_stripes, stripe_col):
    """LEFT FRONT + RIGHT BACK RAISED"""
    img = new_frame()
    d   = ImageDraw.Draw(img)
    draw_cat_tail(d, body_col)
    draw_cat_body(d, body_col, belly_col, 16, 21, 9, 5, has_stripes, stripe_col)
    # Left front paw raised
    pc = alpha(belly_col)
    d.rectangle([12, 15, 16, 18], fill=pc)   # raised left front
    # Right back paw raised (behind body, just show stub)
    d.rectangle([21, 18, 25, 21], fill=pc)   # raised right back
    # Grounded paws
    draw_cat_paws(d, belly_col, [(9, 26), (18, 26)])
    draw_cat_face(d, 24, 14, body_col, belly_col, eye_col, has_stripes, stripe_col)
    return img


def draw_cat_frame2(body_col, belly_col, eye_col, has_stripes, stripe_col):
    """FULL STRIDE EXTENDED"""
    img = new_frame()
    d   = ImageDraw.Draw(img)
    draw_cat_tail(d, body_col)
    # Body stretched slightly wider
    draw_cat_body(d, body_col, belly_col, 16, 20, 11, 5, has_stripes, stripe_col)
    # Front paw extended forward
    pc = alpha(belly_col)
    d.rectangle([26, 18, 30, 22], fill=pc)
    # Rear paw extended back
    d.rectangle([4,  18, 8,  22], fill=pc)
    # Middle paws grounded
    draw_cat_paws(d, belly_col, [(12, 25), (21, 25)])
    draw_cat_face(d, 24, 14, body_col, belly_col, eye_col, has_stripes, stripe_col)
    return img


def draw_cat_frame3(body_col, belly_col, eye_col, has_stripes, stripe_col):
    """RIGHT FRONT + LEFT BACK RAISED"""
    img = new_frame()
    d   = ImageDraw.Draw(img)
    draw_cat_tail(d, body_col)
    draw_cat_body(d, body_col, belly_col, 16, 21, 9, 5, has_stripes, stripe_col)
    pc = alpha(belly_col)
    # Right front paw raised
    d.rectangle([20, 14, 24, 17], fill=pc)
    # Left back paw raised
    d.rectangle([9,  18, 13, 21], fill=pc)
    # Grounded
    draw_cat_paws(d, belly_col, [(12, 26), (21, 26)])
    draw_cat_face(d, 24, 14, body_col, belly_col, eye_col, has_stripes, stripe_col)
    return img


def draw_cat_frame4(body_col, belly_col, eye_col, has_stripes, stripe_col):
    """STRIDE OTHER SIDE — slight variation"""
    img = new_frame()
    d   = ImageDraw.Draw(img)
    draw_cat_tail(d, body_col)
    draw_cat_body(d, body_col, belly_col, 16, 20, 10, 5, has_stripes, stripe_col)
    pc = alpha(belly_col)
    # Other pair extended
    d.rectangle([25, 19, 29, 23], fill=pc)
    d.rectangle([5,  19, 9,  23], fill=pc)
    draw_cat_paws(d, belly_col, [(13, 25), (20, 25)])
    draw_cat_face(d, 24, 14, body_col, belly_col, eye_col, has_stripes, stripe_col)
    return img


CAT_FRAME_FNS = [
    draw_cat_frame0,
    draw_cat_frame1,
    draw_cat_frame2,
    draw_cat_frame3,
    draw_cat_frame4,
]


def build_cats_sheet():
    sheet = Image.new("RGBA", (480, 32), (0, 0, 0, 0))
    col = 0
    for (body, belly, eye_col, has_stripes, stripe_col) in CAT_TYPES:
        for fn in CAT_FRAME_FNS:
            frame = fn(body, belly, eye_col, has_stripes, stripe_col)
            sheet.paste(frame, (col * 32, 0))
            col += 1
    return sheet


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    base = "/Users/timdries/Desktop/Turnwoodstreet"

    birds_dir = os.path.join(base, "assets", "Sprites", "birds")
    cats_dir  = os.path.join(base, "assets", "Sprites", "cats")
    os.makedirs(birds_dir, exist_ok=True)
    os.makedirs(cats_dir,  exist_ok=True)

    pigeons_path = os.path.join(birds_dir, "pigeons_sheet.png")
    cats_path    = os.path.join(cats_dir,  "cats_sheet.png")

    print("Building pigeons sheet…")
    pigeons = build_pigeons_sheet()
    pigeons.save(pigeons_path)
    print(f"  Saved → {pigeons_path}  ({pigeons.width}×{pigeons.height})")

    print("Building cats sheet…")
    cats = build_cats_sheet()
    cats.save(cats_path)
    print(f"  Saved → {cats_path}  ({cats.width}×{cats.height})")

    print("Done.")
