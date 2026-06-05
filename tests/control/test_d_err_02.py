"""D-ERR-02 — FR-11: number parse failure → E002."""

import pytest

from control.conversion_service import ConversionError, parse_unit_value
from entity.exceptions import ErrorCode

# TC ID: D-ERR-02


def test_d_err_02_number_parse_e002():
    with pytest.raises(ConversionError) as exc_info:
        parse_unit_value("meter:abc")
    assert exc_info.value.code is ErrorCode.E002
