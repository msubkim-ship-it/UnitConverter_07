"""D-LOC-03 — FR-LOC-03: BASE_UNIT SSOT in entity.constants."""

from entity.constants import BASE_UNIT, DEFAULT_UNITS, UNIT_RATIOS

# TC ID: D-LOC-03


def test_d_loc_03_base_unit_ssot():
    # Given: BASE_UNIT defined only in entity.constants (FR-LOC-03)
    # When: SSOT is read
    # Then: base unit is canonical meter key with ratio 1.0
    assert BASE_UNIT in UNIT_RATIOS
    assert UNIT_RATIOS[BASE_UNIT] == 1.0
    assert DEFAULT_UNITS[0] == BASE_UNIT
