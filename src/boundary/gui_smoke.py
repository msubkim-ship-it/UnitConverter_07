"""PyQt6/PySide6 GUI smoke-test harness — boundary layer (스모크·수동 확인용)."""

from __future__ import annotations

import sys

from boundary.error_messages import message_for
from control.conversion_service import ConversionError, convert_from_text
from entity.constants import BASE_UNIT, DEFAULT_UNITS, UNIT_RATIOS
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
            "  pip install PySide6\n"
            "또는\n"
            "  pip install PyQt6"
        ) from exc


class SmokeTestWindow(QMainWindow):
    """UnitConverter SSOT·변환 결과를 눈으로 확인하는 스모크 테스트 창."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"UnitConverter_07 — GUI Smoke Test ({_QT_API})")
        self.setMinimumSize(560, 520)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(self._build_ssot_group())
        layout.addWidget(self._build_input_group())
        layout.addWidget(self._build_result_group())

        self._status = QLabel("준비됨 — 변환 버튼을 눌러 동작을 확인하세요.")
        self._status.setStyleSheet("color: #555;")
        layout.addWidget(self._status)

    def _build_ssot_group(self) -> QGroupBox:
        group = QGroupBox("D-LOC-01 — entity.constants SSOT (G1 row-major)")
        form = QFormLayout(group)

        ratios = get_g1_ratios_row_major()
        labels = ("meter ratio", "feet per meter", "yard per meter")
        for label, ratio in zip(labels, ratios, strict=True):
            form.addRow(label, QLabel(f"{ratio}"))

        table = QTableWidget(len(DEFAULT_UNITS), 2)
        table.setHorizontalHeaderLabels(["단위", f"비율 (기준: {BASE_UNIT})"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setMaximumHeight(120)

        for row, unit in enumerate(DEFAULT_UNITS):
            table.setItem(row, 0, QTableWidgetItem(unit))
            table.setItem(row, 1, QTableWidgetItem(str(UNIT_RATIOS[unit])))

        table.resizeColumnsToContents()
        form.addRow("등록 단위", table)
        return group

    def _build_input_group(self) -> QGroupBox:
        group = QGroupBox("변환 입력 (FR-01: 단위:값)")
        outer = QVBoxLayout(group)

        self._raw_input = QLineEdit()
        self._raw_input.setPlaceholderText("meter:2.5")
        self._raw_input.returnPressed.connect(self._on_convert)
        outer.addWidget(QLabel("텍스트 입력:"))
        outer.addWidget(self._raw_input)

        row = QHBoxLayout()
        self._unit_combo = QComboBox()
        self._unit_combo.addItems(DEFAULT_UNITS)
        self._value_spin = QDoubleSpinBox()
        self._value_spin.setRange(0.0, 1_000_000.0)
        self._value_spin.setDecimals(4)
        self._value_spin.setValue(2.5)
        self._value_spin.setSingleStep(0.1)

        row.addWidget(QLabel("단위:"))
        row.addWidget(self._unit_combo)
        row.addWidget(QLabel("값:"))
        row.addWidget(self._value_spin)
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

    def _sync_combo_to_text(self) -> None:
        unit = self._unit_combo.currentText()
        value = self._value_spin.value()
        self._raw_input.setText(f"{unit}:{value}")

    def _on_clear(self) -> None:
        self._raw_input.clear()
        self._output.clear()
        self._status.setText("출력을 지웠습니다.")
        self._status.setStyleSheet("color: #555;")

    def _on_convert(self) -> None:
        raw = self._raw_input.text().strip()
        if not raw:
            self._sync_combo_to_text()
            raw = self._raw_input.text()

        try:
            lines = convert_from_text(raw)
        except ConversionError as exc:
            msg = message_for(exc.code)
            self._output.setPlainText(f"[오류] {msg}")
            self._status.setText("변환 실패 — 입력을 확인하세요.")
            self._status.setStyleSheet("color: #c0392b;")
            QMessageBox.warning(self, "입력 오류", msg)
            return

        self._output.setPlainText("\n".join(lines))
        self._status.setText(f"변환 성공 — {len(lines)}개 단위 출력")
        self._status.setStyleSheet("color: #27ae60;")


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("UnitConverter_07 Smoke Test")
    window = SmokeTestWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
