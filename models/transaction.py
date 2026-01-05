"""
Transaction Model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    """Transaction data model"""
    id: Optional[int] = None
    account_id: int = 0
    category_id: int = 0
    amount: float = 0.0
    transaction_type: str = "expense"  # 'income' or 'expense'
    description: str = ""
    transaction_date: str = ""
    created_at: Optional[datetime] = None
    account_name: str = ""  # Joined from accounts table
    category_name: str = ""  # Joined from categories table

    @classmethod
    def from_dict(cls, data: dict):
        """Create Transaction instance from dictionary"""
        return cls(
            id=data.get('id'),
            account_id=data.get('account_id', 0),
            category_id=data.get('category_id', 0),
            amount=data.get('amount', 0.0),
            transaction_type=data.get('transaction_type', 'expense'),
            description=data.get('description', ''),
            transaction_date=data.get('transaction_date', ''),
            created_at=data.get('created_at'),
            account_name=data.get('account_name', ''),
            category_name=data.get('category_name', '')
        )

    def to_dict(self) -> dict:
        """Convert Transaction instance to dictionary"""
        return {
            'id': self.id,
            'account_id': self.account_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'transaction_date': self.transaction_date,
            'created_at': self.created_at,
            'account_name': self.account_name,
            'category_name': self.category_name
        }

    def __str__(self) -> str:
        return f"{self.transaction_date}: {self.category_name} - ${self.amount:.2f}"
