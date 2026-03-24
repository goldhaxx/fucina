# Implementation Plan: HERO XL Board Renderer with Smart Wire Routing

> Feature: board-renderer
> Created: 1774322118
> Spec hash: c932c3e2
> Based on: docs/spec.md

## Objective

Render a visual HERO XL board graphic alongside the breadboard in SVG diagrams, with smart-routed orthogonal wires connecting board pins to breadboard holes — replacing the current pill-label system.

## Constraints

- **CLI unchanged** except adding optional `--board-position` arg.
- **Fallback preserved:** when `board:` is absent or unknown, pill-labels still work.
- **Wire colors preserved:** routed wires use the same colors from `wiring.yaml`.
- **Hole-to-hole wires untouched:** smart routing only for wires with board pin endpoints.
- **Data-driven boards:** pin layout in YAML, not hardcoded in Python.

## Architecture Overview

```
boards/hero-xl.yaml  →  boards/__init__.py (load_board)
                              ↓
                         mcu.py (render_board → SVG elements)
                              ↓
breadboard.py generate()  ←→  router.py (route_wires → SVG paths)
                              ↑
                         legend.py / renderers.py (delegate board-pin wires)
```

The board graphic and router are new modules. Integration into `generate()` adds two layers: board chrome (before components) and routed wires (replacing pill-label wires). The existing `Board` class gains a `board_position` attribute and adjusts margins accordingly.

### Scale and Positioning

The board graphic uses the same scale as the breadboard: `HOLE_PITCH` (14px) = 2.54mm, so 1mm ≈ 5.51px. The HERO XL board (101.52mm × 53.34mm) renders as approximately 560px × 294px in SVG.

When positioned on the left (default), the layout is:
```
[Module cards] [Board graphic] [routing gap] [Breadboard]
```

The breadboard `Board` class gets an expanded left margin to accommodate the board graphic. Module cards reposition to the left of the MCU board.

### Wire Routing Strategy

**Channel-based orthogonal routing** in the gap between the board graphic and the breadboard:

1. Each board-pin wire exits the board horizontally into the routing gap.
2. In the gap, wires are assigned to **vertical channels** — evenly-spaced pixel offsets.
3. Each wire runs vertically along its channel to align with the destination row.
4. The wire exits the channel horizontally into the breadboard hole.

**Crossing minimization:** Sort wires so that the mapping from board pin Y-positions to breadboard row Y-positions preserves order where possible. Specifically: sort wire assignments so that wires whose board pins are higher go to channels nearer the breadboard when their destination rows are also higher, and vice versa. This is a classic "minimum crossings in bipartite graph" problem — a greedy sort by destination Y handles the common case.

**Smooth bends:** Each wire is rendered as an SVG `<path>` with small arc commands (`A`) at the two 90° turns, giving visually smooth rounded corners.

## Sequence

### Phase 1 — Data Foundation

#### Step 1: Board data file — HERO XL pin layout

- **Test:** `python3 -c "import yaml; d = yaml.safe_load(open('tools/bb/boards/hero-xl.yaml')); assert 'headers' in d"`
- **Implement:** Create `tools/bb/boards/hero-xl.yaml` encoding the Arduino Mega 2560 Rev3 physical pin layout: board dimensions (mm), each header group (name, position, pin list with names and mm offsets), connector positions (USB-B, DC jack), and display name. Pin positions derived from the official Arduino Mega 2560 Rev3 board drawing (2.54mm pitch, header positions in mm from board origin at top-left corner, USB end).
- **Files:** Create `tools/bb/boards/hero-xl.yaml`
- **Verify:** YAML parses successfully; has `name`, `dimensions_mm`, `headers`, `connectors` keys; header pin counts match Mega 2560 spec (54 digital + 16 analog + power/comm pins).

#### Step 2: Board data loader

- **Test:** `python3 -c "from bb.boards import load_board; b = load_board('hero-xl'); assert b['name']"`; also test that `load_board('nonexistent')` returns `None`.
- **Implement:** Create `tools/bb/boards/__init__.py` with `load_board(name: str) -> dict | None`. Searches `tools/bb/boards/<name>.yaml` relative to the package directory. Returns parsed YAML dict or `None` if not found.
- **Files:** Create `tools/bb/boards/__init__.py`
- **Verify:** Loads hero-xl successfully; returns None for unknown boards.

### Phase 2 — Board Graphic Renderer

#### Step 3: McuBoard coordinate mapper

- **Test:** Instantiate `McuBoard` from hero-xl data + board position. Verify `pin_xy("9")` returns a valid (x, y) tuple. Verify `pin_xy("A0")` differs from `pin_xy("9")`. Verify all pins in the data file resolve without error.
- **Implement:** Create `tools/bb/mcu.py` with `McuBoard` class. Constructor takes board data dict, position (`"left"` | `"right"`), and the breadboard `Board` instance for alignment. Converts mm pin positions to pixel coordinates using `HOLE_PITCH / 2.54` scale factor. Stores the board graphic bounding box (`bbox: tuple[float, float, float, float]` — x, y, w, h) for obstacle avoidance. Provides `pin_xy(pin_name: str) -> tuple[float, float]` for looking up any pin by its canonical name (e.g., `"9"`, `"A0"`, `"GND"`, `"5V"`). Also provides `wired_pins: set[str]` populated later by `generate()`.
- **Files:** Create `tools/bb/mcu.py`
- **Verify:** All pins from hero-xl.yaml resolve to coordinates; bbox is positive and non-degenerate.

#### Step 4: Board graphic — outline, connectors, and name label

- **Test:** Call `render_board_outline(mcu_board)` → list of SVG strings. Verify output contains `<rect` (board body), text with board name, and elements for USB-B and DC jack connectors.
- **Implement:** Add `render_board_outline(mcu: McuBoard) -> list[str]` to `mcu.py`. Renders: dark green PCB rectangle with rounded corners and shadow, USB-B connector (small rectangle on one short edge), DC barrel jack (small circle on same edge), board name label (centered, white text). The board is oriented vertically when positioned left/right (rotated 90° from natural — USB at top, digital pins facing breadboard).
- **Files:** `tools/bb/mcu.py`
- **Verify:** SVG elements parse correctly; visual check via test-renderers.

#### Step 5: Board graphic — pin headers with labels

- **Test:** Call `render_board_pins(mcu_board)` → list of SVG strings. Verify output contains: a `<circle` for each pin in the data file, a `<text` label for each pin, and that wired pins (in `mcu.wired_pins`) have a distinct fill color from unwired pins.
- **Implement:** Add `render_board_pins(mcu: McuBoard) -> list[str]` to `mcu.py`. Iterates all headers and pins. Each pin gets a small circle at its pixel position (r=2) and a text label (font-size 6px). Pin fill: gold/highlighted for wired pins, dim gray for unwired. Label positioning: inside the board body, offset from the pin hole. Headers get subtle group labels (e.g., "DIGITAL", "ANALOG", "POWER").
- **Files:** `tools/bb/mcu.py`
- **Verify:** Pin count in SVG matches data file; wired vs unwired pins are visually distinct. AC-2, AC-3, AC-19.

### Phase 3 — Layout and Positioning

#### Step 6: Board position configuration — YAML and CLI

- **Test:** Parse a circuit with `board_position: right` → position is `"right"`. Parse without it → position is `"left"` (default). CLI `--board-position right` overrides YAML `board_position: left`.
- **Implement:** In `breadboard.py`: add `--board-position` CLI arg (choices: `left`, `right`, default: `None`). In `generate()`: read `circuit.get("board_position", "left")`, let CLI override if provided. Pass position into McuBoard constructor.
- **Files:** `tools/breadboard.py`
- **Verify:** AC-4, AC-16.

#### Step 7: Margin and layout adjustment for board graphic

- **Test:** When board is present and positioned left, `Board.margin_left` is wide enough to accommodate the board graphic width + routing gap. SVG width increases accordingly. When board is absent, margins are unchanged.
- **Implement:** In `generate()`: after loading board data and creating `McuBoard`, compute needed left margin = board graphic width + routing gap (40px) + existing module card width. Pass this as `margin_left` to `Board()`. For right position, compute analogous `margin_right` increase (may require adding `margin_right` param to `Board.__init__`). Update `Board.svg_width` property if needed.
- **Files:** `tools/bb/board.py`, `tools/breadboard.py`
- **Verify:** SVG dimensions accommodate the board graphic without clipping.

#### Step 8: Module card repositioning when board is present

- **Test:** Generate SVG with both a module card and board graphic on the left. Module card's right edge does not overlap the board graphic's left edge.
- **Implement:** When board is on the left, module cards compute their `box_right` relative to the board graphic's left edge (instead of `board.board_left`). Pass the MCU board's bbox into `render_module()` (or store it on the `Board` instance) so it knows where the board graphic sits. Module cards stack to the left of the MCU board.
- **Files:** `tools/bb/renderers.py`, `tools/breadboard.py`
- **Verify:** AC-5. Module + board visual check in test-renderers.

### Phase 4 — Smart Wire Router

#### Step 9: Obstacle model

- **Test:** Given a board graphic bbox, breadboard bbox, and module card bboxes, `collect_obstacles()` returns a list of `Rect` tuples. Verify all expected obstacles are present and bounding boxes are correct.
- **Implement:** Create `tools/bb/router.py`. Define `Rect = namedtuple('Rect', 'x y w h')`. Add `collect_obstacles(mcu: McuBoard | None, board: Board, module_bboxes: list[Rect]) -> list[Rect]`. Returns the board graphic bbox, the breadboard body bbox (from `board.board_left/top/right/bottom`), and all module card bboxes.
- **Files:** Create `tools/bb/router.py`
- **Verify:** Obstacle list has expected count and bounds for a test circuit.

#### Step 10: Channel assignment

- **Test:** Given 5 wires with known source/destination Y positions, `assign_channels()` returns channel indices such that no two wires share a channel. Channels are spaced `WIRE_SPACING` (5px) apart in the routing gap.
- **Implement:** In `router.py`: add `assign_channels(wires: list[WireSpec], gap_x_start: float, gap_x_end: float, wire_spacing: float) -> list[int]`. `WireSpec` contains: board pin (x, y), breadboard hole (x, y), color, label. Sort wires by destination row Y. Assign channels left-to-right (or right-to-left depending on board position) in the routing gap. Return channel index per wire.
- **Files:** `tools/bb/router.py`
- **Verify:** No duplicate channels; channels are within the gap bounds.

#### Step 11: Orthogonal path computation

- **Test:** Given a source point, destination point, and channel X position, `compute_path()` returns a list of (x, y) waypoints forming an orthogonal (H-V-H) path. Verify all segments are horizontal or vertical. Verify no segment passes through any obstacle interior.
- **Implement:** In `router.py`: add `compute_path(src: tuple, dst: tuple, channel_x: float) -> list[tuple[float, float]]`. The path has 4 waypoints: (1) source point, (2) horizontal to channel_x, (3) vertical to destination row, (4) horizontal to destination point. For wires where the board pin and breadboard hole are on opposite sides of the breadboard (far-side routing), add additional waypoints to route over/under the breadboard.
- **Files:** `tools/bb/router.py`
- **Verify:** All segments are axis-aligned; path avoids obstacle interiors. AC-6, AC-7.

#### Step 12: Crossing minimization via wire ordering

- **Test:** For sketch 004-joystick-lights (7 board-pin wires), compute crossings with naive order vs optimized order. Optimized order has fewer crossings.
- **Implement:** In `router.py`: before channel assignment, sort wires to minimize crossings. Strategy: for each wire, compute the "slope direction" (board pin Y relative to destination Y). Group wires by direction (rising vs falling). Within each group, sort by destination Y. Assign channels in this order. Count crossings as: two wires cross if their board-pin ordering is opposite to their channel ordering.
- **Files:** `tools/bb/router.py`
- **Verify:** AC-8. Crossing count < naive direct approach for multi-wire circuits.

#### Step 13: SVG path rendering with smooth bends

- **Test:** Given a 4-waypoint path, `render_routed_wire()` produces an SVG `<path>` element with `d` attribute containing `L` (line) and `A` (arc) commands. Arcs appear at the two bend points.
- **Implement:** In `router.py`: add `render_routed_wire(waypoints: list[tuple], color: str, bend_radius: float = 4.0) -> str`. Generates an SVG `<path>` with: `M` to start, straight segments with `L`, and small circular arcs (`A`) at each 90° turn. The arc radius is `bend_radius` pixels, trimming the adjacent straight segments accordingly.
- **Files:** `tools/bb/router.py`
- **Verify:** SVG path is syntactically valid; visual check shows smooth corners. AC-6.

### Phase 5 — Integration

#### Step 14: Wire rendering — delegate board-pin wires to router

- **Test:** Generate SVG for sketch 001-blink with `board: hero-xl`. Board-pin wires (to `pin9`, `gnd`) render as routed paths (contain `<path` elements, not the old `<line` + pill approach). Hole-to-hole wires still render as direct lines.
- **Implement:** In `breadboard.py` `generate()`: after creating board chrome and before rendering wires, partition wires into board-pin wires and hole-to-hole wires. Pass board-pin wires to `route_wires()` from `router.py`, which returns SVG elements. Render hole-to-hole wires via existing `render_wire()`. When no board is loaded, ALL wires use the existing `render_wire()` path (pill labels).
- **Files:** `tools/breadboard.py`, `tools/bb/legend.py`
- **Verify:** AC-10, AC-14, AC-15, AC-18.

#### Step 15: Module board-pin wire integration

- **Test:** Generate SVG for sketch 004-joystick-lights. Module pins with `to: pin_a0` route to the board graphic's A0 pin position (not to a right-margin pill). Module pins with `to: -L37` (power rail, not board pin) still route directly to the power rail.
- **Implement:** In `render_module()`: when a board graphic is present and a pin's `to:` is a board pin, record it as a board-pin wire for the router instead of drawing a cross-diagram pill. The module pin anchor becomes the wire's source; the board pin position becomes the destination. These wires go through the same channel-assignment and routing pipeline.
- **Files:** `tools/bb/renderers.py`, `tools/breadboard.py`
- **Verify:** AC-17. No pills remain for board-pin wires when board graphic is active.

#### Step 16: Integrate board graphic into generate() layer order

- **Test:** Full generate() produces SVG with layers in order: board graphic → breadboard chrome → components → routed wires → hole-to-hole wires → legend → title. Board graphic appears behind breadboard.
- **Implement:** In `generate()`: insert board rendering layers (outline + pins) before breadboard chrome. This ensures the board appears behind/beside the breadboard. Wire routing layers go after components (so wires appear on top). Update `svg_width`/`svg_height` to encompass the full layout.
- **Files:** `tools/breadboard.py`
- **Verify:** AC-1, AC-13. Layer order correct in SVG source.

#### Step 17: Legend preservation

- **Test:** Generate SVG for sketch 003-patterns. Legend section contains entries for all 11 wires with correct labels and color swatches. Legend is not broken by the routing changes.
- **Implement:** Verify `render_legend()` still works — it reads from the `circuit` dict (unchanged). If any wire rendering data changed (e.g., wires are now routed differently), ensure the legend still has access to wire labels and colors. No changes expected — legend reads from `circuit["wires"]`, not from rendered SVG.
- **Files:** (verification only — likely no code changes)
- **Verify:** AC-20.

#### Step 18: Re-export new modules in breadboard.py

- **Test:** `python3 -c "import breadboard as bb; bb.McuBoard; bb.load_board; bb.route_wires"`
- **Implement:** Add re-exports of new public names from `bb.mcu`, `bb.boards`, `bb.router` in `tools/breadboard.py` for backward compatibility and test-renderers.py access.
- **Files:** `tools/breadboard.py`
- **Verify:** All new public APIs accessible via `import breadboard as bb`.

### Phase 6 — Verification and Polish

#### Step 19: Update test-renderers.py with board graphic

- **Test:** `python3 tools/test-renderers.py` produces SVG with board graphic alongside the breadboard, with bounding boxes for the board and routed wires visible.
- **Implement:** Add `board: hero-xl` to the test circuit dict. Add board-pin wires that exercise routing (left-bank, right-bank, power pins, analog pins). Add bounding box overlay for the board graphic. If module card is present, verify it doesn't overlap the board.
- **Files:** `tools/test-renderers.py`
- **Verify:** Visual check of test-renderers output SVG.

#### Step 20: Regenerate all sketch SVGs

- **Test:** All 4 sketch SVGs regenerate without errors. `python3 tools/validate-wiring.py` still passes.
- **Implement:** Loop over all `sketches/*/wiring.yaml`, regenerate each SVG. Visual review of each diagram for correctness.
- **Files:** `sketches/001-blink/wiring.svg`, `sketches/002-pulse/wiring.svg`, `sketches/003-patterns/wiring.svg`, `sketches/004-joystick-lights/wiring.svg`
- **Verify:** AC-13. All SVGs valid, all wires routed correctly, board graphic present.

#### Step 21: Update documentation

- **Test:** N/A (docs only).
- **Implement:** Update `docs/renderers.md` with board renderer documentation: supported boards, board_position config, wire routing behavior. Update CLAUDE.md commands section if any new commands/scripts were added. Update GUIDE.md node-specific section if new architecture patterns were introduced.
- **Files:** `docs/renderers.md`, potentially `CLAUDE.md`
- **Verify:** No stale references to pill-label-only behavior. Board renderer documented.

## Risks

- **Pin layout accuracy:** The HERO XL pin positions must match the physical Mega 2560 Rev3. Mitigation: derive positions from official Arduino board files (KiCad source, available at github.com/arduino/ArduinoMega2560). Cross-reference with inventory.md and datasheets.
- **Scale mismatch:** At 5.51 px/mm, the board graphic is ~560px wide — larger than the current total SVG width. Mitigation: Zach confirmed SVG width is not a concern. The diagram simply gets wider.
- **Router complexity creep:** Smart routing algorithms can become arbitrarily complex. Mitigation: channel-based routing (H-V-H paths in the gap) is sufficient for the ~10-20 wire scale. Full grid-based A* is out of scope unless the channel approach fails visually.
- **Module card collision:** Modules and the board graphic both default to the left side. Mitigation: Step 8 explicitly handles repositioning. Module cards stack to the left of the board.
- **Far-side routing:** Wires to right-bank holes (board on left) must cross the breadboard. Mitigation: route over the top or under the bottom of the breadboard body, adding waypoints to the path. Visually these are U-shaped paths.

## Definition of Done

- [ ] All 20 acceptance criteria from spec pass
- [ ] All existing sketch SVGs regenerate without errors
- [ ] `python3 tools/test-renderers.py` produces valid SVG with board graphic
- [ ] `python3 tools/validate-wiring.py` passes
- [ ] Pill-label fallback works when board is absent
- [ ] Code reviewed (run /review)
