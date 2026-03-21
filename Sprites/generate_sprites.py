#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — Professional Sprite Generator
===================================================
Generates game-ready pixel art sprites for the Turnhoutsebaan RPG project.

Standards (Aseprite-compatible):
  - 1 game-pixel = 1 px; rendered at 2× in SVG source
  - shape-rendering: crispEdges (no anti-aliasing)
  - Single light source: NW (top-left). Shadows fall SE.
  - 32-color master palette only (see palette.json)
  - Output: .svg (source) + .png (game-ready, via Pillow)

Run: python3 generate_sprites.py
"""

import os
import json
from typing import List, Tuple, Optional

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Pillow not installed — SVG only. Run: pip3 install Pillow")

# ── Palette ──────────────────────────────────────────────────────────────────
PAL = {
    # SKY
    "sky_light":   (0x78, 0xAF, 0xE1),
    "sky_mid":     (0xA8, 0xCB, 0xE8),
    "sky_pale":    (0xC8, 0xDF, 0xF2),
    "cloud":       (0xEE, 0xF3, 0xFA),
    # BRICK
    "brick_dark":  (0x6E, 0x2C, 0x18),
    "brick_mid":   (0x98, 0x44, 0x28),
    "brick_light": (0xC0, 0x70, 0x50),
    "mortar":      (0xD4, 0xB8, 0x98),
    # RENDER
    "cream_dark":  (0xC8, 0xA8, 0x6C),
    "cream_mid":   (0xE8, 0xCF, 0xA0),
    "cream_light": (0xF4, 0xE8, 0xC8),
    "ochre":       (0xD4, 0xA0, 0x40),
    # STONE
    "stone_dark":  (0x60, 0x60, 0x58),
    "stone_mid":   (0x88, 0x88, 0x80),
    "stone_light": (0xB4, 0xB0, 0xA8),
    "stone_pale":  (0xD8, 0xD4, 0xCC),
    # GROUND
    "asphalt_dark":  (0x2C, 0x2C, 0x28),
    "asphalt_mid":   (0x48, 0x44, 0x40),
    "asphalt_light": (0x68, 0x64, 0x60),
    "sidewalk":      (0xB4, 0xAE, 0x9E),
    "cobble":        (0x74, 0x70, 0x68),
    "grass":         (0x3C, 0x88, 0x30),
    # TRAM
    "rail":          (0x90, 0x90, 0xA0),
    "tram_bed":      (0x54, 0x50, 0x48),
    "de_lijn_blue":  (0x1C, 0x58, 0x98),
    "de_lijn_yellow":(0xDD, 0xB8, 0x00),
    # ACCENT
    "wood_dark":  (0x4A, 0x2C, 0x10),
    "wood_light": (0x8A, 0x5A, 0x28),
    "glass":      (0xA0, 0xC8, 0xE4),
    "night":      (0x0C, 0x0C, 0x18),
    # UI
    "gold":    (0xFF, 0xD7, 0x00),
    "white":   (0xF0, 0xEE, 0xE8),
    "black":   (0x14, 0x12, 0x10),
    "red_ui":  (0xCC, 0x20, 0x10),
}

def p(name: str) -> Tuple[int,int,int]:
    """Get palette color by name."""
    return PAL[name]

def hex_color(name: str) -> str:
    r, g, b = PAL[name]
    return f"#{r:02X}{g:02X}{b:02X}"

def rgb_to_hex(rgb: Tuple[int,int,int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

TRANS = (0, 0, 0, 0)  # transparent

# ── SVG Builder ──────────────────────────────────────────────────────────────

class SVGSheet:
    """Builds a pixel-art sprite sheet as SVG (4× scale)."""
    SCALE = 4

    def __init__(self, w_px: int, h_px: int, title: str):
        self.w = w_px
        self.h = h_px
        self.title = title
        self.rects: List[str] = []

    def put(self, x: int, y: int, color_name: str, w: int = 1, h: int = 1):
        """Place a pixel (or rectangle of pixels) at game coords."""
        if color_name == "TRANSPARENT":
            return
        s = self.SCALE
        hx = hex_color(color_name)
        self.rects.append(
            f'<rect x="{x*s}" y="{y*s}" width="{w*s}" height="{h*s}" fill="{hx}"/>'
        )

    def put_rgb(self, x: int, y: int, rgb: Tuple[int,int,int], w: int = 1, h: int = 1):
        """Place a pixel with direct RGB (must be from palette)."""
        s = self.SCALE
        hx = rgb_to_hex(rgb)
        self.rects.append(
            f'<rect x="{x*s}" y="{y*s}" width="{w*s}" height="{h*s}" fill="{hx}"/>'
        )

    def label(self, x: int, y: int, text: str, color: str = "#666"):
        s = self.SCALE
        self.rects.append(
            f'<text x="{x*s}" y="{y*s}" font-size="9" fill="{color}" '
            f'font-family="monospace" shape-rendering="auto">{text}</text>'
        )

    def save(self, path: str):
        s = self.SCALE
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.w*s} {self.h*s}" '
            f'width="{self.w*s}" height="{self.h*s}" '
            f'shape-rendering="crispEdges">',
            f'  <!-- {self.title} -->',
            f'  <!-- SCALE: 4×  |  1 game px = 4 SVG px  |  PALETTE: Turnhoutsebaan 32-color -->',
        ]
        lines.extend(f'  {r}' for r in self.rects)
        lines.append('</svg>')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"  SVG → {path}")

    def to_pil(self, png_path: str, out_scale: int = 2):
        """Export as PNG using Pillow at out_scale × game resolution.

        Uses ImageDraw.rectangle() — fast at any out_scale (incl. out_scale=10).
        Each game pixel becomes an (out_scale × out_scale) block of PNG pixels.
        """
        if not HAS_PIL:
            return
        import re
        from PIL import ImageDraw

        pw, ph = self.w * out_scale, self.h * out_scale
        img  = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for r in self.rects:
            if not r.startswith('<rect'):
                continue
            m = re.search(
                r'x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="(#[0-9A-Fa-f]{6})"', r
            )
            if not m:
                continue
            x, y, w, h, fill = int(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5]
            s = self.SCALE
            gx, gy, gw, gh = x // s, y // s, w // s, h // s
            r_val = int(fill[1:3], 16)
            g_val = int(fill[3:5], 16)
            b_val = int(fill[5:7], 16)

            px1 = gx * out_scale
            py1 = gy * out_scale
            px2 = (gx + gw) * out_scale - 1
            py2 = (gy + gh) * out_scale - 1

            # Clamp to image bounds
            if px2 < 0 or py2 < 0 or px1 >= pw or py1 >= ph:
                continue
            px1 = max(0, px1); py1 = max(0, py1)
            px2 = min(pw - 1, px2); py2 = min(ph - 1, py2)

            draw.rectangle([px1, py1, px2, py2], fill=(r_val, g_val, b_val, 255))

        img.save(png_path)
        print(f"  PNG → {png_path}  ({pw}×{ph} px)")


# ── Pixel Art Drawing Helpers ─────────────────────────────────────────────────

def draw_brick_tile(s: SVGSheet, ox: int, oy: int, lit: bool = True):
    """32×32 running-bond brick tile. lit=True means NW-lit face."""
    base  = "brick_mid"
    dark  = "brick_dark"
    light = "brick_light"
    mort  = "mortar"

    # Fill entire tile with base brick color
    s.put(ox, oy, base, 32, 32)

    # Horizontal mortar lines every 5 px (4 brick + 1 mortar)
    for row in range(0, 32, 5):
        s.put(ox, oy + row, mort, 32, 1)

    # Vertical mortar joints — alternate offset rows
    for row_block in range(7):
        ry = oy + row_block * 5 + 1  # y of first brick px in row
        offset = 0 if (row_block % 2 == 0) else 4
        for col_start in range(offset, 32, 8):
            # Right-side mortar joint of each brick
            joint_x = col_start + 7
            if joint_x < 32:
                s.put(ox + joint_x, ry, mort, 1, 4)

    if lit:
        # NW light: highlight top and left edge of each brick
        for row_block in range(7):
            ry = oy + row_block * 5 + 1
            offset = 0 if (row_block % 2 == 0) else 4
            for col_start in range(offset, 32, 8):
                bx = ox + col_start
                bw = min(7, 32 - col_start)
                # Top edge of brick: lighter
                s.put(bx, ry, light, bw, 1)
                # Left edge: slightly lighter
                if bw > 1:
                    s.put(bx, ry + 1, light, 1, 3)
                # Bottom-right shadow
                if bw > 1:
                    s.put(bx + bw - 1, ry + 2, dark, 1, 2)
                s.put(bx, ry + 3, dark, bw - 1, 1)


def draw_render_tile(s: SVGSheet, ox: int, oy: int, base_color: str = "cream_mid"):
    """32×32 plastered render wall tile."""
    colors = {
        "cream_mid":  ("cream_light", "cream_dark", "ochre"),
        "cream_light":("white",       "cream_mid",  "cream_dark"),
        "ochre":      ("cream_mid",   "ochre",      "cream_dark"),
    }
    hi_c, base_c, lo_c = colors.get(base_color, ("cream_light", "cream_mid", "cream_dark"))

    # Base fill
    s.put(ox, oy, base_color, 32, 32)

    # Plaster texture — horizontal bands with slight variation
    for y in range(0, 32, 4):
        # Every other band slightly lighter/darker
        if (y // 4) % 3 == 0:
            s.put(ox, oy + y, hi_c, 32, 1)
        elif (y // 4) % 3 == 2:
            s.put(ox, oy + y + 3, lo_c, 32, 1)

    # Subtle vertical cracks
    crack_x = [7, 19]
    for cx in crack_x:
        for cy in range(0, 32, 3):
            s.put(ox + cx, oy + cy, lo_c, 1, 1)

    # NW highlight edge
    s.put(ox, oy, hi_c, 32, 1)
    s.put(ox, oy, hi_c, 1, 32)


def draw_asphalt_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 asphalt road tile with aggregate texture."""
    s.put(ox, oy, "asphalt_mid", 32, 32)

    # Aggregate — scattered lighter/darker specks
    specks_light = [(2,3),(5,8),(8,1),(11,14),(14,7),(17,20),(20,4),(23,11),(26,18),(29,5),
                    (3,22),(6,15),(9,28),(12,19),(15,2),(18,25),(21,9),(24,22),(27,14),(30,28),
                    (1,11),(4,26),(7,19),(10,5),(13,24),(16,12),(19,29),(22,16),(25,3),(28,21)]
    specks_dark  = [(3,7),(6,12),(9,4),(12,21),(15,16),(18,9),(21,25),(24,7),(27,19),(30,12),
                    (2,18),(5,29),(8,11),(11,0),(14,23),(17,6),(20,17),(23,28),(26,10),(29,23)]

    for (dx, dy) in specks_light:
        if dx < 32 and dy < 32:
            s.put(ox + dx, oy + dy, "asphalt_light", 1, 1)
    for (dx, dy) in specks_dark:
        if dx < 32 and dy < 32:
            s.put(ox + dx, oy + dy, "asphalt_dark", 1, 1)


def draw_sidewalk_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 Belgian bluestone slab tile."""
    s.put(ox, oy, "sidewalk", 32, 32)

    # Slab joints — 16×16 slabs
    s.put(ox,      oy + 15, "stone_mid", 32, 1)
    s.put(ox + 15, oy,      "stone_mid",  1, 32)

    # Each slab: NW highlight + SE shadow
    for sy in [0, 16]:
        for sx in [0, 16]:
            # Top/left highlight
            s.put(ox + sx,      oy + sy, "stone_light", 14, 1)
            s.put(ox + sx,      oy + sy, "stone_light", 1, 14)
            # Bottom/right shadow
            s.put(ox + sx,      oy + sy + 14, "stone_mid", 15, 1)
            s.put(ox + sx + 14, oy + sy,      "stone_mid", 1, 15)


def draw_cobble_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 cobblestone tile (old street / tram zone)."""
    s.put(ox, oy, "cobble", 32, 32)
    # Cobble pattern — irregular rounded stones ~6×5 px
    stones = [
        (0, 0, 5, 4), (6, 0, 5, 4), (12, 0, 6, 4), (19, 0, 5, 4), (25, 0, 7, 4),
        (0, 5, 6, 4), (7, 5, 5, 4), (13, 5, 6, 4), (20, 5, 5, 4), (26, 5, 6, 4),
        (0,10, 5, 4), (6,10, 6, 4), (13,10, 5, 4), (19,10, 6, 4), (26,10, 6, 4),
        (0,15, 6, 4), (7,15, 5, 4), (13,15, 6, 4), (20,15, 5, 4), (26,15, 6, 4),
        (0,20, 5, 4), (6,20, 6, 4), (13,20, 5, 4), (19,20, 6, 4), (26,20, 6, 4),
        (0,25, 6, 4), (7,25, 5, 4), (13,25, 6, 4), (20,25, 5, 4), (26,25, 6, 4),
    ]
    for (sx, sy, sw, sh) in stones:
        # mortar gap (keep base cobble color)
        # stone interior lighter
        s.put(ox+sx+1, oy+sy+1, "stone_mid",  sw-2, sh-2)
        # NW highlight
        s.put(ox+sx+1, oy+sy+1, "stone_light", sw-2, 1)
        s.put(ox+sx+1, oy+sy+1, "stone_light", 1, sh-2)
        # SE shadow
        s.put(ox+sx+1, oy+sy+sh-2, "stone_dark", sw-2, 1)
        s.put(ox+sx+sw-2, oy+sy+1, "stone_dark", 1, sh-2)


def draw_tram_track_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 tram track tile — concrete bed + 2 rails."""
    s.put(ox, oy, "tram_bed", 32, 32)

    # Aggregate in concrete
    specks = [(3,4),(9,12),(15,6),(21,18),(27,9),(5,22),(11,28),(17,3),(23,15),(29,25)]
    for (dx, dy) in specks:
        s.put(ox+dx, oy+dy, "stone_dark", 1, 1)

    # Two steel rails — each 2px wide at x=8 and x=22
    for rail_x in [8, 22]:
        s.put(ox + rail_x, oy, "rail", 2, 32)
        # Rail highlight (NW)
        s.put(ox + rail_x, oy, "stone_light", 1, 32)
        # Rail shadow (SE)
        s.put(ox + rail_x + 1, oy, "stone_dark", 1, 32)

    # Rail tie marks every 8 rows
    for ty in [0, 8, 16, 24]:
        s.put(ox + 6, oy + ty, "stone_dark", 20, 2)


def draw_zebra_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 zebra crossing tile."""
    s.put(ox, oy, "asphalt_mid", 32, 32)
    # White stripes — 4px stripe, 4px gap
    for stripe in range(4):
        sy = stripe * 8
        s.put(ox, oy + sy, "stone_pale", 32, 4)


def draw_lane_mark_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 lane marking tile — dashed centre line."""
    s.put(ox, oy, "asphalt_mid", 32, 32)
    # Yellow dashed line, centred
    s.put(ox + 15, oy,     "de_lijn_yellow", 2, 12)
    s.put(ox + 15, oy + 20,"de_lijn_yellow", 2, 12)


def draw_grass_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 urban grass / verge tile."""
    s.put(ox, oy, "grass", 32, 32)
    # Texture: slightly darker patches
    patches = [(0,0,8,4),(10,6,6,3),(20,2,5,4),(2,14,6,3),(14,18,8,4),(24,12,6,3),
               (4,24,7,4),(16,28,6,3),(26,22,5,3)]
    for (px,py,pw,ph) in patches:
        s.put(ox+px, oy+py, "stone_dark", pw, ph)
        # blades (lighter green = use asphalt_light as stub, closest we have)
        s.put(ox+px, oy+py, "asphalt_light", 1, 1)


def draw_roof_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 rooftop tile (oblique top view) — dark grey tiles."""
    s.put(ox, oy, "stone_dark", 32, 32)
    # Roof tile grid: 8×4 px tiles
    for ty in range(0, 32, 4):
        for tx in range(0, 32, 8):
            # Tile body: slightly lighter
            s.put(ox+tx+1, oy+ty+1, "stone_mid", 6, 2)
            # NW highlight
            s.put(ox+tx+1, oy+ty+1, "stone_light", 6, 1)
            # SE shadow
            s.put(ox+tx+1, oy+ty+3, "stone_dark", 7, 1)


def draw_tram_stop_tile(s: SVGSheet, ox: int, oy: int):
    """32×32 tram stop platform tile — raised bluestone."""
    s.put(ox, oy, "sidewalk", 32, 32)
    # De Lijn blue strip at top
    s.put(ox, oy, "de_lijn_blue", 32, 4)
    # Slab joints
    s.put(ox + 16, oy + 4, "stone_mid", 1, 28)
    s.put(ox, oy + 18, "stone_mid", 32, 1)
    # Platform edge highlight
    s.put(ox, oy + 4, "stone_light", 32, 1)


# ── Window Modules ────────────────────────────────────────────────────────────

def draw_window_arched(s: SVGSheet, ox: int, oy: int):
    """16×24 arched window with Belgian glazing bars."""
    # Stone frame
    s.put(ox, oy, "stone_mid", 16, 24)
    # Arch cutout (simulate with glass fill + stone arch outline)
    s.put(ox+2, oy+6, "glass", 12, 14)  # rectangular pane lower
    # Arch top — 12×6 semicircle approximation
    # Row 0 of arch (top): 2px glass in centre
    s.put(ox+7, oy+2, "glass", 2, 1)
    # Row 1: 4px
    s.put(ox+6, oy+3, "glass", 4, 1)
    # Row 2: 8px
    s.put(ox+4, oy+4, "glass", 8, 1)
    # Row 3: 10px
    s.put(ox+3, oy+5, "glass", 10, 1)
    # Glazing bars (stone cross)
    s.put(ox+2, oy+12, "stone_mid", 12, 1)   # horizontal bar
    s.put(ox+9, oy+6,  "stone_mid", 1, 14)   # vertical bar
    # Interior night shadow
    s.put(ox+3, oy+7, "night", 6, 5)
    s.put(ox+3, oy+13, "night", 6, 5)
    s.put(ox+10,oy+7,  "night", 3, 5)
    s.put(ox+10,oy+13, "night", 3, 5)
    # NW glass reflection
    s.put(ox+3, oy+7, "sky_pale", 2, 2)
    s.put(ox+10,oy+7, "sky_pale", 1, 1)
    # Frame highlight
    s.put(ox, oy, "stone_light", 16, 1)
    s.put(ox, oy, "stone_light", 1, 24)
    # Frame shadow
    s.put(ox+15, oy, "stone_dark", 1, 24)
    s.put(ox, oy+23, "stone_dark", 16, 1)


def draw_window_rect(s: SVGSheet, ox: int, oy: int):
    """14×18 rectangular double window."""
    s.put(ox, oy, "stone_mid", 14, 18)
    # Two panes side by side
    s.put(ox+2, oy+2, "glass", 4, 13)
    s.put(ox+8, oy+2, "glass", 4, 13)
    # Centre divider
    s.put(ox+6, oy+2, "stone_mid", 2, 13)
    # Horizontal glazing bar
    s.put(ox+2, oy+8, "stone_mid", 10, 1)
    # Night interior
    s.put(ox+3, oy+9, "night", 3, 5)
    s.put(ox+9, oy+9, "night", 2, 5)
    # Reflections
    s.put(ox+2, oy+3, "sky_pale", 2, 2)
    s.put(ox+8, oy+3, "sky_pale", 2, 2)
    # Frame light/shadow
    s.put(ox, oy, "stone_light", 14, 1)
    s.put(ox, oy, "stone_light", 1, 18)
    s.put(ox+13, oy, "stone_dark", 1, 18)
    s.put(ox, oy+17, "stone_dark", 14, 1)


def draw_window_shuttered(s: SVGSheet, ox: int, oy: int):
    """14×20 window with wooden shutters (closed)."""
    # Outer stone frame
    s.put(ox, oy, "stone_mid", 14, 20)
    # Left shutter (wood slats)
    s.put(ox+1, oy+1, "wood_light", 5, 18)
    for slat in range(0, 18, 2):
        s.put(ox+1, oy+1+slat, "wood_dark", 5, 1)
    # Right shutter
    s.put(ox+8, oy+1, "wood_light", 5, 18)
    for slat in range(0, 18, 2):
        s.put(ox+8, oy+1+slat, "wood_dark", 5, 1)
    # Centre gap (tiny glimpse of glass)
    s.put(ox+6, oy+1, "glass", 2, 18)
    # Hinges
    s.put(ox+1, oy+4, "stone_dark", 1, 2)
    s.put(ox+1, oy+14, "stone_dark", 1, 2)
    s.put(ox+12,oy+4,  "stone_dark", 1, 2)
    s.put(ox+12,oy+14, "stone_dark", 1, 2)
    # Frame
    s.put(ox, oy, "stone_light", 14, 1)
    s.put(ox, oy, "stone_light", 1, 20)
    s.put(ox+13,oy, "stone_dark", 1, 20)
    s.put(ox, oy+19, "stone_dark", 14, 1)


def draw_window_night(s: SVGSheet, ox: int, oy: int):
    """14×18 lit window (warm night interior glow)."""
    s.put(ox, oy, "stone_mid", 14, 18)
    # Warm light pane
    s.put(ox+2, oy+2, "ochre", 10, 13)
    # Curtain silhouette
    s.put(ox+2, oy+2, "cream_dark", 3, 13)
    s.put(ox+9, oy+2, "cream_dark", 3, 13)
    # Window cross
    s.put(ox+2, oy+9, "stone_dark", 10, 1)
    s.put(ox+7, oy+2, "stone_dark", 1, 13)
    # Glow spill at bottom edge
    s.put(ox+2, oy+15, "de_lijn_yellow", 10, 1)
    # Frame
    s.put(ox, oy, "stone_light", 14, 1)
    s.put(ox, oy, "stone_light", 1, 18)
    s.put(ox+13, oy, "stone_dark", 1, 18)
    s.put(ox, oy+17, "stone_dark", 14, 1)


def draw_window_bay(s: SVGSheet, ox: int, oy: int):
    """20×24 bay window (protruding, 3-section)."""
    # Stone body
    s.put(ox, oy, "stone_mid", 20, 24)
    # Protrusion front panel
    s.put(ox+2, oy, "stone_light", 16, 24)
    # Three panes
    for px_off, pw in [(3, 4), (8, 4), (13, 4)]:
        s.put(ox+px_off, oy+2, "glass", pw, 18)
        s.put(ox+px_off, oy+10, "stone_mid", pw, 1)  # glaze bar
        s.put(ox+px_off, oy+3, "sky_pale", 2, 2)      # reflection
    # Dividers
    s.put(ox+7,  oy+2, "stone_mid", 1, 18)
    s.put(ox+12, oy+2, "stone_mid", 1, 18)
    # Cornice top
    s.put(ox+2, oy, "cream_mid", 16, 2)
    # Night interior
    s.put(ox+3, oy+11, "night", 4, 7)
    s.put(ox+8, oy+11, "night", 4, 7)
    s.put(ox+13,oy+11, "night", 4, 7)
    # Frame
    s.put(ox, oy, "stone_dark", 1, 24)
    s.put(ox+19, oy, "stone_dark", 1, 24)
    s.put(ox, oy+23, "stone_dark", 20, 1)


def draw_window_broken(s: SVGSheet, ox: int, oy: int):
    """14×18 broken/boarded window."""
    s.put(ox, oy, "stone_mid", 14, 18)
    # Plywood boards
    s.put(ox+2, oy+2, "wood_dark", 10, 14)
    # Board grain lines
    for gy in range(4, 14, 3):
        s.put(ox+2, oy+2+gy, "wood_light", 10, 1)
    # X brace
    for i in range(10):
        s.put(ox+2+i, oy+2+i,    "wood_light", 1, 1)
        s.put(ox+11-i, oy+2+i,   "wood_light", 1, 1)
    # Graffiti tag (1 pixel squiggle)
    s.put(ox+4, oy+10, "red_ui", 4, 1)
    s.put(ox+4, oy+11, "red_ui", 1, 2)
    # Frame
    s.put(ox, oy, "stone_light", 14, 1)
    s.put(ox, oy, "stone_light", 1, 18)
    s.put(ox+13, oy, "stone_dark", 1, 18)
    s.put(ox, oy+17, "stone_dark", 14, 1)


# ── Door Modules ─────────────────────────────────────────────────────────────

def draw_door_wooden_arch(s: SVGSheet, ox: int, oy: int):
    """16×28 ornate wooden arched door."""
    s.put(ox, oy, "stone_mid", 16, 28)
    # Arch outline (stone)
    # Door body (wood)
    s.put(ox+2, oy+10, "wood_light", 12, 17)
    # Arch fill (glass fanlight)
    s.put(ox+3, oy+3, "glass", 10, 7)
    # Arch stones above
    s.put(ox+2, oy+2, "stone_light", 12, 1)
    # Keystone
    s.put(ox+7, oy+1, "cream_mid", 2, 3)
    # Door panels (raised)
    s.put(ox+3, oy+12, "wood_dark", 4, 6)
    s.put(ox+9, oy+12, "wood_dark", 4, 6)
    s.put(ox+3, oy+20, "wood_dark", 10, 5)
    # Panel highlights
    s.put(ox+3, oy+12, "wood_light", 4, 1)
    s.put(ox+9, oy+12, "wood_light", 4, 1)
    # Door handle
    s.put(ox+11, oy+20, "ochre", 1, 3)
    s.put(ox+12, oy+21, "ochre", 2, 1)
    # Fanlight reflection
    s.put(ox+4, oy+4, "sky_pale", 3, 2)
    # Step
    s.put(ox, oy+27, "stone_light", 16, 1)
    # Frame
    s.put(ox, oy, "stone_light", 1, 28)
    s.put(ox+15, oy, "stone_dark", 1, 28)
    s.put(ox, oy+27, "stone_dark", 16, 1)


def draw_door_modern_glass(s: SVGSheet, ox: int, oy: int):
    """16×28 modern shop glass door."""
    s.put(ox, oy, "stone_dark", 16, 28)
    # Glass door panel
    s.put(ox+2, oy+1, "glass", 12, 24)
    # Aluminium frame (stone_mid)
    s.put(ox+2, oy+1,  "stone_mid", 12, 1)
    s.put(ox+2, oy+24, "stone_mid", 12, 1)
    s.put(ox+2, oy+1,  "stone_mid", 1, 24)
    s.put(ox+13,oy+1,  "stone_mid", 1, 24)
    # Handle (horizontal bar)
    s.put(ox+4,  oy+13, "stone_light", 7, 1)
    s.put(ox+11, oy+13, "stone_light", 1, 3)
    # Reflection
    s.put(ox+3, oy+2, "sky_light", 4, 6)
    s.put(ox+3, oy+2, "cloud",     2, 3)
    # Transparent interior view
    s.put(ox+4, oy+10, "asphalt_dark", 4, 12)
    s.put(ox+9, oy+10, "asphalt_dark", 3, 12)
    # Step
    s.put(ox, oy+26, "stone_mid", 16, 2)
    # Frame
    s.put(ox, oy, "stone_light", 1, 28)
    s.put(ox+15,oy, "stone_dark", 1, 28)


def draw_door_cellar(s: SVGSheet, ox: int, oy: int):
    """16×16 cellar/basement door (flush with ground, angled)."""
    s.put(ox, oy, "stone_dark", 16, 16)
    # Two door halves
    s.put(ox+1, oy+1, "wood_dark",  7, 13)
    s.put(ox+8, oy+1, "wood_dark",  7, 13)
    # Wood grain
    for gy in range(0, 13, 2):
        s.put(ox+1, oy+1+gy, "wood_light", 7, 1)
        s.put(ox+8, oy+1+gy, "wood_light", 7, 1)
    # Handles
    s.put(ox+4,  oy+7, "mortar", 1, 2)
    s.put(ox+11, oy+7, "mortar", 1, 2)
    # Hinge
    s.put(ox+1, oy+4, "stone_mid", 1, 2)
    s.put(ox+14,oy+4, "stone_mid", 1, 2)
    # Centre seam
    s.put(ox+7, oy+1, "stone_dark", 2, 14)


def draw_door_shutter(s: SVGSheet, ox: int, oy: int):
    """24×20 rolling shop shutter (closed)."""
    s.put(ox, oy, "stone_dark", 24, 20)
    # Shutter panels
    for gy in range(0, 20, 4):
        s.put(ox+2, oy+gy, "stone_mid", 20, 3)
        s.put(ox+2, oy+gy, "stone_light", 20, 1)  # highlight
        s.put(ox+2, oy+gy+2, "stone_dark", 20, 1) # shadow
    # Bottom handle bar
    s.put(ox+4, oy+18, "stone_light", 16, 2)
    # Graffiti detail
    s.put(ox+8, oy+8, "red_ui", 5, 1)
    s.put(ox+8, oy+8, "red_ui", 1, 3)
    s.put(ox+12,oy+8, "red_ui", 1, 3)
    # Frame
    s.put(ox, oy, "stone_light", 1, 20)
    s.put(ox+23,oy, "stone_dark", 1, 20)
    s.put(ox, oy+19, "stone_dark", 24, 1)


# ── Gable / Roofline Modules ──────────────────────────────────────────────────

def draw_gable_trap(s: SVGSheet, ox: int, oy: int):
    """32×24 Belgian trapgevel (stepped gable) — most common on Turnhoutsebaan."""
    # Sky background
    s.put(ox, oy, "sky_mid", 32, 24)
    # Stepped brick gable — 4 steps each side
    # Step widths: 4, 3, 2, 1 px; step heights: 4 px each
    steps = [(0, 4), (4, 4), (8, 4), (12, 4)]  # (x_inset, h)
    for i, (inset, h) in enumerate(steps):
        y = oy + i * 4
        w = 32 - inset * 2
        # Brick-colored step block
        s.put(ox + inset, y, "brick_mid",   w, h)
        s.put(ox + inset, y, "brick_light", w, 1)   # top highlight
        s.put(ox + inset, y, "brick_light", 1, h)   # left highlight
        s.put(ox + inset + w - 1, y, "brick_dark", 1, h)  # right shadow
        s.put(ox + inset, y + h - 1, "brick_dark", w, 1)  # bottom shadow
    # Chimney
    s.put(ox + 14, oy, "brick_dark", 4, 8)
    s.put(ox + 14, oy, "mortar", 4, 1)
    s.put(ox + 13, oy + 8, "stone_dark", 6, 1)   # chimney cap


def draw_gable_klok(s: SVGSheet, ox: int, oy: int):
    """32×24 klokgevel (bell/curved gable) — Art Nouveau style."""
    s.put(ox, oy, "sky_mid", 32, 24)
    # Bell curve — render/plaster
    # Base
    s.put(ox + 2, oy + 18, "cream_mid", 28, 6)
    # Bell curve (approximate with rects)
    curves = [
        (4, 14, 24, 4),
        (6, 10, 20, 4),
        (8,  6, 16, 4),
        (9,  2, 14, 4),
        (11, 0, 10, 2),
    ]
    for (cx, cy, cw, ch) in curves:
        s.put(ox + cx, oy + cy, "cream_mid", cw, ch)
        s.put(ox + cx, oy + cy, "cream_light", cw, 1)
        s.put(ox + cx, oy + cy, "cream_light", 1, ch)
        s.put(ox + cx + cw - 1, oy + cy, "cream_dark", 1, ch)
    # Cornice ornament
    s.put(ox + 13, oy + 2, "ochre", 6, 2)
    # Art Nouveau ironwork accent
    s.put(ox + 8, oy + 14, "stone_dark", 2, 1)
    s.put(ox + 22, oy + 14, "stone_dark", 2, 1)
    # Chimney
    s.put(ox + 14, oy, "stone_mid", 4, 4)
    s.put(ox + 13, oy + 4, "stone_dark", 6, 1)


def draw_gable_flat(s: SVGSheet, ox: int, oy: int):
    """32×16 flat cornice with dentils — most common 1970s style."""
    s.put(ox, oy, "sky_mid", 32, 16)
    # Flat top
    s.put(ox, oy + 4, "cream_mid", 32, 12)
    # Cornice overhang
    s.put(ox, oy + 4, "cream_light", 32, 2)
    # Dentil row
    for dx in range(0, 32, 4):
        s.put(ox + dx, oy + 6, "cream_light", 2, 4)
        s.put(ox + dx + 2, oy + 6, "cream_dark", 2, 4)
    # Top edge
    s.put(ox, oy + 4, "ochre", 32, 1)
    # Parapet
    s.put(ox, oy, "cream_mid", 32, 4)
    s.put(ox, oy, "cream_light", 32, 1)
    s.put(ox, oy + 3, "cream_dark", 32, 1)


def draw_gable_triangular(s: SVGSheet, ox: int, oy: int):
    """32×24 triangular/pediment gable — classical / neo-classical."""
    s.put(ox, oy, "sky_mid", 32, 24)
    # Triangle rows (widening downward)
    for row in range(12):
        inset = 12 - row
        w = row * 2
        y = oy + row
        s.put(ox + inset, y, "cream_mid", w, 1)
        # edges
        s.put(ox + inset, y, "cream_light", 1, 1)
        if w > 1:
            s.put(ox + inset + w - 1, y, "cream_dark", 1, 1)
    # Base cornice
    s.put(ox, oy + 12, "cream_mid", 32, 8)
    s.put(ox, oy + 12, "cream_light", 32, 1)
    s.put(ox, oy + 19, "cream_dark", 32, 1)
    # Dentils
    for dx in range(0, 32, 4):
        s.put(ox + dx, oy + 14, "cream_light", 2, 3)
    # Acroterion
    s.put(ox + 14, oy, "ochre", 4, 2)
    # Pediment walls
    s.put(ox, oy + 20, "cream_mid", 32, 4)


# ── Props ─────────────────────────────────────────────────────────────────────

def draw_lamp_post(s: SVGSheet, ox: int, oy: int):
    """8×40 Antwerp double-arm iron street lamp."""
    # Post shaft
    s.put(ox + 3, oy + 10, "stone_dark",  2, 30)  # main post
    s.put(ox + 3, oy + 10, "stone_light", 1, 30)  # highlight

    # Base (wider)
    s.put(ox + 2, oy + 36, "stone_dark", 4, 4)
    s.put(ox + 1, oy + 38, "stone_dark", 6, 2)

    # Left arm
    s.put(ox + 1, oy + 12, "stone_dark", 2, 1)   # arm horizontal
    s.put(ox + 1, oy + 10, "stone_dark", 1, 3)   # arm vertical
    # Left lamp head
    s.put(ox,     oy + 8,  "stone_mid",  3, 3)
    s.put(ox + 1, oy + 7,  "de_lijn_yellow", 1, 1)   # bulb warm glow
    s.put(ox,     oy + 9,  "stone_dark", 3, 1)

    # Right arm
    s.put(ox + 5, oy + 12, "stone_dark", 2, 1)
    s.put(ox + 6, oy + 10, "stone_dark", 1, 3)
    # Right lamp head
    s.put(ox + 5, oy + 8,  "stone_mid",  3, 3)
    s.put(ox + 6, oy + 7,  "de_lijn_yellow", 1, 1)
    s.put(ox + 5, oy + 9,  "stone_dark", 3, 1)

    # Decorative capital
    s.put(ox + 2, oy + 9,  "stone_mid", 4, 2)
    s.put(ox + 2, oy + 9,  "stone_light", 4, 1)

    # Shadow on ground
    s.put(ox + 5, oy + 39, "asphalt_dark", 3, 1)


def draw_tree_grate(s: SVGSheet, ox: int, oy: int):
    """16×32 urban lime tree in iron grate."""
    # Canopy (top portion)
    # Outer dark leaves
    canopy = [
        (4, 0, 8, 3),
        (2, 2, 12, 4),
        (1, 5, 14, 5),
        (0, 9, 16, 6),
    ]
    for (cx, cy, cw, ch) in canopy:
        s.put(ox+cx, oy+cy, "stone_dark", cw, ch)  # deep shadow

    # Mid foliage
    mid_can = [
        (5, 0, 6, 2),
        (3, 2, 10, 4),
        (1, 5, 14, 4),
        (0, 9, 16, 4),
    ]
    for (cx, cy, cw, ch) in mid_can:
        s.put(ox+cx, oy+cy, "grass", cw, ch)

    # Light highlight (NW sun)
    s.put(ox+5, oy+1, "asphalt_light", 4, 2)  # using asphalt_light as bright green placeholder

    # Trunk
    s.put(ox+7, oy+15, "wood_dark",  2, 11)
    s.put(ox+7, oy+15, "wood_light", 1, 11)  # trunk highlight

    # Grate (iron grid)
    s.put(ox, oy+26, "stone_dark", 16, 6)
    for gx in range(0, 16, 4):
        s.put(ox+gx, oy+26, "stone_mid", 1, 6)
    for gy in range(0, 6, 2):
        s.put(ox, oy+26+gy, "stone_mid", 16, 1)

    # Shadow under grate
    s.put(ox+2, oy+31, "asphalt_dark", 12, 1)


def draw_bench(s: SVGSheet, ox: int, oy: int):
    """24×16 wood-slat bench with cast iron legs."""
    # Seat slats (3 horizontal wooden boards)
    for i in range(3):
        s.put(ox + 2, oy + 4 + i*2, "wood_light", 20, 1)
        s.put(ox + 2, oy + 5 + i*2, "wood_dark",  20, 1)

    # Backrest (2 boards)
    s.put(ox + 2, oy,     "wood_light", 20, 1)
    s.put(ox + 2, oy + 1, "wood_dark",  20, 1)
    s.put(ox + 2, oy + 2, "wood_light", 20, 1)
    s.put(ox + 2, oy + 3, "wood_dark",  20, 1)

    # Cast iron legs
    for lx in [2, 12, 20]:
        s.put(ox + lx, oy + 10, "stone_dark",  2, 6)
        s.put(ox + lx, oy + 10, "stone_light", 1, 6)  # highlight
        # Foot spread
        s.put(ox + lx - 1, oy + 14, "stone_dark", 4, 2)

    # Armrest
    s.put(ox + 2,  oy + 8, "stone_dark", 1, 4)
    s.put(ox + 21, oy + 8, "stone_dark", 1, 4)

    # Shadow
    s.put(ox + 4, oy + 15, "asphalt_dark", 16, 1)


def draw_bin(s: SVGSheet, ox: int, oy: int):
    """10×20 cylindrical city waste bin."""
    # Body (dark green / stone_dark)
    s.put(ox + 1, oy + 3, "stone_dark", 8, 15)
    # Highlight (NW)
    s.put(ox + 1, oy + 3, "stone_mid",  2, 15)
    s.put(ox + 1, oy + 3, "stone_mid",  8, 1)
    # Rim (top)
    s.put(ox, oy + 2, "stone_light", 10, 1)
    s.put(ox, oy + 2, "stone_mid", 10, 2)
    # Lid
    s.put(ox + 1, oy, "stone_mid", 8, 3)
    s.put(ox + 2, oy, "stone_light", 6, 1)
    # Slot opening
    s.put(ox + 3, oy + 1, "black", 4, 1)
    # Stad Antwerpen logo (small white X)
    s.put(ox + 4, oy + 10, "white", 1, 1)
    s.put(ox + 5, oy + 9,  "white", 1, 1)
    s.put(ox + 6, oy + 10, "white", 1, 1)
    s.put(ox + 5, oy + 11, "white", 1, 1)
    # Bottom edge
    s.put(ox + 2, oy + 18, "stone_dark", 6, 2)
    s.put(ox + 3, oy + 19, "asphalt_dark", 4, 1)
    # Shadow
    s.put(ox + 3, oy + 20, "asphalt_dark", 4, 1) if oy + 20 < 200 else None


def draw_bollard(s: SVGSheet, ox: int, oy: int):
    """6×12 short yellow-capped black bollard."""
    # Black body
    s.put(ox + 1, oy + 2, "black", 4, 9)
    s.put(ox + 1, oy + 2, "stone_dark", 1, 9)  # highlight
    # Yellow cap
    s.put(ox, oy, "de_lijn_yellow", 6, 3)
    s.put(ox, oy, "ochre", 6, 1)   # top highlight
    s.put(ox, oy + 2, "cream_dark", 6, 1)  # cap bottom shadow
    # Reflective band
    s.put(ox + 1, oy + 6, "stone_light", 4, 1)
    # Base
    s.put(ox, oy + 11, "stone_dark", 6, 1)
    s.put(ox + 1, oy + 11, "asphalt_dark", 4, 1)


def draw_street_sign(s: SVGSheet, ox: int, oy: int):
    """12×20 Turnhoutsebaan blue street sign on pole."""
    # Post
    s.put(ox + 5, oy + 8, "stone_mid", 2, 12)
    s.put(ox + 5, oy + 8, "stone_light", 1, 12)

    # Sign board (blue background)
    s.put(ox, oy, "de_lijn_blue", 12, 9)
    # White border
    s.put(ox, oy, "white", 12, 1)
    s.put(ox, oy + 8, "white", 12, 1)
    s.put(ox, oy, "white", 1, 9)
    s.put(ox + 11, oy, "white", 1, 9)
    # White text (simplified pixel bars)
    # "TURNHOUTSEBAAN"
    s.put(ox + 1, oy + 2, "white", 10, 1)
    s.put(ox + 1, oy + 4, "white", 8, 1)
    # "BORGERHOUT"
    s.put(ox + 1, oy + 6, "white", 9, 1)

    # Sign highlight
    s.put(ox, oy, "sky_pale", 12, 1)
    s.put(ox, oy, "sky_pale", 1, 9)

    # Ground base
    s.put(ox + 4, oy + 19, "stone_dark", 4, 1)


def draw_bicycle_prop(s: SVGSheet, ox: int, oy: int):
    """16×16 parked bicycle chained to pole."""
    # Wheels (circles approximated)
    # Rear wheel
    for (wx, wy) in [(4,3),(3,4),(2,5),(2,6),(2,7),(3,8),(4,9),(5,10),(6,10),(7,9),
                      (8,8),(8,7),(8,6),(8,5),(7,4),(6,3),(5,3)]:
        s.put(ox+wx, oy+wy, "stone_dark", 1, 1)
    # Front wheel
    for (wx, wy) in [(12,3),(11,4),(10,5),(10,6),(10,7),(11,8),(12,9),(13,10),(14,10),
                      (15,9),(15,8),(15,7),(15,6),(15,5),(14,4),(13,3)]:
        s.put(ox+wx, oy+wy, "stone_dark", 1, 1)
    # Spokes (simplified)
    s.put(ox+5, oy+6, "stone_mid", 3, 1)  # rear spoke H
    s.put(ox+6, oy+5, "stone_mid", 1, 3)  # rear spoke V
    s.put(ox+12, oy+6, "stone_mid", 3, 1)
    s.put(ox+13, oy+5, "stone_mid", 1, 3)
    # Frame (top tube, down tube, chain stay)
    s.put(ox+7, oy+4, "stone_dark", 1, 1)  # head
    s.put(ox+8, oy+4, "stone_mid",  4, 1)  # top tube
    s.put(ox+8, oy+5, "stone_mid",  1, 3)  # seat tube
    s.put(ox+8, oy+7, "stone_mid",  4, 1)  # chain stay
    # Handlebar
    s.put(ox+11, oy+3, "stone_dark", 1, 2)
    s.put(ox+10, oy+3, "stone_light", 2, 1)
    # Seat
    s.put(ox+7, oy+3, "stone_dark", 2, 1)
    s.put(ox+7, oy+2, "stone_light", 2, 1)
    # Chain
    s.put(ox+9, oy+8, "stone_light", 3, 1)


# ── NPC Sprites ───────────────────────────────────────────────────────────────

def draw_npc_hijab_woman(s: SVGSheet, ox: int, oy: int, stride: bool = False):
    """20×48 Hijab woman — modestly dressed, abaya."""
    leg_offset = 2 if stride else 0

    # HEAD + HIJAB
    # Face (small visible area)
    s.put(ox + 7, oy + 6,  "cream_light",  6, 8)  # face
    s.put(ox + 8, oy + 9,  "black",        1, 1)  # eye
    s.put(ox + 11,oy + 9,  "black",        1, 1)
    # Hijab (dark blue/teal — use stone_dark + night mix)
    s.put(ox + 4, oy + 2,  "stone_dark",   12, 6)  # top hijab
    s.put(ox + 3, oy + 7,  "stone_dark",   14, 10) # drape sides
    s.put(ox + 5, oy + 7,  "night",        10, 4)  # dark centre

    # BODY — abaya (full-length dark robe)
    s.put(ox + 3, oy + 17, "night",         14, 24)  # abaya body
    s.put(ox + 3, oy + 17, "stone_dark",    14, 1)   # shoulder line
    s.put(ox + 3, oy + 17, "stone_dark",    1, 24)   # left edge
    s.put(ox + 16,oy + 17, "black",         1, 24)   # right shadow

    # SLEEVES
    s.put(ox + 1, oy + 18, "night",         3, 16)   # left sleeve
    s.put(ox + 1, oy + 18, "stone_dark",    1, 16)
    s.put(ox + 16,oy + 18, "night",         3, 16)   # right sleeve
    s.put(ox + 18,oy + 18, "black",         1, 16)

    # HANDS (visible at hem)
    s.put(ox + 1,  oy + 34, "cream_light",  2, 4)
    s.put(ox + 17, oy + 34, "cream_light",  2, 4)

    # LEGS / FEET (barely visible below abaya)
    s.put(ox + 6,  oy + 40, "stone_dark",   4, 6)   # left foot
    s.put(ox + 10, oy + 40 + leg_offset, "stone_dark",   4, 4)  # right foot (stride)
    # Shoes
    s.put(ox + 6,  oy + 44, "black",        4, 2)
    s.put(ox + 10, oy + 44, "black",        4, 2)

    # NW highlight on hijab
    s.put(ox + 4, oy + 2, "stone_mid",      8, 1)


def draw_npc_djellaba_man(s: SVGSheet, ox: int, oy: int, stride: bool = False):
    """20×48 Man in traditional djellaba — cream/tan robe with hood."""
    leg_offset = 2 if stride else 0

    # HEAD (with kufi cap)
    s.put(ox + 7, oy + 6,  "cream_dark",   6, 2)   # kufi cap
    s.put(ox + 6, oy + 5,  "cream_mid",    8, 3)
    s.put(ox + 7, oy + 8,  "ochre",        6, 8)   # face (warm skin tone)
    s.put(ox + 8, oy + 11, "black",        1, 1)   # eye
    s.put(ox + 11,oy + 11, "black",        1, 1)
    # Beard
    s.put(ox + 7, oy + 14, "stone_dark",   6, 3)

    # HOOD (back, visible behind head)
    s.put(ox + 5, oy + 4,  "cream_mid",    10, 3)  # hood top
    s.put(ox + 4, oy + 7,  "cream_mid",    2, 6)   # hood left
    s.put(ox + 14,oy + 7,  "cream_mid",    2, 6)   # hood right

    # DJELLABA BODY — wide, flowing cream robe
    s.put(ox + 3, oy + 17, "cream_mid",    14, 24)  # robe body
    # Texture / weave lines
    for gy in range(0, 24, 4):
        s.put(ox + 3, oy + 17 + gy, "cream_dark", 14, 1)
    # Robe sides (slightly darker)
    s.put(ox + 3, oy + 17, "cream_dark",   1, 24)
    s.put(ox + 16,oy + 17, "cream_dark",   1, 24)
    # Centre stripe decoration
    s.put(ox + 9, oy + 17, "ochre",        2, 18)  # centre slit/trim

    # SLEEVES (wide)
    s.put(ox + 0, oy + 18, "cream_mid",    4, 14)
    s.put(ox + 0, oy + 18, "cream_dark",   1, 14)
    s.put(ox + 16,oy + 18, "cream_mid",    4, 14)
    s.put(ox + 19,oy + 18, "cream_dark",   1, 14)

    # HANDS
    s.put(ox + 1,  oy + 30, "ochre",       2, 4)
    s.put(ox + 17, oy + 30, "ochre",       2, 4)

    # FEET (babouche slippers)
    s.put(ox + 6,  oy + 40, "cream_mid",   4, 8)
    s.put(ox + 10, oy + 40 + leg_offset, "cream_mid", 4, 6)
    # Slipper tips (pointed)
    s.put(ox + 5,  oy + 45, "ochre",       2, 1)
    s.put(ox + 10, oy + 45, "ochre",       2, 1)

    # NW highlight
    s.put(ox + 3, oy + 17, "cream_light",  14, 1)
    s.put(ox + 3, oy + 17, "cream_light",  1, 24)


def draw_npc_child(s: SVGSheet, ox: int, oy: int, stride: bool = False):
    """16×32 Small child — playful posture."""
    leg_offset = 2 if stride else 0

    # HEAD (bigger relative to body)
    s.put(ox + 4, oy + 2,  "cream_light",  8, 9)   # face
    s.put(ox + 3, oy + 1,  "wood_dark",    10, 4)  # hair (dark)
    s.put(ox + 5, oy + 6,  "black",        1, 1)   # left eye
    s.put(ox + 9, oy + 6,  "black",        1, 1)   # right eye
    s.put(ox + 6, oy + 7,  "black",        1, 1)   # pupil twinkle
    s.put(ox + 9, oy + 8,  "red_ui",       3, 1)   # smile
    # Cheek blush
    s.put(ox + 4, oy + 8,  "brick_light",  2, 1)
    s.put(ox + 10,oy + 8,  "brick_light",  2, 1)

    # BODY — colourful hoodie (blue tracksuit)
    s.put(ox + 4, oy + 11, "de_lijn_blue", 8, 10)
    # Hoodie pocket
    s.put(ox + 5, oy + 18, "night",        6, 3)
    # Sleeves
    s.put(ox + 2, oy + 11, "de_lijn_blue", 3, 8)
    s.put(ox + 2, oy + 11, "night",        1, 8)   # shadow
    s.put(ox + 11,oy + 11, "de_lijn_blue", 3, 8)
    s.put(ox + 13,oy + 11, "night",        1, 8)

    # HANDS
    s.put(ox + 2,  oy + 19, "cream_light", 2, 3)
    s.put(ox + 12, oy + 19, "cream_light", 2, 3)

    # PANTS (dark)
    s.put(ox + 5, oy + 21, "stone_dark", 6, 7)
    s.put(ox + 4, oy + 21, "night",      1, 7)

    # SHOES (sneakers — white with colour stripe)
    s.put(ox + 5,  oy + 28, "white",      3, 4)
    s.put(ox + 5,  oy + 29, "de_lijn_blue", 3, 1)  # stripe
    s.put(ox + 8,  oy + 28 + leg_offset, "white",  3, 2)
    s.put(ox + 8,  oy + 29 + leg_offset, "de_lijn_blue", 3, 1)

    # NW highlight on hoodie
    s.put(ox + 4, oy + 11, "sky_pale",    4, 1)
    s.put(ox + 4, oy + 11, "sky_pale",    1, 5)


def draw_npc_delivery(s: SVGSheet, ox: int, oy: int, stride: bool = False):
    """20×48 Delivery rider in orange safety vest + helmet."""
    leg_offset = 2 if stride else 0

    # HELMET
    s.put(ox + 6, oy + 2,  "stone_dark",   8, 6)   # helmet body
    s.put(ox + 5, oy + 3,  "stone_dark",   10, 5)
    s.put(ox + 6, oy + 2,  "stone_mid",    8, 1)   # top highlight
    s.put(ox + 5, oy + 3,  "stone_light",  4, 2)   # NW reflection
    # Visor
    s.put(ox + 5, oy + 7,  "glass",        10, 2)
    s.put(ox + 5, oy + 7,  "sky_light",    4, 1)   # visor reflection

    # FACE
    s.put(ox + 7, oy + 9,  "cream_mid",    6, 5)
    s.put(ox + 8, oy + 11, "black",        1, 1)
    s.put(ox + 11,oy + 11, "black",        1, 1)

    # ORANGE SAFETY VEST
    s.put(ox + 4, oy + 14, "ochre",        12, 18)  # vest
    # Reflective strips
    s.put(ox + 4, oy + 20, "white",        12, 1)
    s.put(ox + 4, oy + 24, "white",        12, 1)
    # Vest shadow
    s.put(ox + 4, oy + 14, "cream_dark",   1, 18)
    s.put(ox + 15,oy + 14, "cream_dark",   1, 18)

    # DARK SHIRT under vest
    s.put(ox + 3, oy + 14, "night",        1, 18)  # left side
    s.put(ox + 16,oy + 14, "night",        1, 18)  # right side

    # SLEEVES (orange)
    s.put(ox + 1, oy + 15, "ochre",        3, 12)
    s.put(ox + 1, oy + 15, "cream_dark",   1, 12)
    s.put(ox + 16,oy + 15, "ochre",        3, 12)
    s.put(ox + 18,oy + 15, "cream_dark",   1, 12)

    # HANDS (gloves — black)
    s.put(ox + 1,  oy + 27, "black",       3, 5)
    s.put(ox + 16, oy + 27, "black",       3, 5)

    # DELIVERY BAG / BACKPACK (on back, dark box)
    s.put(ox + 3, oy + 16, "stone_dark",   14, 14)  # bag
    s.put(ox + 3, oy + 16, "stone_mid",    14, 1)   # bag top

    # PANTS (black)
    s.put(ox + 5, oy + 32, "night",        10, 10)
    s.put(ox + 5, oy + 32, "black",        1, 10)

    # BOOTS
    s.put(ox + 5,  oy + 42, "black",       4, 6)
    s.put(ox + 5,  oy + 42, "stone_dark",  1, 6)   # highlight
    s.put(ox + 9,  oy + 42 + leg_offset, "black", 4, 4)
    s.put(ox + 9,  oy + 42 + leg_offset, "stone_dark", 1, 4)


# ── Sheet Generators ──────────────────────────────────────────────────────────

SPRITES_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_materials_sheet():
    """Sheet 1 — Ground & Wall Tiles (256×128 px game / 512×256 px SVG)."""
    s = SVGSheet(256, 128, "MATERIALS SHEET — Base tiles, 32×32 px each")

    tiles = [
        # Row 0: Wall / facade tiles
        ("brick_standard",    0,   0, draw_brick_tile),
        ("render_cream",      32,  0, lambda sh, x, y: draw_render_tile(sh, x, y, "cream_mid")),
        ("render_ochre",      64,  0, lambda sh, x, y: draw_render_tile(sh, x, y, "ochre")),
        ("stone_ashlar",      96,  0, None),
        ("roof_tiles",        128, 0, draw_roof_tile),
        ("gable_trapezoid",   160, 0, None),  # See arch_details
        ("sky_panel",         192, 0, None),
        ("grass_patch",       224, 0, draw_grass_tile),
        # Row 1: Ground tiles
        ("asphalt_road",      0,   32, draw_asphalt_tile),
        ("sidewalk_slab",     32,  32, draw_sidewalk_tile),
        ("cobblestone",       64,  32, draw_cobble_tile),
        ("tram_track",        96,  32, draw_tram_track_tile),
        ("zebra_crossing",    128, 32, draw_zebra_tile),
        ("lane_marking",      160, 32, draw_lane_mark_tile),
        ("tram_stop_platform",192, 32, draw_tram_stop_tile),
        ("asphalt_damaged",   224, 32, None),
    ]

    # Stone ashlar (row 0, col 3)
    ox, oy = 96, 0
    s.put(ox, oy, "stone_mid", 32, 32)
    for sy in range(0, 32, 8):
        off = 0 if (sy//8) % 2 == 0 else 6
        for sx in range(off, 32, 12):
            bw = min(10, 32-sx)
            s.put(ox+sx+1, oy+sy+1, "stone_light", bw, 5)
            s.put(ox+sx+1, oy+sy+1, "stone_pale",  bw, 1)
            s.put(ox+sx+1, oy+sy+5, "stone_dark",  bw, 1)

    # Sky panel (row 0, col 6)
    ox, oy = 192, 0
    s.put(ox, oy, "sky_light", 32, 16)
    s.put(ox, oy+16, "sky_mid", 32, 10)
    s.put(ox, oy+26, "sky_pale", 32, 6)
    # Cloud wisps
    s.put(ox+4,  oy+3, "cloud", 12, 3)
    s.put(ox+18, oy+8, "cloud", 8, 2)

    # Asphalt damaged (row 1, col 7)
    ox, oy = 224, 32
    draw_asphalt_tile(s, ox, oy)
    # Cracks
    for cx, cy in [(5,5),(6,6),(7,7),(8,8),(8,9),(9,10),(10,10)]:
        s.put(ox+cx, oy+cy, "asphalt_dark", 1, 1)
    for cx, cy in [(20,15),(21,16),(22,17),(23,18),(24,18)]:
        s.put(ox+cx, oy+cy, "asphalt_dark", 1, 1)

    # Gable placeholder = mini trapgevel swatch
    ox, oy = 160, 0
    s.put(ox, oy, "sky_mid", 32, 32)
    s.put(ox, oy+4, "brick_mid", 32, 28)
    s.put(ox, oy+4, "brick_light", 32, 1)

    # Now draw actual tiles
    for name, tx, ty, fn in tiles:
        if fn:
            fn(s, tx, ty)
        # Label
        s.label(tx + 1, ty + 30, name[:8])

    # Labels row
    for i, (name, tx, ty, _) in enumerate(tiles):
        s.label(tx + 1, ty + 30, name[:8])

    svg_path = os.path.join(SPRITES_DIR, "environment/tilesets/materials_sheet.svg")
    png_path = os.path.join(SPRITES_DIR, "environment/tilesets/materials_sheet.png")
    s.save(svg_path)
    s.to_pil(png_path)


def generate_props_sheet():
    """Sheet 2 — Street Props (160×64 px game / 320×128 px SVG)."""
    s = SVGSheet(160, 64, "PROPS SHEET — Street furniture, Turnhoutsebaan")

    # Lamp post at x=0
    draw_lamp_post(s, 0, 24)
    s.label(0, 62, "lamp")

    # Tree at x=16
    draw_tree_grate(s, 16, 32)
    s.label(16, 62, "tree")

    # Bench at x=40
    draw_bench(s, 40, 46)
    s.label(40, 62, "bench")

    # Bin at x=68
    draw_bin(s, 68, 44)
    s.label(68, 62, "bin")

    # Bollard at x=82
    draw_bollard(s, 82, 50)
    s.label(82, 62, "bollard")

    # Street sign at x=92
    draw_street_sign(s, 92, 40)
    s.label(92, 62, "sign")

    # Bicycle prop at x=110
    draw_bicycle_prop(s, 110, 46)
    s.label(110, 62, "bicycle")

    svg_path = os.path.join(SPRITES_DIR, "environment/props/props_sheet.svg")
    png_path = os.path.join(SPRITES_DIR, "environment/props/props_sheet.png")
    s.save(svg_path)
    s.to_pil(png_path)


def generate_arch_details_sheet():
    """Sheet 3 — Architectural Details (256×128 px game / 512×256 px SVG)."""
    s = SVGSheet(256, 128, "ARCH DETAILS — Windows, Doors, Gables for Flemish ribbon buildings")

    # ─ WINDOWS (row 0, y=0) ─
    s.label(0,   8, "win_arch")
    draw_window_arched(s, 0, 10)

    s.label(20, 8, "win_rect")
    draw_window_rect(s, 20, 10)

    s.label(38, 8, "win_shut")
    draw_window_shuttered(s, 38, 8)

    s.label(56, 8, "win_nite")
    draw_window_night(s, 56, 10)

    s.label(74, 8, "win_bay")
    draw_window_bay(s, 74, 4)

    s.label(98, 8, "win_brkn")
    draw_window_broken(s, 98, 10)

    # ─ DOORS (row 0 continued, x=120+) ─
    s.label(120, 8, "door_arch")
    draw_door_wooden_arch(s, 120, 0)

    s.label(140, 8, "door_glas")
    draw_door_modern_glass(s, 140, 0)

    s.label(160, 8, "door_clar")
    draw_door_cellar(s, 160, 12)

    s.label(180, 8, "door_shut")
    draw_door_shutter(s, 180, 8)

    # ─ GABLES (row 1, y=64) ─
    s.label(0,   68, "gable_trap")
    draw_gable_trap(s, 0, 70)

    s.label(36,  68, "gable_klok")
    draw_gable_klok(s, 36, 70)

    s.label(72,  68, "gable_flat")
    draw_gable_flat(s, 72, 78)

    s.label(108, 68, "gable_tria")
    draw_gable_triangular(s, 108, 70)

    svg_path = os.path.join(SPRITES_DIR, "environment/buildings/arch_details_sheet.svg")
    png_path = os.path.join(SPRITES_DIR, "environment/buildings/arch_details_sheet.png")
    s.save(svg_path)
    s.to_pil(png_path)


def generate_npc_extended_sheet():
    """Sheet 4 — Extended NPC Sheet (8 NPCs × 2 frames, 20×48 px each)."""
    # 8 NPCs * 2 frames = 16 columns; each NPC needs max 24px wide; rows for idle+stride
    s = SVGSheet(320, 100, "NPC EXTENDED SHEET — All 8 Borgerhout NPCs")

    npcs = [
        ("hijab_woman",    0,   draw_npc_hijab_woman),
        ("djellaba_man",   40,  draw_npc_djellaba_man),
        ("child",          80,  draw_npc_child),
        ("delivery",       110, draw_npc_delivery),
    ]

    for name, x, fn in npcs:
        # Idle frame
        fn(s, x, 0, stride=False)
        s.label(x, 96, name[:8])
        # Stride frame (shifted right by 20 or 24)
        stride_x = x + 20 if name != "delivery" else x + 22
        fn(s, stride_x, 0, stride=True)

    svg_path = os.path.join(SPRITES_DIR, "characters/npcs/npc_extended_sheet.svg")
    png_path = os.path.join(SPRITES_DIR, "characters/npcs/npc_extended_sheet.png")
    s.save(svg_path)
    s.to_pil(png_path)


def generate_vehicles_sheet():
    """Sheet 5 — Vehicles (bus, cars, scooter, bakfiets, bicycle prop)."""
    s = SVGSheet(320, 64, "VEHICLES SHEET — De Lijn bus, city cars, scooter, bakfiets")

    # De Lijn Bus (200×52 game-px, scaled to 100×26 for sheet)
    # Use simplified side view at 1:2
    ox, oy = 0, 4
    # Bus body
    s.put(ox, oy + 4, "white",        100, 22)
    # De Lijn livery
    s.put(ox, oy + 4, "de_lijn_blue", 100, 6)   # upper stripe
    s.put(ox, oy + 18,"de_lijn_yellow",100, 2)  # yellow lower stripe
    # Windows (simplified)
    for wx in [4, 18, 32, 46, 60, 74, 88]:
        s.put(ox + wx, oy + 5, "glass", 10, 4)
        s.put(ox + wx, oy + 5, "sky_pale", 4, 2)  # reflection
    # Doors
    s.put(ox + 10, oy + 10, "stone_dark", 6, 10)
    s.put(ox + 70, oy + 10, "stone_dark", 6, 10)
    # Wheels
    for wx in [8, 82]:
        s.put(ox + wx - 2, oy + 24, "black", 8, 6)
        s.put(ox + wx - 1, oy + 24, "stone_mid", 2, 2)  # hubcap
    # Bumpers
    s.put(ox, oy + 4, "stone_mid", 2, 22)
    s.put(ox + 98,oy + 4, "stone_mid", 2, 22)
    # Destination board
    s.put(ox + 4, oy + 4, "night", 12, 5)
    s.put(ox + 5, oy + 5, "de_lijn_yellow", 6, 3)  # destination text
    # Shadow
    s.put(ox + 4, oy + 30, "asphalt_dark", 92, 2)
    s.label(ox, 60, "bus_delijn")

    # Car variants (simplified 32×16 each, 6 colors)
    car_colors = ["brick_mid", "de_lijn_blue", "stone_mid", "night", "grass", "de_lijn_yellow"]
    for ci, cc in enumerate(car_colors):
        cx = 108 + ci * 36
        # Body
        s.put(cx, oy + 8, cc, 32, 14)
        # Roof (narrower)
        s.put(cx + 6, oy + 2, cc, 20, 8)
        # Windscreen
        s.put(cx + 8, oy + 3, "glass", 7, 6)
        s.put(cx + 9, oy + 3, "sky_pale", 3, 2)
        # Rear screen
        s.put(cx + 18,oy + 3, "glass", 6, 6)
        # Wheels
        for wx in [4, 24]:
            s.put(cx + wx, oy + 20, "black", 6, 4)
            s.put(cx + wx + 1, oy + 20, "stone_mid", 2, 2)
        # Shadow
        s.put(cx + 2, oy + 24, "asphalt_dark", 28, 2)
    s.label(108, 60, "cars_x6")

    svg_path = os.path.join(SPRITES_DIR, "vehicles/vehicles_sheet.svg")
    png_path = os.path.join(SPRITES_DIR, "vehicles/vehicles_sheet.png")
    s.save(svg_path)
    s.to_pil(png_path)


def generate_shop_facades_sheet():
    """Sheet 6 — Real Turnhoutsebaan shop façade details (awnings, signs, shopfronts)."""
    s = SVGSheet(320, 96, "SHOP FACADES — Real Turnhoutsebaan businesses")

    shops = [
        # id, x, awning_color, sign_color, name
        ("budgetmkt",  0,   "red_ui",         "white",  "BUDGET MKT"),
        ("hammam",     40,  "stone_dark",     "ochre",  "HAMMAM"),
        ("aladdin",    80,  "de_lijn_yellow", "black",  "ALADDIN"),
        ("frituur",    120, "red_ui",         "white",  "FRITUUR"),
        ("theehuys",   160, "cream_dark",     "night",  "THEEHUYS"),
        ("nachtw",     200, "night",          "de_lijn_yellow", "NACHT W"),
        ("charif",     240, "de_lijn_yellow", "wood_dark", "CHARIF"),
        ("borgerHub",  280, "grass",          "white",  "BORGER HUB"),
    ]

    for (sid, ox, awning, sign_txt_c, name) in shops:
        oy = 8
        # Facade stone base
        s.put(ox, oy, "cream_mid", 36, 80)
        # Brick above
        s.put(ox, oy, "brick_mid", 36, 24)
        # First floor window
        draw_window_arched(s, ox + 10, oy + 2)
        # Awning over shopfront
        s.put(ox, oy + 48, awning, 36, 12)
        # Awning highlight
        s.put(ox, oy + 48, "cream_light" if awning in ["de_lijn_yellow","cream_dark"] else awning, 36, 1)
        # Awning stripes (if applicable)
        for i in range(0, 36, 6):
            s.put(ox + i, oy + 50, "white" if awning != "white" else "stone_mid", 3, 8)
        # Shop window (ground floor glass)
        s.put(ox + 2, oy + 60, "glass",  32, 16)
        s.put(ox + 2, oy + 60, "sky_pale", 10, 6)  # reflection
        # Door in centre
        s.put(ox + 15, oy + 62, "stone_dark", 6, 14)
        s.put(ox + 16, oy + 62, "glass",      4, 12)
        # Sign text (simplified bars)
        s.put(ox + 2, oy + 49, sign_txt_c, 30, 3)
        # Label
        s.label(ox + 2, 90, name[:9])

    svg_path = os.path.join(SPRITES_DIR, "environment/buildings/shop_facades_sheet.svg")
    png_path = os.path.join(SPRITES_DIR, "environment/buildings/shop_facades_sheet.png")
    s.save(svg_path)
    s.to_pil(png_path)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Turnhoutsebaan RPG — Sprite Generator")
    print("=" * 40)

    print("\n[1/6] Materials sheet (ground & wall tiles)...")
    generate_materials_sheet()

    print("\n[2/6] Props sheet (street furniture)...")
    generate_props_sheet()

    print("\n[3/6] Architectural details sheet (windows, doors, gables)...")
    generate_arch_details_sheet()

    print("\n[4/6] Extended NPC sheet (4 new NPC types)...")
    generate_npc_extended_sheet()

    print("\n[5/6] Vehicles sheet (bus, cars, scooter)...")
    generate_vehicles_sheet()

    print("\n[6/6] Shop facades sheet (real Turnhoutsebaan shops)...")
    generate_shop_facades_sheet()

    print("\nDone! Sprites written to Sprites/ subdirectories.")
    if not HAS_PIL:
        print("Install Pillow for PNG export: pip3 install Pillow")
