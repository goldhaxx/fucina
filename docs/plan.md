# Implementation Plan: Split breadboard.py into modular package

> Created: 2026-03-23
> Based on: Discussion — Option A (flat `tools/bb/` package)

## Objective

Refactor the monolithic `tools/breadboard.py` (1513 lines, 48.1k chars) into a `tools/bb/` package with 8 focused modules, keeping `tools/breadboard.py` as a thin CLI entry point — so no single file exceeds the 40k char context threshold.

## Constraints

- **CLI unchanged:** `python3 tools/breadboard.py <input> -o <output>` must keep working.
- **Library API unchanged:** `test-renderers.py` imports `breadboard as bb` and uses `bb.Board`, `bb.RENDERERS`, `bb._is_board_pin`, `bb.render_*`, `bb._text`, `bb._rect`, `bb.FONT`, `bb.HOLE_PITCH`, `bb.detect_row_range`, `bb.load_component_specs`, `bb._seven_segment_body_rows`. All must remain accessible via `import breadboard as bb`.
- **Zero behavior change:** Every SVG generated before and after must be byte-identical.

## Sequence

### Step 1: Capture baselines for regression testing

- **Test:** N/A (setup step)
- **Implement:** Generate SVGs from 3 representative sketches (simple, module, 7-segment) into `/tmp/baseline-*.svg`. These are the regression targets for all subsequent steps.
- **Files:** None (temp files only)
- **Verify:** Baselines exist and are valid SVGs

### Step 2: Create `bb/constants.py` — layout constants and color palettes

- **Test:** Import check from `tools/` directory.
- **Implement:** Extract layout constants (lines 21–79), band colors (lines 125–136), LED palette (lines 138–145), buzzer palette (lines 555–558) into `tools/bb/constants.py`. Create `tools/bb/__init__.py` (empty).
- **Files:** Create `tools/bb/__init__.py`, `tools/bb/constants.py`
- **Verify:** `python3 -c "from bb.constants import HOLE_PITCH, LED_PALETTE, BUZZER_PALETTE; print('OK')"`

### Step 3: Create `bb/svg.py` — SVG primitives and resistor bands

- **Test:** Import check.
- **Implement:** Extract `_attr`, `_circle`, `_rect`, `_line`, `_text`, `resistor_bands` (lines 422–461) into `tools/bb/svg.py`. Imports `BAND_DIGIT`, `BAND_MULTIPLIER`, `BAND_TOLERANCE_GOLD` from `bb.constants` and `escape` from `xml.sax.saxutils`.
- **Files:** Create `tools/bb/svg.py`
- **Verify:** `python3 -c "from bb.svg import _circle, _rect, _text, resistor_bands; print('OK')"`

### Step 4: Create `bb/loaders.py` — YAML loading and specs cache

- **Test:** Import check.
- **Implement:** Extract `load_circuit`, `load_component_specs`, `_SPECS_CACHE`, `_parse_yaml_simple`, `_coerce` (lines 148–240) into `tools/bb/loaders.py`. The `try: import yaml` block moves here. No dependencies on other `bb` modules.
- **Files:** Create `tools/bb/loaders.py`
- **Verify:** `python3 -c "from bb.loaders import load_circuit, load_component_specs; print('OK')"`

### Step 5: Create `bb/geometry.py` — orientation, row detection, pin utilities

- **Test:** Import check.
- **Implement:** Extract `parse_orientation`, `compute_rotated_fit` (lines 82–122), `_extract_row`, `detect_row_range` (lines 243–319), `_is_board_pin`, `_pin_label` (lines 1086–1097) into `tools/bb/geometry.py`. Also move `_seven_segment_body_rows` here (it's a dimension calculation, not a renderer — lines 780–796). Imports from `bb.constants` and `bb.loaders`.
- **Files:** Create `tools/bb/geometry.py`
- **Verify:** `python3 -c "from bb.geometry import detect_row_range, _is_board_pin, parse_orientation; print('OK')"`

### Step 6: Create `bb/board.py` — Board class

- **Test:** Import check.
- **Implement:** Extract class `Board` (lines 324–420) into `tools/bb/board.py`. Imports layout constants from `bb.constants`.
- **Files:** Create `tools/bb/board.py`
- **Verify:** `python3 -c "from bb.board import Board; b = Board(); print(b.hole_xy('a1'))"`

### Step 7: Create `bb/renderers.py` — component render functions

- **Test:** Import check.
- **Implement:** Extract all `render_*` component functions and their helpers: `render_resistor`, `render_led`, `render_button`, `render_buzzer`, `render_sensor`, `render_potentiometer`, `render_rgb_led`, `render_seven_segment`, `render_module`, `_seven_segment_digit`, `_module_box_width`, `_module_wire_color` (lines 464–1083, minus `_seven_segment_body_rows` which went to geometry). Imports from `bb.constants`, `bb.svg`, `bb.geometry`, `bb.board`.
- **Files:** Create `tools/bb/renderers.py`
- **Verify:** `python3 -c "from bb.renderers import render_resistor, render_led, render_module; print('OK')"`

### Step 8: Create `bb/chrome.py` — board background, rails, holes, labels

- **Test:** Import check.
- **Implement:** Extract `render_background`, `render_power_rails`, `render_holes`, `render_labels`, `render_row_connections` (lines 1232–1347) into `tools/bb/chrome.py`. Imports from `bb.constants`, `bb.svg`, `bb.geometry` (`_extract_row`).
- **Files:** Create `tools/bb/chrome.py`
- **Verify:** `python3 -c "from bb.chrome import render_background, render_holes; print('OK')"`

### Step 9: Create `bb/legend.py` — legend rendering, registry, wire rendering

- **Test:** Import check.
- **Implement:** Extract `RENDERERS` dict, all `_legend_*` functions, `render_wire`, `render_legend` (lines 1099–1228, 1349–1384) into `tools/bb/legend.py`. `RENDERERS` references render functions from `bb.renderers` and legend functions defined locally. Imports from `bb.constants`, `bb.svg`, `bb.geometry`.
- **Files:** Create `tools/bb/legend.py`
- **Verify:** `python3 -c "from bb.legend import RENDERERS, render_wire, render_legend; print('OK')"`

### Step 10: Rewrite `breadboard.py` as thin entry point + re-exports

- **Test:** Byte-diff SVGs against baselines from Step 1.
- **Implement:** Replace the 1513-line file with ~80 lines that: (1) re-exports all public names from `bb.*` so `import breadboard as bb` still exposes everything `test-renderers.py` needs, (2) defines `generate()` which orchestrates render layers (the current lines 1389–1482), (3) defines `main()` CLI (lines 1487–1513).
- **Files:** Rewrite `tools/breadboard.py`
- **Verify:** `python3 tools/breadboard.py sketches/001-blink/wiring.yaml -o /tmp/after.svg && diff /tmp/baseline-blink.svg /tmp/after.svg` (empty diff). Also: `python3 tools/test-renderers.py -o /tmp/test.svg` works.

### Step 11: Full regression — regenerate all SVGs and diff

- **Test:** Regenerate every wiring.svg in the project.
- **Implement:** Loop over all `wiring.yaml` files, regenerate SVGs, compare with `git diff`.
- **Files:** None (verification only)
- **Verify:** `git diff --stat` shows zero changes to `.svg` files. `python3 tools/test-renderers.py` also works.

### Step 12: Update documentation references

- **Test:** N/A (docs only)
- **Implement:** Update `docs/renderers.md` line 177 — currently says "add it to `tools/breadboard.py`", update to reference `tools/bb/renderers.py`. Grep for any other stale references that tell developers to edit the monolith.
- **Files:** `docs/renderers.md`
- **Verify:** No docs reference editing `tools/breadboard.py` for adding renderers.

## Circular Import Strategy

`detect_row_range` (geometry) calls `_seven_segment_body_rows`. Moving `_seven_segment_body_rows` to `bb/geometry.py` (it's a pure dimension lookup, not a renderer) eliminates the only potential circular dependency.

Import graph (all edges point one direction — no cycles):
```
constants ← svg ← board
    ↑        ↑      ↑
    └── loaders  geometry
              ↑      ↑
           renderers  chrome
              ↑        ↑
             legend ───┘
                ↑
           breadboard.py (generate + main + re-exports)
```

## Risks

- **`_seven_segment_body_rows` in geometry:** It reads `specs` dict. This is conceptually a geometry/dimension concern, not rendering, so the move is natural. But if future renderers need similar spec lookups, we'd want a shared pattern. Low risk — cross that bridge later.
- **test-renderers.py private name access:** It uses `bb._is_board_pin`, `bb._rect`, `bb._text`, etc. Re-exporting these from `breadboard.py` maintains compatibility. If we ever make `bb/` a public API, we'd formalize these — but that's out of scope.
- **sys.path resolution:** `test-renderers.py` inserts `tools/` into sys.path and imports `breadboard`. The `bb/` package lives in `tools/`, so `from bb.X` resolves correctly through the same sys.path entry.

## Definition of Done

- [ ] All 8 `bb/` modules created with correct imports
- [ ] `tools/breadboard.py` is <200 lines and under 10k chars
- [ ] No single file in `bb/` exceeds 40k chars (~1200 lines)
- [ ] `python3 tools/breadboard.py` CLI works identically
- [ ] `python3 tools/test-renderers.py` works identically
- [ ] All SVGs regenerated with zero byte-level diff
- [ ] `python3 tools/validate-wiring.py` still works
- [ ] Stale doc references updated
