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
