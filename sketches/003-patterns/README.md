# 003 — Patterns

**Board:** HERO XL (Mega 2560)

Five LEDs with four selectable patterns, switchable live via Serial Monitor.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

The red LED from sketches 001/002 stays in place (rows 7-11, pin 9). Four new LED circuits are added below it with identical resistor-LED wiring.

### Ground Bus

The HERO XL only has 3 GND pins, but we need ground for all 5 LEDs. The solution is to use the breadboard's blue (-) power rail as a shared ground bus:

1. **One wire** from HERO XL GND to the blue (-) rail
2. **Short jumpers** from each LED's cathode row to the blue (-) rail

This is the standard way to distribute power/ground on a breadboard — the power rails run the full length of the board, so any number of circuits can tap into them.

### Pin Map

| LED    | Pin | Breadboard Rows |
|--------|-----|-----------------|
| Red    | 9   | 7–11            |
| Green  | 10  | 14–18           |
| Blue   | 11  | 21–25           |
| White  | 5   | 28–32           |
| Yellow | 6   | 35–39           |

All pins are PWM-capable for future fade effects.

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 5x LEDs (red, green, blue, white, yellow)
- 5x 220 ohm resistors (red, red, brown, gold)
- 11x jumper wires (1 GND bus + 5 signal + 5 ground-to-rail)

## Build & Upload

```bash
cd sketches/003-patterns
pio run -e mega -t upload
pio device monitor
```

## Usage

Open the Serial Monitor (9600 baud) after uploading. Send a number to switch patterns:

| Key | Pattern           | Description                                    |
|-----|-------------------|------------------------------------------------|
| 1   | Sequential Chase  | One LED at a time, sweeps back and forth        |
| 2   | All Blink         | All 5 LEDs blink on and off together            |
| 3   | Random Twinkle    | Random LEDs flicker like stars                  |
| 4   | Pattern Cycle     | Rotates through patterns 1-3, 5 seconds each   |

Starts in Chase mode (1) by default.

## How It Works

- Each LED has its own 220 ohm current-limiting resistor wired identically to the 001-blink circuit.
- `checkSerial()` runs between every pattern step so input is responsive even mid-animation.
- Pattern Cycle mode uses `millis()` timing to run each sub-pattern for 5 seconds before rotating.
- `randomSeed(analogRead(A0))` seeds the RNG from a floating analog pin for varied twinkle behavior.

## What to Try Next

- Add speed control (send `+`/`-` to adjust delay times)
- Add a fade/breathing pattern using `analogWrite` on these PWM pins
- Wire a physical button to cycle patterns without the serial monitor
