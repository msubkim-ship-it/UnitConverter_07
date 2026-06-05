"""Length conversion use-case — orchestrates entity SSOT ratios."""

from entity.constants import BASE_UNIT, DEFAULT_UNITS, UNIT_RATIOS
from entity.exceptions import ErrorCode


class ConversionError(Exception):
    """Domain validation error carrying ErrorCode SSOT."""

    def __init__(self, code: ErrorCode) -> None:
        self.code = code
        super().__init__(code.value)


def parse_unit_value(raw: str) -> tuple[str, float]:
    """Parse `unit:value` input (FR-01)."""
    text = raw.strip()
    if not text:
        raise ConversionError(ErrorCode.E001)

    if ":" not in text:
        raise ConversionError(ErrorCode.E001)

    unit, value_str = text.split(":", 1)
    unit = unit.strip()
    value_str = value_str.strip()

    if not unit:
        raise ConversionError(ErrorCode.E005)

    try:
        value = float(value_str)
    except ValueError as exc:
        raise ConversionError(ErrorCode.E002) from exc

    if value < 0:
        raise ConversionError(ErrorCode.E003)

    return unit, value


def to_meters(value: float, unit: str, ratios: dict[str, float] | None = None) -> float:
    """Convert any registered unit value to meters (기준 단위)."""
    table = ratios if ratios is not None else UNIT_RATIOS
    ratio = table.get(unit)
    if ratio is None:
        raise ConversionError(ErrorCode.E004)

    return value / ratio


def convert_unit(
    value: float,
    from_unit: str,
    to_unit: str,
    *,
    decimal_places: int = 1,
    ratios: dict[str, float] | None = None,
) -> float:
    """Convert value between two registered units (FR-05)."""
    table = ratios if ratios is not None else UNIT_RATIOS
    meter_value = to_meters(value, from_unit, table)
    if to_unit not in table:
        raise ConversionError(ErrorCode.E004)
    return round(meter_value * table[to_unit], decimal_places)


def convert_all(
    value: float,
    from_unit: str,
    *,
    decimal_places: int = 1,
    units: tuple[str, ...] | None = None,
    ratios: dict[str, float] | None = None,
) -> list[tuple[str, float]]:
    """Convert to all other registered units (FR-02, FR-04)."""
    table = ratios if ratios is not None else UNIT_RATIOS
    unit_list = units if units is not None else DEFAULT_UNITS
    if from_unit not in table:
        raise ConversionError(ErrorCode.E004)

    meter_value = to_meters(value, from_unit, table)
    results: list[tuple[str, float]] = []

    for unit in unit_list:
        if unit == from_unit:
            continue
        converted = round(meter_value * table[unit], decimal_places)
        results.append((unit, converted))

    return results


def format_line(value: float, from_unit: str, to_unit: str, converted: float) -> str:
    """Format one conversion line (FR-04 표 포맷)."""
    return f"{value} {from_unit} = {converted:.1f} {to_unit}"


def convert_from_text(raw: str) -> list[str]:
    """Parse input and return formatted conversion lines for boundary/GUI."""
    unit, value = parse_unit_value(raw)
    rows = convert_all(value, unit)
    return [format_line(value, unit, to_unit, converted) for to_unit, converted in rows]


def parse_registration(raw: str) -> tuple[str, float]:
    """Parse `1 cubit = 0.4572 meter` registration syntax (FR-08)."""
    text = raw.strip()
    if "=" not in text:
        raise ConversionError(ErrorCode.E006)

    left, right = text.split("=", 1)
    left = left.strip()
    right = right.strip()

    left_parts = left.split()
    right_parts = right.split()
    if len(left_parts) != 2 or len(right_parts) != 2:
        raise ConversionError(ErrorCode.E006)

    try:
        coefficient = float(left_parts[0])
    except ValueError as exc:
        raise ConversionError(ErrorCode.E006) from exc

    unit_name = left_parts[1]
    base_amount = float(right_parts[0])
    base_unit = right_parts[1]

    if base_unit != BASE_UNIT or coefficient <= 0 or base_amount <= 0:
        raise ConversionError(ErrorCode.E006)

    meter_ratio = coefficient / base_amount
    return unit_name, meter_ratio
