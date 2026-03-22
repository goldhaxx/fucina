# Implementation Plan: 004 — Joystick Lights

> Created: 2026-03-21
> Based on: conversation (no formal spec)

## Objective

Create sketch 004 that combines 5 LEDs with a KY-023 joystick, where joystick position selects and controls LED animation effects in real time.

## Effects Matrix

| Joystick Position | Effect | Speed Control |
|---|---|---|
| Center (rest) | Sync pulse — all LEDs breathe together | Fixed ~2s cycle |
| X-axis right | Sequential chase right (1→2→3→4→5) | Faster with more deflection |
| X-axis left | Sequential chase left (5→4→3→2→1) | Faster with more deflection |
| Y-axis up | Random twinkle — LEDs flicker randomly | Faster with more deflection |
| Y-axis down | Ripple — wave expands outward from center LED | Faster with more deflection |

## Hardware

- **LEDs:** Same 5 LEDs from sketch 003 (pins 9, 10, 11, 5, 6 — all PWM-capable)
- **Joystick:** KY-023 — VRx→A0, VRy→A1, SW→Pin 2, powered from 5V/GND
- **Board:** HERO XL (Mega 2560)
- **Joystick placement:** Below the LED array on the breadboard (rows 45+), using right bank (f-j) to keep wiring clean

## Sequence

### Step 1: Create sketch directory and wiring.yaml

- **Test:** `python3 tools/validate-wiring.py` passes; SVG generates without error
- **Implement:** Create `sketches/004-joystick-lights/wiring.yaml` combining the 5-LED layout from 003 with the joystick module. Place joystick in right bank below the LEDs. Add all signal, power, and ground wires.
- **Files:** `sketches/004-joystick-lights/wiring.yaml`, `sketches/004-joystick-lights/wiring.svg`
- **Verify:** SVG renders correctly with all components visible; `validate-wiring.py` clean

### Step 2: Scaffold the sketch (platformio.ini + minimal main.cpp)

- **Test:** `pio run -e mega` compiles clean
- **Implement:** Create `platformio.ini` (same as 003 — no external libs needed). Create `src/main.cpp` with pin constants, `setup()` initializing LED outputs and joystick input, and an empty `loop()`. Pin assignments must match wiring.yaml exactly.
- **Files:** `sketches/004-joystick-lights/platformio.ini`, `sketches/004-joystick-lights/src/main.cpp`
- **Verify:** Compiles with zero warnings

### Step 3: Joystick input reading with dead zone

- **Test:** Upload to board, verify serial output shows X/Y values and correct zone detection
- **Implement:** Add joystick reading logic: `analogRead(A0)` for X, `analogRead(A1)` for Y, `digitalRead(2)` for button. Define a dead zone around center (~512 ± 80). Map joystick position to one of 5 zones: center, left, right, up, down. Calculate deflection magnitude (0.0–1.0) for speed control. Print zone + magnitude to serial for debugging.
- **Files:** `src/main.cpp`
- **Verify:** Serial monitor shows zone transitions as joystick moves; center dead zone is stable

### Step 4: Sync pulse effect (center/rest position)

- **Test:** Upload, leave joystick centered — all 5 LEDs should breathe in unison
- **Implement:** Non-blocking pulse using `millis()` — no `delay()` calls so the loop can read joystick every iteration. Use sine-wave or triangle-wave brightness curve. All LEDs get the same PWM value each frame.
- **Files:** `src/main.cpp`
- **Verify:** Smooth ~2-second pulse cycle; releasing joystick from any direction returns to pulse

### Step 5: Sequential chase effects (X-axis left/right)

- **Test:** Upload, push joystick right → LEDs chase 1→5; push left → LEDs chase 5→1
- **Implement:** Non-blocking chase: track current LED index and last-step timestamp. Step interval = `map(deflection, 0, 1, 200, 40)` — slow when barely tilted, fast when fully tilted. On each step, light current LED, dim previous. Direction determined by X-axis sign.
- **Files:** `src/main.cpp`
- **Verify:** Chase direction matches joystick; speed visibly changes with deflection amount

### Step 6: Random twinkle effect (Y-axis up)

- **Test:** Upload, push joystick up → LEDs twinkle randomly; speed increases with deflection
- **Implement:** Non-blocking: on each tick, randomly toggle one LED on or off using `analogWrite()` with random brightness. Tick interval = `map(deflection, 0, 1, 150, 20)`. More deflection = more frenetic flashing.
- **Files:** `src/main.cpp`
- **Verify:** Twinkle is random-feeling; gentle push = slow shimmer, full push = rapid flicker

### Step 7: Ripple/wave effect (Y-axis down)

- **Test:** Upload, push joystick down → wave expands outward from center LED (LED 3)
- **Implement:** Non-blocking ripple: center LED (index 2) lights first, then indices 1+3, then 0+4 — expanding outward. Use PWM for smooth fade: each ring fades up then down as the wave passes. After the wave reaches the edges, restart. Step interval controlled by Y-axis deflection magnitude.
- **Files:** `src/main.cpp`
- **Verify:** Wave clearly radiates from center; speed responds to joystick push amount

### Step 8: Smooth transitions between effects

- **Test:** Upload, sweep joystick between zones — transitions should be clean, no stuck LEDs
- **Implement:** When zone changes, call `allOff()` to reset LED state, then reinitialize the new effect's state variables. Add a brief transition: quick fade-out of current effect before starting new one (optional, skip if it feels responsive enough without it).
- **Files:** `src/main.cpp`
- **Verify:** No ghost LEDs when switching effects; snappy response to zone changes

### Step 9: Write README.md

- **Test:** N/A (documentation)
- **Implement:** Document the sketch: what it does, parts list, wiring reference, build commands, effect descriptions. Reference `wiring.svg` for the visual diagram.
- **Files:** `sketches/004-joystick-lights/README.md`
- **Verify:** README accurately describes behavior and wiring

## Risks

- **Joystick center drift:** Analog joysticks rarely read exactly 512 at rest. The dead zone in Step 3 (±80) should handle this, but may need tuning on the actual hardware.
- **PWM flicker during fast reads:** Reading analog pins takes ~100μs each. With 2 reads + LED updates per loop iteration, the loop should still run >1kHz — fast enough for smooth PWM. No risk here.
- **Pin conflict:** A0 is used as `randomSeed()` source in 003 — in 004 it's the joystick X-axis. Use A2 (floating) for randomSeed instead.
- **Non-blocking timing:** All effects must use `millis()`-based timing, not `delay()`. This is critical for responsive joystick reading. Sketch 003's `pulseRandom()` already demonstrates this pattern.

## Definition of Done

- [ ] All 5 effects work and respond to joystick position
- [ ] Speed scales with deflection magnitude for chase, twinkle, and ripple
- [ ] Transitions between effects are clean (no stuck LEDs)
- [ ] Dead zone keeps pulse stable when joystick is at rest
- [ ] Compiles with zero warnings
- [ ] wiring.yaml validates clean; wiring.svg is generated
- [ ] README.md documents all effects and wiring
- [ ] Code reviewed (run /review)
