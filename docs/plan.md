# Implementation Plan: Wire Routing Visual Polish — Spacing and Labels

> Feature: wire-routing-polish
> Created: 1774403546
> Spec hash: 0b1d7a18
> Based on: docs/spec.md

## Objective

Improve wire routing visual quality by enforcing minimum spacing between parallel wire segments, adding crossing indicators, inline pill labels on long wires, and smarter channel assignment that respects vertical overlap.

## Analysis

### Current State
- `_assign_channels()` sorts wires by destination Y, spaces evenly across the gap
- Spacing is clamped to `WIRE_SPACING` (5px) max — but with many wires the channels compress to < 5px
- No crossing detection or visualization
- No inline labels — wires are only identifiable by color + legend
- Channel assignment doesn't consider whether vertical segments actually overlap

### Key Insight
The routing gap between MCU board and breadboard is fixed at `MCU_GAP = 40px`. With 7 board-pin wires in 004-joystick-lights, channels compress to ~5px spacing. If we need more space, `MCU_GAP` must grow dynamically. This affects `McuBoard.__init__()` positioning and `generate()` margin calculation.

## Sequence

### Step 1: Interval-graph channel assignment (AC-9, AC-10)
- **Test:** Python unit test — two wires whose vertical segments overlap must get different channels; two wires whose vertical segments don't overlap can share a channel. Test that N wires get at least `ceil(N/2)` distinct positions.
- **Implement:** Replace Y-sort channel assignment with an interval-graph greedy algorithm: each wire's vertical segment is an interval `[min_y, max_y]`. Greedily assign the lowest available channel that doesn't conflict with any overlapping interval already in that channel.
- **Files:** `tools/bb/router.py` — rewrite `_assign_channels()`
- **Verify:** Unit test passes. Regenerate 004-joystick-lights SVG, visually confirm wires are separated.

### Step 2: Dynamic MCU gap (AC-2)
- **Test:** Python unit test — when wire count exceeds what fits at `WIRE_SPACING` in the default gap, the returned gap is wider than `MCU_GAP`.
- **Implement:** Add `compute_mcu_gap(wire_count: int) -> float` that returns `max(MCU_GAP, (wire_count + 1) * WIRE_SPACING + 2 * WIRE_SPACING)`. Wire this into `generate()` margin calculation and `McuBoard` positioning.
- **Files:** `tools/bb/router.py` (new function), `tools/bb/mcu.py` (use dynamic gap), `tools/breadboard.py` (pass wire count to gap calculation)
- **Verify:** Unit test passes. 004-joystick-lights SVG has wider gap when needed.

### Step 3: Minimum spacing enforcement (AC-1)
- **Test:** Python unit test — given assigned channels, assert no two adjacent channels are closer than `WIRE_SPACING` apart.
- **Implement:** After interval-graph assignment, post-process channel positions to enforce `WIRE_SPACING` minimum. If the gap is too narrow (shouldn't happen after Step 2), fall back to even distribution.
- **Files:** `tools/bb/router.py`
- **Verify:** Unit test passes. All sketch SVGs regenerate without visual overlap.

### Step 4: Wire crossing detection and visualization (AC-3)
- **Test:** Python unit test — given two wire paths that cross, the render output contains a crossing indicator (small white gap in the under-wire).
- **Implement:** After computing all paths, detect pairwise segment crossings. For each crossing, insert a small gap (3px break) in the wire that was routed later (lower z-order). Render crossing wires with a path break at the crossing point.
- **Files:** `tools/bb/router.py` — add `_detect_crossings()` and modify `_render_path()`
- **Verify:** Unit test passes. Visual check on multi-wire sketches.

### Step 5: Inline pill labels on long wires (AC-4, AC-5, AC-6, AC-7, AC-8)
- **Test:** Python unit test — wire with path length > threshold gets an inline label SVG element; wire below threshold does not. Label text matches wire label from YAML.
- **Implement:** After path computation, calculate total path length. For wires > `WIRE_LABEL_THRESHOLD` (100px), find the longest segment, place a pill label at its midpoint. Pill uses wire color fill + white text (matching legend style). Shift label along segment if it would overlap another label (greedy placement).
- **Files:** `tools/bb/router.py` — add `_render_inline_label()`, `tools/bb/constants.py` — add `WIRE_LABEL_THRESHOLD`
- **Verify:** Unit test passes. 004-joystick-lights SVG shows inline labels on long wires. Short wires have no labels.

### Step 6: Integration verification and SVG regeneration
- **Test:** Run `python3 tools/validate-wiring.py` on all sketches. Run `python3 tools/test-renderers.py`.
- **Implement:** Regenerate all sketch SVGs. Fix any visual regressions.
- **Files:** `sketches/*/wiring.svg`
- **Verify:** All validation passes. Visual inspection of all 4 sketches.

## Risks

- **Dynamic gap changes SVG dimensions:** All downstream sketch SVGs will change dimensions. This is expected — regeneration handles it.
- **Crossing detection performance:** Pairwise segment comparison is O(N^2 x segments). With < 20 wires this is negligible.
- **Label overlap in dense regions:** Greedy shift may not always find a clear spot. Mitigation: if no clear position exists within the segment, skip the label for that wire (graceful degradation).
- **Interval-graph channel reuse:** Allowing non-overlapping wires to share channels reduces the number of distinct channels needed — but may confuse viewers if wires at different Y ranges share the same X column. Mitigation: preserve Y-sort tiebreaking within each channel so visual flow is maintained.

## Definition of Done

- [ ] All 10 acceptance criteria from spec pass
- [ ] All existing sketches regenerate without errors
- [ ] `validate-wiring.py` passes on all 36 wiring files
- [ ] `test-renderers.py` generates valid output
- [ ] Code reviewed (run /review)
