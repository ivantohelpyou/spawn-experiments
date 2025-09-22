"""
File Path Validator - A comprehensive path validation library for Python.

This library provides robust file and directory path validation with support for:
- Cross-platform compatibility (Windows, POSIX)
- Security validation and path traversal prevention
- Comprehensive error handling with detailed diagnostics
- High-performance validation suitable for production use
- Integration with both os.path and pathlib libraries
"""

from .validators.sync import PathValidator, validate_path, is_valid_path
from .validators.batch import BatchPathValidator
from .core.validator import ValidationResult, ValidationConfig
from .exceptions.errors import (
    PathValidationError,
    PathSyntaxError,
    PathSecurityError,
    PathTraversalError,
    PathPlatformError,
    PathExistenceError,
    PathPermissionError,
    PathLengthError,
    PathUnicodeError,
)
from .platform.detection import get_current_platform, detect_platform_features
from .utils.config import SecurityPolicy, SymlinkPolicy

__version__ = "1.0.0"
__author__ = "Path Validator Development Team"
__license__ = "MIT"

# Public API exports
__all__ = [
    # Main validator classes
    "PathValidator",
    "BatchPathValidator",

    # Convenience functions
    "validate_path",
    "is_valid_path",

    # Configuration classes
    "ValidationConfig",
    "SecurityPolicy",
    "SymlinkPolicy",

    # Result classes
    "ValidationResult",

    # Exception hierarchy
    "PathValidationError",
    "PathSyntaxError",
    "PathSecurityError",
    "PathTraversalError",
    "PathPlatformError",
    "PathExistenceError",
    "PathPermissionError",
    "PathLengthError",
    "PathUnicodeError",

    # Platform utilities
    "get_current_platform",
    "detect_platform_features",
]

# Version information
VERSION_INFO = (1, 0, 0)