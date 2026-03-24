# Checkpoint

> Last updated: 2026-03-23
> Session objective: Split breadboard.py monolith into modular bb/ package

## Accomplished

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

- **Branch:** main, clean (1 commit ahead of origin)
- **Build status:** all sketches compile
- **Validation:** all wiring.yaml files pass
- **No failing tests**

## Next Steps

1. Consider adding HERO XL board renderer to breadboard.py (Zach asked about this)
2. Next sketch ideas: button to cycle effects, combine joystick with buzzer for sound+light
3. Consider sorting `board.occupied` set in `render_row_connections` for deterministic SVG output (observed set-ordering nondeterminism during regression testing)

## Context Notes

- Largest module is `tools/bb/renderers.py` at 614 lines / 22k chars — well under 40k threshold
- `_seven_segment_body_rows` lives in `geometry.py` (not renderers) to avoid circular imports
- Import graph is strictly one-directional: constants → svg → loaders → geometry → board → renderers/chrome → legend
