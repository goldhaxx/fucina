"""Smart wire routing engine — orthogonal paths with obstacle avoidance."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, NamedTuple

from bb.board import Board
from bb.constants import FONT, HOLE_PITCH
from bb.geometry import _is_board_pin
from bb.mcu import MCU_GAP as _MCU_GAP_DEFAULT
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


BOARD_CLEARANCE = 8.0  # px clearance when routing around the board body


def _is_far_side(src_x: float, channel_x: float, board_bbox: Rect | None) -> bool:
    """Check if a pin is on the far side of the board from the routing channel.

    A pin is "far side" if a straight horizontal line from the pin to the
    channel would cross through the board interior. This means the pin is
    on the opposite side of the board center from the channel.
    """
    if board_bbox is None:
        return False
    bx, _, bw, _ = board_bbox
    board_center_x = bx + bw / 2
    # Far side: pin is on the opposite side of the board center from the channel
    if channel_x > board_center_x:
        return src_x < board_center_x
    else:
        return src_x > board_center_x


def _compute_path(src: tuple[float, float], dst: tuple[float, float],
                  channel_x: float,
                  board_bbox: Rect | None = None) -> list[tuple[float, float]]:
    """Compute an orthogonal path from src to dst via a channel.

    For near-side pins: H-V-H path (src → channel → dst).
    For far-side pins: route around the board body — go vertically to
    clear the board top or bottom, then horizontally past the far edge,
    then into the channel, then to the destination.
    """
    sx, sy = src
    dx, dy = dst

    if board_bbox is not None and _is_far_side(sx, channel_x, board_bbox):
        bx, by, bw, bh = board_bbox
        board_top = by
        board_bottom = by + bh

        # Decide whether to route around the top or bottom (shortest path)
        dist_to_top = abs(sy - board_top)
        dist_to_bottom = abs(sy - board_bottom)

        if dist_to_top <= dist_to_bottom:
            clear_y = board_top - BOARD_CLEARANCE
        else:
            clear_y = board_bottom + BOARD_CLEARANCE

        # Far-edge X: the board edge away from the breadboard
        if channel_x > bx + bw / 2:
            far_x = bx - BOARD_CLEARANCE  # board on left, far edge is left
        else:
            far_x = bx + bw + BOARD_CLEARANCE  # board on right, far edge is right

        waypoints = [(sx, sy)]

        # Step 1: vertical from pin to clear the board top/bottom
        if abs(clear_y - sy) > 0.5:
            waypoints.append((sx, clear_y))

        # Step 2: horizontal past the far edge (still outside board Y range)
        if abs(far_x - sx) > 0.5:
            waypoints.append((far_x, clear_y))

        # Step 3: horizontal to the channel X
        if abs(channel_x - far_x) > 0.5:
            waypoints.append((channel_x, clear_y))

        # Step 4: vertical to destination row
        if abs(dy - clear_y) > 0.5:
            waypoints.append((channel_x, dy))

        # Step 5: horizontal to destination
        if abs(dx - channel_x) > 0.5:
            waypoints.append((dx, dy))
        elif waypoints[-1] != (dx, dy):
            waypoints[-1] = (dx, dy)

        return waypoints

    # Near-side: simple H-V-H
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


# ─── Crossing detection and bridge rendering ────────────────────────

BRIDGE_GAP = 6.0  # px — half-width of the gap drawn at crossing points


def _seg_intersect(p1: tuple[float, float], p2: tuple[float, float],
                   p3: tuple[float, float], p4: tuple[float, float]
                   ) -> tuple[float, float] | None:
    """Find intersection of two orthogonal line segments, or None."""
    # Segment 1: p1→p2, Segment 2: p3→p4
    # Only handle axis-aligned segments (H or V)
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    # Classify each segment
    h1 = abs(y2 - y1) < 0.5  # horizontal
    v1 = abs(x2 - x1) < 0.5  # vertical
    h2 = abs(y4 - y3) < 0.5
    v2 = abs(x4 - x3) < 0.5

    if h1 and v2:
        # Seg1 horizontal, Seg2 vertical
        hy = y1
        vx = x3
        if (min(x1, x2) < vx < max(x1, x2) and
                min(y3, y4) < hy < max(y3, y4)):
            return (vx, hy)
    elif v1 and h2:
        # Seg1 vertical, Seg2 horizontal
        vx = x1
        hy = y3
        if (min(y1, y2) < hy < max(y1, y2) and
                min(x3, x4) < vx < max(x3, x4)):
            return (vx, hy)

    return None


def _detect_crossings(paths: list[list[tuple[float, float]]]
                      ) -> list[tuple[int, int, tuple[float, float]]]:
    """Detect pairwise segment crossings between all paths.

    Returns list of (path_i, seg_j_in_path_i, crossing_point) — one entry
    per crossing, attributed to the later path (higher index) so the bridge
    gap is drawn on the wire that renders on top.
    """
    crossings: list[tuple[int, int, tuple[float, float]]] = []

    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            for si in range(len(paths[i]) - 1):
                for sj in range(len(paths[j]) - 1):
                    pt = _seg_intersect(
                        paths[i][si], paths[i][si + 1],
                        paths[j][sj], paths[j][sj + 1],
                    )
                    if pt is not None:
                        # Attribute to the earlier path (under-wire gets the gap)
                        crossings.append((i, si, pt))

    return crossings


def _render_path_with_crossings(waypoints: list[tuple[float, float]],
                                color: str,
                                crossing_points: list[tuple[float, float]]) -> str:
    """Render a wire path with bridge gaps at crossing points.

    Splits the path into sub-segments around each crossing, leaving a small
    gap so the under-wire is visible. Returns concatenated SVG path elements.
    """
    if not crossing_points:
        return _render_path(waypoints, color)

    # For each segment of the path, collect crossings sorted by distance from start
    # Then split the path at each crossing with a gap
    els = []

    # Walk through waypoints, breaking at crossings
    # First, associate crossings with their segment
    seg_crossings: dict[int, list[tuple[float, float]]] = {}
    for pt in crossing_points:
        cx, cy = pt
        # Find which segment this crossing is on
        for si in range(len(waypoints) - 1):
            ax, ay = waypoints[si]
            bx, by = waypoints[si + 1]
            # Check if point is on this segment
            if abs(by - ay) < 0.5:  # horizontal segment
                if abs(cy - ay) < 0.5 and min(ax, bx) <= cx <= max(ax, bx):
                    seg_crossings.setdefault(si, []).append(pt)
                    break
            elif abs(bx - ax) < 0.5:  # vertical segment
                if abs(cx - ax) < 0.5 and min(ay, by) <= cy <= max(ay, by):
                    seg_crossings.setdefault(si, []).append(pt)
                    break

    # Build sub-paths by splitting at crossing gaps
    current_path: list[tuple[float, float]] = [waypoints[0]]

    for si in range(len(waypoints) - 1):
        seg_start = waypoints[si]
        seg_end = waypoints[si + 1]

        if si not in seg_crossings:
            current_path.append(seg_end)
            continue

        # Sort crossings along the segment by distance from segment start
        sx, sy = seg_start
        pts = sorted(seg_crossings[si],
                     key=lambda p: math.hypot(p[0] - sx, p[1] - sy))

        for cx, cy in pts:
            # Direction of this segment
            dx = seg_end[0] - seg_start[0]
            dy = seg_end[1] - seg_start[1]
            seg_len = math.hypot(dx, dy)
            if seg_len < 0.5:
                continue
            ux, uy = dx / seg_len, dy / seg_len

            # Gap before/after crossing, clamped to segment bounds
            dist_from_start = math.hypot(cx - sx, cy - sy)
            dist_to_end = math.hypot(seg_end[0] - cx, seg_end[1] - cy)

            if dist_from_start < BRIDGE_GAP:
                gap_before = seg_start
            else:
                gap_before = (cx - ux * BRIDGE_GAP, cy - uy * BRIDGE_GAP)

            if dist_to_end < BRIDGE_GAP:
                gap_after = seg_end
            else:
                gap_after = (cx + ux * BRIDGE_GAP, cy + uy * BRIDGE_GAP)

            # End current sub-path at gap_before
            current_path.append(gap_before)
            svg = _render_path(current_path, color)
            if svg:
                els.append(svg)

            # Start new sub-path at gap_after
            current_path = [gap_after]

        current_path.append(seg_end)

    # Render final sub-path
    if len(current_path) >= 2:
        svg = _render_path(current_path, color)
        if svg:
            els.append(svg)

    return "\n".join(els)


# ─── Inline pill labels ──────────────────────────────────────────────

WIRE_LABEL_THRESHOLD = 100.0  # px — minimum path length to earn an inline label
WIRE_LABEL_FONT_SIZE = 6.0
WIRE_LABEL_PAD_X = 4.0
WIRE_LABEL_PAD_Y = 2.0


def _path_length(waypoints: list[tuple[float, float]]) -> float:
    """Total length of a multi-segment path."""
    total = 0.0
    for i in range(1, len(waypoints)):
        dx = waypoints[i][0] - waypoints[i - 1][0]
        dy = waypoints[i][1] - waypoints[i - 1][1]
        total += math.hypot(dx, dy)
    return total


def _longest_segment(waypoints: list[tuple[float, float]]
                     ) -> tuple[int, float]:
    """Return (segment_index, length) of the longest segment."""
    best_idx, best_len = 0, 0.0
    for i in range(len(waypoints) - 1):
        dx = waypoints[i + 1][0] - waypoints[i][0]
        dy = waypoints[i + 1][1] - waypoints[i][1]
        seg_len = math.hypot(dx, dy)
        if seg_len > best_len:
            best_idx, best_len = i, seg_len
    return best_idx, best_len


def _truncate_label(text: str, max_chars: int = 18) -> str:
    """Shorten label text to fit in a pill."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 1] + "\u2026"


def _pill_dimensions(label: str) -> tuple[float, float]:
    """Return (width, height) of a pill for the given label text."""
    text = _truncate_label(label)
    char_width = WIRE_LABEL_FONT_SIZE * 0.55
    pill_w = len(text) * char_width + 2 * WIRE_LABEL_PAD_X
    pill_h = WIRE_LABEL_FONT_SIZE + 2 * WIRE_LABEL_PAD_Y
    return pill_w, pill_h


def _label_candidate(waypoints: list[tuple[float, float]], label: str
                     ) -> tuple[float, float, float, float, int, bool] | None:
    """Compute candidate label placement: (cx, cy, pill_w, pill_h, seg_idx, is_vertical).

    Returns None if the wire is too short for a label.
    """
    total = _path_length(waypoints)
    if total < WIRE_LABEL_THRESHOLD or not label:
        return None

    seg_idx, seg_len = _longest_segment(waypoints)
    if seg_len < 30:
        return None

    ax, ay = waypoints[seg_idx]
    bx, by = waypoints[seg_idx + 1]
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    is_vertical = abs(bx - ax) < 0.5
    pill_w, pill_h = _pill_dimensions(label)

    return cx, cy, pill_w, pill_h, seg_idx, is_vertical


LABEL_MARGIN = 4.0  # px margin between labels


def _label_bbox(cx: float, cy: float, pw: float, ph: float,
                is_vertical: bool) -> tuple[float, float, float, float]:
    """Return axis-aligned bounding box (x, y, w, h) for a pill label.

    For vertical segments the pill is rotated 90°, so its effective
    screen bbox swaps width and height.
    """
    if is_vertical:
        return (cx - ph / 2, cy - pw / 2, ph, pw)
    return (cx - pw / 2, cy - ph / 2, pw, ph)


def _bboxes_overlap(a: tuple[float, float, float, float],
                    b: tuple[float, float, float, float],
                    margin: float = LABEL_MARGIN) -> bool:
    """Check if two axis-aligned bounding boxes overlap (with margin)."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (ax - margin < bx + bw and bx - margin < ax + aw and
            ay - margin < by + bh and by - margin < ay + ah)


def _place_labels(candidates: list[dict]
                  ) -> list[tuple[float, float, float, float] | None]:
    """Place labels with collision avoidance.

    Each candidate dict has: waypoints, color, label.
    Returns a list parallel to candidates — either (x, y, w, h) screen bbox
    or None if the label was skipped.

    Strategy: for each candidate, try the midpoint of the longest segment.
    If it overlaps an already-placed label, slide along the segment in both
    directions until a clear spot is found or the segment is exhausted.
    """
    placed: list[tuple[float, float, float, float]] = []
    result: list[tuple[float, float, float, float] | None] = []

    for cand in candidates:
        info = _label_candidate(cand["waypoints"], cand["label"])
        if info is None:
            result.append(None)
            continue

        cx, cy, pw, ph, seg_idx, is_vert = info
        waypoints = cand["waypoints"]
        ax, ay = waypoints[seg_idx]
        bx, by = waypoints[seg_idx + 1]

        # Try midpoint first, then slide along the segment
        seg_dx = bx - ax
        seg_dy = by - ay
        seg_len = math.hypot(seg_dx, seg_dy)
        if seg_len < 0.5:
            result.append(None)
            continue
        ux, uy = seg_dx / seg_len, seg_dy / seg_len

        # Sliding range: from pill half-extent to seg_len minus half-extent
        if is_vert:
            half_extent = pw / 2  # rotated: pill width becomes vertical extent
        else:
            half_extent = pw / 2

        min_t = half_extent
        max_t = seg_len - half_extent
        if min_t > max_t:
            # Segment too short for the pill
            result.append(None)
            continue

        mid_t = seg_len / 2
        # Try positions: midpoint, then alternating offsets
        step = ph + LABEL_MARGIN  # step by pill height + margin
        offsets = [0.0]
        for k in range(1, 20):
            offsets.append(k * step)
            offsets.append(-k * step)

        best_bbox = None
        for offset in offsets:
            t = mid_t + offset
            if t < min_t or t > max_t:
                continue
            test_cx = ax + ux * t
            test_cy = ay + uy * t
            bbox = _label_bbox(test_cx, test_cy, pw, ph, is_vert)
            conflict = False
            for existing in placed:
                if _bboxes_overlap(bbox, existing):
                    conflict = True
                    break
            if not conflict:
                best_bbox = bbox
                break

        if best_bbox is not None:
            placed.append(best_bbox)
            result.append(best_bbox)
        else:
            result.append(None)

    return result


def _render_inline_label(waypoints: list[tuple[float, float]],
                         color: str, label: str,
                         bbox: tuple[float, float, float, float] | None = None
                         ) -> str | None:
    """Render an inline pill label on the wire's longest segment.

    If bbox is provided, use it for placement (from _place_labels).
    Otherwise fall back to midpoint placement (for single-wire use).
    Returns SVG string or None if the wire is too short for a label.
    """
    total = _path_length(waypoints)
    if total < WIRE_LABEL_THRESHOLD or not label:
        return None

    seg_idx, seg_len = _longest_segment(waypoints)
    if seg_len < 30:
        return None

    ax, ay = waypoints[seg_idx]
    bx, by = waypoints[seg_idx + 1]
    is_vertical = abs(bx - ax) < 0.5

    text = _truncate_label(label)
    pill_w, pill_h = _pill_dimensions(label)

    if bbox is not None:
        # Recover center from bbox
        bx_pos, by_pos, bw, bh = bbox
        if is_vertical:
            mx = bx_pos + bh / 2  # swapped for vertical
            my = by_pos + bw / 2
        else:
            mx = bx_pos + bw / 2
            my = by_pos + bh / 2
    else:
        mx, my = (ax + bx) / 2, (ay + by) / 2

    els = []
    if is_vertical:
        rx = mx - pill_w / 2
        ry = my - pill_h / 2
        els.append(
            f'<g transform="translate({mx:.1f},{my:.1f}) rotate(-90) '
            f'translate({-mx:.1f},{-my:.1f})">'
        )
        els.append(
            f'<rect x="{rx:.1f}" y="{ry:.1f}" '
            f'width="{pill_w:.1f}" height="{pill_h:.1f}" '
            f'rx="{pill_h / 2:.1f}" fill="{color}" opacity="0.9"/>'
        )
        els.append(
            f'<text x="{mx:.1f}" y="{my + WIRE_LABEL_FONT_SIZE * 0.35:.1f}" '
            f'text-anchor="middle" font-size="{WIRE_LABEL_FONT_SIZE}" '
            f'fill="white" font-weight="600" '
            f'font-family="{FONT}">{text}</text>'
        )
        els.append('</g>')
    else:
        rx = mx - pill_w / 2
        ry = my - pill_h / 2
        els.append(
            f'<rect x="{rx:.1f}" y="{ry:.1f}" '
            f'width="{pill_w:.1f}" height="{pill_h:.1f}" '
            f'rx="{pill_h / 2:.1f}" fill="{color}" opacity="0.9"/>'
        )
        els.append(
            f'<text x="{mx:.1f}" y="{my + WIRE_LABEL_FONT_SIZE * 0.35:.1f}" '
            f'text-anchor="middle" font-size="{WIRE_LABEL_FONT_SIZE}" '
            f'fill="white" font-weight="600" '
            f'font-family="{FONT}">{text}</text>'
        )

    return "\n".join(els)


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

    # MCU board bounding box for far-side routing
    mcu_bbox = Rect(*mcu.bbox)

    # Compute all paths first for crossing detection
    paths = []
    for i, spec in enumerate(specs):
        paths.append(_compute_path(spec.board_xy, spec.hole_xy, channels[i],
                                   board_bbox=mcu_bbox))

    # Detect crossings across all paths
    all_crossings = _detect_crossings(paths)

    # Group crossing points by path index
    path_crossings: dict[int, list[tuple[float, float]]] = {}
    for path_idx, _seg_idx, point in all_crossings:
        path_crossings.setdefault(path_idx, []).append(point)

    els = []
    for i, spec in enumerate(specs):
        crossing_pts = path_crossings.get(i, [])
        if crossing_pts:
            svg = _render_path_with_crossings(paths[i], spec.color, crossing_pts)
        else:
            svg = _render_path(paths[i], spec.color)
        if svg:
            els.append(svg)

    # Inline pill labels on long wires — with collision avoidance
    label_candidates = [
        {"waypoints": paths[i], "color": specs[i].color, "label": specs[i].label}
        for i in range(len(specs))
    ]
    placements = _place_labels(label_candidates)
    for i, spec in enumerate(specs):
        if placements[i] is not None:
            label_svg = _render_inline_label(
                paths[i], spec.color, spec.label, bbox=placements[i])
            if label_svg:
                els.append(label_svg)

    return els
