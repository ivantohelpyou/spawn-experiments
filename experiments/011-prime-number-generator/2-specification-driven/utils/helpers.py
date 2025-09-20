"""
Utility functions and helpers for the Prime Number Generator application.

This module provides various utility functions for number formatting,
mathematical operations, and configuration management.
"""

import math
import sys
from typing import List, Any, Dict, Union


def format_number(num: int, use_separators: bool = True) -> str:
    """
    Format a number for display with optional thousand separators.

    Args:
        num: The number to format
        use_separators: Whether to use thousand separators

    Returns:
        Formatted number string
    """
    if use_separators:
        return f"{num:,}"
    return str(num)


def format_time(seconds: float) -> str:
    """
    Format time duration in a human-readable format.

    Args:
        seconds: Time duration in seconds

    Returns:
        Formatted time string
    """
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.3f} s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.2f}s"


def format_memory(bytes_used: int) -> str:
    """
    Format memory usage in a human-readable format.

    Args:
        bytes_used: Memory usage in bytes

    Returns:
        Formatted memory string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_used < 1024.0:
            return f"{bytes_used:.2f} {unit}"
        bytes_used /= 1024.0
    return f"{bytes_used:.2f} TB"


def is_perfect_square(n: int) -> bool:
    """
    Check if a number is a perfect square.

    Args:
        n: Number to check

    Returns:
        True if n is a perfect square, False otherwise
    """
    if n < 0:
        return False
    root = int(math.sqrt(n))
    return root * root == n


def get_prime_factors(n: int) -> List[int]:
    """
    Get prime factors of a number using trial division.

    Args:
        n: Number to factorize

    Returns:
        List of prime factors
    """
    factors = []
    d = 2

    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1

    if n > 1:
        factors.append(n)

    return factors


def estimate_sieve_memory(limit: int) -> int:
    """
    Estimate memory usage for Sieve of Eratosthenes.

    Args:
        limit: Upper limit for sieve

    Returns:
        Estimated memory usage in bytes
    """
    # Boolean array uses 1 byte per element in Python
    return limit + 1


def calculate_nth_prime_upper_bound(n: int) -> int:
    """
    Calculate upper bound for the nth prime number.
    Uses asymptotic approximations for estimation.

    Args:
        n: Position of prime (1-indexed)

    Returns:
        Upper bound estimate for nth prime
    """
    if n < 6:
        return [2, 3, 5, 7, 11, 13][n - 1]

    # Use approximation: p_n < n * (ln(n) + ln(ln(n)))
    log_n = math.log(n)
    log_log_n = math.log(log_n)
    return int(n * (log_n + log_log_n) * 1.2)  # Add 20% safety margin


def validate_positive_integer(value: Any, name: str) -> int:
    """
    Validate that a value is a positive integer.

    Args:
        value: Value to validate
        name: Name of the parameter for error messages

    Returns:
        Validated integer value

    Raises:
        InvalidInputError: If value is not a positive integer
    """
    try:
        from .exceptions import InvalidInputError
    except ImportError:
        from utils.exceptions import InvalidInputError

    try:
        int_value = int(value)
        if int_value <= 0:
            raise InvalidInputError(f"{name} must be a positive integer, got {value}")
        return int_value
    except (TypeError, ValueError):
        raise InvalidInputError(f"{name} must be a positive integer, got {value}")


def validate_non_negative_integer(value: Any, name: str) -> int:
    """
    Validate that a value is a non-negative integer.

    Args:
        value: Value to validate
        name: Name of the parameter for error messages

    Returns:
        Validated integer value

    Raises:
        InvalidInputError: If value is not a non-negative integer
    """
    try:
        from .exceptions import InvalidInputError
    except ImportError:
        from utils.exceptions import InvalidInputError

    try:
        int_value = int(value)
        if int_value < 0:
            raise InvalidInputError(f"{name} must be non-negative, got {value}")
        return int_value
    except (TypeError, ValueError):
        raise InvalidInputError(f"{name} must be a non-negative integer, got {value}")


def validate_range(start: Any, end: Any) -> tuple[int, int]:
    """
    Validate and normalize a range.

    Args:
        start: Range start value
        end: Range end value

    Returns:
        Tuple of validated (start, end) values

    Raises:
        InvalidRangeError: If range is invalid
    """
    try:
        from .exceptions import InvalidRangeError
    except ImportError:
        from utils.exceptions import InvalidRangeError

    start_val = validate_non_negative_integer(start, "start")
    end_val = validate_non_negative_integer(end, "end")

    if start_val > end_val:
        raise InvalidRangeError(f"Range start ({start_val}) must be <= end ({end_val})")

    return start_val, end_val


def get_system_info() -> Dict[str, Any]:
    """
    Get system information for performance analysis.

    Returns:
        Dictionary with system information
    """
    return {
        'python_version': sys.version,
        'platform': sys.platform,
        'max_int': sys.maxsize,
        'recursion_limit': sys.getrecursionlimit()
    }


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Create a simple text-based progress bar.

    Args:
        current: Current progress value
        total: Total value
        width: Width of progress bar in characters

    Returns:
        Progress bar string
    """
    if total == 0:
        return "[" + "=" * width + "] 100%"

    progress = current / total
    filled = int(width * progress)
    bar = "=" * filled + "-" * (width - filled)
    percentage = int(progress * 100)

    return f"[{bar}] {percentage}%"