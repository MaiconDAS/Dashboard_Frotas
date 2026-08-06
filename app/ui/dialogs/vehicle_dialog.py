from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
)

from app.core.utils import validar_placa
from app.services.category_service import CategoryService


class VehicleDialog(QDialog):
    def __init__(self, parent=None, vehicle: dict | None = None) -> None:
        super().__init__(parent)
        self.vehicle = vehicle
        self.setWindowTitle("Editar Veiculo" if vehicle else "Novo Veiculo")
        self.setFixedSize(520, 560)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 28, 40, 28)

        title = QLabel("Editar Veiculo" if self.vehicle else "Novo Veiculo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E53935;")
        layout.addWidget(title)

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #E53935;")
        layout.addWidget(line)

        layout.addSpacing(24)

        lbl_placa = QLabel("Placa *")
        lbl_placa.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_placa)

        self.ed_placa = QLineEdit()
        self.ed_placa.setPlaceholderText("Ex: ABC1D23 ou ABC-1234")
        self.ed_placa.setFixedHeight(42)
        self.ed_placa.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_placa)

        layout.addSpacing(16)

        lbl_nome = QLabel("Nome / Identificacao")
        lbl_nome.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_nome)

        self.ed_nome = QLineEdit()
        self.ed_nome.setPlaceholderText("Ex: Caminhao Volvo, Moto Entrega 01, etc")
        self.ed_nome.setFixedHeight(42)
        self.ed_nome.setStyleSheet(self._input_style())
        layout.addWidget(self.ed_nome)

        layout.addSpacing(16)

        lbl_cat = QLabel("Categoria")
        lbl_cat.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_cat)

        self.cb_categoria = QComboBox()
        self.cb_categoria.setFixedHeight(42)
        self.cb_categoria.setStyleSheet("""
            QComboBox {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
            }
            QComboBox:focus { border-color: #E53935; }
        """)
        layout.addWidget(self.cb_categoria)

        layout.addSpacing(16)

        lbl_status = QLabel("Status")
        lbl_status.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_status)

        self.cb_status = QComboBox()
        self.cb_status.addItems(["Ativo", "Inativo", "Em Manutencao"])
        self.cb_status.setFixedHeight(42)
        self.cb_status.setStyleSheet("""
            QComboBox {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
            }
            QComboBox:focus { border-color: #E53935; }
        """)
        layout.addWidget(self.cb_status)

        layout.addSpacing(16)

        lbl_obs = QLabel("Observacoes")
        lbl_obs.setStyleSheet("font-weight: bold; font-size: 13px; color: #e5e7eb;")
        layout.addWidget(lbl_obs)

        self.ed_obs = QTextEdit()
        self.ed_obs.setFixedHeight(100)
        self.ed_obs.setStyleSheet("""
            QTextEdit {
                background-color: #1f2937;
                color: #f3f4f6;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QTextEdit:focus { border-color: #E53935; }
        """)
        layout.addWidget(self.ed_obs)

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

        btn_save = QPushButton("Salvar")
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

        self._load_categories()
        self._load_vehicle_data()

    def _load_categories(self) -> None:
        try:
            cats = CategoryService.list()
            self.cb_categoria.clear()
            self.cb_categoria.addItems(cats)
        except Exception:
            self.cb_categoria.addItems(["Carga Pesada", "Carga Leve", "Outros"])

    def _load_vehicle_data(self) -> None:
        if self.vehicle:
            self.ed_placa.setText(self.vehicle.get("placa", ""))
            self.ed_nome.setText(self.vehicle.get("modelo", "") or "")
            idx = self.cb_categoria.findText(self.vehicle.get("categoria", ""))
            if idx >= 0:
                self.cb_categoria.setCurrentIndex(idx)
            idx_s = self.cb_status.findText(self.vehicle.get("status", "Ativo"))
            if idx_s >= 0:
                self.cb_status.setCurrentIndex(idx_s)
            self.ed_obs.setPlainText(self.vehicle.get("observacoes", "") or "")

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

    def values(self) -> dict:
        return {
            "placa": self.ed_placa.text().strip().upper(),
            "modelo": self.ed_nome.text().strip(),
            "categoria": self.cb_categoria.currentText(),
            "status": self.cb_status.currentText(),
            "observacoes": self.ed_obs.toPlainText().strip() or None,
        }

    def _save(self) -> None:
        v = self.values()
        if not v["placa"]:
            QMessageBox.warning(self, "Validacao", "Placa e obrigatoria.")
            return
        if not validar_placa(v["placa"]):
            QMessageBox.warning(self, "Validacao", "Formato de placa invalido.")
            return
        self.accept()