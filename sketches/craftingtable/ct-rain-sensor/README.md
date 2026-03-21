# Rain Sensor — Water Level Detection

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 050

Reads water level via the HW-038 rain/water level detection sensor and prints the analog value (0--1023) to serial once per second. Power is gated through Pin 7 so the sensor is only energized during reads -- this prevents corrosion of the exposed copper sensing traces over time.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rain-sensor/wiring.yaml -o sketches/craftingtable/ct-rain-sensor/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x HW-038 water level sensor board + control board (connected via included cable)
- 3x jumper wires

## Step-by-Step Wiring

### 1. Connect the sensor board to the control board

The HW-038 kit has two pieces: the sensor board (the flat board with exposed copper traces) and the control board (the small PCB with a potentiometer). Connect them with the included 2-pin cable.

### 2. Place the control board on the breadboard

The control board has 3 pins: **S** (signal), **+** (power), and **-** (ground). Insert them into the breadboard:

- **S** (signal) into hole **a10**
- **+** (power) into hole **a11**
- **-** (ground) into hole **a12**

### 3. Connect jumper wires

- **Wire 1 (signal -- green):** From **a10** to **A0** on the HERO XL analog header
- **Wire 2 (power gate -- orange):** From **a11** to **Pin 7** on the HERO XL digital header
- **Wire 3 (ground -- black):** From **a12** to **GND** on the HERO XL

### 4. Circuit explanation

Unlike most sensors, the power pin is not connected to 5V directly. Instead, Pin 7 acts as a power gate -- the code sets it HIGH only when taking a reading, then immediately sets it LOW. This prevents continuous current flow through the sensing traces, which would accelerate corrosion and degrade the sensor over time.

```
Pin 7 (power gate) → control board + → sensor board
A0 ← control board S (analog signal 0–1023)
GND → control board -
```

Higher analog readings mean more water on the sensor board.

## Build and Upload

```bash
cd sketches/craftingtable/ct-rain-sensor
pio run -e mega -t upload
pio device monitor -b 115200
```

Touch a wet finger to the sensor board -- the value rises. Dry it off -- the value drops back toward zero.

## What to Try Next

- Set a threshold value to classify "wet" vs "dry" and print a status label
- Add a buzzer that sounds an alarm when water is detected
- Combine with an LED to create a visual rain indicator (green = dry, red = wet)
