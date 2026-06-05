"""D-ERR-04 — FR-12: unregistered unit → E004."""

import pytest

from control.conversion_service import ConversionError, convert_unit
from entity.exceptions import ErrorCode

# TC ID: D-ERR-04


def test_d_err_04_unregistered_unit_e004():
    with pytest.raises(ConversionError) as exc_info:
        convert_unit(1.0, "cubit", "meter")
    assert exc_info.value.code is ErrorCode.E004
