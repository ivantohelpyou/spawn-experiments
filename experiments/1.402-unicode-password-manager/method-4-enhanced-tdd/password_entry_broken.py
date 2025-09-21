"""
VALIDATION PHASE: Intentionally broken implementation
This demonstrates that our tests actually catch bugs
"""

from datetime import datetime

class PasswordEntry:
    """BROKEN implementation to validate our tests"""

    def __init__(self, service, username, password):
        # BUG 1: Swapped field assignments
        self.service = username  # WRONG!
        self.username = service  # WRONG!
        self.password = password

        # BUG 2: No timestamp
        # Missing: self.created_date = datetime.now()

    @property
    def normalized_service(self):
        """BROKEN: No normalization at all"""
        # BUG 3: Returns input unchanged (no Unicode normalization)
        return self.service

    def validate(self):
        """BROKEN: No validation"""
        # BUG 4: Always returns True regardless of input
        return True