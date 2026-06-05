"""D-CONV-06 — FR-02: exclude input unit from conversion list."""

from control.conversion_service import convert_all

# TC ID: D-CONV-06


def test_d_conv_06_excludes_input_unit():
    results = convert_all(2.5, "meter")
    units = [unit for unit, _ in results]
    assert "meter" not in units
    assert set(units) == {"feet", "yard"}
