"""D-ERR-06 — FR-14: registration syntax error → E006."""

import pytest

from control.conversion_service import ConversionError, parse_registration
from entity.exceptions import ErrorCode

# TC ID: D-ERR-06


@pytest.mark.parametrize("raw", ["cubit 0.4572", "1 cubit 0.4572 meter", "bad = form"])
def test_d_err_06_registration_syntax_e006(raw: str):
    with pytest.raises(ConversionError) as exc_info:
        parse_registration(raw)
    assert exc_info.value.code is ErrorCode.E006
