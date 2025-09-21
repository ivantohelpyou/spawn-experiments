"""
Custom exceptions for the Prime Number Generator application.

This module defines the custom exception hierarchy used throughout
the application for proper error handling and user feedback.
"""


class PrimeGeneratorError(Exception):
    """Base exception class for Prime Number Generator application."""
    pass


class InvalidInputError(PrimeGeneratorError):
    """Raised when input parameters are invalid."""
    pass


class InvalidRangeError(InvalidInputError):
    """Raised when range parameters are invalid."""
    pass


class InvalidLimitError(InvalidInputError):
    """Raised when limit parameter is invalid."""
    pass


class InvalidNumberError(InvalidInputError):
    """Raised when a number parameter is invalid."""
    pass


class AlgorithmError(PrimeGeneratorError):
    """Raised when algorithm execution encounters an error."""
    pass


class PerformanceError(PrimeGeneratorError):
    """Raised when performance monitoring encounters an error."""
    pass


class MemoryLimitExceededError(PrimeGeneratorError):
    """Raised when memory usage exceeds configured limits."""
    pass


class TimeoutError(PrimeGeneratorError):
    """Raised when operation exceeds time limits."""
    pass