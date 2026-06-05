"""U-CFG-01 — FR-07: load units from config file."""

from pathlib import Path

from boundary.config_loader import load_units_config
from entity.constants import FEET_PER_METER, METER_RATIO, YARD_PER_METER

# TC ID: U-CFG-01


def test_u_cfg_01_load_units_config():
    config_path = Path(__file__).resolve().parents[2] / "config" / "units.json"
    config = load_units_config(config_path)
    assert config["base_unit"] == "meter"
    assert config["units"]["meter"] == METER_RATIO
    assert config["units"]["feet"] == FEET_PER_METER
    assert config["units"]["yard"] == YARD_PER_METER
    assert config["precision"] == 1
