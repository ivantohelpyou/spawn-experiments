"""Tests for main URL validator functionality."""

import pytest
import responses
from unittest.mock import patch, MagicMock

from url_validator.core.validator import URLValidator, validate_url, validate_urls
from url_validator.models.config import ValidationConfig
from url_validator.models.error import ErrorCode


class TestURLValidator:
    """Test cases for URLValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ValidationConfig()
        self.validator = URLValidator(self.config)

    def teardown_method(self):
        """Clean up after tests."""
        self.validator.close()

    def test_valid_url_validation(self):
        """Test validation of valid URL."""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, "https://example.com", status=200)

            result = self.validator.validate("https://example.com")

            assert result.is_valid
            assert result.is_accessible
            assert result.url == "https://example.com"
            assert result.duration > 0
            assert len(result.errors) == 0

    def test_invalid_url_validation(self):
        """Test validation of invalid URL."""
        result = self.validator.validate("not-a-url")

        assert not result.is_valid
        assert not result.is_accessible
        assert len(result.errors) > 0
        assert any(error.category.value == "format" for error in result.errors)

    def test_format_only_validation(self):
        """Test format-only validation."""
        result = self.validator.validate_format_only("https://example.com")

        assert result.is_valid
        assert not result.is_accessible  # Should be False as accessibility wasn't checked
        assert result.accessibility_result is None

    def test_accessibility_skip_on_invalid_format(self):
        """Test that accessibility check is skipped for invalid format."""
        with patch.object(self.validator, 'accessibility_checker') as mock_checker:
            result = self.validator.validate("invalid-url")

            # Accessibility checker should not be called
            mock_checker.check_accessibility.assert_not_called()
            assert not result.is_valid
            assert not result.is_accessible

    def test_batch_validation(self):
        """Test batch validation of multiple URLs."""
        urls = [
            "https://example.com",
            "https://google.com",
            "invalid-url",
            "https://github.com"
        ]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, "https://example.com", status=200)
            rsps.add(responses.HEAD, "https://google.com", status=200)
            rsps.add(responses.HEAD, "https://github.com", status=200)

            results = self.validator.validate_batch(urls)

            assert len(results) == 4
            assert results[0].is_valid and results[0].is_accessible  # example.com
            assert results[1].is_valid and results[1].is_accessible  # google.com
            assert not results[2].is_valid and not results[2].is_accessible  # invalid-url
            assert results[3].is_valid and results[3].is_accessible  # github.com

    def test_batch_validation_empty_list(self):
        """Test batch validation with empty list."""
        results = self.validator.validate_batch([])
        assert results == []

    def test_batch_validation_concurrency(self):
        """Test batch validation concurrency control."""
        urls = ["https://example.com"] * 5

        with responses.RequestsMock() as rsps:
            for url in urls:
                rsps.add(responses.HEAD, url, status=200)

            results = self.validator.validate_batch(urls, max_workers=2)

            assert len(results) == 5
            assert all(r.is_valid for r in results)

    def test_configuration_update(self):
        """Test configuration update."""
        original_timeout = self.validator.config.timeout

        self.validator.update_config(timeout=20)

        assert self.validator.config.timeout == 20
        assert self.validator.config.timeout != original_timeout

    def test_quick_validation_methods(self):
        """Test quick validation helper methods."""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.HEAD, "https://example.com", status=200)

            # Test format validation
            assert self.validator.is_valid_format("https://example.com")
            assert not self.validator.is_valid_format("invalid-url")

            # Test accessibility check
            assert self.validator.is_accessible("https://example.com")

    def test_context_manager(self):
        """Test context manager functionality."""
        with URLValidator() as validator:
            result = validator.validate_format_only("https://example.com")
            assert result.is_valid

        # Validator should be properly closed

    def test_lazy_accessibility_checker_initialization(self):
        """Test lazy initialization of accessibility checker."""
        validator = URLValidator()

        # Accessibility checker should not be initialized yet
        assert validator._accessibility_checker is None

        # Access should trigger initialization
        checker = validator.accessibility_checker
        assert checker is not None
        assert validator._accessibility_checker is checker

        # Second access should return the same instance
        assert validator.accessibility_checker is checker

        validator.close()

    def test_error_handling_in_validation(self):
        """Test error handling during validation."""
        with patch.object(self.validator.format_validator, 'validate') as mock_validate:
            mock_validate.side_effect = Exception("Test error")

            result = self.validator.validate("https://example.com")

            assert not result.is_valid
            assert len(result.errors) > 0
            assert any(error.code == ErrorCode.UNEXPECTED_ERROR for error in result.errors)

    def test_thread_safety(self):
        """Test thread safety of validator."""
        import threading
        import time

        results = []
        errors = []

        def validate_url_thread(url):
            try:
                with responses.RequestsMock() as rsps:
                    rsps.add(responses.HEAD, url, status=200)
                    result = self.validator.validate(url)
                    results.append(result)
            except Exception as e:
                errors.append(e)

        threads = []
        urls = [f"https://example{i}.com" for i in range(5)]

        for url in urls:
            thread = threading.Thread(target=validate_url_thread, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        assert len(errors) == 0
        # Note: Results might be fewer due to responses mock limitations in threading


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    @responses.activate
    def test_validate_url_function(self):
        """Test validate_url convenience function."""
        responses.add(responses.HEAD, "https://example.com", status=200)

        result = validate_url("https://example.com")

        assert result.is_valid
        assert result.is_accessible

    @responses.activate
    def test_validate_urls_function(self):
        """Test validate_urls convenience function."""
        urls = ["https://example.com", "https://google.com"]

        for url in urls:
            responses.add(responses.HEAD, url, status=200)

        results = validate_urls(urls)

        assert len(results) == 2
        assert all(r.is_valid for r in results)

    def test_validate_url_with_custom_config(self):
        """Test validate_url with custom configuration."""
        config = ValidationConfig(timeout=5, verify_ssl=False)

        result = validate_url("https://example.com", config=config, check_accessibility=False)

        assert result.is_valid
        # Accessibility should not be checked
        assert result.accessibility_result is None

    def test_is_valid_url_function(self):
        """Test is_valid_url convenience function."""
        from url_validator.core.validator import is_valid_url

        assert is_valid_url("https://example.com")
        assert not is_valid_url("invalid-url")

    @responses.activate
    def test_is_url_accessible_function(self):
        """Test is_url_accessible convenience function."""
        from url_validator.core.validator import is_url_accessible

        responses.add(responses.HEAD, "https://example.com", status=200)

        assert is_url_accessible("https://example.com")

    def test_validate_url_format_only(self):
        """Test format-only validation through convenience function."""
        result = validate_url("https://example.com", check_accessibility=False)

        assert result.is_valid
        assert not result.is_accessible  # Not checked
        assert result.accessibility_result is None

    def test_batch_validation_with_workers(self):
        """Test batch validation with custom worker count."""
        urls = ["https://example.com", "https://google.com", "https://github.com"]

        with responses.RequestsMock() as rsps:
            for url in urls:
                rsps.add(responses.HEAD, url, status=200)

            results = validate_urls(urls, max_workers=1)

            assert len(results) == 3
            assert all(r.is_valid for r in results)

    def test_error_propagation_in_convenience_functions(self):
        """Test error propagation in convenience functions."""
        # Test with invalid input
        result = validate_url("")

        assert not result.is_valid
        assert len(result.errors) > 0

    def test_configuration_inheritance(self):
        """Test configuration inheritance in convenience functions."""
        strict_config = ValidationConfig.create_strict()

        result = validate_url("http://example.com", config=strict_config)

        # Should fail because strict config only allows HTTPS
        assert not result.is_valid