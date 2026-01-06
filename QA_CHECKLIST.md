# QA Testing Checklist - Personal Finance Tracker v1.1

## Pre-Test Setup
- [ ] Executable built successfully
- [ ] Executable size verified (~100 MB)
- [ ] Test environment: Windows 10/11
- [ ] Clean database (delete existing `%USERPROFILE%\Documents\FinanceTracker\finance.db`)

## Installation & Launch Tests

### Test 1: First Launch
- [ ] Double-click `PersonalFinanceTracker.exe`
- [ ] Application launches without errors
- [ ] Main window appears with tabs: Accounts, Categories, Transactions, Reports
- [ ] Window title shows "Personal Finance Tracker"
- [ ] Status bar shows "Developed by George Mikhael" at the bottom
- [ ] Database file created at `%USERPROFILE%\Documents\FinanceTracker\finance.db`

**Expected Result**: Application launches successfully, UI is responsive, database is created

### Test 2: UI Elements
- [ ] All tabs are visible (Accounts, Categories, Transactions, Reports)
- [ ] Menu bar visible with: File, View, Help
- [ ] Status bar displays developer credit
- [ ] Window is resizable
- [ ] All buttons and controls are visible

**Expected Result**: Complete UI loads correctly with all elements visible

## Account Management Tests

### Test 3: Create Debit Account
- [ ] Navigate to "Accounts" tab
- [ ] Click "Add Account" button
- [ ] Enter account details:
  - Name: "Test Checking"
  - Type: "debit"
  - Initial Balance: "1000.00"
  - Currency: "USD"
- [ ] Click "OK"
- [ ] Account appears in accounts table
- [ ] Balance displays as $1,000.00

**Expected Result**: Debit account created successfully with correct balance

### Test 4: Create Credit Account
- [ ] Click "Add Account" button
- [ ] Enter account details:
  - Name: "Test Credit Card"
  - Type: "credit"
  - Initial Balance: "500.00"
  - Currency: "USD"
- [ ] Click "OK"
- [ ] Account appears in accounts table
- [ ] Balance displays as $500.00

**Expected Result**: Credit account created successfully

### Test 5: Edit Account
- [ ] Double-click "Test Checking" account
- [ ] Change name to "Updated Checking"
- [ ] Change balance to "1500.00"
- [ ] Click "OK"
- [ ] Account name and balance updated in table
- [ ] New balance displays as $1,500.00

**Expected Result**: Account edits saved correctly

### Test 6: Delete Account
- [ ] Select an account without transactions
- [ ] Click "Delete" button
- [ ] Confirm deletion
- [ ] Account removed from table

**Expected Result**: Account deleted successfully

### Test 7: Cash on Hand Calculation
- [ ] Verify "Cash on Hand" displayed at top of Accounts tab
- [ ] Should equal: Total Debit Balances - Total Credit Balances
- [ ] Example: $1,500 (checking) - $500 (credit card) = $1,000

**Expected Result**: Cash on Hand calculated correctly

## Category Management Tests

### Test 8: View Default Categories
- [ ] Navigate to "Categories" tab
- [ ] Verify predefined categories exist (Salary, Groceries, Rent, etc.)
- [ ] Categories show type (income/expense)

**Expected Result**: Default categories loaded

### Test 9: Create Custom Category
- [ ] Click "Add Category"
- [ ] Enter:
  - Name: "Freelance Income"
  - Type: "income"
- [ ] Click "OK"
- [ ] Category appears in table

**Expected Result**: Custom category created

### Test 10: Edit Category
- [ ] Double-click "Freelance Income"
- [ ] Change name to "Consulting Income"
- [ ] Click "OK"
- [ ] Name updated in table

**Expected Result**: Category edited successfully

### Test 11: Delete Category (Unused)
- [ ] Create a new category "Test Category"
- [ ] Delete it immediately (before using in transactions)
- [ ] Confirm deletion
- [ ] Category removed from list

**Expected Result**: Unused category deleted

## Transaction Management Tests

### Test 12: Add Income Transaction
- [ ] Navigate to "Transactions" tab
- [ ] Click "Add Transaction"
- [ ] Enter:
  - Account: "Updated Checking"
  - Type: "income"
  - Category: "Salary"
  - Amount: "2500.00"
  - Date: Current date
  - Description: "Monthly salary"
- [ ] Click "OK"
- [ ] Transaction appears in table (green color)
- [ ] Account balance updated (+$2,500)

**Expected Result**: Income transaction added, balance increased

### Test 13: Add Expense Transaction
- [ ] Click "Add Transaction"
- [ ] Enter:
  - Account: "Updated Checking"
  - Type: "expense"
  - Category: "Groceries"
  - Amount: "150.00"
  - Date: Current date
  - Description: "Weekly groceries"
- [ ] Click "OK"
- [ ] Transaction appears in table (red color)
- [ ] Account balance updated (-$150)

**Expected Result**: Expense transaction added, balance decreased

### Test 14: Add Credit Card Transaction
- [ ] Click "Add Transaction"
- [ ] Enter:
  - Account: "Test Credit Card"
  - Type: "expense"
  - Category: "Shopping"
  - Amount: "75.00"
  - Date: Current date
  - Description: "Online purchase"
- [ ] Click "OK"
- [ ] Transaction added to credit account
- [ ] Credit balance updated (+$75, showing increased debt)

**Expected Result**: Credit card expense added correctly

### Test 15: Edit Transaction
- [ ] Double-click the "Weekly groceries" transaction
- [ ] Change amount to "175.00"
- [ ] Change description to "Weekly groceries - updated"
- [ ] Click "OK"
- [ ] Transaction updated in table
- [ ] Account balance recalculated correctly

**Expected Result**: Transaction edited and balance updated

### Test 16: Delete Transaction
- [ ] Select a transaction
- [ ] Click "Delete" button
- [ ] Confirm deletion
- [ ] Transaction removed from table
- [ ] Account balance adjusted accordingly

**Expected Result**: Transaction deleted and balance corrected

### Test 17: Filter Transactions by Account
- [ ] Select account in filter dropdown
- [ ] Click "Apply Filters"
- [ ] Only transactions for that account shown

**Expected Result**: Filtering by account works

### Test 18: Filter Transactions by Date Range
- [ ] Set "From Date" and "To Date"
- [ ] Click "Apply Filters"
- [ ] Only transactions in date range shown

**Expected Result**: Date filtering works

### Test 19: Filter by Category
- [ ] Select category in filter dropdown
- [ ] Click "Apply Filters"
- [ ] Only transactions in that category shown

**Expected Result**: Category filtering works

### Test 20: Clear Filters
- [ ] Click "Clear Filters"
- [ ] All transactions displayed again

**Expected Result**: Filters cleared successfully

## Reports Tests

### Test 21: Monthly Summary Report
- [ ] Navigate to "Reports" tab
- [ ] Select "Monthly Summary" report type
- [ ] Select current month and year
- [ ] Click "Generate Report"
- [ ] Report displays:
  - Total income
  - Total expenses
  - Net income (income - expenses)
  - Category breakdown

**Expected Result**: Monthly summary generated correctly

### Test 22: Yearly Summary Report
- [ ] Select "Yearly Summary"
- [ ] Select current year
- [ ] Click "Generate Report"
- [ ] Report shows annual financial overview

**Expected Result**: Yearly summary generated

### Test 23: Category Breakdown (Pie Chart)
- [ ] Select "Category Breakdown"
- [ ] Select month and year
- [ ] Click "Generate Report"
- [ ] Pie chart displays showing expense distribution by category
- [ ] Chart is visible and properly labeled

**Expected Result**: Category pie chart generated

### Test 24: Monthly Trend (Line Chart)
- [ ] Select "Monthly Trend"
- [ ] Select year
- [ ] Click "Generate Report"
- [ ] Line chart shows income vs expenses over 12 months
- [ ] Both lines visible and labeled

**Expected Result**: Trend chart generated successfully

### Test 25: Account Balances Report
- [ ] Select "Account Balances"
- [ ] Click "Generate Report"
- [ ] Chart shows all account balances
- [ ] Debit and credit accounts differentiated

**Expected Result**: Account balances chart generated

## Data Import/Export Tests

### Test 26: Export to CSV
- [ ] Menu → File → Export to CSV
- [ ] Choose save location
- [ ] Save file
- [ ] Open CSV file and verify:
  - All transactions exported
  - Columns include: date, account, type, category, amount, description

**Expected Result**: CSV export successful with complete data

### Test 27: Import from CSV
- [ ] Create a test CSV file with sample transactions
- [ ] Menu → File → Import from CSV
- [ ] Browse and select CSV file
- [ ] Select import account
- [ ] Map columns correctly:
  - Date Column: 0
  - Amount Column: 1
  - Description Column: 2 (if applicable)
- [ ] Click "Import"
- [ ] Verify transactions imported
- [ ] Check account balance updated

**Expected Result**: CSV import successful, transactions added

## Backup & Restore Tests

### Test 28: Create Backup
- [ ] Menu → File → Create Backup
- [ ] Select backup location
- [ ] Backup file created with timestamp
- [ ] Verify backup file exists and has reasonable size

**Expected Result**: Backup created successfully

### Test 29: Restore from Backup
- [ ] Make a note of current data
- [ ] Menu → File → Restore from Backup
- [ ] Select backup file
- [ ] Confirm restore
- [ ] Current database backed up automatically
- [ ] Application prompts to restart
- [ ] Restart application
- [ ] Verify data restored correctly

**Expected Result**: Restore successful, data recovered

## Theme Tests

### Test 30: Change Theme to Night Mode
- [ ] Menu → View → Theme → Night Mode
- [ ] Theme changes to dark theme
- [ ] All UI elements remain readable
- [ ] Theme preference saved

**Expected Result**: Theme changed successfully

### Test 31: Change Theme to Night Blue
- [ ] Menu → View → Theme → Night Blue
- [ ] Theme changes to blue dark theme
- [ ] UI is readable

**Expected Result**: Theme switched to Night Blue

### Test 32: Change Theme to White
- [ ] Menu → View → Theme → White
- [ ] Theme returns to light theme
- [ ] Theme saved for next session

**Expected Result**: Theme returned to White

### Test 33: Theme Persistence
- [ ] Set theme to Night Mode
- [ ] Close application
- [ ] Reopen application
- [ ] Verify Night Mode is still active

**Expected Result**: Theme persists across sessions

## About & Help Tests

### Test 34: About Dialog
- [ ] Menu → Help → About
- [ ] About dialog opens
- [ ] Displays:
  - Application name: "Personal Finance Tracker v1.1"
  - Feature list
  - "Built with Python and PyQt5"
  - "Developed by George Mikhael" (with divider line)
- [ ] Click OK to close

**Expected Result**: About dialog shows correct information with developer credit

## Persistence Tests

### Test 35: Data Persistence
- [ ] Create several accounts, categories, and transactions
- [ ] Note the data
- [ ] Close application
- [ ] Reopen application
- [ ] Verify all data is still present and correct

**Expected Result**: All data persists across sessions

### Test 36: Database Location
- [ ] Navigate to `%USERPROFILE%\Documents\FinanceTracker\`
- [ ] Verify `finance.db` file exists
- [ ] Check file size is reasonable (> 0 bytes)

**Expected Result**: Database file exists in correct location

## Error Handling Tests

### Test 37: Invalid Transaction Amount
- [ ] Try to create transaction with invalid amount (e.g., "abc")
- [ ] Application should handle gracefully with error message

**Expected Result**: Error handled gracefully

### Test 38: Empty Required Fields
- [ ] Try to create account/category/transaction with empty required fields
- [ ] Should show validation error

**Expected Result**: Validation works correctly

### Test 39: Delete Category in Use
- [ ] Try to delete a category that has transactions
- [ ] Should show error or warning
- [ ] Category should not be deleted

**Expected Result**: Prevents deleting category in use

## Performance Tests

### Test 40: Large Dataset
- [ ] Import CSV with 100+ transactions
- [ ] Verify application remains responsive
- [ ] Check reports generate in reasonable time (< 5 seconds)
- [ ] Filtering still works smoothly

**Expected Result**: Good performance with larger datasets

### Test 41: Multiple Accounts
- [ ] Create 10+ accounts
- [ ] Verify dropdown menus still responsive
- [ ] Reports display all accounts correctly

**Expected Result**: Handles multiple accounts well

## Final Verification

### Test 42: Developer Credit Visibility
- [ ] Check status bar: "Developed by George Mikhael" is always visible
- [ ] Check About dialog: Developer credit appears with styling
- [ ] Both locations show credit correctly

**Expected Result**: Developer credit displayed in 2 locations

### Test 43: Version Number
- [ ] About dialog shows "v1.1"
- [ ] Consistent version throughout

**Expected Result**: Version 1.1 displayed

### Test 44: Clean Shutdown
- [ ] Close application using window X button
- [ ] Application closes cleanly without errors
- [ ] No hanging processes

**Expected Result**: Clean shutdown

## Summary

**Total Tests**: 44
**Critical Tests**: 30
**Enhancement Tests**: 14

### Pass Criteria
- All critical functionality tests pass (Tests 1-29, 34, 42-44)
- No data loss or corruption
- UI is fully functional and responsive
- Developer credit properly displayed

### Known Limitations
- None expected for v1.1

---

**QA Checklist Version**: 1.1
**Last Updated**: January 5, 2026
**Tested by**: To be completed
**Test Date**: To be completed
