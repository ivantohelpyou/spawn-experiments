"""
Test suite for prime number checking functionality.
Following TDD with comprehensive test validation.
"""
import unittest
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prime_generator import is_prime, InvalidInputError


class TestIsPrime(unittest.TestCase):
    """Test cases for the is_prime function with comprehensive validation."""

    def test_is_prime_with_known_primes(self):
        """Test that known prime numbers return True."""
        known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

        for prime in known_primes:
            with self.subTest(prime=prime):
                self.assertTrue(
                    is_prime(prime),
                    f"Expected {prime} to be identified as prime"
                )

    def test_is_prime_with_known_composites(self):
        """Test that known composite numbers return False."""
        known_composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28]

        for composite in known_composites:
            with self.subTest(composite=composite):
                self.assertFalse(
                    is_prime(composite),
                    f"Expected {composite} to be identified as composite"
                )

    def test_is_prime_edge_cases(self):
        """Test edge cases: 0, 1, and 2."""
        # 0 and 1 are not prime by definition
        self.assertFalse(is_prime(0), "0 should not be considered prime")
        self.assertFalse(is_prime(1), "1 should not be considered prime")

        # 2 is the only even prime
        self.assertTrue(is_prime(2), "2 should be identified as prime")

    def test_is_prime_with_negative_numbers(self):
        """Test that negative numbers are not considered prime."""
        negative_numbers = [-1, -2, -5, -10, -17]

        for negative in negative_numbers:
            with self.subTest(negative=negative):
                self.assertFalse(
                    is_prime(negative),
                    f"Negative number {negative} should not be prime"
                )

    def test_is_prime_with_large_prime(self):
        """Test with a larger known prime number."""
        large_prime = 997  # Known prime
        self.assertTrue(is_prime(large_prime), f"{large_prime} should be identified as prime")

    def test_is_prime_with_large_composite(self):
        """Test with a larger known composite number."""
        large_composite = 1000  # 1000 = 2^3 * 5^3
        self.assertFalse(is_prime(large_composite), f"{large_composite} should be identified as composite")

    def test_is_prime_with_perfect_squares(self):
        """Test that perfect squares (except 1) are correctly identified as composite."""
        perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]

        for square in perfect_squares:
            with self.subTest(square=square):
                self.assertFalse(
                    is_prime(square),
                    f"Perfect square {square} should be identified as composite"
                )

    def test_is_prime_input_validation(self):
        """Test that invalid inputs raise appropriate errors."""
        # Test non-integer inputs
        invalid_inputs = [3.14, "5", None, [], {}]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(InvalidInputError):
                    is_prime(invalid_input)


if __name__ == "__main__":
    unittest.main(verbosity=2)