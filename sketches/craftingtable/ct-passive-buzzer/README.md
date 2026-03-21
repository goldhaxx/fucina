# Passive Buzzer — Tone Generator

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Part Tutorial 020

Plays a 440 Hz tone (A4 note) for 1 second, pauses 1 second, repeats. The passive buzzer has no built-in oscillator — you control the frequency with `tone()`, so you can play melodies.

**Identifying your buzzer:** The passive buzzer has an **open bottom / exposed circuit board** and only clicks when touched to a 9V battery (no sustained tone). The active buzzer has a sealed bottom.

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-passive-buzzer/wiring.yaml -o sketches/craftingtable/ct-passive-buzzer/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x passive buzzer (the one with the open bottom)
- 2x jumper wires

## Step-by-Step Wiring

### 1. Place the buzzer

Same wiring as the active buzzer — the passive buzzer also has 2 pins with polarity.

- **Positive (+)** pin into hole **a10**
- **Negative (-)** pin into hole **a11**

### 2. Connect jumper wires

- **Wire 1 (signal — purple):** From **a10** to **Pin 2** on the HERO XL
- **Wire 2 (ground — black):** From **a11** to **GND** on the HERO XL

## Build and Upload

```bash
cd sketches/craftingtable/ct-passive-buzzer
pio run -e mega -t upload
```

You should hear a clear 440 Hz tone (the note A above middle C) playing for 1 second, then silence for 1 second.

## What to Try Next

- Change `TONE_PITCH` to play different notes: 262 (C4), 330 (E4), 392 (G4), 523 (C5)
- Play a simple melody by calling `tone()` with different frequencies in sequence
- Look up RTTTL (Ring Tone Text Transfer Language) format for playing real ringtones
