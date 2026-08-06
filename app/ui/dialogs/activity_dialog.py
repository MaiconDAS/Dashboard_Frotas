from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFormLayout, QHBoxLayout, QLabel,
    QMessageBox, QPushButton, QSpinBox, QTextEdit, QVBoxLayout,
)


class ActivityDialog(QDialog):
    def __init__(self, parent=None, vehicles: list | None = None, activity: dict | None = None) -> None:
        super().__init__(parent)
        self.activity = activity
        self.setWindowTitle("Editar Atividade" if activity else "Nova Atividade")
        self.setFixedSize(480, 420)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._setup_ui(vehicles)

    def _setup_ui(self, vehicles: list | None) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(32, 28, 32, 28)

        title = QLabel("Editar Atividade" if self.activity else "Nova Atividade")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E53935;")
        layout.addWidget(title)

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #E53935;")
        layout.addWidget(line)

        layout.addSpacing(12)

        form = QFormLayout()
        form.setSpacing(14)
        form.setContentsMargins(0, 0, 0, 0)

        lbl_v = QLabel("Veiculo *")
        lbl_v.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        self.cb_vehicle = QComboBox()
        self.cb_vehicle.addItem("-- Selecione --", None)
        if vehicles:
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
        self.cb_vehicle.setStyleSheet("""
            QComboBox {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
                min-height: 36px;
            }
            QComboBox:focus { border-color: #E53935; }
        """)
        form.addRow(lbl_v, self.cb_vehicle)

        lbl_d = QLabel("Data *")
        lbl_d.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        self.dt = QDateEdit()
        self.dt.setCalendarPopup(True)
        self.dt.setDisplayFormat("dd/MM/yyyy")
        self.dt.setDate(QDate.currentDate())
        self.dt.setStyleSheet("""
            QDateEdit {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
                min-height: 36px;
            }
            QDateEdit:focus { border-color: #E53935; }
        """)
        form.addRow(lbl_d, self.dt)

        lbl_q = QLabel("Quantidade *")
        lbl_q.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        self.sp_qtd = QSpinBox()
        self.sp_qtd.setRange(0, 999999)
        self.sp_qtd.setValue(1)
        self.sp_qtd.setStyleSheet("""
            QSpinBox {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
                min-height: 36px;
            }
            QSpinBox:focus { border-color: #E53935; }
        """)
        form.addRow(lbl_q, self.sp_qtd)

        lbl_o = QLabel("Observacoes")
        lbl_o.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        self.ed_obs = QTextEdit()
        self.ed_obs.setFixedHeight(80)
        self.ed_obs.setStyleSheet("""
            QTextEdit {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QTextEdit:focus { border-color: #E53935; }
        """)
        form.addRow(lbl_o, self.ed_obs)

        layout.addLayout(form)

        if self.activity:
            v_id = self.activity.get("veiculo_id")
            for i in range(self.cb_vehicle.count()):
                if self.cb_vehicle.itemData(i) == v_id:
                    self.cb_vehicle.setCurrentIndex(i)
                    break
            dh = self.activity.get("data_hora")
            if dh:
                if hasattr(dh, "year"):
                    self.dt.setDate(QDate(dh.year, dh.month, dh.day))
                else:
                    self.dt.setDate(QDate.currentDate())
            self.sp_qtd.setValue(self.activity.get("quantidade", 1))
            self.ed_obs.setPlainText(self.activity.get("observacoes", "") or "")

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setFixedHeight(42)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #4b5563;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 24px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #374151; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Salvar")
        btn_save.setFixedHeight(42)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 24px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c62828; }
        """)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self._save)

        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def values(self) -> dict:
        data_py = self.dt.date().toPython()
        agora = datetime.now()
        return {
            "veiculo_id": int(self.cb_vehicle.currentData()) if self.cb_vehicle.currentData() else None,
            "data_hora": datetime(
                year=data_py.year, month=data_py.month, day=data_py.day,
                hour=agora.hour, minute=agora.minute, second=agora.second,
            ),
            "quantidade": self.sp_qtd.value(),
            "observacoes": self.ed_obs.toPlainText().strip() or None,
        }

    def _save(self) -> None:
        v = self.values()
        if v["veiculo_id"] is None:
            QMessageBox.warning(self, "Validacao", "Selecione um veiculo.")
            return
        self.accept()
