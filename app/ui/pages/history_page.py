from __future__ import annotations

import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox, QCompleter, QDateEdit, QDialog, QFileDialog, QHBoxLayout,
    QLabel, QMessageBox, QPushButton, QSpinBox, QTableView, QVBoxLayout, QWidget,
)

from app.core.config_store import ConfigStore
from app.services.activity_service import ActivityFilters, ActivityService
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
        config_store: ConfigStore, open_settings: Callable[[], None], parent=None,
    ) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.report_service = report_service
        self.email_service = email_service
        self.config_store = config_store
        self.open_settings = open_settings

        self.model = ActivityTableModel()
        self._page = 1
        self._total = 0

        title = QLabel("Historico de Atividades")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.cb_vehicle = QComboBox()
        self.cb_vehicle.setEditable(True)
        self.cb_vehicle.setInsertPolicy(QComboBox.NoInsert)

        self.dt_start = QDateEdit()
        self.dt_start.setCalendarPopup(True)
        self.dt_start.setDate(QDate.currentDate().addDays(-7))

        self.dt_end = QDateEdit()
        self.dt_end.setCalendarPopup(True)
        self.dt_end.setDate(QDate.currentDate())

        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(["Todas", "Carga Pesada", "Carga Leve", "Outros"])

        self.cb_order = QComboBox()
        self.cb_order.addItems(["Data (desc)", "Data (asc)", "Veiculo (A->Z)"])

        btn_apply = QPushButton("Aplicar")
        btn_apply.setIcon(icon("refresh"))
        btn_apply.clicked.connect(self.refresh)

        filters = QHBoxLayout()
        filters.addWidget(QLabel("Veiculo"))
        filters.addWidget(self.cb_vehicle, 1)
        filters.addWidget(QLabel("De"))
        filters.addWidget(self.dt_start)
        filters.addWidget(QLabel("Ate"))
        filters.addWidget(self.dt_end)
        filters.addWidget(QLabel("Categoria"))
        filters.addWidget(self.cb_categoria)
        filters.addWidget(QLabel("Ordenar"))
        filters.addWidget(self.cb_order)
        filters.addWidget(btn_apply)

        btn_pdf = QPushButton("Gerar PDF")
        btn_pdf.setIcon(icon("pdf"))
        btn_pdf.clicked.connect(self.generate_pdf)

        btn_email = QPushButton("Gerar e Enviar por E-mail")
        btn_email.setIcon(icon("email"))
        btn_email.clicked.connect(self.generate_and_send_email)

        btn_cfg = QPushButton("Configurar E-mail")
        btn_cfg.setIcon(icon("settings"))
        btn_cfg.clicked.connect(self.open_settings)

        actions = QHBoxLayout()
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
        btn_edit.clicked.connect(self.edit_selected)

        btn_del = QPushButton("Excluir")
        btn_del.setIcon(icon("delete"))
        btn_del.clicked.connect(self.delete_selected)

        row_actions = QHBoxLayout()
        row_actions.addWidget(btn_edit)
        row_actions.addWidget(btn_del)
        row_actions.addStretch(1)

        self.page_size = QSpinBox()
        self.page_size.setRange(10, 200)
        self.page_size.setValue(30)
        self.page_size.valueChanged.connect(lambda _=None: self._reset_and_refresh())

        btn_prev = QPushButton("<")
        btn_prev.clicked.connect(self.prev_page)
        btn_next = QPushButton(">")
        btn_next.clicked.connect(self.next_page)
        self.lbl_page = QLabel("")

        paging = QHBoxLayout()
        paging.addWidget(QLabel("Por pagina"))
        paging.addWidget(self.page_size)
        paging.addStretch(1)
        paging.addWidget(btn_prev)
        paging.addWidget(self.lbl_page)
        paging.addWidget(btn_next)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(filters)
        layout.addLayout(actions)
        layout.addLayout(row_actions)
        layout.addWidget(self.table)
        layout.addLayout(paging)
        self.setLayout(layout)

        self.refresh_vehicles()
        self.refresh()

    def refresh_vehicles(self) -> None:
        try:
            vehicles = self.vehicle_service.list("")
            self.cb_vehicle.clear()
            self.cb_vehicle.addItem("Todos", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
            self.cb_vehicle.setCompleter(
                QCompleter([self.cb_vehicle.itemText(i) for i in range(self.cb_vehicle.count())])
            )
        except Exception:
            logger.exception("Falha ao carregar veiculos no historico")

    def _filters(self) -> ActivityFilters:
        start = datetime.combine(self.dt_start.date().toPython(), datetime.min.time())
        end = datetime.combine(self.dt_end.date().toPython(), datetime.max.time())
        return ActivityFilters(
            vehicle_id=self.cb_vehicle.currentData(),
            start_dt=start, end_dt=end,
            categoria=self.cb_categoria.currentText(),
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
            self.activity_service.update(a["id"], **dlg.values())
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
            self.activity_service.delete(a["id"])
            self.refresh()
        except Exception:
            logger.exception("Falha ao excluir atividade")
            QMessageBox.critical(self, "Erro", "Falha ao excluir. Veja o log.")

    def _report_payload(self):
        filters = self._filters()
        rows = self.activity_service.list_all(filters)
        kpis = self.activity_service.kpis(filters)
        period_label = f"{filters.start_dt.strftime('%d/%m/%Y')} a {filters.end_dt.strftime('%d/%m/%Y')}"
        summary = ReportSummary(
            period_label=period_label,
            total_activities=kpis["total_atividades"],
            km_total=kpis.get("quantidade_total", 0),
            vehicles_involved=len({v["id"] for _, v in rows}) if rows else 0,
        )
        return filters, rows, summary

    def generate_pdf(self) -> None:
        try:
            _filters, rows, summary = self._report_payload()
            if summary.total_activities == 0:
                QMessageBox.information(self, "Sem dados", "Nao ha atividades para o filtro atual.")
                return
            path, _ = QFileDialog.getSaveFileName(
                self, "Salvar relatorio",
                f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                "PDF (*.pdf)",
            )
            if not path:
                return
            self.report_service.generate_pdf(
                output_path=Path(path), config=self.config_store.get(),
                summary=summary, rows=rows,
            )
            QMessageBox.information(self, "OK", "PDF gerado com sucesso.")
        except Exception:
            logger.exception("Falha ao gerar PDF")
            QMessageBox.critical(self, "Erro", "Falha ao gerar PDF. Veja o log.")

    def generate_and_send_email(self) -> None:
        cfg = self.config_store.get()
        if not cfg.smtp_host or not cfg.sender_email or not cfg.manager_email:
            QMessageBox.warning(self, "Configuracao", "Configure o e-mail antes de enviar.")
            self.open_settings()
            return
        try:
            _filters, rows, summary = self._report_payload()
            if summary.total_activities == 0:
                QMessageBox.information(self, "Sem dados", "Nao ha atividades para o filtro atual.")
                return

            tmp_dir = Path(tempfile.gettempdir())
            pdf_path = tmp_dir / f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            self.report_service.generate_pdf(
                output_path=pdf_path, config=cfg, summary=summary, rows=rows,
            )

            company = cfg.company_name or "MADEMAXI - Materiais de Construcao e Ferragem"
            period_label = summary.period_label
            subject = f"[{company}] Relatorio de Atividades de Veiculos - {period_label}"
            avg = round(summary.km_total / summary.vehicles_involved, 1) if summary.vehicles_involved > 0 else 0

            body = (
                f"Prezado Gestor,\n\n"
                f"Segue em anexo o relatorio de atividades de veiculos da {company}.\n\n"
                f"Periodo: {period_label}\n"
                f"Total de atividades: {summary.total_activities}\n"
                f"Quantidade total: {summary.km_total}\n"
                f"Veiculos envolvidos: {summary.vehicles_involved}\n"
                f"Media por veiculo: {avg}\n\n"
                f"Atenciosamente,\n"
                f"Equipe {company}\n"
            )

            html_body = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:20px;background:#f3f4f6;font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;">
<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
  <tr><td style="background:#1a1a1a;padding:24px;text-align:center;border-bottom:4px solid #E53935;">
    <h1 style="color:#ffffff;margin:0;font-size:20px;letter-spacing:1px;">{company}</h1>
    <p style="color:#9ca3af;margin:6px 0 0;font-size:12px;">RELATORIO DE ATIVIDADES DE VEICULOS</p>
  </td></tr>
  <tr><td style="padding:28px;">
    <p style="font-size:14px;color:#374151;margin:0 0 20px;">Prezado Gestor,</p>
    <p style="font-size:14px;color:#374151;margin:0 0 24px;">Segue em anexo o relatorio de atividades de veiculos referente ao periodo <strong>{period_label}</strong>.</p>

    <p style="font-size:14px;font-weight:bold;color:#E53935;margin:0 0 12px;border-bottom:1px solid #e5e7eb;padding-bottom:6px;">RESUMO DO PERIODO</p>
    <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td width="25%" style="padding:4px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafafa;border:1px solid #e5e7eb;border-radius:6px;"><tr><td style="padding:14px 8px;text-align:center;">
          <p style="font-size:22px;font-weight:bold;color:#1a1a1a;margin:0;">{summary.total_activities}</p>
          <p style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin:4px 0 0;">Atividades</p>
        </td></tr></table>
      </td>
      <td width="25%" style="padding:4px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafafa;border:1px solid #e5e7eb;border-radius:6px;"><tr><td style="padding:14px 8px;text-align:center;">
          <p style="font-size:22px;font-weight:bold;color:#1a1a1a;margin:0;">{summary.km_total}</p>
          <p style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin:4px 0 0;">Quantidade Total</p>
        </td></tr></table>
      </td>
      <td width="25%" style="padding:4px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafafa;border:1px solid #e5e7eb;border-radius:6px;"><tr><td style="padding:14px 8px;text-align:center;">
          <p style="font-size:22px;font-weight:bold;color:#1a1a1a;margin:0;">{summary.vehicles_involved}</p>
          <p style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin:4px 0 0;">Veiculos</p>
        </td></tr></table>
      </td>
      <td width="25%" style="padding:4px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafafa;border:1px solid #e5e7eb;border-radius:6px;"><tr><td style="padding:14px 8px;text-align:center;">
          <p style="font-size:22px;font-weight:bold;color:#1a1a1a;margin:0;">{avg}</p>
          <p style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin:4px 0 0;">Media/Veiculo</p>
        </td></tr></table>
      </td>
    </tr></table>

    <p style="font-size:14px;font-weight:bold;color:#E53935;margin:24px 0 12px;border-bottom:1px solid #e5e7eb;padding-bottom:6px;">DETALHES</p>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size:13px;border-collapse:collapse;">
      <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;color:#6b7280;width:40%;">Periodo analisado</td><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-weight:bold;color:#1a1a1a;">{period_label}</td></tr>
      <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;color:#6b7280;">Total de atividades registradas</td><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-weight:bold;color:#1a1a1a;">{summary.total_activities}</td></tr>
      <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;color:#6b7280;">Quantidade total acumulada</td><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-weight:bold;color:#1a1a1a;">{summary.km_total}</td></tr>
      <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;color:#6b7280;">Veiculos que realizaram atividades</td><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-weight:bold;color:#1a1a1a;">{summary.vehicles_involved}</td></tr>
      <tr><td style="padding:8px 0;color:#6b7280;">Media por veiculo</td><td style="padding:8px 0;font-weight:bold;color:#1a1a1a;">{avg}</td></tr>
    </table>

    <p style="font-size:12px;color:#6b7280;margin-top:20px;">O relatorio completo em PDF esta anexo. Para mais informacoes, acesse o sistema MADEMAXI.</p>
  </td></tr>
  <tr><td style="background:#f9fafb;padding:18px 28px;text-align:center;font-size:11px;color:#9ca3af;border-top:1px solid #e5e7eb;">
    <strong style="color:#E53935;">{company}</strong> &mdash; Todos os direitos reservados<br/>Este e-mail foi gerado automaticamente pelo sistema de gestao de frota.
  </td></tr>
</table>
</td></tr></table>
</body></html>"""

            result = self.email_service.send_report(
                config=cfg, subject=subject, body=body, html_body=html_body, attachment_path=pdf_path,
            )
            if result.ok:
                QMessageBox.information(self, "OK", "E-mail enviado com sucesso.")
            else:
                QMessageBox.warning(self, "Falha", result.message)
        except Exception:
            logger.exception("Falha ao gerar/enviar e-mail")
            QMessageBox.critical(self, "Erro", "Falha ao enviar e-mail. Veja o log.")
