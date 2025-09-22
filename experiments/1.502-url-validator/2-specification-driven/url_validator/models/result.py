"""Results and response models for URL validation."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
import json

from .error import ValidationError


@dataclass
class URLComponents:
    """
    Parsed components of a URL.

    This class represents the individual components of a URL as parsed
    by urllib.parse, with additional validation and utility methods.
    """

    scheme: str
    netloc: str
    path: str
    params: str
    query: str
    fragment: str
    username: Optional[str] = None
    password: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert URL components to dictionary."""
        return {
            "scheme": self.scheme,
            "netloc": self.netloc,
            "path": self.path,
            "params": self.params,
            "query": self.query,
            "fragment": self.fragment,
            "username": self.username,
            "password": self.password,
            "hostname": self.hostname,
            "port": self.port,
        }

    @property
    def base_url(self) -> str:
        """Get the base URL (scheme + netloc)."""
        return f"{self.scheme}://{self.netloc}"

    @property
    def is_secure(self) -> bool:
        """Check if the URL uses a secure scheme."""
        return self.scheme.lower() in {"https", "ftps"}

    @property
    def has_auth(self) -> bool:
        """Check if the URL contains authentication information."""
        return self.username is not None or self.password is not None


@dataclass
class AccessibilityResult:
    """
    Results from accessibility checking.

    Contains information about the HTTP response and accessibility status.
    """

    is_accessible: bool
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    final_url: Optional[str] = None
    redirect_count: int = 0
    redirect_chain: List[str] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    ssl_info: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert accessibility result to dictionary."""
        return {
            "is_accessible": self.is_accessible,
            "status_code": self.status_code,
            "response_time": self.response_time,
            "final_url": self.final_url,
            "redirect_count": self.redirect_count,
            "redirect_chain": self.redirect_chain,
            "headers": self.headers,
            "ssl_info": self.ssl_info,
            "error_details": self.error_details,
        }


@dataclass
class ValidationResult:
    """
    Complete result of URL validation.

    This class contains all information about URL validation including
    format validation, accessibility checking, errors, and metadata.

    Attributes:
        url: The original URL that was validated
        is_valid: Whether the URL has valid format
        is_accessible: Whether the URL is accessible over the network
        errors: List of validation errors encountered
        warnings: List of warning messages
        url_components: Parsed URL components (if format is valid)
        accessibility_result: Results from accessibility checking
        metadata: Additional metadata about the validation
        timestamp: When the validation was performed
        duration: How long validation took in seconds
    """

    url: str
    is_valid: bool
    is_accessible: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    url_components: Optional[URLComponents] = None
    accessibility_result: Optional[AccessibilityResult] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    duration: float = 0.0

    def __str__(self) -> str:
        """Return string representation of validation result."""
        status = "VALID" if self.is_valid else "INVALID"
        accessible = " & ACCESSIBLE" if self.is_accessible else " & INACCESSIBLE"
        if not self.is_valid:
            accessible = ""
        return f"{self.url}: {status}{accessible}"

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (
            f"ValidationResult(url='{self.url}', "
            f"is_valid={self.is_valid}, "
            f"is_accessible={self.is_accessible}, "
            f"errors={len(self.errors)})"
        )

    @property
    def has_errors(self) -> bool:
        """Check if validation has any errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if validation has any warnings."""
        return len(self.warnings) > 0

    @property
    def error_codes(self) -> List[str]:
        """Get list of error codes."""
        return [error.code for error in self.errors]

    @property
    def error_categories(self) -> List[str]:
        """Get list of unique error categories."""
        return list(set(error.category.value for error in self.errors))

    def add_error(self, error: ValidationError) -> None:
        """
        Add a validation error.

        Args:
            error: ValidationError to add
        """
        self.errors.append(error)
        # If we have format errors, mark as invalid
        if error.category.value == "format":
            self.is_valid = False

    def add_warning(self, message: str) -> None:
        """
        Add a warning message.

        Args:
            message: Warning message to add
        """
        self.warnings.append(message)

    def set_url_components(self, components: URLComponents) -> None:
        """
        Set the parsed URL components.

        Args:
            components: URLComponents object
        """
        self.url_components = components

    def set_accessibility_result(self, result: AccessibilityResult) -> None:
        """
        Set the accessibility checking result.

        Args:
            result: AccessibilityResult object
        """
        self.accessibility_result = result
        self.is_accessible = result.is_accessible

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert validation result to dictionary.

        Returns:
            Dictionary representation of the validation result
        """
        return {
            "url": self.url,
            "is_valid": self.is_valid,
            "is_accessible": self.is_accessible,
            "errors": [
                {
                    "code": error.code,
                    "category": error.category.value,
                    "message": error.message,
                    "details": error.details,
                }
                for error in self.errors
            ],
            "warnings": self.warnings,
            "url_components": self.url_components.to_dict() if self.url_components else None,
            "accessibility_result": self.accessibility_result.to_dict() if self.accessibility_result else None,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "duration": self.duration,
        }

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Convert validation result to JSON string.

        Args:
            indent: JSON indentation level

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent, default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValidationResult":
        """
        Create ValidationResult from dictionary.

        Args:
            data: Dictionary containing validation result data

        Returns:
            ValidationResult instance
        """
        # Reconstruct errors
        errors = []
        for error_data in data.get("errors", []):
            from .error import ErrorCategory
            errors.append(
                ValidationError(
                    code=error_data["code"],
                    category=ErrorCategory(error_data["category"]),
                    message=error_data["message"],
                    details=error_data.get("details"),
                )
            )

        # Reconstruct URL components
        url_components = None
        if data.get("url_components"):
            url_components = URLComponents(**data["url_components"])

        # Reconstruct accessibility result
        accessibility_result = None
        if data.get("accessibility_result"):
            accessibility_result = AccessibilityResult(**data["accessibility_result"])

        # Parse timestamp
        timestamp = datetime.now()
        if data.get("timestamp"):
            timestamp = datetime.fromisoformat(data["timestamp"])

        return cls(
            url=data["url"],
            is_valid=data["is_valid"],
            is_accessible=data["is_accessible"],
            errors=errors,
            warnings=data.get("warnings", []),
            url_components=url_components,
            accessibility_result=accessibility_result,
            metadata=data.get("metadata", {}),
            timestamp=timestamp,
            duration=data.get("duration", 0.0),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "ValidationResult":
        """
        Create ValidationResult from JSON string.

        Args:
            json_str: JSON string containing validation result

        Returns:
            ValidationResult instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the validation result.

        Returns:
            Dictionary with summary information
        """
        return {
            "url": self.url,
            "status": "valid" if self.is_valid else "invalid",
            "accessible": self.is_accessible if self.is_valid else None,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
        }