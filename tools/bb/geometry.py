"""Orientation, row detection, pin utilities, and dimension lookups."""

import math
import re

from bb.constants import (
    ORIENTATION_DEFAULTS,
    ORIENTATION_PRESETS,
    POWER_RAIL_ROWS,
    TERMINAL_ROWS,
)
from bb.loaders import load_component_specs


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


def _seven_segment_body_rows(comp: dict, specs: dict) -> float:
    """Return the body length in breadboard rows from component specs.

    Prefers the model lookup in component-specs.yaml. Falls back to
    hardcoded datasheet values if no model is specified.
    """
    model = comp.get("model", "")
    if model and model in specs:
        body_mm_val = specs[model].get("body_mm", [])
        if isinstance(body_mm_val, list) and body_mm_val:
            return body_mm_val[0] / 2.54

    # Fallback: hardcoded datasheet dimensions
    digits = comp.get("digits", 1)
    BODY_MM = {1: 12.60, 4: 50.30}
    body_mm = BODY_MM.get(digits, digits * 12.70)
    return body_mm / 2.54


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
        # seven_segment: account for full body extent, not just pin rows.
        # Multi-digit displays have bodies much larger than their pin span.
        if comp.get("type") == "seven_segment":
            rs = int(comp.get("row_start", 0))
            nd = comp.get("digits", 1)
            np = int(comp.get("pins", 10 if nd == 1 else 12)) // 2
            if rs:
                pin_center = rs + (np - 1) / 2
                body_rows = _seven_segment_body_rows(comp, load_component_specs())
                body_lo = int(pin_center - body_rows / 2)
                body_hi = int(pin_center + body_rows / 2) + 1
                for i in range(max(1, body_lo), min(TERMINAL_ROWS + 1, body_hi)):
                    rows_used.add(i)
        # module uses pins list (hole: or to: format)
        pins_val = comp.get("pins", [])
        if isinstance(pins_val, list):
            for pin in pins_val:
                if isinstance(pin, dict):
                    for k in ("hole", "to"):
                        if k in pin:
                            r = _extract_row(str(pin[k]))
                            if r:
                                rows_used.add(r)
        # module row: key for vertical positioning
        if comp.get("type") == "module" and comp.get("row"):
            rows_used.add(int(comp["row"]))

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


def _is_board_pin(s: str) -> bool:
    s = s.lower().strip()
    return s.startswith("pin") or s in ("gnd", "5v", "3v3", "vin")


def _normalize_pin_id(s: str) -> str:
    """Normalize a board pin identifier from wiring.yaml format to lookup key.

    Strips 'pin' or 'pin_' prefix and lowercases.
    Examples: 'pin9' → '9', 'pin_a0' → 'a0', 'gnd' → 'gnd', '5v' → '5v'.
    """
    s = s.strip().lower()
    if s.startswith("pin"):
        s = s[3:].lstrip("_")
    return s


def _pin_label(s: str) -> str:
    s = s.strip()
    if s.lower().startswith("pin"):
        rest = s[3:].lstrip("_")  # handle pin9 and pin_a0
        return f"Pin {rest.upper()}"
    return s.upper()
