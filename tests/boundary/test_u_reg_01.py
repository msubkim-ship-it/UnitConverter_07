"""U-REG-01 — FR-08: registration input via CLI."""

import io

from boundary.cli import run_cli
from control.unit_registry import UnitRegistry

# TC ID: U-REG-01


def test_u_reg_01_registration_cli():
    stdout = io.StringIO()
    registry = UnitRegistry()
    exit_code = run_cli(
        ["1 cubit = 0.4572 meter"],
        stdout=stdout,
        stderr=io.StringIO(),
        registry=registry,
    )
    assert exit_code == 0
    assert "등록 완료" in stdout.getvalue()
    assert "cubit" in registry.ratios
