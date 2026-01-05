-- Personal Finance Tracker Database Schema

-- Accounts table (Debit and Credit accounts)
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    account_type TEXT NOT NULL CHECK(account_type IN ('debit', 'credit')),
    initial_balance REAL DEFAULT 0,
    current_balance REAL DEFAULT 0,
    currency TEXT DEFAULT 'USD',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table (Income and Expense categories)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    description TEXT
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense')),
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_accounts_type ON accounts(account_type);

-- Insert default categories
INSERT OR IGNORE INTO categories (name, type, description) VALUES
    ('Salary', 'income', 'Monthly salary and wages'),
    ('Freelance', 'income', 'Freelance income'),
    ('Investment', 'income', 'Investment returns'),
    ('Other Income', 'income', 'Miscellaneous income'),
    ('Groceries', 'expense', 'Food and groceries'),
    ('Utilities', 'expense', 'Electricity, water, gas, internet'),
    ('Rent', 'expense', 'Rent or mortgage'),
    ('Transportation', 'expense', 'Gas, public transport, car maintenance'),
    ('Entertainment', 'expense', 'Movies, dining out, hobbies'),
    ('Healthcare', 'expense', 'Medical expenses and insurance'),
    ('Shopping', 'expense', 'Clothing and personal items'),
    ('Education', 'expense', 'Courses, books, tuition'),
    ('Insurance', 'expense', 'Various insurance premiums'),
    ('Other Expense', 'expense', 'Miscellaneous expenses');
