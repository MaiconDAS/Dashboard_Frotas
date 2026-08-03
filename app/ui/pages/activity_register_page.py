from __future__ import annotations

import logging
from datetime import datetime

from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QFormLayout, QHBoxLayout, QLabel, QMessageBox,
    QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget,
)

from app.services.activity_service import ActivityService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon

logger = logging.getLogger(__name__)


class ActivityRegisterPage(QWidget):
    activity_changed = Signal()

    def __init__(self, *, vehicle_service: VehicleService,
                 activity_service: ActivityService, parent=None) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service

        title = QLabel("Registrar Atividade")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(False)

        self.dt = QDateEdit()
        self.dt.setCalendarPopup(True)
        self.dt.setDisplayFormat("dd/MM/yyyy")
        self.dt.setDate(QDate.currentDate())
        self.dt.setMaximumDate(QDate.currentDate())

        self.sp_quantidade = QSpinBox()
        self.sp_quantidade.setRange(0, 999999)
        self.sp_quantidade.setValue(1)

        self.ed_obs = QTextEdit()
        self.ed_obs.setFixedHeight(120)

        form = QFormLayout()
        form.addRow("Veiculo*", self.cb_vehicle)
        form.addRow("Data*", self.dt)
        form.addRow("Quantidade de atividades*", self.sp_quantidade)
        form.addRow("Observacoes", self.ed_obs)

        btn_save = QPushButton("Salvar")
        btn_save.setIcon(icon("save"))
        btn_save.clicked.connect(self.save)

        btn_clear = QPushButton("Limpar")
        btn_clear.clicked.connect(self.clear_form)

        actions = QHBoxLayout()
        actions.addStretch(1)
        actions.addWidget(btn_clear)
        actions.addWidget(btn_save)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(actions)
        layout.addStretch(1)
        self.setLayout(layout)

        self.refresh_vehicles()

    def refresh_vehicles(self) -> None:
        try:
            vehicles = self.vehicle_service.list("")
            self.cb_vehicle.clear()
            self.cb_vehicle.addItem("-- Selecione um veiculo --", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
        except Exception:
            logger.exception("Falha ao carregar veiculos para cadastro de atividade")

    def clear_form(self) -> None:
        self.cb_vehicle.setCurrentIndex(0)
        self.dt.setDate(QDate.currentDate())
        self.sp_quantidade.setValue(1)
        self.ed_obs.clear()

    def save(self) -> None:
        if self.cb_vehicle.currentData() is None:
            QMessageBox.warning(self, "Validacao", "Selecione um veiculo cadastrado.")
            return
        try:
            data_py = self.dt.date().toPython()
            agora = datetime.now()
            data_hora = datetime(
                year=data_py.year, month=data_py.month, day=data_py.day,
                hour=agora.hour, minute=agora.minute, second=agora.second,
            )
            self.activity_service.create(
                veiculo_id=int(self.cb_vehicle.currentData()),
                data_hora=data_hora,
                quantidade=self.sp_quantidade.value(),
                observacoes=self.ed_obs.toPlainText().strip() or None,
            )
            self.clear_form()
            self.activity_changed.emit()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
