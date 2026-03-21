# 4x4 Keypad — Matrix Scanning

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 100

Reads key presses from a 4x4 membrane keypad using matrix scanning and prints each pressed key to the serial monitor. Only 8 digital pins are needed to scan all 16 keys -- the Keypad library handles row/column scanning automatically.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-keypad/wiring.yaml -o sketches/craftingtable/ct-keypad/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x 4x4 membrane keypad
- 8x jumper wires

## Step-by-Step Wiring

### 1. Orient the keypad ribbon cable

The keypad ribbon cable has 8 pins. The typical pinout from left to right (with the keys facing you) is:

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-----|---|---|---|---|---|---|---|---|
| Function | Row 1 | Row 2 | Row 3 | Row 4 | Col 1 | Col 2 | Col 3 | Col 4 |

**Note:** Pinout varies by manufacturer. If keys don't map correctly, swap rows and columns or test with a multimeter.

### 2. Insert the keypad ribbon into the breadboard

Insert the 8 ribbon cable pins into holes **a5** through **a12**, one pin per row:

- Pin 1 (Row 1) into **a5**
- Pin 2 (Row 2) into **a6**
- Pin 3 (Row 3) into **a7**
- Pin 4 (Row 4) into **a8**
- Pin 5 (Col 1) into **a9**
- Pin 6 (Col 2) into **a10**
- Pin 7 (Col 3) into **a11**
- Pin 8 (Col 4) into **a12**

### 3. Connect jumper wires to the HERO XL

Run a jumper wire from each breadboard row to the corresponding HERO XL digital pin:

- **Wire 1 (red):** From **a5** to **Pin 9** (Row 1)
- **Wire 2 (orange):** From **a6** to **Pin 8** (Row 2)
- **Wire 3 (yellow):** From **a7** to **Pin 7** (Row 3)
- **Wire 4 (green):** From **a8** to **Pin 6** (Row 4)
- **Wire 5 (blue):** From **a9** to **Pin 5** (Col 1)
- **Wire 6 (purple):** From **a10** to **Pin 4** (Col 2)
- **Wire 7 (brown):** From **a11** to **Pin 3** (Col 3)
- **Wire 8 (grey):** From **a12** to **Pin 2** (Col 4)

### 4. Circuit explanation

No external resistors or pull-ups are needed -- the Keypad library enables internal pull-ups and handles matrix scanning. It sets one row LOW at a time, then reads each column to detect which key (if any) is pressed in that row.

```
Rows (output, active LOW):  Pin 9, 8, 7, 6
Cols (input, pulled HIGH):  Pin 5, 4, 3, 2
```

The key layout matches a standard telephone/calculator arrangement:

```
 1  2  3  A
 4  5  6  B
 7  8  9  C
 *  0  #  D
```

## Build and Upload

```bash
cd sketches/craftingtable/ct-keypad
pio run -e mega -t upload
pio device monitor -b 115200
```

Press any key on the keypad -- the serial monitor prints the character. Try pressing multiple keys to see how the library handles simultaneous presses.

## What to Try Next

- Build a password entry system that unlocks after a correct 4-digit code
- Combine with a servo to create a keypad-controlled door lock
- Add an LCD1602 display to show typed characters
- Build a simple calculator using the number keys and `*`/`#` as operators
