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
    value: 220               # ohms
    from: d7                 # breadboard hole (column + row)
    to: d10

  - type: led                # standard 2-pin LED
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
- Power rails: `+L1` through `+L50`, `-L1` through `-L50` (left side), `+R1`/`-R1` (right side)
- Board pins: `pin9`, `gnd`, `5v`, `3v3`, `vin` (drawn as labeled stubs off the board edge)

## Updating a Diagram

After any change to `wiring.yaml`, regenerate the SVG immediately.
Never commit a `wiring.yaml` change without a matching `wiring.svg` update.
