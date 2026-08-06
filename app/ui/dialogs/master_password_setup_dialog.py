from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout,
)

from app.services.admin_service import AdminService


class MasterPasswordSetupDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Configuracao Inicial — MADEMAXI")
        self.setFixedSize(480, 420)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 28, 40, 28)

        title = QLabel("Configurar Senha Mestra")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E53935;")
        layout.addWidget(title)

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #E53935;")
        layout.addWidget(line)

        layout.addSpacing(20)

        info = QLabel(
            "Bem-vindo ao Dashboard de Controle de Frotas MADEMAXI.\n\n"
            "A senha mestra e utilizada para cadastrar novos administradores "
            "no sistema. Defina uma senha segura e guarde-a em local seguro.\n\n"
            "Esta configuracao so podera ser alterada futuramente "
            "dentro da aba Gestao por um perfil administrativo."
        )
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 12px; color: #9e9e9e; line-height: 1.5;")
        layout.addWidget(info)

        layout.addSpacing(24)

        lbl_pwd = QLabel("Senha Mestra")
        lbl_pwd.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd)

        self.ed_pwd = QLineEdit()
        self.ed_pwd.setPlaceholderText("Digite a senha mestra desejada")
        self.ed_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_pwd.setFixedHeight(42)
        self.ed_pwd.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_pwd)

        layout.addSpacing(16)

        lbl_pwd2 = QLabel("Confirmar Senha Mestra")
        lbl_pwd2.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd2)

        self.ed_pwd2 = QLineEdit()
        self.ed_pwd2.setPlaceholderText("Repita a senha mestra")
        self.ed_pwd2.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_pwd2.setFixedHeight(42)
        self.ed_pwd2.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_pwd2)

        layout.addSpacing(28)

        btn_save = QPushButton("Salvar e Continuar")
        btn_save.setFixedHeight(44)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 28px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c62828; }
        """)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self._save)
        layout.addWidget(btn_save, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def _save(self) -> None:
        pwd = self.ed_pwd.text()
        pwd2 = self.ed_pwd2.text()

        if not pwd:
            QMessageBox.warning(self, "Atencao", "Digite uma senha mestra.")
            return
        if pwd != pwd2:
            QMessageBox.warning(self, "Atencao", "As senhas nao coincidem.")
            return

        try:
            AdminService.set_master_password(pwd)
            QMessageBox.information(
                self, "Sucesso",
                "Senha mestra configurada com sucesso!\n\n"
                "O sistema sera iniciado agora."
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar senha mestra: {str(e)}")
