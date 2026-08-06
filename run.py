from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import QEventLoop
from PySide6.QtWidgets import QApplication, QDialog

from app.core.config_store import ConfigStore
from app.core.database import init_db
from app.core.logging_config import setup_logging
from app.services.activity_service import ActivityService
from app.services.admin_service import AdminService
from app.services.email_service import EmailService
from app.services.report_service import ReportService
from app.services.scheduler_service import SchedulerService
from app.services.vehicle_service import VehicleService
from app.ui.dialogs.login_dialog import LoginDialog
from app.ui.dialogs.master_password_setup_dialog import MasterPasswordSetupDialog
from app.ui.main_window import MainWindow
from app.ui.theme import apply_theme

logger = logging.getLogger(__name__)


def run() -> None:
    setup_logging()
    logger.info("Iniciando aplicacao...")

    init_db()

    app = QApplication(sys.argv)
    app.setApplicationName("Dashboard Frotas MADEMAXI")
    app.setApplicationVersion("2.2.0")

    config_store = ConfigStore()
    apply_theme(app, config_store.get().theme)

    vehicle_service = VehicleService()
    activity_service = ActivityService()
    report_service = ReportService()
    email_service = EmailService()
    scheduler_service = SchedulerService(
        activity_service=activity_service,
        report_service=report_service,
        email_service=email_service,
        config_store=config_store,
    )

    # Verifica se senha mestra ja foi configurada
    if not AdminService.get_master_password_hash():
        logger.info("Primeira execucao: senha mestra nao configurada.")
        setup_dlg = MasterPasswordSetupDialog()
        if setup_dlg.exec() != QDialog.DialogCode.Accepted:
            logger.info("Configuracao de senha mestra cancelada. Encerrando.")
            sys.exit(0)

    while True:
        login = LoginDialog()
        if login.exec() != QDialog.DialogCode.Accepted:
            logger.info("Login cancelado. Encerrando.")
            break

        admin_data = login.get_admin_data()
        if not admin_data:
            logger.warning("Login aceito mas admin_data vazio.")
            continue

        logger.info("Login aceito: %s", admin_data.get("username"))

        window = MainWindow(
            vehicle_service=vehicle_service,
            activity_service=activity_service,
            report_service=report_service,
            email_service=email_service,
            scheduler_service=scheduler_service,
            config_store=config_store,
            apply_theme=lambda t: apply_theme(app, t),
            admin_data=admin_data,
        )
        window.show()

        loop = QEventLoop()
        window.logout_requested.connect(loop.quit)
        window.destroyed.connect(loop.quit)
        loop.exec()

        window.hide()
        window.deleteLater()

        if not QApplication.instance() or not QApplication.instance().topLevelWidgets():
            break

        logger.info("Logout solicitado. Retornando ao login.")

    scheduler_service.shutdown()
    sys.exit(0)


if __name__ == "__main__":
    run()

