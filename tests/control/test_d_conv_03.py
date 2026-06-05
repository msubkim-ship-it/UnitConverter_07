"""D-CONV-03 — FR-05: feet → meter reverse conversion."""

import pytest

from control.conversion_service import convert_unit

# TC ID: D-CONV-03


def test_d_conv_03_feet_to_meter():
    result = convert_unit(8.2, "feet", "meter")
    assert result == pytest.approx(2.5, abs=0.05)
