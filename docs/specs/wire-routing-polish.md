# Feature: Wire Routing Visual Polish — Spacing and Labels

> Feature: wire-routing-polish
> Created: 1774327551
> Status: Complete

## Summary

Routed wires in dense circuits (e.g., 004-joystick-lights with 10 wires) bunch together and overlap, making individual wires indistinguishable. Two improvements: enforce minimum padding between parallel wire segments, and add inline pill labels on longer wire runs so users can identify wires without tracing back to the legend.

## Job To Be Done

**When** I look at a diagram with many routed wires,
**I want to** clearly distinguish each wire and know what it connects without tracing to the legend,
**So that** I can wire the circuit correctly without confusion.

## Acceptance Criteria

### Wire Spacing

- [x] **AC-1:** Parallel wire segments in the routing gap have a minimum spacing of `WIRE_SPACING` (currently 5px) between them. No two wire segments occupy the same pixel column.
- [x] **AC-2:** When the routing gap is too narrow to fit all wires at minimum spacing, the gap is automatically widened (increase `MCU_GAP` dynamically based on wire count).
- [x] **AC-3:** Wire segments that cross other wires have a visual distinction at the crossing point (e.g., a small gap/bridge in one wire, or a dot at the junction) to make crossings explicit rather than ambiguous.

### Inline Wire Labels

- [x] **AC-4:** Wires longer than a threshold (e.g., > 100px total path length) get an inline pill label placed at the midpoint of their longest segment.
- [x] **AC-5:** The pill label shows the wire's label text (from `wiring.yaml`) or the pin name if no label is provided.
- [x] **AC-6:** Pill labels are positioned to avoid overlapping other wires or labels. If overlap would occur, the label shifts along the wire segment.
- [x] **AC-7:** Pill labels use the wire's color as the pill fill (matching the existing pill-label visual style).
- [x] **AC-8:** Short wires (< threshold) do not get inline labels to avoid clutter.

### Channel Assignment Improvements

- [x] **AC-9:** Channel assignment considers the Y-span of each wire's vertical segment. Wires whose vertical segments overlap in Y range must be in different channels (no shared channel for wires that would visually merge).
- [x] **AC-10:** The number of channels scales with wire count — at least `ceil(N / 2)` distinct channel positions for N wires, ensuring visual separation even when destinations are close together.

## Affected Files

| File | Change |
|------|--------|
| `tools/bb/router.py` | Modified — spacing enforcement, dynamic gap, inline labels, improved channel assignment |
| `tools/bb/mcu.py` | Modified — dynamic MCU_GAP based on wire count |
| `tools/bb/constants.py` | Modified — add WIRE_LABEL_THRESHOLD, WIRE_CROSSING_GAP constants |
| `sketches/*/wiring.svg` | Modified — regenerated |

## Dependencies

- **Requires:** Board renderer feature (complete)
- **Benefits from:** obstacle-avoidance spec (can be done independently)

## Out of Scope

- Interactive hover/tooltip on wires (SVG is static)
- Wire bundling/grouping (treating GND wires as a bus)
- Color-blind accessible wire differentiation (separate concern)

## Implementation Notes

- The current `_assign_channels()` sorts by destination Y — this is a good start but doesn't account for vertical segment overlap. Two wires going to rows 7 and 11 may share a channel if their vertical segments don't overlap, but two going to rows 7 and 8 should not.
- Inline pill labels follow the same visual pattern as the existing legend pills: colored rounded rect + white text. Font size 6-7px to fit on the wire without overwhelming the diagram.
- For crossing visualization, the simplest approach is a small white gap in the under-wire at the crossing point (the "bridge" pattern used in circuit schematics).
