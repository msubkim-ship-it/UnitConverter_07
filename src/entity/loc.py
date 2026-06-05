"""Location SSOT — G1 row-major ratio grid."""

from entity.constants import RATIOS_ROW_MAJOR


def find_blank_coords() -> tuple[float, float, float]:
    """Return G1 row-major ratio grid (meter, feet, yard) from constants SSOT."""
    return RATIOS_ROW_MAJOR
