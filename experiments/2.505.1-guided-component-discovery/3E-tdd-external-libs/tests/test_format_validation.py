"""Test suite for format validation (email, date, uri) following TDD methodology."""

import pytest
from unittest.mock import patch, MagicMock

# Import format validation modules - will fail initially (Red phase)
try:
    from json_schema_validator import (
        FormatValidator,
        EmailValidator,
        DateValidator,
        URIValidator,
        validate_email_format,
        validate_date_format,
        validate_uri_format
    )
except ImportError:
    # Expected during TDD - tests written first
    FormatValidator = None
    EmailValidator = None
    DateValidator = None
    URIValidator = None
    validate_email_format = None
    validate_date_format = None
    validate_uri_format = None


class TestEmailFormatValidation:
    """Test email format validation."""

    def test_valid_emails(self):
        """Test validation of valid email addresses."""
        if validate_email_format is None:
            pytest.skip("validate_email_format not implemented yet - TDD Red phase")

        valid_emails = [
            "user@example.com",
            "test.email@domain.org",
            "firstname.lastname@company.co.uk",
            "user+tag@domain.net",
            "123@numeric-domain.com",
            "user_name@domain-name.io"
        ]

        for email in valid_emails:
            result = validate_email_format(email)
            assert result.is_valid is True, f"Email {email} should be valid"
            assert result.errors == []

    def test_invalid_emails(self):
        """Test validation of invalid email addresses."""
        if validate_email_format is None:
            pytest.skip("validate_email_format not implemented yet - TDD Red phase")

        invalid_emails = [
            "not-an-email",
            "@domain.com",
            "user@",
            "user@domain",
            "user.domain.com",
            "",
            "user@domain..com",
            "user..name@domain.com"
        ]

        for email in invalid_emails:
            result = validate_email_format(email)
            assert result.is_valid is False, f"Email {email} should be invalid"
            assert len(result.errors) > 0

    def test_email_validator_class(self):
        """Test EmailValidator class functionality."""
        if EmailValidator is None:
            pytest.skip("EmailValidator not implemented yet - TDD Red phase")

        validator = EmailValidator()

        # Test valid email
        result = validator.validate("user@example.com")
        assert result.is_valid is True

        # Test invalid email
        result = validator.validate("invalid-email")
        assert result.is_valid is False

    def test_email_integration_with_utils(self):
        """Test potential integration with utils validation components."""
        if validate_email_format is None:
            pytest.skip("validate_email_format not implemented yet - TDD Red phase")

        # Test that we can use the utility components if discovered
        # This tests the component discovery aspect of the experiment
        test_email = "test@example.com"
        result = validate_email_format(test_email)

        # Should work regardless of whether utils are used or external libs
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')


class TestDateFormatValidation:
    """Test date format validation."""

    def test_valid_dates(self):
        """Test validation of valid date formats."""
        if validate_date_format is None:
            pytest.skip("validate_date_format not implemented yet - TDD Red phase")

        valid_dates = [
            "2023-12-25",  # ISO format
            "2023-01-01",
            "2023-02-29",  # Leap year (if 2024)
            "1990-05-15",
            "2025-09-22"
        ]

        for date_str in valid_dates:
            result = validate_date_format(date_str)
            assert result.is_valid is True, f"Date {date_str} should be valid"
            assert result.errors == []

    def test_invalid_dates(self):
        """Test validation of invalid date formats."""
        if validate_date_format is None:
            pytest.skip("validate_date_format not implemented yet - TDD Red phase")

        invalid_dates = [
            "not-a-date",
            "2023-13-01",  # Invalid month
            "2023-02-30",  # Invalid day for February
            "2023/12/25",  # Wrong format
            "25-12-2023",  # Wrong format
            "",
            "2023-2-5",    # Missing leading zeros
            "2023-12-32"   # Invalid day
        ]

        for date_str in invalid_dates:
            result = validate_date_format(date_str)
            assert result.is_valid is False, f"Date {date_str} should be invalid"
            assert len(result.errors) > 0

    def test_date_validator_class(self):
        """Test DateValidator class functionality."""
        if DateValidator is None:
            pytest.skip("DateValidator not implemented yet - TDD Red phase")

        validator = DateValidator()

        # Test valid date
        result = validator.validate("2023-12-25")
        assert result.is_valid is True

        # Test invalid date
        result = validator.validate("invalid-date")
        assert result.is_valid is False

    def test_date_integration_with_utils(self):
        """Test potential integration with utils validation components."""
        if validate_date_format is None:
            pytest.skip("validate_date_format not implemented yet - TDD Red phase")

        # Test that we can use the utility components if discovered
        test_date = "2023-12-25"
        result = validate_date_format(test_date)

        # Should work regardless of whether utils are used or external libs
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')


class TestURIFormatValidation:
    """Test URI format validation."""

    def test_valid_uris(self):
        """Test validation of valid URI formats."""
        if validate_uri_format is None:
            pytest.skip("validate_uri_format not implemented yet - TDD Red phase")

        valid_uris = [
            "https://example.com",
            "http://subdomain.example.org",
            "https://example.com/path/to/resource",
            "https://example.com:8080",
            "https://example.com/path?query=value",
            "https://example.com/path#fragment",
            "ftp://files.example.com",
            "mailto:user@example.com",
            "file:///path/to/local/file"
        ]

        for uri in valid_uris:
            result = validate_uri_format(uri)
            assert result.is_valid is True, f"URI {uri} should be valid"
            assert result.errors == []

    def test_invalid_uris(self):
        """Test validation of invalid URI formats."""
        if validate_uri_format is None:
            pytest.skip("validate_uri_format not implemented yet - TDD Red phase")

        invalid_uris = [
            "not-a-uri",
            "://missing-scheme",
            "http://",
            "https://",
            "",
            "just-text",
            "http:// invalid spaces",
            "https://[invalid-host"
        ]

        for uri in invalid_uris:
            result = validate_uri_format(uri)
            assert result.is_valid is False, f"URI {uri} should be invalid"
            assert len(result.errors) > 0

    def test_uri_validator_class(self):
        """Test URIValidator class functionality."""
        if URIValidator is None:
            pytest.skip("URIValidator not implemented yet - TDD Red phase")

        validator = URIValidator()

        # Test valid URI
        result = validator.validate("https://example.com")
        assert result.is_valid is True

        # Test invalid URI
        result = validator.validate("invalid-uri")
        assert result.is_valid is False

    def test_uri_integration_with_utils(self):
        """Test potential integration with utils validation components."""
        if validate_uri_format is None:
            pytest.skip("validate_uri_format not implemented yet - TDD Red phase")

        # Test that we can use the utility components if discovered
        test_uri = "https://example.com"
        result = validate_uri_format(test_uri)

        # Should work regardless of whether utils are used or external libs
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')


class TestFormatValidatorIntegration:
    """Test integration of format validators with JSON schema validation."""

    def test_format_validator_factory(self):
        """Test FormatValidator factory creates appropriate validators."""
        if FormatValidator is None:
            pytest.skip("FormatValidator not implemented yet - TDD Red phase")

        # Test email validator creation
        email_validator = FormatValidator.create("email")
        assert email_validator is not None

        # Test date validator creation
        date_validator = FormatValidator.create("date")
        assert date_validator is not None

        # Test URI validator creation
        uri_validator = FormatValidator.create("uri")
        assert uri_validator is not None

        # Test unknown format
        with pytest.raises(ValueError):
            FormatValidator.create("unknown_format")

    def test_format_validation_in_schema_context(self):
        """Test format validation within JSON schema validation context."""
        if validate_email_format is None or validate_date_format is None or validate_uri_format is None:
            pytest.skip("Format validators not implemented yet - TDD Red phase")

        # This would typically be called by the main validator
        # when it encounters format specifications in schemas

        # Test email in schema context
        email_result = validate_email_format("user@example.com")
        assert email_result.is_valid is True

        # Test date in schema context
        date_result = validate_date_format("2023-12-25")
        assert date_result.is_valid is True

        # Test URI in schema context
        uri_result = validate_uri_format("https://example.com")
        assert uri_result.is_valid is True

    def test_custom_format_validators(self):
        """Test ability to add custom format validators."""
        if FormatValidator is None:
            pytest.skip("FormatValidator not implemented yet - TDD Red phase")

        # Test that we can register custom format validators
        def phone_validator(value):
            # Simple phone validation for testing
            import re
            pattern = r'^\+?[\d\s\-\(\)]{10,}$'
            return re.match(pattern, value) is not None

        try:
            FormatValidator.register("phone", phone_validator)

            validator = FormatValidator.create("phone")
            result = validator.validate("+1-555-123-4567")
            assert result.is_valid is True

            result = validator.validate("invalid-phone")
            assert result.is_valid is False

        except (NotImplementedError, AttributeError):
            # Expected if custom format registration not implemented
            pytest.skip("Custom format registration not implemented")


class TestFormatValidationErrors:
    """Test detailed error reporting for format validation."""

    def test_email_error_details(self):
        """Test detailed error messages for email validation."""
        if validate_email_format is None:
            pytest.skip("validate_email_format not implemented yet - TDD Red phase")

        result = validate_email_format("invalid-email")
        assert result.is_valid is False
        assert len(result.errors) > 0

        # Error message should be descriptive
        error_text = " ".join(result.errors).lower()
        assert "email" in error_text or "format" in error_text

    def test_date_error_details(self):
        """Test detailed error messages for date validation."""
        if validate_date_format is None:
            pytest.skip("validate_date_format not implemented yet - TDD Red phase")

        result = validate_date_format("2023-13-01")  # Invalid month
        assert result.is_valid is False
        assert len(result.errors) > 0

        # Error message should be descriptive
        error_text = " ".join(result.errors).lower()
        assert "date" in error_text or "format" in error_text or "month" in error_text

    def test_uri_error_details(self):
        """Test detailed error messages for URI validation."""
        if validate_uri_format is None:
            pytest.skip("validate_uri_format not implemented yet - TDD Red phase")

        result = validate_uri_format("not-a-uri")
        assert result.is_valid is False
        assert len(result.errors) > 0

        # Error message should be descriptive
        error_text = " ".join(result.errors).lower()
        assert "uri" in error_text or "url" in error_text or "format" in error_text


class TestComponentDiscovery:
    """Test component discovery patterns for format validation."""

    def test_utils_component_discovery(self):
        """Test that utils components are discovered and used when available."""
        # This test verifies the component discovery aspect of the experiment

        # Check if utils directory components might be available
        import sys
        import os

        # Add utils to path for potential discovery
        utils_path = "/home/ivan/projects/spawn-experiments/utils"
        if os.path.exists(utils_path) and utils_path not in sys.path:
            sys.path.insert(0, utils_path)

        try:
            # Try to import validation utils
            from validation import validate_email, validate_date, validate_url

            # If available, test that they work
            email_result = validate_email("test@example.com")
            assert email_result is not None

            date_result = validate_date("2023-12-25")
            assert date_result is not None

            url_result = validate_url("https://example.com")
            assert url_result is not None

        except ImportError:
            # Utils not discovered - will use external libraries instead
            pytest.skip("Utils components not discovered - using external libraries")

    def test_external_library_fallback(self):
        """Test fallback to external libraries when utils not discovered."""
        # This test ensures external libraries work as fallback

        try:
            import pydantic
            from pydantic import EmailStr, AnyUrl
            from datetime import datetime

            # Test external library functionality
            # These would be used if utils components not discovered

            # Email validation with pydantic
            try:
                from pydantic import BaseModel
                class TestModel(BaseModel):
                    email: EmailStr
                TestModel(email="test@example.com")
                email_works = True
            except:
                email_works = False
            assert email_works

            # URL validation with pydantic
            try:
                from pydantic import BaseModel
                class TestModel(BaseModel):
                    url: AnyUrl
                TestModel(url="https://example.com")
                url_works = True
            except:
                url_works = False
            assert url_works

            # Date validation with datetime
            try:
                datetime.strptime("2023-12-25", "%Y-%m-%d")
                date_works = True
            except:
                date_works = False
            assert date_works

        except ImportError:
            pytest.skip("External libraries not available for testing")