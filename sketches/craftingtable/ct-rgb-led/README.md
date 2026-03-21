# RGB LED — Color Cycling

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 004

Cycles through red, green, blue, white, and purple colors using PWM (`analogWrite`) to mix RGB values. Each color holds for 1 second.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rgb-led/wiring.yaml -o sketches/craftingtable/ct-rgb-led/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x RGB LED (common cathode — 4 pins, longest pin is GND)
- 3x 220Ω resistors (bands: red, red, brown, gold)
- 4x jumper wires

## Step-by-Step Wiring

### 1. Identify the RGB LED pins

The RGB LED has 4 pins. The **longest pin** is the common cathode (GND). Looking at the LED from the flat side:

```
Red — Common GND (longest) — Green — Blue
```

### 2. Place the LED

Insert the 4 pins into consecutive rows on the breadboard:
- **Red** leg into **e10**
- **Common GND** (longest) into **e11**
- **Green** leg into **e12**
- **Blue** leg into **e14**

### 3. Place the 220Ω resistors

Each color pin needs a current-limiting resistor:
- **Resistor 1 (red):** From **d7** to **d10** (connects to red leg's row)
- **Resistor 2 (green):** From **d8** to **d12** (connects to green leg's row)
- **Resistor 3 (blue):** From **d9** to **d14** (connects to blue leg's row)

### 4. Connect jumper wires

- **Wire 1 (red):** From **a7** to **Pin 7** on the HERO XL
- **Wire 2 (green):** From **a8** to **Pin 6** on the HERO XL
- **Wire 3 (blue):** From **a9** to **Pin 5** on the HERO XL
- **Wire 4 (ground — black):** From **a11** to **GND** on the HERO XL

### 5. Electrical path

```
Pin 7 → 220Ω → Red LED leg
Pin 6 → 220Ω → Green LED leg    → Common cathode → GND
Pin 5 → 220Ω → Blue LED leg
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-rgb-led
pio run -e mega -t upload
```

You should see the LED cycle through: red → green → blue → white → purple, holding each color for 1 second.

## What to Try Next

- Add a potentiometer to control the hue
- Create a smooth rainbow fade using sine waves or HSV-to-RGB conversion
- Use a button to cycle through preset colors
