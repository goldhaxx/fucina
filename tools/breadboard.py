#!/usr/bin/env python3
"""Generate SVG breadboard wiring diagrams from YAML circuit descriptions.

Usage:
    python3 tools/breadboard.py sketches/001-blink/wiring.yaml -o sketches/001-blink/wiring.svg
    python3 tools/breadboard.py sketches/001-blink/wiring.yaml --rows 1-20 -o out.svg
"""

import argparse
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

try:
    import yaml
except ImportError:
    yaml = None

# ─── Layout Constants (pixels) ───────────────────────────────────

HOLE_RADIUS = 3.0
HOLE_PITCH = 14
CENTER_GAP = 28
POWER_GAP = 20
RAIL_GAP = 10

MARGIN_TOP = 52
MARGIN_BOTTOM = 16
MARGIN_LEFT = 80
MARGIN_RIGHT = 80

BOARD_PAD_X = 12
BOARD_PAD_Y = 12

TERMINAL_ROWS = 63

# Power rail holes are aligned to terminal rows in groups of 5, with a 1-row gap.
# 10 groups: [3-7], [9-13], [15-19], [21-25], [27-31], [33-37], [39-43], [45-49], [51-55], [57-61]
POWER_RAIL_ROWS: list[int] = []
_r = 3
while _r <= 61:
    for _i in range(5):
        if _r + _i <= 61:
            POWER_RAIL_ROWS.append(_r + _i)
    _r += 6

# Colors
BOARD_FILL = "#e8dcc8"
BOARD_STROKE = "#b8a88a"
HOLE_COLOR = "#2a2a2a"
HOLE_OCCUPIED_COLOR = "#666"
RAIL_RED = "#d32f2f"
RAIL_BLUE = "#1565c0"
CENTER_CHANNEL = "#d4c8b0"
LABEL_COLOR = "#666"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"
FONT_MONO = "'SF Mono', 'Cascadia Code', 'Fira Code', monospace"

# Orientation presets — maps named orientations to rotation degrees.
# The orientation describes which direction the component's natural "top"
# faces when placed on the breadboard.
#   up    → 0°    (natural top faces toward row 1)
#   right → 90°   (natural top faces toward column j)
#   down  → 180°  (natural top faces toward row 63)
#   left  → -90°  (natural top faces toward column a)
ORIENTATION_PRESETS = {
    "up": 0,
    "right": 90,
    "down": 180,
    "left": -90,
}

# Default orientation per component type. Only types that use orientation
# are listed here — most components are symmetric or position-derived.
ORIENTATION_DEFAULTS = {
    "seven_segment": "left",
}


def parse_orientation(comp: dict) -> int:
    """Return the rotation angle (degrees) for a component's orientation.

    Reads the optional 'orientation' key from the component dict.
    Falls back to the type-specific default from ORIENTATION_DEFAULTS,
    or 0 (upright / no rotation) if no default exists.
    """
    raw = comp.get("orientation", ORIENTATION_DEFAULTS.get(comp.get("type", ""), "up"))
    if isinstance(raw, (int, float)):
        return int(raw)
    return ORIENTATION_PRESETS.get(str(raw).lower(), 0)


def compute_rotated_fit(natural_w: float, natural_h: float,
                        container_w: float, container_h: float,
                        rotation_deg: float, fill: float = 0.90) -> float:
    """Compute the max scale factor for a natural-size rect to fit inside
    a container after rotation.

    The natural rect (natural_w × natural_h) is rotated by rotation_deg
    around its center. The rotated bounding box must fit within
    container_w × container_h, scaled by `fill` (0.0–1.0) to leave padding.

    Returns the scale factor s such that (natural_w * s, natural_h * s)
    rotated by rotation_deg fits within (container_w * fill, container_h * fill).
    """
    rad = math.radians(rotation_deg)
    cos_a = abs(math.cos(rad))
    sin_a = abs(math.sin(rad))

    # Rotated bounding box dimensions (at scale 1)
    rot_w = natural_w * cos_a + natural_h * sin_a
    rot_h = natural_w * sin_a + natural_h * cos_a

    if rot_w == 0 or rot_h == 0:
        return 1.0

    target_w = container_w * fill
    target_h = container_h * fill

    return min(target_w / rot_w, target_h / rot_h)


# Resistor band colors
BAND_DIGIT = {
    0: "#000", 1: "#8B4513", 2: "#FF0000", 3: "#FF8C00",
    4: "#FFD700", 5: "#228B22", 6: "#0000FF", 7: "#8B00FF",
    8: "#808080", 9: "#FFF",
}
BAND_MULTIPLIER = {
    1: "#000", 10: "#8B4513", 100: "#FF0000",
    1000: "#FF8C00", 10000: "#FFD700", 100000: "#228B22",
    1000000: "#0000FF",
}
BAND_TOLERANCE_GOLD = "#CFB53B"

LED_PALETTE = {
    "red": ("#ff1744", "#ff8a80"),
    "green": ("#00c853", "#69f0ae"),
    "yellow": ("#ffd600", "#fff59d"),
    "blue": ("#2979ff", "#82b1ff"),
    "white": ("#f5f5f5", "#e0e0e0"),
    "orange": ("#ff6d00", "#ffab91"),
}


# ─── YAML Loading ────────────────────────────────────────────────

def load_circuit(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return _parse_yaml_simple(text)


def _parse_yaml_simple(text: str) -> dict:
    result = {}
    current_list = None
    current_item = None

    for raw_line in text.splitlines():
        stripped = raw_line.split("#")[0].rstrip()
        if not stripped:
            continue
        indent = len(raw_line) - len(raw_line.lstrip())

        if indent == 0 and ":" in stripped:
            if current_list is not None and current_item is not None:
                current_list.append(current_item)
                current_item = None
            key, val = stripped.split(":", 1)
            val = val.strip().strip('"').strip("'")
            if not val:
                result[key.strip()] = []
                current_list = result[key.strip()]
            else:
                result[key.strip()] = _coerce(val)
                current_list = None
        elif stripped.lstrip().startswith("- "):
            if current_list is not None and current_item is not None:
                current_list.append(current_item)
            current_item = {}
            pair = stripped.lstrip()[2:]
            if ":" in pair:
                k, v = pair.split(":", 1)
                current_item[k.strip()] = _coerce(v.strip().strip('"').strip("'"))
        elif ":" in stripped and current_item is not None:
            k, v = stripped.strip().split(":", 1)
            current_item[k.strip()] = _coerce(v.strip().strip('"').strip("'"))

    if current_list is not None and current_item is not None:
        current_list.append(current_item)
    return result


def _coerce(val: str):
    if not val:
        return ""
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


# ─── Row Range Detection ─────────────────────────────────────────

def _extract_row(hole_id: str) -> int | None:
    """Extract terminal row number from any hole address.

    Handles terminal strips ('d7' → 7) and power rails ('+L3' → row 5)
    by mapping rail indices back to their aligned terminal rows.
    The L/R side letter selects the physical rail but doesn't affect the row.
    Board pins ('pin9', 'gnd') return None — they have no breadboard row.
    """
    hole_id = hole_id.strip()

    # Terminal strip: a1–j63
    m = re.match(r'^[a-jA-J](\d+)$', hole_id)
    if m:
        return int(m.group(1))

    # Power rail: +L1, -L1, +R1, -R1, +1, -1
    m = re.match(r'^[+-][LR]?(\d+)$', hole_id)
    if m:
        idx = int(m.group(1))
        if 1 <= idx <= len(POWER_RAIL_ROWS):
            return POWER_RAIL_ROWS[idx - 1]

    return None


def detect_row_range(circuit: dict, padding: int = 3) -> tuple[int, int]:
    """Scan circuit to find min/max rows used, with padding."""
    rows_used = set()

    for comp in circuit.get("components", []):
        for key in ("from", "to", "anode", "cathode", "positive", "negative",
                    "pin1", "pin2", "pin3", "red", "common", "green", "blue"):
            if key in comp:
                r = _extract_row(str(comp[key]))
                if r:
                    rows_used.add(r)
        # seven_segment uses row_start + pins to span multiple rows
        if comp.get("type") == "seven_segment":
            rs = int(comp.get("row_start", 0))
            np = int(comp.get("pins", 10)) // 2
            if rs:
                for i in range(np):
                    rows_used.add(rs + i)
        # module uses pins list
        pins_val = comp.get("pins", [])
        if isinstance(pins_val, list):
            for pin in pins_val:
                if isinstance(pin, dict) and "hole" in pin:
                    r = _extract_row(str(pin["hole"]))
                    if r:
                        rows_used.add(r)

    for wire in circuit.get("wires", []):
        for key in ("from", "to"):
            r = _extract_row(str(wire[key]))
            if r:
                rows_used.add(r)

    if not rows_used:
        return 1, TERMINAL_ROWS

    lo = max(1, min(rows_used) - padding)
    hi = min(TERMINAL_ROWS, max(rows_used) + padding)
    return lo, hi


# ─── Coordinate System ───────────────────────────────────────────

class Board:
    """Maps breadboard hole addresses to pixel coordinates.

    Supports rendering a subset of rows (row_lo to row_hi) for focused diagrams.
    """

    def __init__(self, row_lo: int = 1, row_hi: int = TERMINAL_ROWS):
        self.row_lo = row_lo
        self.row_hi = row_hi
        self.visible_rows = row_hi - row_lo + 1
        self._col_x: dict[str, float] = {}
        self._setup_columns()
        self.occupied: set[str] = set()

    def _setup_columns(self):
        x = MARGIN_LEFT
        self._col_x["+L"] = x
        x += RAIL_GAP
        self._col_x["-L"] = x
        x += POWER_GAP
        for col in "abcde":
            self._col_x[col] = x
            x += HOLE_PITCH
        x = self._col_x["e"] + CENTER_GAP
        for col in "fghij":
            self._col_x[col] = x
            x += HOLE_PITCH
        x = self._col_x["j"] + POWER_GAP
        self._col_x["+R"] = x
        x += RAIL_GAP
        self._col_x["-R"] = x

    def hole_xy(self, hole_id: str) -> tuple[float, float]:
        hole_id = hole_id.strip()

        if hole_id[0] in "+-":
            sign = hole_id[0]
            rest = hole_id[1:]
            if rest and rest[0] in "LR":
                side, idx = rest[0], int(rest[1:])
            else:
                side, idx = "L", int(rest)
            # idx is 1-based into POWER_RAIL_ROWS
            if idx < 1 or idx > len(POWER_RAIL_ROWS):
                raise ValueError(f"Power rail index {idx} out of range 1–{len(POWER_RAIL_ROWS)}")
            terminal_row = POWER_RAIL_ROWS[idx - 1]
            return self._col_x[f"{sign}{side}"], self._power_row_y(terminal_row)

        col = hole_id[0].lower()
        row = int(hole_id[1:])
        return self._col_x[col], self._terminal_row_y(row)

    def _terminal_row_y(self, row: int) -> float:
        return MARGIN_TOP + (row - self.row_lo) * HOLE_PITCH

    def _power_row_y(self, terminal_row: int) -> float:
        """Power rail holes sit at the same y as their aligned terminal row."""
        return self._terminal_row_y(terminal_row)

    def _power_rows_in_view(self) -> list[int]:
        """Return the terminal row numbers of power rail holes within the visible range."""
        return [r for r in POWER_RAIL_ROWS if self.row_lo <= r <= self.row_hi]

    @property
    def board_left(self) -> float:
        return self._col_x["+L"] - BOARD_PAD_X

    @property
    def board_right(self) -> float:
        return self._col_x["-R"] + BOARD_PAD_X

    @property
    def board_top(self) -> float:
        return MARGIN_TOP - BOARD_PAD_Y

    @property
    def board_bottom(self) -> float:
        return MARGIN_TOP + (self.visible_rows - 1) * HOLE_PITCH + BOARD_PAD_Y

    @property
    def svg_width(self) -> float:
        return self.board_right + MARGIN_RIGHT

    @property
    def svg_height(self) -> float:
        return self.board_bottom + MARGIN_BOTTOM

    def mark_occupied(self, *holes: str):
        for h in holes:
            self.occupied.add(h.strip().lower())

    def is_occupied(self, hole_id: str) -> bool:
        return hole_id.strip().lower() in self.occupied


# ─── SVG Helpers ─────────────────────────────────────────────────

def _attr(**kw) -> str:
    return " ".join(
        f'{k.replace("_", "-")}="{escape(str(v))}"'
        for k, v in kw.items() if v is not None
    )


def _circle(cx, cy, r, **kw) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {_attr(**kw)}/>'


def _rect(x, y, w, h, **kw) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {_attr(**kw)}/>'


def _line(x1, y1, x2, y2, **kw) -> str:
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {_attr(**kw)}/>'


def _text(x, y, content, **kw) -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" {_attr(**kw)}>{escape(str(content))}</text>'


# ─── Resistor Bands ──────────────────────────────────────────────

def resistor_bands(ohms: int) -> list[str]:
    if ohms <= 0:
        return ["#000"] * 4
    sig, mult = ohms, 1
    while sig >= 100:
        sig //= 10
        mult *= 10
    return [
        BAND_DIGIT.get(sig // 10, "#000"),
        BAND_DIGIT.get(sig % 10, "#000"),
        BAND_MULTIPLIER.get(mult, "#000"),
        BAND_TOLERANCE_GOLD,
    ]


# ─── Component Renderers ─────────────────────────────────────────

def render_resistor(board: Board, comp: dict) -> list[str]:
    x1, y1 = board.hole_xy(comp["from"])
    x2, y2 = board.hole_xy(comp["to"])
    board.mark_occupied(comp["from"], comp["to"])

    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return []

    ux, uy = dx / length, dy / length
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    body_len = min(length * 0.55, 36)
    bh = body_len / 2
    angle = math.degrees(math.atan2(dy, dx))
    body_h = 9

    els = []
    # Lead wires
    els.append(_line(x1, y1, mid_x - ux * bh, mid_y - uy * bh,
                     stroke="#999", stroke_width="1.5"))
    els.append(_line(mid_x + ux * bh, mid_y + uy * bh, x2, y2,
                     stroke="#999", stroke_width="1.5"))

    # Body
    els.append(
        f'<rect x="{-body_len/2:.1f}" y="{-body_h/2:.1f}" '
        f'width="{body_len:.1f}" height="{body_h:.1f}" rx="2.5" '
        f'fill="#c8aa78" stroke="#9a7e50" stroke-width="0.8" '
        f'transform="translate({mid_x:.1f},{mid_y:.1f}) rotate({angle:.1f})"/>'
    )

    # Color bands
    bands = resistor_bands(comp.get("value", 0))
    spacing = body_len / (len(bands) + 1)
    for i, color in enumerate(bands):
        bx = -body_len / 2 + spacing * (i + 1)
        els.append(
            f'<rect x="{bx - 1.3:.1f}" y="{-body_h/2 + 1:.1f}" '
            f'width="2.6" height="{body_h - 2:.1f}" rx="0.3" '
            f'fill="{color}" '
            f'transform="translate({mid_x:.1f},{mid_y:.1f}) rotate({angle:.1f})"/>'
        )

    return els


def render_led(board: Board, comp: dict) -> list[str]:
    ax, ay = board.hole_xy(comp["anode"])
    cx, cy = board.hole_xy(comp["cathode"])
    board.mark_occupied(comp["anode"], comp["cathode"])

    color = comp.get("color", "red")
    fill, glow = LED_PALETTE.get(color, LED_PALETTE["red"])

    dx, dy = cx - ax, cy - ay
    length = math.hypot(dx, dy)
    if length == 0:
        return []

    ux, uy = dx / length, dy / length
    mx, my = (ax + cx) / 2, (ay + cy) / 2
    perp_x, perp_y = -uy, ux

    els = []
    # Glow
    els.append(_circle(mx, my, 9, fill=glow, opacity="0.25"))
    # Body
    els.append(_circle(mx, my, 5.5, fill=fill, stroke="#888", stroke_width="0.6", opacity="0.92"))
    # Inner highlight
    els.append(_circle(mx - 1.5, my - 1.5, 2, fill="white", opacity="0.25"))
    # Cathode bar
    bar_x = mx + ux * 5
    bar_y = my + uy * 5
    els.append(_line(bar_x - perp_x * 5, bar_y - perp_y * 5,
                     bar_x + perp_x * 5, bar_y + perp_y * 5,
                     stroke="#666", stroke_width="1.8"))
    # Anode label
    els.append(_text(ax - ux * 7 - 3, ay - uy * 7 + 3, "+",
                     font_size="8", fill=fill, font_weight="bold", font_family=FONT))
    # Leads
    els.append(_line(ax, ay, mx - ux * 5.5, my - uy * 5.5,
                     stroke="#999", stroke_width="1.2"))
    els.append(_line(mx + ux * 5.5, my + uy * 5.5, cx, cy,
                     stroke="#999", stroke_width="1.2"))

    return els


BUZZER_PALETTE = {
    "active": ("#333", "#555"),
    "passive": ("#555", "#777"),
}


def render_button(board: Board, comp: dict) -> list[str]:
    """Render a push button spanning two rows across the center channel."""
    pin1 = str(comp["from"])
    pin2 = str(comp["to"])
    x1, y1 = board.hole_xy(pin1)
    x2, y2 = board.hole_xy(pin2)
    board.mark_occupied(pin1, pin2)

    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    els = []

    # Body (dark rectangle)
    els.append(_rect(mx - 8, my - 8, 16, 16, rx="2",
                     fill="#444", stroke="#222", stroke_width="0.8"))
    # Button cap (lighter circle)
    els.append(_circle(mx, my, 5, fill="#888", stroke="#666", stroke_width="0.6"))
    # Lead wires
    els.append(_line(x1, y1, mx, my, stroke="#999", stroke_width="1.2"))
    els.append(_line(mx, my, x2, y2, stroke="#999", stroke_width="1.2"))

    return els


def render_buzzer(board: Board, comp: dict) -> list[str]:
    """Render a buzzer (active or passive) as a cylinder viewed from above."""
    pin_pos = str(comp.get("positive", comp.get("from", "")))
    pin_neg = str(comp.get("negative", comp.get("to", "")))
    x1, y1 = board.hole_xy(pin_pos)
    x2, y2 = board.hole_xy(pin_neg)
    board.mark_occupied(pin_pos, pin_neg)

    variant = comp.get("variant", "active")
    fill, stroke = BUZZER_PALETTE.get(variant, BUZZER_PALETTE["active"])

    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    els = []

    # Body circle
    els.append(_circle(mx, my, 8, fill=fill, stroke=stroke, stroke_width="0.8"))
    # Plus marking
    els.append(_text(mx - 3, my - 3, "+", font_size="7", fill="#aaa",
                     font_weight="bold", font_family=FONT))
    # Sound waves (decorative)
    els.append(f'<path d="M {mx+5:.1f} {my-3:.1f} q 3 3 0 6" '
               f'fill="none" stroke="#aaa" stroke-width="0.6" opacity="0.5"/>')
    # Lead wires
    els.append(_line(x1, y1, mx - 4, my, stroke="#999", stroke_width="1.2"))
    els.append(_line(mx + 4, my, x2, y2, stroke="#999", stroke_width="1.2"))

    return els


def render_sensor(board: Board, comp: dict) -> list[str]:
    """Render a generic 3-pin sensor module as a small PCB rectangle."""
    pins = []
    for key in ("pin1", "pin2", "pin3", "from", "to"):
        if key in comp:
            pins.append(str(comp[key]))
    if len(pins) < 2:
        return []

    coords = [board.hole_xy(p) for p in pins]
    for p in pins:
        board.mark_occupied(p)

    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)

    pad = 6
    x_min, x_max = min(xs) - pad, max(xs) + pad
    y_min, y_max = min(ys) - pad, max(ys) + pad
    w = max(x_max - x_min, 18)
    h = max(y_max - y_min, 18)

    label = comp.get("label", comp.get("name", ""))

    els = []
    # PCB body
    els.append(_rect(cx - w / 2, cy - h / 2, w, h, rx="2",
                     fill="#1a6b3c", stroke="#0d4025", stroke_width="0.8"))
    # Module label
    if label:
        els.append(_text(cx, cy + 3, label, font_size="6", fill="#cfc",
                         text_anchor="middle", font_family=FONT_MONO))
    # Pin dots
    for x, y in coords:
        els.append(_circle(x, y, 1.5, fill="#silver", stroke="#999", stroke_width="0.3"))

    return els


def render_potentiometer(board: Board, comp: dict) -> list[str]:
    """Render a potentiometer as a circular knob with 3 pins."""
    pins = []
    for key in ("pin1", "pin2", "pin3"):
        if key in comp:
            pins.append(str(comp[key]))
    if len(pins) < 3:
        return []

    coords = [board.hole_xy(p) for p in pins]
    for p in pins:
        board.mark_occupied(p)

    # Center on the middle pin
    cx, cy = coords[1]
    radius = 10

    els = []
    # Body (dark circle)
    els.append(_circle(cx, cy, radius, fill="#555", stroke="#333", stroke_width="1"))
    # Knob indicator (white line from center to edge)
    els.append(_line(cx, cy, cx, cy - radius + 2,
                     stroke="#ccc", stroke_width="1.5", stroke_linecap="round"))
    # Knob center dot
    els.append(_circle(cx, cy, 2.5, fill="#888", stroke="#666", stroke_width="0.5"))
    # Lead wires to pins
    for x, y in coords:
        els.append(_line(x, y, cx, cy + radius,
                         stroke="#999", stroke_width="1.2"))

    return els


def render_rgb_led(board: Board, comp: dict) -> list[str]:
    """Render a 4-pin common-cathode RGB LED."""
    pin_keys = ("red", "common", "green", "blue")
    pins = {}
    for key in pin_keys:
        if key in comp:
            pins[key] = str(comp[key])
    if len(pins) < 4:
        return []

    coords = {k: board.hole_xy(v) for k, v in pins.items()}
    for v in pins.values():
        board.mark_occupied(v)

    # Center on the common pin
    cx, cy = coords["common"]

    els = []
    # Outer glow
    els.append(_circle(cx, cy, 9, fill="#fff", opacity="0.15"))
    # Main body (frosted clear)
    els.append(_circle(cx, cy, 6.5, fill="#e8e8e8", stroke="#999", stroke_width="0.6"))
    # Color channel dots arranged around the lens
    color_map = {"red": "#ff1744", "green": "#00c853", "blue": "#2979ff"}
    offsets = {"red": (-3.5, -2), "green": (0, 3.5), "blue": (3.5, -2)}
    for channel, color in color_map.items():
        ox, oy = offsets[channel]
        els.append(_circle(cx + ox, cy + oy, 2, fill=color, opacity="0.8"))

    # Cathode bar (on the common pin side)
    rx, ry = coords["common"]
    els.append(_text(rx - 3, ry + 12, "GND", font_size="5", fill="#999",
                     font_family=FONT_MONO))

    # Lead wires
    for key, (x, y) in coords.items():
        els.append(_line(x, y, cx, cy, stroke="#999", stroke_width="1"))

    return els


def _seven_segment_digit(digit_w: float, digit_h: float, sw: float,
                         seg_color: str = "#600", dp_color: str = "#600") -> list[str]:
    """Draw one 7-segment digit glyph centered at the origin in natural coords.

    Natural orientation: upright, segment A at top, DP at bottom-right.
    The caller wraps this in a <g transform="..."> for positioning and rotation.
    """
    hw = digit_w / 2
    hh = digit_h / 2
    els = []

    # 7 segments in natural upright orientation
    segs = [
        (-hw + 1, -hh, hw - 1, -hh),    # A — top
        (-hw + 1, 0, hw - 1, 0),         # G — middle
        (-hw + 1, hh, hw - 1, hh),       # D — bottom
        (-hw, -hh + 1, -hw, -1),          # F — upper-left
        (hw, -hh + 1, hw, -1),            # B — upper-right
        (-hw, 1, -hw, hh - 1),            # E — lower-left
        (hw, 1, hw, hh - 1),              # C — lower-right
    ]
    for sx1, sy1, sx2, sy2 in segs:
        els.append(_line(sx1, sy1, sx2, sy2,
                         stroke=seg_color, stroke_width=f"{sw:.1f}",
                         stroke_linecap="round"))

    # DP at bottom-right
    dp_r = max(0.8, min(digit_w * 0.10, 1.8))
    els.append(_circle(hw + digit_w * 0.20, hh, dp_r, fill=dp_color))

    return els


def render_seven_segment(board: Board, comp: dict) -> list[str]:
    """Render a 7-segment display as a DIP package.

    Proportions from 5161AS/5641AS datasheets:
    - Digit face: 8.1mm × 14.2mm (aspect 1.75:1, height/width)
    - 8° italic slant, DP at bottom-right of each digit
    - Package row spacing: 15.24mm (0.6") → columns e to i
    """
    digits = comp.get("digits", 1)
    row_start = int(comp.get("row_start", 10))
    num_pins = int(comp.get("pins", 10 if digits == 1 else 12))
    pins_per_side = num_pins // 2
    rotation = parse_orientation(comp)

    left_col = comp.get("left_col", "e")
    right_col = comp.get("right_col", "i")

    left_pins = []
    right_pins = []
    for i in range(pins_per_side):
        row = row_start + i
        left_pins.append(f"{left_col}{row}")
        right_pins.append(f"{right_col}{row}")
    all_pins = left_pins + right_pins

    for p in all_pins:
        board.mark_occupied(p)

    # Body rectangle from pin positions
    x_left, y_top = board.hole_xy(left_pins[0])
    x_right, _ = board.hole_xy(right_pins[0])
    _, y_bot = board.hole_xy(left_pins[-1])

    pad_x, pad_y = 6, 4
    body_x = x_left - pad_x
    body_y = y_top - pad_y
    body_w = (x_right - x_left) + pad_x * 2
    body_h = (y_bot - y_top) + pad_y * 2
    body_cx = body_x + body_w / 2
    body_cy = body_y + body_h / 2

    clip_id = f"seg-clip-{row_start}"

    els = []

    # IC body (black DIP package)
    els.append(_rect(body_x, body_y, body_w, body_h, rx="2",
                     fill="#1a1a1a", stroke="#444", stroke_width="0.8"))

    # Notch at top
    notch_cx = body_x + body_w / 2
    els.append(f'<path d="M {notch_cx - 4:.1f} {body_y:.1f} '
               f'a 4 4 0 0 1 8 0" fill="#333" stroke="none"/>')

    # Digit sizing — constrained by the display window and rotation.
    #
    # After rotate + skewX(-8):
    #   horizontal extent = digit_h  (tall dim fills body width)
    #   vertical extent   = digit_w + 0.14*digit_h + stroke  (fits cell)
    #
    # Datasheet: 14.2mm tall × 8.1mm wide → aspect 1.75:1
    skew_deg = 8
    aspect = 1.75   # digit_h / digit_w from datasheet
    k = 0.14        # tan(8°) skew factor
    inv_a = 1.0 / aspect
    vert_fill = 0.90

    win_inset = 6
    avail_w = body_w - win_inset * 2
    avail_h = body_h - win_inset * 2

    # Display window — full face area
    win_x = body_x + win_inset
    win_y = body_y + win_inset
    win_w = avail_w
    win_h = avail_h
    els.append(_rect(win_x, win_y, win_w, win_h, rx="1",
                     fill="#222", stroke="#333", stroke_width="0.4"))

    # ClipPath — structural containment to the display window
    els.append(f'<defs><clipPath id="{clip_id}">'
               f'<rect x="{win_x:.1f}" y="{win_y:.1f}" '
               f'width="{win_w:.1f}" height="{win_h:.1f}"/>'
               f'</clipPath></defs>')
    els.append(f'<g clip-path="url(#{clip_id})">')

    gap = max(2, avail_h * 0.04)
    cell_h = (avail_h - gap * (digits - 1)) / digits
    vert_budget = cell_h * vert_fill

    # Solve: digit_w + k*digit_h + sw ≤ vert_budget
    # where digit_w = digit_h / aspect, sw = min(digit_w * k, 3.0)
    # Two regimes: sw proportional (small digits) vs sw capped at 3 (large)
    coeff_prop = inv_a + k + k * inv_a   # ~0.791
    digit_h = min(vert_budget / coeff_prop, avail_w * vert_fill)
    digit_w = digit_h * inv_a
    sw = max(1.0, min(digit_w * k, 3.0))

    if digit_w * k > 3.0:
        # Stroke capped — recompute with fixed sw = 3.0
        coeff_cap = inv_a + k   # ~0.711
        digit_h = min((vert_budget - 3.0) / coeff_cap, avail_w * vert_fill)
        digit_w = digit_h * inv_a
        sw = 3.0

    total_h = digits * (cell_h + gap) - gap
    start_y = body_cy - total_h / 2

    for d in range(digits):
        cell_top = start_y + d * (cell_h + gap)
        digit_cy = cell_top + cell_h / 2

        # Digit drawn upright at origin, then rotated for board placement
        els.append(
            f'<g transform="translate({body_cx:.1f},{digit_cy:.1f}) '
            f'rotate({rotation}) skewX(-{skew_deg})">'
        )
        els.extend(_seven_segment_digit(digit_w, digit_h, sw))
        els.append('</g>')

    els.append('</g>')  # close clip group

    # Pin dots on both sides (outside clip group)
    for p in left_pins:
        x, y = board.hole_xy(p)
        els.append(_circle(x, y, 1.5, fill="#999", stroke="#777", stroke_width="0.3"))
    for p in right_pins:
        x, y = board.hole_xy(p)
        els.append(_circle(x, y, 1.5, fill="#999", stroke="#777", stroke_width="0.3"))

    return els


def render_module(board: Board, comp: dict) -> list[str]:
    """Render an off-board module as a labeled box at the left margin.

    The box is positioned at the average y-coordinate of its connected holes,
    with lead lines going to each hole.
    """
    name = comp.get("name", "Module")
    color = comp.get("color", "#37474f")
    pins_list = comp.get("pins", [])

    if not pins_list:
        return []

    # Collect hole coordinates
    hole_coords = []
    for pin in pins_list:
        hole = str(pin.get("hole", ""))
        if hole and not _is_board_pin(hole):
            board.mark_occupied(hole)
            hole_coords.append((board.hole_xy(hole), pin.get("label", "")))

    if not hole_coords:
        return []

    # Position the module box at the left margin
    avg_y = sum(c[0][1] for c in hole_coords) / len(hole_coords)
    box_h = max(len(hole_coords) * 12 + 8, 24)
    box_w = max(len(name) * 6 + 16, 60)
    box_x = 4
    box_y = avg_y - box_h / 2
    box_right = box_x + box_w

    els = []

    # Module box
    els.append(_rect(box_x, box_y, box_w, box_h, rx="4",
                     fill=color, stroke="#263238", stroke_width="0.8", opacity="0.92"))

    # Module name
    els.append(_text(box_x + box_w / 2, box_y + 11, name,
                     font_size="8", fill="white", font_weight="600",
                     text_anchor="middle", font_family=FONT))

    # Pin labels and lead lines
    for i, ((hx, hy), label) in enumerate(hole_coords):
        pin_y = box_y + 18 + i * 12
        if label:
            els.append(_text(box_x + 6, pin_y + 3, label,
                             font_size="6", fill="#ccc", font_family=FONT_MONO))
        # Lead line from box edge to hole
        els.append(_line(box_right, pin_y, hx, hy,
                         stroke=color, stroke_width="1.5",
                         stroke_linecap="round", opacity="0.5",
                         stroke_dasharray="3,3"))

    return els


def _is_board_pin(s: str) -> bool:
    s = s.lower().strip()
    return s.startswith("pin") or s in ("gnd", "5v", "3v3", "vin")


def _pin_label(s: str) -> str:
    s = s.strip()
    if s.lower().startswith("pin"):
        return f"Pin {s[3:]}"
    return s.upper()


# ─── Renderer Registry ────────────────────────────────────────────

def _legend_resistor(comp):
    v = comp.get("value", "?")
    return f"{v}\u03A9 resistor  {comp['from']} \u2192 {comp['to']}", "#c8aa78"


def _legend_led(comp):
    c = comp.get("color", "red")
    return (f"{c} LED  {comp['anode']}(+) \u2192 {comp['cathode']}(\u2013)",
            LED_PALETTE.get(c, LED_PALETTE["red"])[0])


def _legend_button(comp):
    return f"button  {comp['from']} \u2192 {comp['to']}", "#444"


def _legend_buzzer(comp):
    v = comp.get("variant", "active")
    pos = comp.get("positive", comp.get("from", "?"))
    neg = comp.get("negative", comp.get("to", "?"))
    return (f"{v} buzzer  {pos}(+) \u2192 {neg}(\u2013)",
            BUZZER_PALETTE.get(v, BUZZER_PALETTE["active"])[0])


def _legend_sensor(comp):
    label = comp.get("label", comp.get("name", "sensor"))
    return f"{label} module", "#1a6b3c"


def _legend_potentiometer(comp):
    return (f"potentiometer  {comp.get('pin1', '?')} / "
            f"{comp.get('pin2', '?')} / {comp.get('pin3', '?')}"), "#555"


def _legend_rgb_led(comp):
    return (f"RGB LED  R={comp.get('red', '?')} G={comp.get('green', '?')} "
            f"B={comp.get('blue', '?')}"), "#e8e8e8"


def _legend_seven_segment(comp):
    d = comp.get("digits", 1)
    return f"{d}-digit 7-segment display (row {comp.get('row_start', '?')})", "#1a1a1a"


def _legend_module(comp):
    return comp.get("name", "module"), comp.get("color", "#37474f")


RENDERERS: dict[str, tuple] = {
    "resistor":      (render_resistor,      _legend_resistor),
    "led":           (render_led,           _legend_led),
    "button":        (render_button,        _legend_button),
    "buzzer":        (render_buzzer,        _legend_buzzer),
    "sensor":        (render_sensor,        _legend_sensor),
    "potentiometer": (render_potentiometer, _legend_potentiometer),
    "rgb_led":       (render_rgb_led,       _legend_rgb_led),
    "seven_segment": (render_seven_segment, _legend_seven_segment),
    "module":        (render_module,        _legend_module),
}


def render_wire(board: Board, wire: dict) -> list[str]:
    color = wire.get("color", "#444")
    from_id, to_id = str(wire["from"]), str(wire["to"])
    from_board, to_board = _is_board_pin(from_id), _is_board_pin(to_id)

    if from_board and to_board:
        return []

    # Get the breadboard-side endpoint
    if not from_board:
        bx, by = board.hole_xy(from_id)
        board.mark_occupied(from_id)
    else:
        bx, by = board.hole_xy(to_id)
        board.mark_occupied(to_id)

    els = []

    if from_board or to_board:
        pin = from_id if from_board else to_id
        hole = to_id if from_board else from_id
        label = _pin_label(pin)

        # Pill dimensions — must fit within HOLE_PITCH (14px) to avoid overlap
        pill_h = 12
        pill_font = "8"
        text_w = max(len(label) * 5.5 + 8, 32)

        # Determine which side of the breadboard the hole is on
        # Right bank: columns f-j and right power rails (+R, -R)
        hole_col = hole.strip().lower()
        on_right = (hole_col[0] in "fghij"
                    or (hole_col[0] in "+-" and len(hole_col) > 1 and hole_col[1] == "r"))

        if on_right:
            pill_right = board.svg_width - 4
            pill_x = pill_right - text_w

            els.append(_line(bx, by, pill_x, by,
                             stroke=color, stroke_width="2",
                             stroke_linecap="round", opacity="0.8"))
            els.append(_rect(pill_x, by - pill_h / 2, text_w, pill_h, rx="4",
                             fill=color, opacity="0.92"))
            els.append(_text(pill_x + 4, by + 3, label,
                             font_size=pill_font, fill="white", font_weight="600",
                             font_family=FONT))
        else:
            pill_x = 4
            pill_right = pill_x + text_w

            els.append(_line(pill_right, by, bx, by,
                             stroke=color, stroke_width="2",
                             stroke_linecap="round", opacity="0.8"))
            els.append(_rect(pill_x, by - pill_h / 2, text_w, pill_h, rx="4",
                             fill=color, opacity="0.92"))
            els.append(_text(pill_x + 4, by + 3, label,
                             font_size=pill_font, fill="white", font_weight="600",
                             font_family=FONT))
    else:
        x1, y1 = board.hole_xy(from_id)
        x2, y2 = board.hole_xy(to_id)
        board.mark_occupied(from_id, to_id)
        els.append(_line(x1, y1, x2, y2,
                         stroke=color, stroke_width="2.8",
                         stroke_linecap="round", opacity="0.8"))

    return els


# ─── Board Chrome ────────────────────────────────────────────────

def render_background(board: Board) -> list[str]:
    bw = board.board_right - board.board_left
    bh = board.board_bottom - board.board_top
    els = []

    # Shadow
    els.append(_rect(board.board_left + 2, board.board_top + 2, bw, bh,
                     rx="8", fill="#00000015"))
    # Body
    els.append(_rect(board.board_left, board.board_top, bw, bh,
                     rx="8", fill=BOARD_FILL, stroke=BOARD_STROKE, stroke_width="1.2"))
    # Center channel
    cx1 = board._col_x["e"] + HOLE_PITCH * 0.5
    cx2 = board._col_x["f"] - HOLE_PITCH * 0.5
    els.append(_rect(cx1, board.board_top + 4, cx2 - cx1, bh - 8,
                     rx="2", fill=CENTER_CHANNEL, stroke="#c4b898", stroke_width="0.4"))

    return els


def render_power_rails(board: Board) -> list[str]:
    els = []
    y_top = board.board_top + 4
    y_bot = board.board_bottom - 4
    for col, c in [("+L", RAIL_RED), ("-L", RAIL_BLUE),
                   ("+R", RAIL_RED), ("-R", RAIL_BLUE)]:
        x = board._col_x[col]
        els.append(_line(x, y_top, x, y_bot,
                         stroke=c, stroke_width="1.2", opacity="0.2",
                         stroke_dasharray="3,5"))
    return els


def render_holes(board: Board) -> list[str]:
    els = []
    for col in "abcdefghij":
        for row in range(board.row_lo, board.row_hi + 1):
            x = board._col_x[col]
            y = board._terminal_row_y(row)
            hid = f"{col}{row}"
            fill = HOLE_OCCUPIED_COLOR if board.is_occupied(hid) else HOLE_COLOR
            els.append(_circle(x, y, HOLE_RADIUS, fill=fill))

    for col in ("+L", "-L", "+R", "-R"):
        for r in board._power_rows_in_view():
            x = board._col_x[col]
            y = board._power_row_y(r)
            els.append(_circle(x, y, HOLE_RADIUS - 0.5, fill=HOLE_COLOR))

    return els


def render_labels(board: Board) -> list[str]:
    els = []

    # Column letters
    for col in "abcdefghij":
        x = board._col_x[col]
        els.append(_text(x, board.board_top - 4, col,
                         font_size="9", fill=LABEL_COLOR,
                         text_anchor="middle", font_family=FONT_MONO))

    # Rail symbols
    for col, sym in [("+L", "+"), ("-L", "\u2013"), ("+R", "+"), ("-R", "\u2013")]:
        x = board._col_x[col]
        c = RAIL_RED if "+" in col else RAIL_BLUE
        els.append(_text(x, board.board_top - 4, sym,
                         font_size="10", fill=c, font_weight="bold",
                         text_anchor="middle", font_family=FONT))

    # Row numbers — every row in the visible range
    for row in range(board.row_lo, board.row_hi + 1):
        y = board._terminal_row_y(row) + 3.5
        # Only label every row if few visible, or every 5th + endpoints
        if board.visible_rows <= 25 or row == board.row_lo or row == board.row_hi or row % 5 == 0:
            lx = (board._col_x["-L"] + board._col_x["a"]) / 2
            els.append(_text(lx, y, str(row),
                             font_size="8", fill=LABEL_COLOR,
                             text_anchor="middle", font_family=FONT_MONO))
            rx = (board._col_x["j"] + board._col_x["+R"]) / 2
            els.append(_text(rx, y, str(row),
                             font_size="8", fill=LABEL_COLOR,
                             text_anchor="middle", font_family=FONT_MONO))

    return els


# ─── Connection Highlights ───────────────────────────────────────

def render_row_connections(board: Board) -> list[str]:
    """Draw subtle highlight bars behind rows that have occupied holes,
    showing which holes are electrically connected."""
    els = []
    occupied_rows = set()
    for hid in board.occupied:
        r = _extract_row(hid)
        if r:
            occupied_rows.add(r)

    for row in occupied_rows:
        if row < board.row_lo or row > board.row_hi:
            continue
        y = board._terminal_row_y(row)
        # Left bank (a-e)
        x_start = board._col_x["a"] - 5
        x_end = board._col_x["e"] + 5
        els.append(_rect(x_start, y - 5, x_end - x_start, 10,
                         rx="3", fill="#ffeaa7", opacity="0.25"))
        # Right bank (f-j)
        x_start = board._col_x["f"] - 5
        x_end = board._col_x["j"] + 5
        els.append(_rect(x_start, y - 5, x_end - x_start, 10,
                         rx="3", fill="#ffeaa7", opacity="0.25"))

    return els


# ─── Legend ───────────────────────────────────────────────────────

def render_legend(board: Board, circuit: dict) -> tuple[list[str], float]:
    els = []
    x = board.board_left
    y = board.board_bottom + 20

    els.append(_text(x, y, "COMPONENTS", font_size="8", fill="#999",
                     font_weight="600", letter_spacing="0.5", font_family=FONT))
    y += 14

    for comp in circuit.get("components", []):
        entry = RENDERERS.get(comp.get("type", ""))
        if entry:
            desc, swatch = entry[1](comp)
        else:
            desc, swatch = str(comp), "#999"

        els.append(_circle(x + 5, y - 3, 4, fill=swatch, stroke="#0002", stroke_width="0.5"))
        els.append(_text(x + 14, y, desc, font_size="9", fill="#444", font_family=FONT))
        y += 15

    if circuit.get("wires"):
        y += 6
        els.append(_text(x, y, "WIRES", font_size="8", fill="#999",
                         font_weight="600", letter_spacing="0.5", font_family=FONT))
        y += 14
        for wire in circuit["wires"]:
            c = wire.get("color", "#444")
            label = wire.get("label", f"{wire['from']} \u2192 {wire['to']}")
            els.append(_line(x + 1, y - 3, x + 10, y - 3,
                             stroke=c, stroke_width="3", stroke_linecap="round"))
            els.append(_text(x + 16, y, label, font_size="9", fill="#444", font_family=FONT))
            y += 15

    return els, y


# ─── Main Generation ─────────────────────────────────────────────

def generate(circuit: dict, rows: tuple[int, int] | None = None) -> str:
    # Determine visible row range
    if rows:
        row_lo, row_hi = rows
    elif circuit.get("rows"):
        r = circuit["rows"]
        if isinstance(r, list):
            row_lo, row_hi = int(r[0]), int(r[1])
        else:
            row_lo, row_hi = 1, int(r)
    else:
        row_lo, row_hi = detect_row_range(circuit, padding=3)

    board = Board(row_lo, row_hi)

    # Mark occupied holes
    for comp in circuit.get("components", []):
        for key in ("from", "to", "anode", "cathode", "positive", "negative",
                    "pin1", "pin2", "pin3", "red", "common", "green", "blue"):
            if key in comp and not _is_board_pin(str(comp[key])):
                board.mark_occupied(str(comp[key]))
        pins_val = comp.get("pins", [])
        if isinstance(pins_val, list):
            for pin in pins_val:
                if isinstance(pin, dict) and "hole" in pin:
                    h = str(pin["hole"])
                    if not _is_board_pin(h):
                        board.mark_occupied(h)
    for wire in circuit.get("wires", []):
        for key in ("from", "to"):
            if not _is_board_pin(str(wire[key])):
                board.mark_occupied(str(wire[key]))

    layers = []

    # Board chrome
    layers.extend(render_background(board))
    layers.extend(render_power_rails(board))
    layers.extend(render_row_connections(board))
    layers.extend(render_holes(board))
    layers.extend(render_labels(board))

    # Components
    for comp in circuit.get("components", []):
        entry = RENDERERS.get(comp.get("type", ""))
        if entry:
            layers.extend(entry[0](board, comp))

    # Wires
    for wire in circuit.get("wires", []):
        layers.extend(render_wire(board, wire))

    # Legend
    legend_els, legend_y = render_legend(board, circuit)
    layers.extend(legend_els)

    # Title
    name = circuit.get("name", "Breadboard Diagram")
    title_x = board.board_left + (board.board_right - board.board_left) / 2
    layers.append(_text(title_x, board.board_top - 22, name,
                        font_size="13", fill="#222", font_weight="700",
                        text_anchor="middle", font_family=FONT))

    # Row range indicator
    if row_lo > 1 or row_hi < TERMINAL_ROWS:
        layers.append(_text(title_x, board.board_top - 10,
                            f"rows {row_lo}\u2013{row_hi} of {TERMINAL_ROWS}",
                            font_size="9", fill="#999", text_anchor="middle",
                            font_family=FONT))

    svg_w = board.svg_width
    svg_h = max(board.svg_height, legend_y + 10)

    body = "\n".join(layers)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {svg_w:.0f} {svg_h:.0f}"
     width="{svg_w:.0f}" height="{svg_h:.0f}"
     style="background:#fff">
{body}
</svg>'''


# ─── CLI ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate SVG breadboard wiring diagrams from YAML.")
    parser.add_argument("input", help="Path to YAML circuit description")
    parser.add_argument("-o", "--output", help="Output SVG path (default: stdout)")
    parser.add_argument("--rows", help="Row range to display, e.g. '1-20'")
    args = parser.parse_args()

    circuit = load_circuit(args.input)

    rows = None
    if args.rows:
        lo, hi = args.rows.split("-")
        rows = (int(lo), int(hi))

    svg_str = generate(circuit, rows=rows)

    if args.output:
        Path(args.output).write_text(svg_str, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(svg_str)


if __name__ == "__main__":
    main()
