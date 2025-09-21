"""
Password Entry data model following specifications
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import unicodedata

@dataclass
class PasswordEntry:
    """
    Represents a single password entry with Unicode support
    Follows SPEC-3.2.1
    """
    service_name: str
    username: str
    password: str
    created_date: datetime
    modified_date: datetime
    category: Optional[str] = None

    def __post_init__(self):
        """Normalize Unicode strings according to SPEC-3.3.1"""
        self.service_name = self._normalize_unicode(self.service_name)
        self.username = self._normalize_unicode(self.username)
        self.password = self._normalize_unicode(self.password)
        if self.category:
            self.category = self._normalize_unicode(self.category)

    @staticmethod
    def _normalize_unicode(text: str) -> str:
        """
        Normalize text to NFC form for consistent storage
        Implements SPEC-3.3.1
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        # Normalize to NFC (Canonical Composition)
        normalized = unicodedata.normalize('NFC', text)

        # Remove any null bytes (RULE-5.1.4)
        normalized = normalized.replace('\x00', '')

        return normalized

    def validate(self) -> bool:
        """
        Validate entry according to business rules
        Implements RULE-5.1.1, RULE-5.1.2, RULE-5.1.3
        """
        # Check service name length (RULE-5.1.1)
        if not (1 <= len(self.service_name) <= 100):
            raise ValueError("Service name must be 1-100 characters")

        # Check username length (RULE-5.1.2)
        if not (1 <= len(self.username) <= 200):
            raise ValueError("Username must be 1-200 characters")

        # Check password length (RULE-5.1.3)
        if not (1 <= len(self.password) <= 500):
            raise ValueError("Password must be 1-500 characters")

        return True

    def to_dict(self) -> dict:
        """Convert entry to dictionary for serialization"""
        return {
            'service_name': self.service_name,
            'username': self.username,
            'password': self.password,
            'created_date': self.created_date.isoformat(),
            'modified_date': self.modified_date.isoformat(),
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PasswordEntry':
        """Create entry from dictionary"""
        return cls(
            service_name=data['service_name'],
            username=data['username'],
            password=data['password'],
            created_date=datetime.fromisoformat(data['created_date']),
            modified_date=datetime.fromisoformat(data['modified_date']),
            category=data.get('category')
        )

    def get_visual_length(self, text: str) -> int:
        """
        Get visual character count using grapheme clusters
        Implements SPEC-3.3.2
        """
        # This is a simplified grapheme counter
        # In production, would use a proper library like grapheme
        import re

        # Remove combining characters for basic counting
        without_combining = ''.join(c for c in text
                                  if unicodedata.category(c) != 'Mn')

        # Handle emoji sequences (basic implementation)
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000026FF\U00002700-\U000027BF]+')

        # This is still simplified - proper grapheme counting requires more work
        return len(without_combining)