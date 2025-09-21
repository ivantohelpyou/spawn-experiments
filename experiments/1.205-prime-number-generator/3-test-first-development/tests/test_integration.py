"""Integration tests for Prime Number Generator

Tests the interaction between PrimeChecker and PrimeGenerator classes,
and end-to-end workflows.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import prime_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prime_generator import PrimeChecker, PrimeGenerator


class TestPrimeGeneratorIntegration(unittest.TestCase):
    """Integration tests for the complete prime number generator system"""

    def test_core_and_generator_consistency(self):
        """Test that PrimeChecker and PrimeGenerator produce consistent results"""
        # Generate primes up to 50
        generated_primes = PrimeGenerator.generate_up_to(50)

        # Verify each generated number is indeed prime
        for prime in generated_primes:
            with self.subTest(prime=prime):
                self.assertTrue(PrimeChecker.is_prime(prime),
                              f"Generated number {prime} should be prime")

        # Verify no primes were missed by checking all numbers up to 50
        expected_primes = []
        for i in range(2, 51):
            if PrimeChecker.is_prime(i):
                expected_primes.append(i)

        self.assertEqual(generated_primes, expected_primes,
                        "Generated primes should match individually checked primes")

    def test_range_generation_with_prime_checking(self):
        """Test range generation and verify each result with prime checker"""
        primes_in_range = PrimeGenerator.generate_in_range(20, 40)
        expected_range_primes = [23, 29, 31, 37]

        self.assertEqual(primes_in_range, expected_range_primes,
                        "Should generate correct primes in range [20, 40]")

        # Verify each is prime
        for prime in primes_in_range:
            self.assertTrue(PrimeChecker.is_prime(prime),
                          f"{prime} should be verified as prime")

    def test_nth_prime_verification(self):
        """Test nth prime finding and verify results with prime checker"""
        test_cases = [
            (1, 2), (5, 11), (10, 29), (15, 47), (20, 71)
        ]

        for n, expected in test_cases:
            with self.subTest(n=n, expected=expected):
                nth_prime = PrimeGenerator.nth_prime(n)
                self.assertEqual(nth_prime, expected,
                               f"{n}th prime should be {expected}")
                self.assertTrue(PrimeChecker.is_prime(nth_prime),
                              f"nth prime {nth_prime} should verify as prime")

    def test_large_scale_consistency(self):
        """Test consistency between methods for larger numbers"""
        # Test that the 100th prime is correctly identified
        hundredth_prime = PrimeGenerator.nth_prime(100)
        self.assertEqual(hundredth_prime, 541, "100th prime should be 541")
        self.assertTrue(PrimeChecker.is_prime(hundredth_prime),
                       "100th prime should verify as prime")

        # Test that generating primes up to 541 includes exactly 100 primes
        primes_up_to_541 = PrimeGenerator.generate_up_to(541)
        self.assertEqual(len(primes_up_to_541), 100,
                        "Should have exactly 100 primes up to 541")
        self.assertEqual(primes_up_to_541[-1], 541,
                        "Last prime in list should be 541")

    def test_edge_case_workflows(self):
        """Test complete workflows with edge cases"""
        # Empty range case
        empty_range = PrimeGenerator.generate_in_range(14, 16)
        self.assertEqual(empty_range, [], "Should return empty list for range [14, 16]")

        # Single prime range
        single_prime = PrimeGenerator.generate_in_range(17, 17)
        self.assertEqual(single_prime, [17], "Should return [17] for range [17, 17]")
        self.assertTrue(PrimeChecker.is_prime(17), "17 should verify as prime")

        # First prime cases
        self.assertEqual(PrimeGenerator.nth_prime(1), 2, "1st prime should be 2")
        self.assertTrue(PrimeChecker.is_prime(2), "2 should verify as prime")

    def test_error_handling_consistency(self):
        """Test that both classes handle errors consistently"""
        # Test negative number handling
        with self.assertRaises(ValueError):
            PrimeChecker.is_prime(-5)
        with self.assertRaises(ValueError):
            PrimeGenerator.generate_up_to(-5)

        # Test type error handling
        with self.assertRaises(TypeError):
            PrimeChecker.is_prime("not a number")
        with self.assertRaises(TypeError):
            PrimeGenerator.nth_prime("not a number")

    def test_performance_regression(self):
        """Basic performance test to catch regressions"""
        import time

        # Test should complete quickly for reasonable input sizes
        start_time = time.time()

        # Generate first 50 primes
        primes = []
        for i in range(1, 51):
            primes.append(PrimeGenerator.nth_prime(i))

        # Verify all are prime
        for prime in primes:
            self.assertTrue(PrimeChecker.is_prime(prime))

        elapsed = time.time() - start_time
        self.assertLess(elapsed, 1.0, "Should complete within 1 second")

    def test_mathematical_properties(self):
        """Test mathematical properties of generated primes"""
        primes = PrimeGenerator.generate_up_to(100)

        # Test that 2 is the only even prime
        even_primes = [p for p in primes if p % 2 == 0]
        self.assertEqual(even_primes, [2], "2 should be the only even prime")

        # Test that all odd primes are indeed odd
        odd_primes = [p for p in primes if p > 2]
        for prime in odd_primes:
            self.assertEqual(prime % 2, 1, f"Prime {prime} > 2 should be odd")

        # Test twin primes (primes that differ by 2)
        twin_primes = []
        for i in range(len(primes) - 1):
            if primes[i + 1] - primes[i] == 2:
                twin_primes.append((primes[i], primes[i + 1]))

        # Should include (3,5), (5,7), (11,13), (17,19), (29,31), (41,43), (59,61), (71,73)
        expected_twins = [(3,5), (5,7), (11,13), (17,19), (29,31), (41,43), (59,61), (71,73)]
        for twin_pair in expected_twins:
            self.assertIn(twin_pair, twin_primes,
                         f"Twin prime pair {twin_pair} should be found")


if __name__ == '__main__':
    unittest.main()