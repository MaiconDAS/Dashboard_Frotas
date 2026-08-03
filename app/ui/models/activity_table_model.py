from __future__ import annotations

from typing import List, Optional, Tuple

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class ActivityTableModel(QAbstractTableModel):
    HEADERS = ["Veiculo", "Data", "Quantidade", "Observacoes"]

    def __init__(self) -> None:
        super().__init__()
        self._rows: List[Tuple[dict, dict]] = []

    def set_rows(self, rows: List[Tuple[dict, dict]]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def row_at(self, row: int) -> Optional[Tuple[dict, dict]]:
        if 0 <= row < len(self._rows):
            return self._rows[row]
        return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        a, v = self._rows[index.row()]
        col = index.column()
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            dh = a.get("data_hora")
            data_str = ""
            if dh:
                if hasattr(dh, "strftime"):
                    data_str = dh.strftime("%d/%m/%Y")
                else:
                    data_str = str(dh)[:10]
            values = [
                f"{v.get('placa', '')} - {v.get('modelo', '')}",
                data_str,
                str(a.get("quantidade", "")),
                a.get("observacoes") or "",
            ]
            return values[col]
        return None
