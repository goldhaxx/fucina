# Joystick — Analog X/Y + Button

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 110

Reads the KY-023 joystick module's two analog axes (X and Y, each 0-1023 with center at ~512) and its digital push button, printing all values to the serial monitor every 500 ms. The button uses `INPUT_PULLUP` so it reads LOW when pressed.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-joystick/wiring.yaml -o sketches/craftingtable/ct-joystick/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x KY-023 joystick module
- 5x jumper wires

## Step-by-Step Wiring

### 1. Identify the joystick pins

The KY-023 module has 5 pins:

```
GND — +5V — VRx — VRy — SW
```

### 2. Place the joystick

Insert the joystick module's 5 header pins into breadboard rows **a10** through **a14** (one pin per row).

| Joystick Pin | Breadboard Hole |
|-------------|-----------------|
| +5V         | a10             |
| GND         | a11             |
| VRx         | a12             |
| VRy         | a13             |
| SW          | a14             |

### 3. Connect jumper wires

- **Wire 1 (red):** From **a10** to **5V** on the HERO XL
- **Wire 2 (black):** From **a11** to **GND** on the HERO XL
- **Wire 3 (green):** From **a12** to **A0** on the HERO XL
- **Wire 4 (blue):** From **a13** to **A1** on the HERO XL
- **Wire 5 (purple):** From **a14** to **Pin 2** on the HERO XL

### 4. Electrical path

```
5V  → joystick +5V
GND → joystick GND
A0  ← joystick VRx (X-axis analog 0-1023)
A1  ← joystick VRy (Y-axis analog 0-1023)
Pin 2 ← joystick SW (LOW when pressed, INPUT_PULLUP)
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-joystick
pio run -e mega -t upload
```

Open the serial monitor at 115200 baud:
```bash
pio device monitor -b 115200
```

You should see output like:
```
Switch: 1  X-axis: 512  Y-axis: 510
Switch: 1  X-axis: 512  Y-axis: 510
Switch: 0  X-axis: 1023  Y-axis: 0
```

## What to Try Next

- Map joystick X/Y to servo position for a pan-tilt mechanism
- Use the joystick to control an LED brightness via PWM
- Build a simple menu navigator using joystick directions + button confirm
- Add deadzone filtering around center (e.g., ignore values within 480-544)
