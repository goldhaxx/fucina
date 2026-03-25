"""Unit tests for wire routing — channel assignment, spacing, crossings, labels."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bb.router import WireSpec, _assign_channels, WIRE_SPACING, compute_mcu_gap
from bb.mcu import MCU_GAP


def _make_spec(board_y: float, hole_y: float,
               board_x: float = 50.0, hole_x: float = 200.0) -> WireSpec:
    """Helper — create a WireSpec with given Y positions."""
    return WireSpec(
        board_xy=(board_x, board_y),
        hole_xy=(hole_x, hole_y),
        color="#e53935",
        label="test wire",
        pin_id="pin1",
    )


# ─── Step 1: Interval-graph channel assignment (AC-9, AC-10) ────────


def test_overlapping_wires_get_different_channels_with_minimum_spacing():
    """Overlapping vertical segments must be separated by >= WIRE_SPACING."""
    # 7 wires all overlapping (simulates 004-joystick-lights) in a 30px gap.
    # Old algorithm compresses to 30/(7-1) = 5px but after padding = (30-10)/6 = 3.3px.
    # New algorithm must report these need 7 distinct channels at WIRE_SPACING apart.
    specs = [_make_spec(board_y=100 + i * 10, hole_y=300 + i * 10) for i in range(7)]
    # Narrow gap that can't fit 7 wires at WIRE_SPACING
    gap_start, gap_end = 100.0, 130.0
    channels = _assign_channels(specs, gap_start, gap_end)

    # All 7 wires overlap, so all channels must be distinct
    sorted_ch = sorted(channels)
    for i in range(1, len(sorted_ch)):
        spacing = sorted_ch[i] - sorted_ch[i - 1]
        assert spacing >= WIRE_SPACING - 0.01, (
            f"Channels {i-1} and {i} too close: {spacing:.1f}px < {WIRE_SPACING}px"
        )


def test_non_overlapping_wires_can_share_channels():
    """Non-overlapping vertical segments should reuse channels, needing fewer distinct positions."""
    # 4 wires in 2 non-overlapping groups:
    # Group A: board_y=100, hole_y=120 and board_y=110, hole_y=130 → overlap [110,120]
    # Group B: board_y=300, hole_y=320 and board_y=310, hole_y=330 → overlap [310,320]
    # Groups A and B don't overlap each other, so they can share channels.
    # Minimum channels needed: 2 (not 4).
    specs = [
        _make_spec(board_y=100, hole_y=120),  # Group A wire 1
        _make_spec(board_y=110, hole_y=130),  # Group A wire 2
        _make_spec(board_y=300, hole_y=320),  # Group B wire 1
        _make_spec(board_y=310, hole_y=330),  # Group B wire 2
    ]
    gap_start, gap_end = 100.0, 120.0  # Narrow gap — only room for ~2 channels
    channels = _assign_channels(specs, gap_start, gap_end)

    distinct = len(set(round(c, 1) for c in channels))
    assert distinct <= 3, (
        f"Non-overlapping groups should share channels — got {distinct} distinct, expected <= 3"
    )
    # But overlapping wires within each group must differ
    assert round(channels[0], 1) != round(channels[1], 1), "Group A wires must differ"
    assert round(channels[2], 1) != round(channels[3], 1), "Group B wires must differ"


def test_channel_count_minimum_half():
    """N wires get at least ceil(N/2) distinct channel positions (AC-10)."""
    # 8 wires — pairs that don't overlap can share
    specs = []
    for i in range(8):
        if i % 2 == 0:
            specs.append(_make_spec(board_y=100, hole_y=150))
        else:
            specs.append(_make_spec(board_y=300, hole_y=350))
    gap_start, gap_end = 80.0, 200.0
    channels = _assign_channels(specs, gap_start, gap_end)

    distinct = len(set(round(c, 1) for c in channels))
    expected_min = math.ceil(len(specs) / 2)
    assert distinct >= expected_min, (
        f"Expected >= {expected_min} distinct channels, got {distinct}"
    )


def test_channels_within_gap_when_gap_is_adequate():
    """When gap is wide enough for all channels, all positions stay in bounds."""
    specs = [_make_spec(board_y=100 + i * 20, hole_y=200 + i * 20) for i in range(5)]
    # 60px gap is enough for 5 wires at 5px spacing (20px span + centering)
    gap_start, gap_end = 100.0, 160.0
    channels = _assign_channels(specs, gap_start, gap_end)

    for i, ch in enumerate(channels):
        assert gap_start <= ch <= gap_end, (
            f"Channel {i} at {ch:.1f} outside gap [{gap_start}, {gap_end}]"
        )


def test_compute_mcu_gap_keeps_channels_in_bounds():
    """When compute_mcu_gap sizes the gap, all channels stay within it."""
    n = 10
    gap_size = compute_mcu_gap(n)
    specs = [_make_spec(board_y=50, hole_y=500) for _ in range(n)]
    gap_start = 100.0
    gap_end = gap_start + gap_size
    channels = _assign_channels(specs, gap_start, gap_end)

    for i, ch in enumerate(channels):
        assert gap_start <= ch <= gap_end, (
            f"Channel {i} at {ch:.1f} outside gap [{gap_start}, {gap_end}]"
        )


def test_single_wire():
    """Single wire gets centered channel."""
    specs = [_make_spec(board_y=100, hole_y=200)]
    gap_start, gap_end = 100.0, 160.0
    channels = _assign_channels(specs, gap_start, gap_end)

    assert len(channels) == 1
    expected_center = (gap_start + gap_end) / 2
    assert abs(channels[0] - expected_center) < 1.0, (
        f"Single wire at {channels[0]:.1f}, expected near center {expected_center:.1f}"
    )


# ─── Step 3: Minimum spacing enforcement (AC-1) ─────────────────────


def test_all_adjacent_channels_have_minimum_spacing():
    """No two adjacent channel X positions are closer than WIRE_SPACING (AC-1)."""
    # 10 wires, all overlapping — maximum channel pressure
    specs = [_make_spec(board_y=50, hole_y=500) for _ in range(10)]
    gap_start, gap_end = 50.0, 200.0
    channels = _assign_channels(specs, gap_start, gap_end)

    sorted_ch = sorted(set(round(c, 2) for c in channels))
    for i in range(1, len(sorted_ch)):
        spacing = sorted_ch[i] - sorted_ch[i - 1]
        assert spacing >= WIRE_SPACING - 0.01, (
            f"Adjacent channels {sorted_ch[i-1]:.1f} and {sorted_ch[i]:.1f} "
            f"only {spacing:.1f}px apart (min {WIRE_SPACING}px)"
        )


# ─── Step 2: Dynamic MCU gap (AC-2) ─────────────────────────────────


def test_dynamic_gap_returns_default_for_few_wires():
    """Small wire count fits in default MCU_GAP — no expansion needed."""
    gap = compute_mcu_gap(2)
    assert gap == MCU_GAP, f"Expected default gap {MCU_GAP}, got {gap}"


def test_dynamic_gap_widens_for_many_wires():
    """When wire count exceeds what fits at WIRE_SPACING, gap must widen."""
    # 10 all-overlapping wires need 10 channels at 5px = 45px between outermost
    # channels + padding on both sides. Default MCU_GAP (40) is too small.
    gap = compute_mcu_gap(10)
    min_needed = (10 - 1) * WIRE_SPACING + 2 * WIRE_SPACING  # 45 + 10 = 55
    assert gap >= min_needed, (
        f"Gap {gap} too small for 10 wires — need at least {min_needed}"
    )
    assert gap > MCU_GAP, f"Gap should exceed default {MCU_GAP}, got {gap}"


def test_dynamic_gap_grows_monotonically():
    """More wires should never produce a smaller gap."""
    prev = compute_mcu_gap(1)
    for n in range(2, 20):
        curr = compute_mcu_gap(n)
        assert curr >= prev, f"Gap shrank from {prev} (n={n-1}) to {curr} (n={n})"
        prev = curr


# ─── Step 4: Wire crossing detection and visualization (AC-3) ───────


def test_crossing_detection_finds_crossing_segments():
    """Two paths that cross should be detected by _detect_crossings."""
    from bb.router import _detect_crossings

    # Path A: horizontal at y=100, from x=50 to x=200
    # Path B: vertical at x=120, from y=50 to y=150
    # These cross at (120, 100).
    path_a = [(50.0, 100.0), (200.0, 100.0)]
    path_b = [(120.0, 50.0), (120.0, 150.0)]

    crossings = _detect_crossings([path_a, path_b])
    assert len(crossings) > 0, "Should detect crossing between perpendicular segments"
    # Each crossing: (path_index, segment_index, crossing_point)
    cx, cy = crossings[0][2]
    assert abs(cx - 120.0) < 1.0 and abs(cy - 100.0) < 1.0, (
        f"Crossing point should be near (120, 100), got ({cx:.1f}, {cy:.1f})"
    )


def test_no_crossing_for_parallel_segments():
    """Parallel segments should produce no crossings."""
    from bb.router import _detect_crossings

    path_a = [(50.0, 100.0), (200.0, 100.0)]
    path_b = [(50.0, 110.0), (200.0, 110.0)]

    crossings = _detect_crossings([path_a, path_b])
    assert len(crossings) == 0, f"Parallel segments shouldn't cross, got {crossings}"


def test_crossing_renders_bridge_gap():
    """A wire with a crossing should render with a gap at the crossing point."""
    from bb.router import _render_path_with_crossings

    # Simple horizontal path with a crossing in the middle
    waypoints = [(50.0, 100.0), (200.0, 100.0)]
    crossing_points = [(120.0, 100.0)]

    svg = _render_path_with_crossings(waypoints, "#e53935", crossing_points)
    # The SVG should contain multiple path segments (gap breaks the path)
    assert svg.count("<path") >= 2, (
        f"Expected >= 2 path segments for bridge gap, got {svg.count('<path')}"
    )


# ─── Step 5: Inline pill labels (AC-4, AC-5, AC-6, AC-7, AC-8) ─────


def test_long_wire_gets_inline_label():
    """Wire with path length > WIRE_LABEL_THRESHOLD gets an inline pill label (AC-4)."""
    from bb.router import _render_inline_label, WIRE_LABEL_THRESHOLD

    # Long horizontal path — well above threshold
    waypoints = [(50.0, 100.0), (300.0, 100.0)]
    total_length = 250.0
    assert total_length > WIRE_LABEL_THRESHOLD

    svg = _render_inline_label(waypoints, "#e53935", "red signal — Pin 9")
    assert svg is not None, "Long wire should get an inline label"
    assert "<rect" in svg, "Inline label should contain a pill (rect)"
    assert "<text" in svg, "Inline label should contain text"


def test_short_wire_no_inline_label():
    """Wire below WIRE_LABEL_THRESHOLD gets no inline label (AC-8)."""
    from bb.router import _render_inline_label, WIRE_LABEL_THRESHOLD

    # Short path — well below threshold
    waypoints = [(50.0, 100.0), (80.0, 100.0)]
    total_length = 30.0
    assert total_length < WIRE_LABEL_THRESHOLD

    svg = _render_inline_label(waypoints, "#e53935", "short wire")
    assert svg is None, "Short wire should not get an inline label"


def test_inline_label_uses_wire_color():
    """Pill label fill matches the wire's color (AC-7)."""
    from bb.router import _render_inline_label

    waypoints = [(50.0, 100.0), (300.0, 100.0)]
    color = "#43a047"
    svg = _render_inline_label(waypoints, color, "green signal")
    assert svg is not None
    assert color in svg, f"Pill fill should use wire color {color}"


def test_inline_label_text_from_wire_label():
    """Pill label displays the wire's label text (AC-5)."""
    from bb.router import _render_inline_label

    waypoints = [(50.0, 100.0), (300.0, 100.0)]
    label = "Pin 9 (PWM)"
    svg = _render_inline_label(waypoints, "#e53935", label)
    assert svg is not None
    assert "Pin 9" in svg, f"Label text should appear in SVG: {label}"


# ─── Step 5b: Label collision avoidance (AC-6) ─────────────────────


def test_labels_do_not_overlap():
    """Placed labels must not overlap each other (AC-6)."""
    from bb.router import _place_labels, WIRE_LABEL_THRESHOLD

    # 5 wires with long vertical segments at nearby X positions.
    # Midpoints would cluster — labels must be nudged apart.
    candidates = []
    for i in range(5):
        waypoints = [(100.0 + i * 5, 50.0), (100.0 + i * 5, 400.0)]
        candidates.append({
            "waypoints": waypoints,
            "color": "#e53935",
            "label": f"wire {i}",
        })

    placements = _place_labels(candidates)

    # Extract pill bounding boxes and check for overlaps
    MARGIN = 2.0
    for i in range(len(placements)):
        for j in range(i + 1, len(placements)):
            pi = placements[i]
            pj = placements[j]
            if pi is None or pj is None:
                continue
            # Check axis-aligned overlap with margin
            ix1, iy1, iw, ih = pi
            jx1, jy1, jw, jh = pj
            ix2, iy2 = ix1 + iw, iy1 + ih
            jx2, jy2 = jx1 + jw, jy1 + jh
            overlap_x = ix1 - MARGIN < jx2 and jx1 - MARGIN < ix2
            overlap_y = iy1 - MARGIN < jy2 and jy1 - MARGIN < iy2
            assert not (overlap_x and overlap_y), (
                f"Labels {i} and {j} overlap: "
                f"[{ix1:.0f},{iy1:.0f},{iw:.0f},{ih:.0f}] vs "
                f"[{jx1:.0f},{jy1:.0f},{jw:.0f},{jh:.0f}]"
            )


def test_label_skipped_when_no_clear_position():
    """If a label can't be placed without overlap, it should be skipped."""
    from bb.router import _place_labels

    # 10 wires all on the same short vertical segment — can't fit 10 labels
    candidates = []
    for i in range(10):
        waypoints = [(100.0, 50.0), (100.0, 120.0)]  # only 70px vertical
        candidates.append({
            "waypoints": waypoints,
            "color": "#e53935",
            "label": f"wire {i}",
        })

    placements = _place_labels(candidates)
    placed_count = sum(1 for p in placements if p is not None)
    # Can't fit all 10 on a 70px segment — some must be None
    assert placed_count < 10, (
        f"Expected some labels to be skipped, but all {placed_count} were placed"
    )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v", "-p", "no:anchorpy"]))
