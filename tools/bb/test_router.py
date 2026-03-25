"""Unit tests for wire routing — channel assignment, spacing, crossings, labels."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bb.router import WireSpec, _assign_channels, WIRE_SPACING


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


def test_channels_within_gap_bounds():
    """All channel positions must be within the routing gap."""
    specs = [_make_spec(board_y=100 + i * 20, hole_y=200 + i * 20) for i in range(5)]
    gap_start, gap_end = 100.0, 160.0
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


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v", "-p", "no:anchorpy"]))
