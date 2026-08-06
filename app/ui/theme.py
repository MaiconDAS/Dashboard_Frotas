from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


def make_palette(theme: str) -> QPalette:
    theme = (theme or "dark").lower()
    if theme == "light":
        p = QPalette()
        p.setColor(QPalette.Window, QColor("#f5f5f5"))
        p.setColor(QPalette.WindowText, QColor("#212121"))
        p.setColor(QPalette.Base, QColor("#ffffff"))
        p.setColor(QPalette.AlternateBase, QColor("#f5f5f5"))
        p.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
        p.setColor(QPalette.ToolTipText, QColor("#212121"))
        p.setColor(QPalette.Text, QColor("#212121"))
        p.setColor(QPalette.Button, QColor("#e0e0e0"))
        p.setColor(QPalette.ButtonText, QColor("#212121"))
        p.setColor(QPalette.Highlight, QColor("#E53935"))
        p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        p.setColor(QPalette.PlaceholderText, QColor("#9e9e9e"))
        p.setColor(QPalette.Light, QColor("#ffffff"))
        p.setColor(QPalette.Midlight, QColor("#e0e0e0"))
        p.setColor(QPalette.Mid, QColor("#9e9e9e"))
        p.setColor(QPalette.Dark, QColor("#616161"))
        p.setColor(QPalette.Shadow, QColor("#424242"))
        return p

    p = QPalette()
    p.setColor(QPalette.Window, QColor("#121212"))
    p.setColor(QPalette.WindowText, QColor("#f5f5f5"))
    p.setColor(QPalette.Base, QColor("#1e1e1e"))
    p.setColor(QPalette.AlternateBase, QColor("#2d2d2d"))
    p.setColor(QPalette.ToolTipBase, QColor("#1e1e1e"))
    p.setColor(QPalette.ToolTipText, QColor("#f5f5f5"))
    p.setColor(QPalette.Text, QColor("#f5f5f5"))
    p.setColor(QPalette.Button, QColor("#2d2d2d"))
    p.setColor(QPalette.ButtonText, QColor("#f5f5f5"))
    p.setColor(QPalette.Highlight, QColor("#E53935"))
    p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.PlaceholderText, QColor("#757575"))
    p.setColor(QPalette.Light, QColor("#2d2d2d"))
    p.setColor(QPalette.Midlight, QColor("#424242"))
    p.setColor(QPalette.Mid, QColor("#616161"))
    p.setColor(QPalette.Dark, QColor("#757575"))
    p.setColor(QPalette.Shadow, QColor("#000000"))
    return p


def _light_stylesheet() -> str:
    return """
    QWidget {
        background-color: #f5f5f5;
        color: #212121;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }
    QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {
        background-color: #ffffff;
        color: #212121;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
        border: 2px solid #E53935;
    }
    QPushButton {
        background-color: #E53935;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover { background-color: #c62828; }
    QPushButton:pressed { background-color: #b71c1c; }
    QPushButton:disabled { background-color: #e0e0e0; color: #9e9e9e; }
    QTableView {
        background-color: #ffffff;
        color: #212121;
        gridline-color: #e5e7eb;
        border: 1px solid #d1d5db;
        border-radius: 6px;
    }
    QTableView::item:selected { background-color: #E53935; color: white; }
    QHeaderView::section {
        background-color: #1a1a1a;
        color: white;
        padding: 10px;
        font-weight: bold;
        font-size: 13px;
        border: none;
        border-bottom: 2px solid #E53935;
    }
    QListWidget {
        background-color: #f5f5f5;
        color: #212121;
        border: none;
    }
    QListWidget::item {
        padding: 12px;
        border-radius: 6px;
        margin: 2px 4px;
    }
    QListWidget::item:selected { background-color: #E53935; color: white; }
    QListWidget::item:hover:!selected { background-color: #e0e0e0; }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #212121;
        border: 1px solid #d1d5db;
        outline: none;
        selection-background-color: #E53935;
        selection-color: white;
    }
    QSpinBox::up-button, QSpinBox::down-button {
        background-color: #e0e0e0;
        border: 1px solid #d1d5db;
        width: 20px;
    }
    QMessageBox { background-color: #f5f5f5; }
    QDialog { background-color: #f5f5f5; }
    QLabel { background-color: transparent; }
    QGroupBox {
        border: 1px solid #d1d5db;
        border-radius: 6px;
        margin-top: 8px;
        padding-top: 8px;
        font-weight: bold;
        color: #212121;
    }
    QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
    QCheckBox::indicator {
        width: 18px; height: 18px;
        border-radius: 4px;
        border: 2px solid #9e9e9e;
    }
    QCheckBox::indicator:checked { background-color: #E53935; border-color: #E53935; }
    QScrollBar:vertical {
        background-color: #e0e0e0;
        width: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background-color: #9e9e9e;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover { background-color: #E53935; }
    """


def _dark_stylesheet() -> str:
    return """
    QWidget {
        background-color: #121212;
        color: #f5f5f5;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }
    QLineEdit, QSpinBox, QComboBox, QDateEdit, QTextEdit {
        background-color: #1e1e1e;
        color: #f5f5f5;
        border: 1px solid #333333;
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
        border: 2px solid #E53935;
    }
    QPushButton {
        background-color: #E53935;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover { background-color: #c62828; }
    QPushButton:pressed { background-color: #b71c1c; }
    QPushButton:disabled { background-color: #333333; color: #757575; }
    QTableView {
        background-color: #1e1e1e;
        color: #f5f5f5;
        gridline-color: #333333;
        border: 1px solid #333333;
        border-radius: 6px;
    }
    QTableView::item:selected { background-color: #E53935; color: white; }
    QHeaderView::section {
        background-color: #1a1a1a;
        color: #f5f5f5;
        padding: 10px;
        font-weight: bold;
        font-size: 13px;
        border: none;
        border-bottom: 2px solid #E53935;
    }
    QListWidget {
        background-color: #121212;
        color: #f5f5f5;
        border: none;
    }
    QListWidget::item {
        padding: 12px;
        border-radius: 6px;
        margin: 2px 4px;
    }
    QListWidget::item:selected { background-color: #E53935; color: white; }
    QListWidget::item:hover:!selected { background-color: #2d2d2d; }
    QComboBox QAbstractItemView {
        background-color: #1e1e1e;
        color: #f5f5f5;
        border: 1px solid #333333;
        outline: none;
        selection-background-color: #E53935;
        selection-color: white;
    }
    QSpinBox::up-button, QSpinBox::down-button {
        background-color: #2d2d2d;
        border: 1px solid #333333;
        width: 20px;
    }
    QMessageBox { background-color: #121212; }
    QDialog { background-color: #121212; }
    QLabel { background-color: transparent; }
    QGroupBox {
        border: 1px solid #333333;
        border-radius: 6px;
        margin-top: 8px;
        padding-top: 8px;
        font-weight: bold;
        color: #f5f5f5;
    }
    QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
    QCheckBox::indicator {
        width: 18px; height: 18px;
        border-radius: 4px;
        border: 2px solid #555;
    }
    QCheckBox::indicator:checked { background-color: #E53935; border-color: #E53935; }
    QScrollBar:vertical {
        background-color: #1e1e1e;
        width: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background-color: #555;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover { background-color: #E53935; }
    """


def apply_theme(app: QApplication, theme: str) -> None:
    theme = (theme or "dark").lower()
    app.setPalette(make_palette(theme))
    app.setStyleSheet(_light_stylesheet() if theme == "light" else _dark_stylesheet())