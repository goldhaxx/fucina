# fucina

A personal hardware forge for prototyping with Arduino and ESP32 components.

## Tech Stack
- Platform: PlatformIO (build system and dependency management)
- Language: C / C++ (Arduino framework)
- Boards: HERO XL (ATmega2560 / Mega 2560), LilyGo TTGO T-Display ESP32
- IDE: Google Antigravity (preferred), Cursor, VS Code

## Commands
```bash
pio run -e mega             # Compile for HERO XL (Mega 2560)
pio run -e esp32            # Compile for TTGO T-Display ESP32
pio run -t upload           # Compile and upload to connected board
pio device monitor          # Open serial monitor (9600 baud default)
pio test                    # Run unit tests (native/desktop)

# Wiring diagrams
python3 tools/breadboard.py sketches/NNN-name/wiring.yaml -o sketches/NNN-name/wiring.svg
python3 tools/breadboard.py sketches/NNN-name/wiring.yaml --rows 1-63 -o full.svg  # show all rows
```

## Architecture
```
sketches/                   # One directory per project/experiment
├── 001-blink/              # Numbered for chronological order
│   ├── src/main.cpp        # Sketch source
│   ├── platformio.ini      # Board + library config for this sketch
│   ├── wiring.yaml         # Machine-readable circuit description
│   ├── wiring.svg          # Generated breadboard diagram (do not hand-edit)
│   └── README.md           # What it does, wiring, notes
├── 002-servo-sweep/
└── ...
tools/
└── breadboard.py           # SVG breadboard diagram generator
lib/                        # Shared helper libraries across sketches
docs/
├── inventory.md            # Full component list with specs and status
├── pinouts.md              # Board pin maps and breadboard reference
├── wiring-patterns.md      # Common circuit recipes
├── renderers.md            # Breadboard diagram component types reference
├── course-map.md           # Maps Crafting Table course lessons to local sketches
├── journal.md              # Build log — what worked, what didn't, ideas
├── spec.md                 # Current feature specification
├── plan.md                 # Implementation plan
└── checkpoint.md           # Progress state for session continuity
```

## Workflow: Explore → Wire → Code → Verify

1. **Pick a component.** Check `docs/inventory.md` for what's available. For a brand-new component, run `/new-component` — it researches specs, updates inventory, and creates the sketch.
2. **Create the sketch directory.** Next number in sequence, e.g. `sketches/002-servo-sweep/`.
3. **Write `wiring.yaml`.** Describe every component and wire on the breadboard. Check `docs/renderers.md` for supported component types.
4. **Generate `wiring.svg`.** Run `python3 tools/breadboard.py sketches/NNN/wiring.yaml -o sketches/NNN/wiring.svg`.
5. **Wire it up.** Follow the generated diagram. Document anything extra in `README.md`.
6. **Write the sketch.** Simplest possible code that proves the component works.
7. **Upload and verify.** Flash to board, open serial monitor, confirm behavior.
8. **Iterate.** Combine components. Try weird ideas. Create a new sketch directory.
9. **Log it.** Note what you learned in sketch README or `docs/journal.md`.

## Conventions
- Each sketch is self-contained with its own `platformio.ini`.
- Sketch directories are numbered (`001-`, `002-`, ...) to preserve build order.
- Every sketch MUST have a `wiring.yaml` and a generated `wiring.svg` breadboard diagram.
- Pin assignments go in `pins.h` or top of `main.cpp` — never buried in logic.
- Pin assignments in `main.cpp` must match the holes and board pins in `wiring.yaml`.
- Use `constexpr` or `#define` for pin numbers. No magic integers.
- Note the target board in each sketch README header (`Board: HERO XL` or `Board: TTGO ESP32`).
- ESP32 GPIO is 3.3V. HERO XL GPIO is 5V. Use the logic level converter between them.

## Reference Documents
### Scaffold Guide — @GUIDE.md
**Read when:** Adding or modifying scaffold commands, rules, agents, skills, hooks, or scripts. Update its diagrams and tables to reflect the change.

### Component Inventory — @docs/inventory.md
**Read when:** Starting a new sketch, checking available parts, looking up specs or datasheets.

### Pinout Reference — @docs/pinouts.md
**Read when:** Wiring a circuit. Pin maps for HERO XL and TTGO ESP32.

### Wiring Patterns — @docs/wiring-patterns.md
**Read when:** Setting up voltage dividers, pull-up/pull-down resistors, motor drivers.

### Build Journal — @docs/journal.md
**Read when:** Picking up after a break. Chronological notes on builds and open questions.

### Breadboard Diagram Tool — @tools/breadboard.py
**Read when:** Creating or modifying a sketch's wiring. Generates SVG breadboard diagrams from YAML circuit descriptions. See any sketch's `wiring.yaml` for the schema.

### Diagram Renderer Reference — @docs/renderers.md
**Read when:** Writing `wiring.yaml` component entries. Lists all supported `type:` values with their required keys and visual description.

### Course Map — @docs/course-map.md
**Read when:** Checking which Crafting Table course lessons have been converted to local sketches.

## Do Not
- Do not connect 5V signals to ESP32 GPIO — use the logic level converter.
- Do not drive motors or relays directly from GPIO pins — use driver boards or transistors.
- Do not overwrite prior sketches — they form a learning trail. Iterate by creating new directories.
- Do not install PlatformIO libraries globally — scope them to each sketch's `platformio.ini`.
