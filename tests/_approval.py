"""Golden Master approval helper."""

import os
from pathlib import Path

_GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"


def golden_path(relative: str) -> Path:
    return _GOLDEN_ROOT / relative


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare *actual* text to ``tests/golden/{relative}``.

    Set ``UPDATE_GOLDEN=1`` to write or refresh the baseline file.
    """
    path = golden_path(relative)
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(
            f"Golden file missing: {path}\n"
            "Run with UPDATE_GOLDEN=1 to create the baseline."
        )

    expected = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Golden mismatch: {relative}\n"
            f"--- expected ({path}) ---\n{expected}"
            f"--- actual ---\n{actual}"
        )
