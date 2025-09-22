"""
Format validation functionality with strategic component reuse.
Integrates utils/validation components for email, URL, and date validation.
"""

import sys
import os
from typing import Any

# Add utils path to enable component reuse - strategic component discovery
utils_path = '/home/ivan/projects/spawn-experiments/utils'
if os.path.exists(utils_path):
    sys.path.insert(0, utils_path)

try:
    # Strategic reuse of research-validated components
    from validation import validate_email as utils_validate_email
    from validation import validate_url as utils_validate_url
    from validation import validate_date as utils_validate_date
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False


class FormatValidator:
    """
    Format validator that strategically reuses utils/validation components.

    Leverages proven implementations from previous experiments:
    - Email validation from 1.501 (TDD Method 3)
    - URL validation from 1.502 (TDD Method 3)
    - Date validation from 1.504 (V4.1 Method 4)
    """

    def validate_format(self, value: Any, format_type: str) -> bool:
        """
        Validate value against specified format.

        Args:
            value: Value to validate
            format_type: Format type (email, uri, date, etc.)

        Returns:
            bool: True if valid or format validation not applicable
        """
        # Format validation only applies to strings per JSON Schema spec
        if not isinstance(value, str):
            return True

        # Empty strings are typically valid for format validation
        if not value:
            return False

        if format_type == "email":
            return self._validate_email(value)
        elif format_type == "uri":
            return self._validate_uri(value)
        elif format_type == "date":
            return self._validate_date(value)
        else:
            # Unknown formats should be ignored per JSON Schema spec
            return True

    def _validate_email(self, email: str) -> bool:
        """Validate email format using utils component."""
        if UTILS_AVAILABLE:
            return utils_validate_email(email)
        else:
            # Fallback basic email validation
            return "@" in email and "." in email.split("@")[-1]

    def _validate_uri(self, uri: str) -> bool:
        """Validate URI format using utils component."""
        if UTILS_AVAILABLE:
            return utils_validate_url(uri)
        else:
            # Fallback basic URI validation
            return uri.startswith(("http://", "https://"))

    def _validate_date(self, date_str: str) -> bool:
        """Validate date format using utils component."""
        if UTILS_AVAILABLE:
            return utils_validate_date(date_str)
        else:
            # Fallback basic date validation (MM/DD/YYYY)
            parts = date_str.split("/")
            if len(parts) != 3:
                return False
            try:
                month, day, year = [int(part) for part in parts]
                return (1 <= month <= 12 and
                       1 <= day <= 31 and
                       1900 <= year <= 2100)
            except ValueError:
                return False


# Global format validator instance
_format_validator = FormatValidator()


def validate_format(value: Any, format_type: str) -> bool:
    """
    Convenience function for format validation.

    Args:
        value: Value to validate
        format_type: Format type to validate against

    Returns:
        bool: True if valid format
    """
    return _format_validator.validate_format(value, format_type)