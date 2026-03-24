# Checkpoint

> Feature: board-renderer
> Last updated: 1774327598
> Plan hash: 76f8ec90

## Accomplished

### Session 9 (2026-03-21)

**HERO XL Board Renderer with Smart Wire Routing:**
- Created data-driven board definition system (`tools/bb/boards/hero-xl.yaml`) with all 86 pins from KiCad footprint data
- Built MCU board graphic renderer (`tools/bb/mcu.py`) — dark green PCB, USB-B, barrel jack, labeled pins with wired-pin highlighting
- Built channel-based orthogonal wire router (`tools/bb/router.py`) — H-V-H paths, crossing minimization via Y-sort, smooth arc bends
- Integrated into `generate()` — board graphic layer, wire partitioning (board-pin vs hole-to-hole), module-to-board-pin wire routing
- Configurable position (left/right) via `board_position:` YAML key or `--board-position` CLI arg
- Pill-label fallback preserved for unknown/absent boards
- All 20 acceptance criteria pass
- Code review: 6 concerns, 0 blocking — fixed 5 (docstring, type annotations, normalization helper, spacing guard, docs), backlogged 1 (obstacle avoidance)
- Security audit: PASS
- `_normalize_pin_id()` helper extracted to `bb/geometry.py` to eliminate triple normalization
- `docs/renderers.md` updated with board renderer documentation
- All 4 sketch SVGs regenerated, 36 wiring files validate

**Backlog specs created (4 total in `docs/specs/`):**
- `new-board-skill` — `/new-board` command for repeatable board onboarding with validation
- `regenerate-svgs` — Extract manual SVG regeneration loop into deterministic script
- `obstacle-avoidance` — Enforce wire routing around board body (collect_obstacles unused)
- `wire-routing-polish` — Wire spacing enforcement, inline pill labels for long runs, crossing visualization

## Current State

- **Branch:** main, clean (4 commits ahead of origin)
- **Build status:** all sketches compile, all SVGs regenerate
- **Validation:** 36 wiring files pass, test-renderers.py works
- **No failing tests**
- **No uncommitted changes**

## Next Steps

1. **Wire routing polish** (`wire-routing-polish` spec) — highest visual impact. The 004-joystick-lights diagram has wires bunched together and overlapping. Needs spacing enforcement and inline labels.
2. **Obstacle avoidance** (`obstacle-avoidance` spec) — wires to far-side pins clip through board body.
3. **Regenerate SVGs script** (`regenerate-svgs` spec) — quick deterministic win, extract the repeated for-loop.
4. **/new-board skill** (`new-board-skill` spec) — repeatable board onboarding process.

## Determinism Review

- **operations_reviewed:** 8
- **candidates_found:** 2
- **`for sketch in sketches/*/wiring.yaml` regeneration loop:** Claude ran this 3 times during the session. Should be `scripts/regenerate-svgs.sh`. Backlogged as `regenerate-svgs` spec. Impact: **high** (recurs every session that touches rendering).
- **Pin layout research via agent:** Used a general-purpose agent to look up Arduino Mega 2560 pin positions from KiCad footprint. Could become a deterministic script that parses `.kicad_mod` files into YAML. Backlogged as part of `new-board-skill` spec. Impact: **medium** (only recurs when onboarding new boards).
