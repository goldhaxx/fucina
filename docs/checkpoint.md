# Checkpoint

> Last updated: 2026-03-23
> Session objective: Deterministic SVG fix, README, backlog triage

## Accomplished

### Session 8 (2026-03-23)

**Deterministic SVG output:**
- Sorted `occupied_rows` set iteration in `render_row_connections` (`tools/bb/chrome.py:119`)
- Regenerated all 4 sketch SVGs — confirmed byte-identical across repeated runs
- Regenerated `ct-photoresistor/wiring.svg` to fix stale `fill="#silver"` (invalid SVG, rendered as black)
- Code review PASS, security audit PASS

**Project README:**
- Created `README.md` with inline SVG breadboard diagrams, progressive sketch table, tooling docs, quick start guide, project structure, and hardware table
- Acknowledgments section crediting inventrdotio/AdventureKit2 and Crafting Table
- Clone URL verified against `git remote` (goldhaxx/fucina)

### Session 7 (2026-03-23)

**breadboard.py modular split:**
- Split 1513-line monolith (48k chars) into 8 modules under `tools/bb/`
- `constants.py` (88 lines), `svg.py` (43), `loaders.py` (101), `geometry.py` (164), `board.py` (114), `renderers.py` (614), `chrome.py` (134), `legend.py` (190)
- `breadboard.py` remains as thin CLI entry + re-exports (186 lines)
- All SVGs verified byte-identical after split
- CLI (`python3 tools/breadboard.py`) and library API (`import breadboard as bb`) unchanged
- `test-renderers.py` backward compatibility preserved
- Fixed pre-existing bug: `#silver` → `silver` in render_sensor
- Fixed namespace leak: `_r`/`_i` loop vars → list comprehension in constants
- Updated `docs/renderers.md` to reference new module paths
- Code review PASS, security audit PASS, self-review PASS

### Session 6 (2026-03-22)

**Sketch 004 — Joystick Lights:**
- 5 LEDs + HW-504 joystick on HERO XL, 5 effects controlled by joystick position
- Effects: sync pulse (center), chase left/right (X-axis), random twinkle (up), ripple from center (down)
- Auto-calibration at startup, cubic intensity curves, hysteresis on zone transitions
- Compiled, uploaded, tested on hardware — all effects working

**HW-504 Joystick Onboarding + Module Renderer Overhaul:**
- Full HW-504 component onboarding (specs, inventory, wiring patterns)
- New `to:` pin format for modules, dynamic left margin, board pin pills
- All 23 module-containing SVGs regenerated

## Current State

- **Branch:** main, clean (5 commits ahead of origin)
- **Build status:** all sketches compile
- **Validation:** all wiring.yaml files pass
- **No failing tests**
- **No uncommitted changes**

## Next Steps

1. Add HERO XL board renderer to breadboard.py (Zach asked about this)
2. Next sketch ideas: button to cycle effects, combine joystick with buzzer for sound+light
3. Code reviewer flagged: no automated determinism regression test (generate twice, assert identical) — consider adding

## Context Notes

- Largest module is `tools/bb/renderers.py` at 614 lines / 22k chars — well under 40k threshold
- `_seven_segment_body_rows` lives in `geometry.py` (not renderers) to avoid circular imports
- Import graph is strictly one-directional: constants → svg → loaders → geometry → board → renderers/chrome → legend
- Set-ordering nondeterminism (item 3 from session 7) is now resolved

## Determinism Review

- **operations_reviewed:** 4
- **candidates_found:** 0
- No candidates this session. The sorted() fix itself was the determinism improvement. README creation is inherently stochastic (content generation).
