"""U-IN-01 — FR-IN-01: negative input surfaces E003 message."""

import io

from boundary.cli import run_cli

# TC ID: U-IN-01


def test_u_in_01_negative_input_message():
    stderr = io.StringIO()
    exit_code = run_cli(["meter:-2.5"], stdout=io.StringIO(), stderr=stderr)
    assert exit_code != 0
    assert "음수" in stderr.getvalue()
