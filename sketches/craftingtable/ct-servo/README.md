# Servo Motor — 180° Sweep

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 170

Sweeps an SG90 micro servo back and forth from 0° to 180° continuously. The servo moves in 1° increments with a 15ms delay between steps for smooth motion.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-servo/wiring.yaml -o sketches/craftingtable/ct-servo/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x SG90 micro servo motor (the small blue one with 3 wires)
- 3x jumper wires (or use the servo's built-in connector directly)

## Step-by-Step Wiring

The SG90 servo has 3 color-coded wires:
- **Orange/Yellow** = signal (PWM)
- **Red** = power (VCC)
- **Brown/Black** = ground (GND)

### Connect the servo wires

- **Orange wire** → **Pin 9** on the HERO XL (via breadboard row 10)
- **Red wire** → **5V** on the HERO XL (via breadboard row 11)
- **Brown wire** → **GND** on the HERO XL (via breadboard row 12)

You can plug the servo's female connector into male-to-male jumper wires, then into the breadboard.

## Build and Upload

```bash
cd sketches/craftingtable/ct-servo
pio run -e mega -t upload
```

The servo should immediately begin sweeping back and forth. It takes about 5.4 seconds for a full sweep cycle (180 steps × 15ms × 2 directions).

## What to Try Next

- Use a potentiometer on A0 to control the servo angle with `map(analogRead(A0), 0, 1023, 0, 180)`
- Add a button to toggle between two positions (e.g., 0° and 90°)
- Combine with an ultrasonic sensor to build a scanning radar
