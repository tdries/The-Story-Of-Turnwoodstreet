#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — Vehicle Sprite Sheet
==========================================
7 vehicle types for the Turnhoutsebaan street scene.
Vehicles viewed from slightly above and to the left (oblique top-down),
moving left to right.

Frame layout: 64x28 game pixels per vehicle, SCALE=5 → 320x140 px per frame
1 frame per vehicle (static)
7 vehicles → horizontal sheet: 2240x140 px

Run: python3 generate_vehicles.py
"""

import os
from PIL import Image, ImageDraw

# ── Config ────────────────────────────────────────────────────────────────────
SCALE       = 5          # px per game pixel
GW, GH      = 64, 28     # game frame size per vehicle
FW          = GW * SCALE  # 320 px
FH          = GH * SCALE  # 140 px
NUM_VEHICLES = 7

BASE_DIR    = os.path.join(os.path.dirname(__file__), "..", "assets", "Sprites", "vehicles")

# ── Palette ───────────────────────────────────────────────────────────────────
ASPHALT     = (0x48, 0x44, 0x40, 255)
SHADOW      = (0x20, 0x1C, 0x18, 100)
GLASS_D     = (0x18, 0x28, 0x38, 255)
GLASS_L     = (0x48, 0x68, 0x88, 255)
GLASS_GLINT = (0x88, 0xA8, 0xC0, 255)
TYRE        = (0x20, 0x1C, 0x18, 255)
TYRE_HL     = (0x38, 0x34, 0x30, 255)
CHROME      = (0xC0, 0xBC, 0xB8, 255)
WHITE_C     = (0xF0, 0xEE, 0xE8, 255)
BLUE_CAR    = (0x24, 0x48, 0x8C, 255)
BLUE_CAR_L  = (0x38, 0x5C, 0xA0, 255)
BLUE_CAR_D  = (0x18, 0x34, 0x64, 255)
RED_CAR     = (0xC0, 0x20, 0x10, 255)
RED_CAR_L   = (0xD8, 0x38, 0x28, 255)
RED_CAR_D   = (0x88, 0x14, 0x08, 255)
SILVER      = (0x90, 0x90, 0x98, 255)
SILVER_L    = (0xC0, 0xBC, 0xC0, 255)
SILVER_D    = (0x60, 0x60, 0x68, 255)
TAXI_BLUE   = (0x18, 0x48, 0x88, 255)
TAXI_BLUE_L = (0x28, 0x58, 0x98, 255)
TAXI_BLUE_D = (0x10, 0x34, 0x60, 255)
DELIJN_BL   = (0x10, 0x38, 0x78, 255)
DELIJN_BL_L = (0x20, 0x48, 0x88, 255)
DELIJN_BL_D = (0x08, 0x24, 0x54, 255)
DELIJN_YL   = (0xDD, 0xB8, 0x00, 255)
DELIJN_YL_L = (0xF0, 0xCC, 0x20, 255)
SCOOTER_R   = (0xC0, 0x18, 0x08, 255)
SCOOTER_R_L = (0xD8, 0x30, 0x20, 255)
SCOOTER_R_D = (0x80, 0x10, 0x04, 255)
DARK_METAL  = (0x28, 0x24, 0x20, 255)
DARK_METAL_L = (0x40, 0x3C, 0x38, 255)
HEADLIGHT   = (0xF4, 0xEC, 0xC0, 255)
TAILLIGHT   = (0xCC, 0x30, 0x10, 255)
TAILLIGHT_L = (0xFF, 0x50, 0x30, 255)
UNDERBODY   = (0x30, 0x2C, 0x28, 255)
ROAD_LINE   = (0x60, 0x5C, 0x58, 255)
WHEEL_RIM   = (0x88, 0x84, 0x80, 255)
VAN_GREY    = (0xC0, 0xBC, 0xB8, 255)
VAN_GREY_L  = (0xD8, 0xD4, 0xD0, 255)
VAN_GREY_D  = (0x90, 0x8C, 0x88, 255)
RUBBER_TRIM = (0x30, 0x2C, 0x28, 255)
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


# ── Vehicle drawing functions ─────────────────────────────────────────────────
# All vehicles are drawn in game-pixel space (0..63 x, 0..27 y).
# Vehicles are viewed from slightly above (oblique), moving left to right.
# Front of car is on the RIGHT side.

def draw_shadow(d, x_start, y_start, width, height):
    """Draw a semi-transparent shadow below and right of vehicle."""
    # Shadow drawn as a dark rectangle offset
    for gy in range(y_start, y_start + height):
        for gx in range(x_start + 1, x_start + width + 2):
            x1 = gx * SCALE
            y1 = gy * SCALE
            x2 = (gx + 1) * SCALE - 1
            y2 = (gy + 1) * SCALE - 1
            d.rectangle([x1, y1, x2, y2], fill=SHADOW)


def draw_wheel(d, cx, cy, is_front=False):
    """Draw a wheel as a filled rectangle (top-down oblique view)."""
    # Tyre (outer)
    px(d, cx-2, cy, 4, 2, TYRE)
    # Tyre top highlight
    px(d, cx-2, cy, 4, 1, TYRE_HL)
    # Wheel rim (inner circle approximated as rect)
    px(d, cx-1, cy, 2, 2, WHEEL_RIM)
    # Hub cap
    px(d, cx, cy, 1, 1, CHROME)
    if is_front:
        # Slightly more visible tread on front wheels
        px(d, cx-2, cy+1, 1, 1, (0x14, 0x10, 0x0C, 255))
        px(d, cx+1, cy+1, 1, 1, (0x14, 0x10, 0x0C, 255))


def draw_clio(d, body_color, body_light, body_dark, name_tag="clio"):
    """Draw a small hatchback (Renault Clio-like).
    Car occupies game coords: body from x=4..57, y=6..24
    """
    # Shadow (under car, offset right)
    draw_shadow(d, 5, 22, 52, 3)

    # Underbody (dark sill)
    px(d, 4, 22, 53, 2, UNDERBODY)

    # Main body sides (lower body panel)
    px(d, 4, 15, 53, 7, body_color)
    # Body shadow right (darker panel, simulating top-down angle)
    px(d, 50, 15, 7, 7, body_dark)
    # Body highlight left edge
    px(d, 4, 15, 3, 7, body_light)
    # Lower body trim / rocker panel
    px(d, 5, 21, 52, 1, body_dark)

    # Roof (slightly narrower, centered, raised appearance)
    px(d, 12, 9, 36, 6, body_color)
    # Roof top highlight strip
    px(d, 13, 9, 20, 1, body_light)
    # Roof right shadow
    px(d, 42, 9, 6, 6, body_dark)
    # Roof left highlight
    px(d, 12, 9, 3, 6, body_light)

    # A-pillar (front, right)
    px(d, 45, 9, 5, 6, body_dark)
    # C-pillar (rear, left)
    px(d, 12, 9, 3, 6, body_color)

    # Windscreen (front, right side) - dark glass
    px(d, 38, 9, 9, 6, GLASS_D)
    # Windscreen light reflection
    px(d, 38, 9, 4, 2, GLASS_GLINT)
    px(d, 42, 11, 2, 1, GLASS_L)

    # Rear window (left side)
    px(d, 14, 9, 8, 6, GLASS_D)
    px(d, 14, 9, 3, 2, GLASS_GLINT)

    # Side windows (middle section)
    px(d, 23, 9, 14, 6, GLASS_D)
    px(d, 23, 9, 5, 2, GLASS_GLINT)
    # Window frame / B-pillar
    px(d, 22, 9, 1, 6, body_color)
    px(d, 37, 9, 1, 6, body_color)

    # Door lines (subtle panel breaks)
    px(d, 22, 15, 1, 7, body_dark)
    px(d, 37, 15, 1, 7, body_dark)

    # Door handles
    px(d, 26, 18, 3, 1, CHROME)
    px(d, 41, 18, 3, 1, CHROME)

    # Front bumper
    px(d, 50, 16, 7, 5, body_dark)
    px(d, 55, 17, 2, 3, body_dark)
    # Front grille
    px(d, 52, 18, 5, 3, DARK_METAL)
    px(d, 52, 19, 5, 1, (0x18, 0x18, 0x14, 255))  # grille shadow
    # Headlights (right/front)
    px(d, 54, 16, 3, 2, HEADLIGHT)
    px(d, 54, 16, 1, 1, (0xFF, 0xFF, 0xE8, 255))  # bright center
    # Front fog light
    px(d, 54, 19, 2, 1, (0xE0, 0xD0, 0x90, 255))

    # Rear bumper (left side)
    px(d, 4, 16, 6, 5, body_dark)
    # Taillights (rear/left)
    px(d, 4, 16, 4, 2, TAILLIGHT)
    px(d, 5, 16, 2, 1, TAILLIGHT_L)
    # Exhaust
    px(d, 5, 21, 2, 1, DARK_METAL)

    # Wheels (4 wheels, front 2 more visible)
    # Front-right wheel
    draw_wheel(d, 48, 21, is_front=True)
    # Front-left wheel (foreshortened due to oblique view, slightly higher)
    px(d, 46, 20, 4, 1, TYRE)
    px(d, 47, 20, 2, 1, WHEEL_RIM)
    # Rear-right wheel
    draw_wheel(d, 14, 21, is_front=False)
    # Rear-left wheel (foreshortened)
    px(d, 12, 20, 4, 1, TYRE)
    px(d, 13, 20, 2, 1, WHEEL_RIM)

    # Wheel arches (body curves around wheels)
    px(d, 44, 20, 8, 2, body_color)
    px(d, 44, 21, 8, 1, body_dark)
    px(d, 10, 20, 8, 2, body_color)
    px(d, 10, 21, 8, 1, body_dark)

    # Licence plate (front)
    px(d, 56, 19, 2, 2, (0xF0, 0xEC, 0xE0, 255))
    px(d, 56, 20, 2, 1, (0x80, 0x80, 0x80, 255))  # plate detail


def draw_kangoo(d):
    """Draw a Renault Kangoo delivery van (white/grey, taller, boxy)."""
    # Shadow
    draw_shadow(d, 3, 22, 58, 3)

    # Underbody
    px(d, 3, 22, 58, 2, UNDERBODY)

    # Main body (boxy van shape, taller than car)
    px(d, 3, 11, 58, 11, VAN_GREY)
    # Body shadow right panel
    px(d, 53, 11, 8, 11, VAN_GREY_D)
    # Body highlight left
    px(d, 3, 11, 3, 11, VAN_GREY_L)
    # Body bottom trim
    px(d, 4, 20, 57, 1, VAN_GREY_D)

    # Roof (slightly raised, flat van roof)
    px(d, 5, 7, 54, 4, VAN_GREY)
    px(d, 5, 7, 25, 1, VAN_GREY_L)  # roof highlight
    px(d, 48, 7, 11, 4, VAN_GREY_D)  # roof shadow

    # Roof rack rails suggestion
    px(d, 8, 7, 2, 1, DARK_METAL_L)
    px(d, 16, 7, 2, 1, DARK_METAL_L)
    px(d, 24, 7, 2, 1, DARK_METAL_L)

    # Front windscreen (large, angled)
    px(d, 43, 8, 14, 8, GLASS_D)
    px(d, 43, 8, 7, 3, GLASS_GLINT)
    px(d, 50, 10, 4, 2, GLASS_L)
    # Windscreen A-pillar
    px(d, 42, 8, 1, 8, VAN_GREY_D)
    px(d, 57, 8, 1, 8, VAN_GREY_D)

    # Rear window (small, van style)
    px(d, 4, 11, 10, 7, GLASS_D)
    px(d, 4, 11, 4, 3, GLASS_GLINT)

    # Side window (driver's area, middle)
    px(d, 38, 11, 6, 6, GLASS_D)
    px(d, 38, 11, 3, 2, GLASS_GLINT)

    # Sliding side door panel (large, panel van)
    px(d, 15, 11, 22, 9, VAN_GREY)
    # Door channel (slight recess)
    px(d, 14, 11, 1, 9, VAN_GREY_D)
    px(d, 37, 11, 1, 9, VAN_GREY_D)
    # Door handle
    px(d, 20, 15, 5, 1, CHROME)
    # Riveted panel line (van look)
    px(d, 15, 14, 22, 1, VAN_GREY_D)

    # Door behind driver
    px(d, 37, 11, 5, 9, VAN_GREY)
    px(d, 41, 11, 1, 9, VAN_GREY_D)
    px(d, 42, 15, 2, 1, CHROME)

    # Front bumper (van, squarish)
    px(d, 55, 13, 8, 8, VAN_GREY_D)
    # Front grille (large van grille)
    px(d, 55, 15, 7, 5, DARK_METAL)
    px(d, 56, 16, 5, 3, (0x1C, 0x1C, 0x18, 255))
    # Headlights
    px(d, 58, 13, 4, 3, HEADLIGHT)
    px(d, 58, 13, 2, 1, (0xFF, 0xFF, 0xE8, 255))
    # Front badge
    px(d, 60, 19, 2, 1, (0xE0, 0xDC, 0xD4, 255))

    # Rear of van (left)
    px(d, 3, 11, 6, 11, VAN_GREY_D)
    # Rear doors (van rear doors)
    px(d, 4, 11, 5, 10, VAN_GREY_D)
    # Rear door handle
    px(d, 5, 16, 1, 2, CHROME)
    # Taillights
    px(d, 3, 11, 3, 3, TAILLIGHT)
    px(d, 4, 11, 1, 2, TAILLIGHT_L)

    # Delivery company livery: grey/white two-tone + logo area
    px(d, 15, 13, 22, 2, (0xD0, 0xCC, 0xC8, 255))

    # Wheels
    draw_wheel(d, 52, 21, is_front=True)
    px(d, 50, 20, 4, 1, TYRE)
    px(d, 51, 20, 2, 1, WHEEL_RIM)
    draw_wheel(d, 14, 21, is_front=False)
    px(d, 12, 20, 4, 1, TYRE)
    px(d, 13, 20, 2, 1, WHEEL_RIM)

    # Wheel arches
    px(d, 48, 20, 8, 2, VAN_GREY)
    px(d, 48, 21, 8, 1, VAN_GREY_D)
    px(d, 10, 20, 8, 2, VAN_GREY)
    px(d, 10, 21, 8, 1, VAN_GREY_D)

    # Licence plate
    px(d, 61, 20, 2, 2, (0xF0, 0xEC, 0xE0, 255))


def draw_suv(d):
    """Draw a larger silver SUV/estate car."""
    body_color = SILVER
    body_light = SILVER_L
    body_dark  = SILVER_D

    # Shadow
    draw_shadow(d, 3, 22, 58, 3)

    # Underbody
    px(d, 3, 22, 58, 2, UNDERBODY)

    # Main body (wider, taller than hatchback)
    px(d, 3, 13, 58, 9, body_color)
    px(d, 52, 13, 9, 9, body_dark)
    px(d, 3, 13, 4, 9, body_light)
    # Lower side trim (black rubber)
    px(d, 4, 20, 56, 2, RUBBER_TRIM)

    # Roof (flat, SUV roof line, long)
    px(d, 8, 7, 50, 6, body_color)
    px(d, 8, 7, 28, 1, body_light)
    px(d, 48, 7, 10, 6, body_dark)
    px(d, 8, 7, 3, 6, body_light)

    # Roof rails (SUV style)
    px(d, 10, 7, 2, 1, DARK_METAL_L)
    px(d, 22, 7, 2, 1, DARK_METAL_L)
    px(d, 34, 7, 2, 1, DARK_METAL_L)

    # Windscreen (large, slightly slanted)
    px(d, 42, 7, 14, 10, GLASS_D)
    px(d, 42, 7, 7, 3, GLASS_GLINT)
    px(d, 49, 9, 5, 3, GLASS_L)
    # A-pillar
    px(d, 41, 7, 1, 6, body_dark)

    # Side windows (large SUV windows)
    px(d, 20, 7, 10, 6, GLASS_D)
    px(d, 20, 7, 4, 2, GLASS_GLINT)
    # B-pillar
    px(d, 30, 7, 2, 6, body_color)

    # Rear side window
    px(d, 9, 7, 10, 6, GLASS_D)
    px(d, 9, 7, 4, 2, GLASS_GLINT)
    # C-pillar
    px(d, 8, 7, 1, 6, body_color)

    # Door panels
    px(d, 19, 13, 1, 9, body_dark)
    px(d, 32, 13, 1, 9, body_dark)
    px(d, 41, 13, 1, 9, body_dark)

    # Door handles (SUV style, longer)
    px(d, 22, 17, 4, 1, CHROME)
    px(d, 34, 17, 4, 1, CHROME)

    # Front bumper (large, SUV)
    px(d, 53, 14, 10, 7, body_dark)
    # Grille (horizontal slat style)
    px(d, 54, 16, 8, 4, DARK_METAL)
    px(d, 54, 17, 8, 1, (0x1C, 0x1C, 0x18, 255))
    px(d, 54, 19, 8, 1, (0x1C, 0x1C, 0x18, 255))
    # Headlights (LED style, wider)
    px(d, 56, 14, 5, 2, HEADLIGHT)
    px(d, 56, 14, 2, 1, (0xFF, 0xFF, 0xE8, 255))
    # DRL strip (LED daytime running)
    px(d, 53, 14, 10, 1, (0xF0, 0xE8, 0xC0, 255))

    # Rear (left)
    px(d, 3, 13, 6, 9, body_dark)
    # Taillights (LED style, wide)
    px(d, 3, 13, 5, 3, TAILLIGHT)
    px(d, 4, 13, 3, 1, TAILLIGHT_L)
    # Tail badge
    px(d, 5, 18, 2, 1, CHROME)

    # Wheels (larger diameter SUV wheels)
    draw_wheel(d, 51, 21, is_front=True)
    px(d, 48, 20, 5, 1, TYRE)
    px(d, 49, 20, 3, 1, WHEEL_RIM)
    draw_wheel(d, 13, 21, is_front=False)
    px(d, 10, 20, 5, 1, TYRE)
    px(d, 11, 20, 3, 1, WHEEL_RIM)

    # Wheel arches (flared)
    px(d, 47, 19, 9, 3, body_color)
    px(d, 47, 21, 9, 1, body_dark)
    px(d, 9, 19, 9, 3, body_color)
    px(d, 9, 21, 9, 1, body_dark)
    # Mud flaps
    px(d, 56, 21, 2, 2, RUBBER_TRIM)
    px(d, 8, 21, 2, 2, RUBBER_TRIM)

    # Licence plate
    px(d, 59, 20, 3, 2, (0xF0, 0xEC, 0xE0, 255))


def draw_taxi(d):
    """Draw a Belgian taxi (white body, blue stripes)."""
    body_color = WHITE_C
    body_dark  = (0xC8, 0xC4, 0xBC, 255)
    body_light = (0xFF, 0xFF, 0xFF, 255)

    # Shadow
    draw_shadow(d, 4, 22, 54, 3)

    # Underbody
    px(d, 4, 22, 54, 2, UNDERBODY)

    # Main body
    px(d, 4, 14, 54, 8, body_color)
    px(d, 50, 14, 8, 8, body_dark)
    px(d, 4, 14, 3, 8, body_light)

    # BLUE TAXI STRIPES (horizontal stripes along door panels)
    px(d, 4, 16, 54, 2, TAXI_BLUE)
    px(d, 4, 16, 3, 2, TAXI_BLUE_L)
    px(d, 51, 16, 7, 2, TAXI_BLUE_D)

    # Roof (sedan-style)
    px(d, 10, 8, 38, 6, body_color)
    px(d, 10, 8, 20, 1, body_light)
    px(d, 40, 8, 8, 6, body_dark)
    px(d, 10, 8, 3, 6, body_light)

    # TAXI SIGN on roof
    px(d, 22, 6, 10, 2, TAXI_BLUE)
    px(d, 23, 6, 8, 1, TAXI_BLUE_L)
    px(d, 23, 7, 2, 1, (0xF0, 0xEC, 0xE0, 255))  # TAXI text approx

    # Windscreen
    px(d, 40, 8, 10, 6, GLASS_D)
    px(d, 40, 8, 5, 2, GLASS_GLINT)
    px(d, 45, 10, 3, 2, GLASS_L)

    # Side windows
    px(d, 20, 8, 10, 6, GLASS_D)
    px(d, 20, 8, 4, 2, GLASS_GLINT)
    px(d, 11, 8, 8, 6, GLASS_D)
    px(d, 11, 8, 3, 2, GLASS_GLINT)

    # B-pillar, C-pillar
    px(d, 30, 8, 2, 6, body_color)
    px(d, 10, 8, 1, 6, body_color)

    # Door lines
    px(d, 19, 14, 1, 8, body_dark)
    px(d, 30, 14, 1, 8, body_dark)
    px(d, 39, 14, 1, 8, body_dark)

    # Door handles
    px(d, 22, 18, 3, 1, CHROME)
    px(d, 33, 18, 3, 1, CHROME)

    # Blue stripe also on door bottoms
    px(d, 5, 19, 53, 2, TAXI_BLUE_D)

    # Front bumper
    px(d, 51, 15, 7, 6, body_dark)
    # Grille
    px(d, 52, 17, 6, 3, DARK_METAL)
    # Headlights
    px(d, 54, 15, 3, 2, HEADLIGHT)
    px(d, 54, 15, 1, 1, (0xFF, 0xFF, 0xE8, 255))

    # Rear
    px(d, 4, 15, 5, 6, body_dark)
    px(d, 4, 14, 4, 3, TAILLIGHT)
    px(d, 5, 14, 2, 1, TAILLIGHT_L)

    # Wheels
    draw_wheel(d, 48, 21, is_front=True)
    px(d, 46, 20, 4, 1, TYRE)
    px(d, 47, 20, 2, 1, WHEEL_RIM)
    draw_wheel(d, 13, 21, is_front=False)
    px(d, 11, 20, 4, 1, TYRE)
    px(d, 12, 20, 2, 1, WHEEL_RIM)

    # Wheel arches
    px(d, 44, 20, 8, 2, body_color)
    px(d, 44, 21, 8, 1, body_dark)
    px(d, 9, 20, 8, 2, body_color)
    px(d, 9, 21, 8, 1, body_dark)

    # Licence plate
    px(d, 57, 19, 2, 2, (0xF0, 0xEC, 0xE0, 255))


def draw_delijn_bus(d):
    """Draw a De Lijn bus (dark blue body, yellow stripe, long)."""
    body_color = DELIJN_BL
    body_light = DELIJN_BL_L
    body_dark  = DELIJN_BL_D

    # Shadow (long bus shadow)
    draw_shadow(d, 1, 22, 62, 4)

    # Underbody
    px(d, 1, 22, 62, 2, UNDERBODY)

    # Main body (tall, long bus)
    px(d, 1, 8, 62, 14, body_color)
    # Body right shadow
    px(d, 57, 8, 6, 14, body_dark)
    # Body left highlight
    px(d, 1, 8, 3, 14, body_light)
    # Body top edge highlight
    px(d, 2, 8, 58, 1, body_light)

    # Roof (flat bus roof, with equipment)
    px(d, 1, 5, 62, 3, body_color)
    px(d, 2, 5, 40, 1, body_light)
    px(d, 52, 5, 10, 3, body_dark)
    # Roof ventilation / AC unit
    px(d, 30, 5, 8, 2, DARK_METAL)
    px(d, 30, 5, 8, 1, DARK_METAL_L)
    # Destination display box
    px(d, 42, 5, 12, 3, DARK_METAL)
    px(d, 43, 6, 10, 1, (0xF0, 0xD0, 0x00, 255))  # amber destination display

    # DE LIJN YELLOW STRIPE (horizontal, mid-body)
    px(d, 1, 16, 62, 3, DELIJN_YL)
    px(d, 1, 16, 3, 3, DELIJN_YL_L)  # left highlight
    px(d, 58, 16, 5, 3, (0xAA, 0x8C, 0x00, 255))  # right shadow

    # Large windows (side windows, many)
    for wx in range(4, 50, 8):
        px(d, wx, 9, 6, 6, GLASS_D)
        px(d, wx, 9, 3, 2, GLASS_GLINT)

    # Front windscreen (large, bus front)
    px(d, 52, 8, 10, 7, GLASS_D)
    px(d, 52, 8, 5, 3, GLASS_GLINT)
    px(d, 57, 10, 3, 2, GLASS_L)

    # Front door (right side, wide)
    px(d, 50, 8, 3, 13, body_dark)
    # Door glass
    px(d, 50, 9, 3, 6, GLASS_D)
    px(d, 50, 9, 2, 2, GLASS_GLINT)
    # Door frame
    px(d, 50, 15, 3, 1, body_light)

    # Rear door (middle)
    px(d, 28, 8, 3, 13, body_dark)
    px(d, 28, 9, 3, 6, GLASS_D)
    px(d, 28, 9, 2, 2, GLASS_GLINT)

    # DE LIJN logo area (front, top right)
    px(d, 54, 8, 5, 2, DELIJN_YL)
    px(d, 55, 8, 3, 1, (0xFF, 0xCC, 0x00, 255))

    # Number / route display (front)
    px(d, 54, 19, 6, 2, DARK_METAL)
    px(d, 55, 19, 4, 1, (0xF0, 0xD0, 0x00, 255))

    # Headlights (front, large)
    px(d, 59, 9, 3, 3, HEADLIGHT)
    px(d, 59, 9, 2, 1, (0xFF, 0xFF, 0xE8, 255))
    # DRL strip
    px(d, 52, 8, 10, 1, (0xF0, 0xE8, 0xC0, 255))

    # Rear of bus (left)
    px(d, 1, 8, 3, 13, body_dark)
    # Rear window
    px(d, 2, 9, 6, 6, GLASS_D)
    px(d, 2, 9, 3, 2, GLASS_GLINT)
    # Taillights (long strip)
    px(d, 1, 8, 2, 4, TAILLIGHT)
    px(d, 2, 8, 1, 2, TAILLIGHT_L)

    # Undercarriage / skirt panels
    px(d, 2, 20, 60, 2, body_dark)

    # Wheels (large bus wheels, double rear)
    draw_wheel(d, 56, 22, is_front=True)
    px(d, 53, 21, 5, 1, TYRE)
    px(d, 54, 21, 3, 1, WHEEL_RIM)
    # Double rear wheels
    draw_wheel(d, 18, 22, is_front=False)
    px(d, 15, 21, 5, 1, TYRE)
    px(d, 16, 21, 3, 1, WHEEL_RIM)
    draw_wheel(d, 24, 22, is_front=False)
    px(d, 21, 21, 5, 1, TYRE)
    px(d, 22, 21, 3, 1, WHEEL_RIM)

    # Wheel arches
    px(d, 52, 21, 9, 2, body_color)
    px(d, 52, 22, 9, 1, body_dark)
    px(d, 14, 21, 14, 2, body_color)
    px(d, 14, 22, 14, 1, body_dark)

    # Licence plate / bus number (front bottom)
    px(d, 61, 21, 2, 2, (0xF0, 0xEC, 0xE0, 255))


def draw_scooter(d):
    """Draw a small red moped/scooter (narrow, viewed from slightly above)."""
    # Scooter occupies roughly x=20..44 (24px wide), y=6..26
    body_color = SCOOTER_R
    body_light = SCOOTER_R_L
    body_dark  = SCOOTER_R_D

    # Shadow (small)
    draw_shadow(d, 22, 24, 22, 2)

    # REAR WHEEL (left/rear)
    draw_wheel(d, 26, 22, is_front=False)
    px(d, 24, 21, 4, 1, TYRE)
    px(d, 25, 21, 2, 1, WHEEL_RIM)

    # FRONT WHEEL (right/front)
    draw_wheel(d, 38, 22, is_front=True)
    px(d, 36, 21, 4, 1, TYRE)
    px(d, 37, 21, 2, 1, WHEEL_RIM)

    # Swingarm / chain guard (connecting rear wheel to body)
    px(d, 26, 20, 6, 1, DARK_METAL)

    # Main body / step-through frame
    px(d, 24, 14, 18, 7, body_color)
    # Body right shadow
    px(d, 38, 14, 4, 7, body_dark)
    # Body left highlight
    px(d, 24, 14, 2, 7, body_light)
    # Body top edge
    px(d, 24, 14, 18, 1, body_light)

    # Engine/underseat storage (lower front)
    px(d, 31, 18, 10, 4, body_dark)
    px(d, 31, 18, 4, 1, body_color)

    # SEAT (top, darker, padded look)
    px(d, 26, 11, 12, 4, (0x20, 0x1C, 0x18, 255))
    px(d, 26, 11, 6, 1, (0x38, 0x34, 0x30, 255))  # seat highlight
    # Seat contour
    px(d, 25, 12, 1, 2, (0x18, 0x14, 0x10, 255))
    px(d, 38, 12, 1, 2, (0x18, 0x14, 0x10, 255))

    # HANDLEBARS (front right, across the top)
    px(d, 36, 10, 6, 1, DARK_METAL)
    px(d, 38, 9, 2, 2, DARK_METAL)
    # Handlebar grips
    px(d, 36, 10, 2, 1, RUBBER_TRIM)
    px(d, 42, 10, 2, 1, RUBBER_TRIM)
    # Mirror (small rectangular)
    px(d, 42, 9, 2, 1, GLASS_L)

    # Headlight (front)
    px(d, 41, 13, 3, 3, HEADLIGHT)
    px(d, 41, 13, 2, 1, (0xFF, 0xFF, 0xE8, 255))
    # Headlight housing
    px(d, 40, 12, 4, 4, body_dark)
    px(d, 41, 13, 3, 3, HEADLIGHT)

    # Front fork / suspension
    px(d, 39, 17, 2, 5, DARK_METAL)
    px(d, 39, 17, 1, 5, DARK_METAL_L)

    # Rear light (left/rear)
    px(d, 23, 14, 2, 2, TAILLIGHT)
    px(d, 23, 14, 1, 1, TAILLIGHT_L)

    # Exhaust pipe (underside)
    px(d, 25, 22, 8, 1, DARK_METAL)
    px(d, 32, 22, 4, 1, DARK_METAL_L)  # exhaust heat shield

    # Leg shield / front body panel
    px(d, 36, 15, 5, 4, body_color)
    px(d, 40, 15, 1, 4, body_dark)

    # Scooter badge / detail
    px(d, 29, 15, 3, 2, body_dark)
    px(d, 30, 15, 1, 1, CHROME)

    # Footrest
    px(d, 24, 21, 3, 1, DARK_METAL)
    px(d, 38, 21, 3, 1, DARK_METAL)

    # Wheel arch (rear)
    px(d, 23, 20, 7, 2, body_color)
    px(d, 23, 21, 7, 1, body_dark)
    # Wheel arch (front)
    px(d, 35, 20, 7, 2, body_color)
    px(d, 35, 21, 7, 1, body_dark)

    # Licence plate (small, rear)
    px(d, 23, 19, 3, 2, (0xF0, 0xEC, 0xE0, 255))
    px(d, 24, 19, 2, 1, (0x80, 0x80, 0x80, 255))


# ── Vehicle registry ──────────────────────────────────────────────────────────
def draw_vehicle_0(d):
    draw_clio(d, BLUE_CAR, BLUE_CAR_L, BLUE_CAR_D, "clio_blue")

def draw_vehicle_1(d):
    draw_clio(d, RED_CAR, RED_CAR_L, RED_CAR_D, "clio_red")


VEHICLES = [
    ("clio_blue",     draw_vehicle_0),
    ("clio_red",      draw_vehicle_1),
    ("kangoo_white",  draw_kangoo),
    ("suv_silver",    draw_suv),
    ("taxi_bluewhite",draw_taxi),
    ("bus_delijn",    draw_delijn_bus),
    ("scooter",       draw_scooter),
]


def main():
    os.makedirs(BASE_DIR, exist_ok=True)

    sheet_w = FW * NUM_VEHICLES  # 2240
    sheet = Image.new('RGBA', (sheet_w, FH), (0, 0, 0, 0))

    print("=" * 60)
    print("Turnhoutsebaan Vehicle Sprite Generator")
    print(f"  Frame: {GW}x{GH} game px | SCALE={SCALE} | {FW}x{FH} px per frame")
    print(f"  Sheet: {sheet_w}x{FH} px")
    print("=" * 60)

    for i, (name, draw_fn) in enumerate(VEHICLES):
        frame_img = make_frame()
        d = ImageDraw.Draw(frame_img)
        draw_fn(d)

        vehicle_path = os.path.join(BASE_DIR, f"vehicle_{i}_{name}.png")
        frame_img.save(vehicle_path)
        sheet.paste(frame_img, (i * FW, 0))
        print(f"  [{i}] {name}")

    sheet_path = os.path.join(BASE_DIR, "vehicles_sheet.png")
    sheet.save(sheet_path)
    print(f"\n✓ vehicles_sheet.png ({sheet_w}x{FH} px)")
    print(f"  → {sheet_path}")


if __name__ == '__main__':
    main()
