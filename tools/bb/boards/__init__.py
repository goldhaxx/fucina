"""Board data loader — loads pin layout YAML files by board name."""

from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


_BOARDS_DIR = Path(__file__).parent


def load_board(name: str) -> dict | None:
    """Load a board definition by name.

    Searches for ``<name>.yaml`` in the boards directory.
    Returns the parsed dict, or None if the file doesn't exist
    or PyYAML is unavailable.
    """
    if yaml is None:
        return None
    path = _BOARDS_DIR / f"{name}.yaml"
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))
