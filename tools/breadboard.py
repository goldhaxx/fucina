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
MARGIN_RIGHT = 20

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
        for key in ("from", "to", "anode", "cathode"):
            if key in comp:
                r = _extract_row(str(comp[key]))
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


def _is_board_pin(s: str) -> bool:
    s = s.lower().strip()
    return s.startswith("pin") or s in ("gnd", "5v", "3v3", "vin")


def _pin_label(s: str) -> str:
    s = s.strip()
    if s.lower().startswith("pin"):
        return f"Pin {s[3:]}"
    return s.upper()


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
        label = _pin_label(pin)
        text_w = max(len(label) * 7 + 12, 40)
        pill_x = 4
        pill_right = pill_x + text_w

        # Wire line from pill to hole
        els.append(_line(pill_right, by, bx, by,
                         stroke=color, stroke_width="2.8",
                         stroke_linecap="round", opacity="0.8"))

        # Label pill
        els.append(_rect(pill_x, by - 9, text_w, 18, rx="5",
                         fill=color, opacity="0.92"))
        els.append(_text(pill_x + 6, by + 4, label,
                         font_size="10", fill="white", font_weight="600",
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
        t = comp.get("type", "?")
        if t == "resistor":
            v = comp.get("value", "?")
            desc = f"{v}\u03A9 resistor  {comp['from']} \u2192 {comp['to']}"
            swatch = "#c8aa78"
        elif t == "led":
            c = comp.get("color", "red")
            desc = f"{c} LED  {comp['anode']}(+) \u2192 {comp['cathode']}(\u2013)"
            swatch = LED_PALETTE.get(c, LED_PALETTE["red"])[0]
        else:
            desc = str(comp)
            swatch = "#999"

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
        for key in ("from", "to", "anode", "cathode"):
            if key in comp and not _is_board_pin(str(comp[key])):
                board.mark_occupied(str(comp[key]))
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
        t = comp.get("type", "")
        if t == "resistor":
            layers.extend(render_resistor(board, comp))
        elif t == "led":
            layers.extend(render_led(board, comp))

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
