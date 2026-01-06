# Personal Finance Tracker

A simple, offline desktop application for managing personal finances - similar to QuickBooks but simpler and designed for personal use.

## Features

### Core Functionality
- **Account Management**: Manage both debit accounts (bank accounts, cash) and credit accounts (credit cards, loans)
- **Category Management**: Full CRUD operations on income and expense categories (including predefined categories)
- **Transaction Tracking**: Add, edit, and delete transactions with automatic balance calculations
- **Cash on Hand Calculation**: Automatically calculates total assets minus liabilities

### Reporting & Analytics
- Monthly and yearly financial summaries
- Category breakdown charts (pie charts for income/expense distribution)
- Monthly trend analysis (income vs expenses over time)
- Account balance visualization
- Income vs expense comparisons

### Data Management
- **CSV Import**: Import transactions from bank CSV files with flexible column mapping
- **CSV Export**: Export all transactions for external analysis
- **Backup**: Create timestamped backups of your database
- **Restore**: Restore from previous backups (with automatic backup of current data)

### User Interface
- Clean, professional tabbed interface
- Color-coded transactions (green for income, red for expenses)
- Advanced filtering (by date range, account, category, transaction type)
- Interactive charts using matplotlib
- Double-click to edit entries

## Installation

### Prerequisites
- **Windows 10/11**
- **Python 3.10 or higher** (download from [python.org](https://www.python.org/downloads/))

### Option 1: Run from Source

1. **Install Python** if not already installed
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install Dependencies**
   ```batch
   cd "C:\Users\georg\Desktop\Personal Financial Tracker"
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```batch
   python main.py
   ```

### Option 2: Build Windows Executable

1. **Run the Build Script**
   ```batch
   cd "C:\Users\georg\Desktop\Personal Financial Tracker"
   build_windows.bat
   ```

2. **Find the Executable**
   - The executable will be created in the `dist` folder
   - File: `dist\PersonalFinanceTracker.exe`
   - You can copy this `.exe` file anywhere and run it directly

3. **First Run**
   - On first run, the application will create a database at:
     `C:\Users\[YourUsername]\Documents\FinanceTracker\finance.db`

## Usage Guide

### Getting Started

1. **Launch the Application**
   - Run `python main.py` or double-click `PersonalFinanceTracker.exe`

2. **Create Your First Account**
   - Go to the "Accounts" tab
   - Click "Add Account"
   - Enter account details:
     - Name: e.g., "My Checking Account"
     - Type: "debit" for bank accounts/cash, "credit" for credit cards/loans
     - Initial Balance: Your starting balance
     - Currency: USD (or your currency)

3. **Review Categories**
   - Go to the "Categories" tab
   - The app comes with predefined categories (Salary, Groceries, Rent, etc.)
   - You can add, edit, or delete any category as needed

4. **Add Transactions**
   - Go to the "Transactions" tab
   - Click "Add Transaction"
   - Fill in the details:
     - Account: Select which account the transaction affects
     - Type: Income or Expense
     - Category: Select from available categories
     - Amount: Transaction amount
     - Date: Transaction date
     - Description: Optional notes

### Understanding Account Types

**Debit Accounts** (Assets)
- Bank accounts, savings accounts, cash
- Positive balance = money you have
- Examples: Checking Account, Savings, Cash Wallet

**Credit Accounts** (Liabilities)
- Credit cards, loans, mortgages
- Positive balance = money you owe
- Examples: Visa Card, Car Loan, Mortgage

**Cash on Hand Calculation**
```
Cash on Hand = Total Debit Balances - Total Credit Balances
```

### Using Filters (Transactions Tab)

Filter transactions by:
- **Account**: Show only transactions for a specific account
- **Category**: Filter by category (e.g., only groceries)
- **Type**: Income or Expense only
- **Date Range**: Custom date range

Click "Clear Filters" to reset all filters.

### Generating Reports

1. Go to the "Reports" tab
2. Select report type:
   - **Monthly Summary**: Income vs expenses for a specific month
   - **Yearly Summary**: Annual financial overview
   - **Category Breakdown**: Pie chart showing spending by category
   - **Monthly Trend**: Line chart showing 12-month trend
   - **Account Balances**: Current balances of all accounts
3. Select year and month (if applicable)
4. Click "Generate Report"

### Importing Transactions from CSV

1. Menu → File → Import from CSV
2. Click "Browse" to select your CSV file
3. Select the account to import transactions into
4. Map the columns:
   - **Date Column**: Column containing transaction dates
   - **Amount Column**: Column containing amounts
   - **Description Column**: Optional description
   - **Category Column**: Optional category name
   - **Type Column**: Optional (income/expense)
5. Click "Import"

**Supported Date Formats**:
- YYYY-MM-DD
- MM/DD/YYYY
- DD/MM/YYYY
- And more...

**CSV Example**:
```csv
date,amount,description,category,type
2024-01-15,2500.00,Monthly Salary,Salary,income
2024-01-16,45.50,Grocery shopping,Groceries,expense
2024-01-17,1200.00,Rent payment,Rent,expense
```

### Exporting Transactions

1. Menu → File → Export to CSV
2. Choose save location and filename
3. All transactions will be exported with full details

### Backup & Restore

**Creating a Backup**:
1. Menu → File → Create Backup
2. Select folder to save backup
3. A timestamped backup file will be created (e.g., `finance_backup_20240115_143022.db`)

**Restoring from Backup**:
1. Menu → File → Restore from Backup
2. Select the backup file
3. Confirm the restore operation
4. Current database will be backed up automatically before restore
5. Restart the application

**Recommendation**: Create regular backups, especially before importing large CSV files!

## Project Structure

```
Personal Financial Tracker/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── build_windows.bat          # Windows build script
├── README.md                  # This file
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py          # Database operations
│   └── schema.sql             # Database schema
│
├── models/
│   ├── __init__.py
│   ├── account.py             # Account data model
│   ├── category.py            # Category data model
│   └── transaction.py         # Transaction data model
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # Main application window
│   ├── accounts_tab.py        # Account management UI
│   ├── categories_tab.py      # Category management UI
│   ├── transactions_tab.py    # Transaction management UI
│   ├── reports_tab.py         # Reports and charts UI
│   └── dialogs.py             # Add/Edit dialogs
│
├── utils/
│   ├── __init__.py
│   ├── csv_handler.py         # CSV import/export
│   └── backup.py              # Backup/restore
│
└── resources/
    └── app_icon.ico           # Application icon
```

## Database

### Location
- **Windows**: `C:\Users\[YourUsername]\Documents\FinanceTracker\finance.db`

### Technology
- SQLite3 (no installation required, embedded database)

### Tables
- **accounts**: Store debit and credit accounts
- **categories**: Store income and expense categories
- **transactions**: Store all financial transactions

### Backup Location
- Backups can be saved anywhere you choose
- Recommended: External drive or cloud storage for safety

## Troubleshooting

### Application won't start
- Ensure Python 3.10+ is installed
- Run `pip install -r requirements.txt` to install dependencies
- Check for error messages in the console

### Database errors
- Check that `Documents\FinanceTracker` folder exists and is writable
- Restore from a backup if database is corrupted

### CSV import fails
- Ensure CSV file is properly formatted
- Check column mapping is correct
- Look at the preview table to verify data
- Verify date format is recognized

### Charts not displaying
- Ensure matplotlib is installed: `pip install matplotlib`
- Check that you have data for the selected time period

### Build fails (PyInstaller)
- Install PyInstaller: `pip install pyinstaller`
- Run from command prompt (not PowerShell) for better compatibility
- Check that all dependencies are installed

## Technical Details

### Dependencies
- **PyQt5 5.15.10**: GUI framework
- **matplotlib 3.8.2**: Charts and visualization
- **pandas 2.1.4**: CSV handling
- **numpy 1.26.3**: Numerical operations (required by pandas)
- **pyinstaller 6.3.0**: Build executable

### Platform
- Primary: Windows 10/11
- Compatible with: Windows 7+ (with Python 3.10+)
- Code is cross-platform compatible (Linux/macOS with minor adjustments)

### Database Schema
- Foreign keys enabled for data integrity
- Cascading deletes for accounts → transactions
- Restricted deletes for categories (prevents deleting categories in use)
- Automatic balance recalculation on transaction changes

## Tips & Best Practices

1. **Create accounts first** before adding transactions
2. **Use descriptive names** for accounts and categories
3. **Regular backups**: Backup before major imports or changes
4. **Consistent categories**: Reuse categories for better reporting
5. **Date accuracy**: Use correct transaction dates for accurate trends
6. **Check balances**: Regularly verify account balances match real accounts
7. **CSV imports**: Test with a small file first to verify column mapping

## Keyboard Shortcuts

- **Double-click**: Edit selected item (account, category, or transaction)
- **Delete key**: Delete selected item (after confirmation)
- **Ctrl+Tab**: Switch between tabs
- **Alt+F4**: Close application

## Support & Feedback

This is a standalone application with no internet connectivity required. All data is stored locally on your computer.

For issues or suggestions:
- Review this README for common solutions
- Check the database file exists and is accessible
- Ensure all dependencies are installed correctly

## License

This software is provided as-is for personal use.

---

**Version**: 1.1
**Last Updated**: January 2026
**Developed by**: George Mikhael
**Built with**: Python, PyQt5, SQLite, Matplotlib
