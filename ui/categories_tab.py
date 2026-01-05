"""
Categories Tab - Manage income and expense categories
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.dialogs import CategoryDialog

class CategoriesTab(QWidget):
    """Categories management tab"""
    categories_changed = pyqtSignal()  # Signal when categories are modified

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_categories()

    def init_ui(self):
        layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Category")
        self.edit_btn = QPushButton("Edit Category")
        self.delete_btn = QPushButton("Delete Category")
        self.refresh_btn = QPushButton("Refresh")

        self.add_btn.clicked.connect(self.add_category)
        self.edit_btn.clicked.connect(self.edit_category)
        self.delete_btn.clicked.connect(self.delete_category)
        self.refresh_btn.clicked.connect(self.load_categories)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)

        layout.addLayout(button_layout)

        # Categories table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Type', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)  # Hide ID column
        self.table.doubleClicked.connect(self.edit_category)

        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_categories(self):
        """Load categories from database"""
        try:
            categories = self.db.get_all_categories()
            self.table.setRowCount(len(categories))

            for row, category in enumerate(categories):
                self.table.setItem(row, 0, QTableWidgetItem(str(category['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(category['name']))

                # Color code category type
                type_item = QTableWidgetItem(category['type'].capitalize())
                if category['type'] == 'income':
                    type_item.setForeground(Qt.darkGreen)
                else:
                    type_item.setForeground(Qt.darkRed)
                self.table.setItem(row, 2, type_item)

                self.table.setItem(row, 3, QTableWidgetItem(category['description'] or ''))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load categories: {str(e)}")

    def add_category(self):
        """Open dialog to add new category"""
        dialog = CategoryDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.db.add_category(
                    data['name'],
                    data['type'],
                    data['description']
                )
                self.load_categories()
                self.categories_changed.emit()
                QMessageBox.information(self, "Success", "Category added successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add category: {str(e)}")

    def edit_category(self):
        """Open dialog to edit selected category"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a category to edit")
            return

        category_id = int(self.table.item(current_row, 0).text())
        category = self.db.get_category(category_id)

        if category:
            dialog = CategoryDialog(self, category)
            if dialog.exec_():
                data = dialog.get_data()
                try:
                    self.db.update_category(
                        category_id,
                        data['name'],
                        data['type'],
                        data['description']
                    )
                    self.load_categories()
                    self.categories_changed.emit()
                    QMessageBox.information(self, "Success", "Category updated successfully")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update category: {str(e)}")

    def delete_category(self):
        """Delete selected category"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a category to delete")
            return

        category_id = int(self.table.item(current_row, 0).text())
        category_name = self.table.item(current_row, 1).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete category '{category_name}'?\n\n"
            "Note: You cannot delete a category that has associated transactions.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.db.delete_category(category_id)
                self.load_categories()
                self.categories_changed.emit()
                QMessageBox.information(self, "Success", "Category deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete category: {str(e)}")
