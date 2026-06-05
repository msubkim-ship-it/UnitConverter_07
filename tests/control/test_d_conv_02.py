"""D-CONV-02 — FR-05: meter → yard conversion accuracy."""

import pytest

from control.conversion_service import convert_unit

# TC ID: D-CONV-02


def test_d_conv_02_meter_to_yard():
    result = convert_unit(2.5, "meter", "yard")
    assert result == pytest.approx(2.7, abs=0.05)
