"""
Custom exceptions for the Expression Evaluator system.

This module defines all custom exceptions used throughout the system
to provide clear error handling and reporting.
"""

from typing import Optional


class ExpressionError(Exception):
    """Base exception for all expression evaluator errors."""

    def __init__(self, message: str, position: Optional[int] = None, suggestion: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.position = position
        self.suggestion = suggestion

    def __str__(self) -> str:
        result = self.message
        if self.position is not None:
            result += f" at position {self.position}"
        if self.suggestion:
            result += f". Suggestion: {self.suggestion}"
        return result


class SyntaxError(ExpressionError):
    """Raised when expression has syntax errors."""
    pass


class EvaluationError(ExpressionError):
    """Raised when expression evaluation fails."""
    pass


class VariableError(ExpressionError):
    """Raised when variable-related errors occur."""
    pass


class FunctionError(ExpressionError):
    """Raised when function-related errors occur."""
    pass


class ValidationError(ExpressionError):
    """Raised when expression validation fails."""
    pass


class TimeoutError(ExpressionError):
    """Raised when expression evaluation times out."""
    pass


class MemoryError(ExpressionError):
    """Raised when memory limits are exceeded."""
    pass