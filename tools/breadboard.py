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


# ─── Main Generation ─────────────────────────────────────────────

def generate(circuit: dict, rows: tuple[int, int] | None = None,
             specs: dict | None = None) -> str:
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

    # Compute left margin — widen when module cards need space
    margin_left = MARGIN_LEFT
    for comp in circuit.get("components", []):
        if comp.get("type") == "module":
            card_w = _module_box_width(comp.get("name", "Module"))
            # card needs: 4px left pad + card_w + 16px gap + BOARD_PAD_X
            needed = 4 + card_w + 16 + BOARD_PAD_X
            margin_left = max(margin_left, needed)

    board = Board(row_lo, row_hi, margin_left=margin_left)
    board.specs = specs if specs is not None else load_component_specs()

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
    specs = load_component_specs(args.input)

    rows = None
    if args.rows:
        lo, hi = args.rows.split("-")
        rows = (int(lo), int(hi))

    svg_str = generate(circuit, rows=rows, specs=specs)

    if args.output:
        Path(args.output).write_text(svg_str, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(svg_str)


if __name__ == "__main__":
    main()
