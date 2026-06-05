"""U-IN-02 — FR-IN-02: missing colon surfaces E001 message."""

import io

from boundary.cli import run_cli

# TC ID: U-IN-02


def test_u_in_02_format_error_message():
    stderr = io.StringIO()
    exit_code = run_cli(["meter2.5"], stdout=io.StringIO(), stderr=stderr)
    assert exit_code != 0
    assert "형식 오류" in stderr.getvalue()
