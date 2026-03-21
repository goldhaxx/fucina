# Keypad Door Lock — Secret Code Entry

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 02, Lesson 02

Enter a 4-digit secret code on the 4x4 membrane keypad to "unlock the door" (serial message). Press `*` to reset entry, `#` to delete the last character. If the code matches, the serial monitor prints an unlock message; otherwise it reports wrong code and resets.

Uses high-numbered pins (23-37 odd) to avoid conflicts with SPI, I2C, and PWM pins.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-keypad-lock/wiring.yaml -o sketches/craftingtable/ct-keypad-lock/wiring.svg
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

- **Wire 1 (red):** From **a5** to **Pin 23** (Row 1)
- **Wire 2 (orange):** From **a6** to **Pin 25** (Row 2)
- **Wire 3 (yellow):** From **a7** to **Pin 27** (Row 3)
- **Wire 4 (green):** From **a8** to **Pin 29** (Row 4)
- **Wire 5 (blue):** From **a9** to **Pin 31** (Col 1)
- **Wire 6 (purple):** From **a10** to **Pin 33** (Col 2)
- **Wire 7 (brown):** From **a11** to **Pin 35** (Col 3)
- **Wire 8 (grey):** From **a12** to **Pin 37** (Col 4)

### 4. Circuit explanation

No external resistors or pull-ups are needed -- the Keypad library enables internal pull-ups and handles matrix scanning. It sets one row LOW at a time, then reads each column to detect which key (if any) is pressed in that row.

```
Rows (output, active LOW):  Pin 23, 25, 27, 29
Cols (input, pulled HIGH):  Pin 31, 33, 35, 37
```

The key layout matches a standard telephone/calculator arrangement:

```
 1  2  3  A
 4  5  6  B
 7  8  9  C
 *  0  #  D
```

### 5. How the lock works

- Type digits 0-9 or letters A-D to build up the code
- Press `*` to clear and start over
- Press `#` to delete the last character entered
- After 4 characters are entered, the code is checked automatically
- Default secret code is `1234` -- change `SECRET_CODE` in `main.cpp`

## Build and Upload

```bash
cd sketches/craftingtable/ct-keypad-lock
pio run -e mega -t upload
pio device monitor -b 9600
```

Press keys on the keypad to enter a code. The serial monitor shows each character as you type and reports whether the code is correct.

## What to Try Next

- Change the secret code to something longer or shorter
- Add a servo motor to physically lock/unlock a latch
- Add an LCD1602 display to show `*` characters as you type
- Add a lockout after 3 wrong attempts (with a timeout)
- Combine with an RGB LED for red (locked) / green (unlocked) feedback
