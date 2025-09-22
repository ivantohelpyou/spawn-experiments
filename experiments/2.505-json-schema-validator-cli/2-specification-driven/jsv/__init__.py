"""JSON Schema Validator CLI - A command-line JSON Schema validation tool."""

__version__ = "1.0.0"
__author__ = "CLI Developer"
__email__ = "dev@example.com"
__description__ = "A command-line JSON Schema Validator tool"

from .validator import JSONValidator, ValidationResult, ValidationError
from .schema_checker import SchemaChecker
from .exceptions import JSVError, SchemaError, FileError

__all__ = [
    "JSONValidator",
    "ValidationResult",
    "ValidationError",
    "SchemaChecker",
    "JSVError",
    "SchemaError",
    "FileError",
]