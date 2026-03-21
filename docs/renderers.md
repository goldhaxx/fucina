# Breadboard Diagram Renderers

Reference for component types supported by `tools/breadboard.py`. Use these `type:` values in `wiring.yaml` component entries.

## Supported Renderers

### `resistor` — Axial resistor with color bands

```yaml
- type: resistor
  value: 220          # ohms — determines color band pattern
  from: d7            # one lead
  to: d10             # other lead
```

Draws a tan body with 4 color bands (2 digits + multiplier + tolerance gold) and lead wires to each hole.

---

### `led` — Standard 2-pin LED

```yaml
- type: led
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
  digits: 1            # 1 or 4
  row_start: 10        # first breadboard row
  pins: 10             # total pin count (10 for 1-digit, 12 for 4-digit)
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

## Fallback Strategy

If no renderer exists for a component, use one of these:

1. **`sensor`** — for anything small that plugs into the breadboard (2-4 pins)
2. **`module`** — for anything that connects via jumper wires from off-board
3. **Omit from `components:`** — the wires still render, just no component body shown

When a new renderer is needed, add it to `tools/breadboard.py` following the pattern of existing `render_*` functions, update the dispatch in `generate()`, update the legend in `render_legend()`, and add the type to this document.
