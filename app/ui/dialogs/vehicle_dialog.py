from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)


class VehicleDialog(QDialog):
    def __init__(self, parent=None, vehicle: dict | None = None) -> None:
        super().__init__(parent)
        self.vehicle = vehicle
        self.setWindowTitle("Editar Veiculo" if vehicle else "Novo Veiculo")
        self.resize(400, 280)

        self.ed_placa = QLineEdit()
        self.ed_placa.setMaxLength(10)
        self.ed_modelo = QLineEdit()
        self.ed_modelo.setMaxLength(80)
        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(["Carga Pesada", "Carga Leve", "Outros"])
        self.ed_obs = QTextEdit()
        self.ed_obs.setMaximumHeight(80)

        form = QFormLayout()
        form.addRow("Placa*", self.ed_placa)
        form.addRow("Nome (Modelo)*", self.ed_modelo)
        form.addRow("Categoria*", self.cb_categoria)
        form.addRow("Observacoes", self.ed_obs)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btns)
        self.setLayout(layout)

        if vehicle:
            self.ed_placa.setText(vehicle.get("placa", ""))
            self.ed_modelo.setText(vehicle.get("modelo", ""))
            idx = self.cb_categoria.findText(vehicle.get("categoria", "Outros"))
            if idx >= 0:
                self.cb_categoria.setCurrentIndex(idx)
            self.ed_obs.setPlainText(vehicle.get("observacoes") or "")

    def values(self) -> dict:
        return {
            "placa": self.ed_placa.text().strip(),
            "modelo": self.ed_modelo.text().strip(),
            "categoria": self.cb_categoria.currentText(),
            "observacoes": self.ed_obs.toPlainText().strip() or None,
        }
