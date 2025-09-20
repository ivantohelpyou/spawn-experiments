"""Core prime number checking functionality

This module provides efficient algorithms for determining if a number is prime.
Uses optimized trial division with early termination conditions.
"""

import math


class PrimeChecker:
    """Handles prime number validation using optimized algorithms"""

    @staticmethod
    def is_prime(n):
        """
        Check if a number is prime using optimized trial division.

        A prime number is a natural number greater than 1 that has no positive
        divisors other than 1 and itself.

        Args:
            n (int): Integer to check for primality

        Returns:
            bool: True if n is prime, False otherwise

        Raises:
            TypeError: If n is not an integer
            ValueError: If n is negative

        Examples:
            >>> PrimeChecker.is_prime(17)
            True
            >>> PrimeChecker.is_prime(18)
            False
            >>> PrimeChecker.is_prime(2)
            True
        """
        # Input validation
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")

        if n < 0:
            raise ValueError("Cannot check primality of negative numbers")

        # Handle special cases
        if n <= 1:
            return False

        if n <= 3:
            return True

        if n % 2 == 0 or n % 3 == 0:
            return False

        # Check for divisors using 6k±1 optimization
        # All primes > 3 are of the form 6k±1
        limit = int(math.sqrt(n)) + 1
        for i in range(5, limit, 6):
            if n % i == 0 or n % (i + 2) == 0:
                return False

        return True