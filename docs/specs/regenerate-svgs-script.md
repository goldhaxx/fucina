# Feature: Deterministic SVG Regeneration Script

> Feature: regenerate-svgs
> Created: 1774327268
> Status: Draft

## Summary

Extract the repeated "loop over all sketches and regenerate SVGs" pattern into a deterministic script. This pattern has been performed manually in at least 4 sessions (sessions 7, 8, and twice in the board-renderer session), consuming context each time for the same computable operation.

## Job To Be Done

**When** I modify the breadboard rendering pipeline and need to regenerate all sketch SVGs,
**I want to** run one command (`scripts/regenerate-svgs.sh` or `python3 tools/regenerate-svgs.py`),
**So that** all SVGs are regenerated deterministically without Claude writing a for loop each time.

## Acceptance Criteria

- [ ] **AC-1:** A single script command regenerates all `wiring.svg` files from their `wiring.yaml` sources.
- [ ] **AC-2:** The script discovers all `wiring.yaml` files automatically (no hardcoded list).
- [ ] **AC-3:** The script reports which files were regenerated and whether any changed (`git diff --stat` integration).
- [ ] **AC-4:** A `--dry-run` flag shows which files would be regenerated without writing them.
- [ ] **AC-5:** A `--check` flag exits non-zero if any SVGs are stale (useful for CI/hooks).
- [ ] **AC-6:** Exit code 0 on success, non-zero on any generation failure.

## Affected Files

| File | Change |
|------|--------|
| `scripts/regenerate-svgs.sh` | New — SVG regeneration script |
| `CLAUDE.md` | Modified — add command to Commands section |

## Dependencies

- **Requires:** None (uses existing `tools/breadboard.py`)

## Out of Scope

- Watch mode / auto-regeneration on file change
- Parallel generation (not needed at current scale)

## Implementation Notes

- Pattern: `find sketches/ -name wiring.yaml | while read yaml; do ... done`
- Should also handle `sketches/craftingtable/` subdirectories
- Consider adding as a post-commit hook or lint-on-write hook for wiring.yaml changes
