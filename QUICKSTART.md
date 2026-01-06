# Quick Start Guide

Get up and running with Personal Finance Tracker in 5 minutes!

## Installation (Choose One)

### Option A: Run Directly (Recommended for first-time use)

1. **Install Python 3.10+** from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

2. **Open Command Prompt** in this folder

3. **Install dependencies**:
   ```batch
   pip install -r requirements.txt
   ```

4. **Create the application icon** (optional):
   ```batch
   python create_icon.py
   ```

5. **Run the app**:
   ```batch
   python main.py
   ```

### Option B: Build Windows Executable

1. **Follow Option A steps 1-4 first**

2. **Build the executable**:
   ```batch
   build_windows.bat
   ```

3. **Run the app**:
   - Find `PersonalFinanceTracker.exe` in the `dist` folder
   - Double-click to run!

## First-Time Setup (5 Steps)

### Step 1: Create Your First Account
- Click the **"Accounts"** tab
- Click **"Add Account"**
- Fill in:
  - Name: "My Bank Account"
  - Type: "debit"
  - Initial Balance: Your current balance (e.g., 1000.00)
- Click **"Save"**

### Step 2: Review Categories
- Click the **"Categories"** tab
- You'll see predefined categories (Salary, Groceries, etc.)
- You can add more, edit, or delete any category!

### Step 3: Add a Transaction
- Click the **"Transactions"** tab
- Click **"Add Transaction"**
- Fill in:
  - Account: Select your account
  - Type: "expense" (or "income")
  - Category: "Groceries" (for example)
  - Amount: 45.50
  - Date: Today's date
  - Description: "Weekly shopping"
- Click **"Save"**

### Step 4: Check Your Balance
- Go back to **"Accounts"** tab
- See your updated balance!
- Check **"Cash on Hand"** summary

### Step 5: View Reports
- Click the **"Reports"** tab
- Select "Monthly Summary"
- Click **"Generate Report"**
- See your income vs expenses chart!

## Daily Usage

### Recording Expenses
1. Transactions tab → Add Transaction
2. Select account and category
3. Enter amount and description
4. Save!

### Checking Balance
- Accounts tab shows all account balances
- "Cash on Hand" = Total money available

### Viewing Spending
- Reports tab → Category Breakdown
- See where your money goes!

## Common Tasks

### Import Bank Statement (CSV)
1. File menu → Import from CSV
2. Select your bank's CSV export
3. Map columns (date, amount, description)
4. Import!

### Create Backup
1. File menu → Create Backup
2. Choose folder (Documents recommended)
3. Done! Backup created with timestamp

### Add New Credit Card
1. Accounts tab → Add Account
2. Name: "Visa Card"
3. Type: "credit"
4. Initial Balance: Current amount owed
5. Save

## Tips

✅ **Create accounts first**, then add transactions
✅ **Backup regularly** - especially before importing CSVs
✅ **Use consistent categories** for better reports
✅ **Double-click to edit** any item in tables
✅ **Filter transactions** by date/account/category to find specific items

## Need Help?

- Read the full **README.md** for detailed instructions
- Check the **Troubleshooting** section in README.md
- Review your filters if transactions aren't showing

## Keyboard Shortcuts

- **Double-click** = Edit item
- **Ctrl+Tab** = Switch tabs
- **Alt+F4** = Close app

---

**That's it! You're ready to track your finances!** 🎉

Start by adding your accounts and a few recent transactions to get familiar with the app.
