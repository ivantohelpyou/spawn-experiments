"""Unit tests for core prime checking functionality"""

import unittest
import sys
import os

# Add the parent directory to the path to import prime_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prime_generator.core import PrimeChecker
from prime_generator.exceptions import InvalidInputError


class TestPrimeChecker(unittest.TestCase):
    """Test cases for PrimeChecker class"""

    def test_is_prime_with_small_primes(self):
        """Test that small prime numbers are correctly identified as prime"""
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for prime in small_primes:
            with self.subTest(prime=prime):
                self.assertTrue(PrimeChecker.is_prime(prime),
                              f"{prime} should be identified as prime")

    def test_is_prime_with_composite_numbers(self):
        """Test that composite numbers are correctly identified as non-prime"""
        composite_numbers = [4, 6, 8, 9, 10, 12, 15, 16, 18, 20]
        for composite in composite_numbers:
            with self.subTest(composite=composite):
                self.assertFalse(PrimeChecker.is_prime(composite),
                               f"{composite} should be identified as composite")

    def test_is_prime_edge_cases(self):
        """Test edge cases: 0, 1, and 2"""
        self.assertFalse(PrimeChecker.is_prime(0), "0 should not be prime")
        self.assertFalse(PrimeChecker.is_prime(1), "1 should not be prime")
        self.assertTrue(PrimeChecker.is_prime(2), "2 should be prime")

    def test_is_prime_with_large_prime(self):
        """Test with a large prime number"""
        self.assertTrue(PrimeChecker.is_prime(97), "97 should be prime")
        self.assertTrue(PrimeChecker.is_prime(997), "997 should be prime")

    def test_is_prime_with_large_composite(self):
        """Test with large composite numbers"""
        self.assertFalse(PrimeChecker.is_prime(100), "100 should not be prime")
        self.assertFalse(PrimeChecker.is_prime(999), "999 should not be prime")

    def test_is_prime_raises_error_for_negative_numbers(self):
        """Test that negative numbers raise ValueError"""
        with self.assertRaises(ValueError):
            PrimeChecker.is_prime(-1)
        with self.assertRaises(ValueError):
            PrimeChecker.is_prime(-10)

    def test_is_prime_raises_error_for_non_integers(self):
        """Test that non-integer inputs raise TypeError"""
        with self.assertRaises(TypeError):
            PrimeChecker.is_prime(3.14)
        with self.assertRaises(TypeError):
            PrimeChecker.is_prime("5")
        with self.assertRaises(TypeError):
            PrimeChecker.is_prime(None)


if __name__ == '__main__':
    unittest.main()