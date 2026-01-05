"""
Database Manager for Personal Finance Tracker
Handles all SQLite database operations
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = None):
        """Initialize database manager with connection to SQLite database"""
        if db_path is None:
            # Default to Documents folder
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents', 'FinanceTracker')
            os.makedirs(documents_path, exist_ok=True)
            db_path = os.path.join(documents_path, 'finance.db')

        self.db_path = db_path
        self.conn = None
        self.connect()
        self.initialize_database()

    def connect(self):
        """Create database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Access columns by name
            self.conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {e}")

    def initialize_database(self):
        """Create tables if they don't exist"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        try:
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            self.conn.executescript(schema_sql)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Database initialization error: {e}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    # ==================== ACCOUNT OPERATIONS ====================

    def add_account(self, name: str, account_type: str, initial_balance: float = 0, currency: str = 'USD') -> int:
        """Add a new account"""
        try:
            cursor = self.conn.execute(
                """INSERT INTO accounts (name, account_type, initial_balance, current_balance, currency)
                   VALUES (?, ?, ?, ?, ?)""",
                (name, account_type, initial_balance, initial_balance, currency)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise Exception(f"Error adding account: {e}")

    def update_account(self, account_id: int, name: str, account_type: str, initial_balance: float, currency: str):
        """Update account details (recalculates current balance based on transactions)"""
        try:
            # Get current balance from transactions
            cursor = self.conn.execute(
                """SELECT SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) as balance
                   FROM transactions WHERE account_id = ?""",
                (account_id,)
            )
            transaction_balance = cursor.fetchone()['balance'] or 0
            new_current_balance = initial_balance + transaction_balance

            self.conn.execute(
                """UPDATE accounts
                   SET name = ?, account_type = ?, initial_balance = ?, current_balance = ?, currency = ?
                   WHERE id = ?""",
                (name, account_type, initial_balance, new_current_balance, currency, account_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error updating account: {e}")

    def delete_account(self, account_id: int):
        """Delete an account (cascades to transactions)"""
        try:
            self.conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error deleting account: {e}")

    def get_account(self, account_id: int) -> Optional[Dict]:
        """Get a single account by ID"""
        cursor = self.conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_accounts(self) -> List[Dict]:
        """Get all accounts"""
        cursor = self.conn.execute("SELECT * FROM accounts ORDER BY created_date DESC")
        return [dict(row) for row in cursor.fetchall()]

    def get_accounts_by_type(self, account_type: str) -> List[Dict]:
        """Get accounts by type (debit or credit)"""
        cursor = self.conn.execute(
            "SELECT * FROM accounts WHERE account_type = ? ORDER BY name",
            (account_type,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def recalculate_account_balance(self, account_id: int):
        """Recalculate account balance based on transactions"""
        try:
            account = self.get_account(account_id)
            if not account:
                return

            cursor = self.conn.execute(
                """SELECT SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) as balance
                   FROM transactions WHERE account_id = ?""",
                (account_id,)
            )
            transaction_balance = cursor.fetchone()['balance'] or 0
            new_balance = account['initial_balance'] + transaction_balance

            self.conn.execute(
                "UPDATE accounts SET current_balance = ? WHERE id = ?",
                (new_balance, account_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error recalculating balance: {e}")

    # ==================== CATEGORY OPERATIONS ====================

    def add_category(self, name: str, category_type: str, description: str = '') -> int:
        """Add a new category"""
        try:
            cursor = self.conn.execute(
                "INSERT INTO categories (name, type, description) VALUES (?, ?, ?)",
                (name, category_type, description)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise Exception(f"Category '{name}' already exists")
        except sqlite3.Error as e:
            raise Exception(f"Error adding category: {e}")

    def update_category(self, category_id: int, name: str, category_type: str, description: str = ''):
        """Update category details"""
        try:
            self.conn.execute(
                "UPDATE categories SET name = ?, type = ?, description = ? WHERE id = ?",
                (name, category_type, description, category_id)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception(f"Category '{name}' already exists")
        except sqlite3.Error as e:
            raise Exception(f"Error updating category: {e}")

    def delete_category(self, category_id: int):
        """Delete a category (will fail if it has transactions)"""
        try:
            self.conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Cannot delete category: it has associated transactions")
        except sqlite3.Error as e:
            raise Exception(f"Error deleting category: {e}")

    def get_category(self, category_id: int) -> Optional[Dict]:
        """Get a single category by ID"""
        cursor = self.conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_categories(self) -> List[Dict]:
        """Get all categories"""
        cursor = self.conn.execute("SELECT * FROM categories ORDER BY type, name")
        return [dict(row) for row in cursor.fetchall()]

    def get_categories_by_type(self, category_type: str) -> List[Dict]:
        """Get categories by type (income or expense)"""
        cursor = self.conn.execute(
            "SELECT * FROM categories WHERE type = ? ORDER BY name",
            (category_type,)
        )
        return [dict(row) for row in cursor.fetchall()]

    # ==================== TRANSACTION OPERATIONS ====================

    def add_transaction(self, account_id: int, category_id: int, amount: float,
                       transaction_type: str, description: str, transaction_date: str) -> int:
        """Add a new transaction"""
        try:
            cursor = self.conn.execute(
                """INSERT INTO transactions
                   (account_id, category_id, amount, transaction_type, description, transaction_date)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (account_id, category_id, amount, transaction_type, description, transaction_date)
            )
            transaction_id = cursor.lastrowid
            self.conn.commit()

            # Update account balance
            self.recalculate_account_balance(account_id)

            return transaction_id
        except sqlite3.Error as e:
            raise Exception(f"Error adding transaction: {e}")

    def update_transaction(self, transaction_id: int, account_id: int, category_id: int,
                          amount: float, transaction_type: str, description: str, transaction_date: str):
        """Update transaction details"""
        try:
            # Get old transaction to update old account balance
            old_transaction = self.get_transaction(transaction_id)
            old_account_id = old_transaction['account_id'] if old_transaction else None

            self.conn.execute(
                """UPDATE transactions
                   SET account_id = ?, category_id = ?, amount = ?, transaction_type = ?,
                       description = ?, transaction_date = ?
                   WHERE id = ?""",
                (account_id, category_id, amount, transaction_type, description, transaction_date, transaction_id)
            )
            self.conn.commit()

            # Recalculate balances for both old and new accounts
            if old_account_id and old_account_id != account_id:
                self.recalculate_account_balance(old_account_id)
            self.recalculate_account_balance(account_id)

        except sqlite3.Error as e:
            raise Exception(f"Error updating transaction: {e}")

    def delete_transaction(self, transaction_id: int):
        """Delete a transaction"""
        try:
            # Get account_id before deleting
            transaction = self.get_transaction(transaction_id)
            account_id = transaction['account_id'] if transaction else None

            self.conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.conn.commit()

            # Recalculate account balance
            if account_id:
                self.recalculate_account_balance(account_id)

        except sqlite3.Error as e:
            raise Exception(f"Error deleting transaction: {e}")

    def get_transaction(self, transaction_id: int) -> Optional[Dict]:
        """Get a single transaction by ID"""
        cursor = self.conn.execute(
            """SELECT t.*, a.name as account_name, c.name as category_name
               FROM transactions t
               JOIN accounts a ON t.account_id = a.id
               JOIN categories c ON t.category_id = c.id
               WHERE t.id = ?""",
            (transaction_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_transactions(self, limit: int = None) -> List[Dict]:
        """Get all transactions"""
        query = """SELECT t.*, a.name as account_name, c.name as category_name
                   FROM transactions t
                   JOIN accounts a ON t.account_id = a.id
                   JOIN categories c ON t.category_id = c.id
                   ORDER BY t.transaction_date DESC, t.created_at DESC"""

        if limit:
            query += f" LIMIT {limit}"

        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_transactions_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get transactions within a date range"""
        cursor = self.conn.execute(
            """SELECT t.*, a.name as account_name, c.name as category_name
               FROM transactions t
               JOIN accounts a ON t.account_id = a.id
               JOIN categories c ON t.category_id = c.id
               WHERE t.transaction_date BETWEEN ? AND ?
               ORDER BY t.transaction_date DESC""",
            (start_date, end_date)
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_transactions_by_account(self, account_id: int) -> List[Dict]:
        """Get all transactions for a specific account"""
        cursor = self.conn.execute(
            """SELECT t.*, a.name as account_name, c.name as category_name
               FROM transactions t
               JOIN accounts a ON t.account_id = a.id
               JOIN categories c ON t.category_id = c.id
               WHERE t.account_id = ?
               ORDER BY t.transaction_date DESC""",
            (account_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_transactions_by_category(self, category_id: int) -> List[Dict]:
        """Get all transactions for a specific category"""
        cursor = self.conn.execute(
            """SELECT t.*, a.name as account_name, c.name as category_name
               FROM transactions t
               JOIN accounts a ON t.account_id = a.id
               JOIN categories c ON t.category_id = c.id
               WHERE t.category_id = ?
               ORDER BY t.transaction_date DESC""",
            (category_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    # ==================== REPORTING & ANALYTICS ====================

    def get_cash_on_hand(self) -> float:
        """Calculate cash on hand (debit accounts - credit accounts)"""
        cursor = self.conn.execute(
            """SELECT
                SUM(CASE WHEN account_type = 'debit' THEN current_balance ELSE 0 END) -
                SUM(CASE WHEN account_type = 'credit' THEN current_balance ELSE 0 END) as cash_on_hand
               FROM accounts"""
        )
        result = cursor.fetchone()
        return result['cash_on_hand'] or 0

    def get_total_by_type(self, account_type: str) -> float:
        """Get total balance for account type"""
        cursor = self.conn.execute(
            "SELECT SUM(current_balance) as total FROM accounts WHERE account_type = ?",
            (account_type,)
        )
        result = cursor.fetchone()
        return result['total'] or 0

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get income/expense summary for a specific month"""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"

        cursor = self.conn.execute(
            """SELECT
                transaction_type,
                SUM(amount) as total
               FROM transactions
               WHERE transaction_date >= ? AND transaction_date < ?
               GROUP BY transaction_type""",
            (start_date, end_date)
        )

        summary = {'income': 0, 'expense': 0}
        for row in cursor.fetchall():
            summary[row['transaction_type']] = row['total']

        summary['net'] = summary['income'] - summary['expense']
        return summary

    def get_yearly_summary(self, year: int) -> Dict:
        """Get income/expense summary for a specific year"""
        cursor = self.conn.execute(
            """SELECT
                transaction_type,
                SUM(amount) as total
               FROM transactions
               WHERE strftime('%Y', transaction_date) = ?
               GROUP BY transaction_type""",
            (str(year),)
        )

        summary = {'income': 0, 'expense': 0}
        for row in cursor.fetchall():
            summary[row['transaction_type']] = row['total']

        summary['net'] = summary['income'] - summary['expense']
        return summary

    def get_category_breakdown(self, start_date: str, end_date: str, transaction_type: str) -> List[Dict]:
        """Get spending/income breakdown by category for date range"""
        cursor = self.conn.execute(
            """SELECT c.name, SUM(t.amount) as total
               FROM transactions t
               JOIN categories c ON t.category_id = c.id
               WHERE t.transaction_date BETWEEN ? AND ?
                 AND t.transaction_type = ?
               GROUP BY c.id, c.name
               ORDER BY total DESC""",
            (start_date, end_date, transaction_type)
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_monthly_trend(self, months: int = 12) -> List[Dict]:
        """Get monthly income/expense trend for the last N months"""
        cursor = self.conn.execute(
            """SELECT
                strftime('%Y-%m', transaction_date) as month,
                transaction_type,
                SUM(amount) as total
               FROM transactions
               WHERE transaction_date >= date('now', '-' || ? || ' months')
               GROUP BY month, transaction_type
               ORDER BY month DESC""",
            (months,)
        )
        return [dict(row) for row in cursor.fetchall()]
