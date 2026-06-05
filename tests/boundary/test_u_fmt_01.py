"""U-FMT-01 — FR-09: JSON output format."""

import io
import json

from boundary.cli import run_cli

# TC ID: U-FMT-01


def test_u_fmt_01_json_output():
    stdout = io.StringIO()
    exit_code = run_cli(["meter:2.5", "--format", "json"], stdout=stdout, stderr=io.StringIO())
    payload = json.loads(stdout.getvalue())
    assert exit_code == 0
    assert payload["input"] == {"unit": "meter", "value": 2.5}
    assert len(payload["conversions"]) == 2
