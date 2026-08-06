from __future__ import annotations

import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox, QCompleter, QDateEdit, QDialog, QFileDialog, QGridLayout, QHBoxLayout,
    QLabel, QMessageBox, QPushButton, QSpinBox, QTableView, QVBoxLayout, QWidget,
)

from app.core.config_store import ConfigStore
from app.services.activity_service import ActivityFilters, ActivityService
from app.services.category_service import CategoryService
from app.services.email_service import EmailService
from app.services.report_service import ReportService, ReportSummary
from app.services.vehicle_service import VehicleService
from app.ui.dialogs.activity_dialog import ActivityDialog
from app.ui.icons import icon
from app.ui.models.activity_table_model import ActivityTableModel

logger = logging.getLogger(__name__)


class HistoryPage(QWidget):
    def __init__(
        self, *, vehicle_service: VehicleService, activity_service: ActivityService,
        report_service: ReportService, email_service: EmailService,
        config_store: ConfigStore, open_settings: Callable[[], None],
        admin_data: dict | None = None, parent=None,
    ) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.report_service = report_service
        self.email_service = email_service
        self.config_store = config_store
        self.open_settings = open_settings
        self.admin_data = admin_data or {}
        self._generated_by = self.admin_data.get("username", "")

        self.model = ActivityTableModel()
        self._page = 1
        self._total = 0

        title = QLabel("Historico de Atividades")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #E53935;")

        subtitle = QLabel("Consulte, filtre e exporte o historico de atividades")
        subtitle.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 8px;")

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(False)
        self.cb_vehicle.setFixedHeight(42)

        self.dt_start = QDateEdit()
        self.dt_start.setCalendarPopup(True)
        self.dt_start.setDate(QDate.currentDate().addDays(-7))
        self.dt_start.setFixedHeight(42)

        self.dt_end = QDateEdit()
        self.dt_end.setCalendarPopup(True)
        self.dt_end.setDate(QDate.currentDate())
        self.dt_end.setFixedHeight(42)

        self.cb_categoria = QComboBox()
        self.cb_categoria.setFixedHeight(42)
        self._load_categories()

        self.cb_order = QComboBox()
        self.cb_order.addItems(["Data (desc)", "Data (asc)", "Veiculo (A->Z)"])
        self.cb_order.setFixedHeight(42)

        btn_apply = QPushButton("Aplicar")
        btn_apply.setIcon(icon("refresh"))
        btn_apply.setFixedHeight(44)
        btn_apply.clicked.connect(self.refresh)

        filters_grid = QGridLayout()
        filters_grid.setSpacing(12)
        filters_grid.setColumnStretch(0, 1)
        filters_grid.setColumnStretch(1, 2)
        filters_grid.setColumnStretch(2, 1)
        filters_grid.setColumnStretch(3, 1)
        filters_grid.setColumnStretch(4, 1)
        filters_grid.setColumnStretch(5, 1)
        filters_grid.setColumnStretch(6, 0)

        lbl_v = QLabel("Veiculo")
        lbl_v.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        lbl_d = QLabel("De")
        lbl_d.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        lbl_a = QLabel("Ate")
        lbl_a.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        lbl_c = QLabel("Categoria")
        lbl_c.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        lbl_o = QLabel("Ordenar")
        lbl_o.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")

        filters_grid.addWidget(lbl_v, 0, 0)
        filters_grid.addWidget(lbl_d, 0, 2)
        filters_grid.addWidget(lbl_a, 0, 4)
        filters_grid.addWidget(self.cb_vehicle, 1, 0, 1, 2)
        filters_grid.addWidget(self.dt_start, 1, 2)
        filters_grid.addWidget(self.dt_end, 1, 4)

        filters_grid.addWidget(lbl_c, 2, 0)
        filters_grid.addWidget(lbl_o, 2, 2)
        filters_grid.addWidget(self.cb_categoria, 3, 0, 1, 2)
        filters_grid.addWidget(self.cb_order, 3, 2, 1, 2)
        filters_grid.addWidget(btn_apply, 3, 4, 1, 2, Qt.AlignmentFlag.AlignRight)

        btn_pdf = QPushButton("Gerar PDF")
        btn_pdf.setIcon(icon("pdf"))
        btn_pdf.setFixedHeight(44)
        btn_pdf.clicked.connect(self.generate_pdf)

        btn_email = QPushButton("Gerar e Enviar por E-mail")
        btn_email.setIcon(icon("email"))
        btn_email.setFixedHeight(44)
        btn_email.clicked.connect(self.generate_and_send_email)

        btn_cfg = QPushButton("Configurar E-mail")
        btn_cfg.setIcon(icon("settings"))
        btn_cfg.setFixedHeight(44)
        btn_cfg.clicked.connect(self.open_settings)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        actions.addWidget(btn_pdf)
        actions.addWidget(btn_email)
        actions.addWidget(btn_cfg)
        actions.addStretch(1)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.doubleClicked.connect(lambda _=None: self.edit_selected())

        btn_edit = QPushButton("Editar")
        btn_edit.setIcon(icon("edit"))
        btn_edit.setFixedHeight(44)
        btn_edit.clicked.connect(self.edit_selected)

        btn_del = QPushButton("Excluir")
        btn_del.setIcon(icon("delete"))
        btn_del.setFixedHeight(44)
        btn_del.clicked.connect(self.delete_selected)

        row_actions = QHBoxLayout()
        row_actions.setSpacing(12)
        row_actions.addWidget(btn_edit)
        row_actions.addWidget(btn_del)
        row_actions.addStretch(1)

        lbl_ps = QLabel("Por pagina")
        lbl_ps.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        self.page_size = QSpinBox()
        self.page_size.setRange(10, 200)
        self.page_size.setValue(30)
        self.page_size.setFixedHeight(42)
        self.page_size.valueChanged.connect(lambda _=None: self._reset_and_refresh())

        btn_prev = QPushButton("<")
        btn_prev.setFixedHeight(44)
        btn_prev.clicked.connect(self.prev_page)

        btn_next = QPushButton(">")
        btn_next.setFixedHeight(44)
        btn_next.clicked.connect(self.next_page)

        self.lbl_page = QLabel("")
        self.lbl_page.setStyleSheet("font-size: 13px; color: #e5e7eb;")

        paging = QHBoxLayout()
        paging.setSpacing(12)
        paging.addWidget(lbl_ps)
        paging.addWidget(self.page_size)
        paging.addStretch(1)
        paging.addWidget(btn_prev)
        paging.addWidget(self.lbl_page)
        paging.addWidget(btn_next)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20, 16, 20, 16)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(20)
        layout.addLayout(filters_grid)

        layout.addSpacing(20)
        layout.addLayout(actions)

        layout.addSpacing(12)
        layout.addLayout(row_actions)

        layout.addSpacing(12)
        layout.addWidget(self.table, 1)

        layout.addSpacing(12)
        layout.addLayout(paging)

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

    def refresh_vehicles(self) -> None:
        try:
            vehicles = self.vehicle_service.list("")
            current_id = self.cb_vehicle.currentData()
            self.cb_vehicle.clear()
            self.cb_vehicle.addItem("Todos", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
            if current_id is not None:
                for i in range(self.cb_vehicle.count()):
                    if self.cb_vehicle.itemData(i) == current_id:
                        self.cb_vehicle.setCurrentIndex(i)
                        break
        except Exception:
            logger.exception("Falha ao carregar veiculos no historico")

    def _filters(self) -> ActivityFilters:
        start = datetime.combine(self.dt_start.date().toPython(), datetime.min.time())
        end = datetime.combine(self.dt_end.date().toPython(), datetime.max.time())
        cat = self.cb_categoria.currentText()
        return ActivityFilters(
            vehicle_id=self.cb_vehicle.currentData(),
            start_dt=start, end_dt=end,
            categoria=cat,
        )

    def _order(self):
        text = self.cb_order.currentText()
        if text == "Data (asc)":
            return ("data_hora", False)
        if text == "Veiculo (A->Z)":
            return ("veiculo", False)
        return ("data_hora", True)

    def _reset_and_refresh(self) -> None:
        self._page = 1
        self.refresh()

    def refresh(self) -> None:
        try:
            order_by, order_desc = self._order()
            rows, total = self.activity_service.list_paginated(
                self._filters(), page=self._page, page_size=int(self.page_size.value()),
                order_by=order_by, order_desc=order_desc,
            )
            self.model.set_rows(rows)
            self._total = total
            self._update_page_label()
        except Exception:
            logger.exception("Falha ao carregar historico")
            QMessageBox.critical(self, "Erro", "Falha ao carregar historico. Veja o log.")

    def _update_page_label(self) -> None:
        page_size = int(self.page_size.value())
        total_pages = max(1, (self._total + page_size - 1) // page_size)
        self.lbl_page.setText(f"Pagina {self._page} / {total_pages} (Total: {self._total})")

    def prev_page(self) -> None:
        if self._page > 1:
            self._page -= 1
            self.refresh()

    def next_page(self) -> None:
        page_size = int(self.page_size.value())
        total_pages = max(1, (self._total + page_size - 1) // page_size)
        if self._page < total_pages:
            self._page += 1
            self.refresh()

    def _selected(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return None
        return self.model.row_at(idx.row())

    def edit_selected(self) -> None:
        sel = self._selected()
        if not sel:
            QMessageBox.information(self, "Selecionar", "Selecione uma atividade.")
            return
        a, v = sel
        vehicles = self.vehicle_service.list("")
        dlg = ActivityDialog(self, vehicles=vehicles, activity=a)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.activity_service.update(a["id"], username=self.admin_data.get("username"), **dlg.values())
            self.refresh()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

    def delete_selected(self) -> None:
        sel = self._selected()
        if not sel:
            QMessageBox.information(self, "Selecionar", "Selecione uma atividade.")
            return
        a, v = sel
        dh = a.get("data_hora")
        data_str = ""
        if dh:
            data_str = dh.strftime("%d/%m/%Y") if hasattr(dh, "strftime") else str(dh)[:10]
        r = QMessageBox.question(self, "Confirmar", f"Excluir a atividade de {v.get('placa','')} em {data_str}?")
        if r != QMessageBox.Yes:
            return
        try:
            self.activity_service.delete(a["id"], username=self.admin_data.get("username"))
            self.refresh()
        except Exception:
            logger.exception("Falha ao excluir atividade")
            QMessageBox.critical(self, "Erro", "Falha ao excluir. Veja o log.")

    def _build_summary(self, rows) -> ReportSummary:
        start = datetime.combine(self.dt_start.date().toPython(), datetime.min.time())
        end = datetime.combine(self.dt_end.date().toPython(), datetime.max.time())
        period_label = f"{start.strftime('%d/%m/%Y')} a {end.strftime('%d/%m/%Y')}"
        total_qty = sum(a.get("quantidade", 0) for a, _ in rows)
        vehicles_involved = len({v["id"] for _, v in rows}) if rows else 0
        return ReportSummary(
            period_label=period_label,
            total_activities=self._total,
            km_total=total_qty,
            vehicles_involved=vehicles_involved,
        )

    def generate_pdf(self) -> None:
        try:
            path, _ = QFileDialog.getSaveFileName(
                self, "Salvar PDF", "relatorio_mademaxi.pdf", "PDF (*.pdf)"
            )
            if not path:
                return
            rows = self.activity_service.list_all(self._filters())
            summary = self._build_summary(rows)
            cfg = self.config_store.get()
            self.report_service.generate_pdf(
                output_path=Path(path),
                config=cfg,
                summary=summary,
                rows=rows,
                generated_by=self._generated_by,
            )
            QMessageBox.information(self, "Sucesso", f"PDF salvo em:\n{path}")
        except Exception:
            logger.exception("Falha ao gerar PDF")
            QMessageBox.critical(self, "Erro", "Falha ao gerar PDF. Veja o log.")

    def generate_and_send_email(self) -> None:
        try:
            cfg = self.config_store.get()
            if not cfg.manager_email or not cfg.smtp_host:
                QMessageBox.warning(self, "Configuracao", "Configure o e-mail em Configuracoes primeiro.")
                self.open_settings()
                return
            rows = self.activity_service.list_all(self._filters())
            summary = self._build_summary(rows)

            with tempfile.TemporaryDirectory() as tmp:
                pdf_path = Path(tmp) / "relatorio_mademaxi.pdf"
                self.report_service.generate_pdf(
                    output_path=pdf_path,
                    config=cfg,
                    summary=summary,
                    rows=rows,
                    generated_by=self._generated_by,
                )

                period_label = summary.period_label
                company = cfg.company_name or "MADEMAXI"
                subject = f"[{company}] Relatorio de Atividades - {period_label}"
                body = (
                    f"Prezado Gestor,\n\n"
                    f"Segue em anexo o relatorio de atividades da frota.\n\n"
                    f"Periodo: {period_label}\n"
                    f"Total de atividades: {summary.total_activities}\n"
                    f"Quantidade total: {summary.km_total}\n"
                    f"Veiculos envolvidos: {summary.vehicles_involved}\n\n"
                    f"Atenciosamente,\n"
                    f"Equipe {company}\n"
                )

                result = self.email_service.send_report(
                    config=cfg,
                    subject=subject,
                    body=body,
                    attachment_path=pdf_path,
                    generated_by=self._generated_by,
                )
                if result.ok:
                    QMessageBox.information(self, "Sucesso", result.message)
                else:
                    QMessageBox.warning(self, "Falha", result.message)
        except Exception:
            logger.exception("Falha ao enviar e-mail")
            QMessageBox.critical(self, "Erro", "Falha ao enviar e-mail. Veja o log.")