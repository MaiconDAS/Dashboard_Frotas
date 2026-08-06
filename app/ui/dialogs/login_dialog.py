from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget, QInputDialog,
)

from app.services.admin_service import AdminService


class LoginDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Login — MADEMAXI")
        self.setFixedSize(420, 520)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._admin_data = None

        # Atalho global F1 (funciona mesmo com foco em QLineEdit)
        shortcut = QShortcut(QKeySequence("F1"), self)
        shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        shortcut.activated.connect(self._master_register)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(40, 20, 40, 32)

        logo_container = QWidget()
        logo_container.setFixedHeight(200)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_path = Path(__file__).parent.parent.parent / "assets" / "logo_mademaxi.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                scaled = pixmap.scaled(220, 170, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled)
        logo_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        sub = QLabel("Dashboard de Controle de Frotas")
        sub.setStyleSheet("font-size: 11px; color: #757575;")
        sub.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(sub)

        layout.addWidget(logo_container)

        layout.addSpacing(10)

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #E53935; border-radius: 1px;")
        layout.addWidget(line)

        layout.addSpacing(12)

        lbl_user = QLabel("Usuario")
        lbl_user.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_user)

        self.ed_user = QLineEdit()
        self.ed_user.setPlaceholderText("Digite seu usuario")
        self.ed_user.setFixedHeight(40)
        self.ed_user.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_user)

        lbl_pwd = QLabel("Senha")
        lbl_pwd.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd)

        self.ed_pwd = QLineEdit()
        self.ed_pwd.setPlaceholderText("Digite sua senha")
        self.ed_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_pwd.setFixedHeight(40)
        self.ed_pwd.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_pwd)

        layout.addSpacing(12)

        btn_login = QPushButton("Entrar")
        btn_login.setFixedHeight(44)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c62828; }
            QPushButton:pressed { background-color: #b71c1c; }
        """)
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self._login)
        layout.addWidget(btn_login)

        layout.addStretch(1)

    def _input_style(self):
        return """
            QLineEdit {
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
                color: #f3f4f6;
                background-color: #1f2937;
            }
            QLineEdit:focus { border-color: #E53935; }
            QLineEdit::placeholder { color: #9ca3af; }
        """

    def _login(self) -> None:
        user = self.ed_user.text().strip()
        pwd = self.ed_pwd.text().strip()
        if not user or not pwd:
            QMessageBox.warning(self, "Atencao", "Preencha usuario e senha.")
            return
        try:
            admin = AdminService.authenticate(user, pwd)
            if admin:
                self._admin_data = admin
                self.accept()
            else:
                QMessageBox.warning(self, "Erro", "Usuario ou senha incorretos.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na autenticacao: {str(e)}")

    def _master_register(self) -> None:
        from app.ui.dialogs.admin_register_dialog import AdminRegisterDialog
        pwd, ok = QInputDialog.getText(
            self, "Senha Mestra",
            "Digite a senha mestra para acessar o cadastro:",
            QLineEdit.EchoMode.Password
        )
        if not ok or not pwd:
            return
        try:
            if AdminService.validate_master_password(pwd):
                dlg = AdminRegisterDialog(self)
                dlg.exec()
            else:
                QMessageBox.warning(self, "Erro", "Senha mestra incorreta.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na validacao: {str(e)}")

    def get_admin_data(self) -> dict | None:
        return self._admin_data
