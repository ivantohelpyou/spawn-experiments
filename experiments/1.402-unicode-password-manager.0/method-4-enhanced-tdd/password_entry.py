"""
GREEN PHASE: Correct implementation after test validation
This implementation passes all validated tests
"""

from datetime import datetime
import unicodedata

class PasswordEntry:
    """
    Password entry with validated Unicode support
    Implemented after thorough test validation
    """

    def __init__(self, service, username, password):
        """Initialize password entry with proper field assignment"""
        # Correct field assignment (tests validated this)
        self.service = service
        self.username = username
        self.password = password

        # Timestamp creation (tests validated this is required)
        self.created_date = datetime.now()

    @property
    def normalized_service(self):
        """
        Unicode normalization using NFC form
        Implementation validated by testing broken version first
        """
        # Proper Unicode normalization (tests validated this works)
        return unicodedata.normalize('NFC', self.service)

    @property
    def normalized_username(self):
        """Unicode normalization for username"""
        return unicodedata.normalize('NFC', self.username)

    @property
    def normalized_password(self):
        """Unicode normalization for password"""
        return unicodedata.normalize('NFC', self.password)

    def validate(self):
        """
        Input validation with proper error handling
        Validation logic thoroughly tested with edge cases
        """
        # Service name validation (1-100 characters)
        if not (1 <= len(self.service) <= 100):
            raise ValueError("Service name must be 1-100 characters")

        # Username validation (1-200 characters)
        if not (1 <= len(self.username) <= 200):
            raise ValueError("Username must be 1-200 characters")

        # Password validation (1-500 characters)
        if not (1 <= len(self.password) <= 500):
            raise ValueError("Password must be 1-500 characters")

        return True

    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'service': self.service,
            'username': self.username,
            'password': self.password,
            'created_date': self.created_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        entry = cls(
            service=data['service'],
            username=data['username'],
            password=data['password']
        )
        # Restore original timestamp if provided
        if 'created_date' in data:
            entry.created_date = datetime.fromisoformat(data['created_date'])
        return entry

    def __repr__(self):
        """String representation for debugging"""
        return f"PasswordEntry(service='{self.service}', username='{self.username}')"

    def __eq__(self, other):
        """Equality comparison using normalized values"""
        if not isinstance(other, PasswordEntry):
            return False

        return (
            self.normalized_service == other.normalized_service and
            self.normalized_username == other.normalized_username and
            self.normalized_password == other.normalized_password
        )