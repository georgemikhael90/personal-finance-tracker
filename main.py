"""
Personal Finance Tracker - Main Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from database.db_manager import DatabaseManager
from ui.main_window import MainWindow

def main():
    """Main application entry point"""
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Personal Finance Tracker")

    # Set application style
    app.setStyle('Fusion')

    try:
        # Initialize database
        db_manager = DatabaseManager()

        # Create and show main window
        window = MainWindow(db_manager)
        window.show()

        # Run application
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
