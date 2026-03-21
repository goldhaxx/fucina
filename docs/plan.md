# Implementation Plan: Component Orientation & Rendering System

> Created: 2026-03-21
> Based on: 7-segment fix session learnings + user feedback

## Objective

Introduce a first-principles component rendering architecture where components are defined in their natural (datasheet) coordinate system, transformed automatically for breadboard placement, and verifiable via visual test fixtures — eliminating multi-hour debugging sessions per component.

## Core Concepts

**Natural orientation:** How the component looks face-on per its datasheet. Width, height, aspect ratio, feature positions (DP, labels, pins) are all defined in this space. This never changes.

**Board orientation:** How the component sits on the breadboard after rotation. Derived automatically from the natural orientation + a rotation angle. The renderer builds in natural space, then applies one transform.

**The contract:** Every renderer draws its content in a local coordinate system centered at (0, 0), sized by datasheet-derived dimensions. The framework handles translation to the board position and rotation for breadboard placement. The renderer never needs to know where it is on the board or which way it faces.

## Sequence

### Step 1: Create visual test fixture script

- **Test:** Run `python3 tools/test-renderers.py` — generates a single SVG with every component type rendered at multiple sizes with red bounding boxes showing expected containment.
- **Implement:** Create `tools/test-renderers.py` that builds a synthetic `circuit` dict containing one of each component type, calls `generate()`, and writes a test SVG. Include red outline rects at each component's expected bounds for visual regression.
- **Files:** `tools/test-renderers.py` (new)
- **Verify:** Open the output SVG — every component should be visible, within its red bounds, with no clipping or overflow.

### Step 2: Extract renderer registry and dispatch cleanup

- **Test:** Existing `generate()` dispatch still works — all 32 sketch SVGs produce identical output.
- **Implement:** In `breadboard.py`:
  1. Create a `RENDERERS` dict mapping type strings to `(render_fn, legend_fn)` tuples, replacing the if-elif chains in `generate()` and `render_legend()`.
  2. Each render function signature stays `(board, comp) -> list[str]`.
  3. Adding a new component type becomes: define the function + add one entry to `RENDERERS`.
- **Files:** `tools/breadboard.py`
- **Verify:** Regenerate all 32 SVGs, diff against previous — zero visual changes.

### Step 3: Add `orientation` key to wiring.yaml schema

- **Test:** Existing wiring.yaml files without `orientation` still parse and render correctly (default = component-specific).
- **Implement:**
  1. Add optional `orientation` key to the component schema. Values: `top-left`, `top-right`, `bottom-left`, `bottom-right` — indicating which direction the component's natural "top" faces in the diagram. Default varies by type (e.g., `top-left` for DIP packages = top faces toward column a).
  2. Parse `orientation` in `generate()` and pass it through to renderers.
  3. Document the orientation model and defaults in `docs/renderers.md`.
- **Files:** `tools/breadboard.py`, `docs/renderers.md`, `.claude/rules/sketches.md`
- **Verify:** All sketches still generate identical SVGs (no orientation keys added yet, defaults match current behavior).

### Step 4: Refactor seven_segment to use the orientation model

- **Test:** `ct-7seg-1digit`, `ct-7seg-4digit`, and `ct-alarm-clock` produce identical SVGs before and after refactor.
- **Implement:**
  1. Factor `render_seven_segment` into two parts:
     - `_seven_segment_natural(digits, digit_w, digit_h, sw)` → returns SVG elements in natural (upright) coords, centered at origin. Pure geometry — no board awareness.
     - `render_seven_segment(board, comp)` → computes bounds, calls the natural renderer, wraps output in a `<g transform="translate(...) rotate(...)">` based on `orientation`.
  2. The natural renderer draws the digit face, segments, and DP — exactly what the current code does inside the `for d in range(digits)` loop.
  3. Move the sizing constraint math (aspect ratio, skew budget, stroke cap) into a `_seven_segment_size(body_w, body_h, digits, rotation)` helper that returns `(digit_w, digit_h, sw)`.
- **Files:** `tools/breadboard.py`
- **Verify:** Regenerate the 3 seven-segment SVGs — identical output. Run `tools/test-renderers.py` — seven_segment shows within bounds.

### Step 5: Generalize the sizing framework for future components

- **Test:** A new hypothetical component using the framework renders correctly with different orientations.
- **Implement:**
  1. Create a `compute_rotated_fit(natural_w, natural_h, container_w, container_h, rotation_deg, fill=0.90)` utility that returns the max scale factor for a natural-orientation rectangle to fit inside a container after rotation. This generalizes the constraint math from seven_segment.
  2. Document the sizing framework in `docs/renderers.md` under a new "Renderer Development Guide" section: how to derive natural dimensions from a datasheet, how fill/rotation/containment interact.
- **Files:** `tools/breadboard.py`, `docs/renderers.md`
- **Verify:** The seven_segment renderer uses `compute_rotated_fit()` and produces identical output. The test fixture exercises the utility with multiple rotations.

### Step 6: Add datasheet dimension comments to all existing renderers

- **Test:** All 32 sketch SVGs still produce identical output.
- **Implement:** For each renderer that currently uses hardcoded sizes (button, buzzer, sensor, potentiometer, rgb_led), add comments documenting:
  1. What the natural dimensions should be (from datasheet or measurement)
  2. What the current hardcoded values are and why
  3. Whether the component needs orientation support (most don't — symmetric or always placed the same way)
- **Files:** `tools/breadboard.py`
- **Verify:** No functional changes — comments only. Run test fixture to confirm.

### Step 7: Update documentation and rules

- **Test:** N/A (docs only)
- **Implement:**
  1. Update `docs/renderers.md`:
     - Add "Orientation Model" section explaining natural vs board orientation
     - Add "Renderer Development Guide" section with the process for creating a new renderer
     - Update the `seven_segment` entry with the new `orientation` key
     - Add standard DIP widths table (0.3", 0.5", 0.6")
  2. Update `.claude/rules/sketches.md`:
     - Add `orientation` to the wiring.yaml schema section
     - Document defaults per component type
  3. Update `.claude/rules/components.md`:
     - Add "Orientation" to the checklist for new components
  4. Update `CLAUDE.md` architecture tree to include `tools/test-renderers.py`
  5. Update `GUIDE.md` node-specific section if any commands changed
- **Files:** `docs/renderers.md`, `.claude/rules/sketches.md`, `.claude/rules/components.md`, `CLAUDE.md`
- **Verify:** Read through docs for consistency. Run test fixture as final smoke test.

## Risks

- **Regression in existing SVGs:** Every step that touches `breadboard.py` must regenerate all 32 SVGs and diff. The test fixture catches visual regressions early.
- **Over-engineering:** Most components (resistor, LED, button) are symmetric or pin-position-derived — they don't need orientation support. The plan explicitly scopes orientation to DIP/module types that benefit from it.
- **Naming confusion:** "natural" vs "board" orientation could confuse. The docs must be clear with concrete examples (e.g., "The 5161AS is 12.6mm wide × 19mm tall in natural orientation. On the breadboard, it rotates -90° so the 19mm dimension runs horizontally.").

## Definition of Done

- [x] `tools/test-renderers.py` generates a visual test SVG with all 9 component types
- [x] `RENDERERS` registry replaces if-elif dispatch in `generate()` and `render_legend()`
- [x] `orientation` key documented in wiring.yaml schema with per-type defaults
- [x] `render_seven_segment` factored into natural renderer + orientation transform
- [x] `compute_rotated_fit()` utility available for future renderer development
- [x] `docs/renderers.md` has Orientation Model and Renderer Development Guide sections
- [x] All 32 existing sketch SVGs are unchanged (visual regression check)
- [x] Rules updated: `sketches.md`, `components.md`
