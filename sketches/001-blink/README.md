# 001 — Blink

**Board:** HERO XL (Mega 2560)

Blinks an external LED on pin 9 at 1 Hz (500 ms on, 500 ms off).

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for a visual breadboard layout showing exactly where each component goes.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/001-blink/wiring.yaml -o sketches/001-blink/wiring.svg
```

## Parts

Grab these from your kit:

- HERO XL board
- USB A-B cable (the thick printer-style USB cable)
- 830-point breadboard (the big one)
- 1x LED (any color from the Circuits Essentials bag)
- 1x 220 ohm resistor (bands: red, red, brown, gold)
- 2x jumper wires from the rigid jumper wire kit (any colors — I suggest red and black)

## Step-by-Step Wiring

### 1. Orient the breadboard

Place the 830-point breadboard on your desk horizontally, with the long side facing you. You'll see:

- **Power rails** along the top and bottom edges (marked with red `+` and blue `-` lines)
- **Numbered rows** (1, 2, 3...) running left to right
- **Lettered columns** (a through j) running top to bottom
- A **center channel** dividing the board into a top half (rows a-e) and bottom half (rows f-j)

Each group of 5 holes in a row (like a1-e1) is electrically connected. The center channel breaks the connection.

### 2. Place the LED

Pick up your LED. Notice one leg is longer than the other:

- **Long leg = anode (+)** — this is the positive side
- **Short leg = cathode (-)** — this is the negative/ground side

Push the LED into the breadboard:

- **Long leg (anode)** into hole **e10**
- **Short leg (cathode)** into hole **e11**

The LED should straddle two rows, standing upright.

### 3. Place the 220 ohm resistor

The resistor doesn't have a direction — either way works.

- One leg into hole **d7**
- Other leg into hole **d10**

This connects the resistor to the same row as the LED's long leg (row 10).

### 4. Connect the jumper wires

**Wire 1 (signal — I suggest red):**
- One end into hole **a7** on the breadboard (same row as one end of the resistor)
- Other end into the **pin labeled 9** on the HERO XL's digital header (the double row of pins along the edge of the board — pin 9 is printed on the board)

**Wire 2 (ground — I suggest black):**
- One end into hole **a11** on the breadboard (same row as the LED's short leg)
- Other end into any pin labeled **GND** on the HERO XL (there are several — pick whichever is closest)

### 5. What you should have

The electrical path goes:

```
HERO XL Pin 9 → jumper wire → row 7 → resistor → row 10 → LED anode (+)
                                                             LED cathode (-) → row 11 → jumper wire → HERO XL GND
```

Visual layout on the breadboard:

```
        col:  7    8    9    10   11
             ─────────────────────────
row a:   [wire to pin 9]          [wire to GND]
row b:
row c:
row d:   [resistor leg]------[resistor leg]
row e:                        [LED +]  [LED -]
```

### 6. Connect the board to your computer

Plug the USB A-B cable from the HERO XL to your computer. The flat rectangular end (Type A) goes into your computer. The square end (Type B) goes into the HERO XL.

You should see a small green power LED light up on the HERO XL board.

## Build and Upload

From the project root:

```bash
cd sketches/001-blink
pio run -e mega -t upload
```

Within a few seconds, your LED should start blinking — half a second on, half a second off.

## Troubleshooting

- **LED doesn't light up at all:** Check that the long leg is in row 10 (same row as the resistor) and the short leg is in row 11 (same row as the GND wire). If it's backwards, the LED won't be damaged — just flip it around.
- **Upload fails with "no device found":** Make sure the USB cable is plugged in firmly. Try a different USB port. Some USB-C hubs don't pass through serial devices properly — connect directly if possible.
- **LED is very dim:** Double-check the resistor value. 220 ohm should give a clear, bright light. If you accidentally grabbed a 10K or 100K resistor, it will be very dim.

## What to Try Next

- Change the `delay(500)` values in `src/main.cpp` to make it blink faster or slower
- Try `delay(100)` for a fast strobe, or `delay(2000)` for a slow pulse
- Try an asymmetric pattern: `delay(100)` for on, `delay(900)` for off — a quick flash every second
