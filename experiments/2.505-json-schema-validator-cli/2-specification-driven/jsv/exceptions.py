"""Custom exceptions for JSON Schema Validator CLI."""


class JSVError(Exception):
    """Base exception for all JSV errors."""
    pass


class SchemaError(JSVError):
    """Raised when schema file is invalid or cannot be loaded."""
    pass


class ValidationError(JSVError):
    """Raised when JSON validation fails."""
    pass


class FileError(JSVError):
    """Raised when file operations fail."""
    pass


class UsageError(JSVError):
    """Raised when command-line arguments are invalid."""
    pass