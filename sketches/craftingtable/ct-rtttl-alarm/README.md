# RTTTL Alarm — Melody Player

**Board:** HERO XL (Mega 2560)
**Source:** Crafting Table course — Chapter 02, Lesson 04

Plays RTTTL (Ring Tone Text Transfer Language) melodies through a passive buzzer. RTTTL was Nokia's ringtone format from the late 1990s — a compact text encoding for monophonic melodies. This sketch includes several classic tunes as commented-out alternatives: Never Gonna Give You Up (default), Star Wars, Mission Impossible, Indiana Jones, The Simpsons, Take On Me, Jeopardy, The Flintstones, and M*A*S*H.

**RTTTL format:** `name:d=<default_duration>,o=<default_octave>,b=<bpm>:<notes>` where each note is `[duration]<letter>[#][.][octave]`. For example, `8c#.6` is an eighth-note dotted C-sharp in octave 6. The `p` note is a rest (pause). You can find thousands of RTTTL songs online at sites like [adamonsoon/rtttl-parse](https://github.com/adamonsoon/rtttl-parse) or by searching "RTTTL songs collection."

## Wiring Diagram

Open [`wiring.svg`](wiring.svg) for the visual breadboard layout.

To regenerate after changes:
```bash
python3 tools/breadboard.py sketches/craftingtable/ct-rtttl-alarm/wiring.yaml -o sketches/craftingtable/ct-rtttl-alarm/wiring.svg
```

## Parts

- HERO XL board + USB A-B cable
- 830-point breadboard
- 1x passive buzzer (the one with the open bottom / exposed circuit board)
- 2x jumper wires

## Step-by-Step Wiring

### 1. Place the buzzer

- **Positive (+)** pin into hole **a10**
- **Negative (-)** pin into hole **a11**

### 2. Connect jumper wires

- **Wire 1 (signal — purple):** From **a10** to **Pin 24** on the HERO XL
- **Wire 2 (ground — black):** From **a11** to **GND** on the HERO XL

## Build and Upload

```bash
cd sketches/craftingtable/ct-rtttl-alarm
pio run -e mega -t upload
```

Open the serial monitor to see playback status:
```bash
pio device monitor
```

You should hear the melody playing through the buzzer, with BPM and song metadata printed to serial.

## What to Try Next

- Uncomment a different `song` line in `main.cpp` to play another melody
- Search online for "RTTTL songs" and paste new song strings into the code
- Add a button to cycle through songs, or a potentiometer to control playback speed
- Chain multiple songs together for a jukebox effect
