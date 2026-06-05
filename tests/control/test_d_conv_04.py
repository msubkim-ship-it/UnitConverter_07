"""D-CONV-04 — FR-05: yard → meter reverse conversion."""

import pytest

from control.conversion_service import convert_unit

# TC ID: D-CONV-04


def test_d_conv_04_yard_to_meter():
    result = convert_unit(2.7, "yard", "meter")
    assert result == pytest.approx(2.5, abs=0.05)
