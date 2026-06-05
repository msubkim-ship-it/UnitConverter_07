"""Shared pytest fixtures for UnitConverter TDD."""

import pytest


@pytest.fixture
def grid_g1():
    """G1 row-major ratio grid — GREEN: (1.0, FEET_PER_METER, YARD_PER_METER) via entity.constants."""
    from entity.constants import FEET_PER_METER, YARD_PER_METER

    return (1.0, FEET_PER_METER, YARD_PER_METER)
