"""D-ERR-05 — FR-13: empty unit name → E005."""

import pytest

from control.conversion_service import ConversionError, parse_unit_value
from entity.exceptions import ErrorCode

# TC ID: D-ERR-05


def test_d_err_05_empty_unit_name_e005():
    with pytest.raises(ConversionError) as exc_info:
        parse_unit_value(":2.5")
    assert exc_info.value.code is ErrorCode.E005
