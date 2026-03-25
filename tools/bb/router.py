"""Smart wire routing engine — orthogonal paths with obstacle avoidance."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, NamedTuple

from bb.board import Board
from bb.constants import FONT, HOLE_PITCH
from bb.geometry import _is_board_pin
from bb.svg import _attr

if TYPE_CHECKING:
    from bb.mcu import McuBoard


class Rect(NamedTuple):
    """Axis-aligned bounding box."""
    x: float
    y: float
    w: float
    h: float


class WireSpec(NamedTuple):
    """A wire to be routed between a board pin and a breadboard hole."""
    board_xy: tuple[float, float]   # MCU pin pixel position
    hole_xy: tuple[float, float]    # Breadboard hole pixel position
    color: str
    label: str
    pin_id: str                     # Original pin identifier


# Routing parameters
WIRE_SPACING = 5.0     # px between parallel wires in routing channels
BEND_RADIUS = 4.0      # px radius for rounded corners
WIRE_WIDTH = 2.0
WIRE_OPACITY = 0.85

# Default gap imported for compute_mcu_gap baseline
from bb.mcu import MCU_GAP as _MCU_GAP_DEFAULT


def compute_mcu_gap(wire_count: int) -> float:
    """Compute the routing gap needed for the given number of board-pin wires.

    Returns at least MCU_GAP (the default). When more wires need channels
    than fit at WIRE_SPACING in the default gap, the gap widens.
    """
    if wire_count <= 1:
        return _MCU_GAP_DEFAULT
    # Need (wire_count - 1) inter-channel spaces + padding on both edges
    needed = (wire_count - 1) * WIRE_SPACING + 2 * WIRE_SPACING
    return max(_MCU_GAP_DEFAULT, needed)


def collect_obstacles(mcu: McuBoard | None, board: Board) -> list[Rect]:
    """Collect obstacle bounding boxes for routing avoidance."""
    obstacles = []

    # MCU board graphic
    if mcu is not None:
        bx, by, bw, bh = mcu.bbox
        obstacles.append(Rect(bx, by, bw, bh))

    # Breadboard body
    obstacles.append(Rect(board.board_left, board.board_top,
                          board.board_right - board.board_left,
                          board.board_bottom - board.board_top))

    return obstacles


def _build_wire_specs(board: Board, mcu: McuBoard, wires: list[dict]) -> list[WireSpec]:
    """Convert wire dicts into WireSpec tuples with resolved coordinates."""
    specs = []
    for wire in wires:
        from_id, to_id = str(wire["from"]), str(wire["to"])
        color = wire.get("color", "#444")
        label = wire.get("label", f"{from_id} → {to_id}")

        if _is_board_pin(from_id):
            pin_id, hole_id = from_id, to_id
        else:
            pin_id, hole_id = to_id, from_id

        # Resolve breadboard hole position
        if _is_board_pin(hole_id):
            # Both endpoints are board pins — skip
            continue
        hx, hy = board.hole_xy(hole_id)
        board.mark_occupied(hole_id)

        # Resolve MCU pin position (nearest to the breadboard hole)
        pin_xy = mcu.pin_xy(pin_id, near=(hx, hy))
        if pin_xy is None:
            continue

        specs.append(WireSpec(
            board_xy=pin_xy,
            hole_xy=(hx, hy),
            color=color,
            label=label,
            pin_id=pin_id,
        ))

    return specs


def _vertical_span(spec: WireSpec) -> tuple[float, float]:
    """Return the Y-interval of a wire's vertical segment."""
    y1 = spec.board_xy[1]
    y2 = spec.hole_xy[1]
    return (min(y1, y2), max(y1, y2))


def _intervals_overlap(a: tuple[float, float], b: tuple[float, float]) -> bool:
    """Check if two Y-intervals overlap (exclusive of touching endpoints)."""
    return a[0] < b[1] and b[0] < a[1]


def _assign_channels(specs: list[WireSpec], gap_start_x: float,
                     gap_end_x: float) -> list[float]:
    """Assign vertical channel X positions using interval-graph coloring.

    Wires whose vertical segments overlap must be in different channels.
    Wires that don't overlap can share a channel, reducing the total number
    of distinct channel positions needed.

    Channels are spaced at WIRE_SPACING intervals, centered in the gap.
    If the gap is too narrow, channels extend beyond the gap boundaries
    (the caller should use compute_mcu_gap() to size the gap properly).
    """
    n = len(specs)
    if n == 0:
        return []
    if n == 1:
        return [(gap_start_x + gap_end_x) / 2]

    # Sort wires by destination Y (crossing minimization heuristic)
    sorted_indices = sorted(range(n), key=lambda i: specs[i].hole_xy[1])

    # Greedy interval-graph coloring: assign each wire (in Y-sorted order)
    # to the lowest-numbered channel that has no overlapping wire.
    # Each channel is a list of Y-intervals already assigned to it.
    channel_intervals: list[list[tuple[float, float]]] = []
    wire_channel = [0] * n  # maps original wire index → channel number

    for idx in sorted_indices:
        span = _vertical_span(specs[idx])
        assigned = False
        for ch_num, intervals in enumerate(channel_intervals):
            conflict = False
            for existing_span in intervals:
                if _intervals_overlap(span, existing_span):
                    conflict = True
                    break
            if not conflict:
                intervals.append(span)
                wire_channel[idx] = ch_num
                assigned = True
                break
        if not assigned:
            channel_intervals.append([span])
            wire_channel[idx] = len(channel_intervals) - 1

    # Convert channel numbers to pixel X positions
    num_channels = len(channel_intervals)
    center = (gap_start_x + gap_end_x) / 2
    total_span = WIRE_SPACING * (num_channels - 1) if num_channels > 1 else 0
    start_x = center - total_span / 2

    channels = [0.0] * n
    for i in range(n):
        channels[i] = start_x + wire_channel[i] * WIRE_SPACING

    return channels


def _compute_path(src: tuple[float, float], dst: tuple[float, float],
                  channel_x: float) -> list[tuple[float, float]]:
    """Compute an orthogonal H-V-H path from src to dst via a channel.

    Returns waypoints: src → (channel_x, src_y) → (channel_x, dst_y) → dst
    Collapses redundant segments when points are colinear.
    """
    sx, sy = src
    dx, dy = dst
    waypoints = [(sx, sy)]

    # Horizontal to channel
    if abs(channel_x - sx) > 0.5:
        waypoints.append((channel_x, sy))

    # Vertical to destination row
    if abs(dy - sy) > 0.5:
        waypoints.append((channel_x, dy))
    elif len(waypoints) == 1:
        # Same Y, just go straight
        waypoints.append((dx, dy))
        return waypoints

    # Horizontal to destination
    if abs(dx - channel_x) > 0.5:
        waypoints.append((dx, dy))
    elif waypoints[-1] != (dx, dy):
        waypoints[-1] = (dx, dy)

    return waypoints


def _render_path(waypoints: list[tuple[float, float]], color: str) -> str:
    """Render waypoints as an SVG <path> with rounded corners at bends."""
    if len(waypoints) < 2:
        return ""

    parts = [f"M {waypoints[0][0]:.1f} {waypoints[0][1]:.1f}"]

    for i in range(1, len(waypoints)):
        x, y = waypoints[i]
        if i < len(waypoints) - 1:
            # Check if there's a bend at this point
            px, py = waypoints[i - 1]
            nx, ny = waypoints[i + 1]

            # Determine bend direction
            dx_in = x - px
            dy_in = y - py
            dx_out = nx - x
            dy_out = ny - y

            if (abs(dx_in) > 0.5 and abs(dy_out) > 0.5) or \
               (abs(dy_in) > 0.5 and abs(dx_out) > 0.5):
                # 90° bend — add arc
                r = min(BEND_RADIUS,
                        math.hypot(dx_in, dy_in) / 2,
                        math.hypot(dx_out, dy_out) / 2)
                if r < 0.5:
                    parts.append(f"L {x:.1f} {y:.1f}")
                    continue

                # Point just before the bend
                len_in = math.hypot(dx_in, dy_in)
                ux_in = dx_in / len_in if len_in else 0
                uy_in = dy_in / len_in if len_in else 0
                bx = x - ux_in * r
                by = y - uy_in * r

                # Point just after the bend
                len_out = math.hypot(dx_out, dy_out)
                ux_out = dx_out / len_out if len_out else 0
                uy_out = dy_out / len_out if len_out else 0
                ax = x + ux_out * r
                ay = y + uy_out * r

                # Determine sweep direction
                cross = ux_in * uy_out - uy_in * ux_out
                sweep = 1 if cross > 0 else 0

                parts.append(f"L {bx:.1f} {by:.1f}")
                parts.append(f"A {r:.1f} {r:.1f} 0 0 {sweep} {ax:.1f} {ay:.1f}")
            else:
                parts.append(f"L {x:.1f} {y:.1f}")
        else:
            parts.append(f"L {x:.1f} {y:.1f}")

    d = " ".join(parts)
    return (f'<path d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{WIRE_WIDTH}" stroke-linecap="round" '
            f'opacity="{WIRE_OPACITY}"/>')


def route_wires(board: Board, mcu: McuBoard, wires: list[dict]) -> list[str]:
    """Route board-pin wires with smart orthogonal paths.

    Also routes module-to-board-pin wires collected during render_module().
    Returns SVG elements for all routed wires.
    """
    specs = _build_wire_specs(board, mcu, wires)

    # Add module board-pin wires (set by render_module when MCU is present)
    module_wires = getattr(board, "_module_board_wires", [])
    for mw in module_wires:
        specs.append(WireSpec(
            board_xy=mw["dst"],   # MCU pin position
            hole_xy=mw["src"],    # Module pin anchor
            color=mw["color"],
            label="",
            pin_id="",
        ))

    if not specs:
        return []

    # Determine routing gap boundaries
    if mcu.position == "left":
        gap_start_x = mcu.facing_edge_x + WIRE_SPACING
        gap_end_x = board.board_left - WIRE_SPACING
    else:
        gap_start_x = board.board_right + WIRE_SPACING
        gap_end_x = mcu.facing_edge_x - WIRE_SPACING

    channels = _assign_channels(specs, gap_start_x, gap_end_x)

    els = []
    for i, spec in enumerate(specs):
        path = _compute_path(spec.board_xy, spec.hole_xy, channels[i])
        svg = _render_path(path, spec.color)
        if svg:
            els.append(svg)

    return els
