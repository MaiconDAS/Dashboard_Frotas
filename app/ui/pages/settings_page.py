from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

from app.core.config_store import AppConfig, ConfigStore
from app.services.email_service import EmailService
from app.ui.icons import icon

logger = logging.getLogger(__name__)


class SettingsPage(QWidget):
    def __init__(
        self,
        *,
        config_store: ConfigStore,
        email_service: EmailService,
        on_saved: Callable[[], None],
        apply_theme: Callable[[str], None],
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.config_store = config_store
        self.email_service = email_service
        self.on_saved = on_saved
        self.apply_theme_cb = apply_theme

        title = QLabel("Configuracoes")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.ed_company = QLineEdit()
        self.ed_logo = QLineEdit()
        btn_logo = QPushButton("...")
        btn_logo.clicked.connect(self.pick_logo)

        self.cb_theme = QComboBox()
        self.cb_theme.addItems(["dark", "light"])

        self.ed_host = QLineEdit()
        self.sp_port = QSpinBox()
        self.sp_port.setRange(1, 65535)
        self.sp_port.setValue(587)
        self.ed_sender = QLineEdit()
        self.ed_pass = QLineEdit()
        self.ed_pass.setEchoMode(QLineEdit.Password)
        self.ed_manager = QLineEdit()
        self.ck_tls = QCheckBox("Usar TLS (STARTTLS)")
        self.ck_ssl = QCheckBox("Usar SSL")
        self.ck_weekly = QCheckBox("Habilitar envio automatico semanal (segunda 08:00)")

        form = QFormLayout()
        form.addRow("Empresa", self.ed_company)
        logo_row = QHBoxLayout()
        logo_row.addWidget(self.ed_logo, 1)
        logo_row.addWidget(btn_logo)
        form.addRow("Logo (opcional)", logo_row)
        form.addRow("Tema", self.cb_theme)

        form.addRow(QLabel(""))
        form.addRow(QLabel("E-mail (SMTP)"))

        help_row = QHBoxLayout()
        btn_tutorial = QPushButton("Tutorial")
        btn_tutorial.setToolTip("Como configurar o envio de e-mail")
        btn_tutorial.clicked.connect(self.show_smtp_tutorial)

        btn_google = QPushButton("Usar Gmail")
        btn_google.setToolTip("Preencher configuracoes do Gmail automaticamente")
        btn_google.clicked.connect(self.setup_gmail)

        help_row.addWidget(btn_tutorial)
        help_row.addWidget(btn_google)
        help_row.addStretch(1)
        form.addRow("", help_row)

        form.addRow("Servidor SMTP*", self.ed_host)
        form.addRow("Porta SMTP*", self.sp_port)
        form.addRow("E-mail remetente*", self.ed_sender)
        form.addRow("Senha / App Password*", self.ed_pass)
        form.addRow("E-mail do gestor*", self.ed_manager)
        form.addRow("", self.ck_tls)
        form.addRow("", self.ck_ssl)
        form.addRow("", self.ck_weekly)

        btn_test = QPushButton("Testar Configuracao")
        btn_test.clicked.connect(self.test_smtp)

        btn_save = QPushButton("Salvar")
        btn_save.setIcon(icon("save"))
        btn_save.clicked.connect(self.save)

        actions = QHBoxLayout()
        actions.addWidget(btn_test)
        actions.addStretch(1)
        actions.addWidget(btn_save)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(actions)
        layout.addStretch(1)
        self.setLayout(layout)

        self.load()

    def pick_logo(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar logo", "", "Imagens (*.png *.jpg *.jpeg)")
        if path:
            self.ed_logo.setText(path)

    def show_smtp_tutorial(self) -> None:
        texto = (
            "<h3>Como configurar o envio de e-mail automatico</h3>"
            "<p><b>Servidor SMTP:</b> Endereco do servidor de e-mail.<br>"
            "&nbsp;&nbsp;• Gmail: <code>smtp.gmail.com</code><br>"
            "&nbsp;&nbsp;• Outlook/Hotmail: <code>smtp.office365.com</code><br>"
            "&nbsp;&nbsp;• Yahoo: <code>smtp.mail.yahoo.com</code></p>"
            "<p><b>Porta SMTP:</b> Porta de conexao do servidor.<br>"
            "&nbsp;&nbsp;• Gmail: <code>587</code> (TLS) ou <code>465</code> (SSL)<br>"
            "&nbsp;&nbsp;• Outlook: <code>587</code></p>"
            "<p><b>E-mail remetente:</b> Seu endereco de e-mail completo.</p>"
            "<p><b>Senha / App Password:</b> <u>Nao use sua senha normal!</u><br>"
            "&nbsp;&nbsp;• Gmail: ative a verificacao em 2 etapas e gere uma "
            "<a href='https://myaccount.google.com/apppasswords'>App Password</a> "
            "em <i>Seguranca -> Como fazer login no Google -> Senhas de app</i>.<br>"
            "&nbsp;&nbsp;• Outlook: use sua senha normal ou uma senha de app.</p>"
            "<p><b>E-mail do gestor:</b> Endereco que recebera os relatorios semanais.</p>"
            "<p><b>TLS / SSL:</b> Marque <i>Usar TLS</i> para porta 587, ou "
            "<i>Usar SSL</i> para porta 465.</p>"
        )
        msg = QMessageBox(self)
        msg.setWindowTitle("Tutorial de Configuracao SMTP")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(texto)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def setup_gmail(self) -> None:
        import webbrowser

        # Abre a pagina de App Passwords do Google
        webbrowser.open("https://myaccount.google.com/apppasswords")

        # Preenche automaticamente os campos do Gmail
        self.ed_host.setText("smtp.gmail.com")
        self.sp_port.setValue(587)
        self.ck_tls.setChecked(True)
        self.ck_ssl.setChecked(False)

        QMessageBox.information(
            self,
            "Configuracao Gmail",
            "A pagina de App Passwords do Google foi aberta no navegador.\n\n"
            "Campos preenchidos automaticamente:\n"
            "  Servidor: smtp.gmail.com\n"
            "  Porta: 587\n"
            "  TLS: Ativado\n\n"
            "Agora voce precisa:\n"
            "1. Gerar uma App Password no Google (senha de 16 caracteres)\n"
            "2. Preencher seu e-mail no campo 'E-mail remetente'\n"
            "3. Colar a App Password no campo 'Senha'\n"
            "4. Preencher o e-mail do gestor\n"
            "5. Clicar em 'Salvar'"
        )

    def load(self) -> None:
        cfg = self.config_store.get()
        self.ed_company.setText(cfg.company_name)
        self.ed_logo.setText(cfg.logo_path)
        self.cb_theme.setCurrentText(cfg.theme)
        self.ed_host.setText(cfg.smtp_host)
        self.sp_port.setValue(int(cfg.smtp_port))
        self.ed_sender.setText(cfg.sender_email)
        self.ed_pass.setText(cfg.sender_password)
        self.ed_manager.setText(cfg.manager_email)
        self.ck_tls.setChecked(bool(cfg.use_tls))
        self.ck_ssl.setChecked(bool(cfg.use_ssl))
        self.ck_weekly.setChecked(bool(cfg.weekly_enabled))

    def _read_form(self) -> AppConfig:
        cfg = self.config_store.get()
        cfg.company_name = self.ed_company.text().strip() or cfg.company_name
        cfg.logo_path = self.ed_logo.text().strip()
        cfg.theme = self.cb_theme.currentText()
        cfg.smtp_host = self.ed_host.text().strip()
        cfg.smtp_port = int(self.sp_port.value())
        cfg.sender_email = self.ed_sender.text().strip()
        cfg.sender_password = self.ed_pass.text()
        cfg.manager_email = self.ed_manager.text().strip()
        cfg.use_tls = self.ck_tls.isChecked()
        cfg.use_ssl = self.ck_ssl.isChecked()
        cfg.weekly_enabled = self.ck_weekly.isChecked()
        return cfg

    def save(self) -> None:
        try:
            cfg = self._read_form()
            self.config_store.save(cfg)
            self.apply_theme_cb(cfg.theme)
            self.on_saved()
            QMessageBox.information(self, "OK", "Configuracoes salvas.")
        except Exception:
            logger.exception("Falha ao salvar configuracoes")
            QMessageBox.critical(self, "Erro", "Falha ao salvar. Veja o log.")

    def test_smtp(self) -> None:
        try:
            cfg = self._read_form()
            result = self.email_service.test_connection(cfg)
            if result.ok:
                QMessageBox.information(self, "OK", result.message)
            else:
                QMessageBox.warning(self, "Falha", result.message)
        except Exception as e:
            QMessageBox.warning(self, "Falha", str(e))
