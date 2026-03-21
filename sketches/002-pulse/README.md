# 002 — Pulse

**Board:** HERO XL (Mega 2560)

Smoothly fades an LED from off to full brightness and back, creating a breathing/pulse effect using PWM.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

Same circuit as 001-blink — if your LED is still wired up from that sketch, you're ready to go.

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x LED (any color)
- 1x 220 ohm resistor (red, red, brown, gold)
- 2x jumper wires

## Build & Upload

```bash
cd sketches/002-pulse
pio run -e mega -t upload
```

## How It Works

Unlike 001-blink which used `digitalWrite` (fully on or fully off), this sketch uses `analogWrite` which outputs a **PWM signal** — the pin rapidly switches between on and off, and the ratio of on-time to off-time controls perceived brightness.

- `analogWrite(pin, 0)` = always off (0% duty cycle)
- `analogWrite(pin, 127)` = half brightness (50% duty cycle)
- `analogWrite(pin, 255)` = full brightness (100% duty cycle)

The loop ramps from 0 to 255 and back, with a 10 ms delay per step — one full breath cycle takes about 5 seconds.

## What to Try Next

- Change `STEP_DELAY_MS` to speed up or slow down the breathing
- Try a non-linear curve for a more natural-looking fade (the eye perceives brightness logarithmically)
