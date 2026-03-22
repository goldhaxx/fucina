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

## Phase 2: Physical Specs

4. From the datasheet, extract physical dimensions for the component:
   - Body dimensions in mm (width × height × depth)
   - Pin count, pin pitch (mm), pin diameter (mm)
   - Pin row spacing (mm) for DIP packages
   - Pin span (total distance from first to last pin on one side)
   - Any renderer-specific fields (digit face dimensions, slant angle, etc.)
5. Read `docs/component-specs.yaml` and check if this component already has an entry.
6. If missing, add a structured entry with all measured dimensions and the datasheet URL as the source. Follow the schema documented in the file header. Use the part number as the key (e.g., `5641AS`, `B3F-1000`). For generic commodities without part numbers, use a descriptive key (e.g., `axial-resistor-1/4W`, `led-5mm`).

This step is **mandatory** for components that sit on the breadboard (DIP, through-hole, on-board modules). It is optional for off-board modules (servos, LCDs connected via jumper wires) that render as labeled boxes.

## Phase 3: Inventory

7. Read `docs/inventory.md` and check if this component already has an entry.
8. If missing, add it following the exact format of existing entries — include status `[ ]`, specs, interface, libraries, operating voltage, pin description, and any safety notes. Include the physical dimensions from Phase 2.
9. If the component uses I2C, update the I2C Address Map table.
10. If the component introduces a new wiring pattern not in `docs/wiring-patterns.md`, add the pattern.

## Phase 4: Renderer Check

11. Read `docs/renderers.md` to check if a matching breadboard renderer type exists for this component.
12. If no renderer exists, inform the user: "No breadboard renderer for [type] yet — the SVG will show wires but not the component body. A renderer can be added later."
13. If a renderer exists, note which `type:` value and `model:` key to use in wiring.yaml.

## Phase 5: Sketch Creation

14. Ask the user:
    - Which board? (HERO XL or ESP32)
    - What should the sketch do? (basic test? specific behavior?)
    - Sketch name preference? (default: next number in `sketches/` sequence)
15. Follow the sketch creation process from `.claude/rules/sketches.md`:
    - Create directory structure
    - Write `wiring.yaml` with all components and wires. Include `model:` key on every component that has a specs entry. Pin assignments must avoid conflicts — check `docs/pinouts.md`.
    - Generate `wiring.svg`
    - Write `platformio.ini` with correct board and `lib_deps`
    - Write `src/main.cpp` — simplest code that proves the component works
    - Write `README.md`

## Phase 6: Verify

16. Run `python3 tools/validate-wiring.py sketches/NNN-name/wiring.yaml` to validate component specs.
17. Compile with `pio run` to confirm the sketch builds.
18. Summarize what was created and what the user should do next (wire it up, upload, open serial monitor, etc.).
