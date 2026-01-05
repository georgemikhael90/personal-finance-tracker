"""
Transactions Tab - Manage transactions with filtering
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
                             QComboBox, QDateEdit, QLabel, QGroupBox)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from ui.dialogs import TransactionDialog
from datetime import datetime, timedelta

class TransactionsTab(QWidget):
    """Transactions management tab"""
    transactions_changed = pyqtSignal()  # Signal when transactions are modified

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_transactions()

    def init_ui(self):
        layout = QVBoxLayout()

        # Filter section
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()

        # Account filter
        filter_layout.addWidget(QLabel("Account:"))
        self.account_filter = QComboBox()
        self.account_filter.addItem("All Accounts", None)
        self.account_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.account_filter)

        # Category filter
        filter_layout.addWidget(QLabel("Category:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories", None)
        self.category_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.category_filter)

        # Type filter
        filter_layout.addWidget(QLabel("Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Income", "Expense"])
        self.type_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_filter)

        # Date range
        filter_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.dateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.setDate(QDate.currentDate())
        self.date_to.dateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.date_to)

        # Clear filters button
        self.clear_filters_btn = QPushButton("Clear Filters")
        self.clear_filters_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(self.clear_filters_btn)

        filter_layout.addStretch()
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Transaction")
        self.edit_btn = QPushButton("Edit Transaction")
        self.delete_btn = QPushButton("Delete Transaction")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_transaction)
        self.edit_btn.clicked.connect(self.edit_transaction)
        self.delete_btn.clicked.connect(self.delete_transaction)
        self.refresh_btn.clicked.connect(self.load_transactions)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)

        layout.addLayout(button_layout)

        # Transactions table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Account', 'Category', 'Type', 'Amount', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)  # Hide ID column
        self.table.doubleClicked.connect(self.edit_transaction)

        layout.addWidget(self.table)

        # Summary label
        self.summary_label = QLabel("Showing 0 transactions")
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

    def load_filter_options(self):
        """Load accounts and categories into filter dropdowns"""
        # Load accounts
        self.account_filter.clear()
        self.account_filter.addItem("All Accounts", None)
        accounts = self.db.get_all_accounts()
        for account in accounts:
            self.account_filter.addItem(f"{account['name']} ({account['account_type']})", account['id'])

        # Load categories
        self.category_filter.clear()
        self.category_filter.addItem("All Categories", None)
        categories = self.db.get_all_categories()
        for category in categories:
            self.category_filter.addItem(f"{category['name']} ({category['type']})", category['id'])

    def load_transactions(self):
        """Load all transactions from database"""
        self.load_filter_options()
        self.apply_filters()

    def apply_filters(self):
        """Apply current filters to transaction list"""
        try:
            # Get all transactions
            start_date = self.date_from.date().toString('yyyy-MM-dd')
            end_date = self.date_to.date().toString('yyyy-MM-dd')
            transactions = self.db.get_transactions_by_date_range(start_date, end_date)

            # Apply account filter
            account_id = self.account_filter.currentData()
            if account_id is not None:
                transactions = [t for t in transactions if t['account_id'] == account_id]

            # Apply category filter
            category_id = self.category_filter.currentData()
            if category_id is not None:
                transactions = [t for t in transactions if t['category_id'] == category_id]

            # Apply type filter
            type_text = self.type_filter.currentText()
            if type_text != "All Types":
                transactions = [t for t in transactions if t['transaction_type'] == type_text.lower()]

            # Update table
            self.display_transactions(transactions)

            # Update summary
            total_income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
            total_expense = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
            net = total_income - total_expense

            self.summary_label.setText(
                f"Showing {len(transactions)} transactions | "
                f"Income: ${total_income:.2f} | "
                f"Expense: ${total_expense:.2f} | "
                f"Net: ${net:.2f}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load transactions: {str(e)}")

    def display_transactions(self, transactions):
        """Display transactions in table"""
        self.table.setRowCount(len(transactions))

        for row, transaction in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(str(transaction['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(transaction['transaction_date']))
            self.table.setItem(row, 2, QTableWidgetItem(transaction['account_name']))
            self.table.setItem(row, 3, QTableWidgetItem(transaction['category_name']))

            # Color code type
            type_item = QTableWidgetItem(transaction['transaction_type'].capitalize())
            if transaction['transaction_type'] == 'income':
                type_item.setForeground(Qt.darkGreen)
            else:
                type_item.setForeground(Qt.darkRed)
            self.table.setItem(row, 4, type_item)

            # Color code amount
            amount_item = QTableWidgetItem(f"${transaction['amount']:.2f}")
            if transaction['transaction_type'] == 'income':
                amount_item.setForeground(Qt.darkGreen)
            else:
                amount_item.setForeground(Qt.darkRed)
            self.table.setItem(row, 5, amount_item)

            self.table.setItem(row, 6, QTableWidgetItem(transaction['description'] or ''))

    def clear_filters(self):
        """Reset all filters to default"""
        self.account_filter.setCurrentIndex(0)
        self.category_filter.setCurrentIndex(0)
        self.type_filter.setCurrentIndex(0)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_to.setDate(QDate.currentDate())

    def add_transaction(self):
        """Open dialog to add new transaction"""
        accounts = self.db.get_all_accounts()
        categories = self.db.get_all_categories()

        if not accounts:
            QMessageBox.warning(self, "No Accounts", "Please create an account first")
            return
        if not categories:
            QMessageBox.warning(self, "No Categories", "Please create a category first")
            return

        dialog = TransactionDialog(self, accounts=accounts, categories=categories)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.db.add_transaction(
                    data['account_id'],
                    data['category_id'],
                    data['amount'],
                    data['transaction_type'],
                    data['description'],
                    data['transaction_date']
                )
                self.load_transactions()
                self.transactions_changed.emit()
                QMessageBox.information(self, "Success", "Transaction added successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add transaction: {str(e)}")

    def edit_transaction(self):
        """Open dialog to edit selected transaction"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a transaction to edit")
            return

        transaction_id = int(self.table.item(current_row, 0).text())
        transaction = self.db.get_transaction(transaction_id)
        accounts = self.db.get_all_accounts()
        categories = self.db.get_all_categories()

        if transaction:
            dialog = TransactionDialog(self, transaction, accounts, categories)
            if dialog.exec_():
                data = dialog.get_data()
                try:
                    self.db.update_transaction(
                        transaction_id,
                        data['account_id'],
                        data['category_id'],
                        data['amount'],
                        data['transaction_type'],
                        data['description'],
                        data['transaction_date']
                    )
                    self.load_transactions()
                    self.transactions_changed.emit()
                    QMessageBox.information(self, "Success", "Transaction updated successfully")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update transaction: {str(e)}")

    def delete_transaction(self):
        """Delete selected transaction"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a transaction to delete")
            return

        transaction_id = int(self.table.item(current_row, 0).text())
        amount = self.table.item(current_row, 5).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this transaction of {amount}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.db.delete_transaction(transaction_id)
                self.load_transactions()
                self.transactions_changed.emit()
                QMessageBox.information(self, "Success", "Transaction deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete transaction: {str(e)}")
