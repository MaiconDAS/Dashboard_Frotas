from __future__ import annotations

from PySide6.QtGui import QIcon

try:
    import qtawesome as qta
except Exception:  # pragma: no cover
    qta = None


def icon(name: str) -> QIcon:
    if qta is None:
        return QIcon()
    # FontAwesome 5 (prefixo "fa5s")
    mapping = {
        "dashboard": "fa5s.chart-line",
        "vehicles": "fa5s.truck",
        "register": "fa5s.edit",
        "history": "fa5s.history",
        "settings": "fa5s.cog",
        "add": "fa5s.plus",
        "edit": "fa5s.pen",
        "delete": "fa5s.trash",
        "pdf": "fa5s.file-pdf",
        "email": "fa5s.envelope",
        "refresh": "fa5s.sync",
        "save": "fa5s.save",
        "search": "fa5s.search",
    }
    key = mapping.get(name, "fa5s.circle")
    return qta.icon(key)

