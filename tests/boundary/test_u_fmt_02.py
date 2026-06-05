"""U-FMT-02 — FR-09: CSV output format."""

import io

from boundary.cli import run_cli

# TC ID: U-FMT-02


def test_u_fmt_02_csv_output():
    stdout = io.StringIO()
    exit_code = run_cli(["meter:2.5", "--format", "csv"], stdout=stdout, stderr=io.StringIO())
    output = stdout.getvalue()
    assert exit_code == 0
    assert "from_unit,from_value,to_unit,to_value" in output
    assert "meter,2.5,feet,8.2" in output
