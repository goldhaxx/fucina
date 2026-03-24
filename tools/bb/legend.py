"""Legend rendering, renderer registry, and wire rendering."""

from bb.board import Board
from bb.constants import BUZZER_PALETTE, FONT, LED_PALETTE
from bb.geometry import _is_board_pin, _pin_label
from bb.renderers import (
    render_button,
    render_buzzer,
    render_led,
    render_module,
    render_potentiometer,
    render_resistor,
    render_rgb_led,
    render_sensor,
    render_seven_segment,
)
from bb.svg import _circle, _line, _rect, _text


# ─── Legend description functions ─────────────────────────────────

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


# ─── Renderer Registry ───────────────────────────────────────────

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


# ─── Wire Rendering ──────────────────────────────────────────────

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


# ─── Legend Rendering ─────────────────────────────────────────────

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
