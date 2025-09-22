"""
Exception hierarchy for path validation errors.
"""

from datetime import datetime
from typing import Optional, List


class ErrorCodes:
    """Standardized error codes for path validation failures."""

    # Syntax errors (1000-1999)
    INVALID_SYNTAX = "E1001"
    EMPTY_PATH = "E1002"
    INVALID_CHARACTERS = "E1003"
    MALFORMED_UNC = "E1004"
    INVALID_DRIVE_LETTER = "E1005"

    # Security errors (2000-2999)
    PATH_TRAVERSAL = "E2001"
    SYMLINK_ATTACK = "E2002"
    INJECTION_ATTEMPT = "E2003"
    SANDBOX_VIOLATION = "E2004"
    PERMISSION_DENIED = "E2005"

    # Platform errors (3000-3999)
    WINDOWS_RESERVED_NAME = "E3001"
    PATH_TOO_LONG = "E3002"
    COMPONENT_TOO_LONG = "E3003"
    UNSUPPORTED_PLATFORM = "E3004"
    CASE_SENSITIVITY_CONFLICT = "E3005"

    # Existence errors (4000-4999)
    PATH_NOT_FOUND = "E4001"
    NOT_A_FILE = "E4002"
    NOT_A_DIRECTORY = "E4003"
    ACCESS_DENIED = "E4004"
    DISK_FULL = "E4005"

    # Configuration errors (5000-5999)
    INVALID_CONFIG = "E5001"
    MISSING_PARAMETER = "E5002"
    CONFLICTING_OPTIONS = "E5003"

    # Resource errors (6000-6999)
    MEMORY_EXHAUSTED = "E6001"
    RATE_LIMIT_EXCEEDED = "E6002"
    TIMEOUT = "E6003"

    # Unicode errors (7000-7999)
    ENCODING_ERROR = "E7001"
    NORMALIZATION_ERROR = "E7002"
    SURROGATE_ERROR = "E7003"


class PathValidationError(Exception):
    """Base exception for all path validation errors."""

    def __init__(self, message: str, path: Optional[str] = None, error_code: Optional[str] = None):
        super().__init__(message)
        self.path = path
        self.error_code = error_code
        self.timestamp = datetime.utcnow()

    def __str__(self) -> str:
        if self.path:
            return f"{super().__str__()} (Path: '{self.path}')"
        return super().__str__()

    def get_debug_info(self) -> dict:
        """Return comprehensive debugging information."""
        return {
            "error_message": str(self),
            "error_code": self.error_code,
            "path": self.path,
            "error_type": self.__class__.__name__,
            "timestamp": self.timestamp.isoformat(),
        }


class PathSyntaxError(PathValidationError):
    """Invalid path syntax or format."""

    def __init__(self, message: str, path: Optional[str] = None, invalid_chars: Optional[List[str]] = None):
        super().__init__(message, path, ErrorCodes.INVALID_SYNTAX)
        self.invalid_chars = invalid_chars or []


class PathSecurityError(PathValidationError):
    """Security-related path validation failure."""

    def __init__(self, message: str, path: Optional[str] = None, threat_type: Optional[str] = None):
        super().__init__(message, path, ErrorCodes.INJECTION_ATTEMPT)
        self.threat_type = threat_type


class PathTraversalError(PathSecurityError):
    """Path traversal attempt detected."""

    def __init__(self, message: str, path: Optional[str] = None, pattern: Optional[str] = None):
        super().__init__(message, path, "TRAVERSAL_ATTEMPT")
        self.error_code = ErrorCodes.PATH_TRAVERSAL
        self.pattern = pattern


class PathPlatformError(PathValidationError):
    """Platform-specific constraint violation."""

    def __init__(self, message: str, path: Optional[str] = None, platform: Optional[str] = None):
        super().__init__(message, path, ErrorCodes.UNSUPPORTED_PLATFORM)
        self.platform = platform


class PathExistenceError(PathValidationError):
    """File or directory existence/access issues."""

    def __init__(self, message: str, path: Optional[str] = None):
        super().__init__(message, path, ErrorCodes.PATH_NOT_FOUND)


class PathPermissionError(PathExistenceError):
    """Insufficient permissions for path operation."""

    def __init__(self, message: str, path: Optional[str] = None, required_permission: Optional[str] = None):
        super().__init__(message, path)
        self.error_code = ErrorCodes.PERMISSION_DENIED
        self.required_permission = required_permission


class PathLengthError(PathValidationError):
    """Path or component length exceeds limits."""

    def __init__(self, message: str, path: Optional[str] = None,
                 actual_length: Optional[int] = None, max_length: Optional[int] = None):
        super().__init__(message, path, ErrorCodes.PATH_TOO_LONG)
        self.actual_length = actual_length
        self.max_length = max_length


class PathUnicodeError(PathValidationError):
    """Unicode encoding or normalization error."""

    def __init__(self, message: str, path: Optional[str] = None, encoding: Optional[str] = None):
        super().__init__(message, path, ErrorCodes.ENCODING_ERROR)
        self.encoding = encoding