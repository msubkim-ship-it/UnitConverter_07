"""Shared pytest fixtures for UnitConverter TDD."""

import pytest


@pytest.fixture
def grid_g1():
    """G1 row-major ratio grid — SSOT via entity.constants.RATIOS_ROW_MAJOR."""
    from entity.constants import RATIOS_ROW_MAJOR

    return RATIOS_ROW_MAJOR
