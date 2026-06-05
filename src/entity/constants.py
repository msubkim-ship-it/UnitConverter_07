"""Conversion ratio SSOT — MagicConstants defined here only."""

FEET_PER_METER = 3.28084
YARD_PER_METER = 1.09361
METER_RATIO = 1.0

RATIOS_ROW_MAJOR = (METER_RATIO, FEET_PER_METER, YARD_PER_METER)

BASE_UNIT = "meter"
DEFAULT_UNITS = ("meter", "feet", "yard")

UNIT_RATIOS = {
    "meter": METER_RATIO,
    "feet": FEET_PER_METER,
    "yard": YARD_PER_METER,
}
