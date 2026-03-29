#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — NPC Portrait Sprites  (high-precision crop version)
========================================================================
Strategy: draw each NPC at full 64×96 native scale, then crop to the
head + neck + shoulders region (x=6..58, y=0..52) and upscale with
nearest-neighbour to a 512×512 portrait frame.

Result: 4× larger face details vs the old 64×64-full-body approach.

Output PNG: 1024×512 px (2 × 512×512 frames)
  Frame 0: neutral  (mouth closed)
  Frame 1: talking  (mouth open)
Phaser load: frameWidth=512, frameHeight=512
"""

import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))

from generate_sprites import SVGSheet
from generate_npcs import (
    draw_fatima, draw_omar, draw_baert, draw_reza, draw_el_osri,
    draw_yusuf, draw_aziz, draw_sofia, draw_hamza, draw_tine,
)

try:
    from PIL import Image, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Pillow not installed — run: pip3 install Pillow")

# ── constants ─────────────────────────────────────────────────────────────────

INTERMEDIATE_SCALE = 4          # render NPC at 4× before cropping
PORTRAIT_PX        = 512        # final frame size in PNG pixels

# Face+shoulders crop box in GAME coordinates (before intermediate_scale)
# x=6..58 (52px wide)  y=0..52 (52px tall)  →  square crop centred on face
CROP_GX1, CROP_GY1 = 6,  0
CROP_GX2, CROP_GY2 = 58, 52    # exclusive

OUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "assets", "Sprites", "characters", "npcs", "portraits"
)


# ── SVG → PIL helper ─────────────────────────────────────────────────────────

def render_sheet(sheet: SVGSheet) -> "Image.Image":
    """Rasterise an SVGSheet into a PIL RGBA image (at INTERMEDIATE_SCALE)."""
    s = sheet.SCALE
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
        r_val = int(fill[1:3], 16)
        g_val = int(fill[3:5], 16)
        b_val = int(fill[5:7], 16)
        px1 = max(0, gx * INTERMEDIATE_SCALE)
        py1 = max(0, gy * INTERMEDIATE_SCALE)
        px2 = min(ow - 1, (gx + gw) * INTERMEDIATE_SCALE - 1)
        py2 = min(oh - 1, (gy + gh) * INTERMEDIATE_SCALE - 1)
        if px2 < px1 or py2 < py1:
            continue
        draw.rectangle([px1, py1, px2, py2], fill=(r_val, g_val, b_val, 255))
    return img


# ── open-mouth overlay ────────────────────────────────────────────────────────

def add_open_mouth(s: SVGSheet, ox: int, mouth_y: int = 22) -> None:
    """Overwrite the closed mouth with a small talking gap (drawn on top)."""
    s.put(ox + 26, mouth_y,     "stone_dark", 6, 1)
    s.put(ox + 27, mouth_y + 1, "night",      4, 1)
    s.put(ox + 26, mouth_y + 2, "stone_dark", 6, 1)


# ── crop + upscale ────────────────────────────────────────────────────────────

def crop_to_portrait(full_img: "Image.Image") -> "Image.Image":
    """Crop head+shoulders box and upscale to PORTRAIT_PX × PORTRAIT_PX."""
    px1 = CROP_GX1 * INTERMEDIATE_SCALE
    py1 = CROP_GY1 * INTERMEDIATE_SCALE
    px2 = CROP_GX2 * INTERMEDIATE_SCALE
    py2 = CROP_GY2 * INTERMEDIATE_SCALE
    cropped = full_img.crop((px1, py1, px2, py2))
    return cropped.resize((PORTRAIT_PX, PORTRAIT_PX), Image.NEAREST)


# ── per-NPC config ────────────────────────────────────────────────────────────
#   (npc_id, draw_fn, mouth_y, skip_mouth)

NPCS = [
    ("fatima",  draw_fatima,  22, False),
    ("omar",    draw_omar,    22, False),
    ("baert",   draw_baert,   22, False),
    ("reza",    draw_reza,    22, False),
    ("el_osri", draw_el_osri, 22, False),
    ("yusuf",   draw_yusuf,   23, False),   # cap head — mouth at oy+23
    ("aziz",    draw_aziz,    22, True),    # beard hides mouth
    ("sofia",   draw_sofia,   22, False),
    ("hamza",   draw_hamza,   22, False),
    ("tine",    draw_tine,    22, False),
]


# ── generator ─────────────────────────────────────────────────────────────────

def generate_portrait(npc_id: str, draw_fn, mouth_y: int, skip_mouth: bool) -> None:
    if not HAS_PIL:
        print("  ✗ Pillow unavailable — skipping")
        return

    # ── frame 0: neutral ─────────────────────────────────────────────────────
    s0 = SVGSheet(64, 96, f"{npc_id}_idle")
    s0.put(0, 0, "night", 64, 96)           # dark background
    draw_fn(s0, 0, 0, frame=0)
    frame0 = crop_to_portrait(render_sheet(s0))

    # ── frame 1: talking ─────────────────────────────────────────────────────
    s1 = SVGSheet(64, 96, f"{npc_id}_talk")
    s1.put(0, 0, "night", 64, 96)
    draw_fn(s1, 0, 0, frame=0)
    if not skip_mouth:
        add_open_mouth(s1, 0, mouth_y)
    frame1 = crop_to_portrait(render_sheet(s1))

    # ── stitch 2-frame sheet ─────────────────────────────────────────────────
    sheet = Image.new("RGBA", (PORTRAIT_PX * 2, PORTRAIT_PX), (0, 0, 0, 0))
    sheet.paste(frame0, (0, 0))
    sheet.paste(frame1, (PORTRAIT_PX, 0))

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{npc_id}_portrait.png")
    sheet.save(out_path)
    print(f"  PNG → {out_path}  ({PORTRAIT_PX * 2}×{PORTRAIT_PX} px)")


def main() -> None:
    print("=" * 60)
    print("Turnhoutsebaan NPC Portrait Generator  (crop+upscale)")
    print(f"  Crop: game x={CROP_GX1}..{CROP_GX2}, y={CROP_GY1}..{CROP_GY2}")
    print(f"  Output frame: {PORTRAIT_PX}×{PORTRAIT_PX} px")
    print("=" * 60)
    for npc_id, draw_fn, mouth_y, skip_mouth in NPCS:
        print(f"\n● {npc_id}")
        generate_portrait(npc_id, draw_fn, mouth_y, skip_mouth)
    print(f"\n✓ All portraits → {OUT_DIR}")


if __name__ == "__main__":
    main()
