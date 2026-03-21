# Component Integration Rules

## Before Writing Code for a Component

1. Check `docs/inventory.md` for an existing entry. If missing, add one with full specs before proceeding.
2. **Look up the datasheet** for the component's physical dimensions — pin count, pin pitch, row spacing (for DIPs), operating voltage, interface type. These are non-negotiable inputs to the wiring.yaml.
3. Check `docs/wiring-patterns.md` for the circuit pattern this component uses. Add if missing.
4. Check `docs/pinouts.md` for pin conflicts with other components in the same sketch.
5. Check `docs/renderers.md` to know which `type:` value to use in `wiring.yaml`.
6. For DIP packages or components with an asymmetric face, determine the correct `orientation` value (see Orientation Model in `docs/renderers.md`).

## When a New Component Enters the Project

A component is "new" if it doesn't have an entry in `docs/inventory.md`. The `/new-component` command handles the full onboarding flow, but if you're adding a component outside that workflow:

- Always add the inventory entry first — other devs need to know what's available.
- Note the operating voltage. Never connect 5V signals to 3.3V-only components without a level converter.
- Pin library dependencies with exact versions in `platformio.ini` (`lib_deps`).
- If the component uses I2C, check the I2C Address Map in inventory for conflicts.

## Component Types in wiring.yaml

Every physical component on the breadboard should be declared in the `components:` section of `wiring.yaml`. Use the type that matches the component (see `docs/renderers.md` for the full list). If no renderer exists for the component type, use `type: sensor` with a `label:` as a fallback — it renders as a generic green PCB module.

Components that connect via jumper wires but don't physically sit on the breadboard (servos, external modules, LCD shields) should use `type: module` with a `name:` label.

## Physical Accuracy is Non-Negotiable

Hole addresses in wiring.yaml represent real physical positions on the breadboard. Every address must be derived from the component's datasheet dimensions, not assumed or simplified.

- **DIP packages** have pins on both sides of the breadboard. Left pins go in the left bank (a–e), right pins go in the right bank (f–j). The column depends on the DIP's row spacing — look it up, don't guess.
- **Jumper wires** connect a specific breadboard hole to a specific board pin. The `from:` hole must be in the correct column and row for the electrical connection to work.
- **Never put all connections on one bank** when the physical component spans both. This produces diagrams that don't match reality and would fail if someone tried to wire it.
- When in doubt, consult the datasheet. If no datasheet exists, measure the component or find a verified reference.
