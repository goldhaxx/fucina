# Stepper Motor — 28BYJ-48

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 210

Rotates the 28BYJ-48 stepper motor one full revolution clockwise at 5 RPM, pauses, then one full revolution counter-clockwise at 10 RPM.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-stepper/wiring.yaml -o sketches/craftingtable/ct-stepper/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x 28BYJ-48 stepper motor (the white motor with blue label)
- 1x ULN2003 driver board (the red/blue board with 4 LEDs)
- 5x jumper wires
- External 5V power supply recommended (stepper draws more current than USB can reliably supply)

## Step-by-Step Wiring

### 1. Connect the motor to the driver board

Plug the stepper motor's white 5-pin JST connector into the ULN2003 driver board. It only fits one way.

### 2. Connect the driver board to the HERO XL

**IMPORTANT:** The pin order is IN1–IN3–IN2–IN4 (not sequential!) — this is required for the correct step sequence.

- **IN1** → **Pin 8**
- **IN3** → **Pin 10**
- **IN2** → **Pin 9**
- **IN4** → **Pin 11**

### 3. Power the driver board

- **-** (GND) on driver → **GND** on HERO XL
- **+** (VCC) on driver → External 5V supply (or HERO XL 5V for testing — but motor may stall under load)

## Build and Upload

```bash
cd sketches/craftingtable/ct-stepper
pio run -e mega -t upload
```

The motor rotates slowly clockwise for one full revolution (~24 seconds at 5 RPM), pauses 1 second, then rotates counter-clockwise (~12 seconds at 10 RPM).

## What to Try Next

- Use a potentiometer to control the speed
- Combine with a button to control direction
- Build a camera pan mechanism or turntable
