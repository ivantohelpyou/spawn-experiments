"""Prime number generation algorithms

This module provides efficient algorithms for generating prime numbers,
including the Sieve of Eratosthenes for bulk generation and optimized
methods for finding specific primes.
"""

import math
from .core import PrimeChecker


class PrimeGenerator:
    """Handles prime number generation using various algorithms"""

    @staticmethod
    def generate_up_to(limit):
        """
        Generate all prime numbers up to and including limit.

        Args:
            limit (int): Upper bound for prime generation

        Returns:
            List[int]: List of prime numbers <= limit

        Raises:
            TypeError: If limit is not an integer
            ValueError: If limit is negative
        """
        # Input validation
        if not isinstance(limit, int):
            raise TypeError(f"Expected integer, got {type(limit).__name__}")

        if limit < 0:
            raise ValueError("Limit cannot be negative")

        # Handle edge cases
        if limit < 2:
            return []

        # Use Sieve of Eratosthenes for efficiency
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False

        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = False

        return [i for i in range(2, limit + 1) if sieve[i]]

    @staticmethod
    def generate_in_range(start, end):
        """
        Generate prime numbers in the range [start, end].

        Args:
            start (int): Lower bound (inclusive)
            end (int): Upper bound (inclusive)

        Returns:
            List[int]: List of prime numbers in range

        Raises:
            TypeError: If start or end is not an integer
            ValueError: If start or end is negative, or start > end
        """
        # Input validation
        if not isinstance(start, int):
            raise TypeError(f"Expected integer for start, got {type(start).__name__}")
        if not isinstance(end, int):
            raise TypeError(f"Expected integer for end, got {type(end).__name__}")

        if start < 0:
            raise ValueError("Start cannot be negative")
        if end < 0:
            raise ValueError("End cannot be negative")
        if start > end:
            raise ValueError("Start cannot be greater than end")

        # Generate all primes up to end, then filter by range
        all_primes = PrimeGenerator.generate_up_to(end)
        return [p for p in all_primes if p >= start]

    @staticmethod
    def nth_prime(n):
        """
        Find the nth prime number using optimized upper bound estimation.

        Uses the prime number theorem to estimate an upper bound for the nth prime,
        then applies the Sieve of Eratosthenes to generate primes efficiently.

        Args:
            n (int): Position of prime to find (1-indexed)

        Returns:
            int: The nth prime number

        Raises:
            TypeError: If n is not an integer
            ValueError: If n <= 0

        Examples:
            >>> PrimeGenerator.nth_prime(1)
            2
            >>> PrimeGenerator.nth_prime(10)
            29
        """
        # Input validation
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")

        if n <= 0:
            raise ValueError("n must be positive")

        # Calculate upper bound using prime number theorem approximation
        upper_bound = PrimeGenerator._estimate_nth_prime_upper_bound(n)

        while True:
            primes = PrimeGenerator.generate_up_to(upper_bound)
            if len(primes) >= n:
                return primes[n - 1]
            # If we don't have enough primes, double the bound
            upper_bound *= 2

    @staticmethod
    def _estimate_nth_prime_upper_bound(n):
        """
        Estimate an upper bound for the nth prime number.

        Uses improved bounds based on the prime number theorem.

        Args:
            n (int): Position of prime to estimate

        Returns:
            int: Estimated upper bound for the nth prime
        """
        if n < 6:
            return 12
        elif n < 11:
            return 31
        else:
            # For larger n, use the formula: n * (ln(n) + ln(ln(n)))
            # with a safety factor
            ln_n = math.log(n)
            estimate = n * (ln_n + math.log(ln_n))
            return int(estimate * 1.2)  # Add 20% safety margin