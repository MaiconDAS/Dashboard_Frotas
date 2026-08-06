from __future__ import annotations

from typing import Dict
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMessageBox, QPushButton, QStackedWidget, QVBoxLayout, QWidget,
)

from app.core.config_store import ConfigStore
from app.services.activity_service import ActivityService
from app.services.email_service import EmailService
from app.services.report_service import ReportService
from app.services.scheduler_service import SchedulerService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon
from app.ui.pages.activity_register_page import ActivityRegisterPage
from app.ui.pages.admin_management_page import AdminManagementPage
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.history_page import HistoryPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.vehicles_page import VehiclesPage


class MainWindow(QMainWindow):
    logout_requested = Signal()

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
        admin_data: dict | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.admin_data = admin_data or {}
        is_master = self.admin_data.get("is_master", False)
        admin_name = self.admin_data.get("nome_completo", "Usuario")

        self.setWindowTitle(f"Dashboard Frotas — MADEMAXI  |  Logado: {admin_name}")
        self.resize(1366, 768)

        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.report_service = report_service
        self.email_service = email_service
        self.scheduler_service = scheduler_service
        self.config_store = config_store
        self.apply_theme = apply_theme

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setSpacing(4)
        self.sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #0a0a0a;
                color: #9e9e9e;
                border: none;
                outline: none;
                padding: 8px 0;
            }
            QListWidget::item {
                padding: 14px 16px;
                border-radius: 8px;
                margin: 2px 10px;
                font-size: 13px;
                font-weight: 500;
            }
            QListWidget::item:selected {
                background-color: #E53935;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #1f1f1f;
                color: #f5f5f5;
            }
        """)

        logo_widget = QWidget()
        logo_widget.setStyleSheet("background-color: #0a0a0a;")
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(16, 20, 16, 16)
        logo_layout.setSpacing(6)

        logo_label = QLabel()
        logo_path = Path(__file__).parent.parent.parent / "assets" / "logo_mademaxi.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                scaled = pixmap.scaledToWidth(160, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled)
                logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        company_label = QLabel("MADEMAXI")
        company_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #E53935; letter-spacing: 1px;")
        company_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(company_label)

        sub_label = QLabel("Materiais de Construcao e Ferragem")
        sub_label.setStyleSheet("font-size: 10px; color: #757575;")
        sub_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(sub_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #333333;")
        logo_layout.addWidget(sep)

        logo_layout.addStretch(1)

        self.stack = QStackedWidget()

        def open_settings():
            self.navigate("settings")

        self.pages: Dict[str, QWidget] = {
            "dashboard": DashboardPage(
                vehicle_service=vehicle_service, activity_service=activity_service
            ),
            "vehicles": VehiclesPage(vehicle_service=vehicle_service),
            "register": ActivityRegisterPage(
                vehicle_service=vehicle_service,
                activity_service=activity_service,
                admin_data=self.admin_data,
            ),
            "history": HistoryPage(
                vehicle_service=vehicle_service,
                activity_service=activity_service,
                report_service=report_service,
                email_service=email_service,
                config_store=config_store,
                open_settings=open_settings,
                admin_data=self.admin_data,
            ),
            "settings": SettingsPage(
                config_store=config_store,
                email_service=email_service,
                on_saved=self._on_settings_saved,
                apply_theme=self.apply_theme,
            ),
        }

        if is_master:
            self.pages["admin"] = AdminManagementPage(current_admin_id=self.admin_data.get("id"))

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

        nav_order = ["dashboard", "vehicles", "register", "history"]
        if is_master:
            nav_order.append("admin")
        nav_order.append("settings")

        for key in nav_order:
            if key == "dashboard":
                self._add_nav_item(key, "Dashboard", "dashboard")
            elif key == "vehicles":
                self._add_nav_item(key, "Veiculos", "vehicles")
            elif key == "register":
                self._add_nav_item(key, "Registrar Atividade", "register")
            elif key == "history":
                self._add_nav_item(key, "Historico", "history")
            elif key == "admin":
                self._add_nav_item(key, "Gestao", "users")
            elif key == "settings":
                self._add_nav_item(key, "Configuracoes", "settings")

        for key in nav_order:
            self.stack.addWidget(self.pages[key])

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar_container = QWidget()
        sidebar_container.setFixedWidth(240)
        sidebar_container.setStyleSheet("background-color: #0a0a0a;")
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar_layout.addWidget(logo_widget)
        sidebar_layout.addWidget(self.sidebar, 1)

        btn_logout = QPushButton("  Sair")
        btn_logout.setIcon(icon("logout"))
        btn_logout.setFixedHeight(42)
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #b71c1c;
                color: white;
                border: none;
                border-radius: 8px;
                margin: 4px 10px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 500;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #E53935;
                color: white;
            }
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self._confirm_logout)
        sidebar_layout.addWidget(btn_logout)

        footer = QLabel("2026 MADEMAXI")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("font-size: 9px; color: #424242; padding: 8px; background-color: #0a0a0a;")
        sidebar_layout.addWidget(footer)

        layout.addWidget(sidebar_container)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        self.statusBar().showMessage("Pronto")
        self.statusBar().setStyleSheet("background-color: #1a1a1a; color: #757575; border-top: 1px solid #333;")
        self.sidebar.setCurrentRow(0)

    def _add_nav_item(self, key: str, label: str, icon_name: str) -> None:
        item = QListWidgetItem(icon(icon_name), f"  {label}")
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

    def _confirm_logout(self) -> None:
        r = QMessageBox.question(
            self, "Confirmar",
            "Deseja sair e voltar para a tela de login?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
