from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


def make_palette(theme: str) -> QPalette:
    theme = (theme or "dark").lower()
    if theme == "light":
        p = QPalette()
        p.setColor(QPalette.Window, QColor("#f3f4f6"))
        p.setColor(QPalette.WindowText, QColor("#111827"))
        p.setColor(QPalette.Base, QColor("#ffffff"))
        p.setColor(QPalette.AlternateBase, QColor("#e5e7eb"))
        p.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
        p.setColor(QPalette.ToolTipText, QColor("#111827"))
        p.setColor(QPalette.Text, QColor("#111827"))
        p.setColor(QPalette.Button, QColor("#e5e7eb"))
        p.setColor(QPalette.ButtonText, QColor("#111827"))
        p.setColor(QPalette.Highlight, QColor("#2563eb"))
        p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        p.setColor(QPalette.PlaceholderText, QColor("#6b7280"))
        p.setColor(QPalette.Light, QColor("#ffffff"))
        p.setColor(QPalette.Midlight, QColor("#e5e7eb"))
        p.setColor(QPalette.Mid, QColor("#9ca3af"))
        p.setColor(QPalette.Dark, QColor("#4b5563"))
        p.setColor(QPalette.Shadow, QColor("#374151"))
        return p

    p = QPalette()
    p.setColor(QPalette.Window, QColor("#0b1220"))
    p.setColor(QPalette.WindowText, QColor("#e5e7eb"))
    p.setColor(QPalette.Base, QColor("#0f172a"))
    p.setColor(QPalette.AlternateBase, QColor("#111827"))
    p.setColor(QPalette.ToolTipBase, QColor("#e5e7eb"))
    p.setColor(QPalette.ToolTipText, QColor("#111827"))
    p.setColor(QPalette.Text, QColor("#e5e7eb"))
    p.setColor(QPalette.Button, QColor("#111827"))
    p.setColor(QPalette.ButtonText, QColor("#e5e7eb"))
    p.setColor(QPalette.Highlight, QColor("#3b82f6"))
    p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.PlaceholderText, QColor("#6b7280"))
    p.setColor(QPalette.Light, QColor("#1f2937"))
    p.setColor(QPalette.Midlight, QColor("#374151"))
    p.setColor(QPalette.Mid, QColor("#6b7280"))
    p.setColor(QPalette.Dark, QColor("#9ca3af"))
    p.setColor(QPalette.Shadow, QColor("#000000"))
    return p


def _light_stylesheet() -> str:
    return """
    QWidget {
        background-color: #f3f4f6;
        color: #111827;
    }
    QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {
        background-color: #ffffff;
        color: #111827;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 4px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
        border: 1px solid #2563eb;
    }
    QPushButton {
        background-color: #e5e7eb;
        color: #111827;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #d1d5db;
    }
    QPushButton:pressed {
        background-color: #9ca3af;
    }
    QTableView {
        background-color: #ffffff;
        color: #111827;
        gridline-color: #e5e7eb;
        border: 1px solid #d1d5db;
    }
    QTableView::item:selected {
        background-color: #2563eb;
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #e5e7eb;
        color: #111827;
        padding: 6px;
        border: 1px solid #d1d5db;
    }
    QListWidget {
        background-color: #f3f4f6;
        color: #111827;
        border: none;
    }
    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
    }
    QListWidget::item:selected {
        background-color: #2563eb;
        color: #ffffff;
    }
    QListWidget::item:hover {
        background-color: #d1d5db;
    }
    QTabWidget::pane {
        border: 1px solid #d1d5db;
    }
    QMessageBox {
        background-color: #f3f4f6;
        color: #111827;
    }
    QDialog {
        background-color: #f3f4f6;
        color: #111827;
    }
    QLabel {
        background-color: transparent;
    }
    """


def _dark_stylesheet() -> str:
    return """
    QWidget {
        background-color: #0b1220;
        color: #e5e7eb;
    }
    QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {
        background-color: #111827;
        color: #e5e7eb;
        border: 1px solid #374151;
        border-radius: 4px;
        padding: 4px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
        border: 1px solid #3b82f6;
    }
    QPushButton {
        background-color: #111827;
        color: #e5e7eb;
        border: 1px solid #374151;
        border-radius: 4px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #1f2937;
    }
    QPushButton:pressed {
        background-color: #374151;
    }
    QTableView {
        background-color: #0f172a;
        color: #e5e7eb;
        gridline-color: #1f2937;
        border: 1px solid #374151;
    }
    QTableView::item:selected {
        background-color: #3b82f6;
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #111827;
        color: #e5e7eb;
        padding: 6px;
        border: 1px solid #374151;
    }
    QListWidget {
        background-color: #0b1220;
        color: #e5e7eb;
        border: none;
    }
    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
    }
    QListWidget::item:selected {
        background-color: #3b82f6;
        color: #ffffff;
    }
    QListWidget::item:hover {
        background-color: #1f2937;
    }
    QTabWidget::pane {
        border: 1px solid #374151;
    }
    QMessageBox {
        background-color: #0b1220;
        color: #e5e7eb;
    }
    QDialog {
        background-color: #0b1220;
        color: #e5e7eb;
    }
    QLabel {
        background-color: transparent;
    }
    """


def apply_theme(app: QApplication, theme: str) -> None:
    theme = (theme or "dark").lower()
    app.setPalette(make_palette(theme))
    app.setStyleSheet(_light_stylesheet() if theme == "light" else _dark_stylesheet())
