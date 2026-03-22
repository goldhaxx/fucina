# Implementation Plan: Component Specs Registry with Validation

> Created: 2026-03-21
> Based on: Option C discussion — specs registry + validation

## Objective

Create a machine-readable component specs file (`docs/component-specs.yaml`) as the single source of truth for physical dimensions, wire renderers to read from it via a `model` key in wiring.yaml, update `/new-component` to populate it, and add validation that catches dimension mismatches before they become wrong diagrams.

## Core Concepts

**Why this exists:** Physical dimensions are properties of a *part number*, not a *sketch*. A 5641AS is 50.3mm wide whether it's in the alarm clock or the counter. Hardcoding dimensions in renderer logic (like `BODY_MM = {1: 12.60, 4: 50.30}`) breaks this — the renderer "knows" about specific parts instead of reading from data.

**The flow:**
1. `/new-component` researches a datasheet → writes structured specs to `docs/component-specs.yaml`
2. `wiring.yaml` references the part via `model: 5641AS`
3. `breadboard.py` loads the specs file, looks up the model, uses exact dimensions
4. `validate-wiring.py` cross-checks every wiring.yaml against the specs file and flags problems

## Sequence

### Step 1: Create `docs/component-specs.yaml` and seed with existing components

- **Test:** The file parses as valid YAML. Every component that has a dedicated renderer type has an entry with at minimum `body_mm`, `pins`, and `pin_pitch_mm`.
- **Implement:**
  1. Create `docs/component-specs.yaml` with a clear schema comment header.
  2. Seed entries for the two components we already have datasheet dimensions for: `5161AS` (1-digit 7-seg) and `5641AS` (4-digit 7-seg).
  3. Research datasheets and add entries for ALL other components currently in `docs/inventory.md` that sit on the breadboard: resistors (generic axial), LEDs (5mm), tactile buttons (6mm), buzzers (12mm cylinder), potentiometers (vertical trimmer), RGB LEDs (5mm), KY-series sensor modules. Off-board modules (`type: module`) don't need physical specs since they render as labeled boxes.
  4. Each entry includes: `body_mm` (dimensions), `pins`, `pin_pitch_mm`, `datasheet` URL where available, and renderer-specific fields (e.g., `digit_face_mm`, `slant_deg` for 7-segment displays).
- **Files:** `docs/component-specs.yaml` (new)
- **Verify:** `python3 -c "import yaml; yaml.safe_load(open('docs/component-specs.yaml'))"` succeeds. Spot-check 3-4 entries against their datasheets.

### Step 2: Add `load_component_specs()` to breadboard.py

- **Test:** `load_component_specs()` returns a dict keyed by model string. When the file is missing, returns empty dict (graceful fallback). When the file exists, all seeded entries are present.
- **Implement:**
  1. Add `load_component_specs(path=None) -> dict` to `breadboard.py`. Default path is `docs/component-specs.yaml` relative to the YAML input file's location (walk up to find it), or relative to CWD.
  2. The function caches its result (module-level `_SPECS_CACHE`) so it's only loaded once per process.
  3. Add a `specs` parameter to `generate()` that accepts a pre-loaded specs dict (for testing) or loads on demand.
- **Files:** `tools/breadboard.py`
- **Verify:** Unit test in `tools/test-renderers.py` — call `load_component_specs()` and assert expected keys exist.

### Step 3: Add `model` key to wiring.yaml schema and update seven_segment renderer

- **Test:** A wiring.yaml with `model: 5641AS` on a seven_segment component produces the same SVG as the current hardcoded behavior. A wiring.yaml *without* `model` still works (backward compatible).
- **Implement:**
  1. In `render_seven_segment()`, if `comp` has a `model` key, look up the model in the specs dict to get `body_mm[0]` (body length). Replace `_seven_segment_body_rows(digits)` with a lookup that prefers specs data, falls back to the hardcoded dict.
  2. Thread the `specs` dict through from `generate()` to renderer calls — either via a new parameter on render functions, or by storing it on the `Board` object.
  3. Update `sketches.md` schema to document the `model` key.
- **Files:** `tools/breadboard.py`, `.claude/rules/sketches.md`
- **Verify:** Update the 3 seven_segment wiring.yaml files to add `model: 5641AS` / `model: 5161AS`. Regenerate SVGs — output must be identical to current.

### Step 4: Update wiring.yaml files with model keys

- **Test:** All wiring.yaml files that reference components with known part numbers have `model` keys. All SVGs regenerate identically.
- **Implement:**
  1. Audit all `wiring.yaml` files. For every component entry where we know the exact part number (from inventory), add the `model` key.
  2. For generic components (e.g., "220Ω resistor" where no specific part number exists), use a generic model identifier like `axial-resistor` or `led-5mm` that maps to the generic specs in `component-specs.yaml`.
- **Files:** All `wiring.yaml` files across `sketches/`
- **Verify:** Regenerate all SVGs — no visual changes.

### Step 5: Create `tools/validate-wiring.py`

- **Test:** Run against the current sketches — all pass. Introduce a deliberate error (wrong pin count) — validation catches it.
- **Implement:**
  1. Create `tools/validate-wiring.py` that:
     - Scans `sketches/` for all `wiring.yaml` files
     - Loads `docs/component-specs.yaml`
     - For each component with a `model` key, cross-checks:
       - `pins` count matches specs
       - `row_start` + pin span doesn't exceed breadboard rows
       - Component type in wiring.yaml matches expected renderer type in specs (if specified)
     - For each component *without* a `model` key, warns: "No model specified — physical dimensions not validated"
     - Prints PASS/WARN/FAIL per sketch with a summary
  2. Exit code 0 if all pass, 1 if any fail (for CI use).
- **Files:** `tools/validate-wiring.py` (new)
- **Verify:** Run against all sketches — clean pass. Temporarily corrupt one wiring.yaml, confirm failure is caught, restore.

### Step 6: Update `/new-component` to populate specs file

- **Test:** N/A (command prompt, not code).
- **Implement:**
  1. Add a new **Phase 1.5: Physical Specs** to `.claude/commands/new-component.md` between Research and Inventory:
     - After researching the component, extract physical dimensions from the datasheet
     - Write a structured entry to `docs/component-specs.yaml` with all measured dimensions
     - This is mandatory for components that sit on the breadboard (DIP, through-hole, on-board modules)
     - Optional for off-board modules (servos, LCDs connected via jumper wires)
  2. Update Phase 4 (Sketch Creation) to require `model` key in wiring.yaml, referencing the specs entry.
  3. Add a validation step to Phase 5: run `python3 tools/validate-wiring.py sketches/NNN-name/wiring.yaml` before compiling.
- **Files:** `.claude/commands/new-component.md`
- **Verify:** Read through the updated command and trace the flow mentally — specs file gets populated, model key gets used, validation runs.

### Step 7: Update rules and documentation

- **Test:** N/A (docs only).
- **Implement:**
  1. Update `.claude/rules/components.md`:
     - Add "Check `docs/component-specs.yaml` for an existing physical specs entry" to the pre-code checklist
     - Add "If missing, add specs entry with datasheet dimensions" to the new-component section
     - Add "After writing wiring.yaml, run `python3 tools/validate-wiring.py` to verify" to the physical accuracy section
  2. Update `docs/renderers.md` Renderer Development Guide:
     - Step 1 now says "Add dimensions to `docs/component-specs.yaml`" not just "look up the datasheet"
     - Add note that renderers should read from specs dict, not hardcode dimensions
  3. Update `CLAUDE.md`:
     - Add `docs/component-specs.yaml` to the architecture tree
     - Add `validate-wiring.py` to the tools tree and commands section
  4. Update node-specific section of `GUIDE.md`:
     - Add `validate-wiring.py` to the utility commands table
     - Update the `/new-component` description to mention specs population

- **Files:** `.claude/rules/components.md`, `docs/renderers.md`, `CLAUDE.md`, `GUIDE.md`
- **Verify:** Read through all updated docs for consistency. Run test fixture and validator as final smoke test.

## Risks

- **Specs file scope creep:** Not every component needs mm-level physical specs. Off-board modules (servo, LCD, RFID reader) render as labeled boxes — their physical size doesn't matter for the diagram. The specs file should only contain entries for components that physically sit on the breadboard.
- **Backward compatibility:** Existing wiring.yaml files without `model` keys must continue to work. The specs lookup must be optional with graceful fallback to current behavior.
- **Research effort for Step 1:** Seeding specs for all existing components requires finding datasheets for ~8 component types. Some (generic resistors, LEDs) may not have a single canonical datasheet — use typical/standard dimensions.
- **Specs dict threading:** Passing the specs dict to every renderer call is a design choice. Storing on `Board` or using a module global are alternatives — pick the simplest that doesn't pollute the API.

## Definition of Done

- [ ] `docs/component-specs.yaml` exists with entries for all breadboard-sitting component types
- [ ] `breadboard.py` loads specs and uses them for body sizing (seven_segment as proof of concept)
- [ ] `model` key documented in wiring.yaml schema, used in all seven_segment entries
- [ ] `tools/validate-wiring.py` validates all wiring.yaml files against specs
- [ ] `/new-component` command updated to populate specs file
- [ ] Rules and docs updated: `components.md`, `renderers.md`, `CLAUDE.md`, `GUIDE.md`
- [ ] All existing SVGs unchanged (or intentionally improved with more accurate dimensions)
- [ ] Validator passes on all existing sketches
