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
        "board": "hero-xl",
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

        # Seven segment: use datasheet body dimensions, not pin span
        if t == "seven_segment":
            row_start = int(comp.get("row_start", 10))
            pins_count = int(comp.get("pins", 10))
            pins_per_side = pins_count // 2
            left_col = comp.get("left_col", "e")
            right_col = comp.get("right_col", "i")

            x_left, _ = board.hole_xy(f"{left_col}{row_start}")
            x_right, _ = board.hole_xy(f"{right_col}{row_start}")
            _, y_pin_top = board.hole_xy(f"{left_col}{row_start}")
            _, y_pin_bot = board.hole_xy(f"{left_col}{row_start + pins_per_side - 1}")
            pin_span_cy = (y_pin_top + y_pin_bot) / 2
            body_rows = bb._seven_segment_body_rows(comp, board.specs)
            body_h = body_rows * bb.HOLE_PITCH

            pad = 4
            els.append(bb._rect(
                x_left - pad, pin_span_cy - body_h / 2 - pad,
                (x_right - x_left) + pad * 2,
                body_h + pad * 2,
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
    """Generate the test SVG using bb.generate() with bounding box overlays.

    Uses the main generate() function so the test fixture exercises the same
    code paths as production (including board graphic and wire routing).
    Bounding boxes are injected as a post-processing overlay.
    """
    # Generate the base SVG via the production pipeline
    base_svg = bb.generate(circuit)

    # Build bounding box overlays using a separate Board for coordinate lookups
    row_lo, row_hi = bb.detect_row_range(circuit, padding=2)
    board = bb.Board(row_lo, row_hi)
    board.specs = bb.load_component_specs()
    bbox_els = add_bounding_boxes(board, circuit)

    if not bbox_els:
        return base_svg

    # Inject bounding boxes just before </svg>
    bbox_layer = "\n".join(bbox_els)
    return base_svg.replace("</svg>", f"{bbox_layer}\n</svg>")


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
