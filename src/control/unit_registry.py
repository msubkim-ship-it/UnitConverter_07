"""Unit registry — dynamic unit registration (FR-08, FR-15)."""

from entity.constants import DEFAULT_UNITS, UNIT_RATIOS
from entity.exceptions import ErrorCode

from control.conversion_service import ConversionError


class UnitRegistry:
    """Mutable unit table built on entity SSOT defaults."""

    def __init__(self) -> None:
        self._ratios: dict[str, float] = dict(UNIT_RATIOS)
        self._units: tuple[str, ...] = DEFAULT_UNITS

    @property
    def ratios(self) -> dict[str, float]:
        return dict(self._ratios)

    @property
    def units(self) -> tuple[str, ...]:
        return self._units

    def register(self, name: str, meter_ratio: float) -> None:
        if name in self._ratios:
            raise ConversionError(ErrorCode.E007)
        self._ratios[name] = meter_ratio
        self._units = (*self._units, name)
