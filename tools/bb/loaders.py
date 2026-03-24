"""YAML loading utilities and component specs cache."""

from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def load_circuit(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return _parse_yaml_simple(text)


_SPECS_CACHE: dict | None = None


def load_component_specs(path: str | None = None) -> dict:
    """Load the component specs registry (docs/component-specs.yaml).

    Searches for the file by walking up from the given path (or CWD) until
    it finds docs/component-specs.yaml. Returns an empty dict if not found
    or if PyYAML is unavailable. Caches the result for the process lifetime.
    """
    global _SPECS_CACHE
    if _SPECS_CACHE is not None:
        return _SPECS_CACHE

    if yaml is None:
        _SPECS_CACHE = {}
        return _SPECS_CACHE

    # Search upward for docs/component-specs.yaml
    search = Path(path).resolve() if path else Path.cwd()
    if search.is_file():
        search = search.parent
    for ancestor in [search, *search.parents]:
        candidate = ancestor / "docs" / "component-specs.yaml"
        if candidate.is_file():
            _SPECS_CACHE = yaml.safe_load(candidate.read_text(encoding="utf-8")) or {}
            return _SPECS_CACHE

    _SPECS_CACHE = {}
    return _SPECS_CACHE


def _parse_yaml_simple(text: str) -> dict:
    result = {}
    current_list = None
    current_item = None

    for raw_line in text.splitlines():
        stripped = raw_line.split("#")[0].rstrip()
        if not stripped:
            continue
        indent = len(raw_line) - len(raw_line.lstrip())

        if indent == 0 and ":" in stripped:
            if current_list is not None and current_item is not None:
                current_list.append(current_item)
                current_item = None
            key, val = stripped.split(":", 1)
            val = val.strip().strip('"').strip("'")
            if not val:
                result[key.strip()] = []
                current_list = result[key.strip()]
            else:
                result[key.strip()] = _coerce(val)
                current_list = None
        elif stripped.lstrip().startswith("- "):
            if current_list is not None and current_item is not None:
                current_list.append(current_item)
            current_item = {}
            pair = stripped.lstrip()[2:]
            if ":" in pair:
                k, v = pair.split(":", 1)
                current_item[k.strip()] = _coerce(v.strip().strip('"').strip("'"))
        elif ":" in stripped and current_item is not None:
            k, v = stripped.strip().split(":", 1)
            current_item[k.strip()] = _coerce(v.strip().strip('"').strip("'"))

    if current_list is not None and current_item is not None:
        current_list.append(current_item)
    return result


def _coerce(val: str):
    if not val:
        return ""
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val
