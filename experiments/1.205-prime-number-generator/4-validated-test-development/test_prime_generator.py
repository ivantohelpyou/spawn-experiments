"""
Test suite for prime generation functionality.
Following TDD with comprehensive test validation.
"""
import unittest
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prime_generator import generate_primes, InvalidInputError


class TestGeneratePrimes(unittest.TestCase):
    """Test cases for the generate_primes function with comprehensive validation."""

    def test_generate_primes_small_limits(self):
        """Test prime generation for small limits with known results."""
        test_cases = [
            (2, [2]),
            (3, [2, 3]),
            (10, [2, 3, 5, 7]),
            (20, [2, 3, 5, 7, 11, 13, 17, 19]),
            (30, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        ]

        for limit, expected in test_cases:
            with self.subTest(limit=limit):
                result = generate_primes(limit)
                self.assertEqual(
                    result, expected,
                    f"generate_primes({limit}) returned {result}, expected {expected}"
                )

    def test_generate_primes_edge_cases(self):
        """Test edge cases for prime generation."""
        # Limit less than 2 should return empty list
        self.assertEqual(generate_primes(0), [], "generate_primes(0) should return empty list")
        self.assertEqual(generate_primes(1), [], "generate_primes(1) should return empty list")

        # Exactly 2 should return [2]
        self.assertEqual(generate_primes(2), [2], "generate_primes(2) should return [2]")

    def test_generate_primes_returns_list(self):
        """Test that function returns a list, not other iterable."""
        result = generate_primes(10)
        self.assertIsInstance(result, list, "generate_primes should return a list")

    def test_generate_primes_sorted_order(self):
        """Test that returned primes are in ascending order."""
        result = generate_primes(50)
        self.assertEqual(
            result, sorted(result),
            "Primes should be returned in ascending order"
        )

    def test_generate_primes_no_duplicates(self):
        """Test that returned list contains no duplicates."""
        result = generate_primes(50)
        self.assertEqual(
            len(result), len(set(result)),
            "Prime list should contain no duplicates"
        )

    def test_generate_primes_larger_limit(self):
        """Test prime generation for a larger limit."""
        result = generate_primes(100)
        expected_count = 25  # There are 25 primes <= 100
        self.assertEqual(
            len(result), expected_count,
            f"Expected {expected_count} primes <= 100, got {len(result)}"
        )

        # Check first few and last few primes
        self.assertEqual(result[:5], [2, 3, 5, 7, 11])
        self.assertEqual(result[-3:], [83, 89, 97])

    def test_generate_primes_all_results_are_prime(self):
        """Test that all returned numbers are actually prime."""
        from prime_generator import is_prime  # Import our tested function

        result = generate_primes(50)
        for num in result:
            with self.subTest(num=num):
                self.assertTrue(
                    is_prime(num),
                    f"Number {num} in result is not prime"
                )

    def test_generate_primes_completeness(self):
        """Test that all primes up to limit are included."""
        from prime_generator import is_prime  # Import our tested function

        limit = 30
        result = generate_primes(limit)

        # Check that no primes are missing
        for num in range(2, limit + 1):
            if is_prime(num):
                with self.subTest(num=num):
                    self.assertIn(
                        num, result,
                        f"Prime {num} missing from result for limit {limit}"
                    )

    def test_generate_primes_input_validation(self):
        """Test that invalid inputs raise appropriate errors."""
        # Test non-integer inputs
        invalid_inputs = [3.14, "5", None, [], {}]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(InvalidInputError):
                    generate_primes(invalid_input)

        # Test negative inputs
        with self.assertRaises(InvalidInputError):
            generate_primes(-5)

    def test_generate_primes_performance_smoke_test(self):
        """Smoke test for performance with larger input."""
        # This should complete quickly and not raise errors
        result = generate_primes(1000)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 150)  # Should be 168 primes <= 1000


if __name__ == "__main__":
    unittest.main(verbosity=2)