"""
Account Model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Account:
    """Account data model"""
    id: Optional[int] = None
    name: str = ""
    account_type: str = "debit"  # 'debit' or 'credit'
    initial_balance: float = 0.0
    current_balance: float = 0.0
    currency: str = "USD"
    created_date: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict):
        """Create Account instance from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            account_type=data.get('account_type', 'debit'),
            initial_balance=data.get('initial_balance', 0.0),
            current_balance=data.get('current_balance', 0.0),
            currency=data.get('currency', 'USD'),
            created_date=data.get('created_date')
        )

    def to_dict(self) -> dict:
        """Convert Account instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'account_type': self.account_type,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'currency': self.currency,
            'created_date': self.created_date
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.account_type}): {self.currency} {self.current_balance:.2f}"
