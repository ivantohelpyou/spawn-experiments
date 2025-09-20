"""Custom exception classes for Prime Number Generator"""


class PrimeGeneratorError(Exception):
    """Base exception for prime generator errors"""
    pass


class InvalidInputError(PrimeGeneratorError):
    """Raised when input validation fails"""
    pass


class ComputationError(PrimeGeneratorError):
    """Raised when computation fails or exceeds limits"""
    pass