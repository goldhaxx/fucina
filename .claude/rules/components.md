# Component Integration Rules

## Before Writing Code for a Component

1. Check `docs/inventory.md` for an existing entry. If missing, add one with full specs before proceeding.
2. Check `docs/wiring-patterns.md` for the circuit pattern this component uses. Add if missing.
3. Check `docs/pinouts.md` for pin conflicts with other components in the same sketch.
4. Check `docs/renderers.md` to know which `type:` value to use in `wiring.yaml`.

## When a New Component Enters the Project

A component is "new" if it doesn't have an entry in `docs/inventory.md`. The `/new-component` command handles the full onboarding flow, but if you're adding a component outside that workflow:

- Always add the inventory entry first — other devs need to know what's available.
- Note the operating voltage. Never connect 5V signals to 3.3V-only components without a level converter.
- Pin library dependencies with exact versions in `platformio.ini` (`lib_deps`).
- If the component uses I2C, check the I2C Address Map in inventory for conflicts.

## Component Types in wiring.yaml

Every physical component on the breadboard should be declared in the `components:` section of `wiring.yaml`. Use the type that matches the component (see `docs/renderers.md` for the full list). If no renderer exists for the component type, use `type: sensor` with a `label:` as a fallback — it renders as a generic green PCB module.

Components that connect via jumper wires but don't physically sit on the breadboard (servos, external modules, LCD shields) should use `type: module` with a `name:` label.
