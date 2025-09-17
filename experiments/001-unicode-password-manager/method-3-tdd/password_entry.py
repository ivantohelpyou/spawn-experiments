"""
Password entry implementation - evolved through TDD cycles
"""

from datetime import datetime
import unicodedata

class PasswordEntry:
    """Password entry with Unicode normalization (TDD Cycle 2)"""

    def __init__(self, service, username, password):
        self.service = service
        self.username = username
        self.password = password
        self.created_date = datetime.now()

    @property
    def normalized_service(self):
        """Unicode normalization for consistent comparison (TDD Cycle 2)"""
        return unicodedata.normalize('NFC', self.service)

    @property
    def normalized_username(self):
        """Unicode normalization for username"""
        return unicodedata.normalize('NFC', self.username)

    @property
    def normalized_password(self):
        """Unicode normalization for password"""
        return unicodedata.normalize('NFC', self.password)