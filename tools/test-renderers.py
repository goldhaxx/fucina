#!/usr/bin/env python3
"""Visual test fixture for breadboard.py component renderers.

Generates a single SVG containing one of each component type, laid out
on the breadboard with red bounding boxes showing expected containment.
Open the output SVG to visually verify that every renderer works correctly.

Usage:
    python3 tools/test-renderers.py -o tools/test-renderers-output.svg
    open tools/test-renderers-output.svg
"""

import argparse
import sys
from pathlib import Path

# Import the breadboard module from the same directory
sys.path.insert(0, str(Path(__file__).parent))
import breadboard as bb


def build_test_circuit() -> dict:
    """Build a synthetic circuit with one of each component type."""
    return {
        "name": "Renderer Test Fixture — All Component Types",
        "components": [
            # 1. Resistor — rows 3-6
            {
                "type": "resistor",
                "value": 220,
                "from": "d3",
                "to": "d6",
            },
            # 2. LED — rows 8-9
            {
                "type": "led",
                "color": "red",
                "anode": "e8",
                "cathode": "e9",
            },
            # 3. LED (different color) — rows 8-9 right bank
            {
                "type": "led",
                "color": "blue",
                "anode": "f8",
                "cathode": "f9",
            },
            # 4. Button — row 12 spanning center channel
            {
                "type": "button",
                "from": "e12",
                "to": "f12",
            },
            # 5. Active buzzer — rows 15-16
            {
                "type": "buzzer",
                "variant": "active",
                "positive": "a15",
                "negative": "a16",
            },
            # 6. Passive buzzer — rows 15-16 right bank
            {
                "type": "buzzer",
                "variant": "passive",
                "positive": "j15",
                "negative": "j16",
            },
            # 7. Sensor — rows 19-21
            {
                "type": "sensor",
                "label": "LDR",
                "pin1": "a19",
                "pin2": "a20",
                "pin3": "a21",
            },
            # 8. Potentiometer — rows 24-26
            {
                "type": "potentiometer",
                "pin1": "a24",
                "pin2": "a25",
                "pin3": "a26",
            },
            # 9. RGB LED — rows 29-32
            {
                "type": "rgb_led",
                "red": "e29",
                "common": "e30",
                "green": "e31",
                "blue": "e32",
            },
            # 10. Seven segment (1-digit) — rows 35-39
            {
                "type": "seven_segment",
                "digits": 1,
                "row_start": 35,
                "pins": 10,
                "left_col": "e",
                "right_col": "i",
            },
            # 11. Seven segment (4-digit) — rows 42-47
            {
                "type": "seven_segment",
                "digits": 4,
                "row_start": 42,
                "pins": 12,
                "left_col": "e",
                "right_col": "i",
            },
            # 12. Module — rows 50-53
            {
                "type": "module",
                "name": "HC-SR04",
                "color": "#1565c0",
                "pins": [
                    {"hole": "a50", "label": "VCC"},
                    {"hole": "a51", "label": "TRIG"},
                    {"hole": "a52", "label": "ECHO"},
                    {"hole": "a53", "label": "GND"},
                ],
            },
        ],
        "wires": [
            # Wire to left-bank hole (pin label on left)
            {"from": "pin9", "to": "a3", "color": "#e53935", "label": "signal — Pin 9"},
            # Wire to right-bank hole (pin label on right)
            {"from": "pin10", "to": "j3", "color": "#1e88e5", "label": "PWM — Pin 10"},
            # Breadboard-to-breadboard wire
            {"from": "e6", "to": "e8", "color": "#43a047", "label": "R1 to LED anode"},
            # Power rail wires
            {"from": "5v", "to": "+L1", "color": "#d32f2f", "label": "5V rail"},
            {"from": "gnd", "to": "-L1", "color": "#333", "label": "GND rail"},
        ],
    }


def add_bounding_boxes(board: bb.Board, circuit: dict) -> list[str]:
    """Generate red bounding-box outlines for components that have spatial extent.

    These boxes are NOT part of the production renderer — they're test-only
    visual aids for verifying that components render within expected bounds.
    """
    els = []

    for comp in circuit.get("components", []):
        t = comp.get("type", "")
        coords = []

        # Collect all hole coordinates for this component
        for key in ("from", "to", "anode", "cathode", "positive", "negative",
                    "pin1", "pin2", "pin3", "red", "common", "green", "blue"):
            if key in comp and not bb._is_board_pin(str(comp[key])):
                coords.append(board.hole_xy(str(comp[key])))

        if isinstance(comp.get("pins"), list):
            for pin in comp["pins"]:
                if isinstance(pin, dict) and "hole" in pin:
                    h = str(pin["hole"])
                    if not bb._is_board_pin(h):
                        coords.append(board.hole_xy(h))

        if not coords:
            continue

        # Seven segment gets a tighter box from its body dimensions
        if t == "seven_segment":
            row_start = int(comp.get("row_start", 10))
            pins_count = int(comp.get("pins", 10))
            pins_per_side = pins_count // 2
            left_col = comp.get("left_col", "e")
            right_col = comp.get("right_col", "i")

            x_left, y_top = board.hole_xy(f"{left_col}{row_start}")
            x_right, _ = board.hole_xy(f"{right_col}{row_start}")
            _, y_bot = board.hole_xy(f"{left_col}{row_start + pins_per_side - 1}")

            pad = 8
            els.append(bb._rect(
                x_left - pad, y_top - pad,
                (x_right - x_left) + pad * 2,
                (y_bot - y_top) + pad * 2,
                rx="2", fill="none", stroke="#ff0000",
                stroke_width="1", stroke_dasharray="3,2", opacity="0.6",
            ))
            continue

        # Generic bounding box from coordinates
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        pad = 12
        x_min, x_max = min(xs) - pad, max(xs) + pad
        y_min, y_max = min(ys) - pad, max(ys) + pad

        els.append(bb._rect(
            x_min, y_min, x_max - x_min, y_max - y_min,
            rx="2", fill="none", stroke="#ff0000",
            stroke_width="1", stroke_dasharray="3,2", opacity="0.6",
        ))

    return els


def generate_test_svg(circuit: dict) -> str:
    """Generate the test SVG with bounding boxes overlaid."""
    # Use full board height to show all components
    row_lo, row_hi = bb.detect_row_range(circuit, padding=2)
    board = bb.Board(row_lo, row_hi)

    # Mark all occupied holes (same as generate())
    for comp in circuit.get("components", []):
        for key in ("from", "to", "anode", "cathode", "positive", "negative",
                    "pin1", "pin2", "pin3", "red", "common", "green", "blue"):
            if key in comp and not bb._is_board_pin(str(comp[key])):
                board.mark_occupied(str(comp[key]))
        pins_val = comp.get("pins", [])
        if isinstance(pins_val, list):
            for pin in pins_val:
                if isinstance(pin, dict) and "hole" in pin:
                    h = str(pin["hole"])
                    if not bb._is_board_pin(h):
                        board.mark_occupied(h)
    for wire in circuit.get("wires", []):
        for key in ("from", "to"):
            if not bb._is_board_pin(str(wire[key])):
                board.mark_occupied(str(wire[key]))

    layers = []

    # Board chrome
    layers.extend(bb.render_background(board))
    layers.extend(bb.render_power_rails(board))
    layers.extend(bb.render_row_connections(board))
    layers.extend(bb.render_holes(board))
    layers.extend(bb.render_labels(board))

    # Bounding boxes (rendered BEFORE components so they appear behind)
    layers.extend(add_bounding_boxes(board, circuit))

    # Components — use the RENDERERS registry
    for comp in circuit.get("components", []):
        entry = bb.RENDERERS.get(comp.get("type", ""))
        if entry:
            layers.extend(entry[0](board, comp))

    # Wires
    for wire in circuit.get("wires", []):
        layers.extend(bb.render_wire(board, wire))

    # Legend
    legend_els, legend_y = bb.render_legend(board, circuit)
    layers.extend(legend_els)

    # Title
    title_x = board.board_left + (board.board_right - board.board_left) / 2
    layers.append(bb._text(title_x, board.board_top - 22, circuit["name"],
                           font_size="13", fill="#222", font_weight="700",
                           text_anchor="middle", font_family=bb.FONT))

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


def main():
    parser = argparse.ArgumentParser(
        description="Generate visual test SVG for all breadboard.py renderers.")
    parser.add_argument("-o", "--output", default="tools/test-renderers-output.svg",
                        help="Output SVG path (default: tools/test-renderers-output.svg)")
    args = parser.parse_args()

    circuit = build_test_circuit()
    svg_str = generate_test_svg(circuit)

    Path(args.output).write_text(svg_str, encoding="utf-8")
    print(f"Wrote {args.output} — open in browser to inspect", file=sys.stderr)

    # Print summary
    comp_types = set(c.get("type", "?") for c in circuit["components"])
    print(f"  {len(circuit['components'])} components ({len(comp_types)} types): "
          f"{', '.join(sorted(comp_types))}", file=sys.stderr)
    print(f"  {len(circuit['wires'])} wires", file=sys.stderr)


if __name__ == "__main__":
    main()
