"""Location SSOT — G1 row-major ratio grid."""

from entity.constants import RATIOS_ROW_MAJOR


def get_g1_ratios_row_major() -> tuple[float, float, float]:
    """Return G1 row-major ratio grid (meter, feet, yard) from constants SSOT."""
    return RATIOS_ROW_MAJOR
