# Active Buzzer — Simple Alarm

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 010

Produces a 1-second beep followed by 1-second silence in a loop. The active buzzer has a built-in oscillator — just apply voltage and it sounds. No `tone()` needed.

**Identifying your buzzer:** The active buzzer has a **sealed/closed bottom** and makes a continuous tone when touched to a 9V battery. The passive buzzer has an **open bottom** and only clicks.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-active-buzzer/wiring.yaml -o sketches/craftingtable/ct-active-buzzer/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x active buzzer (the one with the sealed bottom)
- 2x jumper wires

## Step-by-Step Wiring

### 1. Place the buzzer

The active buzzer has 2 pins and a polarity marking (+ or longer pin).

- **Positive (+)** pin into hole **a10**
- **Negative (-)** pin into hole **a11**

### 2. Connect jumper wires

- **Wire 1 (signal — orange):** From **a10** to **Pin 2** on the HERO XL
- **Wire 2 (ground — black):** From **a11** to **GND** on the HERO XL

## Build and Upload

```bash
cd sketches/craftingtable/ct-active-buzzer
pio run -e mega -t upload
```

You should hear a beeping pattern — 1 second on, 1 second off.

## What to Try Next

- Change `ON_LENGTH` and `OFF_LENGTH` for different rhythms
- Use shorter pulses (50ms on, 200ms off) for a rapid chirp alarm
- Combine with a PIR sensor to make a motion-triggered alarm
