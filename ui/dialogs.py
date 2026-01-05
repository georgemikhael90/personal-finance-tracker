"""
Dialog windows for add/edit operations
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit,
                             QPushButton, QDateEdit, QLabel, QMessageBox)
from PyQt5.QtCore import QDate, Qt
from datetime import datetime

class AccountDialog(QDialog):
    """Dialog for adding/editing accounts"""
    def __init__(self, parent=None, account_data=None):
        super().__init__(parent)
        self.account_data = account_data
        self.setWindowTitle("Add Account" if account_data is None else "Edit Account")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Form layout
        form_layout = QFormLayout()

        # Account name
        self.name_edit = QLineEdit()
        if self.account_data:
            self.name_edit.setText(self.account_data.get('name', ''))
        form_layout.addRow("Account Name:", self.name_edit)

        # Account type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["debit", "credit"])
        if self.account_data:
            index = self.type_combo.findText(self.account_data.get('account_type', 'debit'))
            self.type_combo.setCurrentIndex(index)
        form_layout.addRow("Account Type:", self.type_combo)

        # Initial balance
        self.balance_spin = QDoubleSpinBox()
        self.balance_spin.setRange(-999999999, 999999999)
        self.balance_spin.setDecimals(2)
        self.balance_spin.setPrefix("$ ")
        if self.account_data:
            self.balance_spin.setValue(self.account_data.get('initial_balance', 0))
        form_layout.addRow("Initial Balance:", self.balance_spin)

        # Currency
        self.currency_edit = QLineEdit()
        self.currency_edit.setText(self.account_data.get('currency', 'USD') if self.account_data else 'USD')
        form_layout.addRow("Currency:", self.currency_edit)

        layout.addLayout(form_layout)

        # Help text
        help_label = QLabel("Debit accounts: Bank accounts, cash (positive = money available)\n"
                           "Credit accounts: Credit cards, loans (positive = amount owed)")
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: gray; font-size: 9pt;")
        layout.addWidget(help_label)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.validate_and_accept)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def validate_and_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Account name is required")
            return
        if not self.currency_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Currency is required")
            return
        self.accept()

    def get_data(self):
        """Return form data as dictionary"""
        return {
            'name': self.name_edit.text().strip(),
            'account_type': self.type_combo.currentText(),
            'initial_balance': self.balance_spin.value(),
            'currency': self.currency_edit.text().strip()
        }


class CategoryDialog(QDialog):
    """Dialog for adding/editing categories"""
    def __init__(self, parent=None, category_data=None):
        super().__init__(parent)
        self.category_data = category_data
        self.setWindowTitle("Add Category" if category_data is None else "Edit Category")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Form layout
        form_layout = QFormLayout()

        # Category name
        self.name_edit = QLineEdit()
        if self.category_data:
            self.name_edit.setText(self.category_data.get('name', ''))
        form_layout.addRow("Category Name:", self.name_edit)

        # Category type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        if self.category_data:
            index = self.type_combo.findText(self.category_data.get('type', 'expense'))
            self.type_combo.setCurrentIndex(index)
        form_layout.addRow("Type:", self.type_combo)

        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        if self.category_data:
            self.description_edit.setPlainText(self.category_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.validate_and_accept)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def validate_and_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Category name is required")
            return
        self.accept()

    def get_data(self):
        """Return form data as dictionary"""
        return {
            'name': self.name_edit.text().strip(),
            'type': self.type_combo.currentText(),
            'description': self.description_edit.toPlainText().strip()
        }


class TransactionDialog(QDialog):
    """Dialog for adding/editing transactions"""
    def __init__(self, parent=None, transaction_data=None, accounts=None, categories=None):
        super().__init__(parent)
        self.transaction_data = transaction_data
        self.accounts = accounts or []
        self.categories = categories or []
        self.setWindowTitle("Add Transaction" if transaction_data is None else "Edit Transaction")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Form layout
        form_layout = QFormLayout()

        # Account
        self.account_combo = QComboBox()
        for account in self.accounts:
            self.account_combo.addItem(f"{account['name']} ({account['account_type']})", account['id'])
        if self.transaction_data:
            index = self.account_combo.findData(self.transaction_data.get('account_id'))
            if index >= 0:
                self.account_combo.setCurrentIndex(index)
        form_layout.addRow("Account:", self.account_combo)

        # Transaction type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        if self.transaction_data:
            index = self.type_combo.findText(self.transaction_data.get('transaction_type', 'expense'))
            self.type_combo.setCurrentIndex(index)
        form_layout.addRow("Type:", self.type_combo)

        # Category
        self.category_combo = QComboBox()
        self.populate_categories()
        if self.transaction_data:
            index = self.category_combo.findData(self.transaction_data.get('category_id'))
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        form_layout.addRow("Category:", self.category_combo)

        # Amount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 999999999)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setPrefix("$ ")
        if self.transaction_data:
            self.amount_spin.setValue(self.transaction_data.get('amount', 0))
        else:
            self.amount_spin.setValue(0.01)
        form_layout.addRow("Amount:", self.amount_spin)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.transaction_data and self.transaction_data.get('transaction_date'):
            date_str = self.transaction_data.get('transaction_date')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            self.date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
        else:
            self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_edit)

        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        if self.transaction_data:
            self.description_edit.setPlainText(self.transaction_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.validate_and_accept)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_type_changed(self, transaction_type):
        """Filter categories based on transaction type"""
        self.populate_categories()

    def populate_categories(self):
        """Populate category combo based on transaction type"""
        self.category_combo.clear()
        transaction_type = self.type_combo.currentText()

        for category in self.categories:
            if category['type'] == transaction_type:
                self.category_combo.addItem(category['name'], category['id'])

    def validate_and_accept(self):
        if self.account_combo.count() == 0:
            QMessageBox.warning(self, "Validation Error", "Please create an account first")
            return
        if self.category_combo.count() == 0:
            QMessageBox.warning(self, "Validation Error", "No categories available for this transaction type")
            return
        if self.amount_spin.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than 0")
            return
        self.accept()

    def get_data(self):
        """Return form data as dictionary"""
        return {
            'account_id': self.account_combo.currentData(),
            'category_id': self.category_combo.currentData(),
            'amount': self.amount_spin.value(),
            'transaction_type': self.type_combo.currentText(),
            'description': self.description_edit.toPlainText().strip(),
            'transaction_date': self.date_edit.date().toString('yyyy-MM-dd')
        }
