"""D-ERR-03 — FR-10: negative value → E003."""

import pytest

from control.conversion_service import ConversionError, parse_unit_value
from entity.exceptions import ErrorCode

# TC ID: D-ERR-03


def test_d_err_03_negative_value_e003():
    with pytest.raises(ConversionError) as exc_info:
        parse_unit_value("meter:-2.5")
    assert exc_info.value.code is ErrorCode.E003
