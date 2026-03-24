# Breadboard Diagram Renderers

Reference for component types supported by `tools/breadboard.py`. Use these `type:` values in `wiring.yaml` component entries.

## Supported Renderers

### `resistor` — Axial resistor with color bands

```yaml
- type: resistor
  model: axial-resistor-1/4W  # key in docs/component-specs.yaml
  value: 220          # ohms — determines color band pattern
  from: d7            # one lead
  to: d10             # other lead
```

Draws a tan body with 4 color bands (2 digits + multiplier + tolerance gold) and lead wires to each hole.

---

### `led` — Standard 2-pin LED

```yaml
- type: led
  model: led-5mm       # key in docs/component-specs.yaml
  color: red           # red, green, yellow, blue, white, orange
  anode: e10           # long leg (+)
  cathode: e11         # short leg (-)
```

Draws a colored dome with glow effect, cathode bar, and "+" anode label.

---

### `button` — Momentary push button

```yaml
- type: button
  from: e10            # one side
  to: f10              # other side (typically spans center channel)
```

Draws a dark square body with a circular button cap. Best placed spanning the center channel (e-row to f-row on the same numbered row).

---

### `buzzer` — Active or passive buzzer

```yaml
- type: buzzer
  variant: active      # "active" (sealed, fixed tone) or "passive" (open, tone()-driven)
  positive: a10        # + pin
  negative: a11        # - pin
```

Draws a dark circular body with "+" marking and decorative sound wave. Active variant is darker than passive.

---

### `sensor` — Generic on-board sensor/module (PCB)

```yaml
- type: sensor
  label: "LDR"         # short label shown on the PCB body
  pin1: a10            # first pin
  pin2: a11            # second pin
  pin3: a12            # third pin (optional — supports 2-4 pins)
```

Draws a green PCB rectangle centered on the pin positions. Good fallback for any small module that sits directly on the breadboard. Also accepts `from`/`to` shorthand for 2-pin components.

---

### `potentiometer` — 3-pin rotary knob

```yaml
- type: potentiometer
  pin1: a10            # wiper output
  pin2: a11            # reference voltage
  pin3: a12            # ground
```

Draws a circular knob with a position indicator line and 3 lead wires.

---

### `rgb_led` — 4-pin common-cathode RGB LED

```yaml
- type: rgb_led
  red: e10             # red pin
  common: e11          # longest pin (GND)
  green: e12           # green pin
  blue: e14            # blue pin
```

Draws a frosted dome with 3 colored channel dots (R/G/B) and a GND label on the common pin.

---

### `seven_segment` — DIP display spanning center channel

```yaml
- type: seven_segment
  model: 5161AS        # key in docs/component-specs.yaml (or 5641AS for 4-digit)
  digits: 1            # 1 or 4
  row_start: 10        # first breadboard row
  pins: 10             # total pin count (10 for 1-digit, 12 for 4-digit)
  orientation: left    # optional — default "left" (segment A faces column a)
```

Draws a black DIP IC body spanning columns e–f (across the center channel) with a notch at the top, stylized "8" digit segments, and pin dots on both sides.

---

### `module` — Off-board component (labeled box at margin)

```yaml
- type: module
  name: "HC-SR04"      # displayed on the label
  color: "#1565c0"     # box color
  pins:
    - hole: a10
      label: VCC
    - hole: a11
      label: TRIG
    - hole: a12
      label: ECHO
    - hole: a13
      label: GND
```

Draws a labeled box at the left edge of the board with pin labels and dashed lead lines to the breadboard holes. Use for any component that connects via jumper wires but doesn't physically sit on the breadboard (servos, sensor modules, RFID readers, LCDs, etc.).

**Color conventions:**
- `#1565c0` (blue) — sensors
- `#6a1b9a` (purple) — input devices (keypad, encoder, joystick)
- `#2e7d32` (green) — output devices (servo, stepper, LCD)
- `#e65100` (orange) — communication modules (RFID, RTC, Bluetooth)

---

## Orientation Model

Some components (DIP packages, displays) have a natural "top" direction defined by their datasheet. The optional `orientation` key controls which direction that natural top faces when the component is placed on the breadboard.

### Values

| Value | Rotation | Natural top faces... |
|-------|----------|---------------------|
| `up` | 0° | Toward row 1 (default for most types) |
| `right` | 90° | Toward column j |
| `down` | 180° | Toward row 63 |
| `left` | -90° | Toward column a |

You can also pass a numeric angle (e.g., `orientation: -90`).

### Defaults per type

| Type | Default | Why |
|------|---------|-----|
| `seven_segment` | `left` | DIP display's segment A faces toward column a, matching physical placement |
| All others | `up` (no rotation) | Symmetric or position-derived — orientation not needed |

Most components (resistor, LED, button, buzzer, sensor, potentiometer, rgb_led) derive their visual layout from pin positions and don't use orientation. Only add `orientation` when the component has an asymmetric face that needs to point a specific direction.

---

## Fallback Strategy

If no renderer exists for a component, use one of these:

1. **`sensor`** — for anything small that plugs into the breadboard (2-4 pins)
2. **`module`** — for anything that connects via jumper wires from off-board
3. **Omit from `components:`** — the wires still render, just no component body shown

When a new renderer is needed, add a `render_*` function in `tools/bb/renderers.py` and a `_legend_*` function in `tools/bb/legend.py`, then add one entry to the `RENDERERS` dict in `legend.py`. Update this document with the new type.

---

## Renderer Development Guide

### Creating a new renderer

1. **Look up the datasheet** and add dimensions to `docs/component-specs.yaml`. This is the single source of truth — renderers read from it, not from hardcoded constants.
2. **Choose a coordinate strategy:**
   - **Position-derived** (most components): renderer computes geometry from pin hole positions. No orientation needed. Examples: resistor, LED, button, buzzer, sensor.
   - **Orientation-based** (DIP packages, displays): renderer draws in natural (datasheet) coords centered at origin, wrapped in a `<g transform="translate(...) rotate(...)">`. Uses `parse_orientation(comp)` for the rotation angle. Example: seven_segment.
3. **Write `render_*(board, comp) -> list[str]`:** Returns SVG element strings. Call `board.hole_xy()` for coordinates, `board.mark_occupied()` for each pin.
4. **Write `_legend_*(comp) -> tuple[str, str]`:** Returns `(description, swatch_color)` for the diagram legend.
5. **Add to `RENDERERS` dict:** One line maps the type string to the `(render_fn, legend_fn)` tuple.
6. **Add to this document:** Document the type, its YAML keys, and what it draws.
7. **Test:** Run `python3 tools/test-renderers.py` — add an instance of the new type to `build_test_circuit()`.

### Sizing with rotation

For orientation-based components, use `compute_rotated_fit()` to find the maximum scale factor:

```python
scale = compute_rotated_fit(
    natural_w, natural_h,    # from datasheet
    container_w, container_h, # available space on board
    rotation_deg,             # from parse_orientation()
    fill=0.90                 # leave 10% padding
)
digit_w = natural_w * scale
digit_h = natural_h * scale
```

### Standard DIP widths

| Row spacing | Columns | Use for |
|------------|---------|---------|
| 0.3" (7.62mm) | `e` to `f` | Standard ICs (spans center channel only) |
| 0.5" (12.7mm) | `d` to `g` | Wider ICs |
| 0.6" (15.24mm) | `e` to `i` | 7-segment displays, wide DIP packages |

---

## MCU Board Renderer

When a `wiring.yaml` file specifies `board: hero-xl`, a visual representation of the HERO XL (Arduino Mega 2560 Rev3) board is rendered alongside the breadboard. All pin headers are shown with labeled pins, and wires connecting breadboard holes to board pins are smart-routed with orthogonal paths.

### Configuration

```yaml
name: "001 — Blink"
board: hero-xl              # renders the board graphic
board_position: left        # optional: "left" (default) or "right"
```

CLI override: `--board-position right`

### Board Graphic

The board is drawn rotated 90° CW from its natural orientation, so the digital pins (0-13, GND, AREF, SDA, SCL) face the breadboard for short wire routes. Features:

- **Dark green PCB** rectangle with USB-B and DC barrel jack connectors
- **All 86 pins** labeled: digital 0-53, analog A0-A15, power (3V3, 5V, GND, VIN), AREF, SDA, SCL, TX/RX pairs
- **Wired pins** are highlighted in gold; unused pins are dim gray

### Wire Routing

Wires connecting breadboard holes to board pins are routed through a gap between the board graphic and the breadboard:

1. Wire exits the board pin **horizontally** into the routing gap
2. Wire runs **vertically** along an assigned channel to align with the destination row
3. Wire enters the breadboard hole **horizontally**

Routing features:
- **Orthogonal paths** with smooth rounded corners at 90° bends
- **Channel assignment** spaces parallel wires apart to prevent overlap
- **Crossing minimization** sorts wires by destination row to reduce intersections
- **Module integration** — module `to: pin9` wires route to the board graphic instead of margin pills

### Fallback Behavior

When `board:` is absent or set to an unrecognized board name, wires to board pins render as horizontal lines to colored pill labels on the diagram margins (the pre-existing behavior). The pill-label code path is preserved as a fallback.

### Adding New Boards

Board pin layouts are defined in YAML data files at `tools/bb/boards/<name>.yaml`. Each file specifies board dimensions, pin headers with positions, and connector locations. See `hero-xl.yaml` for the reference format. Adding a new board requires only creating the YAML file — no Python code changes.

### Source Files

| File | Purpose |
|------|---------|
| `tools/bb/boards/hero-xl.yaml` | HERO XL pin layout data (from KiCad footprint) |
| `tools/bb/boards/__init__.py` | Board data loader |
| `tools/bb/mcu.py` | Board coordinate mapper and SVG renderer |
| `tools/bb/router.py` | Smart wire routing engine |
