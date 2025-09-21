"""
Prime number generator module developed using Test-Driven Development
with comprehensive test validation.

This module provides functions for prime number checking and generation,
following mathematical definitions and optimized algorithms.
"""

import math


class InvalidInputError(Exception):
    """Raised when invalid input is provided to prime functions."""
    pass


def _validate_integer_input(value, parameter_name="value"):
    """
    Validate that input is an integer.

    Args:
        value: Value to validate
        parameter_name: Name of parameter for error messages

    Raises:
        InvalidInputError: If value is not an integer
    """
    if not isinstance(value, int):
        raise InvalidInputError(
            f"Parameter '{parameter_name}' must be an integer, "
            f"got {type(value).__name__}"
        )


def is_prime(n):
    """
    Determine if a number is prime.

    A prime number is a natural number greater than 1 that has no positive
    divisors other than 1 and itself.

    Args:
        n: Integer to test for primality

    Returns:
        bool: True if n is prime, False otherwise

    Raises:
        InvalidInputError: If n is not an integer

    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(4)
        False
        >>> is_prime(17)
        True
    """
    # Input validation
    _validate_integer_input(n, "n")

    # Handle edge cases
    if n < 2:
        return False

    if n == 2:
        return True

    # Even numbers (except 2) are not prime
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    # Use int(math.sqrt) + 1 for clarity and accuracy
    sqrt_n = int(math.sqrt(n))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False

    return True


def generate_primes(limit):
    """
    Generate all prime numbers up to and including the given limit.

    Uses the Sieve of Eratosthenes algorithm for efficient prime generation.
    For small limits (< 100), uses a simple trial division for clarity.

    Args:
        limit: Upper bound for prime generation (inclusive)

    Returns:
        list: List of all prime numbers <= limit, in ascending order

    Raises:
        InvalidInputError: If limit is not an integer or is negative

    Examples:
        >>> generate_primes(10)
        [2, 3, 5, 7]
        >>> generate_primes(2)
        [2]
        >>> generate_primes(1)
        []
    """
    # Input validation
    _validate_integer_input(limit, "limit")

    if limit < 0:
        raise InvalidInputError("limit cannot be negative")

    if limit < 2:
        return []

    # For small limits, use simple approach for clarity
    if limit < 100:
        return _generate_primes_simple(limit)
    else:
        return _generate_primes_sieve(limit)


def _generate_primes_simple(limit):
    """Generate primes using simple trial division."""
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes


def _generate_primes_sieve(limit):
    """Generate primes using Sieve of Eratosthenes."""
    # Create a boolean array "prime[0..limit]" and initialize
    # all entries as True
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False  # 0 and 1 are not prime

    p = 2
    while p * p <= limit:
        # If prime[p] is not changed, then it is a prime
        if prime[p]:
            # Update all multiples of p
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1

    # Collect all prime numbers
    primes = []
    for i in range(2, limit + 1):
        if prime[i]:
            primes.append(i)

    return primes