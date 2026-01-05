"""
Theme Manager for Personal Finance Tracker
Provides Dark, Night Blue, and Light themes
"""

class ThemeManager:
    """Manage application themes and color schemes"""

    THEMES = {
        'white': {
            'name': 'White (Light)',
            'stylesheet': """
                QMainWindow, QDialog, QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }

                QMenuBar {
                    background-color: #f0f0f0;
                    color: #000000;
                }

                QMenuBar::item:selected {
                    background-color: #0078d4;
                    color: #ffffff;
                }

                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                }

                QMenu::item:selected {
                    background-color: #0078d4;
                    color: #ffffff;
                }

                QTabWidget::pane {
                    border: 1px solid #cccccc;
                    background-color: #ffffff;
                }

                QTabBar::tab {
                    background-color: #f0f0f0;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 8px 16px;
                    margin-right: 2px;
                }

                QTabBar::tab:selected {
                    background-color: #ffffff;
                    border-bottom: 2px solid #0078d4;
                }

                QTableWidget {
                    background-color: #ffffff;
                    alternate-background-color: #f5f5f5;
                    gridline-color: #e0e0e0;
                    color: #000000;
                    selection-background-color: #0078d4;
                    selection-color: #ffffff;
                }

                QHeaderView::section {
                    background-color: #f0f0f0;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 6px;
                    font-weight: bold;
                }

                QPushButton {
                    background-color: #0078d4;
                    color: #ffffff;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #005a9e;
                }

                QPushButton:pressed {
                    background-color: #004578;
                }

                QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 6px;
                    border-radius: 3px;
                }

                QLineEdit:focus, QTextEdit:focus {
                    border: 2px solid #0078d4;
                }

                QComboBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    padding: 6px;
                    border-radius: 3px;
                }

                QComboBox:hover {
                    border: 1px solid #0078d4;
                }

                QGroupBox {
                    border: 2px solid #cccccc;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                }

                QGroupBox::title {
                    color: #0078d4;
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }

                QLabel {
                    color: #000000;
                }
            """
        },

        'night': {
            'name': 'Night (Dark)',
            'stylesheet': """
                QMainWindow, QDialog, QWidget {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }

                QMenuBar {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }

                QMenuBar::item:selected {
                    background-color: #3f3f3f;
                    color: #ffffff;
                }

                QMenu {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3f3f3f;
                }

                QMenu::item:selected {
                    background-color: #3f3f3f;
                    color: #ffffff;
                }

                QTabWidget::pane {
                    border: 1px solid #3f3f3f;
                    background-color: #1e1e1e;
                }

                QTabBar::tab {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3f3f3f;
                    padding: 8px 16px;
                    margin-right: 2px;
                }

                QTabBar::tab:selected {
                    background-color: #1e1e1e;
                    border-bottom: 2px solid #bb86fc;
                }

                QTableWidget {
                    background-color: #1e1e1e;
                    alternate-background-color: #252525;
                    gridline-color: #3f3f3f;
                    color: #e0e0e0;
                    selection-background-color: #bb86fc;
                    selection-color: #000000;
                }

                QHeaderView::section {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3f3f3f;
                    padding: 6px;
                    font-weight: bold;
                }

                QPushButton {
                    background-color: #bb86fc;
                    color: #000000;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #d0a9ff;
                }

                QPushButton:pressed {
                    background-color: #9965f4;
                }

                QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3f3f3f;
                    padding: 6px;
                    border-radius: 3px;
                }

                QLineEdit:focus, QTextEdit:focus {
                    border: 2px solid #bb86fc;
                }

                QComboBox {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3f3f3f;
                    padding: 6px;
                    border-radius: 3px;
                }

                QComboBox:hover {
                    border: 1px solid #bb86fc;
                }

                QComboBox QAbstractItemView {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    selection-background-color: #bb86fc;
                    selection-color: #000000;
                }

                QGroupBox {
                    border: 2px solid #3f3f3f;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                    color: #e0e0e0;
                }

                QGroupBox::title {
                    color: #bb86fc;
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }

                QLabel {
                    color: #e0e0e0;
                }
            """
        },

        'night_blue': {
            'name': 'Night Blue',
            'stylesheet': """
                QMainWindow, QDialog, QWidget {
                    background-color: #0d1b2a;
                    color: #e0e8f0;
                }

                QMenuBar {
                    background-color: #1b263b;
                    color: #e0e8f0;
                }

                QMenuBar::item:selected {
                    background-color: #415a77;
                    color: #ffffff;
                }

                QMenu {
                    background-color: #1b263b;
                    color: #e0e8f0;
                    border: 1px solid #415a77;
                }

                QMenu::item:selected {
                    background-color: #415a77;
                    color: #ffffff;
                }

                QTabWidget::pane {
                    border: 1px solid #415a77;
                    background-color: #0d1b2a;
                }

                QTabBar::tab {
                    background-color: #1b263b;
                    color: #e0e8f0;
                    border: 1px solid #415a77;
                    padding: 8px 16px;
                    margin-right: 2px;
                }

                QTabBar::tab:selected {
                    background-color: #0d1b2a;
                    border-bottom: 2px solid #4fc3f7;
                }

                QTableWidget {
                    background-color: #0d1b2a;
                    alternate-background-color: #1b263b;
                    gridline-color: #415a77;
                    color: #e0e8f0;
                    selection-background-color: #4fc3f7;
                    selection-color: #000000;
                }

                QHeaderView::section {
                    background-color: #1b263b;
                    color: #e0e8f0;
                    border: 1px solid #415a77;
                    padding: 6px;
                    font-weight: bold;
                }

                QPushButton {
                    background-color: #4fc3f7;
                    color: #000000;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #29b6f6;
                }

                QPushButton:pressed {
                    background-color: #039be5;
                }

                QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {
                    background-color: #1b263b;
                    color: #e0e8f0;
                    border: 1px solid #415a77;
                    padding: 6px;
                    border-radius: 3px;
                }

                QLineEdit:focus, QTextEdit:focus {
                    border: 2px solid #4fc3f7;
                }

                QComboBox {
                    background-color: #1b263b;
                    color: #e0e8f0;
                    border: 1px solid #415a77;
                    padding: 6px;
                    border-radius: 3px;
                }

                QComboBox:hover {
                    border: 1px solid #4fc3f7;
                }

                QComboBox QAbstractItemView {
                    background-color: #1b263b;
                    color: #e0e8f0;
                    selection-background-color: #4fc3f7;
                    selection-color: #000000;
                }

                QGroupBox {
                    border: 2px solid #415a77;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                    color: #e0e8f0;
                }

                QGroupBox::title {
                    color: #4fc3f7;
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }

                QLabel {
                    color: #e0e8f0;
                }
            """
        }
    }

    @staticmethod
    def get_theme(theme_name):
        """Get theme stylesheet by name"""
        return ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES['white'])

    @staticmethod
    def get_theme_names():
        """Get list of available theme names"""
        return list(ThemeManager.THEMES.keys())

    @staticmethod
    def get_theme_display_names():
        """Get list of theme display names"""
        return {key: value['name'] for key, value in ThemeManager.THEMES.items()}
