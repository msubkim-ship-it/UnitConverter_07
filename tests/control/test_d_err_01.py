"""D-ERR-01 — FR-11: format error → E001."""

import pytest

from control.conversion_service import ConversionError, parse_unit_value
from entity.exceptions import ErrorCode

# TC ID: D-ERR-01


@pytest.mark.parametrize("raw", ["", "meter2.5", "   "])
def test_d_err_01_format_error_e001(raw: str):
    with pytest.raises(ConversionError) as exc_info:
        parse_unit_value(raw)
    assert exc_info.value.code is ErrorCode.E001
