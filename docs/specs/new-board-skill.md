# Feature: /new-board Skill — Deterministic Board Onboarding

> Feature: new-board-skill
> Created: 1774327268
> Status: Draft

## Summary

Create a `/new-board` slash command (or skill) that automates the full process of onboarding a new MCU board into the breadboard diagram system. Given a board make/model, the process researches pin layout data, generates a board YAML data file, validates it, and tests rendering — following the same steps used to onboard the HERO XL but with deterministic tooling replacing manual research.

## Job To Be Done

**When** I want to add support for a new board (e.g., ESP32, Arduino Uno, Raspberry Pi Pico),
**I want to** run `/new-board <make> <model>` and have a guided, repeatable process,
**So that** the board data file is created correctly without re-discovering the workflow each time.

## Acceptance Criteria

- [ ] **AC-1:** `/new-board` command exists and triggers a multi-phase guided workflow.
- [ ] **AC-2:** Phase 1 (Research): the command launches a research agent to find the board's physical pin header layout from official sources (KiCad footprints, datasheets, manufacturer docs). Returns structured pin data.
- [ ] **AC-3:** Phase 2 (Generate): a deterministic script (`scripts/generate-board-yaml.sh` or Python equivalent) converts the structured pin data into a `tools/bb/boards/<name>.yaml` file following the hero-xl.yaml schema.
- [ ] **AC-4:** Phase 3 (Validate): a deterministic script validates the generated YAML: required fields present, pin IDs are unique (excluding shared GND/5V), dimensions are positive, pin positions are within board bounds.
- [ ] **AC-5:** Phase 4 (Test): generates a test SVG with the new board and a sample circuit, opens for visual verification.
- [ ] **AC-6:** Phase 5 (Register): adds the board to `docs/inventory.md` if not already present, and commits the new board data file.
- [ ] **AC-7:** The workflow produces the same output structure regardless of which board is being onboarded. The only stochastic step is the initial research (Phase 2); all other phases are deterministic.
- [ ] **AC-8:** A validation script (`scripts/validate-board.sh` or `tools/validate-board.py`) can be run standalone to check any board YAML file against the schema.

## Affected Files

| File | Change |
|------|--------|
| `.claude/commands/new-board.md` | New — slash command definition |
| `scripts/validate-board.py` | New — board YAML validation script |
| `tools/bb/boards/hero-xl.yaml` | Reference — schema template |

## Dependencies

- **Requires:** Board renderer feature (complete — `tools/bb/mcu.py`, `tools/bb/boards/`)

## Out of Scope

- Automatic KiCad footprint parsing (research agent handles this stochastically)
- Board-specific renderer customizations (all boards use the same `McuBoard` renderer)
- Automated testing against real wiring.yaml files (Phase 5 uses a synthetic test circuit)

## Implementation Notes

- Pattern: follows `/new-component` command structure (multi-phase, research + deterministic steps)
- The hero-xl.yaml file serves as the schema reference — the validation script checks against the same structure
- Pin ID normalization uses the existing `_normalize_pin_id()` helper from `bb/geometry.py`
- The research phase should extract from KiCad `.kicad_mod` files when available (most Arduino boards have open KiCad libraries)
