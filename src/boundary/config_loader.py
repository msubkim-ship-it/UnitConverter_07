"""Load unit configuration from JSON (FR-07)."""

import json
from pathlib import Path

from entity.constants import UNIT_RATIOS


def load_units_config(path: Path) -> dict:
    """Load units config; ratios reference entity SSOT values."""
    data = json.loads(path.read_text(encoding="utf-8"))
    units = data.get("units", {})
    result = {
        "base_unit": data.get("base_unit", "meter"),
        "units": {name: float(ratio) for name, ratio in units.items()},
        "precision": int(data.get("precision", 1)),
    }
    for name, ratio in UNIT_RATIOS.items():
        if name in result["units"]:
            result["units"][name] = ratio
    return result
