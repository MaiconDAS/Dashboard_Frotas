from __future__ import annotations

import logging
from datetime import datetime

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QHBoxLayout, QLabel, QMessageBox,
    QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget,
)

from app.services.activity_service import ActivityService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon

logger = logging.getLogger(__name__)


class ActivityRegisterPage(QWidget):
    activity_changed = Signal()

    def __init__(self, *, vehicle_service: VehicleService,
                 activity_service: ActivityService,
                 admin_data: dict | None = None,
                 parent=None) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.admin_data = admin_data or {}

        title = QLabel("Registrar Atividade")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #E53935;")

        subtitle = QLabel("Registre uma nova atividade da frota")
        subtitle.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 8px;")

        lbl_v = QLabel("Veiculo *")
        lbl_v.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(False)
        self.cb_vehicle.setFixedHeight(42)

        lbl_d = QLabel("Data *")
        lbl_d.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")

        self.dt = QDateEdit()
        self.dt.setCalendarPopup(True)
        self.dt.setDisplayFormat("dd/MM/yyyy")
        self.dt.setDate(QDate.currentDate())
        self.dt.setMaximumDate(QDate.currentDate())
        self.dt.setFixedHeight(42)

        lbl_q = QLabel("Quantidade de atividades *")
        lbl_q.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")

        self.sp_quantidade = QSpinBox()
        self.sp_quantidade.setRange(0, 999999)
        self.sp_quantidade.setValue(1)
        self.sp_quantidade.setFixedHeight(42)

        lbl_o = QLabel("Observacoes")
        lbl_o.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")

        self.ed_obs = QTextEdit()
        self.ed_obs.setFixedHeight(120)

        btn_save = QPushButton("Salvar")
        btn_save.setIcon(icon("save"))
        btn_save.setFixedHeight(44)
        btn_save.clicked.connect(self.save)

        btn_clear = QPushButton("Limpar")
        btn_clear.setFixedHeight(44)
        btn_clear.clicked.connect(self.clear_form)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        actions.addStretch(1)
        actions.addWidget(btn_clear)
        actions.addWidget(btn_save)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20, 16, 20, 16)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(24)

        layout.addWidget(lbl_v)
        layout.addWidget(self.cb_vehicle)

        layout.addSpacing(16)

        layout.addWidget(lbl_d)
        layout.addWidget(self.dt)

        layout.addSpacing(16)

        layout.addWidget(lbl_q)
        layout.addWidget(self.sp_quantidade)

        layout.addSpacing(16)

        layout.addWidget(lbl_o)
        layout.addWidget(self.ed_obs)

        layout.addSpacing(28)

        layout.addLayout(actions)
        layout.addStretch(1)

        self.setLayout(layout)

        self.refresh_vehicles()

    def refresh_vehicles(self) -> None:
        try:
            current_id = self.cb_vehicle.currentData()
            vehicles = self.vehicle_service.list("")
            self.cb_vehicle.clear()
            self.cb_vehicle.addItem("-- Selecione um veiculo --", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
            if current_id is not None:
                for i in range(self.cb_vehicle.count()):
                    if self.cb_vehicle.itemData(i) == current_id:
                        self.cb_vehicle.setCurrentIndex(i)
                        break
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
                username=self.admin_data.get("username"),
            )
            self.sp_quantidade.setValue(1)
            self.ed_obs.clear()
            self.activity_changed.emit()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))