"""样式常量"""

DARK_STYLE = """
QMainWindow {
    background-color: #1e1e2e;
}
QLabel {
    color: #cdd6f4;
}
QGroupBox {
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 8px;
    font-weight: bold;
}
QGroupBox::title {
    color: #cdd6f4;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
}
QLineEdit, QSpinBox, QComboBox, QListWidget {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 4px;
}
QListWidget {
    background-color: #1e1e2e;
}
QListWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #2a2a3e;
}
QListWidget::item:selected {
    background-color: #45475a;
    color: #89b4fa;
}
QListWidget::item:hover {
    background-color: #313244;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #6366f1;
}
QPushButton:disabled {
    background-color: #252526;
    color: #6b7280;
}
QPushButton.primary {
    background-color: #6366f1;
    color: white;
    font-weight: bold;
    border: none;
}
QPushButton.primary:hover {
    background-color: #4f46e5;
}
QCheckBox {
    color: #cdd6f4;
}
QScrollBar:vertical {
    background: #313244;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #6c7086;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #89b4fa;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QStatusBar {
    color: #a6adc8;
    background-color: #1e1e2e;
}
QMenuBar {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-bottom: 1px solid #313244;
}
QMenuBar::item:selected {
    background-color: #313244;
}
QMenu {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #313244;
}
QMenu::item:selected {
    background-color: #313244;
}
"""

MENU_BAR_STYLE = """
QMenuBar {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-bottom: 1px solid #313244;
}
QMenuBar::item:selected {
    background-color: #313244;
}
QMenu {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #313244;
}
QMenu::item:selected {
    background-color: #313244;
}
"""