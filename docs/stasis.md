# Checkpoint

> Feature: wire-routing-polish
> Last updated: 1774554827
> Plan hash: 05d8f20c

## Accomplished

### Session 10 (2026-03-26)

**Wire Routing Visual Polish — all 10 ACs complete:**
- Interval-graph channel assignment — greedy coloring ensures overlapping vertical segments get different channels; non-overlapping wires reuse channels (AC-9, AC-10)
- Dynamic MCU gap — `compute_mcu_gap()` widens the routing gap when wire count exceeds what fits at `WIRE_SPACING` (AC-2)
- Minimum spacing enforcement — channels are always `WIRE_SPACING` (5px) apart by construction (AC-1)
- Wire crossing bridge gaps — `_detect_crossings()` finds pairwise segment crossings; `_render_path_with_crossings()` splits the under-wire with a visible gap (AC-3)
- Inline pill labels — `_render_inline_label()` places colored pill labels on wires > 100px; `_place_labels()` resolves collisions by sliding along segments (AC-4–8)
- Code review: 1 blocking (bridge gap on wrong wire — fixed), 2 concerns (import order, gap clamp — fixed)

**Far-side pin routing (bonus — partially addresses obstacle-avoidance spec):**
- `_is_far_side()` detects pins on the opposite side of the board from the routing channel
- Far-side paths route vertically to clear the board top/bottom, then horizontally around the perimeter
- Per-wire perimeter spreading — `perimeter_index` offsets exit column (X) and clearance row (Y) so co-linear far-side wires run side-by-side
- Fixes A0/A1 overlap in 004-joystick-lights
- Fixes module wire direction — VRx now exits joystick pin rightward toward channel
- Updated `obstacle-avoidance` spec: AC-2 and AC-3 marked done

**Test suite:** 23 unit tests in `tools/bb/test_router.py`
**Validation:** 36 wiring files pass, 4 sketch SVGs regenerated, test-renderers output updated

### Session 9 (2026-03-21)

*(See previous checkpoint for board-renderer session details)*

## Current State

- **Branch:** `main`, clean — PR #1 merged
- **Spec status:** `wire-routing-polish` marked Complete
- **Build status:** all sketches compile, all SVGs regenerate
- **Validation:** 36 wiring files pass, test-renderers.py works
- **Tests:** 23 pass in `tools/bb/test_router.py`
- **No failing tests**

## Next Steps

1. **Regenerate SVGs script** (`regenerate-svgs` spec) — quick deterministic win, extract the `for sketch in sketches/*/wiring.yaml` loop.
2. **Obstacle avoidance remainder** (`obstacle-avoidance` spec) — AC-1 (formalize collect_obstacles call) and AC-4 (module card bbox as obstacle) still open. Low priority since the critical far-side routing is done.
3. **/new-board skill** (`new-board-skill` spec) — repeatable board onboarding.

## Determinism Review

- **operations_reviewed:** 6
- **candidates_found:** 1
- **`for sketch in sketches/*/wiring.yaml` regeneration loop:** Claude ran this 4 times during the session. Should be `scripts/regenerate-svgs.sh`. Already backlogged as `regenerate-svgs` spec from session 9. Impact: **high** (recurs every session that touches rendering).
