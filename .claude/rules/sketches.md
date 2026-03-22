# Sketch Creation Rules

## Every Sketch Must Include

1. `src/main.cpp` — sketch source code
2. `platformio.ini` — board and library config
3. `wiring.yaml` — machine-readable circuit description
4. `wiring.svg` — generated breadboard diagram (never hand-edit)
5. `README.md` — what it does, parts list, wiring reference, build commands

## Creating a New Sketch

1. Determine the next sketch number by reading `sketches/` directory.
2. Create `sketches/NNN-name/src/` directory structure.
3. Write `wiring.yaml` FIRST — define every component and wire before writing code.
4. Generate the SVG: `python3 tools/breadboard.py sketches/NNN-name/wiring.yaml -o sketches/NNN-name/wiring.svg`
5. Write `platformio.ini` targeting the correct board.
6. Write `src/main.cpp` — pin numbers must match `wiring.yaml`.
7. Write `README.md` referencing `wiring.svg` for the visual diagram.
8. Compile with `pio run` to verify before suggesting upload.

## wiring.yaml Schema

```yaml
name: "NNN — Sketch Name"
board: hero-xl              # or esp32

components:
  - type: resistor           # axial resistor with color bands
    model: axial-resistor-1/4W  # key in docs/component-specs.yaml
    value: 220               # ohms
    from: d7                 # breadboard hole (column + row)
    to: d10

  - type: led                # standard 2-pin LED
    model: led-5mm           # key in docs/component-specs.yaml
    color: red               # red, green, yellow, blue, white, orange
    anode: e10               # long leg (+)
    cathode: e11             # short leg (-)

  - type: button             # momentary push button
    from: e10                # one side
    to: f10                  # other side (spans center channel)

  - type: buzzer             # active or passive buzzer
    variant: active          # "active" or "passive"
    positive: e10
    negative: e11

  - type: potentiometer      # 3-pin rotary knob
    pin1: a10                # wiper
    pin2: a11                # reference
    pin3: a12                # ground

  - type: rgb_led            # 4-pin common-cathode RGB LED
    red: e10
    common: e11              # longest pin (GND)
    green: e12
    blue: e14

  - type: sensor             # generic on-board PCB module (2-4 pins)
    label: "LDR"             # short label on the body
    pin1: e10
    pin2: e12

  - type: seven_segment      # DIP display spanning center channel
    digits: 1                # 1 or 4
    row_start: 10            # first breadboard row
    orientation: left        # optional — up/right/down/left (default: left)
    pins: 10                 # total pin count (10 or 12)

  - type: module             # off-board component (labeled box at margin)
    name: "HC-SR04"          # displayed on the label
    color: "#1565c0"         # box color
    pins:
      - hole: a10
        label: VCC
      - hole: a11
        label: TRIG

wires:
  - from: a7
    to: pin9                 # board pin: pin{N}, gnd, 5v, 3v3, vin
    color: "#e53935"         # CSS color for diagram
    label: "signal — Pin 9"  # shown in legend
```

See `docs/renderers.md` for the full reference on each component type.

### Hole Addresses
- Terminal strips: `a1` through `j63` (column letter + row number)
- Left bank: columns `a` through `e` — connected per row within the bank
- Right bank: columns `f` through `j` — connected per row within the bank
- Center channel: the gap between columns `e` and `f` — breaks the connection
- Power rails: `+L1` through `+L50`, `-L1` through `-L50` (left side), `+R1`/`-R1` (right side)
- Board pins: `pin9`, `gnd`, `5v`, `3v3`, `vin` (drawn as labeled stubs off the board edge)

## Physical Accuracy Requirements

**Every hole address in wiring.yaml must reflect the actual physical breadboard position.** No simplifications, no assumptions.

### Both-bank wiring for DIP components
DIP packages (7-segment displays, ICs, any component with two rows of pins) physically straddle the breadboard. Their left-side pins go into the left bank (columns a–e) and their right-side pins go into the right bank (columns f–j). The wiring.yaml MUST reflect this:
- Left-side pins: use columns a–e (typically `e` for the innermost column)
- Right-side pins: use columns f–j (typically `i` or `j` depending on package width)
- NEVER put all connections on one side when the physical component spans both

### Deriving dimensions from datasheets
When placing a component on the breadboard, look up its datasheet for:
- **Pin pitch** (distance between pins in the same row) — almost always 0.1" = 1 breadboard hole
- **Row spacing** (distance between the two rows of a DIP) — determines which columns the pins occupy
  - 0.3" DIP (standard IC): left pins in `e`, right pins in `f` (spans center channel only)
  - 0.5–0.6" DIP (7-segment displays, wide ICs): left pins in `e`, right pins in `i`
- **Pin count** — determines how many rows the component spans

Never guess which columns a component's pins occupy. Calculate from the datasheet's row spacing and the breadboard's 0.1" hole pitch.

### Wire side determines pin label placement
Wires connecting to left-bank holes (a–e) get their board-pin label on the left side of the diagram. Wires connecting to right-bank holes (f–j) get their label on the right side. This is handled automatically by `breadboard.py` — but only if the hole addresses are correct.

## Updating a Diagram

After any change to `wiring.yaml`, regenerate the SVG immediately.
Never commit a `wiring.yaml` change without a matching `wiring.svg` update.
