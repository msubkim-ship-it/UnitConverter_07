"""Length conversion use-case — orchestrates entity SSOT ratios."""

from entity.constants import DEFAULT_UNITS, UNIT_RATIOS


class ConversionError(Exception):
    """Smoke-test level validation error (E001~E007 SSOT는 exceptions.py 도입 후 교체)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def parse_unit_value(raw: str) -> tuple[str, float]:
    """Parse `unit:value` input (FR-01)."""
    text = raw.strip()
    if not text:
        raise ConversionError("빈 입력입니다. `단위:값` 형식으로 입력하세요. (예: meter:2.5)")

    if ":" not in text:
        raise ConversionError("형식 오류: `단위:값` 형식이 필요합니다. (예: meter:2.5)")

    unit, value_str = text.split(":", 1)
    unit = unit.strip()
    value_str = value_str.strip()

    if not unit:
        raise ConversionError("단위명이 비어 있습니다.")

    try:
        value = float(value_str)
    except ValueError as exc:
        raise ConversionError(f"숫자 변환 실패: '{value_str}'") from exc

    if value < 0:
        raise ConversionError("음수는 허용되지 않습니다.")

    return unit, value


def to_meters(value: float, unit: str) -> float:
    """Convert any registered unit value to meters (기준 단위)."""
    ratio = UNIT_RATIOS.get(unit)
    if ratio is None:
        raise ConversionError(f"미등록 단위: '{unit}'")

    return value / ratio


def convert_all(value: float, from_unit: str, *, decimal_places: int = 1) -> list[tuple[str, float]]:
    """Convert to all other registered units (FR-02, FR-04)."""
    if from_unit not in UNIT_RATIOS:
        raise ConversionError(f"미등록 단위: '{from_unit}'")

    meter_value = to_meters(value, from_unit)
    results: list[tuple[str, float]] = []

    for unit in DEFAULT_UNITS:
        if unit == from_unit:
            continue
        converted = round(meter_value * UNIT_RATIOS[unit], decimal_places)
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
