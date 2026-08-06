from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout,
)

from app.services.audit_service import AuditService


class AuditDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Auditoria de Atividades")
        self.setMinimumSize(980, 640)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("Auditoria de Atividades")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #E53935;")

        subtitle = QLabel("Registro de todas as adicoes, edicoes e exclusoes de atividades da frota")
        subtitle.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 8px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(16)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Data/Hora do Sistema", "Usuario", "Acao", "Descricao", "Data Retroativa"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #f5f5f5;
                border: 1px solid #333333;
                border-radius: 6px;
                gridline-color: #333333;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #e5e7eb;
                padding: 8px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #333333;
            }
            QTableWidget::item {
                padding: 6px 8px;
            }
            QTableWidget::item:selected {
                background-color: #E53935;
                color: white;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        layout.addSpacing(16)

        btn_close = QPushButton("Fechar")
        btn_close.setFixedHeight(44)
        btn_close.setStyleSheet("""
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
        btn_close.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

    def _load_data(self) -> None:
        try:
            logs = AuditService.list_all(limit=2000)
            self.table.setRowCount(len(logs))
            for row, log in enumerate(logs):
                dh = log["data_hora"]
                dh_str = dh.strftime("%d/%m/%Y %H:%M") if hasattr(dh, "strftime") else str(dh)[:16]

                dr = log["data_retroativa"]
                dr_str = dr.strftime("%d/%m/%Y") if dr and hasattr(dr, "strftime") else "-"

                acao_map = {"CREATE": "Criacao", "UPDATE": "Edicao", "DELETE": "Exclusao"}
                acao_str = acao_map.get(log["acao"], log["acao"])

                self.table.setItem(row, 0, QTableWidgetItem(dh_str))
                self.table.setItem(row, 1, QTableWidgetItem(log["usuario"]))
                self.table.setItem(row, 2, QTableWidgetItem(acao_str))
                self.table.setItem(row, 3, QTableWidgetItem(log["descricao"]))
                self.table.setItem(row, 4, QTableWidgetItem(dr_str))

            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setStretchLastSection(True)
        except Exception:
            self.table.setRowCount(0)
