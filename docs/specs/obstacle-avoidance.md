# Feature: Wire Routing Obstacle Avoidance

> Feature: obstacle-avoidance
> Created: 1774327551
> Status: Draft

## Summary

The wire router's `collect_obstacles()` function is defined but never called. Wires from pins on the far side of the MCU board (power, analog) clip through the board body instead of routing around it. Enforce AC-7 from the board-renderer spec: no wire segment passes through the interior of the board graphic.

## Job To Be Done

**When** a wire connects a breadboard hole to a pin on the away-from-breadboard side of the MCU,
**I want to** see the wire route around the board body to reach the pin,
**So that** the diagram is physically accurate and visually clear.

## Acceptance Criteria

- [ ] **AC-1:** `route_wires()` calls `collect_obstacles()` and passes obstacle rects to path computation.
- [x] **AC-2:** No wire segment intersects the interior of the MCU board graphic bounding box. *(Done in wire-routing-polish session — far-side detection + perimeter routing)*
- [x] **AC-3:** Wires to far-side pins route around the board (over the top or under the bottom) with orthogonal segments. *(Done in wire-routing-polish session)*
- [ ] **AC-4:** Module card bounding boxes are also treated as obstacles when present.

## Dependencies

- **Requires:** Board renderer feature (complete)

## Out of Scope

- Full grid-based A* pathfinding (channel approach with obstacle-aware waypoints is sufficient)
