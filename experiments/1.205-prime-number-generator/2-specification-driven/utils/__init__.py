"""
Utility modules for the Prime Number Generator application.

This package contains utility functions, helper methods, and
custom exception definitions.
"""

from .exceptions import (
    PrimeGeneratorError,
    InvalidInputError,
    InvalidRangeError,
    InvalidLimitError,
    InvalidNumberError,
    AlgorithmError,
    PerformanceError,
    MemoryLimitExceededError,
    TimeoutError
)

from .helpers import (
    format_number,
    format_time,
    format_memory,
    is_perfect_square,
    get_prime_factors,
    estimate_sieve_memory,
    calculate_nth_prime_upper_bound,
    validate_positive_integer,
    validate_non_negative_integer,
    validate_range,
    get_system_info,
    create_progress_bar
)

__all__ = [
    # Exceptions
    'PrimeGeneratorError',
    'InvalidInputError',
    'InvalidRangeError',
    'InvalidLimitError',
    'InvalidNumberError',
    'AlgorithmError',
    'PerformanceError',
    'MemoryLimitExceededError',
    'TimeoutError',

    # Helpers
    'format_number',
    'format_time',
    'format_memory',
    'is_perfect_square',
    'get_prime_factors',
    'estimate_sieve_memory',
    'calculate_nth_prime_upper_bound',
    'validate_positive_integer',
    'validate_non_negative_integer',
    'validate_range',
    'get_system_info',
    'create_progress_bar'
]