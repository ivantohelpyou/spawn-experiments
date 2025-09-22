"""
URL Validator - A comprehensive URL validation library.

This library provides robust URL validation capabilities including:
- Format validation using urllib.parse
- Accessibility checking using requests
- Batch processing with concurrency
- Security features and SSRF protection
- Comprehensive error handling
"""

from .core.validator import URLValidator, validate_url, validate_urls
from .models.result import ValidationResult
from .models.error import ValidationError, ErrorCategory
from .models.config import ValidationConfig

__version__ = "1.0.0"
__author__ = "URL Validator Project"
__email__ = "contact@urlvalidator.com"

__all__ = [
    "URLValidator",
    "validate_url",
    "validate_urls",
    "ValidationResult",
    "ValidationError",
    "ErrorCategory",
    "ValidationConfig",
]