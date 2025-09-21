"""
Prime number validation functionality for the Prime Number Generator application.

This module provides comprehensive validation capabilities for single numbers
and batch validation of multiple numbers.
"""

import time
from typing import List, Optional
from dataclasses import dataclass
try:
    from ..utils.exceptions import InvalidNumberError, InvalidInputError
    from ..utils.helpers import validate_non_negative_integer, get_prime_factors
except ImportError:
    from utils.exceptions import InvalidNumberError, InvalidInputError
    from utils.helpers import validate_non_negative_integer, get_prime_factors


@dataclass
class ValidationResult:
    """Result of prime number validation."""
    number: int
    is_prime: bool
    factors: Optional[List[int]]
    execution_time: float
    explanation: str


class PrimeValidator:
    """
    Comprehensive prime number validator with detailed results.

    This class provides validation for single numbers with detailed
    explanations and performance metrics.
    """

    def __init__(self):
        self.algorithm_name = "Optimized Trial Division"

    def validate(self, number: int, include_factors: bool = True) -> ValidationResult:
        """
        Validate if a number is prime with detailed analysis.

        Args:
            number: Number to validate
            include_factors: Whether to include prime factors for composite numbers

        Returns:
            ValidationResult with detailed information

        Raises:
            InvalidNumberError: If number is invalid
        """
        try:
            num = validate_non_negative_integer(number, "number")
        except InvalidInputError as e:
            raise InvalidNumberError(str(e))

        start_time = time.perf_counter()

        # Check primality
        is_prime = self._is_prime_optimized(num)

        execution_time = time.perf_counter() - start_time

        # Generate explanation and factors
        explanation = self._generate_explanation(num, is_prime)
        factors = None

        if not is_prime and include_factors and num > 1:
            factors = get_prime_factors(num)

        return ValidationResult(
            number=num,
            is_prime=is_prime,
            factors=factors,
            execution_time=execution_time,
            explanation=explanation
        )

    def _is_prime_optimized(self, n: int) -> bool:
        """
        Optimized primality test using trial division.

        Args:
            n: Number to test

        Returns:
            True if n is prime, False otherwise
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        # Check odd divisors up to sqrt(n)
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2

        return True

    def _generate_explanation(self, number: int, is_prime: bool) -> str:
        """
        Generate detailed explanation for the validation result.

        Args:
            number: The number that was tested
            is_prime: Whether the number is prime

        Returns:
            Human-readable explanation
        """
        if number < 0:
            return f"{number} is negative. Prime numbers are positive integers greater than 1."

        if number == 0:
            return "0 is not prime. Prime numbers are positive integers greater than 1."

        if number == 1:
            return "1 is not prime by definition. Prime numbers have exactly two divisors: 1 and themselves."

        if number == 2:
            return "2 is prime. It is the only even prime number."

        if number % 2 == 0:
            return f"{number} is even and greater than 2, so it is divisible by 2 and therefore not prime."

        if is_prime:
            return f"{number} is prime. It has no positive divisors other than 1 and {number}."
        else:
            # Find the smallest factor for explanation
            for i in range(3, int(number**0.5) + 1, 2):
                if number % i == 0:
                    return f"{number} is not prime. It is divisible by {i} (and {number // i})."

        return f"{number} is not prime."


class BatchValidator:
    """
    Batch validation for multiple numbers with performance optimization.

    This class efficiently validates multiple numbers and provides
    summary statistics and performance metrics.
    """

    def __init__(self, max_batch_size: int = 10000):
        self.validator = PrimeValidator()
        self.max_batch_size = max_batch_size

    def validate_batch(self, numbers: List[int], include_factors: bool = False) -> List[ValidationResult]:
        """
        Validate multiple numbers in batch.

        Args:
            numbers: List of numbers to validate
            include_factors: Whether to include factors for composite numbers

        Returns:
            List of ValidationResult objects

        Raises:
            InvalidInputError: If batch size exceeds limit
        """
        if len(numbers) > self.max_batch_size:
            raise InvalidInputError(
                f"Batch size ({len(numbers)}) exceeds maximum ({self.max_batch_size})"
            )

        results = []
        for number in numbers:
            try:
                result = self.validator.validate(number, include_factors)
                results.append(result)
            except InvalidNumberError:
                # Create error result for invalid numbers
                results.append(ValidationResult(
                    number=number,
                    is_prime=False,
                    factors=None,
                    execution_time=0.0,
                    explanation=f"Invalid input: {number}"
                ))

        return results

    def get_batch_summary(self, results: List[ValidationResult]) -> dict:
        """
        Generate summary statistics for batch validation results.

        Args:
            results: List of validation results

        Returns:
            Dictionary with summary statistics
        """
        total_numbers = len(results)
        prime_count = sum(1 for r in results if r.is_prime)
        composite_count = sum(1 for r in results if not r.is_prime and r.number > 1)
        invalid_count = sum(1 for r in results if r.number <= 1)

        total_time = sum(r.execution_time for r in results)
        avg_time = total_time / total_numbers if total_numbers > 0 else 0

        valid_results = [r for r in results if r.number > 1]
        if valid_results:
            fastest_time = min(r.execution_time for r in valid_results)
            slowest_time = max(r.execution_time for r in valid_results)
            largest_prime = max((r.number for r in valid_results if r.is_prime), default=None)
            largest_composite = max((r.number for r in valid_results if not r.is_prime), default=None)
        else:
            fastest_time = slowest_time = 0
            largest_prime = largest_composite = None

        return {
            'total_numbers': total_numbers,
            'prime_count': prime_count,
            'composite_count': composite_count,
            'invalid_count': invalid_count,
            'prime_percentage': (prime_count / total_numbers * 100) if total_numbers > 0 else 0,
            'total_execution_time': total_time,
            'average_execution_time': avg_time,
            'fastest_execution_time': fastest_time,
            'slowest_execution_time': slowest_time,
            'largest_prime': largest_prime,
            'largest_composite': largest_composite
        }

    def validate_range(self, start: int, end: int, include_factors: bool = False) -> List[ValidationResult]:
        """
        Validate all numbers in a given range.

        Args:
            start: Range start (inclusive)
            end: Range end (inclusive)
            include_factors: Whether to include factors for composite numbers

        Returns:
            List of ValidationResult objects

        Raises:
            InvalidInputError: If range is too large
        """
        start = validate_non_negative_integer(start, "start")
        end = validate_non_negative_integer(end, "end")

        if start > end:
            raise InvalidInputError(f"Start ({start}) must be <= end ({end})")

        range_size = end - start + 1
        if range_size > self.max_batch_size:
            raise InvalidInputError(
                f"Range size ({range_size}) exceeds maximum batch size ({self.max_batch_size})"
            )

        numbers = list(range(start, end + 1))
        return self.validate_batch(numbers, include_factors)


def quick_prime_check(number: int) -> bool:
    """
    Quick prime check function for simple use cases.

    Args:
        number: Number to check

    Returns:
        True if number is prime, False otherwise
    """
    validator = PrimeValidator()
    try:
        result = validator.validate(number, include_factors=False)
        return result.is_prime
    except InvalidNumberError:
        return False


def validate_prime_list(numbers: List[int]) -> dict:
    """
    Validate a list of numbers and return summary.

    Args:
        numbers: List of numbers to validate

    Returns:
        Dictionary with validation summary
    """
    batch_validator = BatchValidator()
    results = batch_validator.validate_batch(numbers, include_factors=False)
    return batch_validator.get_batch_summary(results)