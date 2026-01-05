"""
Accounts Tab - Manage debit and credit accounts
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
                             QLabel, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.dialogs import AccountDialog

class AccountsTab(QWidget):
    """Accounts management tab"""
    accounts_changed = pyqtSignal()  # Signal when accounts are modified

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_accounts()

    def init_ui(self):
        layout = QVBoxLayout()

        # Summary section
        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout()

        self.cash_label = QLabel("Cash on Hand: $0.00")
        self.cash_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2e7d32;")
        summary_layout.addWidget(self.cash_label)

        summary_stats = QHBoxLayout()
        self.debit_label = QLabel("Total Debit: $0.00")
        self.credit_label = QLabel("Total Credit: $0.00")
        summary_stats.addWidget(self.debit_label)
        summary_stats.addWidget(self.credit_label)
        summary_stats.addStretch()
        summary_layout.addLayout(summary_stats)

        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Account")
        self.edit_btn = QPushButton("Edit Account")
        self.delete_btn = QPushButton("Delete Account")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_account)
        self.edit_btn.clicked.connect(self.edit_account)
        self.delete_btn.clicked.connect(self.delete_account)
        self.refresh_btn.clicked.connect(self.load_accounts)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)

        layout.addLayout(button_layout)

        # Accounts table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Type', 'Initial Balance', 'Current Balance'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)  # Hide ID column
        self.table.doubleClicked.connect(self.edit_account)

        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_accounts(self):
        """Load accounts from database"""
        try:
            accounts = self.db.get_all_accounts()
            self.table.setRowCount(len(accounts))

            for row, account in enumerate(accounts):
                self.table.setItem(row, 0, QTableWidgetItem(str(account['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(account['name']))

                # Color code account type
                type_item = QTableWidgetItem(account['account_type'].capitalize())
                if account['account_type'] == 'debit':
                    type_item.setForeground(Qt.blue)
                else:
                    type_item.setForeground(Qt.red)
                self.table.setItem(row, 2, type_item)

                # Initial balance
                initial_balance = f"${account['initial_balance']:.2f}"
                self.table.setItem(row, 3, QTableWidgetItem(initial_balance))

                # Current balance with color coding
                current_balance_item = QTableWidgetItem(f"${account['current_balance']:.2f}")
                if account['current_balance'] < 0:
                    current_balance_item.setForeground(Qt.red)
                elif account['current_balance'] > 0:
                    current_balance_item.setForeground(Qt.darkGreen)
                self.table.setItem(row, 4, current_balance_item)

            # Update summary
            self.update_summary()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load accounts: {str(e)}")

    def update_summary(self):
        """Update summary statistics"""
        try:
            cash_on_hand = self.db.get_cash_on_hand()
            total_debit = self.db.get_total_by_type('debit')
            total_credit = self.db.get_total_by_type('credit')

            self.cash_label.setText(f"Cash on Hand: ${cash_on_hand:.2f}")
            self.debit_label.setText(f"Total Debit: ${total_debit:.2f}")
            self.credit_label.setText(f"Total Credit: ${total_credit:.2f}")

            # Color code cash on hand
            if cash_on_hand < 0:
                self.cash_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #c62828;")
            else:
                self.cash_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2e7d32;")

        except Exception as e:
            print(f"Error updating summary: {e}")

    def add_account(self):
        """Open dialog to add new account"""
        dialog = AccountDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.db.add_account(
                    data['name'],
                    data['account_type'],
                    data['initial_balance'],
                    data['currency']
                )
                self.load_accounts()
                self.accounts_changed.emit()
                QMessageBox.information(self, "Success", "Account added successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add account: {str(e)}")

    def edit_account(self):
        """Open dialog to edit selected account"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an account to edit")
            return

        account_id = int(self.table.item(current_row, 0).text())
        account = self.db.get_account(account_id)

        if account:
            dialog = AccountDialog(self, account)
            if dialog.exec_():
                data = dialog.get_data()
                try:
                    self.db.update_account(
                        account_id,
                        data['name'],
                        data['account_type'],
                        data['initial_balance'],
                        data['currency']
                    )
                    self.load_accounts()
                    self.accounts_changed.emit()
                    QMessageBox.information(self, "Success", "Account updated successfully")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update account: {str(e)}")

    def delete_account(self):
        """Delete selected account"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an account to delete")
            return

        account_id = int(self.table.item(current_row, 0).text())
        account_name = self.table.item(current_row, 1).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete account '{account_name}'?\n\n"
            "This will also delete all associated transactions.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.db.delete_account(account_id)
                self.load_accounts()
                self.accounts_changed.emit()
                QMessageBox.information(self, "Success", "Account deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete account: {str(e)}")
