"""PyQt6/PySide6 GUI smoke-test harness — boundary layer (스모크·수동 확인용)."""

from __future__ import annotations

import csv
import io
import json
import sys

from boundary.error_messages import message_for
from control.conversion_service import (
    ConversionError,
    convert_all,
    format_line,
    parse_registration,
    parse_unit_value,
)
from control.unit_registry import UnitRegistry
from entity.constants import BASE_UNIT, UNIT_RATIOS
from entity.exceptions import ErrorCode
from entity.loc import get_g1_ratios_row_major

_QT_API = ""
try:
    from PyQt6.QtGui import QFont
    from PyQt6.QtWidgets import (
        QApplication,
        QComboBox,
        QDoubleSpinBox,
        QFormLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    _QT_API = "PyQt6"
except ImportError:
    try:
        from PySide6.QtGui import QFont
        from PySide6.QtWidgets import (
            QApplication,
            QComboBox,
            QDoubleSpinBox,
            QFormLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QMainWindow,
            QMessageBox,
            QPushButton,
            QTableWidget,
            QTableWidgetItem,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )

        _QT_API = "PySide6"
    except ImportError as exc:
        raise SystemExit(
            "Qt GUI 바인딩이 설치되어 있지 않습니다.\n"
            "  pip install -e \".[gui]\"\n"
            "또는\n"
            "  pip install PySide6"
        ) from exc


class SmokeTestWindow(QMainWindow):
    """UnitConverter SSOT·변환·등록·에러 표면화를 눈으로 확인하는 스모크 테스트 창."""

    def __init__(self) -> None:
        super().__init__()
        self._registry = UnitRegistry()
        self.setWindowTitle(f"UnitConverter_07 — GUI Smoke Test ({_QT_API})")
        self.setMinimumSize(620, 680)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(self._build_ssot_group())
        layout.addWidget(self._build_register_group())
        layout.addWidget(self._build_input_group())
        layout.addWidget(self._build_result_group())

        self._status = QLabel("준비됨 — 변환·등록 버튼으로 동작을 확인하세요.")
        self._status.setStyleSheet("color: #555;")
        layout.addWidget(self._status)

        self._refresh_units_table()
        self._refresh_unit_combo()

    def _build_ssot_group(self) -> QGroupBox:
        group = QGroupBox("entity SSOT — FR-LOC-01~03 (constants · ErrorCode)")
        outer = QVBoxLayout(group)

        form = QFormLayout()
        ratios = get_g1_ratios_row_major()
        labels = ("meter ratio", "feet per meter", "yard per meter")
        for label, ratio in zip(labels, ratios, strict=True):
            form.addRow(label, QLabel(f"{ratio}"))
        outer.addLayout(form)

        codes = ", ".join(code.value for code in ErrorCode)
        outer.addWidget(QLabel(f"ErrorCode: {codes}"))

        self._units_table = QTableWidget(0, 2)
        self._units_table.setHorizontalHeaderLabels(["단위", f"비율 (기준: {BASE_UNIT})"])
        self._units_table.verticalHeader().setVisible(False)
        self._units_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._units_table.setMaximumHeight(140)
        outer.addWidget(QLabel("등록 단위 (UnitRegistry — 기본 + 동적)"))
        outer.addWidget(self._units_table)
        return group

    def _build_register_group(self) -> QGroupBox:
        group = QGroupBox("동적 단위 등록 (FR-08 — U-REG-01)")
        layout = QVBoxLayout(group)

        self._reg_input = QLineEdit()
        self._reg_input.setPlaceholderText("1 cubit = 0.4572 meter")
        self._reg_input.returnPressed.connect(self._on_register)
        layout.addWidget(QLabel("등록 입력:"))
        layout.addWidget(self._reg_input)

        btn_row = QHBoxLayout()
        register_btn = QPushButton("등록")
        register_btn.clicked.connect(self._on_register)
        sample_btn = QPushButton("샘플 입력")
        sample_btn.clicked.connect(
            lambda: self._reg_input.setText("1 cubit = 0.4572 meter")
        )
        btn_row.addWidget(register_btn)
        btn_row.addWidget(sample_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return group

    def _build_input_group(self) -> QGroupBox:
        group = QGroupBox("변환 입력 (FR-01: 단위:값 · FR-09: 출력 포맷)")
        outer = QVBoxLayout(group)

        self._raw_input = QLineEdit()
        self._raw_input.setPlaceholderText("meter:2.5")
        self._raw_input.returnPressed.connect(self._on_convert)
        outer.addWidget(QLabel("텍스트 입력:"))
        outer.addWidget(self._raw_input)

        row = QHBoxLayout()
        self._unit_combo = QComboBox()
        self._value_spin = QDoubleSpinBox()
        self._value_spin.setRange(0.0, 1_000_000.0)
        self._value_spin.setDecimals(4)
        self._value_spin.setValue(2.5)
        self._value_spin.setSingleStep(0.1)

        self._format_combo = QComboBox()
        self._format_combo.addItems(["table", "json", "csv"])

        row.addWidget(QLabel("단위:"))
        row.addWidget(self._unit_combo)
        row.addWidget(QLabel("값:"))
        row.addWidget(self._value_spin)
        row.addWidget(QLabel("포맷:"))
        row.addWidget(self._format_combo)
        row.addStretch()
        outer.addLayout(row)

        btn_row = QHBoxLayout()
        convert_btn = QPushButton("변환")
        convert_btn.clicked.connect(self._on_convert)
        sync_btn = QPushButton("콤보 → 텍스트")
        sync_btn.clicked.connect(self._sync_combo_to_text)
        clear_btn = QPushButton("지우기")
        clear_btn.clicked.connect(self._on_clear)

        btn_row.addWidget(convert_btn)
        btn_row.addWidget(sync_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        outer.addLayout(btn_row)
        return group

    def _build_result_group(self) -> QGroupBox:
        group = QGroupBox("변환 결과 (FR-02, FR-04 — 입력 단위 제외, 소수 1자리)")
        layout = QVBoxLayout(group)
        self._output = QTextEdit()
        self._output.setReadOnly(True)
        mono = QFont("Consolas")
        if not mono.family():
            mono = QFont("Courier New")
        self._output.setFont(mono)
        layout.addWidget(self._output)
        return group

    def _refresh_units_table(self) -> None:
        ratios = self._registry.ratios
        units = self._registry.units
        self._units_table.setRowCount(len(units))
        for row, unit in enumerate(units):
            self._units_table.setItem(row, 0, QTableWidgetItem(unit))
            ratio = ratios[unit]
            suffix = " (SSOT)" if unit in UNIT_RATIOS else ""
            self._units_table.setItem(row, 1, QTableWidgetItem(f"{ratio}{suffix}"))
        self._units_table.resizeColumnsToContents()

    def _refresh_unit_combo(self) -> None:
        current = self._unit_combo.currentText()
        self._unit_combo.clear()
        self._unit_combo.addItems(self._registry.units)
        idx = self._unit_combo.findText(current)
        if idx >= 0:
            self._unit_combo.setCurrentIndex(idx)

    def _sync_combo_to_text(self) -> None:
        unit = self._unit_combo.currentText()
        value = self._value_spin.value()
        self._raw_input.setText(f"{unit}:{value}")

    def _on_clear(self) -> None:
        self._raw_input.clear()
        self._output.clear()
        self._status.setText("출력을 지웠습니다.")
        self._status.setStyleSheet("color: #555;")

    def _format_output(self, raw: str) -> str:
        unit, value = parse_unit_value(raw)
        ratios = self._registry.ratios
        units = self._registry.units
        fmt = self._format_combo.currentText()
        rows = convert_all(value, unit, ratios=ratios, units=units)

        if fmt == "json":
            payload = {
                "input": {"unit": unit, "value": value},
                "conversions": [{"unit": to_unit, "value": converted} for to_unit, converted in rows],
            }
            return json.dumps(payload, ensure_ascii=False, indent=2)

        if fmt == "csv":
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["from_unit", "from_value", "to_unit", "to_value"])
            for to_unit, converted in rows:
                writer.writerow([unit, value, to_unit, converted])
            return buffer.getvalue().strip()

        lines = [format_line(value, unit, to_unit, converted) for to_unit, converted in rows]
        return "\n".join(lines)

    def _show_error(self, exc: ConversionError) -> None:
        msg = message_for(exc.code)
        self._output.setPlainText(f"[{exc.code.value}] {msg}")
        self._status.setText(f"실패 — {exc.code.value}")
        self._status.setStyleSheet("color: #c0392b;")
        QMessageBox.warning(self, exc.code.value, msg)

    def _on_register(self) -> None:
        raw = self._reg_input.text().strip()
        if not raw:
            self._show_error(ConversionError(ErrorCode.E006))
            return

        try:
            unit_name, ratio = parse_registration(raw)
            self._registry.register(unit_name, ratio)
        except ConversionError as exc:
            self._show_error(exc)
            return

        self._refresh_units_table()
        self._refresh_unit_combo()
        self._output.setPlainText(f"등록 완료: {unit_name} (meter ratio {ratio})")
        self._status.setText(f"등록 성공 — {unit_name} (FR-08)")
        self._status.setStyleSheet("color: #27ae60;")

    def _on_convert(self) -> None:
        raw = self._raw_input.text().strip()
        if not raw:
            self._sync_combo_to_text()
            raw = self._raw_input.text()

        try:
            text = self._format_output(raw)
        except ConversionError as exc:
            self._show_error(exc)
            return

        self._output.setPlainText(text)
        line_count = max(1, text.count("\n") + 1) if text else 0
        fmt = self._format_combo.currentText()
        self._status.setText(f"변환 성공 — {fmt} ({line_count}줄)")
        self._status.setStyleSheet("color: #27ae60;")


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("UnitConverter_07 Smoke Test")
    window = SmokeTestWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
