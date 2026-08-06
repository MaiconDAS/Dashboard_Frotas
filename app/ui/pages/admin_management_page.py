from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox,
    QPushButton, QTableView, QVBoxLayout, QWidget, QInputDialog,
)

from app.services.admin_service import AdminService
from app.services.category_service import CategoryService
from app.ui.dialogs.admin_edit_dialog import AdminEditDialog
from app.ui.dialogs.audit_dialog import AuditDialog
from app.ui.icons import icon
from app.ui.models.admin_table_model import AdminTableModel

logger = logging.getLogger(__name__)


class AdminManagementPage(QWidget):
    def __init__(self, current_admin_id: int | None = None, parent=None) -> None:
        super().__init__(parent)
        self.current_admin_id = current_admin_id
        self.model = AdminTableModel()

        title = QLabel("Gestao")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #E53935;")

        subtitle = QLabel("Gerencie os usuarios administrativos e categorias de veiculos")
        subtitle.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 8px;")

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.doubleClicked.connect(lambda _=None: self.edit_admin())

        btn_edit = QPushButton("Alterar Cadastro")
        btn_edit.setIcon(icon("edit"))
        btn_edit.setFixedHeight(42)
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c62828; }
        """)
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.clicked.connect(self.edit_admin)

        btn_master = QPushButton("Alterar Senha Mestra")
        btn_master.setFixedHeight(42)
        btn_master.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E53935; border-color: #E53935; color: white; }
        """)
        btn_master.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_master.clicked.connect(self.change_master_password)

        btn_audit = QPushButton("Auditoria")
        btn_audit.setFixedHeight(42)
        btn_audit.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E53935; border-color: #E53935; color: white; }
        """)
        btn_audit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_audit.clicked.connect(self.open_audit)

        top = QHBoxLayout()
        top.setSpacing(10)
        top.addWidget(title)
        top.addStretch(1)
        top.addWidget(btn_audit)
        top.addWidget(btn_master)
        top.addWidget(btn_edit)

        sep = QLabel()
        sep.setFixedHeight(2)
        sep.setStyleSheet("background-color: #333333; margin-top: 8px; margin-bottom: 8px;")

        cat_title = QLabel("Categorias de Veiculos")
        cat_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #E53935;")

        cat_sub = QLabel("Adicione, edite ou remova as categorias disponiveis no cadastro de veiculos")
        cat_sub.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 8px;")

        self.cat_list = QListWidget()
        self.cat_list.setFixedHeight(160)
        self.cat_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #f5f5f5;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 4px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #E53935;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #2d2d2d;
            }
        """)

        btn_add_cat = QPushButton("Adicionar")
        btn_add_cat.setFixedHeight(40)
        btn_add_cat.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #E53935; border-color: #E53935; color: white; }
        """)
        btn_add_cat.clicked.connect(self.add_category)

        btn_edit_cat = QPushButton("Editar")
        btn_edit_cat.setFixedHeight(40)
        btn_edit_cat.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #E53935; border-color: #E53935; color: white; }
        """)
        btn_edit_cat.clicked.connect(self.edit_category)

        btn_del_cat = QPushButton("Excluir")
        btn_del_cat.setFixedHeight(40)
        btn_del_cat.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #dc2626; border-color: #dc2626; color: white; }
        """)
        btn_del_cat.clicked.connect(self.delete_category)

        cat_actions = QHBoxLayout()
        cat_actions.setSpacing(10)
        cat_actions.addWidget(btn_add_cat)
        cat_actions.addWidget(btn_edit_cat)
        cat_actions.addWidget(btn_del_cat)
        cat_actions.addStretch(1)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20, 16, 20, 16)

        layout.addLayout(top)
        layout.addWidget(subtitle)
        layout.addWidget(self.table)

        layout.addSpacing(20)
        layout.addWidget(sep)

        layout.addSpacing(16)
        layout.addWidget(cat_title)
        layout.addWidget(cat_sub)
        layout.addWidget(self.cat_list)
        layout.addLayout(cat_actions)

        self.setLayout(layout)

        self.refresh()
        self.refresh_categories()

    def _selected_admin(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return None
        return self.model.item_at(idx.row())

    def refresh(self) -> None:
        try:
            items = AdminService.get_all()
            self.model.set_items(items)
        except Exception:
            logger.exception("Falha ao listar administradores")
            QMessageBox.critical(self, "Erro", "Falha ao carregar administradores. Veja o log.")

    def edit_admin(self) -> None:
        a = self._selected_admin()
        if not a:
            QMessageBox.information(self, "Selecionar", "Selecione um administrador.")
            return
        dlg = AdminEditDialog(
            admin_id=a["id"],
            username=a["username"],
            nome_completo=a["nome_completo"],
            is_master=bool(a.get("is_master", False)),
            current_admin_id=self.current_admin_id,
            parent=self,
        )
        result = dlg.exec()
        if result in (2, 3):
            self.refresh()

    def change_master_password(self) -> None:
        pwd, ok = QInputDialog.getText(
            self, "Nova Senha Mestra",
            "Digite a nova senha mestra:",
            QLineEdit.EchoMode.Password
        )
        if not ok or not pwd:
            return
        pwd2, ok2 = QInputDialog.getText(
            self, "Confirmar",
            "Confirme a nova senha mestra:",
            QLineEdit.EchoMode.Password
        )
        if not ok2 or pwd != pwd2:
            QMessageBox.warning(self, "Atencao", "As senhas nao coincidem.")
            return
        try:
            AdminService.set_master_password(pwd)
            QMessageBox.information(self, "Sucesso", "Senha mestra alterada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao alterar senha mestra: {str(e)}")

    def open_audit(self) -> None:
        dlg = AuditDialog(self)
        dlg.exec()

    def refresh_categories(self) -> None:
        try:
            cats = CategoryService.list()
            self.cat_list.clear()
            for c in cats:
                self.cat_list.addItem(c)
        except Exception:
            logger.exception("Falha ao carregar categorias")

    def add_category(self) -> None:
        name, ok = QInputDialog.getText(self, "Nova Categoria", "Nome da nova categoria:")
        if not ok or not name.strip():
            return
        try:
            CategoryService.add(name.strip())
            self.refresh_categories()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

    def edit_category(self) -> None:
        item = self.cat_list.currentItem()
        if not item:
            QMessageBox.information(self, "Selecionar", "Selecione uma categoria para editar.")
            return
        old_name = item.text()
        new_name, ok = QInputDialog.getText(self, "Editar Categoria", "Novo nome:", text=old_name)
        if not ok or not new_name.strip():
            return
        try:
            CategoryService.update(old_name, new_name.strip())
            self.refresh_categories()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

    def delete_category(self) -> None:
        item = self.cat_list.currentItem()
        if not item:
            QMessageBox.information(self, "Selecionar", "Selecione uma categoria para excluir.")
            return
        name = item.text()
        r = QMessageBox.question(self, "Confirmar", f"Excluir a categoria '{name}'?")
        if r != QMessageBox.Yes:
            return
        try:
            CategoryService.delete(name)
            self.refresh_categories()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
