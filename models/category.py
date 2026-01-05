"""
Category Model
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    """Category data model"""
    id: Optional[int] = None
    name: str = ""
    type: str = "expense"  # 'income' or 'expense'
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict):
        """Create Category instance from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            type=data.get('type', 'expense'),
            description=data.get('description', '')
        )

    def to_dict(self) -> dict:
        """Convert Category instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"
