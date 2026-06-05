"""U-CLI-01 — FR-01, FR-04: CLI table output."""

import io

from boundary.cli import run_cli

# TC ID: U-CLI-01


def test_u_cli_01_table_output(capsys):
    stdout = io.StringIO()
    exit_code = run_cli(["meter:2.5"], stdout=stdout, stderr=io.StringIO())
    output = stdout.getvalue()
    assert exit_code == 0
    assert "2.5 meter = 8.2 feet" in output
    assert "2.5 meter = 2.7 yard" in output
