"""Data models for URL validation."""

from .result import ValidationResult
from .error import ValidationError, ErrorCategory
from .config import ValidationConfig

__all__ = ["ValidationResult", "ValidationError", "ErrorCategory", "ValidationConfig"]