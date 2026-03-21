# Research: Programmatic Breadboard Diagram Generation

> Date: 2026-03-20
> Goal: Find tools that can take a description of components/wires and output a visual breadboard diagram (SVG preferred), driven from code or config rather than a GUI.

---

## Executive Summary

**Best option for our use case: schemdraw (Python)**. It has a dedicated `pictorial` module with a `Breadboard` element, `ArduinoUno` support, component placement at named pin anchors, colored jumper wires, and SVG output -- all from pure Python code. It's actively maintained (v0.22, 2025), well-documented, and pip-installable.

**Runner-up: Wokwi diagram.json**. Define circuits in JSON, render via Wokwi's simulator. The CLI can take PNG screenshots of parts. The JSON format is clean and well-documented, but exporting a full diagram image requires the web UI or partial CLI screenshot support (per-part only).

**Honorable mention: Fritzing CLI**. Can export .fzz sketches to SVG from the command line (`fritzing -svg <folder>`), but you'd need to programmatically generate the .fzz files first (ZIP of XML), which is doable but verbose.

---

## Category 1: Existing Breadboard Visualization Tools

### Fritzing
- **URL:** https://fritzing.org / https://github.com/fritzing/fritzing-app
- **Scriptable:** Partially. CLI supports `-svg <folder>` to batch-export all views (breadboard, schematic, PCB) to SVG. Cannot select individual views from CLI.
- **Output:** SVG, PNG, PDF, Gerber
- **Maturity:** Very mature (10+ years), but development has slowed. Now requires purchase ($8).
- **CLI integration:** You could programmatically generate .fzz files (ZIP archives containing XML .fz sketch files) then run `fritzing -svg` to export. The XML format is well-documented (parts, wires, positions, transforms). This is a viable but heavyweight pipeline.
- **File format:** .fzz = ZIP containing .fz (XML). Parts reference SVG graphics. Wires have endpoint coordinates, colors, wireFlags (64 = breadboard wire). Positions use x/y + 3x3 transform matrices.
- **Verdict:** Feasible but requires generating XML and shelling out to the Fritzing binary. Not lightweight.

### Tinkercad Circuits
- **URL:** https://www.tinkercad.com/circuits
- **Scriptable:** No. Browser-only, no public API, no CLI. Export limited to PNG and Eagle format via GUI.
- **Verdict:** Not viable for automation.

### Circuit Canvas
- **URL:** https://circuitcanvas.com
- **Scriptable:** No. Web-based GUI tool. Exports SVG/PNG via UI. Can import Fritzing parts and custom SVG components. Has a Layout mode specifically for breadboard wiring diagrams.
- **Maturity:** Active development (by Oyvind Nydal Dahl). Custom parts use SVG import.
- **Verdict:** Good for manual diagrams, not automatable.

### EasyEDA
- **URL:** https://easyeda.com
- **Scriptable:** No public CLI or API. Web-based. Can export schematics as SVG/PNG/PDF/JSON, but only through the GUI.
- **Verdict:** Not viable for automation.

### DigiKey Scheme-It
- **URL:** https://www.digikey.com/en/schemeit
- **Scriptable:** No. Browser-based only. Exports SVG/PNG/PDF from the UI.
- **Verdict:** Not viable for automation.

---

## Category 2: The Top Contenders (Scriptable)

### schemdraw (Python) -- RECOMMENDED
- **URL:** https://schemdraw.readthedocs.io / https://pypi.org/project/schemdraw/
- **Version:** 0.22 (latest, actively maintained)
- **Install:** `pip install schemdraw`
- **Output:** SVG (primary for pictorial elements), PNG (via matplotlib backend)
- **Scriptable:** 100% Python API. Define everything in code.

**Pictorial module elements:**
- `Breadboard` -- full 830-point breadboard with anchors at every pin (A1-J30, L1_x, L2_x, R1_x, R2_x power rails)
- `ArduinoUno` -- via `ElementImage` with pin anchors (pin0-pin13, A0-A5, gnd1, gnd2, fivev, threev3, vin, reset, etc.)
- `Resistor(value)` -- renders with correct color bands (e.g., `Resistor(330)` shows orange-orange-brown)
- `LED`, `LEDOrange`, `LEDYellow`, `LEDGreen`, `LEDBlue`, `LEDWhite`
- `CapacitorCeramic`, `CapacitorMylar`, `CapacitorElectrolytic`
- `TO92` (transistor package)
- `Diode`
- `DIP(npins=N, wide=bool)` -- generic DIP ICs with configurable pin count
- `FritzingPart('file.fzpz')` -- imports any Fritzing part file (SVG backend only)

**Wiring example:**
```python
import schemdraw
import schemdraw.elements as elm
from schemdraw import pictorial

with schemdraw.Drawing() as d:
    ard = ArduinoUno()
    bb = pictorial.Breadboard().at((0, 9)).up()
    elm.Wire('n', k=-1).at(ard.gnd2).to(bb.L2_29).linewidth(4)
    elm.Wire().at(ard.pin12).to(bb.A14).color('red').linewidth(4)
    pictorial.LED().at(bb.E14)
    pictorial.Resistor(330).at(bb.D15).to(bb.L2_15)
    d.save('breadboard_demo.svg')
```

**Key strengths:**
- Pure Python, no external binaries needed
- Anchored component placement at specific breadboard holes
- Colored, routable wires between any anchors
- Can import Fritzing .fzpz parts for components not built in
- SVG output is clean and embeddable
- Constants: `pictorial.PINSPACING` = 0.1 inch standard

**Limitations:**
- FritzingPart requires SVG backend (not matplotlib)
- No built-in Mega 2560 or ESP32 board elements (but you could create them with `ElementImage` or `FritzingPart`)
- Wire routing is manual (you specify start/end points)
- Breadboard is fixed at ~30 rows (standard half-size), not a full 830-point

**Verdict:** Best fit for our workflow. Define circuits in Python, output SVG. Could wrap in a CLI script that reads YAML/JSON and generates diagrams.

### Wokwi diagram.json
- **URL:** https://wokwi.com / https://docs.wokwi.com/diagram-format
- **Scriptable:** Yes. Circuits defined in JSON. CLI available for headless simulation.
- **Output:** PNG screenshots via CLI (`--screenshot-part <id>`). Full diagram rendering is web-only.
- **Install CLI:** `npm install -g @wokwi/wokwi-cli` (requires API token from wokwi.com)

**diagram.json format:**
```json
{
  "version": 1,
  "parts": [
    {"id": "uno", "type": "wokwi-arduino-uno", "left": 160, "top": 200},
    {"id": "led1", "type": "wokwi-led", "left": 350, "top": 100, "attrs": {"color": "red"}},
    {"id": "r1", "type": "wokwi-resistor", "left": 350, "top": 150, "attrs": {"resistance": "220"}}
  ],
  "connections": [
    ["uno:13", "r1:1", "green", []],
    ["r1:2", "led1:A", "green", []],
    ["led1:C", "uno:GND", "black", []]
  ]
}
```

**Wire routing mini-language:** `["v10", "h5", "*", "v-15"]` for vertical/horizontal offsets.

**Key strengths:**
- Clean JSON format, easy to generate programmatically
- Huge part library (Arduino Uno, Mega, ESP32, breadboards, all common components)
- Beautiful rendered diagrams in the web UI
- VS Code extension available
- CLI supports headless simulation + per-part screenshots

**Limitations:**
- CLI screenshots capture individual parts, not full diagram view
- Full diagram export is a requested feature (GitHub issues #80, #345) but not implemented
- Requires API token (pricing unclear, likely freemium)
- The visual rendering engine is not open source -- it runs server-side

**Verdict:** Great JSON format for defining circuits. If you generate diagram.json files, you get simulation for free, and beautiful diagrams in the web UI. But no automated full-diagram SVG/PNG export yet.

---

## Category 3: SVG Generation Libraries (Build Your Own)

### svgwrite (Python)
- **URL:** https://pypi.org/project/svgwrite/
- **Status:** v1.4.3, UNMAINTAINED (author has moved on)
- **Use case:** Low-level SVG generation. You'd draw every breadboard hole, component, and wire manually.
- **Verdict:** Works but you'd build everything from scratch. Use schemdraw instead.

### drawsvg (Python)
- **URL:** https://pypi.org/project/drawsvg/ / https://github.com/cduck/drawSvg
- **Status:** v2.4.1, actively maintained
- **Use case:** General SVG generation with animation support, Jupyter widget rendering
- **Verdict:** More modern than svgwrite, but still no circuit primitives. Building-block level.

### svg.py (Python)
- **URL:** https://github.com/orsinium-labs/svg.py
- **Status:** Active, type-safe SVG generation
- **Verdict:** Clean API but same story -- you'd build all circuit primitives yourself.

### D3.js (JavaScript)
- **URL:** https://d3js.org
- **Use case:** Could render breadboard diagrams in browser/Node with SVG output.
- **Verdict:** Very powerful but massive overkill for static diagrams.

---

## Category 4: Adjacent/Niche Tools

### bblayout (Python)
- **URL:** https://github.com/patricksurry/bblayout
- **Status:** 3 commits, 0 stars, last updated 2024-03-19. Proof of concept.
- **What it does:** Python DSL for placing DIP components on breadboards and wiring them. Uses the `svg` Python library. Supports multi-breadboard layouts, power rails, DIP/SIP components, wire bundles with color coding.
- **Example API:** `cpu = DIP.new('W65C02'); layout.place(cpu @ layout.BB4.C8); layout.wiring(cpu.VDD - power.VDD, color='red')`
- **Verdict:** Interesting concept very close to what we want, but too immature/undocumented to use directly. Good reference for building our own.

### diagram-to-breadboard (Scala)
- **URL:** https://github.com/bartekkalinka/diagram-to-breadboard
- **Status:** 306 commits, 0 stars. Niche tool for converting ciat-lonbarde paper circuits.
- **What it does:** Takes circuit description as Scala data structures, algorithmically places components on a breadboard, renders interactive web visualization.
- **Verdict:** Interesting auto-placement algorithm, but very specialized and not reusable.

### svg_schematic (Python)
- **URL:** https://github.com/KenKundert/svg_schematic
- **Status:** v1.3, 31 stars, GPL-3.0. Updated July 2025.
- **What it does:** Generates SVG schematics (not breadboard views) from Python code. Components: Resistor, Capacitor, Inductor, Wire.
- **Verdict:** Schematic-only, no breadboard rendering.

### netlistsvg (JavaScript)
- **URL:** https://github.com/nturley/netlistsvg
- **Status:** Well-maintained, significant stars. Uses elkjs for layout.
- **What it does:** Renders SVG schematics from Yosys JSON netlists. Digital logic focused.
- **Verdict:** No breadboard support. Digital schematic only.

### pinout (Python)
- **URL:** https://github.com/j0ono0/pinout / https://pypi.org/project/pinout/
- **Status:** Active, MIT licensed.
- **What it does:** Generates hardware pinout diagrams as SVG. Define pin labels, groups, colors in Python, output SVG.
- **Verdict:** Adjacent tool -- great for documenting board pinouts (could complement breadboard diagrams), but doesn't render breadboards.

### SVG-PCB (JavaScript)
- **URL:** https://github.com/leomcelroy/svg-pcb
- **What it does:** Programmatic PCB design using JavaScript as an HDL. Outputs SVG and Gerber.
- **Verdict:** PCB design, not breadboard visualization.

### AACircuit (Python)
- **URL:** https://github.com/Blokkendoos/AACircuit
- **Status:** 604 commits, 165 stars. Python 3 + GTK.
- **What it does:** GUI tool for drawing electronic circuits with ASCII characters. Exports ASCII text.
- **Scriptable:** No -- GUI-driven. Component libraries loaded from JSON.
- **Verdict:** Not automatable in its current form.

### VirtualBreadboard (Commercial)
- **URL:** https://www.virtualbreadboard.com
- **Scriptable:** Has SVG export. Windows-only commercial software.
- **Verdict:** Not suitable for CLI automation.

---

## Category 5: ASCII/Text-Based Alternatives

| Tool | URL | Notes |
|------|-----|-------|
| AACircuit | https://github.com/Blokkendoos/AACircuit | GUI-based ASCII circuit editor, not scriptable |
| ASCIIFlow | https://asciiflow.com | General ASCII diagram editor, not circuit-specific |
| Textik | https://textik.com | ASCII diagram editor, browser-based |
| Diagon | https://arthursonzogni.com/Diagon/ | ASCII art generator for various diagram types |

**Verdict:** No good scriptable ASCII breadboard tools exist. The closest would be hand-crafting ASCII art or building a custom renderer.

---

## Recommended Approach

### Tier 1: Use schemdraw (Quickest Path to Working Tool)

```bash
pip install schemdraw
```

Write a Python script that:
1. Reads a YAML/JSON description of components and connections
2. Creates a `schemdraw.Drawing` with `pictorial.Breadboard()`
3. Places components at breadboard anchors
4. Draws colored wires between pins
5. Exports to SVG

**Estimated effort:** 1-2 sessions to build a working prototype.

**Gap to fill:** Need to create `ElementImage` definitions for boards not built in (HERO XL / Mega, TTGO ESP32). Can use Fritzing SVG parts via `FritzingPart`.

### Tier 2: Use Wokwi diagram.json (Best Visual Quality)

Write a script that generates diagram.json files from your circuit description. View in browser at wokwi.com or VS Code extension. Accept that full-diagram export is manual (screenshot from browser).

**Estimated effort:** <1 session to generate JSON. Ongoing manual step for export.

### Tier 3: Build Custom SVG Renderer (Most Control)

Use `drawsvg` or `svg.py` to build a breadboard renderer from scratch, inspired by the `bblayout` project's approach. Define breadboard geometry, component shapes, and wire routing.

**Estimated effort:** 3-5 sessions for a polished tool. Maximum flexibility.

---

## Quick Reference: Scriptability Matrix

| Tool | Scriptable | Output | Input Format | CLI | Quality |
|------|-----------|--------|-------------|-----|---------|
| **schemdraw** | Yes (Python) | SVG, PNG | Python code | No (library) | Good |
| **Wokwi** | Yes (JSON) | PNG (CLI), web render | diagram.json | Yes | Excellent |
| **Fritzing** | Partial | SVG, PNG | .fzz (XML in ZIP) | Yes | Excellent |
| Circuit Canvas | No | SVG, PNG | GUI only | No | Good |
| Tinkercad | No | PNG | GUI only | No | Excellent |
| EasyEDA | No | SVG, PNG | GUI only | No | Good |
| Scheme-It | No | SVG, PNG | GUI only | No | Good |
