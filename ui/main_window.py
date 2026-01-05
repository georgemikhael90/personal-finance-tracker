"""
Main Application Window
"""

from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QMessageBox, QFileDialog,
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QPushButton, QComboBox, QSpinBox,
                             QHeaderView, QGroupBox, QFormLayout, QLineEdit, QActionGroup)
from PyQt5.QtCore import Qt, QDate, QSettings
from ui.accounts_tab import AccountsTab
from ui.categories_tab import CategoriesTab
from ui.transactions_tab import TransactionsTab
from ui.reports_tab import ReportsTab
from ui.themes import ThemeManager
from utils.csv_handler import CSVHandler
from utils.backup import BackupManager
import os
import json

class CSVImportDialog(QDialog):
    """Dialog for CSV import with column mapping"""
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db = db_manager
        self.csv_file = None
        self.preview_data = []
        self.setWindowTitle("Import Transactions from CSV")
        self.setModal(True)
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        file_group = QGroupBox("Select CSV File")
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.browse_btn)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Account selection
        account_group = QGroupBox("Import Settings")
        account_layout = QFormLayout()

        self.account_combo = QComboBox()
        accounts = self.db.get_all_accounts()
        for account in accounts:
            self.account_combo.addItem(f"{account['name']} ({account['account_type']})", account['id'])
        account_layout.addRow("Import to Account:", self.account_combo)
        account_group.setLayout(account_layout)
        layout.addWidget(account_group)

        # Preview table
        preview_group = QGroupBox("CSV Preview")
        preview_layout = QVBoxLayout()
        self.preview_table = QTableWidget()
        self.preview_table.setMaximumHeight(200)
        preview_layout.addWidget(self.preview_table)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # Column mapping
        mapping_group = QGroupBox("Column Mapping")
        mapping_layout = QFormLayout()

        self.date_col = QSpinBox()
        self.date_col.setMinimum(0)
        self.date_col.setMaximum(20)
        mapping_layout.addRow("Date Column (0-indexed):", self.date_col)

        self.amount_col = QSpinBox()
        self.amount_col.setMinimum(0)
        self.amount_col.setMaximum(20)
        mapping_layout.addRow("Amount Column:", self.amount_col)

        self.description_col = QSpinBox()
        self.description_col.setMinimum(-1)
        self.description_col.setMaximum(20)
        self.description_col.setValue(-1)
        mapping_layout.addRow("Description Column (-1 = none):", self.description_col)

        self.category_col = QSpinBox()
        self.category_col.setMinimum(-1)
        self.category_col.setMaximum(20)
        self.category_col.setValue(-1)
        mapping_layout.addRow("Category Column (-1 = none):", self.category_col)

        self.type_col = QSpinBox()
        self.type_col.setMinimum(-1)
        self.type_col.setMaximum(20)
        self.type_col.setValue(-1)
        mapping_layout.addRow("Type Column (-1 = none):", self.type_col)

        mapping_group.setLayout(mapping_layout)
        layout.addWidget(mapping_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import")
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self.do_import)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_file(self):
        """Browse for CSV file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*.*)"
        )

        if filename:
            try:
                self.csv_file = filename
                self.file_label.setText(os.path.basename(filename))
                self.preview_data = CSVHandler.get_csv_preview(filename, 5)
                self.show_preview()
                self.import_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV file: {str(e)}")

    def show_preview(self):
        """Show preview of CSV data"""
        if not self.preview_data:
            return

        self.preview_table.setRowCount(len(self.preview_data))
        self.preview_table.setColumnCount(len(self.preview_data[0]) if self.preview_data else 0)

        for row_idx, row_data in enumerate(self.preview_data):
            for col_idx, cell_data in enumerate(row_data):
                self.preview_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def do_import(self):
        """Perform the import"""
        if not self.csv_file:
            QMessageBox.warning(self, "No File", "Please select a CSV file first")
            return

        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "No Account", "Please create an account first")
            return

        # Get column mapping
        column_mapping = {
            'date': self.date_col.value(),
            'amount': self.amount_col.value(),
        }

        if self.description_col.value() >= 0:
            column_mapping['description'] = self.description_col.value()

        if self.category_col.value() >= 0:
            column_mapping['category'] = self.category_col.value()

        if self.type_col.value() >= 0:
            column_mapping['type'] = self.type_col.value()

        # Build category map
        categories = self.db.get_all_categories()
        category_map = {cat['name']: cat['id'] for cat in categories}

        # Perform import
        try:
            account_id = self.account_combo.currentData()
            success_count, error_count, errors = CSVHandler.import_transactions(
                self.csv_file,
                account_id,
                column_mapping,
                self.db,
                category_map
            )

            # Show results
            result_msg = f"Import completed!\n\nSuccessfully imported: {success_count} transactions\nErrors: {error_count}"

            if errors:
                result_msg += "\n\nFirst 10 errors:\n" + "\n".join(errors[:10])

            QMessageBox.information(self, "Import Complete", result_msg)

            if success_count > 0:
                self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import transactions: {str(e)}")


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Personal Finance Tracker")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize settings
        self.settings = QSettings("PersonalFinanceTracker", "Settings")

        # Initialize UI
        self.init_ui()
        self.create_menu_bar()

        # Load and apply saved theme
        self.load_settings()

    def init_ui(self):
        """Initialize the UI"""
        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.accounts_tab = AccountsTab(self.db)
        self.categories_tab = CategoriesTab(self.db)
        self.transactions_tab = TransactionsTab(self.db)
        self.reports_tab = ReportsTab(self.db)

        # Add tabs
        self.tabs.addTab(self.accounts_tab, "Accounts")
        self.tabs.addTab(self.categories_tab, "Categories")
        self.tabs.addTab(self.transactions_tab, "Transactions")
        self.tabs.addTab(self.reports_tab, "Reports")

        # Connect signals to refresh related tabs
        self.accounts_tab.accounts_changed.connect(self.on_accounts_changed)
        self.categories_tab.categories_changed.connect(self.on_categories_changed)
        self.transactions_tab.transactions_changed.connect(self.on_transactions_changed)

        self.setCentralWidget(self.tabs)

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        # Save report
        save_action = file_menu.addAction('Save Report...')
        save_action.triggered.connect(self.save_report)
        save_action.setShortcut('Ctrl+S')

        # Save report as
        save_as_action = file_menu.addAction('Save Report As...')
        save_as_action.triggered.connect(self.save_report_as)
        save_as_action.setShortcut('Ctrl+Shift+S')

        file_menu.addSeparator()

        # Import CSV
        import_action = file_menu.addAction('Import from CSV...')
        import_action.triggered.connect(self.import_csv)

        # Export CSV
        export_action = file_menu.addAction('Export to CSV...')
        export_action.triggered.connect(self.export_csv)

        file_menu.addSeparator()

        # Backup
        backup_action = file_menu.addAction('Create Backup...')
        backup_action.triggered.connect(self.create_backup)

        # Restore
        restore_action = file_menu.addAction('Restore from Backup...')
        restore_action.triggered.connect(self.restore_backup)

        file_menu.addSeparator()

        # Exit
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)

        # View menu
        view_menu = menubar.addMenu('View')

        # Theme submenu
        theme_menu = view_menu.addMenu('Theme')
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        # Add theme options
        theme_names = ThemeManager.get_theme_display_names()
        for theme_key, theme_name in theme_names.items():
            theme_action = theme_menu.addAction(theme_name)
            theme_action.setCheckable(True)
            theme_action.setData(theme_key)
            theme_action.triggered.connect(lambda checked, key=theme_key: self.change_theme(key))
            theme_group.addAction(theme_action)

        # Store theme actions for later reference
        self.theme_actions = theme_group.actions()

        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)

    def on_accounts_changed(self):
        """Refresh when accounts are modified"""
        self.transactions_tab.load_filter_options()

    def on_categories_changed(self):
        """Refresh when categories are modified"""
        self.transactions_tab.load_filter_options()

    def on_transactions_changed(self):
        """Refresh when transactions are modified"""
        self.accounts_tab.load_accounts()

    def import_csv(self):
        """Import transactions from CSV"""
        dialog = CSVImportDialog(self, self.db)
        if dialog.exec_():
            self.transactions_tab.load_transactions()
            self.accounts_tab.load_accounts()
            QMessageBox.information(self, "Success", "Transactions imported and accounts updated")

    def export_csv(self):
        """Export transactions to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Transactions to CSV",
            f"transactions_{QDate.currentDate().toString('yyyyMMdd')}.csv",
            "CSV Files (*.csv)"
        )

        if filename:
            try:
                transactions = self.db.get_all_transactions()
                if not transactions:
                    QMessageBox.warning(self, "No Data", "No transactions to export")
                    return

                CSVHandler.export_transactions(transactions, filename)
                QMessageBox.information(self, "Success", f"Exported {len(transactions)} transactions to {filename}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export transactions: {str(e)}")

    def create_backup(self):
        """Create database backup"""
        backup_location = QFileDialog.getExistingDirectory(
            self,
            "Select Backup Location",
            os.path.expanduser("~/Documents")
        )

        if backup_location:
            try:
                backup_path = BackupManager.create_backup(self.db.db_path, backup_location)
                QMessageBox.information(
                    self,
                    "Backup Created",
                    f"Database backup created successfully:\n{backup_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create backup: {str(e)}")

    def restore_backup(self):
        """Restore database from backup"""
        backup_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Backup File",
            os.path.expanduser("~/Documents"),
            "Database Files (*.db);;All Files (*.*)"
        )

        if backup_file:
            reply = QMessageBox.question(
                self,
                "Confirm Restore",
                "Restoring from backup will replace your current database.\n"
                "A backup of your current database will be created first.\n\n"
                "Are you sure you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    BackupManager.restore_backup(backup_file, self.db.db_path, create_backup_of_current=True)

                    QMessageBox.information(
                        self,
                        "Restore Complete",
                        "Database restored successfully.\n\n"
                        "Please restart the application for changes to take effect."
                    )

                    self.close()

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to restore backup: {str(e)}")

    def save_report(self):
        """Save current report with last used settings"""
        last_save_path = self.settings.value("last_report_path", "")

        if last_save_path:
            self.save_report_to_file(last_save_path)
        else:
            self.save_report_as()

    def save_report_as(self):
        """Save current report to a new file"""
        # Determine default filename based on current tab
        current_tab = self.tabs.currentWidget()
        default_name = "financial_report"

        if current_tab == self.reports_tab:
            default_name = f"report_{QDate.currentDate().toString('yyyyMMdd')}"
        elif current_tab == self.transactions_tab:
            default_name = f"transactions_{QDate.currentDate().toString('yyyyMMdd')}"
        elif current_tab == self.accounts_tab:
            default_name = f"accounts_{QDate.currentDate().toString('yyyyMMdd')}"

        filename, file_type = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            f"{default_name}.pdf",
            "PDF Files (*.pdf);;CSV Files (*.csv);;JSON Files (*.json);;All Files (*.*)"
        )

        if filename:
            self.save_report_to_file(filename)
            self.settings.setValue("last_report_path", filename)

    def save_report_to_file(self, filename):
        """Save report data to specified file"""
        try:
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext == '.csv':
                # Export transactions to CSV
                transactions = self.db.get_all_transactions()
                CSVHandler.export_transactions(transactions, filename)
                QMessageBox.information(self, "Success", f"Report saved to:\n{filename}")

            elif file_ext == '.json':
                # Export data to JSON
                data = {
                    'accounts': self.db.get_all_accounts(),
                    'categories': self.db.get_all_categories(),
                    'transactions': self.db.get_all_transactions(),
                    'export_date': QDate.currentDate().toString('yyyy-MM-dd')
                }
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                QMessageBox.information(self, "Success", f"Data exported to:\n{filename}")

            elif file_ext == '.pdf':
                # Save current report as PDF (requires matplotlib figure from reports tab)
                if self.tabs.currentWidget() == self.reports_tab:
                    self.reports_tab.save_current_report(filename)
                else:
                    QMessageBox.information(self, "Info",
                                          "Please switch to Reports tab to save charts as PDF.\n"
                                          "For data export, use CSV or JSON format.")
            else:
                QMessageBox.warning(self, "Unsupported Format",
                                   "Please use .csv, .json, or .pdf extension")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save report: {str(e)}")

    def change_theme(self, theme_name):
        """Change application theme"""
        theme = ThemeManager.get_theme(theme_name)
        self.setStyleSheet(theme['stylesheet'])

        # Update theme selection in menu
        for action in self.theme_actions:
            if action.data() == theme_name:
                action.setChecked(True)

        # Save theme preference
        self.settings.setValue("theme", theme_name)

        QMessageBox.information(self, "Theme Changed",
                              f"Theme changed to: {theme['name']}\n\n"
                              "The theme will be remembered for next time.")

    def load_settings(self):
        """Load saved settings"""
        # Load theme
        saved_theme = self.settings.value("theme", "white")
        theme = ThemeManager.get_theme(saved_theme)
        self.setStyleSheet(theme['stylesheet'])

        # Update theme menu selection
        for action in self.theme_actions:
            if action.data() == saved_theme:
                action.setChecked(True)
                break

    def save_settings(self):
        """Save current settings"""
        # Settings are saved automatically by QSettings when values change
        pass

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Personal Finance Tracker",
            "<h3>Personal Finance Tracker v1.0</h3>"
            "<p>A simple, offline desktop application for managing personal finances.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Manage debit and credit accounts</li>"
            "<li>Track income and expenses</li>"
            "<li>Categorize transactions</li>"
            "<li>Generate reports and charts</li>"
            "<li>Import/Export CSV files</li>"
            "<li>Backup and restore database</li>"
            "<li>Multiple themes (White, Night, Night Blue)</li>"
            "</ul>"
            "<p>Built with Python and PyQt5</p>"
        )

    def closeEvent(self, event):
        """Handle window close event"""
        self.save_settings()
        self.db.close()
        event.accept()
