"""D-CONV-01 — FR-05: meter → feet conversion accuracy."""

import pytest

from control.conversion_service import convert_unit

# TC ID: D-CONV-01


def test_d_conv_01_meter_to_feet():
    result = convert_unit(2.5, "meter", "feet")
    assert result == pytest.approx(8.2, abs=0.05)
