from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)


class ActivityDialog(QDialog):
    def __init__(self, parent=None, vehicles: list = None, activity: dict = None) -> None:
        super().__init__(parent)
        self.activity = activity
        self.setWindowTitle("Editar Atividade" if activity else "Nova Atividade")
        self.resize(400, 280)

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(False)
        if vehicles:
            self.cb_vehicle.addItem("-- Selecione --", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])

        self.dt = QDateEdit()
        self.dt.setCalendarPopup(True)
        self.dt.setDisplayFormat("dd/MM/yyyy")
        self.dt.setDate(QDate.currentDate())
        self.dt.setMaximumDate(QDate.currentDate())

        self.sp_quantidade = QSpinBox()
        self.sp_quantidade.setRange(0, 999999)
        self.sp_quantidade.setValue(1)

        self.ed_obs = QTextEdit()
        self.ed_obs.setMaximumHeight(80)

        form = QFormLayout()
        form.addRow("Veiculo*", self.cb_vehicle)
        form.addRow("Data*", self.dt)
        form.addRow("Quantidade*", self.sp_quantidade)
        form.addRow("Observacoes", self.ed_obs)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btns)
        self.setLayout(layout)

        if activity:
            vid = activity.get("veiculo_id")
            for i in range(self.cb_vehicle.count()):
                if self.cb_vehicle.itemData(i) == vid:
                    self.cb_vehicle.setCurrentIndex(i)
                    break
            dh = activity.get("data_hora")
            if dh:
                if isinstance(dh, str):
                    dh = datetime.fromisoformat(dh)
                self.dt.setDate(QDate(dh.year, dh.month, dh.day))
            self.sp_quantidade.setValue(activity.get("quantidade", 1))
            self.ed_obs.setPlainText(activity.get("observacoes") or "")

    def values(self) -> dict:
        data_py = self.dt.date().toPython()
        agora = datetime.now()
        data_hora = datetime(
            year=data_py.year,
            month=data_py.month,
            day=data_py.day,
            hour=agora.hour,
            minute=agora.minute,
            second=agora.second,
        )
        return {
            "veiculo_id": int(self.cb_vehicle.currentData()),
            "data_hora": data_hora,
            "quantidade": self.sp_quantidade.value(),
            "observacoes": self.ed_obs.toPlainText().strip() or None,
        }
