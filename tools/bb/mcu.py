"""MCU board graphic — coordinate mapping and SVG rendering."""

from __future__ import annotations

import math

from bb.constants import FONT, FONT_MONO, HOLE_PITCH
from bb.geometry import _normalize_pin_id
from bb.svg import _circle, _line, _rect, _text

# Scale: breadboard HOLE_PITCH (14px) = 2.54mm
MM_TO_PX = HOLE_PITCH / 2.54

# Board graphic colors
MCU_FILL = "#1a5c2a"
MCU_STROKE = "#0d3318"
MCU_PIN_WIRED = "#ffd600"
MCU_PIN_UNWIRED = "#666"
MCU_PIN_RADIUS = 2.0
MCU_LABEL_COLOR = "#ccc"
MCU_LABEL_WIRED_COLOR = "#ffd600"
MCU_HEADER_LABEL_COLOR = "#8fbc8f"
MCU_CONNECTOR_FILL = "#888"
MCU_CONNECTOR_STROKE = "#555"

# Gap between MCU board graphic and breadboard
MCU_GAP = 40


class McuBoard:
    """Maps MCU pin names to pixel coordinates in the SVG.

    The board is drawn vertically (rotated 90° CW from natural orientation):
    - Natural left (USB end, low X) → BOTTOM of drawn board (high rot_y)
    - Natural right (double header, high X) → TOP of drawn board (low rot_y)
    - Natural top (power/analog, low Y) → LEFT side of drawn board
    - Natural bottom (digital 0-13, high Y) → RIGHT side, FACING breadboard

    This puts the most-used pins (digital 0-13, GND, AREF, SDA/SCL) on the
    breadboard-facing side, keeping wire routes short.
    """

    def __init__(self, board_data: dict, position: str,
                 breadboard_left: float, breadboard_right: float,
                 breadboard_top: float, breadboard_bottom: float,
                 gap: float | None = None):
        self.data = board_data
        self.position = position  # "left" or "right"
        self.gap = gap if gap is not None else MCU_GAP

        dims = board_data["dimensions_mm"]
        # After 90° CW rotation: natural width → height, natural height → width
        self.board_w_px = dims["height"] * MM_TO_PX  # ~294px
        self.board_h_px = dims["width"] * MM_TO_PX   # ~560px

        # Position the board relative to the breadboard
        if position == "left":
            self.board_x = breadboard_left - self.gap - self.board_w_px
            self.board_y = breadboard_top
        else:  # right
            self.board_x = breadboard_right + self.gap
            self.board_y = breadboard_top

        # Wired pins — populated by generate() before rendering
        self.wired_pins: set[str] = set()

        # Build pin lookup: id → list of (px_x, px_y, display_name)
        self._pin_map: dict[str, list[tuple[float, float, str]]] = {}
        self._all_pins: list[tuple[float, float, str, str | None]] = []
        self._build_pin_map()

    def _natural_to_px(self, nat_x_mm: float, nat_y_mm: float) -> tuple[float, float]:
        """Convert natural board mm coords to rotated SVG pixel coords.

        90° CW rotation: (x, y) → (y, board_natural_width - x)
        Then scale mm→px and offset to board position.
        """
        nat_w_mm = self.data["dimensions_mm"]["width"]
        # After rotation: px_x maps from natural Y, px_y maps from natural X (inverted)
        rot_x_mm = nat_y_mm
        rot_y_mm = nat_w_mm - nat_x_mm
        return (
            self.board_x + rot_x_mm * MM_TO_PX,
            self.board_y + rot_y_mm * MM_TO_PX,
        )

    def _build_pin_map(self):
        """Build lookup from pin ID to pixel positions."""
        for header in self.data.get("headers", []):
            sx, sy = header["start_mm"]
            dx, dy = header["pitch_mm"]
            for i, pin in enumerate(header["pins"]):
                nat_x = sx + i * dx
                nat_y = sy + i * dy
                px_x, px_y = self._natural_to_px(nat_x, nat_y)
                name = pin.get("name", "")
                pid = pin.get("id")

                self._all_pins.append((px_x, px_y, name, pid))

                if pid is not None:
                    pid_lower = str(pid).lower()
                    if pid_lower not in self._pin_map:
                        self._pin_map[pid_lower] = []
                    self._pin_map[pid_lower].append((px_x, px_y, name))

    def pin_xy(self, pin_id: str,
               near: tuple[float, float] | None = None) -> tuple[float, float] | None:
        """Look up pixel coordinates for a board pin.

        Args:
            pin_id: Raw wiring.yaml value (e.g., "pin9", "gnd", "5v", "pin_a0").
            near: Optional (x, y) hint — when multiple pins share the same id
                  (GND, 5V), returns the nearest one.

        Returns:
            (px_x, px_y) or None if pin not found.
        """
        key = _normalize_pin_id(pin_id)

        entries = self._pin_map.get(key)
        if not entries:
            return None

        if len(entries) == 1 or near is None:
            return entries[0][0], entries[0][1]

        # Pick nearest to hint point
        nx, ny = near
        best = min(entries, key=lambda e: math.hypot(e[0] - nx, e[1] - ny))
        return best[0], best[1]

    def all_pins(self) -> list[tuple[float, float, str, str | None]]:
        """Return all pins as (px_x, px_y, display_name, id_or_none)."""
        return self._all_pins

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        """Bounding box (x, y, w, h) of the board graphic."""
        return self.board_x, self.board_y, self.board_w_px, self.board_h_px

    @property
    def left_edge(self) -> float:
        return self.board_x

    @property
    def right_edge(self) -> float:
        return self.board_x + self.board_w_px

    @property
    def facing_edge_x(self) -> float:
        """X coordinate of the board edge that faces the breadboard."""
        if self.position == "left":
            return self.right_edge
        return self.left_edge


# ─── Board Graphic Rendering ─────────────────────────────────────

def render_board_outline(mcu: McuBoard) -> list[str]:
    """Render the MCU board body: PCB rectangle, connectors, name label."""
    bx, by, bw, bh = mcu.bbox
    els = []

    # Shadow
    els.append(_rect(bx + 2, by + 2, bw, bh, rx="4", fill="#00000020"))

    # PCB body
    els.append(_rect(bx, by, bw, bh, rx="4",
                     fill=MCU_FILL, stroke=MCU_STROKE, stroke_width="1.2"))

    # Connectors
    for conn in mcu.data.get("connectors", []):
        cx, cy = mcu._natural_to_px(conn["x_mm"], conn["y_mm"])
        # Connector dimensions also rotate
        cw = conn["height_mm"] * MM_TO_PX
        ch = conn["width_mm"] * MM_TO_PX

        if conn["type"] == "usb-b":
            els.append(_rect(cx, cy - ch, cw, ch, rx="2",
                             fill=MCU_CONNECTOR_FILL, stroke=MCU_CONNECTOR_STROKE,
                             stroke_width="0.8"))
            els.append(_text(cx + cw / 2, cy - ch / 2 + 3, "USB",
                             font_size="5", fill="#333", font_weight="600",
                             text_anchor="middle", font_family=FONT_MONO))
        elif conn["type"] == "barrel-jack":
            r = min(cw, ch) / 2 - 1
            els.append(_circle(cx + cw / 2, cy - ch / 2, r,
                               fill=MCU_CONNECTOR_FILL, stroke=MCU_CONNECTOR_STROKE,
                               stroke_width="0.8"))

    # Board name label — centered at top of board
    label_x = bx + bw / 2
    label_y = by + 16
    els.append(_text(label_x, label_y, mcu.data.get("display_name", mcu.data["name"]),
                     font_size="7", fill="white", font_weight="700",
                     text_anchor="middle", font_family=FONT))

    return els


def render_board_pins(mcu: McuBoard) -> list[str]:
    """Render all pin holes and labels on the MCU board graphic."""
    els = []

    for px_x, px_y, name, pid in mcu.all_pins():
        is_wired = pid is not None and str(pid).lower() in mcu.wired_pins
        pin_fill = MCU_PIN_WIRED if is_wired else MCU_PIN_UNWIRED
        pin_stroke = "#b8860b" if is_wired else "#444"

        # Pin hole
        els.append(_circle(px_x, px_y, MCU_PIN_RADIUS,
                           fill=pin_fill, stroke=pin_stroke, stroke_width="0.5"))

        # Pin label
        if name:
            label_color = MCU_LABEL_WIRED_COLOR if is_wired else MCU_LABEL_COLOR
            # Position label offset from pin based on which edge the pin is on
            bx, _, bw, _ = mcu.bbox
            bcx = bx + bw / 2
            if px_x < bcx:
                # Pin is on left half — label to the right
                els.append(_text(px_x + 4, px_y + 2.5, name,
                                 font_size="5", fill=label_color,
                                 font_family=FONT_MONO))
            else:
                # Pin is on right half — label to the left
                els.append(_text(px_x - 4, px_y + 2.5, name,
                                 font_size="5", fill=label_color,
                                 text_anchor="end", font_family=FONT_MONO))

    return els
