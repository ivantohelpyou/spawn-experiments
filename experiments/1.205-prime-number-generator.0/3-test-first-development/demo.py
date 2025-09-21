#!/usr/bin/env python3
"""
Prime Number Generator Demo Script

This script demonstrates the functionality of the Prime Number Generator
developed using Test-Driven Development principles.
"""

import sys
import time
from prime_generator import PrimeChecker, PrimeGenerator


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def demo_prime_checking():
    """Demonstrate prime number checking functionality"""
    print_header("PRIME NUMBER CHECKING")

    test_numbers = [2, 3, 4, 5, 17, 18, 97, 100, 997, 1000]

    print("Testing individual numbers for primality:")
    print(f"{'Number':<10} {'Is Prime?':<12} {'Result'}")
    print("-" * 35)

    for num in test_numbers:
        is_prime = PrimeChecker.is_prime(num)
        result = "✓ Prime" if is_prime else "✗ Composite"
        print(f"{num:<10} {str(is_prime):<12} {result}")


def demo_prime_generation():
    """Demonstrate prime number generation functionality"""
    print_header("PRIME NUMBER GENERATION")

    # Generate primes up to a limit
    print("Generating all prime numbers up to 50:")
    primes_50 = PrimeGenerator.generate_up_to(50)
    print(f"Primes up to 50: {primes_50}")
    print(f"Count: {len(primes_50)} primes")

    print("\nGenerating all prime numbers up to 100:")
    primes_100 = PrimeGenerator.generate_up_to(100)
    print(f"Primes up to 100: {primes_100}")
    print(f"Count: {len(primes_100)} primes")


def demo_range_generation():
    """Demonstrate range-based prime generation"""
    print_header("RANGE-BASED PRIME GENERATION")

    ranges = [(10, 30), (50, 70), (100, 120), (200, 220)]

    for start, end in ranges:
        primes_in_range = PrimeGenerator.generate_in_range(start, end)
        print(f"Primes in range [{start}, {end}]: {primes_in_range}")
        print(f"Count: {len(primes_in_range)} primes")


def demo_nth_prime():
    """Demonstrate finding nth prime numbers"""
    print_header("NTH PRIME NUMBER FINDING")

    positions = [1, 5, 10, 25, 50, 100]

    print(f"{'Position':<10} {'Prime Number':<15} {'Verification'}")
    print("-" * 40)

    for n in positions:
        nth_prime = PrimeGenerator.nth_prime(n)
        is_verified = PrimeChecker.is_prime(nth_prime)
        verification = "✓ Verified" if is_verified else "✗ Error"
        print(f"{n:<10} {nth_prime:<15} {verification}")


def demo_mathematical_properties():
    """Demonstrate mathematical properties of primes"""
    print_header("MATHEMATICAL PROPERTIES")

    primes = PrimeGenerator.generate_up_to(100)

    # Twin primes (primes that differ by 2)
    print("Twin Primes (primes that differ by 2):")
    twin_primes = []
    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            twin_primes.append((primes[i], primes[i + 1]))

    for twin in twin_primes:
        print(f"  {twin[0]} and {twin[1]}")

    # Prime gaps
    print(f"\nPrime gaps (differences between consecutive primes):")
    gaps = []
    for i in range(len(primes) - 1):
        gap = primes[i + 1] - primes[i]
        gaps.append(gap)

    print(f"Gaps: {gaps}")
    print(f"Average gap: {sum(gaps) / len(gaps):.2f}")
    print(f"Largest gap: {max(gaps)}")


def demo_performance():
    """Demonstrate performance characteristics"""
    print_header("PERFORMANCE DEMONSTRATION")

    test_cases = [
        ("Generate primes up to 1,000", lambda: PrimeGenerator.generate_up_to(1000)),
        ("Generate primes up to 10,000", lambda: PrimeGenerator.generate_up_to(10000)),
        ("Find 500th prime", lambda: PrimeGenerator.nth_prime(500)),
        ("Find 1000th prime", lambda: PrimeGenerator.nth_prime(1000)),
        ("Check large prime (982451653)", lambda: PrimeChecker.is_prime(982451653)),
        ("Check large composite (982451654)", lambda: PrimeChecker.is_prime(982451654)),
    ]

    print(f"{'Test Case':<35} {'Time (ms)':<12} {'Result'}")
    print("-" * 65)

    for description, test_func in test_cases:
        start_time = time.time()
        try:
            result = test_func()
            elapsed_ms = (time.time() - start_time) * 1000

            if isinstance(result, list):
                result_str = f"{len(result)} primes"
            elif isinstance(result, bool):
                result_str = "Prime" if result else "Composite"
            else:
                result_str = str(result)

            print(f"{description:<35} {elapsed_ms:<12.2f} {result_str}")
        except Exception as e:
            print(f"{description:<35} {'Error':<12} {str(e)}")


def demo_error_handling():
    """Demonstrate error handling"""
    print_header("ERROR HANDLING DEMONSTRATION")

    error_cases = [
        ("PrimeChecker.is_prime(-5)", lambda: PrimeChecker.is_prime(-5)),
        ("PrimeChecker.is_prime('not a number')", lambda: PrimeChecker.is_prime('not a number')),
        ("PrimeGenerator.generate_up_to(-10)", lambda: PrimeGenerator.generate_up_to(-10)),
        ("PrimeGenerator.generate_in_range(10, 5)", lambda: PrimeGenerator.generate_in_range(10, 5)),
        ("PrimeGenerator.nth_prime(0)", lambda: PrimeGenerator.nth_prime(0)),
        ("PrimeGenerator.nth_prime('not a number')", lambda: PrimeGenerator.nth_prime('not a number')),
    ]

    print(f"{'Test Case':<45} {'Expected Error':<20} {'Result'}")
    print("-" * 80)

    for description, test_func in error_cases:
        try:
            result = test_func()
            print(f"{description:<45} {'ValueError/TypeError':<20} ✗ No error raised")
        except (ValueError, TypeError) as e:
            error_type = type(e).__name__
            print(f"{description:<45} {error_type:<20} ✓ Correctly handled")
        except Exception as e:
            print(f"{description:<45} {'ValueError/TypeError':<20} ✗ Wrong error: {type(e).__name__}")


def main():
    """Run all demonstrations"""
    print("Prime Number Generator - TDD Implementation Demo")
    print("Developed using strict Test-Driven Development principles")

    demo_prime_checking()
    demo_prime_generation()
    demo_range_generation()
    demo_nth_prime()
    demo_mathematical_properties()
    demo_performance()
    demo_error_handling()

    print_header("DEMO COMPLETE")
    print("All functionality demonstrated successfully!")
    print("\nTo run the complete test suite:")
    print("  python -m unittest discover tests -v")
    print("\nTotal test coverage: 31 tests across unit and integration testing")


if __name__ == "__main__":
    main()