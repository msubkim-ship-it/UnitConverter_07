"""CLI boundary — stdin/stdout conversion and error surface (FR-01~04, FR-IN)."""

from __future__ import annotations

import sys
from typing import TextIO

from boundary.error_messages import message_for
from boundary.formatter import format_csv, format_json, format_table
from control.conversion_service import (
    ConversionError,
    convert_from_text,
    parse_registration,
    parse_unit_value,
)
from control.unit_registry import UnitRegistry


def run_cli(
    argv: list[str] | None = None,
    *,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    registry: UnitRegistry | None = None,
) -> int:
    """Run one-shot CLI. Returns process exit code."""
    argv = list(sys.argv[1:] if argv is None else argv)
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr

    output_format = "table"
    config_path = None
    positional: list[str] = []
    idx = 0
    while idx < len(argv):
        arg = argv[idx]
        if arg == "--format" and idx + 1 < len(argv):
            output_format = argv[idx + 1]
            idx += 2
            continue
        if arg == "--config" and idx + 1 < len(argv):
            config_path = argv[idx + 1]
            idx += 2
            continue
        positional.append(arg)
        idx += 1

    if positional:
        raw = positional[0]
    else:
        raw = stdin.read().strip()

    try:
        if raw.startswith("1 ") and "=" in raw:
            unit_name, ratio = parse_registration(raw)
            active_registry = registry or UnitRegistry()
            active_registry.register(unit_name, ratio)
            stdout.write(f"등록 완료: {unit_name}\n")
            return 0

        unit, value = parse_unit_value(raw)
        if output_format == "json":
            stdout.write(format_json(value, unit) + "\n")
        elif output_format == "csv":
            stdout.write(format_csv(value, unit) + "\n")
        else:
            if output_format == "table":
                stdout.write(format_table(value, unit) + "\n")
            else:
                for line in convert_from_text(raw):
                    stdout.write(line + "\n")
        return 0
    except ConversionError as exc:
        stderr.write(message_for(exc.code) + "\n")
        return 1
