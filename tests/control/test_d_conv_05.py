"""D-CONV-05 — FR-06: feet ↔ yard indirect conversion via meter."""

import pytest

from control.conversion_service import convert_unit

# TC ID: D-CONV-05


def test_d_conv_05_feet_to_yard_indirect():
    result = convert_unit(8.2, "feet", "yard")
    assert result == pytest.approx(2.7, abs=0.05)


def test_d_conv_05_yard_to_feet_indirect():
    result = convert_unit(2.7, "yard", "feet")
    assert result == pytest.approx(8.1, abs=0.05)
