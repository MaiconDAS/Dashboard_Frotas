from __future__ import annotations

import logging
import tempfile
from datetime import datetime, time, timedelta
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config_store import ConfigStore
from app.core.utils import previous_week_monday_to_sunday
from app.services.activity_service import ActivityFilters, ActivityService
from app.services.email_service import EmailService
from app.services.report_service import ReportService, ReportSummary

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(
        self,
        *,
        config_store: ConfigStore,
        activity_service: ActivityService,
        report_service: ReportService,
        email_service: EmailService,
    ) -> None:
        self.config_store = config_store
        self.activity_service = activity_service
        self.report_service = report_service
        self.email_service = email_service
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        self.scheduler.start()
        self._refresh_job()
        logger.info("Scheduler iniciado")

    def shutdown(self) -> None:
        try:
            self.scheduler.shutdown(wait=False)
        except Exception:
            pass

    def refresh(self) -> None:
        self._refresh_job()

    def _refresh_job(self) -> None:
        cfg = self.config_store.get()
        self.scheduler.remove_all_jobs()
        if cfg.weekly_enabled:
            trigger = CronTrigger(day_of_week="mon", hour=8, minute=0)
            self.scheduler.add_job(
                self.run_weekly_report,
                trigger=trigger,
                id="weekly_report",
                replace_existing=True,
                max_instances=1,
                coalesce=True,
            )
            logger.info("Job semanal habilitado")
        else:
            logger.info("Job semanal desabilitado")

    def startup_catch_up(self) -> None:
        cfg = self.config_store.get()
        if not cfg.weekly_enabled:
            return

        now = datetime.now()
        this_monday = (now.date() - timedelta(days=now.date().weekday()))
        monday_8 = datetime.combine(this_monday, time(hour=8, minute=0))

        if now < monday_8:
            return

        start, end = previous_week_monday_to_sunday(now)
        prev_sunday_iso = end.strftime("%Y-%m-%d")
        if cfg.last_weekly_sent_end_iso == prev_sunday_iso:
            return

        logger.info("Catch-up: disparando envio semanal pendente (%s)", prev_sunday_iso)
        self.run_weekly_report()

    def run_weekly_report(self) -> None:
        cfg = self.config_store.get()
        if not cfg.weekly_enabled:
            return

        start, end = previous_week_monday_to_sunday()
        filters = ActivityFilters(start_dt=start, end_dt=end)
        rows = self.activity_service.list_all(filters)

        kpis = self.activity_service.kpis(filters)
        period_label = f"{start.strftime('%d/%m/%Y')} a {end.strftime('%d/%m/%Y')}"
        summary = ReportSummary(
            period_label=period_label,
            total_activities=kpis["total_atividades"],
            km_total=kpis["quantidade_total"],
            vehicles_involved=len({v["id"] for _, v in rows}) if rows else 0,
        )

        if summary.total_activities == 0:
            logger.info("Relatorio semanal: nenhuma atividade no periodo (%s).", period_label)
            self.config_store.set_last_weekly_sent_end(end)
            return

        tmp_dir = Path(tempfile.gettempdir())
        file_name = f"relatorio_semanal_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.pdf"
        pdf_path = tmp_dir / file_name

        self.report_service.generate_pdf(
            output_path=pdf_path,
            config=cfg,
            summary=summary,
            rows=rows,
        )

        company = cfg.company_name or "MADEMAXI - Materiais de Construcao e Ferragem"
        subject = f"[{company}] Relatorio Semanal de Atividades - {period_label}"
        avg = round(summary.km_total / summary.vehicles_involved, 1) if summary.vehicles_involved > 0 else 0

        body = (
            f"Prezado Gestor,\n\n"
            f"Segue em anexo o relatorio semanal de atividades de veiculos da {company}.\n\n"
            f"Periodo: {period_label}\n"
            f"Total de atividades: {summary.total_activities}\n"
            f"Quantidade total: {summary.km_total}\n"
            f"Veiculos envolvidos: {summary.vehicles_involved}\n\n"
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
    <p style="color:#9ca3af;margin:6px 0 0;font-size:12px;">RELATORIO SEMANAL DE ATIVIDADES DE VEICULOS</p>
  </td></tr>
  <tr><td style="padding:28px;">
    <p style="font-size:14px;color:#374151;margin:0 0 20px;">Prezado Gestor,</p>
    <p style="font-size:14px;color:#374151;margin:0 0 24px;">Segue em anexo o relatorio semanal de atividades referente ao periodo <strong>{period_label}</strong>.</p>

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
            self.config_store.set_last_weekly_sent_end(end)
            logger.info("Relatorio semanal enviado com sucesso.")
        else:
            logger.error("Relatorio semanal falhou: %s", result.message)
