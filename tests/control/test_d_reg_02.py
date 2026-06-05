"""D-REG-02 — FR-15: duplicate registration → E007."""

import pytest

from control.conversion_service import ConversionError
from control.unit_registry import UnitRegistry
from entity.exceptions import ErrorCode

# TC ID: D-REG-02


def test_d_reg_02_duplicate_registration_e007():
    registry = UnitRegistry()
    with pytest.raises(ConversionError) as exc_info:
        registry.register("meter", 1.0)
    assert exc_info.value.code is ErrorCode.E007
