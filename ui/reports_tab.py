"""
Reports Tab - Analytics and charts
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QComboBox, QLabel, QGroupBox, QMessageBox, QScrollArea)
from PyQt5.QtCore import QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

class ReportsTab(QWidget):
    """Reports and analytics tab"""

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Control panel
        control_group = QGroupBox("Report Controls")
        control_layout = QHBoxLayout()

        # Report type selector
        control_layout.addWidget(QLabel("Report Type:"))
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Monthly Summary",
            "Yearly Summary",
            "Category Breakdown (Expenses)",
            "Category Breakdown (Income)",
            "Monthly Trend",
            "Account Balances"
        ])
        control_layout.addWidget(self.report_type)

        # Year selector
        control_layout.addWidget(QLabel("Year:"))
        self.year_selector = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 2):
            self.year_selector.addItem(str(year))
        self.year_selector.setCurrentText(str(current_year))
        control_layout.addWidget(self.year_selector)

        # Month selector
        control_layout.addWidget(QLabel("Month:"))
        self.month_selector = QComboBox()
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        for i, month in enumerate(months, 1):
            self.month_selector.addItem(month, i)
        self.month_selector.setCurrentIndex(datetime.now().month - 1)
        control_layout.addWidget(self.month_selector)

        # Generate button
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self.generate_report)
        control_layout.addWidget(self.generate_btn)

        control_layout.addStretch()
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)

        # Summary section
        self.summary_label = QLabel("Select a report type and click 'Generate Report'")
        self.summary_label.setStyleSheet("font-size: 11pt; padding: 10px;")
        layout.addWidget(self.summary_label)

        # Chart area
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def generate_report(self):
        """Generate selected report"""
        report_type = self.report_type.currentText()
        year = int(self.year_selector.currentText())
        month = self.month_selector.currentData()

        try:
            if report_type == "Monthly Summary":
                self.show_monthly_summary(year, month)
            elif report_type == "Yearly Summary":
                self.show_yearly_summary(year)
            elif report_type == "Category Breakdown (Expenses)":
                self.show_category_breakdown(year, month, 'expense')
            elif report_type == "Category Breakdown (Income)":
                self.show_category_breakdown(year, month, 'income')
            elif report_type == "Monthly Trend":
                self.show_monthly_trend()
            elif report_type == "Account Balances":
                self.show_account_balances()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")

    def show_monthly_summary(self, year, month):
        """Show monthly income vs expense summary"""
        summary = self.db.get_monthly_summary(year, month)

        # Update summary text
        month_name = self.month_selector.currentText()
        self.summary_label.setText(
            f"<b>{month_name} {year} Summary</b><br>"
            f"Income: <span style='color: green;'>${summary['income']:.2f}</span> | "
            f"Expenses: <span style='color: red;'>${summary['expense']:.2f}</span> | "
            f"Net: <span style='color: {'green' if summary['net'] >= 0 else 'red'};'>${summary['net']:.2f}</span>"
        )

        # Create chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        categories = ['Income', 'Expenses', 'Net']
        values = [summary['income'], summary['expense'], summary['net']]
        colors = ['#4caf50', '#f44336', '#2196f3']

        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        ax.set_ylabel('Amount ($)')
        ax.set_title(f'{month_name} {year} Financial Summary')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.2f}',
                   ha='center', va='bottom' if height > 0 else 'top')

        self.canvas.draw()

    def show_yearly_summary(self, year):
        """Show yearly income vs expense summary"""
        summary = self.db.get_yearly_summary(year)

        # Update summary text
        self.summary_label.setText(
            f"<b>{year} Annual Summary</b><br>"
            f"Total Income: <span style='color: green;'>${summary['income']:.2f}</span> | "
            f"Total Expenses: <span style='color: red;'>${summary['expense']:.2f}</span> | "
            f"Net: <span style='color: {'green' if summary['net'] >= 0 else 'red'};'>${summary['net']:.2f}</span>"
        )

        # Create chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        categories = ['Income', 'Expenses', 'Net']
        values = [summary['income'], summary['expense'], summary['net']]
        colors = ['#4caf50', '#f44336', '#2196f3']

        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        ax.set_ylabel('Amount ($)')
        ax.set_title(f'{year} Annual Financial Summary')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.2f}',
                   ha='center', va='bottom' if height > 0 else 'top')

        self.canvas.draw()

    def show_category_breakdown(self, year, month, transaction_type):
        """Show pie chart of category breakdown"""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"

        breakdown = self.db.get_category_breakdown(start_date, end_date, transaction_type)

        if not breakdown:
            self.summary_label.setText(f"No {transaction_type} data for this period")
            self.figure.clear()
            self.canvas.draw()
            return

        # Update summary text
        total = sum(item['total'] for item in breakdown)
        month_name = self.month_selector.currentText()
        self.summary_label.setText(
            f"<b>{month_name} {year} {transaction_type.capitalize()} Breakdown</b><br>"
            f"Total {transaction_type.capitalize()}: ${total:.2f}"
        )

        # Create pie chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = [item['name'] for item in breakdown]
        sizes = [item['total'] for item in breakdown]
        colors = plt.cm.Set3(range(len(labels)))

        # Only show percentages > 2% in labels
        def autopct_format(pct):
            return f'{pct:.1f}%' if pct > 2 else ''

        ax.pie(sizes, labels=labels, colors=colors, autopct=autopct_format,
               startangle=90, textprops={'fontsize': 9})
        ax.set_title(f'{month_name} {year} - {transaction_type.capitalize()} by Category')
        ax.axis('equal')

        self.canvas.draw()

    def show_monthly_trend(self):
        """Show monthly income/expense trend for last 12 months"""
        trend_data = self.db.get_monthly_trend(12)

        # Organize data by month
        months = {}
        for row in trend_data:
            month = row['month']
            if month not in months:
                months[month] = {'income': 0, 'expense': 0}
            months[month][row['transaction_type']] = row['total']

        if not months:
            self.summary_label.setText("No transaction data available")
            self.figure.clear()
            self.canvas.draw()
            return

        # Sort months and prepare data
        sorted_months = sorted(months.keys(), reverse=False)
        income_values = [months[m]['income'] for m in sorted_months]
        expense_values = [months[m]['expense'] for m in sorted_months]

        # Update summary text
        total_income = sum(income_values)
        total_expense = sum(expense_values)
        avg_income = total_income / len(sorted_months) if sorted_months else 0
        avg_expense = total_expense / len(sorted_months) if sorted_months else 0

        self.summary_label.setText(
            f"<b>Last {len(sorted_months)} Months Trend</b><br>"
            f"Avg Monthly Income: <span style='color: green;'>${avg_income:.2f}</span> | "
            f"Avg Monthly Expenses: <span style='color: red;'>${avg_expense:.2f}</span>"
        )

        # Create line chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = range(len(sorted_months))
        ax.plot(x, income_values, marker='o', label='Income', color='#4caf50', linewidth=2)
        ax.plot(x, expense_values, marker='o', label='Expenses', color='#f44336', linewidth=2)

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Monthly Income vs Expenses Trend')
        ax.set_xticks(x)
        ax.set_xticklabels(sorted_months, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)

        self.figure.tight_layout()
        self.canvas.draw()

    def show_account_balances(self):
        """Show current account balances"""
        accounts = self.db.get_all_accounts()

        if not accounts:
            self.summary_label.setText("No accounts available")
            self.figure.clear()
            self.canvas.draw()
            return

        # Calculate totals
        cash_on_hand = self.db.get_cash_on_hand()
        total_debit = self.db.get_total_by_type('debit')
        total_credit = self.db.get_total_by_type('credit')

        # Update summary text
        self.summary_label.setText(
            f"<b>Account Balances Summary</b><br>"
            f"Cash on Hand: <span style='color: {'green' if cash_on_hand >= 0 else 'red'};'>${cash_on_hand:.2f}</span> | "
            f"Total Debit: <span style='color: blue;'>${total_debit:.2f}</span> | "
            f"Total Credit: <span style='color: red;'>${total_credit:.2f}</span>"
        )

        # Create horizontal bar chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        account_names = [f"{a['name']} ({a['account_type']})" for a in accounts]
        balances = [a['current_balance'] for a in accounts]
        colors = ['#2196f3' if a['account_type'] == 'debit' else '#f44336' for a in accounts]

        y_pos = range(len(account_names))
        bars = ax.barh(y_pos, balances, color=colors, alpha=0.7)

        ax.set_xlabel('Balance ($)')
        ax.set_title('Account Balances')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(account_names)
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

        # Add value labels
        for i, (bar, balance) in enumerate(zip(bars, balances)):
            ax.text(balance, i, f' ${balance:.2f}', va='center')

        self.figure.tight_layout()
        self.canvas.draw()

    def save_current_report(self, filename):
        """Save the current chart/report to a PDF file"""
        try:
            if self.figure:
                self.figure.savefig(filename, format='pdf', bbox_inches='tight', dpi=300)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"Failed to save report as PDF: {str(e)}")
