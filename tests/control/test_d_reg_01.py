"""D-REG-01 — FR-08: dynamic unit registration enables conversion."""

import pytest

from control.conversion_service import convert_unit, parse_registration
from control.unit_registry import UnitRegistry

# TC ID: D-REG-01


def test_d_reg_01_dynamic_registration_conversion():
    registry = UnitRegistry()
    unit_name, meter_ratio = parse_registration("1 cubit = 0.4572 meter")
    registry.register(unit_name, meter_ratio)
    result = convert_unit(1.0, "cubit", "meter", ratios=registry.ratios)
    assert result == pytest.approx(0.5, abs=0.05)
