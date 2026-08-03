from __future__ import annotations

from typing import Dict
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMessageBox, QStackedWidget, QVBoxLayout, QWidget,
)

from app.core.config_store import ConfigStore
from app.services.activity_service import ActivityService
from app.services.email_service import EmailService
from app.services.report_service import ReportService
from app.services.scheduler_service import SchedulerService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon
from app.ui.pages.activity_register_page import ActivityRegisterPage
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.history_page import HistoryPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.vehicles_page import VehiclesPage


class MainWindow(QMainWindow):
    def __init__(
        self,
        *,
        vehicle_service: VehicleService,
        activity_service: ActivityService,
        report_service: ReportService,
        email_service: EmailService,
        scheduler_service: SchedulerService,
        config_store: ConfigStore,
        apply_theme,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Dashboard de Atividades de Veiculos")
        self.resize(1280, 720)

        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.report_service = report_service
        self.email_service = email_service
        self.scheduler_service = scheduler_service
        self.config_store = config_store
        self.apply_theme = apply_theme

        # === SIDEBAR COM LOGO ===
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setSpacing(8)
        self.sidebar.setFrameShape(QFrame.Shape.NoFrame)

        logo_widget = QWidget()
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(10, 10, 10, 10)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        logo_path = Path(__file__).parent.parent.parent / "assets" / "logo_mademaxi.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                scaled = pixmap.scaledToWidth(180, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled)
                logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        company_label = QLabel("MADEMAXI")
        company_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #E53935;")
        company_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(company_label)

        sub_label = QLabel("Materiais de Construcao\ne Ferragem")
        sub_label.setStyleSheet("font-size: 9px; color: #6b7280;")
        sub_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(sub_label)

        logo_layout.addStretch(1)
        # =======================

        self.stack = QStackedWidget()

        def open_settings():
            self.navigate("settings")

        self.pages: Dict[str, QWidget] = {
            "dashboard": DashboardPage(
                vehicle_service=vehicle_service, activity_service=activity_service
            ),
            "vehicles": VehiclesPage(vehicle_service=vehicle_service),
            "register": ActivityRegisterPage(
                vehicle_service=vehicle_service, activity_service=activity_service
            ),
            "history": HistoryPage(
                vehicle_service=vehicle_service,
                activity_service=activity_service,
                report_service=report_service,
                email_service=email_service,
                config_store=config_store,
                open_settings=open_settings,
            ),
            "settings": SettingsPage(
                config_store=config_store,
                email_service=email_service,
                on_saved=self._on_settings_saved,
                apply_theme=self.apply_theme,
            ),
        }

        self.pages["vehicles"].vehicle_changed.connect(
            self.pages["register"].refresh_vehicles
        )
        self.pages["vehicles"].vehicle_changed.connect(
            self.pages["dashboard"].on_vehicles_changed
        )
        self.pages["vehicles"].vehicle_changed.connect(
            self.pages["history"].refresh_vehicles
        )

        self.pages["register"].activity_changed.connect(
            self.pages["history"].refresh
        )
        self.pages["register"].activity_changed.connect(
            self.pages["dashboard"].refresh
        )

        self._add_nav_item("dashboard", "Dashboard", "dashboard")
        self._add_nav_item("vehicles", "Veiculos", "vehicles")
        self._add_nav_item("register", "Registrar Atividade", "register")
        self._add_nav_item("history", "Historico", "history")
        self._add_nav_item("settings", "Configuracoes", "settings")

        for key in ["dashboard", "vehicles", "register", "history", "settings"]:
            self.stack.addWidget(self.pages[key])

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)

        sidebar_container = QWidget()
        sidebar_container.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar_layout.addWidget(logo_widget)
        sidebar_layout.addWidget(self.sidebar, 1)

        layout.addWidget(sidebar_container)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        self.statusBar().showMessage("Pronto")
        self.sidebar.setCurrentRow(0)

    def _add_nav_item(self, key: str, label: str, icon_name: str) -> None:
        item = QListWidgetItem(icon(icon_name), label)
        item.setData(Qt.UserRole, key)
        item.setSizeHint(item.sizeHint())
        self.sidebar.addItem(item)

    def navigate(self, key: str) -> None:
        for i in range(self.sidebar.count()):
            it = self.sidebar.item(i)
            if it.data(Qt.UserRole) == key:
                self.sidebar.setCurrentRow(i)
                return

    def _on_settings_saved(self) -> None:
        self.scheduler_service.refresh()
        self.scheduler_service.startup_catch_up()

