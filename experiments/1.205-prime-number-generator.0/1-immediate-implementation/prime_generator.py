"""
Prime Number Generator Module

This module provides comprehensive prime number generation and analysis functionality
using only Python's standard library.

Features:
- Multiple prime checking algorithms
- Prime generation with different strategies
- Sieve of Eratosthenes implementation
- Prime factorization
- Performance timing utilities
"""

import time
import math
from typing import List, Iterator, Tuple, Optional


class PrimeGenerator:
    """
    A comprehensive prime number generator with multiple algorithms and utilities.
    """

    def __init__(self):
        """Initialize the prime generator."""
        self._cache = {2: True, 3: True}  # Cache for is_prime results
        self._known_primes = [2, 3]  # Cache for generated primes

    def is_prime(self, n: int, method: str = "optimized") -> bool:
        """
        Check if a number is prime using the specified method.

        Args:
            n: Number to check
            method: Algorithm to use ("basic", "optimized", or "cached")

        Returns:
            True if n is prime, False otherwise
        """
        if n < 2:
            return False

        if n in self._cache:
            return self._cache[n]

        if method == "basic":
            result = self._is_prime_basic(n)
        elif method == "optimized":
            result = self._is_prime_optimized(n)
        elif method == "cached":
            result = self._is_prime_cached(n)
        else:
            raise ValueError(f"Unknown method: {method}")

        self._cache[n] = result
        return result

    def _is_prime_basic(self, n: int) -> bool:
        """Basic trial division algorithm."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def _is_prime_optimized(self, n: int) -> bool:
        """Optimized trial division with 6k±1 optimization."""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _is_prime_cached(self, n: int) -> bool:
        """Use cached primes for faster checking."""
        if n < 2:
            return False

        # Generate primes up to sqrt(n) if needed
        sqrt_n = int(n**0.5) + 1
        while self._known_primes[-1] < sqrt_n:
            self._extend_known_primes()

        # Check divisibility by known primes
        for prime in self._known_primes:
            if prime * prime > n:
                break
            if n % prime == 0:
                return False
        return True

    def _extend_known_primes(self):
        """Extend the cache of known primes."""
        candidate = self._known_primes[-1] + 2
        while not self._is_prime_optimized(candidate):
            candidate += 2
        self._known_primes.append(candidate)

    def generate_primes_up_to(self, limit: int, method: str = "sieve") -> List[int]:
        """
        Generate all prime numbers up to a given limit.

        Args:
            limit: Upper limit (inclusive)
            method: Algorithm to use ("sieve", "trial", or "optimized")

        Returns:
            List of prime numbers up to the limit
        """
        if limit < 2:
            return []

        if method == "sieve":
            return self._sieve_of_eratosthenes(limit)
        elif method == "trial":
            return [n for n in range(2, limit + 1) if self.is_prime(n, "basic")]
        elif method == "optimized":
            return [n for n in range(2, limit + 1) if self.is_prime(n, "optimized")]
        else:
            raise ValueError(f"Unknown method: {method}")

    def _sieve_of_eratosthenes(self, limit: int) -> List[int]:
        """
        Sieve of Eratosthenes algorithm for efficient prime generation.

        Args:
            limit: Upper limit (inclusive)

        Returns:
            List of prime numbers up to the limit
        """
        if limit < 2:
            return []

        # Create boolean array and initialize all entries as True
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False

        p = 2
        while p * p <= limit:
            if is_prime[p]:
                # Mark all multiples of p as not prime
                for i in range(p * p, limit + 1, p):
                    is_prime[i] = False
            p += 1

        # Collect all prime numbers
        return [i for i in range(2, limit + 1) if is_prime[i]]

    def generate_first_n_primes(self, n: int) -> List[int]:
        """
        Generate the first n prime numbers.

        Args:
            n: Number of primes to generate

        Returns:
            List of the first n prime numbers
        """
        if n <= 0:
            return []

        primes = []
        candidate = 2

        while len(primes) < n:
            if self.is_prime(candidate, "optimized"):
                primes.append(candidate)
            candidate += 1

        return primes

    def prime_factorization(self, n: int) -> List[Tuple[int, int]]:
        """
        Find the prime factorization of a number.

        Args:
            n: Number to factorize

        Returns:
            List of (prime, power) tuples representing the factorization
        """
        if n < 2:
            return []

        factors = []
        d = 2

        while d * d <= n:
            power = 0
            while n % d == 0:
                power += 1
                n //= d
            if power > 0:
                factors.append((d, power))
            d += 1

        if n > 1:
            factors.append((n, 1))

        return factors

    def next_prime(self, n: int) -> int:
        """
        Find the next prime number greater than n.

        Args:
            n: Starting number

        Returns:
            Next prime number after n
        """
        candidate = n + 1
        while not self.is_prime(candidate, "optimized"):
            candidate += 1
        return candidate

    def previous_prime(self, n: int) -> Optional[int]:
        """
        Find the previous prime number less than n.

        Args:
            n: Starting number

        Returns:
            Previous prime number before n, or None if no such prime exists
        """
        if n <= 2:
            return None

        candidate = n - 1
        while candidate >= 2:
            if self.is_prime(candidate, "optimized"):
                return candidate
            candidate -= 1
        return None

    def is_mersenne_prime(self, p: int) -> bool:
        """
        Check if 2^p - 1 is a Mersenne prime (where p is prime).

        Args:
            p: Exponent to check

        Returns:
            True if 2^p - 1 is prime and p is prime
        """
        if not self.is_prime(p):
            return False

        mersenne_candidate = (2 ** p) - 1
        return self.is_prime(mersenne_candidate, "optimized")

    def prime_gaps(self, limit: int) -> List[Tuple[int, int, int]]:
        """
        Find gaps between consecutive primes up to a limit.

        Args:
            limit: Upper limit for prime search

        Returns:
            List of (prime1, prime2, gap) tuples
        """
        primes = self.generate_primes_up_to(limit, "sieve")
        gaps = []

        for i in range(len(primes) - 1):
            gap = primes[i + 1] - primes[i]
            gaps.append((primes[i], primes[i + 1], gap))

        return gaps

    def benchmark_methods(self, limit: int) -> dict:
        """
        Benchmark different prime generation methods.

        Args:
            limit: Upper limit for benchmark

        Returns:
            Dictionary with timing results for each method
        """
        results = {}

        # Benchmark sieve method
        start_time = time.time()
        sieve_primes = self.generate_primes_up_to(limit, "sieve")
        results["sieve"] = {
            "time": time.time() - start_time,
            "count": len(sieve_primes)
        }

        # Benchmark trial division
        start_time = time.time()
        trial_primes = self.generate_primes_up_to(limit, "trial")
        results["trial"] = {
            "time": time.time() - start_time,
            "count": len(trial_primes)
        }

        # Benchmark optimized method
        start_time = time.time()
        optimized_primes = self.generate_primes_up_to(limit, "optimized")
        results["optimized"] = {
            "time": time.time() - start_time,
            "count": len(optimized_primes)
        }

        return results


def timing_decorator(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper


# Utility functions for common operations
def is_prime_simple(n: int) -> bool:
    """Simple prime checking function for quick use."""
    generator = PrimeGenerator()
    return generator.is_prime(n)


def primes_up_to(limit: int) -> List[int]:
    """Generate primes up to limit using the most efficient method."""
    generator = PrimeGenerator()
    return generator.generate_primes_up_to(limit, "sieve")


def first_n_primes(n: int) -> List[int]:
    """Generate the first n prime numbers."""
    generator = PrimeGenerator()
    return generator.generate_first_n_primes(n)


if __name__ == "__main__":
    # Quick demonstration
    gen = PrimeGenerator()

    print("Prime Number Generator Demo")
    print("=" * 40)

    # Test prime checking
    test_numbers = [2, 3, 4, 17, 25, 29, 97, 100]
    print("\nPrime checking:")
    for num in test_numbers:
        print(f"{num}: {'Prime' if gen.is_prime(num) else 'Not prime'}")

    # Generate first 10 primes
    print(f"\nFirst 10 primes: {gen.generate_first_n_primes(10)}")

    # Generate primes up to 50
    print(f"\nPrimes up to 50: {gen.generate_primes_up_to(50)}")

    # Prime factorization
    print(f"\nPrime factorization of 60: {gen.prime_factorization(60)}")