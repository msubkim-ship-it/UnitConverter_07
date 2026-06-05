"""Output formatters — table, JSON, CSV (FR-09)."""

import csv
import io
import json

from control.conversion_service import convert_all, format_line


def format_table(value: float, unit: str) -> str:
    rows = convert_all(value, unit)
    lines = [format_line(value, unit, to_unit, converted) for to_unit, converted in rows]
    return "\n".join(lines)


def format_json(value: float, unit: str) -> str:
    rows = convert_all(value, unit)
    payload = {
        "input": {"unit": unit, "value": value},
        "conversions": [{"unit": to_unit, "value": converted} for to_unit, converted in rows],
    }
    return json.dumps(payload, ensure_ascii=False)


def format_csv(value: float, unit: str) -> str:
    rows = convert_all(value, unit)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["from_unit", "from_value", "to_unit", "to_value"])
    for to_unit, converted in rows:
        writer.writerow([unit, value, to_unit, converted])
    return buffer.getvalue().strip()
