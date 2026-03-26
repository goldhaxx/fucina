#!/usr/bin/env python3
"""Generate SVG breadboard wiring diagrams from YAML circuit descriptions.

Usage:
    python3 tools/breadboard.py sketches/001-blink/wiring.yaml -o sketches/001-blink/wiring.svg
    python3 tools/breadboard.py sketches/001-blink/wiring.yaml --rows 1-20 -o out.svg
"""

import argparse
import sys
from pathlib import Path

# ─── Public API — re-export everything for backward compatibility ─
# test-renderers.py imports `breadboard as bb` and uses bb.Board,
# bb.RENDERERS, bb._is_board_pin, bb.render_*, bb._text, etc.

from bb.constants import *  # noqa: F401,F403
from bb.svg import (  # noqa: F401
    _attr, _circle, _rect, _line, _text, resistor_bands,
)
from bb.loaders import load_circuit, load_component_specs  # noqa: F401
from bb.geometry import (  # noqa: F401
    compute_rotated_fit,
    detect_row_range,
    parse_orientation,
    _extract_row,
    _is_board_pin,
    _normalize_pin_id,
    _pin_label,
    _seven_segment_body_rows,
)
from bb.board import Board  # noqa: F401
from bb.renderers import (  # noqa: F401
    render_resistor,
    render_led,
    render_button,
    render_buzzer,
    render_sensor,
    render_potentiometer,
    render_rgb_led,
    render_seven_segment,
    render_module,
    _seven_segment_digit,
    _module_box_width,
    _module_wire_color,
)
from bb.chrome import (  # noqa: F401
    render_background,
    render_power_rails,
    render_holes,
    render_labels,
    render_row_connections,
)
from bb.legend import (  # noqa: F401
    RENDERERS,
    render_wire,
    render_legend,
)
from bb.boards import load_board  # noqa: F401
from bb.mcu import (  # noqa: F401
    McuBoard,
    render_board_outline,
    render_board_pins,
    MCU_GAP,
)
from bb.router import compute_mcu_gap  # noqa: F401


# ─── Main Generation ─────────────────────────────────────────────

def generate(circuit: dict, rows: tuple[int, int] | None = None,
             specs: dict | None = None,
             board_position: str | None = None) -> str:
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

    # Resolve board position: CLI arg > YAML > default
    pos = board_position or circuit.get("board_position", "left")

    # Load MCU board data (if specified and known)
    board_name = circuit.get("board")
    board_data = load_board(board_name) if board_name else None

    # Compute left/right margins — account for MCU board graphic + module cards
    margin_left = MARGIN_LEFT
    margin_right = MARGIN_RIGHT

    # Module card width
    module_card_w = 0
    for comp in circuit.get("components", []):
        if comp.get("type") == "module":
            card_w = _module_box_width(comp.get("name", "Module"))
            module_card_w = max(module_card_w, card_w)

    # Count board-pin wires to compute dynamic routing gap
    mcu_gap = MCU_GAP
    if board_data is not None:
        board_pin_count = 0
        for wire in circuit.get("wires", []):
            from_id, to_id = str(wire["from"]), str(wire["to"])
            if _is_board_pin(from_id) or _is_board_pin(to_id):
                board_pin_count += 1
        # Also count module pins that route to board pins
        for comp in circuit.get("components", []):
            if comp.get("type") == "module":
                for pin in comp.get("pins", []):
                    if isinstance(pin, dict):
                        dest = str(pin.get("to", ""))
                        if dest and _is_board_pin(dest):
                            board_pin_count += 1
        mcu_gap = compute_mcu_gap(board_pin_count)

    if board_data is not None:
        # MCU board graphic needs space
        from bb.mcu import MM_TO_PX
        mcu_w = board_data["dimensions_mm"]["height"] * MM_TO_PX  # rotated
        mcu_space = mcu_w + mcu_gap + BOARD_PAD_X
        if module_card_w > 0:
            # Module cards go to the left of the MCU board
            mcu_space += module_card_w + 20  # card + gap
        if pos == "left":
            margin_left = max(margin_left, mcu_space)
        else:
            margin_right = max(margin_right, mcu_space)
    elif module_card_w > 0:
        needed = 4 + module_card_w + 16 + BOARD_PAD_X
        margin_left = max(margin_left, needed)

    board = Board(row_lo, row_hi, margin_left=margin_left,
                  margin_right=margin_right)
    board.specs = specs if specs is not None else load_component_specs()

    # Create MCU board coordinate mapper if data loaded
    mcu: McuBoard | None = None
    if board_data is not None:
        mcu = McuBoard(board_data, pos,
                       breadboard_left=board.board_left,
                       breadboard_right=board.board_right,
                       breadboard_top=board.board_top,
                       breadboard_bottom=board.board_bottom,
                       gap=mcu_gap)

    # Collect wired pin IDs for MCU highlighting
    if mcu is not None:
        for wire in circuit.get("wires", []):
            for key in ("from", "to"):
                val = str(wire[key])
                if _is_board_pin(val):
                    mcu.wired_pins.add(_normalize_pin_id(val))
        for comp in circuit.get("components", []):
            pins_val = comp.get("pins", [])
            if isinstance(pins_val, list):
                for pin in pins_val:
                    if isinstance(pin, dict):
                        dest = str(pin.get("to", ""))
                        if dest and _is_board_pin(dest):
                            mcu.wired_pins.add(_normalize_pin_id(dest))

    # Store MCU reference on board for module renderer access
    board.mcu = mcu

    # Mark occupied holes
    for comp in circuit.get("components", []):
        for key in ("from", "to", "anode", "cathode", "positive", "negative",
                    "pin1", "pin2", "pin3", "red", "common", "green", "blue"):
            if key in comp and not _is_board_pin(str(comp[key])):
                board.mark_occupied(str(comp[key]))
        pins_val = comp.get("pins", [])
        if isinstance(pins_val, list):
            for pin in pins_val:
                if isinstance(pin, dict):
                    for k in ("hole", "to"):
                        if k in pin:
                            h = str(pin[k])
                            if not _is_board_pin(h):
                                board.mark_occupied(h)
    for wire in circuit.get("wires", []):
        for key in ("from", "to"):
            if not _is_board_pin(str(wire[key])):
                board.mark_occupied(str(wire[key]))

    layers = []

    # MCU board graphic (behind breadboard)
    if mcu is not None:
        layers.extend(render_board_outline(mcu))
        layers.extend(render_board_pins(mcu))

    # Breadboard chrome
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

    # Wires — partition into board-pin wires and hole-to-hole wires
    board_pin_wires = []
    for wire in circuit.get("wires", []):
        from_id, to_id = str(wire["from"]), str(wire["to"])
        if mcu is not None and (_is_board_pin(from_id) or _is_board_pin(to_id)):
            board_pin_wires.append(wire)
        else:
            layers.extend(render_wire(board, wire))

    # Routed wires (board-pin wires with smart routing)
    if mcu is not None and board_pin_wires:
        from bb.router import route_wires
        layers.extend(route_wires(board, mcu, board_pin_wires))

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
    # Ensure SVG encompasses the MCU board graphic
    if mcu is not None:
        bx, by, bw, bh = mcu.bbox
        svg_w = max(svg_w, bx + bw + MARGIN_RIGHT)
        svg_h = max(svg_h, by + bh + MARGIN_BOTTOM)

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
    parser.add_argument("--board-position", choices=["left", "right"],
                        help="Position of MCU board graphic (default: left)")
    args = parser.parse_args()

    circuit = load_circuit(args.input)
    specs = load_component_specs(args.input)

    rows = None
    if args.rows:
        lo, hi = args.rows.split("-")
        rows = (int(lo), int(hi))

    svg_str = generate(circuit, rows=rows, specs=specs,
                       board_position=args.board_position)

    if args.output:
        Path(args.output).write_text(svg_str, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(svg_str)


if __name__ == "__main__":
    main()
