# 004 — Joystick Lights

**Board:** HERO XL (Mega 2560)

Control 5 LEDs with a joystick. Each joystick direction triggers a different light effect, and the deflection amount controls the animation speed.

## Effects

| Direction | Effect | Speed |
|-----------|--------|-------|
| Center | Sync pulse — all LEDs breathe together | Fixed ~2s cycle |
| Right | Sequential chase →  (LED 1→2→3→4→5) | Faster with deflection |
| Left | Sequential chase ← (LED 5→4→3→2→1) | Faster with deflection |
| Up | Random twinkle — LEDs flicker randomly | Faster with deflection |
| Down | Ripple — wave expands outward from center | Faster with deflection |

## Parts

| Component | Qty | Notes |
|-----------|-----|-------|
| LED (5mm, assorted colors) | 5 | Red, green, blue, white, yellow |
| 220Ω resistor | 5 | Current limiting for each LED |
| HW-504 Joystick Module | 1 | Dual-axis analog + push button |
| Jumper wires | ~18 | Signal, power, ground |

## Wiring

![Breadboard diagram](wiring.svg)

### Pin Assignments

| Component | Pin | Type |
|-----------|-----|------|
| Red LED | 9 | PWM output |
| Green LED | 10 | PWM output |
| Blue LED | 11 | PWM output |
| White LED | 5 | PWM output |
| Yellow LED | 6 | PWM output |
| Joystick VRx | A0 | Analog input (X-axis) |
| Joystick VRy | A1 | Analog input (Y-axis) |
| Joystick SW | 2 | Digital input (button) |

### Power

- 5V and GND from HERO XL to breadboard power rails
- LEDs share a GND bus on the negative rail
- Joystick powered from the positive rail

## Build

```bash
cd sketches/004-joystick-lights
pio run -e mega        # Compile
pio run -t upload      # Upload to board
pio device monitor     # Serial monitor (9600 baud)
```

## Notes

- Joystick center reads ~512 on each axis. A dead zone of ±80 keeps the pulse effect stable at rest.
- All effects use `millis()`-based timing (no `delay()`) for responsive joystick reading.
- Zone changes print to serial for debugging.
- `randomSeed(analogRead(A2))` uses a floating pin for entropy since A0 is the joystick.
