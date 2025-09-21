#!/usr/bin/env python3
"""
Prime Number Generator - Main Application Entry Point

A comprehensive prime number generation and analysis application that provides
multiple algorithms, validation capabilities, and performance benchmarking.

This application implements:
- Multiple prime generation algorithms (Sieve of Eratosthenes, Trial Division, Optimized Trial Division)
- Prime number validation with detailed explanations
- Batch validation and analysis
- Performance monitoring and algorithm comparison
- Comprehensive command-line interface

Author: Claude Code
Version: 1.0.0
License: MIT

Usage:
    python main.py generate --limit 100
    python main.py validate 97
    python main.py benchmark --limit 10000
    python main.py algorithms

For detailed help:
    python main.py --help
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import main as cli_main
from core import PrimeGenerator, PrimeValidator
from utils import PrimeGeneratorError


def main():
    """
    Main entry point for the Prime Number Generator application.

    This function serves as the primary entry point and handles high-level
    error handling and application initialization.
    """
    try:
        # Run the CLI interface
        cli_main()

    except KeyboardInterrupt:
        print("\nApplication interrupted by user", file=sys.stderr)
        sys.exit(130)

    except PrimeGeneratorError as e:
        print(f"Prime Generator Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        print("Please report this issue if it persists.", file=sys.stderr)
        sys.exit(2)


def demo():
    """
    Demonstration function showing basic usage of the Prime Number Generator.

    This function can be called directly to see examples of the core
    functionality without using the CLI interface.
    """
    print("Prime Number Generator - Demonstration")
    print("=" * 40)

    # Initialize components
    generator = PrimeGenerator()
    validator = PrimeValidator()

    try:
        # Example 1: Generate primes up to 100
        print("\n1. Generating primes up to 100:")
        primes = generator.generate_primes_up_to(100)
        print(f"Found {len(primes)} primes: {primes}")

        # Example 2: Generate first 20 primes
        print("\n2. Generating first 20 primes:")
        first_20 = generator.generate_first_n_primes(20)
        print(f"First 20 primes: {first_20}")

        # Example 3: Generate primes in range
        print("\n3. Generating primes between 50 and 100:")
        range_primes = generator.generate_primes_in_range(50, 100)
        print(f"Primes in range: {range_primes}")

        # Example 4: Validate some numbers
        print("\n4. Validating some numbers:")
        test_numbers = [97, 98, 99, 100, 101]
        for num in test_numbers:
            result = validator.validate(num, include_factors=True)
            status = "PRIME" if result.is_prime else "NOT PRIME"
            print(f"{num}: {status} - {result.explanation}")
            if result.factors and len(result.factors) > 1:
                print(f"    Factors: {' × '.join(map(str, result.factors))}")

        # Example 5: Algorithm comparison
        print("\n5. Comparing algorithms for generating primes up to 1000:")
        from core import AlgorithmComparator
        comparator = AlgorithmComparator()

        algorithms = {
            'sieve': lambda: generator.generate_primes_up_to(1000, 'sieve'),
            'trial_division': lambda: generator.generate_primes_up_to(1000, 'trial_division'),
            'optimized_trial': lambda: generator.generate_primes_up_to(1000, 'optimized_trial')
        }

        comparison = comparator.compare_algorithms(algorithms, {'limit': 1000})
        print(f"Fastest algorithm: {comparison.fastest_algorithm}")
        print(f"Most memory efficient: {comparison.memory_efficient_algorithm}")

        print("\nDemonstration completed successfully!")

    except Exception as e:
        print(f"Error during demonstration: {e}", file=sys.stderr)


if __name__ == '__main__':
    # Check if demo mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        main()