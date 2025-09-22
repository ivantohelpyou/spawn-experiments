"""
Format validators using research-validated components from utils.
Integrates email, date, and URL validators discovered in component exploration.
"""

import sys
import os

# Add the project root to path to import utils
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
sys.path.insert(0, project_root)

from utils.validation import validate_email, validate_date
from utils.validation.url_validator import URLValidator


class FormatValidatorRegistry:
    """Registry for format validators using utils components."""

    def __init__(self):
        self.url_validator = URLValidator()
        self._validators = {
            'email': self._validate_email,
            'date': self._validate_date,
            'uri': self._validate_uri,
            'url': self._validate_uri  # Alias for uri
        }

    def validate_format(self, value: str, format_name: str) -> tuple[bool, str]:
        """
        Validate a value against a specific format.

        Args:
            value: The string value to validate
            format_name: The format type (email, date, uri, etc.)

        Returns:
            Tuple of (is_valid, error_message)
        """
        if format_name not in self._validators:
            return True, ""  # Unknown formats are considered valid

        try:
            return self._validators[format_name](value)
        except Exception as e:
            return False, f"Format validation error: {str(e)}"

    def _validate_email(self, value: str) -> tuple[bool, str]:
        """Validate email using utils.validation.email_validator."""
        # Note: Using is_valid_email from the utils component
        from utils.validation.email_validator import is_valid_email

        is_valid = is_valid_email(value)
        return is_valid, "" if is_valid else "Invalid email format"

    def _validate_date(self, value: str) -> tuple[bool, str]:
        """Validate date using utils.validation.date_validator."""
        is_valid = validate_date(value, format_type='auto')
        return is_valid, "" if is_valid else "Invalid date format (expected MM/DD/YYYY or DD/MM/YYYY)"

    def _validate_uri(self, value: str) -> tuple[bool, str]:
        """Validate URI using utils.validation.url_validator."""
        is_valid = self.url_validator.is_valid(value)
        return is_valid, "" if is_valid else "Invalid URI format"

    def get_supported_formats(self) -> list[str]:
        """Get list of supported format types."""
        return list(self._validators.keys())


# Global instance for use throughout the application
format_registry = FormatValidatorRegistry()