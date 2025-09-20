"""
Prime number generation algorithms for the Prime Number Generator application.

This module implements various algorithms for generating and working with
prime numbers, including the Sieve of Eratosthenes and Trial Division methods.
"""

import math
from typing import List, Generator, Optional, Tuple
from dataclasses import dataclass
try:
    from ..utils.exceptions import InvalidLimitError, InvalidRangeError, AlgorithmError
    from ..utils.helpers import validate_positive_integer, validate_non_negative_integer, estimate_sieve_memory
except ImportError:
    from utils.exceptions import InvalidLimitError, InvalidRangeError, AlgorithmError
    from utils.helpers import validate_positive_integer, validate_non_negative_integer, estimate_sieve_memory


@dataclass
class AlgorithmConfig:
    """Configuration for prime generation algorithms."""
    name: str
    description: str
    optimal_range: Tuple[int, int]
    memory_efficient: bool
    time_complexity: str
    space_complexity: str


class SieveOfEratosthenes:
    """
    Implementation of the Sieve of Eratosthenes algorithm.

    This algorithm is highly efficient for generating all prime numbers
    up to a given limit, with time complexity O(n log log n).
    """

    def __init__(self):
        self.config = AlgorithmConfig(
            name="Sieve of Eratosthenes",
            description="Efficient algorithm for finding all primes up to a limit",
            optimal_range=(1000, 10_000_000),
            memory_efficient=False,
            time_complexity="O(n log log n)",
            space_complexity="O(n)"
        )

    def generate_primes_up_to(self, limit: int) -> List[int]:
        """
        Generate all prime numbers up to the given limit.

        Args:
            limit: Upper limit (inclusive)

        Returns:
            List of prime numbers up to limit

        Raises:
            InvalidLimitError: If limit is invalid
        """
        limit = validate_non_negative_integer(limit, "limit")

        if limit < 2:
            return []

        # Estimate memory usage and warn if excessive
        estimated_memory = estimate_sieve_memory(limit)
        if estimated_memory > 1_000_000_000:  # 1GB limit
            raise AlgorithmError(f"Estimated memory usage ({estimated_memory} bytes) exceeds limit")

        # Create boolean array "prime[0..limit]" and initialize all entries as True
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
        return [i for i in range(2, limit + 1) if prime[i]]

    def generate_primes_in_range(self, start: int, end: int) -> List[int]:
        """
        Generate prime numbers within a given range.

        Args:
            start: Range start (inclusive)
            end: Range end (inclusive)

        Returns:
            List of prime numbers in range

        Raises:
            InvalidRangeError: If range is invalid
        """
        start = validate_non_negative_integer(start, "start")
        end = validate_non_negative_integer(end, "end")

        if start > end:
            raise InvalidRangeError(f"Start ({start}) must be <= end ({end})")

        if end < 2:
            return []

        # Generate all primes up to end, then filter by range
        all_primes = self.generate_primes_up_to(end)
        return [p for p in all_primes if p >= start]


class TrialDivision:
    """
    Implementation of the Trial Division algorithm.

    This algorithm tests divisibility by all numbers up to sqrt(n).
    Simple but less efficient for large ranges.
    """

    def __init__(self):
        self.config = AlgorithmConfig(
            name="Trial Division",
            description="Simple algorithm testing divisibility",
            optimal_range=(1, 1000),
            memory_efficient=True,
            time_complexity="O(sqrt(n)) per number",
            space_complexity="O(1)"
        )

    def is_prime(self, n: int) -> bool:
        """
        Check if a number is prime using trial division.

        Args:
            n: Number to test

        Returns:
            True if n is prime, False otherwise
        """
        n = validate_non_negative_integer(n, "n")

        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        # Check odd divisors up to sqrt(n)
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False

        return True

    def generate_primes_up_to(self, limit: int) -> List[int]:
        """
        Generate all prime numbers up to the given limit using trial division.

        Args:
            limit: Upper limit (inclusive)

        Returns:
            List of prime numbers up to limit
        """
        limit = validate_non_negative_integer(limit, "limit")

        if limit < 2:
            return []

        primes = []
        for num in range(2, limit + 1):
            if self.is_prime(num):
                primes.append(num)

        return primes

    def generate_primes_in_range(self, start: int, end: int) -> List[int]:
        """
        Generate prime numbers within a given range using trial division.

        Args:
            start: Range start (inclusive)
            end: Range end (inclusive)

        Returns:
            List of prime numbers in range
        """
        start = validate_non_negative_integer(start, "start")
        end = validate_non_negative_integer(end, "end")

        if start > end:
            raise InvalidRangeError(f"Start ({start}) must be <= end ({end})")

        primes = []
        for num in range(max(2, start), end + 1):
            if self.is_prime(num):
                primes.append(num)

        return primes


class OptimizedTrialDivision:
    """
    Optimized version of Trial Division algorithm.

    This implementation includes several optimizations:
    - Early termination for even numbers
    - Testing only odd divisors
    - Caching small primes for faster testing
    """

    def __init__(self):
        self.config = AlgorithmConfig(
            name="Optimized Trial Division",
            description="Enhanced trial division with optimizations",
            optimal_range=(100, 100_000),
            memory_efficient=True,
            time_complexity="O(sqrt(n)) per number",
            space_complexity="O(sqrt(n))"
        )
        # Cache small primes for faster testing
        self._small_primes = self._generate_small_primes(1000)

    def _generate_small_primes(self, limit: int) -> List[int]:
        """Generate small primes for caching."""
        sieve = SieveOfEratosthenes()
        return sieve.generate_primes_up_to(limit)

    def is_prime(self, n: int) -> bool:
        """
        Check if a number is prime using optimized trial division.

        Args:
            n: Number to test

        Returns:
            True if n is prime, False otherwise
        """
        n = validate_non_negative_integer(n, "n")

        if n < 2:
            return False
        if n in self._small_primes:
            return True
        if n % 2 == 0:
            return False

        # Test divisibility by cached small primes
        sqrt_n = int(math.sqrt(n))
        for prime in self._small_primes:
            if prime > sqrt_n:
                break
            if n % prime == 0:
                return False

        # If we've tested all small primes, continue with remaining odd numbers
        start = self._small_primes[-1] + 2 if self._small_primes else 3
        for i in range(start, sqrt_n + 1, 2):
            if n % i == 0:
                return False

        return True

    def generate_primes_up_to(self, limit: int) -> List[int]:
        """
        Generate all prime numbers up to the given limit.

        Args:
            limit: Upper limit (inclusive)

        Returns:
            List of prime numbers up to limit
        """
        limit = validate_non_negative_integer(limit, "limit")

        if limit < 2:
            return []

        primes = []
        for num in range(2, limit + 1):
            if self.is_prime(num):
                primes.append(num)

        return primes

    def generate_primes_in_range(self, start: int, end: int) -> List[int]:
        """
        Generate prime numbers within a given range.

        Args:
            start: Range start (inclusive)
            end: Range end (inclusive)

        Returns:
            List of prime numbers in range
        """
        start = validate_non_negative_integer(start, "start")
        end = validate_non_negative_integer(end, "end")

        if start > end:
            raise InvalidRangeError(f"Start ({start}) must be <= end ({end})")

        primes = []
        for num in range(max(2, start), end + 1):
            if self.is_prime(num):
                primes.append(num)

        return primes


class PrimeGenerator:
    """
    Unified interface for prime number generation using multiple algorithms.

    This class automatically selects the most appropriate algorithm based
    on the input parameters and provides a consistent interface.
    """

    def __init__(self):
        self.sieve = SieveOfEratosthenes()
        self.trial_division = TrialDivision()
        self.optimized_trial = OptimizedTrialDivision()

    def select_algorithm(self, operation_type: str, limit: Optional[int] = None,
                        range_size: Optional[int] = None) -> str:
        """
        Select the most appropriate algorithm based on parameters.

        Args:
            operation_type: Type of operation ('generate', 'validate', 'range')
            limit: Upper limit for generation
            range_size: Size of range for generation

        Returns:
            Name of selected algorithm
        """
        if operation_type == 'validate':
            return 'optimized_trial'

        if limit is not None:
            if limit <= 1000:
                return 'trial_division'
            elif limit <= 100_000:
                return 'optimized_trial'
            else:
                return 'sieve'

        if range_size is not None:
            if range_size <= 1000:
                return 'optimized_trial'
            else:
                return 'sieve'

        return 'optimized_trial'  # Default

    def generate_primes_up_to(self, limit: int, algorithm: str = 'auto') -> List[int]:
        """
        Generate all prime numbers up to the given limit.

        Args:
            limit: Upper limit (inclusive)
            algorithm: Algorithm to use ('auto', 'sieve', 'trial', 'optimized_trial')

        Returns:
            List of prime numbers up to limit
        """
        if algorithm == 'auto':
            algorithm = self.select_algorithm('generate', limit=limit)

        if algorithm == 'sieve':
            return self.sieve.generate_primes_up_to(limit)
        elif algorithm == 'trial_division':
            return self.trial_division.generate_primes_up_to(limit)
        elif algorithm == 'optimized_trial':
            return self.optimized_trial.generate_primes_up_to(limit)
        else:
            raise AlgorithmError(f"Unknown algorithm: {algorithm}")

    def generate_first_n_primes(self, count: int, algorithm: str = 'auto') -> List[int]:
        """
        Generate the first N prime numbers.

        Args:
            count: Number of primes to generate
            algorithm: Algorithm to use

        Returns:
            List of first N prime numbers
        """
        count = validate_positive_integer(count, "count")

        # Estimate upper bound for nth prime
        try:
            from ..utils.helpers import calculate_nth_prime_upper_bound
        except ImportError:
            from utils.helpers import calculate_nth_prime_upper_bound
        estimated_limit = calculate_nth_prime_upper_bound(count)

        if algorithm == 'auto':
            algorithm = self.select_algorithm('generate', limit=estimated_limit)

        # Generate primes up to estimated limit and take first N
        primes = self.generate_primes_up_to(estimated_limit, algorithm)

        if len(primes) >= count:
            return primes[:count]

        # If estimate was too low, expand the search
        multiplier = 2
        while len(primes) < count:
            expanded_limit = estimated_limit * multiplier
            primes = self.generate_primes_up_to(expanded_limit, algorithm)
            multiplier += 1

            # Safety check to prevent infinite loops
            if multiplier > 10:
                raise AlgorithmError(f"Could not find {count} primes within reasonable limits")

        return primes[:count]

    def generate_primes_in_range(self, start: int, end: int, algorithm: str = 'auto') -> List[int]:
        """
        Generate prime numbers within a given range.

        Args:
            start: Range start (inclusive)
            end: Range end (inclusive)
            algorithm: Algorithm to use

        Returns:
            List of prime numbers in range
        """
        start = validate_non_negative_integer(start, "start")
        end = validate_non_negative_integer(end, "end")

        if start > end:
            raise InvalidRangeError(f"Start ({start}) must be <= end ({end})")

        range_size = end - start + 1

        if algorithm == 'auto':
            algorithm = self.select_algorithm('range', range_size=range_size)

        if algorithm == 'sieve':
            return self.sieve.generate_primes_in_range(start, end)
        elif algorithm == 'trial_division':
            return self.trial_division.generate_primes_in_range(start, end)
        elif algorithm == 'optimized_trial':
            return self.optimized_trial.generate_primes_in_range(start, end)
        else:
            raise AlgorithmError(f"Unknown algorithm: {algorithm}")

    def is_prime(self, n: int) -> bool:
        """
        Check if a number is prime.

        Args:
            n: Number to test

        Returns:
            True if n is prime, False otherwise
        """
        return self.optimized_trial.is_prime(n)

    def get_available_algorithms(self) -> List[AlgorithmConfig]:
        """
        Get information about available algorithms.

        Returns:
            List of algorithm configurations
        """
        return [
            self.sieve.config,
            self.trial_division.config,
            self.optimized_trial.config
        ]