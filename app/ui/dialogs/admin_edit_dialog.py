from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt

from app.services.admin_service import AdminService


class AdminEditDialog(QDialog):
    def __init__(self, admin_id: int, username: str, nome_completo: str, is_master: bool,
                 current_admin_id: int | None = None, parent=None):
        super().__init__(parent)
        self.admin_id = admin_id
        self.current_admin_id = current_admin_id
        self.setWindowTitle(f"Alterar Cadastro — {username}")
        self.setFixedSize(540, 640)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._setup_ui(username, nome_completo, is_master)

    def _setup_ui(self, username: str, nome_completo: str, is_master: bool):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 28, 40, 28)

        title = QLabel("Alterar Cadastro")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #E53935; margin-bottom: 4px;"
        )
        layout.addWidget(title)

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #E53935;")
        layout.addWidget(line)

        layout.addSpacing(20)

        lbl_nome = QLabel("Nome Completo")
        lbl_nome.setStyleSheet("font-weight: bold; font-size: 14px; color: #e5e7eb;")
        layout.addWidget(lbl_nome)

        self.nome_input = QLineEdit()
        self.nome_input.setText(nome_completo)
        self.nome_input.setPlaceholderText("Digite o nome completo")
        self.nome_input.setFixedHeight(40)
        self.nome_input.setStyleSheet(self._input_style())
        layout.addWidget(self.nome_input)

        layout.addSpacing(16)

        lbl_user = QLabel("Usuario (Login)")
        lbl_user.setStyleSheet("font-weight: bold; font-size: 14px; color: #e5e7eb;")
        layout.addWidget(lbl_user)

        self.user_input = QLineEdit()
        self.user_input.setText(username)
        self.user_input.setPlaceholderText("Digite o nome de usuario")
        self.user_input.setFixedHeight(40)
        self.user_input.setStyleSheet(self._input_style())
        layout.addWidget(self.user_input)

        layout.addSpacing(16)

        lbl_pwd = QLabel("Nova Senha (deixe em branco para manter a atual)")
        lbl_pwd.setStyleSheet("font-weight: bold; font-size: 14px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Digite a nova senha")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setFixedHeight(40)
        self.pwd_input.setStyleSheet(self._input_style())
        layout.addWidget(self.pwd_input)

        layout.addSpacing(16)

        lbl_pwd2 = QLabel("Confirmar Nova Senha")
        lbl_pwd2.setStyleSheet("font-weight: bold; font-size: 14px; color: #e5e7eb;")
        layout.addWidget(lbl_pwd2)

        self.pwd2_input = QLineEdit()
        self.pwd2_input.setPlaceholderText("Repita a nova senha")
        self.pwd2_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd2_input.setFixedHeight(40)
        self.pwd2_input.setStyleSheet(self._input_style())
        layout.addWidget(self.pwd2_input)

        layout.addSpacing(16)

        self.chk_master = QCheckBox("Conta Administradora")
        self.chk_master.setChecked(is_master)
        self.chk_master.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #e5e7eb;
                margin-top: 8px;
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

        layout.addSpacing(24)

        # Botoes em grid 2x2
        btn_grid = QVBoxLayout()
        btn_grid.setSpacing(10)

        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self.deactivate_btn = QPushButton("Inativar")
        self.deactivate_btn.setFixedHeight(44)
        self.deactivate_btn.setStyleSheet("""
            QPushButton {
                background-color: #d97706;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #b45309; }
        """)
        self.deactivate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.deactivate_btn.clicked.connect(self._deactivate)

        self.delete_btn = QPushButton("Excluir Cadastro")
        self.delete_btn.setFixedHeight(44)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self._delete)

        row1.addWidget(self.deactivate_btn, 1)
        row1.addWidget(self.delete_btn, 1)

        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setFixedHeight(44)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #4b5563;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #374151; }
        """)
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("Salvar")
        self.save_btn.setFixedHeight(44)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c62828; }
        """)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self._save)

        row2.addWidget(self.cancel_btn, 1)
        row2.addWidget(self.save_btn, 1)

        btn_grid.addLayout(row1)
        btn_grid.addLayout(row2)
        layout.addLayout(btn_grid)

        layout.addStretch()

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

    def _save(self):
        nome = self.nome_input.text().strip()
        username = self.user_input.text().strip()
        password = self.pwd_input.text()
        password2 = self.pwd2_input.text()

        if not nome or not username:
            QMessageBox.warning(self, "Atencao", "Preencha nome e usuario.")
            return

        new_password = None
        if password or password2:
            if password != password2:
                QMessageBox.warning(self, "Atencao", "As senhas nao coincidem.")
                return
            new_password = password

        try:
            AdminService.update_admin(
                self.admin_id,
                nome_completo=nome,
                username=username,
                new_password=new_password,
            )
            QMessageBox.information(self, "Sucesso", "Cadastro atualizado com sucesso!")
            self.accept()
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                QMessageBox.critical(self, "Erro", f"O usuario '{username}' ja existe.")
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar: {str(e)}")

    def _deactivate(self):
        if self.admin_id == self.current_admin_id:
            QMessageBox.warning(self, "Bloqueado", "Nao e possivel inativar o perfil em uso.")
            return

        username = self.user_input.text().strip()
        r = QMessageBox.question(
            self,
            "Confirmar Inativacao",
            f"Deseja inativar o cadastro de '{username}'?\n\n"
            "O usuario nao podera mais fazer login, mas o cadastro permanece no sistema.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r != QMessageBox.Yes:
            return

        try:
            if AdminService.deactivate_admin(self.admin_id):
                QMessageBox.information(self, "Sucesso", f"Cadastro de '{username}' inativado.")
                self.done(2)
            else:
                QMessageBox.critical(self, "Erro", "Nao foi possivel inativar o cadastro.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inativar: {str(e)}")

    def _delete(self):
        if self.admin_id == self.current_admin_id:
            QMessageBox.warning(self, "Bloqueado", "Nao e possivel excluir o perfil em uso.")
            return

        username = self.user_input.text().strip()
        r = QMessageBox.question(
            self,
            "Confirmar Exclusao",
            f"Tem certeza que deseja EXCLUIR permanentemente o cadastro de '{username}'?\n\n"
            "Esta acao nao pode ser desfeita. O login ficara disponivel para novo cadastro.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r != QMessageBox.Yes:
            return

        try:
            if AdminService.hard_delete_admin(self.admin_id):
                QMessageBox.information(self, "Sucesso", f"Cadastro de '{username}' excluido permanentemente!")
                self.done(3)
            else:
                QMessageBox.critical(self, "Erro", "Nao foi possivel excluir o cadastro.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir: {str(e)}")
