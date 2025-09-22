"""Error handling models and enumerations."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional


class ErrorCategory(Enum):
    """Categories of validation errors."""

    FORMAT = "format"
    NETWORK = "network"
    SECURITY = "security"
    CONFIGURATION = "configuration"
    SYSTEM = "system"


class ErrorCode:
    """Standard error codes for URL validation."""

    # Format error codes (URL_xxx)
    INVALID_STRUCTURE = "URL_001"
    MISSING_SCHEME = "URL_002"
    UNSUPPORTED_SCHEME = "URL_003"
    INVALID_DOMAIN = "URL_004"
    INVALID_IP_ADDRESS = "URL_005"
    INVALID_PORT = "URL_006"
    INVALID_ENCODING = "URL_007"
    MALFORMED_URL = "URL_008"

    # Network error codes (NET_xxx)
    CONNECTION_TIMEOUT = "NET_001"
    DNS_RESOLUTION_FAILED = "NET_002"
    CONNECTION_REFUSED = "NET_003"
    SSL_CERTIFICATE_ERROR = "NET_004"
    TOO_MANY_REDIRECTS = "NET_005"
    INVALID_RESPONSE = "NET_006"
    NETWORK_UNREACHABLE = "NET_007"
    READ_TIMEOUT = "NET_008"

    # Security error codes (SEC_xxx)
    SSRF_DETECTED = "SEC_001"
    PRIVATE_IP_BLOCKED = "SEC_002"
    MALICIOUS_PATTERN = "SEC_003"
    RATE_LIMIT_EXCEEDED = "SEC_004"

    # Configuration error codes (CFG_xxx)
    INVALID_TIMEOUT = "CFG_001"
    INVALID_REDIRECT_LIMIT = "CFG_002"
    INVALID_SCHEME_CONFIG = "CFG_003"
    MISSING_CONFIGURATION = "CFG_004"

    # System error codes (SYS_xxx)
    MEMORY_ERROR = "SYS_001"
    RESOURCE_EXHAUSTED = "SYS_002"
    UNEXPECTED_ERROR = "SYS_003"


@dataclass
class ValidationError:
    """
    Represents a validation error with detailed information.

    Attributes:
        code: Unique error code identifying the error type
        category: High-level category of the error
        message: Human-readable error message
        details: Additional error-specific information
    """

    code: str
    category: ErrorCategory
    message: str
    details: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        """Return string representation of the error."""
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"ValidationError(code='{self.code}', category={self.category}, message='{self.message}')"

    @classmethod
    def format_error(cls, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> "ValidationError":
        """Create a format validation error."""
        return cls(
            code=code,
            category=ErrorCategory.FORMAT,
            message=message,
            details=details
        )

    @classmethod
    def network_error(cls, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> "ValidationError":
        """Create a network validation error."""
        return cls(
            code=code,
            category=ErrorCategory.NETWORK,
            message=message,
            details=details
        )

    @classmethod
    def security_error(cls, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> "ValidationError":
        """Create a security validation error."""
        return cls(
            code=code,
            category=ErrorCategory.SECURITY,
            message=message,
            details=details
        )

    @classmethod
    def config_error(cls, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> "ValidationError":
        """Create a configuration validation error."""
        return cls(
            code=code,
            category=ErrorCategory.CONFIGURATION,
            message=message,
            details=details
        )

    @classmethod
    def system_error(cls, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> "ValidationError":
        """Create a system validation error."""
        return cls(
            code=code,
            category=ErrorCategory.SYSTEM,
            message=message,
            details=details
        )


class URLValidationException(Exception):
    """
    Exception raised for URL validation errors.

    This exception is used for critical errors that prevent
    validation from continuing.
    """

    def __init__(self, error: ValidationError):
        """Initialize with a ValidationError object."""
        self.error = error
        super().__init__(str(error))

    @property
    def code(self) -> str:
        """Get the error code."""
        return self.error.code

    @property
    def category(self) -> ErrorCategory:
        """Get the error category."""
        return self.error.category