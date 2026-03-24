# Feature: HERO XL Board Renderer with Smart Wire Routing

> Feature: board-renderer
> Created: 1774321016
> Status: Draft

## Summary

Add a visual representation of the HERO XL (Arduino Mega 2560) microcontroller board to breadboard SVG diagrams, replacing the current pill-label system for board pin connections. The board graphic shows all pin headers with labels. Wires connecting breadboard holes to board pins route intelligently around obstacles using orthogonal paths that minimize crossings — similar to smart-routing in Visio or KiCad. Board position relative to the breadboard is configurable (default: left).

## Job To Be Done

**When** I generate a breadboard wiring diagram with `breadboard.py`,
**I want to** see a visual representation of the HERO XL board with labeled pins and clearly routed wires connecting it to the breadboard,
**So that** I can look at the diagram and know exactly which board pins to connect without cross-referencing a separate pinout chart.

## Acceptance Criteria

Each criterion is independently testable. Binary pass/fail.

### Board Graphic

- [ ] **AC-1:** When `board: hero-xl` is specified in `wiring.yaml`, the SVG includes a board graphic showing the board outline, USB-B connector, DC barrel jack, and board name label.
- [ ] **AC-2:** All HERO XL pin headers are rendered with labeled pins: digital 0–53, analog A0–A15, power (IOREF, RESET, 3.3V, 5V, GND×3, VIN), communication (TX/RX pairs), AREF, SDA, SCL. Every pin position matches the physical Mega 2560 Rev3 header layout.
- [ ] **AC-3:** Pins that are wired in the circuit are visually highlighted (distinct fill or border) compared to unwired pins.

### Positioning

- [ ] **AC-4:** The board graphic defaults to the left side of the breadboard. When `board_position: right` is set in `wiring.yaml` (or `--board-position right` CLI arg), the board renders on the right. CLI arg overrides YAML.
- [ ] **AC-5:** When the board is on the left and module cards are also present, both are visible without overlapping. Module cards stack to the left of the board or reposition automatically.

### Wire Routing

- [ ] **AC-6:** Wires from breadboard holes to board pins use orthogonal segments (horizontal and vertical only) with visually smooth bends (rounded corners or short diagonal chamfers at turns).
- [ ] **AC-7:** No wire segment passes through the interior of the board graphic, the breadboard body, or any module card. Wires route around these obstacles.
- [ ] **AC-8:** Wire crossings are minimized. Given N wires, the router produces fewer crossings than a naive direct-line approach. (Testable: count crossings in a multi-wire sketch like 004-joystick-lights.)
- [ ] **AC-9:** Parallel wires running in the same direction are spaced apart (channel assignment), not drawn on top of each other.
- [ ] **AC-10:** Wires between breadboard holes (hole-to-hole, not involving board pins) continue to render as direct lines — smart routing only applies to wires with at least one board pin endpoint.

### Data Model

- [ ] **AC-11:** The HERO XL pin layout is defined in a data file (`tools/bb/boards/hero-xl.yaml` or equivalent), not hardcoded in Python. Adding a new board (e.g., ESP32) requires only adding a new data file, not modifying renderer code.
- [ ] **AC-12:** The board data file specifies: board dimensions (mm), pin header positions (mm offsets from board origin), pin names per header, connector positions (USB, DC jack), and board display name.

### Integration

- [ ] **AC-13:** Existing sketches that specify `board: hero-xl` render with the board graphic and routed wires. No changes to `wiring.yaml` files are required (the `board:` field already exists).
- [ ] **AC-14:** When `board:` is absent or set to an unknown value, the diagram falls back to the current pill-label behavior. No board graphic is rendered.
- [ ] **AC-15:** The pill-label code path is preserved as the fallback — not deleted.
- [ ] **AC-16:** `python3 tools/breadboard.py <input> -o <output>` CLI interface is unchanged except for the new optional `--board-position` argument.
- [ ] **AC-17:** Module `to: pin9` wires that previously rendered as cross-diagram pills now route to the board graphic's pin 9 position instead.

### Visual Quality

- [ ] **AC-18:** Wire colors from `wiring.yaml` are preserved in the routed paths.
- [ ] **AC-19:** Board pin labels are legible at the diagram's default scale (font size >= 6px).
- [ ] **AC-20:** The legend section continues to list all wires with their labels and colors.

## Affected Files

| File | Change |
|------|--------|
| `tools/bb/boards/hero-xl.yaml` | New — board pin layout data |
| `tools/bb/boards/__init__.py` | New — board data loader |
| `tools/bb/mcu.py` | New — board graphic renderer |
| `tools/bb/router.py` | New — smart wire routing engine |
| `tools/bb/constants.py` | Modified — new board-related color constants |
| `tools/bb/legend.py` | Modified — wire rendering delegates to router when board is present |
| `tools/bb/renderers.py` | Modified — module renderer delegates board-pin wires to router |
| `tools/breadboard.py` | Modified — board rendering layer, CLI `--board-position` arg, router integration |
| `docs/renderers.md` | Modified — document board renderer and routing behavior |
| `sketches/*/wiring.svg` | Modified — regenerated with board graphics |

## Dependencies

- **Requires:** HERO XL physical pin header layout (derivable from Arduino Mega 2560 Rev3 schematic and board files, publicly available)
- **Blocked by:** Nothing

## Out of Scope

- Rendering boards other than HERO XL (data model supports it, but only hero-xl.yaml ships)
- Interactive/clickable SVG elements
- Curved or diagonal wire routing (orthogonal only)
- Automatic pin assignment (wiring.yaml still specifies which pins are used)
- Routing optimization beyond crossing minimization (e.g., minimizing total wire length is nice-to-have, not required)

## Implementation Notes

- Follow the existing renderer pattern: `render_board()` in `mcu.py` takes `(board: Board, circuit: dict)` and returns `list[str]` of SVG elements.
- The router needs obstacle rectangles as input. Each obstacle is an axis-aligned bounding box. Sources: board graphic bounds, `board.board_left/right/top/bottom` for the breadboard, module card bounds from `render_module`.
- For routing algorithm: a grid-based approach (coarse grid over the SVG canvas, A* or BFS per wire, ordered by Y-coordinate to minimize crossings) is a reasonable starting point. Channel assignment prevents parallel wires from overlapping.
- The board graphic should use a consistent scale factor: mm-to-px conversion based on `HOLE_PITCH` (14px = 2.54mm, so 1mm ≈ 5.51px).
- Pin headers on the board graphic should have small circular holes at each pin position, matching the breadboard hole visual style but smaller.
- The board data file should use mm coordinates relative to the board's origin (bottom-left corner matching PCB convention, or top-left matching SVG convention — document whichever is chosen).
