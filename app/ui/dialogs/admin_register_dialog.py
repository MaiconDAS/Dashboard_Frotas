from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QVBoxLayout,
)

from app.services.admin_service import AdminService


class AdminRegisterDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Cadastro")
        self.setFixedSize(520, 580)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 28, 40, 28)

        title = QLabel("Cadastro")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E53935;")
        layout.addWidget(title)

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #E53935;")
        layout.addWidget(line)

        layout.addSpacing(24)

        lbl_nome = QLabel("Nome Completo *")
        lbl_nome.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_nome)

        self.ed_nome = QLineEdit()
        self.ed_nome.setPlaceholderText("Digite o nome completo")
        self.ed_nome.setFixedHeight(42)
        self.ed_nome.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_nome)

        layout.addSpacing(16)

        lbl_user = QLabel("Usuario (Login) *")
        lbl_user.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_user)

        self.ed_user = QLineEdit()
        self.ed_user.setPlaceholderText("Digite o nome de usuario")
        self.ed_user.setFixedHeight(42)
        self.ed_user.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_user)

        layout.addSpacing(16)

        lbl_pwd = QLabel("Senha *")
        lbl_pwd.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd)

        self.ed_pwd = QLineEdit()
        self.ed_pwd.setPlaceholderText("Digite a senha")
        self.ed_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_pwd.setFixedHeight(42)
        self.ed_pwd.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_pwd)

        layout.addSpacing(16)

        lbl_pwd2 = QLabel("Confirmar Senha *")
        lbl_pwd2.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd2)

        self.ed_pwd2 = QLineEdit()
        self.ed_pwd2.setPlaceholderText("Repita a senha")
        self.ed_pwd2.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_pwd2.setFixedHeight(42)
        self.ed_pwd2.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_pwd2)

        layout.addSpacing(12)

        self.chk_master = QCheckBox("Conta Administradora (acesso total ao sistema)")
        self.chk_master.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #e5e7eb;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #555;
            }
            QCheckBox::indicator:checked {
                background-color: #E53935;
                border-color: #E53935;
            }
        """)
        layout.addWidget(self.chk_master)

        layout.addSpacing(28)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setFixedHeight(44)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #4b5563;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 28px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #374151; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Cadastrar")
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

        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

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
        nome = self.ed_nome.text().strip()
        username = self.ed_user.text().strip()
        password = self.ed_pwd.text()
        password2 = self.ed_pwd2.text()
        is_master = self.chk_master.isChecked()

        if not nome or not username or not password:
            QMessageBox.warning(self, "Atencao", "Preencha todos os campos obrigatorios.")
            return
        if password != password2:
            QMessageBox.warning(self, "Atencao", "As senhas nao coincidem.")
            return

        try:
            AdminService.create_admin(
                username=username,
                password=password,
                nome_completo=nome,
                is_master=is_master,
            )
            QMessageBox.information(self, "Sucesso", "Administrador cadastrado com sucesso!")
            self.accept()
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                QMessageBox.critical(self, "Erro", f"O usuario '{username}' ja existe.")
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao cadastrar: {str(e)}")
