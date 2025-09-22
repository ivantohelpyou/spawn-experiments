"""
Tests for format validation functionality.
Tests the strategic integration of utils/validation components.
"""

import pytest
from jsv.formats import FormatValidator


class TestFormatValidator:
    """Test cases for format validation with component reuse."""

    def test_email_format_validation(self):
        """Test email format validation using utils/validation component."""
        validator = FormatValidator()

        # Valid emails
        assert validator.validate_format("user@domain.com", "email") == True
        assert validator.validate_format("test+tag@example.org", "email") == True
        assert validator.validate_format("user.name@domain-name.co.uk", "email") == True

        # Invalid emails
        assert validator.validate_format("invalid.email", "email") == False
        assert validator.validate_format("@domain.com", "email") == False
        assert validator.validate_format("user@", "email") == False
        assert validator.validate_format("", "email") == False

    def test_uri_format_validation(self):
        """Test URI format validation using utils/validation component."""
        validator = FormatValidator()

        # Valid URIs
        assert validator.validate_format("http://example.com", "uri") == True
        assert validator.validate_format("https://www.example.com/path", "uri") == True
        assert validator.validate_format("https://example.com:8080/path?query=value", "uri") == True

        # Invalid URIs
        assert validator.validate_format("not-a-url", "uri") == False
        assert validator.validate_format("ftp://example.com", "uri") == False  # Only http/https allowed
        assert validator.validate_format("", "uri") == False

    def test_date_format_validation(self):
        """Test date format validation using utils/validation component."""
        validator = FormatValidator()

        # Valid dates
        assert validator.validate_format("12/25/2023", "date") == True
        assert validator.validate_format("01/01/2000", "date") == True
        assert validator.validate_format("02/29/2020", "date") == True  # Leap year

        # Invalid dates
        assert validator.validate_format("13/01/2023", "date") == False  # Invalid month
        assert validator.validate_format("12/32/2023", "date") == False  # Invalid day
        assert validator.validate_format("02/29/2021", "date") == False  # Not a leap year
        assert validator.validate_format("not-a-date", "date") == False
        assert validator.validate_format("", "date") == False

    def test_unknown_format(self):
        """Test handling of unknown format types."""
        validator = FormatValidator()

        # Unknown format should return True (JSON Schema spec behavior)
        assert validator.validate_format("anything", "unknown-format") == True

    def test_format_validation_with_non_string(self):
        """Test format validation with non-string values."""
        validator = FormatValidator()

        # Format validation only applies to strings
        assert validator.validate_format(123, "email") == True
        assert validator.validate_format(None, "uri") == True
        assert validator.validate_format([], "date") == True

    def test_format_integration_with_schema_validator(self):
        """Test format validation integrated with main schema validator."""
        from jsv.validator import JSONSchemaValidator

        # Schema with format constraints
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "website": {"type": "string", "format": "uri"},
                "birthdate": {"type": "string", "format": "date"}
            }
        }

        validator = JSONSchemaValidator(schema)

        # Valid data
        valid_data = {
            "email": "user@example.com",
            "website": "https://example.com",
            "birthdate": "12/25/1990"
        }
        assert validator.validate(valid_data) == True

        # Invalid email format
        invalid_email_data = {
            "email": "invalid-email",
            "website": "https://example.com",
            "birthdate": "12/25/1990"
        }
        assert validator.validate(invalid_email_data) == False

        # Invalid URI format
        invalid_uri_data = {
            "email": "user@example.com",
            "website": "not-a-url",
            "birthdate": "12/25/1990"
        }
        assert validator.validate(invalid_uri_data) == False