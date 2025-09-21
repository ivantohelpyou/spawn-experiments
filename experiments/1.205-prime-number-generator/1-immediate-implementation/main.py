#!/usr/bin/env python3
"""
Prime Number Generator - Main Entry Point

This is the main entry point for the Prime Number Generator application.
It supports both interactive CLI mode and command-line arguments for
batch operations and scripting.

Usage:
    python main.py                          # Interactive mode
    python main.py --check 17               # Check if 17 is prime
    python main.py --generate 100           # Generate primes up to 100
    python main.py --first 10               # First 10 primes
    python main.py --factorize 60           # Prime factorization of 60
    python main.py --benchmark 1000         # Benchmark algorithms up to 1000
"""

import sys
import argparse
from typing import List, Optional
from prime_generator import PrimeGenerator, timing_decorator
from cli_interface import PrimeGeneratorCLI


class PrimeGeneratorApp:
    """
    Main application class that handles both CLI and command-line argument modes.
    """

    def __init__(self):
        """Initialize the application."""
        self.generator = PrimeGenerator()

    def setup_argument_parser(self) -> argparse.ArgumentParser:
        """Set up command-line argument parser."""
        parser = argparse.ArgumentParser(
            description='Prime Number Generator - A comprehensive prime number toolkit',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s                        Start interactive mode
  %(prog)s --check 97             Check if 97 is prime
  %(prog)s --generate 100         Generate all primes up to 100
  %(prog)s --first 20             Generate first 20 primes
  %(prog)s --factorize 84         Find prime factorization of 84
  %(prog)s --next 50              Find next prime after 50
  %(prog)s --gaps 100             Analyze prime gaps up to 100
  %(prog)s --mersenne 13          Check if 2^13-1 is Mersenne prime
  %(prog)s --benchmark 1000       Benchmark algorithms up to 1000
  %(prog)s --batch 2,3,4,17,25    Check multiple numbers for primality

For more features and educational content, run without arguments
to enter interactive mode.
            """
        )

        # Main operation modes (mutually exclusive)
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            '--check', type=int, metavar='N',
            help='Check if number N is prime'
        )

        group.add_argument(
            '--generate', type=int, metavar='LIMIT',
            help='Generate all prime numbers up to LIMIT'
        )

        group.add_argument(
            '--first', type=int, metavar='COUNT',
            help='Generate first COUNT prime numbers'
        )

        group.add_argument(
            '--factorize', type=int, metavar='N',
            help='Find prime factorization of N'
        )

        group.add_argument(
            '--next', type=int, metavar='N',
            help='Find next prime number after N'
        )

        group.add_argument(
            '--previous', type=int, metavar='N',
            help='Find previous prime number before N'
        )

        group.add_argument(
            '--gaps', type=int, metavar='LIMIT',
            help='Analyze prime gaps up to LIMIT'
        )

        group.add_argument(
            '--mersenne', type=int, metavar='P',
            help='Check if 2^P-1 is a Mersenne prime'
        )

        group.add_argument(
            '--benchmark', type=int, metavar='LIMIT',
            help='Benchmark prime generation algorithms up to LIMIT'
        )

        group.add_argument(
            '--batch', type=str, metavar='NUMBERS',
            help='Check multiple numbers (comma-separated) for primality'
        )

        # Optional parameters
        parser.add_argument(
            '--method', choices=['basic', 'optimized', 'sieve', 'cached'],
            default='optimized',
            help='Algorithm method to use (default: optimized)'
        )

        parser.add_argument(
            '--format', choices=['list', 'grid', 'count'],
            default='list',
            help='Output format for prime lists (default: list)'
        )

        parser.add_argument(
            '--timing', action='store_true',
            help='Show execution timing information'
        )

        parser.add_argument(
            '--verbose', '-v', action='store_true',
            help='Verbose output with additional information'
        )

        parser.add_argument(
            '--version', action='version', version='Prime Number Generator 1.0'
        )

        return parser

    def format_primes_output(self, primes: List[int], format_type: str, verbose: bool = False):
        """Format prime number output according to specified format."""
        if not primes:
            print("No primes found.")
            return

        if format_type == 'count':
            print(f"Count: {len(primes)}")
            if verbose:
                print(f"Range: {primes[0]} to {primes[-1]}")
        elif format_type == 'grid':
            print(f"Prime numbers ({len(primes)} found):")
            for i, prime in enumerate(primes):
                print(f"{prime:6d}", end="")
                if (i + 1) % 10 == 0:
                    print()
            if len(primes) % 10 != 0:
                print()
        else:  # list format
            if len(primes) <= 50 or verbose:
                print(f"Primes: {primes}")
            else:
                print(f"First 10: {primes[:10]}")
                print(f"Last 10: {primes[-10:]}")
                print(f"Total count: {len(primes)}")

    def handle_check(self, number: int, method: str, timing: bool, verbose: bool):
        """Handle prime checking command."""
        if timing:
            @timing_decorator
            def check_with_timing():
                return self.generator.is_prime(number, method)
            result = check_with_timing()
        else:
            result = self.generator.is_prime(number, method)

        print(f"{number} is {'prime' if result else 'not prime'}")

        if verbose and result:
            prev_prime = self.generator.previous_prime(number)
            next_prime = self.generator.next_prime(number)
            print(f"Previous prime: {prev_prime}")
            print(f"Next prime: {next_prime}")

    def handle_generate(self, limit: int, method: str, format_type: str,
                       timing: bool, verbose: bool):
        """Handle prime generation up to limit."""
        if timing:
            @timing_decorator
            def generate_with_timing():
                return self.generator.generate_primes_up_to(limit, method)
            primes = generate_with_timing()
        else:
            primes = self.generator.generate_primes_up_to(limit, method)

        self.format_primes_output(primes, format_type, verbose)

    def handle_first_n(self, count: int, format_type: str, timing: bool, verbose: bool):
        """Handle generating first N primes."""
        if timing:
            @timing_decorator
            def generate_with_timing():
                return self.generator.generate_first_n_primes(count)
            primes = generate_with_timing()
        else:
            primes = self.generator.generate_first_n_primes(count)

        self.format_primes_output(primes, format_type, verbose)

        if verbose and primes:
            print(f"Largest prime: {primes[-1]}")

    def handle_factorize(self, number: int, timing: bool, verbose: bool):
        """Handle prime factorization."""
        if timing:
            @timing_decorator
            def factorize_with_timing():
                return self.generator.prime_factorization(number)
            factors = factorize_with_timing()
        else:
            factors = self.generator.prime_factorization(number)

        if not factors:
            print(f"{number} has no prime factors (number < 2)")
            return

        # Format factorization
        factor_strings = []
        for prime, power in factors:
            if power == 1:
                factor_strings.append(str(prime))
            else:
                factor_strings.append(f"{prime}^{power}")

        factorization = " × ".join(factor_strings)
        print(f"{number} = {factorization}")

        if verbose:
            # Verify the factorization
            product = 1
            for prime, power in factors:
                product *= prime ** power
            print(f"Verification: {product} = {number}")

    def handle_next_prime(self, number: int, verbose: bool):
        """Handle finding next prime."""
        next_prime = self.generator.next_prime(number)
        print(f"Next prime after {number}: {next_prime}")

        if verbose:
            gap = next_prime - number
            print(f"Gap: {gap}")

    def handle_previous_prime(self, number: int, verbose: bool):
        """Handle finding previous prime."""
        prev_prime = self.generator.previous_prime(number)
        if prev_prime:
            print(f"Previous prime before {number}: {prev_prime}")
            if verbose:
                gap = number - prev_prime
                print(f"Gap: {gap}")
        else:
            print(f"No prime number exists before {number}")

    def handle_gaps(self, limit: int, timing: bool, verbose: bool):
        """Handle prime gaps analysis."""
        if timing:
            @timing_decorator
            def analyze_with_timing():
                return self.generator.prime_gaps(limit)
            gaps = analyze_with_timing()
        else:
            gaps = self.generator.prime_gaps(limit)

        if not gaps:
            print("No gaps found (limit too small)")
            return

        gap_sizes = [gap for _, _, gap in gaps]
        print(f"Prime gaps up to {limit}:")
        print(f"Number of gaps: {len(gaps)}")
        print(f"Minimum gap: {min(gap_sizes)}")
        print(f"Maximum gap: {max(gap_sizes)}")
        print(f"Average gap: {sum(gap_sizes) / len(gap_sizes):.2f}")

        if verbose:
            # Show largest gaps
            gaps.sort(key=lambda x: x[2], reverse=True)
            print("\nLargest gaps:")
            for i, (p1, p2, gap) in enumerate(gaps[:5]):
                print(f"  {i+1}. {p1} → {p2} (gap: {gap})")

    def handle_mersenne(self, p: int, timing: bool, verbose: bool):
        """Handle Mersenne prime checking."""
        if not self.generator.is_prime(p):
            print(f"{p} is not prime, so 2^{p}-1 cannot be a Mersenne prime")
            return

        mersenne_number = (2 ** p) - 1

        if timing:
            @timing_decorator
            def check_with_timing():
                return self.generator.is_prime(mersenne_number)
            is_prime = check_with_timing()
        else:
            is_prime = self.generator.is_prime(mersenne_number)

        print(f"2^{p} - 1 = {mersenne_number}")
        print(f"Result: {'Mersenne prime' if is_prime else 'Not a Mersenne prime'}")

        if verbose:
            print(f"Number of digits: {len(str(mersenne_number))}")

    def handle_benchmark(self, limit: int, verbose: bool):
        """Handle performance benchmarking."""
        print(f"Benchmarking prime generation methods up to {limit}...")

        results = self.generator.benchmark_methods(limit)

        print("\nBenchmark Results:")
        print("-" * 50)
        for method, data in results.items():
            print(f"{method.capitalize():12s}: {data['time']:.4f}s ({data['count']} primes)")

        # Find fastest and slowest
        fastest = min(results.items(), key=lambda x: x[1]['time'])
        slowest = max(results.items(), key=lambda x: x[1]['time'])

        print(f"\nFastest: {fastest[0]} ({fastest[1]['time']:.4f}s)")

        if verbose:
            print(f"Slowest: {slowest[0]} ({slowest[1]['time']:.4f}s)")
            speedup = slowest[1]['time'] / fastest[1]['time']
            print(f"Speedup: {speedup:.1f}x faster")

    def handle_batch(self, numbers_str: str, method: str, verbose: bool):
        """Handle batch prime checking."""
        try:
            # Parse comma-separated numbers
            numbers = [int(x.strip()) for x in numbers_str.split(',') if x.strip()]
        except ValueError:
            print("Error: Invalid number format in batch list")
            return

        if not numbers:
            print("No valid numbers provided")
            return

        print(f"Checking {len(numbers)} numbers for primality...")
        print("-" * 40)

        prime_count = 0
        primes_found = []

        for num in numbers:
            is_prime = self.generator.is_prime(num, method)
            status = "Prime" if is_prime else "Composite"
            print(f"{num:8d}: {status}")

            if is_prime:
                prime_count += 1
                primes_found.append(num)

        print("-" * 40)
        print(f"Summary: {prime_count}/{len(numbers)} numbers are prime")

        if verbose and primes_found:
            print(f"Primes found: {primes_found}")

    def run_command_line(self, args):
        """Run application in command-line mode."""
        try:
            if args.check is not None:
                self.handle_check(args.check, args.method, args.timing, args.verbose)

            elif args.generate is not None:
                method = args.method if args.method != 'cached' else 'sieve'
                self.handle_generate(args.generate, method, args.format,
                                   args.timing, args.verbose)

            elif args.first is not None:
                self.handle_first_n(args.first, args.format, args.timing, args.verbose)

            elif args.factorize is not None:
                self.handle_factorize(args.factorize, args.timing, args.verbose)

            elif args.next is not None:
                self.handle_next_prime(args.next, args.verbose)

            elif args.previous is not None:
                self.handle_previous_prime(args.previous, args.verbose)

            elif args.gaps is not None:
                self.handle_gaps(args.gaps, args.timing, args.verbose)

            elif args.mersenne is not None:
                self.handle_mersenne(args.mersenne, args.timing, args.verbose)

            elif args.benchmark is not None:
                self.handle_benchmark(args.benchmark, args.verbose)

            elif args.batch is not None:
                self.handle_batch(args.batch, args.method, args.verbose)

        except KeyboardInterrupt:
            print("\nOperation interrupted by user.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def run_interactive(self):
        """Run application in interactive CLI mode."""
        cli = PrimeGeneratorCLI()
        cli.run()

    def run(self):
        """Main application entry point."""
        parser = self.setup_argument_parser()
        args = parser.parse_args()

        # Check if any command-line arguments were provided
        has_args = any([
            args.check is not None,
            args.generate is not None,
            args.first is not None,
            args.factorize is not None,
            args.next is not None,
            args.previous is not None,
            args.gaps is not None,
            args.mersenne is not None,
            args.benchmark is not None,
            args.batch is not None
        ])

        if has_args:
            # Command-line mode
            self.run_command_line(args)
        else:
            # Interactive mode
            self.run_interactive()


def main():
    """Main entry point for the application."""
    app = PrimeGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()