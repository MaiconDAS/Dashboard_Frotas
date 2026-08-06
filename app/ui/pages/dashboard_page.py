from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

import pyqtgraph as pg
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from app.services.activity_service import ActivityFilters, ActivityService
from app.services.category_service import CategoryService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon

logger = logging.getLogger(__name__)


def _info_button(help_text: str, parent: QWidget | None = None) -> QPushButton:
    btn = QPushButton("i", parent)
    btn.setFixedSize(20, 20)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #333333;
            color: #9e9e9e;
            border: 1px solid #555555;
            border-radius: 10px;
            font-size: 11px;
            font-weight: bold;
            font-family: Georgia, serif;
            padding: 0;
        }
        QPushButton:hover {
            background-color: #E53935;
            color: white;
            border-color: #E53935;
        }
    """)
    btn.setToolTip("Clique para mais informacoes")
    btn.clicked.connect(lambda: QMessageBox.information(
        parent, "Informacao", help_text
    ))
    return btn


def _card(title: str, help_text: str) -> tuple[QFrame, QLabel]:
    box = QFrame()
    box.setStyleSheet("""
        QFrame {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 10px;
            padding: 16px;
        }
    """)
    v = QVBoxLayout(box)
    v.setSpacing(6)
    v.setContentsMargins(16, 16, 16, 16)

    header = QHBoxLayout()
    header.setSpacing(8)

    lbl_title = QLabel(title)
    lbl_title.setStyleSheet("font-size: 11px; color: #9e9e9e; text-transform: uppercase; letter-spacing: 0.5px;")
    header.addWidget(lbl_title, 1)

    btn_info = _info_button(help_text, box)
    header.addWidget(btn_info, 0, Qt.AlignmentFlag.AlignTop)

    v.addLayout(header)

    lbl_value = QLabel("—")
    lbl_value.setStyleSheet("font-size: 28px; font-weight: bold; color: #f5f5f5;")
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
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #E53935;")

        subtitle = QLabel("Acompanhe as atividades da frota em tempo real")
        subtitle.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 8px;")

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(False)

        self.dt_start = QDateEdit()
        self.dt_start.setCalendarPopup(True)
        self.dt_start.setDate(QDate.currentDate().addDays(-30))

        self.dt_end = QDateEdit()
        self.dt_end.setCalendarPopup(True)
        self.dt_end.setDate(QDate.currentDate())

        self.cb_categoria = QComboBox()
        self._load_categories()

        btn_apply = QPushButton("Atualizar")
        btn_apply.setIcon(icon("refresh"))
        btn_apply.clicked.connect(self.refresh)

        filters_grid = QGridLayout()
        filters_grid.setSpacing(12)
        filters_grid.setColumnStretch(0, 3)
        filters_grid.setColumnStretch(1, 1)
        filters_grid.setColumnStretch(2, 1)
        filters_grid.setColumnStretch(3, 1)

        lbl_v = QLabel("Veiculo")
        lbl_v.setStyleSheet("font-weight: bold; font-size: 12px; color: #9e9e9e;")
        lbl_c = QLabel("Categoria")
        lbl_c.setStyleSheet("font-weight: bold; font-size: 12px; color: #9e9e9e;")
        lbl_d = QLabel("De")
        lbl_d.setStyleSheet("font-weight: bold; font-size: 12px; color: #9e9e9e;")
        lbl_a = QLabel("Ate")
        lbl_a.setStyleSheet("font-weight: bold; font-size: 12px; color: #9e9e9e;")

        filters_grid.addWidget(lbl_v, 0, 0)
        filters_grid.addWidget(lbl_c, 0, 1)
        filters_grid.addWidget(lbl_d, 0, 2)
        filters_grid.addWidget(lbl_a, 0, 3)

        filters_grid.addWidget(self.cb_vehicle, 1, 0)
        filters_grid.addWidget(self.cb_categoria, 1, 1)
        filters_grid.addWidget(self.dt_start, 1, 2)
        filters_grid.addWidget(self.dt_end, 1, 3)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(btn_apply)

        filters = QVBoxLayout()
        filters.setSpacing(8)
        filters.addLayout(filters_grid)
        filters.addLayout(btn_row)

        cards = QGridLayout()
        cards.setSpacing(12)

        c1, self.lbl_total = _card(
            "Total de Atividades",
            "Quantidade total de registros de atividade no periodo filtrado.\n\n"
            "Cada vez que voce clica em 'Salvar' na aba Registrar Atividade, "
            "conta como 1 registro, independente da quantidade informada."
        )
        c2, self.lbl_qtd = _card(
            "Quantidade Total",
            "Soma de todas as quantidades informadas em cada registro de atividade "
            "no periodo filtrado.\n\n"
            "Exemplo: se voce registrou 3 atividades com quantidades 50, 40 e 62, "
            "o total sera 152."
        )
        c3, self.lbl_top = _card(
            "Veiculo Mais Usado",
            "Nome/Identificacao do veiculo que aparece em mais registros de atividade "
            "no periodo filtrado.\n\n"
            "Este dado e baseado na quantidade de entradas (registros), "
            "nao na soma das quantidades."
        )
        c4, self.lbl_dias = _card(
            "Dias com Atividade",
            "Quantidade de dias distintos em que houve pelo menos 1 registro de "
            "atividade no periodo filtrado."
        )

        cards.addWidget(c1, 0, 0)
        cards.addWidget(c2, 0, 1)
        cards.addWidget(c3, 0, 2)
        cards.addWidget(c4, 0, 3)

        pg.setConfigOptions(antialias=True)
        self.plot_top = pg.PlotWidget(title="Veiculos Mais Usados")
        self.plot_top.setBackground("#121212")
        self.plot_top.showGrid(x=True, y=True, alpha=0.15)
        self.plot_top.setMenuEnabled(False)
        self.plot_top.getAxis("bottom").setTextPen("#9e9e9e")
        self.plot_top.getAxis("left").setTextPen("#9e9e9e")
        self.plot_top.getAxis("bottom").setPen("#333333")
        self.plot_top.getAxis("left").setPen("#333333")

        self.plot_dia = pg.PlotWidget(title="Atividades por Dia")
        self.plot_dia.setBackground("#121212")
        self.plot_dia.showGrid(x=True, y=True, alpha=0.15)
        self.plot_dia.setMenuEnabled(False)
        self.plot_dia.getAxis("bottom").setTextPen("#9e9e9e")
        self.plot_dia.getAxis("left").setTextPen("#9e9e9e")
        self.plot_dia.getAxis("bottom").setPen("#333333")
        self.plot_dia.getAxis("left").setPen("#333333")

        charts = QGridLayout()
        charts.setSpacing(12)
        charts.addWidget(self.plot_top, 0, 0)
        charts.addWidget(self.plot_dia, 0, 1)

        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(filters)
        layout.addLayout(cards)
        layout.addLayout(charts)
        self.setLayout(layout)

        self.refresh_vehicles()
        self.refresh()

    def _load_categories(self) -> None:
        self.cb_categoria.clear()
        self.cb_categoria.addItem("Todas")
        try:
            for cat in CategoryService.list():
                self.cb_categoria.addItem(cat)
        except Exception:
            self.cb_categoria.addItems(["Carga Pesada", "Carga Leve", "Outros"])

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
        cat = self.cb_categoria.currentText()
        return ActivityFilters(
            vehicle_id=self.cb_vehicle.currentData(),
            start_dt=start, end_dt=end,
            categoria=cat,
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
        bg = pg.BarGraphItem(x=x, height=values, width=0.6, brush=pg.mkBrush("#E53935"))
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
        self.plot_dia.plot(x, values, pen=pg.mkPen("#E53935", width=2), symbol="o", symbolSize=6, symbolBrush="#E53935")
        ax = self.plot_dia.getAxis("bottom")
        ax.setTicks([list(zip(x, labels))])