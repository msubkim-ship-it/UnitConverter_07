"""D-LOC-01 — FR-LOC-01: entity.constants ratio SSOT (row-major G1)."""

# TC ID: D-LOC-01


def test_d_loc_01(grid_g1):
    # Given: grid_g1 — row-major G1 ratio tuple from entity.constants SSOT
    from entity.constants import FEET_PER_METER, METER_RATIO, YARD_PER_METER
    from entity.loc import find_blank_coords

    # When: find_blank_coords returns row-major ratio tuple from SSOT
    result = find_blank_coords()

    # Then: row-major G1 matches fixture and constants (no MagicConstant literals)
    assert len(result) == 3
    assert result == grid_g1
    assert result[0] == METER_RATIO
    assert result[1] == FEET_PER_METER
    assert result[2] == YARD_PER_METER
