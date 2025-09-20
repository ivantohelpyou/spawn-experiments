"""Unit tests for prime number generation functionality"""

import unittest
import sys
import os

# Add the parent directory to the path to import prime_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prime_generator.generator import PrimeGenerator


class TestPrimeGenerator(unittest.TestCase):
    """Test cases for PrimeGenerator class"""

    def test_generate_up_to_small_limit(self):
        """Test generating primes up to a small limit"""
        result = PrimeGenerator.generate_up_to(10)
        expected = [2, 3, 5, 7]
        self.assertEqual(result, expected, "Should generate primes [2, 3, 5, 7] for limit 10")

    def test_generate_up_to_limit_2(self):
        """Test generating primes up to limit 2"""
        result = PrimeGenerator.generate_up_to(2)
        expected = [2]
        self.assertEqual(result, expected, "Should generate [2] for limit 2")

    def test_generate_up_to_limit_1(self):
        """Test generating primes up to limit 1"""
        result = PrimeGenerator.generate_up_to(1)
        expected = []
        self.assertEqual(result, expected, "Should generate empty list for limit 1")

    def test_generate_up_to_limit_0(self):
        """Test generating primes up to limit 0"""
        result = PrimeGenerator.generate_up_to(0)
        expected = []
        self.assertEqual(result, expected, "Should generate empty list for limit 0")

    def test_generate_up_to_larger_limit(self):
        """Test generating primes up to a larger limit"""
        result = PrimeGenerator.generate_up_to(30)
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertEqual(result, expected, "Should generate correct primes up to 30")

    def test_generate_up_to_raises_error_for_negative_limit(self):
        """Test that negative limit raises ValueError"""
        with self.assertRaises(ValueError):
            PrimeGenerator.generate_up_to(-1)
        with self.assertRaises(ValueError):
            PrimeGenerator.generate_up_to(-10)

    def test_generate_up_to_raises_error_for_non_integer(self):
        """Test that non-integer limit raises TypeError"""
        with self.assertRaises(TypeError):
            PrimeGenerator.generate_up_to(10.5)
        with self.assertRaises(TypeError):
            PrimeGenerator.generate_up_to("10")
        with self.assertRaises(TypeError):
            PrimeGenerator.generate_up_to(None)

    def test_generate_in_range_basic(self):
        """Test generating primes in a basic range"""
        result = PrimeGenerator.generate_in_range(10, 20)
        expected = [11, 13, 17, 19]
        self.assertEqual(result, expected, "Should generate primes [11, 13, 17, 19] in range [10, 20]")

    def test_generate_in_range_single_prime(self):
        """Test generating primes in range containing single prime"""
        result = PrimeGenerator.generate_in_range(7, 7)
        expected = [7]
        self.assertEqual(result, expected, "Should generate [7] for range [7, 7]")

    def test_generate_in_range_no_primes(self):
        """Test generating primes in range with no primes"""
        result = PrimeGenerator.generate_in_range(8, 10)
        expected = []
        self.assertEqual(result, expected, "Should generate empty list for range [8, 10]")

    def test_generate_in_range_start_greater_than_end(self):
        """Test that start > end raises ValueError"""
        with self.assertRaises(ValueError):
            PrimeGenerator.generate_in_range(10, 5)

    def test_generate_in_range_negative_values(self):
        """Test that negative values raise ValueError"""
        with self.assertRaises(ValueError):
            PrimeGenerator.generate_in_range(-5, 10)
        with self.assertRaises(ValueError):
            PrimeGenerator.generate_in_range(5, -10)

    def test_nth_prime_first_few(self):
        """Test finding first few prime numbers by position"""
        self.assertEqual(PrimeGenerator.nth_prime(1), 2, "1st prime should be 2")
        self.assertEqual(PrimeGenerator.nth_prime(2), 3, "2nd prime should be 3")
        self.assertEqual(PrimeGenerator.nth_prime(3), 5, "3rd prime should be 5")
        self.assertEqual(PrimeGenerator.nth_prime(4), 7, "4th prime should be 7")
        self.assertEqual(PrimeGenerator.nth_prime(5), 11, "5th prime should be 11")

    def test_nth_prime_larger_values(self):
        """Test finding larger nth primes"""
        self.assertEqual(PrimeGenerator.nth_prime(10), 29, "10th prime should be 29")
        self.assertEqual(PrimeGenerator.nth_prime(25), 97, "25th prime should be 97")

    def test_nth_prime_invalid_input(self):
        """Test that invalid n values raise ValueError"""
        with self.assertRaises(ValueError):
            PrimeGenerator.nth_prime(0)
        with self.assertRaises(ValueError):
            PrimeGenerator.nth_prime(-1)

    def test_nth_prime_non_integer(self):
        """Test that non-integer n raises TypeError"""
        with self.assertRaises(TypeError):
            PrimeGenerator.nth_prime(5.5)
        with self.assertRaises(TypeError):
            PrimeGenerator.nth_prime("5")


if __name__ == '__main__':
    unittest.main()