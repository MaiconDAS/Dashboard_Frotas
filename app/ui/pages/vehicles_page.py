from __future__ import annotations

import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app.services.vehicle_service import VehicleService
from app.ui.dialogs.vehicle_dialog import VehicleDialog
from app.ui.icons import icon
from app.ui.models.vehicle_table_model import VehicleTableModel

logger = logging.getLogger(__name__)


class VehiclesPage(QWidget):
    vehicle_changed = Signal()

    def __init__(self, *, vehicle_service: VehicleService, parent=None) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.model = VehicleTableModel()

        title = QLabel("Veiculos")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar por placa ou nome...")
        self.search.textChanged.connect(self.refresh)

        btn_add = QPushButton("Novo")
        btn_add.setIcon(icon("add"))
        btn_add.clicked.connect(self.add_vehicle)

        btn_edit = QPushButton("Editar")
        btn_edit.setIcon(icon("edit"))
        btn_edit.clicked.connect(self.edit_vehicle)

        btn_del = QPushButton("Excluir")
        btn_del.setIcon(icon("delete"))
        btn_del.clicked.connect(self.delete_vehicle)

        top = QHBoxLayout()
        top.addWidget(title)
        top.addStretch(1)
        top.addWidget(self.search, 1)
        top.addWidget(btn_add)
        top.addWidget(btn_edit)
        top.addWidget(btn_del)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(lambda _=None: self.edit_vehicle())
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.refresh()

    def _selected_vehicle(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return None
        return self.model.item_at(idx.row())

    def refresh(self) -> None:
        try:
            items = self.vehicle_service.list(self.search.text())
            self.model.set_items(items)
        except Exception:
            logger.exception("Falha ao listar veiculos")
            QMessageBox.critical(self, "Erro", "Falha ao carregar veiculos. Veja o log.")

    def add_vehicle(self) -> None:
        dlg = VehicleDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.vehicle_service.create(**dlg.values())
            self.refresh()
            self.vehicle_changed.emit()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

    def edit_vehicle(self) -> None:
        v = self._selected_vehicle()
        if not v:
            QMessageBox.information(self, "Selecionar", "Selecione um veiculo.")
            return
        dlg = VehicleDialog(self, vehicle=v)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.vehicle_service.update(v["id"], **dlg.values())
            self.refresh()
            self.vehicle_changed.emit()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

    def delete_vehicle(self) -> None:
        v = self._selected_vehicle()
        if not v:
            QMessageBox.information(self, "Selecionar", "Selecione um veiculo.")
            return
        r = QMessageBox.question(self, "Confirmar", f"Excluir o veiculo {v['placa']}?")
        if r != QMessageBox.Yes:
            return
        try:
            self.vehicle_service.delete(v["id"])
            self.refresh()
            self.vehicle_changed.emit()
        except Exception:
            logger.exception("Falha ao excluir veiculo")
            QMessageBox.critical(self, "Erro", "Falha ao excluir. Veja o log.")
