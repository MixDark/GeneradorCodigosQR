"""
Definición de estilos CSS para los temas claro y oscuro
"""

# Tema Oscuro
ESTILO_OSCURO = """
    QMainWindow {
        background-color: #1a1f2e;
    }
    QWidget {
        background-color: #1a1f2e;
        color: #e0e6ed;
    }
    QLineEdit {
        background-color: #252d3d;
        color: #e0e6ed;
        border: 1px solid #4a7ba7;
        border-radius: 4px;
        padding: 5px;
        selection-background-color: #4a7ba7;
    }
    QPushButton {
        background-color: #4a7ba7;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #5a8bc7;
    }
    QPushButton:pressed {
        background-color: #3a6b87;
    }
    QPushButton:disabled {
        background-color: #3d4556;
        color: #808080;
    }
    QLabel {
        color: #e0e6ed;
    }
    QTabWidget {
        background-color: #1a1f2e;
        border: none;
    }
    QTabBar {
        background-color: #1a1f2e;
    }
    QTabBar::tab {
        background-color: #252d3d;
        color: #b0c3db;
        padding: 6px 20px;
        border: 1px solid #3d4556;
    }
    QTabBar::tab:selected {
        background-color: #4a7ba7;
        color: #ffffff;
        border: 1px solid #4a7ba7;
    }
    QTabBar::tab:hover {
        background-color: #2d5a80;
    }
    QTextEdit {
        background-color: #252d3d;
        color: #e0e6ed;
        border: 1px solid #4a7ba7;
        border-radius: 4px;
        padding: 5px;
    }
    QComboBox {
        background-color: #252d3d;
        color: #e0e6ed;
        border: 1px solid #4a7ba7;
        border-radius: 4px;
        padding: 5px;
    }
    QComboBox::drop-down {
        background-color: #4a7ba7;
        border: none;
    }
    QComboBox QAbstractItemView {
        background-color: #252d3d;
        color: #e0e6ed;
        selection-background-color: #4a7ba7;
    }
    QSpinBox {
        background-color: #252d3d;
        color: #e0e6ed;
        border: 1px solid #4a7ba7;
        border-radius: 4px;
        padding: 5px;
    }
    QCheckBox {
        color: #e0e6ed;
    }
    QCheckBox::indicator {
        border: 1px solid #4a7ba7;
        border-radius: 2px;
    }
    QCheckBox::indicator:checked {
        background-color: #4a7ba7;
    }
    QListWidget {
        background-color: #252d3d;
        color: #e0e6ed;
        border: 1px solid #4a7ba7;
        border-radius: 4px;
    }
    QListWidget::item:selected {
        background-color: #4a7ba7;
    }
    QTableWidget {
        background-color: #252d3d;
        color: #e0e6ed;
        border: 1px solid #4a7ba7;
        gridline-color: #3d4556;
    }
    QTableWidget::item:selected {
        background-color: #4a7ba7;
    }
    QHeaderView::section {
        background-color: #4a7ba7;
        color: #ffffff;
        padding: 5px;
        border: none;
    }
    QProgressBar {
        background-color: #252d3d;
        border: 1px solid #4a7ba7;
        border-radius: 4px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #4a7ba7;
    }
    QScrollBar:vertical {
        background-color: #1a1f2e;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background-color: #4a7ba7;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #5a8bc7;
    }
"""

# Tema Claro
ESTILO_CLARO = """
    QMainWindow {
        background-color: #e8eef5;
    }
    QWidget {
        background-color: #e8eef5;
        color: #1a1f2e;
    }
    QLineEdit {
        background-color: #ffffff;
        color: #1a1f2e;
        border: 1px solid #b0c3db;
        border-radius: 4px;
        padding: 6px;
        selection-background-color: #4a7ba7;
        selection-color: #ffffff;
    }
    QLineEdit:focus {
        border: 2px solid #4a7ba7;
    }
    QPushButton {
        background-color: #4a7ba7;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 7px 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #2d5a80;
    }
    QPushButton:pressed {
        background-color: #1a3a5a;
    }
    QPushButton:disabled {
        background-color: #d0d9e8;
        color: #808080;
    }
    QLabel {
        color: #1a1f2e;
    }
    QTabWidget {
        background-color: #e8eef5;
        border: none;
    }
    QTabBar {
        background-color: #e8eef5;
    }
    QTabBar::tab {
        background-color: #d9e3e9;
        color: #2d5a80;
        padding: 7px 20px;
        border: 1px solid #b0c3db;
        border-bottom: none;
    }
    QTabBar::tab:selected {
        background-color: #4a7ba7;
        color: #ffffff;
        border: 1px solid #4a7ba7;
        border-bottom: none;
    }
    QTabBar::tab:hover {
        background-color: #c9d9e5;
    }
    QTextEdit {
        background-color: #ffffff;
        color: #1a1f2e;
        border: 1px solid #b0c3db;
        border-radius: 4px;
        padding: 6px;
    }
    QTextEdit:focus {
        border: 2px solid #4a7ba7;
    }
    QComboBox {
        background-color: #ffffff;
        color: #1a1f2e;
        border: 1px solid #b0c3db;
        border-radius: 4px;
        padding: 6px;
    }
    QComboBox::drop-down {
        background-color: #4a7ba7;
        border: none;
        width: 20px;
    }
    QComboBox::down-arrow {
        image: none;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #1a1f2e;
        selection-background-color: #4a7ba7;
        selection-color: #ffffff;
    }
    QSpinBox {
        background-color: #ffffff;
        color: #1a1f2e;
        border: 1px solid #b0c3db;
        border-radius: 4px;
        padding: 6px;
    }
    QCheckBox {
        color: #1a1f2e;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 1px solid #b0c3db;
        border-radius: 3px;
        background-color: #ffffff;
    }
    QCheckBox::indicator:checked {
        background-color: #4a7ba7;
        border-color: #4a7ba7;
    }
    QCheckBox::indicator:hover {
        border: 1px solid #4a7ba7;
    }
    QListWidget {
        background-color: #ffffff;
        color: #1a1f2e;
        border: 1px solid #b0c3db;
        border-radius: 4px;
    }
    QListWidget::item {
        padding: 4px;
    }
    QListWidget::item:selected {
        background-color: #4a7ba7;
        color: #ffffff;
    }
    QListWidget::item:hover {
        background-color: #d9e3e9;
    }
    QTableWidget {
        background-color: #ffffff;
        color: #1a1f2e;
        border: 1px solid #b0c3db;
        border-radius: 4px;
        gridline-color: #d9e3e9;
    }
    QTableWidget::item {
        padding: 4px;
    }
    QTableWidget::item:selected {
        background-color: #4a7ba7;
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #d9e3e9;
        color: #2d5a80;
        padding: 6px;
        border: 1px solid #b0c3db;
        font-weight: bold;
    }
    QProgressBar {
        background-color: #d9e3e9;
        border: 1px solid #b0c3db;
        border-radius: 4px;
        text-align: center;
        color: #2d5a80;
    }
    QProgressBar::chunk {
        background-color: #4a7ba7;
        border-radius: 3px;
    }
    QScrollBar:vertical {
        background-color: #e8eef5;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background-color: #b0c3db;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #4a7ba7;
    }
    QDialog {
        background-color: #e8eef5;
    }
"""
