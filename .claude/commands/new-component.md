Onboard a new hardware component into the fucina project.

The user provides a make/model, part number, or identifying description. You research the component, then walk through a guided checklist to integrate it into the project.

## Phase 1: Research

1. Ask the user what they can tell you about the component — make, model, part number, any markings, where they bought it. Accept whatever they have.
2. Using that info, research the component:
   - Search for the official datasheet or product page
   - Find the operating voltage, pin count, interface type (digital, analog, I2C, SPI, UART, PWM)
   - Find the pinout (which pin does what)
   - Identify any required libraries for Arduino/PlatformIO
   - Note safety constraints (e.g., 3.3V only, max current, needs pull-up resistors)
   - Find example wiring diagrams or circuit patterns from documentation
3. Present a summary of what you found and confirm with the user before proceeding.

## Phase 2: Inventory

4. Read `docs/inventory.md` and check if this component already has an entry.
5. If missing, add it following the exact format of existing entries — include status `[ ]`, specs, interface, libraries, operating voltage, pin description, and any safety notes.
6. If the component uses I2C, update the I2C Address Map table.
7. If the component introduces a new wiring pattern not in `docs/wiring-patterns.md`, add the pattern.

## Phase 3: Renderer Check

8. Read `docs/renderers.md` to check if a matching breadboard renderer type exists for this component.
9. If no renderer exists, inform the user: "No breadboard renderer for [type] yet — the SVG will show wires but not the component body. A renderer can be added later."
10. If a renderer exists, note which `type:` value to use in wiring.yaml.

## Phase 4: Sketch Creation

11. Ask the user:
    - Which board? (HERO XL or ESP32)
    - What should the sketch do? (basic test? specific behavior?)
    - Sketch name preference? (default: next number in `sketches/` sequence)
12. Follow the sketch creation process from `.claude/rules/sketches.md`:
    - Create directory structure
    - Write `wiring.yaml` with all components and wires (pin assignments must avoid conflicts — check `docs/pinouts.md`)
    - Generate `wiring.svg`
    - Write `platformio.ini` with correct board and `lib_deps`
    - Write `src/main.cpp` — simplest code that proves the component works
    - Write `README.md`

## Phase 5: Verify

13. Compile with `pio run` to confirm the sketch builds.
14. Summarize what was created and what the user should do next (wire it up, upload, open serial monitor, etc.).
