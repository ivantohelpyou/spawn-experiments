"""Main URL validator class integrating all validation components."""

import time
from typing import List, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from ..models.config import ValidationConfig
from ..models.result import ValidationResult
from ..models.error import ValidationError, ErrorCode, URLValidationException
from .format_validator import FormatValidator
from .accessibility_checker import AccessibilityChecker


class URLValidator:
    """
    Main URL validator class that coordinates format and accessibility validation.

    This class provides a high-level interface for URL validation, integrating
    format checking and accessibility testing with configurable options.
    """

    def __init__(self, config: Optional[ValidationConfig] = None):
        """
        Initialize URL validator with configuration.

        Args:
            config: Validation configuration. If None, default config is used.
        """
        self.config = config or ValidationConfig()
        self.logger = self.config.get_logger(__name__)

        # Initialize validators
        self.format_validator = FormatValidator(self.config)
        self._accessibility_checker = None
        self._lock = threading.Lock()

    @property
    def accessibility_checker(self) -> AccessibilityChecker:
        """
        Get accessibility checker instance (lazy initialization).

        Returns:
            AccessibilityChecker instance
        """
        if self._accessibility_checker is None:
            with self._lock:
                if self._accessibility_checker is None:
                    self._accessibility_checker = AccessibilityChecker(self.config)
        return self._accessibility_checker

    def validate(self, url: str, check_accessibility: bool = True) -> ValidationResult:
        """
        Validate a single URL.

        Args:
            url: URL string to validate
            check_accessibility: Whether to check URL accessibility

        Returns:
            ValidationResult with validation details

        Raises:
            URLValidationException: For critical validation errors
        """
        start_time = time.time()

        try:
            self.logger.debug(f"Starting validation for URL: {url}")

            # Step 1: Format validation
            result = self.format_validator.validate(url)

            # Step 2: Accessibility validation (only if format is valid)
            if result.is_valid and check_accessibility:
                self.accessibility_checker.check_accessibility(url, result)
            elif not result.is_valid:
                self.logger.debug(f"Skipping accessibility check due to format errors: {url}")
                result.is_accessible = False

            # Update timing
            result.duration = time.time() - start_time

            self.logger.debug(
                f"Validation completed for {url}: "
                f"valid={result.is_valid}, accessible={result.is_accessible}, "
                f"duration={result.duration:.3f}s"
            )

            return result

        except Exception as e:
            self.logger.error(f"Critical error during validation of {url}: {e}")

            # Create error result
            error_result = ValidationResult(url=url, is_valid=False, is_accessible=False)
            error_result.add_error(ValidationError.system_error(
                ErrorCode.UNEXPECTED_ERROR,
                f"Critical validation error: {e}",
                {"error": str(e), "type": type(e).__name__}
            ))
            error_result.duration = time.time() - start_time

            return error_result

    def validate_batch(self, urls: List[str],
                      check_accessibility: bool = True,
                      max_workers: Optional[int] = None) -> List[ValidationResult]:
        """
        Validate multiple URLs concurrently.

        Args:
            urls: List of URL strings to validate
            check_accessibility: Whether to check URL accessibility
            max_workers: Maximum number of worker threads

        Returns:
            List of ValidationResult objects in same order as input URLs
        """
        if not urls:
            return []

        if max_workers is None:
            max_workers = min(10, len(urls))

        self.logger.info(f"Starting batch validation of {len(urls)} URLs with {max_workers} workers")

        results = [None] * len(urls)  # Pre-allocate results list

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all validation tasks
            future_to_index = {
                executor.submit(self.validate, url, check_accessibility): index
                for index, url in enumerate(urls)
            }

            # Collect results as they complete
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                except Exception as e:
                    # Create error result for failed validation
                    url = urls[index]
                    error_result = ValidationResult(url=url, is_valid=False, is_accessible=False)
                    error_result.add_error(ValidationError.system_error(
                        ErrorCode.UNEXPECTED_ERROR,
                        f"Batch validation error: {e}",
                        {"error": str(e), "type": type(e).__name__}
                    ))
                    results[index] = error_result
                    self.logger.error(f"Error validating {url} in batch: {e}")

        self.logger.info(f"Completed batch validation of {len(urls)} URLs")
        return results

    def validate_format_only(self, url: str) -> ValidationResult:
        """
        Validate only URL format (skip accessibility check).

        Args:
            url: URL string to validate

        Returns:
            ValidationResult with format validation only
        """
        return self.validate(url, check_accessibility=False)

    def is_valid_format(self, url: str) -> bool:
        """
        Quick check if URL has valid format.

        Args:
            url: URL string to check

        Returns:
            True if URL format is valid
        """
        try:
            result = self.validate_format_only(url)
            return result.is_valid
        except Exception:
            return False

    def is_accessible(self, url: str) -> bool:
        """
        Quick check if URL is accessible.

        Args:
            url: URL string to check

        Returns:
            True if URL is accessible
        """
        try:
            return self.accessibility_checker.quick_check(url)
        except Exception:
            return False

    def update_config(self, **kwargs) -> None:
        """
        Update configuration parameters.

        Args:
            **kwargs: Configuration parameters to update
        """
        self.config = self.config.update(**kwargs)

        # Recreate validators with new config
        self.format_validator = FormatValidator(self.config)
        with self._lock:
            if self._accessibility_checker is not None:
                self._accessibility_checker.close()
                self._accessibility_checker = None

    def get_config(self) -> ValidationConfig:
        """
        Get current configuration.

        Returns:
            Current ValidationConfig
        """
        return self.config

    def close(self) -> None:
        """Close validator and clean up resources."""
        with self._lock:
            if self._accessibility_checker is not None:
                self._accessibility_checker.close()
                self._accessibility_checker = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience functions for simple usage

def validate_url(url: str, config: Optional[ValidationConfig] = None,
                check_accessibility: bool = True) -> ValidationResult:
    """
    Validate a single URL with default or provided configuration.

    Args:
        url: URL string to validate
        config: Optional validation configuration
        check_accessibility: Whether to check URL accessibility

    Returns:
        ValidationResult with validation details

    Example:
        >>> result = validate_url("https://example.com")
        >>> print(result.is_valid, result.is_accessible)
        True True

        >>> result = validate_url("invalid-url")
        >>> print(result.is_valid)
        False
    """
    with URLValidator(config) as validator:
        return validator.validate(url, check_accessibility)


def validate_urls(urls: List[str], config: Optional[ValidationConfig] = None,
                 check_accessibility: bool = True,
                 max_workers: Optional[int] = None) -> List[ValidationResult]:
    """
    Validate multiple URLs concurrently with default or provided configuration.

    Args:
        urls: List of URL strings to validate
        config: Optional validation configuration
        check_accessibility: Whether to check URL accessibility
        max_workers: Maximum number of worker threads

    Returns:
        List of ValidationResult objects

    Example:
        >>> urls = ["https://example.com", "https://google.com", "invalid-url"]
        >>> results = validate_urls(urls)
        >>> for result in results:
        ...     print(f"{result.url}: {result.is_valid}")
        https://example.com: True
        https://google.com: True
        invalid-url: False
    """
    with URLValidator(config) as validator:
        return validator.validate_batch(urls, check_accessibility, max_workers)


def is_valid_url(url: str, config: Optional[ValidationConfig] = None) -> bool:
    """
    Quick check if URL is valid (format only).

    Args:
        url: URL string to check
        config: Optional validation configuration

    Returns:
        True if URL is valid

    Example:
        >>> is_valid_url("https://example.com")
        True
        >>> is_valid_url("invalid-url")
        False
    """
    with URLValidator(config) as validator:
        return validator.is_valid_format(url)


def is_url_accessible(url: str, config: Optional[ValidationConfig] = None) -> bool:
    """
    Quick check if URL is accessible.

    Args:
        url: URL string to check
        config: Optional validation configuration

    Returns:
        True if URL is accessible

    Example:
        >>> is_url_accessible("https://google.com")
        True
        >>> is_url_accessible("https://thisdomaindoesnotexist123.com")
        False
    """
    with URLValidator(config) as validator:
        return validator.is_accessible(url)