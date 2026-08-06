from __future__ import annotations

from typing import List, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class VehicleTableModel(QAbstractTableModel):
    HEADERS = ["Placa", "Nome / Identificacao", "Categoria", "Observacoes"]

    def __init__(self) -> None:
        super().__init__()
        self._items: List[dict] = []

    def set_items(self, items: List[dict]) -> None:
        self.beginResetModel()
        self._items = list(items)
        self.endResetModel()

    def item_at(self, row: int) -> Optional[dict]:
        if 0 <= row < len(self._items):
            return self._items[row]
        return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._items)

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
        v = self._items[index.row()]
        col = index.column()
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            values = [
                v.get("placa", ""),
                v.get("modelo", ""),
                v.get("categoria", ""),
                v.get("observacoes") or "",
            ]
            return values[col]
        return None