"""Component render functions for breadboard SVG diagrams."""

import math

from bb.board import Board
from bb.constants import (
    BUZZER_PALETTE,
    FONT,
    FONT_MONO,
    HOLE_PITCH,
    LED_PALETTE,
)
from bb.geometry import (
    _is_board_pin,
    _pin_label,
    _seven_segment_body_rows,
    parse_orientation,
)
from bb.svg import _circle, _line, _rect, _text, resistor_bands


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


def render_button(board: Board, comp: dict) -> list[str]:
    """Render a push button spanning two rows across the center channel.

    Physical: 6mm tactile switch, ~12mm pin-to-pin across channel.
    Hardcoded: 16×16 body, 5px cap radius. Symmetric — no orientation needed.
    """
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
    """Render a buzzer (active or passive) as a cylinder viewed from above.

    Physical: ~12mm diameter cylinder, 2 pins at 7.6mm spacing.
    Hardcoded: 8px radius circle. Rotationally symmetric — no orientation needed.
    """
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
    """Render a generic 3-pin sensor module as a small PCB rectangle.

    Physical: varies widely (KY-series modules are ~24×15mm typical).
    Hardcoded: auto-sized from pin positions, min 18×18. Symmetric — no orientation needed.
    """
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
        els.append(_circle(x, y, 1.5, fill="silver", stroke="#999", stroke_width="0.3"))

    return els


def render_potentiometer(board: Board, comp: dict) -> list[str]:
    """Render a potentiometer as a circular knob with 3 pins.

    Physical: ~6.5mm body, 10mm knob, 3 pins at 2.54mm pitch.
    Hardcoded: 10px radius circle. Rotationally symmetric — no orientation needed.
    """
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
    """Render a 4-pin common-cathode RGB LED.

    Physical: 5mm dome, 4 pins at 2.54mm pitch.
    Hardcoded: 6.5px body radius. Position-derived layout — no orientation needed.
    """
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
    - 5161AS: 12.6mm × 19.0mm body, 10 pins (5/side), 10.16mm pin span
    - 5641AS: 50.3mm × 19.0mm body, 12 pins (6/side), 12.70mm pin span
    - Digit face: 8.1mm × 14.2mm (aspect 1.75:1, height/width)
    - 8° italic slant, DP at bottom-right of each digit
    - Pin row spacing: 15.24mm (0.6") → columns e to i
    - Pins are centered on the body along the long axis
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

    # Pin positions on the board
    x_left, y_pin_top = board.hole_xy(left_pins[0])
    x_right, _ = board.hole_xy(right_pins[0])
    _, y_pin_bot = board.hole_xy(left_pins[-1])
    pin_span_cy = (y_pin_top + y_pin_bot) / 2

    # Body dimensions — derived from datasheet, NOT from pin span.
    # The body length (along rows) is much larger than the pin span for
    # multi-digit displays. Pins are centered on the body.
    body_rows = _seven_segment_body_rows(comp, board.specs)
    body_h = body_rows * HOLE_PITCH
    pad_x = 6
    body_w = (x_right - x_left) + pad_x * 2
    body_x = x_left - pad_x
    body_y = pin_span_cy - body_h / 2
    body_cx = body_x + body_w / 2
    body_cy = pin_span_cy

    clip_id = f"seg-clip-{row_start}"

    els = []

    # IC body (black DIP package)
    els.append(_rect(body_x, body_y, body_w, body_h, rx="2",
                     fill="#1a1a1a", stroke="#444", stroke_width="0.8"))

    # Notch — positioned at the top edge of the body
    notch_cx = body_cx
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


def _module_box_width(name: str) -> float:
    """Compute the rendered width of a module box from its name."""
    return max(len(name) * 6 + 16, 60)


def _module_wire_color(label: str, default_color: str) -> str:
    """Pick a wire color based on a module pin label."""
    lbl = label.lower().strip().strip('"').strip("'")
    if lbl in ("gnd", "ground", "-"):
        return "#333333"
    if lbl in ("+5v", "5v", "vcc", "vin", "+3v3", "3v3", "+"):
        return "#e53935"
    return default_color


def render_module(board: Board, comp: dict) -> list[str]:
    """Render an off-board module as a labeled card left of the breadboard.

    Supports two pin formats:
      hole: (legacy) — pin maps to a breadboard hole, wire drawn to it
      to:   (direct) — pin connects directly to a destination (board pin,
             power rail, or breadboard hole). No intermediate holes needed.

    The card is positioned entirely outside the breadboard area. Pin anchors
    sit on the right edge of the card (facing the breadboard). Each pin's
    wire routes to its destination without overlapping other wires.
    """
    name = comp.get("name", "Module")
    color = comp.get("color", "#37474f")
    pins_list = comp.get("pins", [])

    if not pins_list:
        return []

    # Detect format: any pin with 'to:' → direct routing
    use_direct = any(isinstance(p, dict) and p.get("to") for p in pins_list)

    # Resolve vertical anchor and pin data
    pin_data = []  # list of (label, wire_color, dest_xy_or_none, dest_id)
    y_samples = []

    for pin in pins_list:
        if not isinstance(pin, dict):
            continue
        label = pin.get("label", "")
        wire_color = pin.get("color", _module_wire_color(label, color))

        if use_direct:
            dest = str(pin.get("to", ""))
            if dest and not _is_board_pin(dest):
                # Breadboard hole or power rail — has coordinates
                board.mark_occupied(dest)
                dx, dy = board.hole_xy(dest)
                y_samples.append(dy)
                pin_data.append((label, wire_color, (dx, dy), dest))
            else:
                # Board pin — no breadboard position
                pin_data.append((label, wire_color, None, dest))
        else:
            hole = str(pin.get("hole", ""))
            if hole and not _is_board_pin(hole):
                board.mark_occupied(hole)
                hx, hy = board.hole_xy(hole)
                y_samples.append(hy)
                pin_data.append((label, wire_color, (hx, hy), hole))

    if not pin_data:
        return []

    # Vertical positioning: use 'row' key, or average of resolved destinations
    row_key = comp.get("row")
    if row_key is not None:
        anchor_y = board._terminal_row_y(int(row_key))
    elif y_samples:
        anchor_y = sum(y_samples) / len(y_samples)
    else:
        anchor_y = (board.board_top + board.board_bottom) / 2

    # Card dimensions and position
    gap = 16
    pin_spacing = 14
    box_h = max(len(pin_data) * pin_spacing + 16, 32)
    box_w = _module_box_width(name)
    box_right = board.board_left - gap
    box_x = box_right - box_w
    box_y = anchor_y - box_h / 2
    pin_block_top = box_y + 20

    els = []

    # Card body
    els.append(_rect(box_x, box_y, box_w, box_h, rx="5",
                     fill=color, stroke="#263238", stroke_width="1", opacity="0.95"))

    # Module name
    els.append(_text(box_x + box_w / 2, box_y + 13, name,
                     font_size="8", fill="white", font_weight="700",
                     text_anchor="middle", font_family=FONT))

    # Render each pin: anchor dot, label, wire to destination
    for i, (label, wire_color, dest_xy, dest_id) in enumerate(pin_data):
        pin_y = pin_block_top + i * pin_spacing
        anchor_x = box_right

        # Pin anchor dot
        els.append(_circle(anchor_x, pin_y, 2.5,
                           fill="white", stroke=color, stroke_width="0.8"))

        # Pin label inside card
        if label:
            els.append(_text(anchor_x - 8, pin_y + 3, label,
                             font_size="6", fill="#ddd", font_weight="600",
                             text_anchor="end", font_family=FONT_MONO))

        if use_direct and dest_id and _is_board_pin(dest_id):
            mcu = getattr(board, "mcu", None)
            if mcu is not None:
                # Route to MCU board pin — defer to router via pending_module_wires
                pin_xy = mcu.pin_xy(dest_id, near=(anchor_x, pin_y))
                if pin_xy is not None:
                    if not hasattr(board, "_module_board_wires"):
                        board._module_board_wires = []
                    board._module_board_wires.append({
                        "src": (anchor_x, pin_y),
                        "dst": pin_xy,
                        "color": wire_color,
                    })
                    # Skip pill — wire will be rendered by the router
                    continue

            # Fallback: pill label on the right margin
            pill_label = _pin_label(dest_id)
            pill_h = 12
            text_w = max(len(pill_label) * 5.5 + 8, 32)
            pill_right = board.svg_width - 4
            pill_x = pill_right - text_w

            els.append(_line(anchor_x, pin_y, pill_x, pin_y,
                             stroke=wire_color, stroke_width="2",
                             stroke_linecap="round", opacity="0.8"))
            els.append(_rect(pill_x, pin_y - pill_h / 2, text_w, pill_h,
                             rx="4", fill=wire_color, opacity="0.92"))
            els.append(_text(pill_x + 4, pin_y + 3, pill_label,
                             font_size="8", fill="white", font_weight="600",
                             font_family=FONT))

        elif dest_xy:
            # Breadboard hole or power rail — wire to that position
            dx, dy = dest_xy
            # L-shaped route: horizontal to the destination's x, then vertical
            els.append(_line(anchor_x, pin_y, dx, pin_y,
                             stroke=wire_color, stroke_width="2",
                             stroke_linecap="round", opacity="0.8"))
            if abs(dy - pin_y) > 1:
                els.append(_line(dx, pin_y, dx, dy,
                                 stroke=wire_color, stroke_width="2",
                                 stroke_linecap="round", opacity="0.8"))

    return els
