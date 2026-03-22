#!/usr/bin/env python3
"""Validate wiring.yaml files against the component specs registry.

Cross-references component entries in wiring.yaml against
docs/component-specs.yaml to catch dimension mismatches, missing
models, and pin count errors before they become wrong diagrams.

Usage:
    python3 tools/validate-wiring.py                          # validate all sketches
    python3 tools/validate-wiring.py sketches/001-blink/wiring.yaml  # validate one file

Exit codes:
    0 = all pass
    1 = failures found
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_specs(search_from: Path) -> dict:
    """Find and load docs/component-specs.yaml by walking up from search_from."""
    d = search_from if search_from.is_dir() else search_from.parent
    for ancestor in [d, *d.parents]:
        candidate = ancestor / "docs" / "component-specs.yaml"
        if candidate.is_file():
            return yaml.safe_load(candidate.read_text(encoding="utf-8")) or {}
    return {}


def validate_file(yaml_path: Path, specs: dict) -> tuple[list[str], list[str], list[str]]:
    """Validate one wiring.yaml file against the specs registry.

    Returns (passes, warnings, failures).
    """
    passes = []
    warnings = []
    failures = []

    if not yaml_path.is_file():
        failures.append(f"File not found: {yaml_path}")
        return passes, warnings, failures

    text = yaml_path.read_text(encoding="utf-8")
    circuit = yaml.safe_load(text)
    if not circuit:
        warnings.append("Empty or unparseable YAML")
        return passes, warnings, failures

    components = circuit.get("components", [])
    if not components:
        passes.append("No components to validate")
        return passes, warnings, failures

    for i, comp in enumerate(components):
        comp_type = comp.get("type", "unknown")
        model = comp.get("model", "")
        label = f"component[{i}] type={comp_type}"
        if model:
            label += f" model={model}"

        # Check 1: model key present?
        if not model:
            if comp_type in ("module",):
                passes.append(f"{label}: module type — model not required")
            else:
                warnings.append(f"{label}: no model specified — physical dimensions not validated")
            continue

        # Check 2: model exists in specs?
        if model not in specs:
            failures.append(f"{label}: model '{model}' not found in component-specs.yaml")
            continue

        spec = specs[model]

        # Check 3: renderer type matches?
        expected_renderer = spec.get("renderer", "")
        if expected_renderer and expected_renderer != comp_type:
            failures.append(
                f"{label}: type '{comp_type}' doesn't match spec renderer '{expected_renderer}'"
            )

        # Check 4: pin count matches? (for types that declare pins)
        spec_pins = spec.get("pins")
        comp_pins = comp.get("pins")
        if spec_pins and comp_pins and isinstance(comp_pins, int):
            if comp_pins != spec_pins:
                failures.append(
                    f"{label}: pins={comp_pins} but spec says pins={spec_pins}"
                )
            else:
                passes.append(f"{label}: pin count matches ({comp_pins})")

        # Check 5: seven_segment digit count matches?
        spec_digits = spec.get("digits")
        comp_digits = comp.get("digits")
        if spec_digits and comp_digits:
            if comp_digits != spec_digits:
                failures.append(
                    f"{label}: digits={comp_digits} but spec says digits={spec_digits}"
                )

        # Check 6: body_mm present in spec?
        if not spec.get("body_mm"):
            warnings.append(f"{label}: spec exists but has no body_mm dimensions")
        else:
            passes.append(f"{label}: spec has body dimensions {spec['body_mm']}mm")

        # Check 7: datasheet URL present?
        if not spec.get("datasheet"):
            warnings.append(f"{label}: spec has no datasheet URL")

    return passes, warnings, failures


def main():
    parser = argparse.ArgumentParser(
        description="Validate wiring.yaml files against component specs.")
    parser.add_argument("files", nargs="*",
                        help="wiring.yaml files to validate (default: all in sketches/)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Only show warnings and failures")
    args = parser.parse_args()

    # Find files to validate
    project_root = Path(__file__).resolve().parent.parent
    if args.files:
        yaml_files = [Path(f) for f in args.files]
    else:
        yaml_files = sorted((project_root / "sketches").rglob("wiring.yaml"))

    if not yaml_files:
        print("No wiring.yaml files found.", file=sys.stderr)
        sys.exit(1)

    # Load specs once
    specs = load_specs(yaml_files[0])
    if not specs:
        print("WARNING: Could not find docs/component-specs.yaml", file=sys.stderr)

    total_pass = 0
    total_warn = 0
    total_fail = 0

    for yf in yaml_files:
        passes, warnings, failures = validate_file(yf, specs)
        total_pass += len(passes)
        total_warn += len(warnings)
        total_fail += len(failures)

        # Determine status
        if failures:
            status = "FAIL"
        elif warnings:
            status = "WARN"
        else:
            status = "PASS"

        # Print results
        rel = yf.relative_to(Path.cwd()) if yf.is_relative_to(Path.cwd()) else yf
        print(f"\n{status}  {rel}")

        if not args.quiet:
            for p in passes:
                print(f"  + {p}")
        for w in warnings:
            print(f"  ? {w}")
        for f in failures:
            print(f"  x {f}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Validated {len(yaml_files)} files: "
          f"{total_pass} pass, {total_warn} warn, {total_fail} fail")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
