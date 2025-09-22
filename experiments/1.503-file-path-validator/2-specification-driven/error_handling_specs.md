# Error Handling Specifications

## Error Classification System

### Error Categories
1. **Syntax Errors**: Invalid path format or structure
2. **Security Errors**: Path traversal, injection attempts, permission violations
3. **Platform Errors**: OS-specific constraint violations
4. **Existence Errors**: File/directory not found, access denied
5. **Configuration Errors**: Invalid validator configuration or parameters
6. **Resource Errors**: Path too long, insufficient memory, disk space
7. **Unicode Errors**: Character encoding and normalization issues

## Error Hierarchy

```python
class PathValidationError(Exception):
    """Base exception for all path validation errors."""
    def __init__(self, message: str, path: str = None, error_code: str = None):
        super().__init__(message)
        self.path = path
        self.error_code = error_code
        self.timestamp = datetime.utcnow()

class PathSyntaxError(PathValidationError):
    """Invalid path syntax or format."""
    pass

class PathSecurityError(PathValidationError):
    """Security-related path validation failure."""
    def __init__(self, message: str, path: str = None, threat_type: str = None):
        super().__init__(message, path, "SECURITY_VIOLATION")
        self.threat_type = threat_type

class PathTraversalError(PathSecurityError):
    """Path traversal attempt detected."""
    def __init__(self, message: str, path: str = None):
        super().__init__(message, path, "TRAVERSAL_ATTEMPT")

class PathPlatformError(PathValidationError):
    """Platform-specific constraint violation."""
    def __init__(self, message: str, path: str = None, platform: str = None):
        super().__init__(message, path, "PLATFORM_VIOLATION")
        self.platform = platform

class PathExistenceError(PathValidationError):
    """File or directory existence/access issues."""
    pass

class PathPermissionError(PathExistenceError):
    """Insufficient permissions for path operation."""
    def __init__(self, message: str, path: str = None, required_permission: str = None):
        super().__init__(message, path, "PERMISSION_DENIED")
        self.required_permission = required_permission

class PathLengthError(PathValidationError):
    """Path or component length exceeds limits."""
    def __init__(self, message: str, path: str = None, actual_length: int = None, max_length: int = None):
        super().__init__(message, path, "LENGTH_EXCEEDED")
        self.actual_length = actual_length
        self.max_length = max_length

class PathUnicodeError(PathValidationError):
    """Unicode encoding or normalization error."""
    def __init__(self, message: str, path: str = None, encoding: str = None):
        super().__init__(message, path, "UNICODE_ERROR")
        self.encoding = encoding
```

## Error Code System

### Standardized Error Codes
```python
class ErrorCodes:
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
```

## Error Message Templates

### Localized Error Messages
```python
ERROR_MESSAGES = {
    "en": {
        "E1001": "Invalid path syntax: '{path}'",
        "E1002": "Path cannot be empty",
        "E1003": "Path contains invalid characters: {invalid_chars}",
        "E2001": "Path traversal detected in: '{path}'",
        "E2002": "Unsafe symbolic link detected: '{path}'",
        "E3001": "Reserved name '{name}' not allowed on Windows",
        "E3002": "Path length {length} exceeds maximum {max_length}",
        "E4001": "Path not found: '{path}'",
        "E4002": "Expected file but found directory: '{path}'",
        "E5001": "Invalid configuration: {details}",
        "E6001": "Memory limit exceeded during validation",
        "E7001": "Character encoding error in path: '{path}'",
    },
    "es": {
        "E1001": "Sintaxis de ruta inválida: '{path}'",
        "E1002": "La ruta no puede estar vacía",
        "E2001": "Travesía de directorio detectada en: '{path}'",
        # ... additional translations
    },
    # Additional languages...
}
```

### Dynamic Error Message Generation
```python
def format_error_message(error_code: str, locale: str = "en", **kwargs) -> str:
    """
    Generate localized error message with dynamic parameters.
    """
    template = ERROR_MESSAGES.get(locale, ERROR_MESSAGES["en"]).get(error_code)
    if not template:
        return f"Unknown error: {error_code}"

    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"Error formatting message for {error_code}: missing parameter {e}"
```

## Error Context and Debugging

### Rich Error Context
```python
@dataclass
class ErrorContext:
    """Rich context information for debugging validation errors."""
    validation_step: str           # Which validation step failed
    input_path: str               # Original input path
    normalized_path: str          # Path after normalization
    platform: str                # Target platform
    validator_config: dict        # Validator configuration
    stack_trace: List[str]        # Call stack when error occurred
    suggested_fix: Optional[str]  # Suggested resolution
    related_paths: List[str]      # Related paths that might help debugging

class DetailedPathValidationError(PathValidationError):
    """Enhanced error with rich debugging context."""
    def __init__(self, message: str, context: ErrorContext):
        super().__init__(message, context.input_path)
        self.context = context

    def get_debug_info(self) -> dict:
        """Return comprehensive debugging information."""
        return {
            "error_message": str(self),
            "error_code": self.error_code,
            "input_path": self.context.input_path,
            "normalized_path": self.context.normalized_path,
            "validation_step": self.context.validation_step,
            "platform": self.context.platform,
            "config": self.context.validator_config,
            "suggested_fix": self.context.suggested_fix,
            "timestamp": self.timestamp.isoformat(),
            "stack_trace": self.context.stack_trace,
        }
```

## Error Recovery and Suggestions

### Automatic Error Recovery
```python
class ErrorRecovery:
    """Attempt to recover from common path validation errors."""

    @staticmethod
    def suggest_fixes(error: PathValidationError) -> List[str]:
        """Generate suggestions for fixing validation errors."""
        suggestions = []

        if isinstance(error, PathTraversalError):
            suggestions.extend([
                "Remove '../' sequences from the path",
                "Use absolute paths instead of relative paths",
                "Validate path against allowed directories"
            ])

        elif isinstance(error, PathLengthError):
            suggestions.extend([
                f"Reduce path length to under {error.max_length} characters",
                "Use shorter directory or file names",
                "Consider using symbolic links to reduce path depth"
            ])

        elif isinstance(error, PathPlatformError):
            if "reserved name" in str(error).lower():
                suggestions.append("Choose a different filename (avoid CON, PRN, AUX, etc.)")

        return suggestions

    @staticmethod
    def attempt_auto_fix(path: str, error: PathValidationError) -> Optional[str]:
        """Attempt to automatically fix common path issues."""
        if isinstance(error, PathSyntaxError):
            # Try normalizing separators
            fixed = path.replace('\\', '/') if os.sep == '/' else path.replace('/', '\\')
            return fixed

        elif isinstance(error, PathLengthError):
            # Try shortening the path
            if len(path) > 260:  # Common Windows limit
                return path[:260]

        return None
```

## Error Logging and Monitoring

### Structured Error Logging
```python
import logging
import json
from typing import Dict, Any

class PathValidationLogger:
    """Structured logging for path validation errors."""

    def __init__(self, logger_name: str = "path_validator"):
        self.logger = logging.getLogger(logger_name)

    def log_error(self, error: PathValidationError, extra_context: Dict[str, Any] = None):
        """Log path validation error with structured data."""
        log_data = {
            "event": "path_validation_error",
            "error_type": error.__class__.__name__,
            "error_code": error.error_code,
            "error_message": str(error),
            "path": error.path,
            "timestamp": error.timestamp.isoformat(),
        }

        if extra_context:
            log_data.update(extra_context)

        if isinstance(error, PathSecurityError):
            log_data["security_threat"] = error.threat_type
            self.logger.warning("Security violation detected", extra=log_data)
        else:
            self.logger.error("Path validation failed", extra=log_data)

    def log_suspicious_activity(self, client_id: str, patterns: List[str]):
        """Log suspicious validation patterns that might indicate attacks."""
        log_data = {
            "event": "suspicious_activity",
            "client_id": client_id,
            "patterns": patterns,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.logger.warning("Suspicious path validation patterns", extra=log_data)
```

### Error Metrics and Monitoring
```python
from collections import defaultdict, Counter
from datetime import datetime, timedelta

class ErrorMetrics:
    """Track error patterns and frequencies for monitoring."""

    def __init__(self):
        self.error_counts = Counter()
        self.error_history = defaultdict(list)
        self.security_events = []

    def record_error(self, error: PathValidationError):
        """Record error occurrence for metrics."""
        error_key = f"{error.__class__.__name__}:{error.error_code}"
        self.error_counts[error_key] += 1
        self.error_history[error_key].append(datetime.utcnow())

        if isinstance(error, PathSecurityError):
            self.security_events.append({
                "timestamp": datetime.utcnow(),
                "error_type": error.__class__.__name__,
                "path": error.path,
                "threat_type": getattr(error, 'threat_type', 'unknown')
            })

    def get_error_rate(self, error_type: str, window_minutes: int = 60) -> float:
        """Calculate error rate for specific error type."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        recent_errors = [
            ts for ts in self.error_history[error_type]
            if ts >= cutoff
        ]
        return len(recent_errors) / window_minutes  # errors per minute

    def get_security_alerts(self, window_minutes: int = 60) -> List[dict]:
        """Get recent security events for alerting."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        return [
            event for event in self.security_events
            if event["timestamp"] >= cutoff
        ]
```

## Error Handling Best Practices

### Exception Handling Guidelines
```python
def validate_path_with_proper_error_handling(path: str) -> ValidationResult:
    """Example of proper error handling in path validation."""
    try:
        # Attempt validation
        result = perform_path_validation(path)
        return result

    except PathTraversalError as e:
        # Log security event immediately
        security_logger.log_security_event(e)
        # Return secure error response
        return ValidationResult(
            valid=False,
            error=e,
            safe_error_message="Path validation failed due to security constraints"
        )

    except PathPlatformError as e:
        # Suggest platform-specific fixes
        suggestions = ErrorRecovery.suggest_fixes(e)
        return ValidationResult(
            valid=False,
            error=e,
            suggestions=suggestions
        )

    except Exception as e:
        # Log unexpected errors for debugging
        logger.exception("Unexpected error during path validation")
        # Convert to standardized error
        wrapped_error = PathValidationError(
            "Internal validation error",
            path=path,
            error_code="E9999"
        )
        return ValidationResult(valid=False, error=wrapped_error)
```

### Error Response Format
```python
@dataclass
class ValidationResult:
    """Standardized validation result with error information."""
    valid: bool
    path: Optional[str] = None
    normalized_path: Optional[str] = None
    error: Optional[PathValidationError] = None
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert result to dictionary for API responses."""
        result = {
            "valid": self.valid,
            "path": self.path,
            "normalized_path": self.normalized_path,
        }

        if self.error:
            result["error"] = {
                "code": self.error.error_code,
                "message": str(self.error),
                "type": self.error.__class__.__name__,
            }

        if self.warnings:
            result["warnings"] = self.warnings

        if self.suggestions:
            result["suggestions"] = self.suggestions

        if self.metadata:
            result["metadata"] = self.metadata

        return result
```