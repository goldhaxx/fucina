# Implementation Plan: Breadboard Component Renderers

> Created: 2026-03-21
> Based on: user request to render all physical components onto wiring.svg diagrams

## Objective

Add visual renderers to `tools/breadboard.py` for every component type used across sketches, update all `wiring.yaml` files to declare their components, and regenerate all SVGs so every diagram shows what's physically on the breadboard.

## Current State

**Existing renderers:** `resistor`, `led`, `button` (new), `buzzer` (new), `sensor` (new)

**Missing renderers needed:**

| Renderer | Visual concept | Sketches |
|----------|---------------|----------|
| `potentiometer` | 3-pin knob, circular body | ct-potentiometer |
| `seven_segment_1` | 10-pin DIP spanning center channel | ct-7seg-1digit |
| `seven_segment_4` | 12-pin DIP spanning center channel, wider | ct-7seg-4digit, ct-alarm-clock |
| `rgb_led` | 4-pin LED with R/G/B color indicators | ct-rgb-led |
| `dip` | Generic multi-pin IC/module spanning center channel | ct-lcd1602 (as off-board labeled box) |
| `module` | Off-board labeled box at board edge (like board pins but for modules) | ct-servo, ct-stepper, ct-rfid, ct-rtc, ct-gyroscope, ct-ir-receiver, ct-rotary-encoder, ct-joystick, ct-keypad, ct-radar-sweep, ct-rfid-lock, ct-lcd1602 |

**Key design decision:** Components fall into two categories:
1. **On-board** — physically in breadboard holes. Draw at hole coordinates. (potentiometer, 7-seg, button, buzzer, RGB LED)
2. **Off-board modules** — connect via jumper wires but sit outside the breadboard. Draw as labeled boxes at the board edge, similar to board-pin pills. (servo, stepper, RFID, RTC, gyroscope, keypad, IR receiver, rotary encoder, joystick, LCD)

The existing `sensor` renderer (green PCB rectangle) covers on-board sensor modules. The `module` renderer will handle off-board components by drawing a labeled pill/box at the left margin showing what the wires connect to — visually similar to the board-pin labels but styled as a module.

## Sequence

### Step 1: Potentiometer renderer
- **Implement:** Add `render_potentiometer()` — draws a circular knob with 3 pin leads. Takes `pin1`, `pin2`, `pin3` keys (or `from`/`to` shorthand for the 3 consecutive holes).
- **Files:** `tools/breadboard.py`
- **Verify:** Create a test YAML with `type: potentiometer`, generate SVG, inspect visually.

### Step 2: RGB LED renderer
- **Implement:** Add `render_rgb_led()` — draws a multi-color LED with 4 pins (red, common, green, blue). Shows the 3 color channels as small colored dots around a central white/clear lens.
- **Files:** `tools/breadboard.py`
- **Verify:** Test YAML with `type: rgb_led`, generate SVG, inspect.

### Step 3: 7-segment display renderer
- **Implement:** Add `render_seven_segment()` — draws a DIP-style IC package spanning the center channel. The body rectangle covers both banks (columns a–e and f–j). Pin dots on both sides. Shows a stylized "8" digit pattern on the body. Accepts `pins_left` and `pins_right` arrays, or auto-calculates from a `row_start` and `num_pins` config. Single renderer handles both 1-digit (10 pins) and 4-digit (12 pins) via a `digits` parameter.
- **Files:** `tools/breadboard.py`
- **Verify:** Test with both 1-digit and 4-digit configs.

### Step 4: Module renderer (off-board components)
- **Implement:** Add `render_module()` — draws a labeled box at the left edge of the board (similar to board-pin pills but wider/taller). The box shows the module name (e.g., "SG90 Servo", "DS3231 RTC", "HC-SR04"). Wires from this box go to the breadboard holes where jumpers connect. Accepts `name`, `color`, and a list of `pins` with their hole addresses.
- **Files:** `tools/breadboard.py`
- **Verify:** Test with a 3-pin module (VCC, SIG, GND) and a 5-pin module.

### Step 5: Update wiring.yaml for simple on-board components
- **Implement:** Add component entries to wiring.yaml files for sketches that use on-board components already supported by renderers:
  - `ct-potentiometer` — add `type: potentiometer`
  - `ct-push-button` — add `type: button`
  - `ct-active-buzzer` — add `type: buzzer, variant: active`
  - `ct-passive-buzzer` — add `type: buzzer, variant: passive`
  - `ct-rgb-led` — add `type: rgb_led`
  - `ct-rtttl-alarm` — add `type: buzzer, variant: passive`
  - `ct-photoresistor` — add `type: sensor, label: LDR` (the LDR itself, resistor already there)
- **Files:** 7 `wiring.yaml` files
- **Verify:** Regenerate SVGs, inspect each.

### Step 6: Update wiring.yaml for 7-segment displays
- **Implement:** Add 7-segment component entries:
  - `ct-7seg-1digit` — add `type: seven_segment, digits: 1`
  - `ct-7seg-4digit` — add `type: seven_segment, digits: 4`
  - `ct-alarm-clock` — add `type: seven_segment, digits: 4` (plus buzzer)
- **Files:** 3 `wiring.yaml` files
- **Verify:** Regenerate SVGs, inspect.

### Step 7: Update wiring.yaml for off-board modules
- **Implement:** Add module component entries to all sketches that use external modules connected via jumper wires:
  - `ct-pir-motion` — `type: module, name: HC-SR501`
  - `ct-ultrasonic` — `type: module, name: HC-SR04`
  - `ct-sound-sensor` — `type: module, name: KY-038`
  - `ct-dht-sensor` — `type: module, name: DHT11` (resistor already there)
  - `ct-rain-sensor` — `type: module, name: HW-038`
  - `ct-joystick` — `type: module, name: KY-023`
  - `ct-gyroscope` — `type: module, name: GY-521`
  - `ct-ir-receiver` — `type: module, name: KY-022`
  - `ct-rotary-encoder` — `type: module, name: KY-040`
  - `ct-servo` — `type: module, name: SG90`
  - `ct-stepper` — `type: module, name: ULN2003`
  - `ct-rtc` — `type: module, name: DS3231`
  - `ct-rfid` — `type: module, name: RC522`
  - `ct-keypad` — `type: module, name: 4x4 Keypad`
  - `ct-lcd1602` — `type: module, name: LCD1602`
  - `ct-ir-receiver` — `type: module, name: KY-022`
- **Files:** ~16 `wiring.yaml` files
- **Verify:** Regenerate SVGs, inspect.

### Step 8: Update wiring.yaml for chapter project sketches
- **Implement:** Add component entries for multi-component chapter projects:
  - `ct-security-motion` — add `type: module, name: HC-SR501` (LED + resistor already there)
  - `ct-keypad-lock` — add `type: module, name: 4x4 Keypad`
  - `ct-rfid-lock` — add `type: module, name: RC522` + `type: module, name: LCD1602`
  - `ct-plant-monitor` — add `type: module, name: HW-038` (LED already there)
  - `ct-clap-lights` — add `type: module, name: KY-038`
  - `ct-alarm-clock` — add buzzer + RTC module (7-seg from step 6)
  - `ct-radar-sweep` — add `type: module, name: HC-SR04` + `type: module, name: SG90`
  - `ct-wifi-lights` — add `type: led` (simple, on ESP32)
- **Files:** ~8 `wiring.yaml` files
- **Verify:** Regenerate all SVGs, inspect.

### Step 9: Batch regenerate all SVGs and verify
- **Implement:** Run breadboard.py on every sketch's wiring.yaml to regenerate all SVGs. Compile-check still passes (SVG changes don't affect compilation, but sanity-check).
- **Files:** All `wiring.svg` files
- **Verify:** `for d in sketches/*/wiring.yaml sketches/craftingtable/*/wiring.yaml; do python3 tools/breadboard.py "$d" -o "${d%.yaml}.svg"; done` — no errors.

### Step 10: Update sketches.md rule with new component types
- **Implement:** Update `.claude/rules/sketches.md` wiring.yaml schema section to document the new component types (`potentiometer`, `rgb_led`, `seven_segment`, `button`, `buzzer`, `sensor`, `module`) with their required keys.
- **Files:** `.claude/rules/sketches.md`
- **Verify:** Schema examples cover all new types.

## Risks

- **Visual quality:** SVG renderers are approximations. Components like the 7-segment display have complex pin layouts — the renderer needs to look good enough to be useful without being pixel-perfect. Mitigation: keep renderers simple, focus on recognizability over accuracy.
- **Module renderer overlap:** Multiple off-board modules stacked at the left edge could visually overlap. Mitigation: auto-stack module boxes vertically based on the y-coordinate of their connected wires.
- **Existing SVGs change:** Regenerating SVGs for sketches that already had correct diagrams (001-blink, etc.) will produce visually identical output since no new components are added. Low risk.

## Definition of Done

- [ ] All 6 new renderer types produce valid SVG output
- [ ] Every sketch's `wiring.yaml` declares all physical components
- [ ] All `wiring.svg` files regenerated with components visible
- [ ] No breadboard.py crashes on any wiring.yaml
- [ ] `sketches.md` documents all component types
