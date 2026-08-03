from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from app.core.config_store import ConfigStore
from app.core.database import init_db
from app.core.logging_config import setup_logging
from app.services.activity_service import ActivityService
from app.services.email_service import EmailService
from app.services.report_service import ReportService
from app.services.scheduler_service import SchedulerService
from app.services.vehicle_service import VehicleService
from app.ui.main_window import MainWindow
from app.ui.theme import apply_theme

logger = logging.getLogger(__name__)


def run() -> None:
    setup_logging()
    logger.info("Iniciando aplicacao...")

    init_db()

    config_store = ConfigStore()
    config_store.load()

    vehicle_service = VehicleService()
    activity_service = ActivityService()
    report_service = ReportService()
    email_service = EmailService()

    scheduler_service = SchedulerService(
        config_store=config_store,
        activity_service=activity_service,
        report_service=report_service,
        email_service=email_service,
    )

    app = QApplication(sys.argv)
    apply_theme(app, config_store.get().theme)

    window = MainWindow(
        vehicle_service=vehicle_service,
        activity_service=activity_service,
        report_service=report_service,
        email_service=email_service,
        scheduler_service=scheduler_service,
        config_store=config_store,
        apply_theme=lambda t: apply_theme(app, t),
    )
    window.show()

    scheduler_service.start()
    scheduler_service.startup_catch_up()

    exit_code = app.exec()
    scheduler_service.shutdown()
    sys.exit(exit_code)
