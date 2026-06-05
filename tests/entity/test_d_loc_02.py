"""D-LOC-02 — FR-LOC-02: entity.exceptions ErrorCode E001~E007 SSOT."""

from entity.exceptions import ErrorCode

# TC ID: D-LOC-02

_EXPECTED = ("E001", "E002", "E003", "E004", "E005", "E006", "E007")


def test_d_loc_02_error_code_enum_ssot():
    # Given: ErrorCode SSOT in entity.exceptions (FR-LOC-02)
    # When: all enum members are collected
    members = tuple(ErrorCode)
    names = {member.name for member in members}
    values = {member.value for member in members}

    # Then: exactly E001~E007 — Logic assert by code, not user message
    assert len(members) == 7
    assert names == set(_EXPECTED)
    assert values == set(_EXPECTED)
    for code in _EXPECTED:
        assert getattr(ErrorCode, code).value == code
