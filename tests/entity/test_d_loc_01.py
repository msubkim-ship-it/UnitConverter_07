"""D-LOC-01 — FR-LOC-01: entity.constants ratio SSOT (row-major G1)."""

from entity.loc import find_blank_coords

from tests._approval import assert_matches_golden

# TC ID: D-LOC-01

GOLDEN_REL = "d_loc_01_g1_step_a.approved.txt"


def _format_g1_row_major(coords: tuple[float, float, float]) -> str:
    """1-index row-major lines: ``{index}:{value}`` (golden format SSOT)."""
    return "\n".join(f"{i}:{v}" for i, v in enumerate(coords, start=1)) + "\n"


def test_d_loc_01(grid_g1):
    # Given: grid_g1 — row-major G1 ratio tuple from entity.constants SSOT
    from entity.constants import FEET_PER_METER, METER_RATIO, YARD_PER_METER

    # When: find_blank_coords returns row-major ratio tuple from SSOT
    result = find_blank_coords()

    # Then: row-major G1 matches fixture and constants (no MagicConstant literals)
    assert len(result) == 3
    assert result == grid_g1
    assert result[0] == METER_RATIO
    assert result[1] == FEET_PER_METER
    assert result[2] == YARD_PER_METER


def test_d_loc_01_step_a_success():
    # When: find_blank_coords returns SSOT G1 row-major ratios
    result = find_blank_coords()

    # Then: golden master matched (UPDATE_GOLDEN=1 to refresh baseline)
    actual = _format_g1_row_major(result)
    assert_matches_golden(actual, GOLDEN_REL)
