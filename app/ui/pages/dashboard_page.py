from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

import pyqtgraph as pg
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QVBoxLayout, QWidget,
)

from app.services.activity_service import ActivityFilters, ActivityService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon

logger = logging.getLogger(__name__)


def _card(title: str) -> tuple[QFrame, QLabel]:
    box = QFrame()
    box.setFrameShape(QFrame.StyledPanel)
    box.setStyleSheet("QFrame{border-radius:10px; padding:10px;}")
    v = QVBoxLayout(box)
    lbl_title = QLabel(title)
    lbl_title.setStyleSheet("font-size: 12px; color: #9ca3af;")
    lbl_value = QLabel("—")
    lbl_value.setStyleSheet("font-size: 20px; font-weight: 700;")
    v.addWidget(lbl_title)
    v.addWidget(lbl_value)
    v.addStretch(1)
    return box, lbl_value


class DashboardPage(QWidget):
    def __init__(self, *, vehicle_service: VehicleService,
                 activity_service: ActivityService, parent=None) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(False)

        self.dt_start = QDateEdit()
        self.dt_start.setCalendarPopup(True)
        self.dt_start.setDate(QDate.currentDate().addDays(-30))

        self.dt_end = QDateEdit()
        self.dt_end.setCalendarPopup(True)
        self.dt_end.setDate(QDate.currentDate())

        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(["Todas", "Carga Pesada", "Carga Leve", "Outros"])

        btn_apply = QPushButton("Atualizar")
        btn_apply.setIcon(icon("refresh"))
        btn_apply.clicked.connect(self.refresh)

        filters_grid = QGridLayout()
        filters_grid.setSpacing(10)
        filters_grid.setColumnStretch(0, 3)
        filters_grid.setColumnStretch(1, 1)
        filters_grid.setColumnStretch(2, 1)
        filters_grid.setColumnStretch(3, 1)

        filters_grid.addWidget(QLabel("Veiculo"), 0, 0)
        filters_grid.addWidget(QLabel("Categoria"), 0, 1)
        filters_grid.addWidget(QLabel("De"), 0, 2)
        filters_grid.addWidget(QLabel("Ate"), 0, 3)

        filters_grid.addWidget(self.cb_vehicle, 1, 0)
        filters_grid.addWidget(self.cb_categoria, 1, 1)
        filters_grid.addWidget(self.dt_start, 1, 2)
        filters_grid.addWidget(self.dt_end, 1, 3)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(btn_apply)

        filters = QVBoxLayout()
        filters.addLayout(filters_grid)
        filters.addLayout(btn_row)

        cards = QGridLayout()
        c1, self.lbl_total = _card("Total de atividades")
        c2, self.lbl_qtd = _card("Quantidade total")
        c3, self.lbl_top = _card("Veiculo mais usado")
        c4, self.lbl_dias = _card("Dias com atividade")
        cards.addWidget(c1, 0, 0)
        cards.addWidget(c2, 0, 1)
        cards.addWidget(c3, 0, 2)
        cards.addWidget(c4, 0, 3)

        pg.setConfigOptions(antialias=True)
        self.plot_top = pg.PlotWidget(title="Veiculos mais usados")
        self.plot_top.setBackground(None)
        self.plot_top.showGrid(x=True, y=True, alpha=0.2)
        self.plot_top.setMenuEnabled(False)

        self.plot_dia = pg.PlotWidget(title="Atividades por dia")
        self.plot_dia.setBackground(None)
        self.plot_dia.showGrid(x=True, y=True, alpha=0.2)
        self.plot_dia.setMenuEnabled(False)

        charts = QGridLayout()
        charts.addWidget(self.plot_top, 0, 0)
        charts.addWidget(self.plot_dia, 0, 1)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(filters)
        layout.addLayout(cards)
        layout.addLayout(charts)
        self.setLayout(layout)

        self.refresh_vehicles()
        self.refresh()

    def on_vehicles_changed(self) -> None:
        self.refresh_vehicles()

    def refresh_vehicles(self) -> None:
        try:
            vehicles = self.vehicle_service.list("")
            self.cb_vehicle.clear()
            self.cb_vehicle.addItem("Todos", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
        except Exception:
            logger.exception("Falha ao carregar veiculos no dashboard")

    def _filters(self) -> ActivityFilters:
        start = datetime.combine(self.dt_start.date().toPython(), datetime.min.time())
        end = datetime.combine(self.dt_end.date().toPython(), datetime.max.time())
        return ActivityFilters(
            vehicle_id=self.cb_vehicle.currentData(),
            start_dt=start, end_dt=end,
            categoria=self.cb_categoria.currentText(),
        )

    def refresh(self) -> None:
        try:
            f = self._filters()
            k = self.activity_service.kpis(f)
            self.lbl_total.setText(str(k["total_atividades"]))
            self.lbl_qtd.setText(str(k.get("quantidade_total", 0)))
            self.lbl_top.setText(k["top_veiculos"][0][0] if k["top_veiculos"] else "—")
            self.lbl_dias.setText(str(len(k["por_dia"])))
            self._plot_top(k["top_veiculos"])
            self._plot_days(k["por_dia"])
        except Exception:
            logger.exception("Falha ao atualizar dashboard")

    def _plot_top(self, items):
        self.plot_top.clear()
        if not items:
            return
        labels = [p for p, _ in items]
        values = [q for _, q in items]
        x = list(range(len(values)))
        bg = pg.BarGraphItem(x=x, height=values, width=0.6, brush=pg.mkBrush("#60a5fa"))
        self.plot_top.addItem(bg)
        ax = self.plot_top.getAxis("bottom")
        ax.setTicks([list(zip(x, labels))])

    def _plot_days(self, items):
        self.plot_dia.clear()
        if not items:
            return
        labels = [d for d, _ in items]
        values = [q for _, q in items]
        x = list(range(len(values)))
        self.plot_dia.plot(x, values, pen=pg.mkPen("#f59e0b", width=2), symbol="o", symbolSize=6)
        ax = self.plot_dia.getAxis("bottom")
        ax.setTicks([list(zip(x, labels))])
