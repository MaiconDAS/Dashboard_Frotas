from PySide6.QtCore import QAbstractTableModel, Qt


class AdminTableModel(QAbstractTableModel):
    _headers = ["ID", "Nome Completo", "Usuario", "Administrador", "Ativo"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []

    def set_items(self, items: list[dict]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def item_at(self, row: int) -> dict | None:
        if 0 <= row < len(self._items):
            return self._items[row]
        return None

    def rowCount(self, parent=None):
        return len(self._items)

    def columnCount(self, parent=None):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        item = self._items[row]

        if role == Qt.DisplayRole:
            if col == 0:
                return str(item.get("id", ""))
            elif col == 1:
                return item.get("nome_completo", "")
            elif col == 2:
                return item.get("username", "")
            elif col == 3:
                return "Sim" if item.get("is_master") else "Nao"
            elif col == 4:
                return "Sim" if item.get("is_active", True) else "Nao"
        return None
