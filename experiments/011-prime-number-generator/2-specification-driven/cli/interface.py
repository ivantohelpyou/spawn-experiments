"""
Command-line interface for the Prime Number Generator application.

This module provides a comprehensive CLI with support for all major
operations including generation, validation, and performance benchmarking.
"""

import argparse
import json
import sys
import time
from typing import List, Any, Dict, Optional

try:
    from ..core import (
        PrimeGenerator,
        PrimeValidator,
        BatchValidator,
        AlgorithmComparator,
        BenchmarkRunner,
        format_performance_report,
        format_comparison_report
    )
    from ..utils import (
        format_number,
        format_time,
        format_memory,
        PrimeGeneratorError,
        InvalidInputError
    )
except ImportError:
    # Handle case when running as main module
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from core import (
        PrimeGenerator,
        PrimeValidator,
        BatchValidator,
        AlgorithmComparator,
        BenchmarkRunner,
        format_performance_report,
        format_comparison_report
    )
    from utils import (
        format_number,
        format_time,
        format_memory,
        PrimeGeneratorError,
        InvalidInputError
    )


class CLIInterface:
    """
    Command-line interface for the Prime Number Generator.

    This class handles argument parsing, user interaction, and
    output formatting for all application features.
    """

    def __init__(self):
        self.generator = PrimeGenerator()
        self.validator = PrimeValidator()
        self.batch_validator = BatchValidator()
        self.comparator = AlgorithmComparator()
        self.benchmark_runner = BenchmarkRunner()

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the argument parser.

        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="Prime Number Generator - Comprehensive prime number operations",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s generate --limit 100
  %(prog)s generate --count 50
  %(prog)s generate --range 100 200
  %(prog)s validate 97
  %(prog)s validate 97 98 99 100
  %(prog)s benchmark --limit 10000
  %(prog)s algorithms
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Generate command
        generate_parser = subparsers.add_parser('generate', help='Generate prime numbers')
        generate_group = generate_parser.add_mutually_exclusive_group(required=True)
        generate_group.add_argument('--limit', type=int, help='Generate primes up to limit')
        generate_group.add_argument('--count', type=int, help='Generate first N primes')
        generate_group.add_argument('--range', nargs=2, type=int, metavar=('START', 'END'),
                                  help='Generate primes in range')

        generate_parser.add_argument('--algorithm', choices=['auto', 'sieve', 'trial_division', 'optimized_trial'],
                                   default='auto', help='Algorithm to use')
        generate_parser.add_argument('--format', choices=['list', 'json', 'csv'], default='list',
                                   help='Output format')
        generate_parser.add_argument('--output', help='Output file path')
        generate_parser.add_argument('--performance', action='store_true',
                                   help='Include performance metrics')
        generate_parser.add_argument('--verbose', action='store_true', help='Verbose output')

        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate prime numbers')
        validate_parser.add_argument('numbers', nargs='+', type=int, help='Numbers to validate')
        validate_parser.add_argument('--factors', action='store_true',
                                   help='Include prime factors for composite numbers')
        validate_parser.add_argument('--format', choices=['text', 'json'], default='text',
                                   help='Output format')
        validate_parser.add_argument('--summary', action='store_true',
                                   help='Include batch summary statistics')

        # Benchmark command
        benchmark_parser = subparsers.add_parser('benchmark', help='Performance benchmarking')
        benchmark_parser.add_argument('--limit', type=int, default=10000,
                                    help='Upper limit for benchmark')
        benchmark_parser.add_argument('--algorithms', nargs='+',
                                    choices=['sieve', 'trial_division', 'optimized_trial'],
                                    help='Algorithms to compare')
        benchmark_parser.add_argument('--comprehensive', action='store_true',
                                    help='Run comprehensive benchmark suite')
        benchmark_parser.add_argument('--output', help='Output file for results')

        # Algorithms command
        algorithms_parser = subparsers.add_parser('algorithms', help='List available algorithms')
        algorithms_parser.add_argument('--detailed', action='store_true',
                                     help='Show detailed algorithm information')

        # Version command
        subparsers.add_parser('version', help='Show version information')

        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI application.

        Args:
            args: Command line arguments (uses sys.argv if None)

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        parser = self.create_parser()

        try:
            parsed_args = parser.parse_args(args)

            if not parsed_args.command:
                parser.print_help()
                return 1

            # Route to appropriate handler
            if parsed_args.command == 'generate':
                return self._handle_generate(parsed_args)
            elif parsed_args.command == 'validate':
                return self._handle_validate(parsed_args)
            elif parsed_args.command == 'benchmark':
                return self._handle_benchmark(parsed_args)
            elif parsed_args.command == 'algorithms':
                return self._handle_algorithms(parsed_args)
            elif parsed_args.command == 'version':
                return self._handle_version(parsed_args)
            else:
                print(f"Unknown command: {parsed_args.command}", file=sys.stderr)
                return 1

        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            return 130
        except PrimeGeneratorError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 2

    def _handle_generate(self, args) -> int:
        """Handle the generate command."""
        try:
            start_time = time.perf_counter()

            # Determine generation parameters
            if args.limit is not None:
                if args.verbose:
                    print(f"Generating primes up to {format_number(args.limit)}...")
                result = self.generator.generate_primes_up_to(args.limit, args.algorithm)
                operation = f"Generated primes up to {format_number(args.limit)}"

            elif args.count is not None:
                if args.verbose:
                    print(f"Generating first {format_number(args.count)} primes...")
                result = self.generator.generate_first_n_primes(args.count, args.algorithm)
                operation = f"Generated first {format_number(args.count)} primes"

            elif args.range:
                start, end = args.range
                if args.verbose:
                    print(f"Generating primes from {format_number(start)} to {format_number(end)}...")
                result = self.generator.generate_primes_in_range(start, end, args.algorithm)
                operation = f"Generated primes from {format_number(start)} to {format_number(end)}"

            end_time = time.perf_counter()
            execution_time = end_time - start_time

            # Format and output results
            output_content = self._format_generation_output(
                result, operation, execution_time, args
            )

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_content)
                print(f"Results saved to {args.output}")
            else:
                print(output_content)

            return 0

        except Exception as e:
            raise PrimeGeneratorError(f"Generation failed: {e}")

    def _handle_validate(self, args) -> int:
        """Handle the validate command."""
        try:
            if args.format == 'json':
                results = []
                for number in args.numbers:
                    result = self.validator.validate(number, args.factors)
                    results.append({
                        'number': result.number,
                        'is_prime': result.is_prime,
                        'factors': result.factors,
                        'execution_time': result.execution_time,
                        'explanation': result.explanation
                    })

                output = {'results': results}
                if args.summary:
                    batch_results = self.batch_validator.validate_batch(args.numbers, args.factors)
                    summary = self.batch_validator.get_batch_summary(batch_results)
                    output['summary'] = summary

                print(json.dumps(output, indent=2))

            else:
                # Text format
                for number in args.numbers:
                    result = self.validator.validate(number, args.factors)
                    print(f"\nNumber: {format_number(result.number)}")
                    print(f"Is Prime: {result.is_prime}")
                    print(f"Explanation: {result.explanation}")

                    if result.factors:
                        factors_str = " × ".join(map(str, result.factors))
                        print(f"Prime Factors: {factors_str}")

                    if hasattr(args, 'verbose') and args.verbose:
                        print(f"Validation Time: {format_time(result.execution_time)}")

                if args.summary and len(args.numbers) > 1:
                    batch_results = self.batch_validator.validate_batch(args.numbers, args.factors)
                    summary = self.batch_validator.get_batch_summary(batch_results)
                    self._print_validation_summary(summary)

            return 0

        except Exception as e:
            raise PrimeGeneratorError(f"Validation failed: {e}")

    def _handle_benchmark(self, args) -> int:
        """Handle the benchmark command."""
        try:
            if args.comprehensive:
                print("Running comprehensive benchmark suite...")
                algorithms = {
                    'sieve': lambda **kwargs: self.generator.generate_primes_up_to(algorithm='sieve', **kwargs),
                    'trial_division': lambda **kwargs: self.generator.generate_primes_up_to(algorithm='trial_division', **kwargs),
                    'optimized_trial': lambda **kwargs: self.generator.generate_primes_up_to(algorithm='optimized_trial', **kwargs)
                }

                results = self.benchmark_runner.run_standard_benchmarks(algorithms)
                output_content = self._format_benchmark_results(results)

            else:
                # Single benchmark
                print(f"Benchmarking algorithms up to {format_number(args.limit)}...")

                algorithms_to_test = args.algorithms or ['sieve', 'trial_division', 'optimized_trial']
                algorithms = {}

                for alg_name in algorithms_to_test:
                    algorithms[alg_name] = lambda limit, alg=alg_name: self.generator.generate_primes_up_to(limit, alg)

                comparison = self.comparator.compare_algorithms(algorithms, {'limit': args.limit})
                output_content = format_comparison_report(comparison)

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_content)
                print(f"Benchmark results saved to {args.output}")
            else:
                print(output_content)

            return 0

        except Exception as e:
            raise PrimeGeneratorError(f"Benchmark failed: {e}")

    def _handle_algorithms(self, args) -> int:
        """Handle the algorithms command."""
        algorithms = self.generator.get_available_algorithms()

        print("Available Prime Generation Algorithms")
        print("=" * 40)

        for config in algorithms:
            print(f"\nName: {config.name}")
            print(f"Description: {config.description}")

            if args.detailed:
                print(f"Optimal Range: {format_number(config.optimal_range[0])} - {format_number(config.optimal_range[1])}")
                print(f"Memory Efficient: {config.memory_efficient}")
                print(f"Time Complexity: {config.time_complexity}")
                print(f"Space Complexity: {config.space_complexity}")

        return 0

    def _handle_version(self, args) -> int:
        """Handle the version command."""
        print("Prime Number Generator v1.0.0")
        print("Comprehensive prime number generation and analysis tool")
        print("Built with Python standard library only")
        return 0

    def _format_generation_output(self, result: List[int], operation: str,
                                execution_time: float, args) -> str:
        """Format prime generation output."""
        if args.format == 'json':
            output = {
                'operation': operation,
                'count': len(result),
                'primes': result,
                'execution_time': execution_time
            }
            return json.dumps(output, indent=2)

        elif args.format == 'csv':
            output = "prime_number\n"
            for prime in result:
                output += f"{prime}\n"
            return output

        else:  # list format
            output = f"{operation}\n"
            output += f"Found {format_number(len(result))} prime numbers\n"

            if args.performance:
                output += f"Execution time: {format_time(execution_time)}\n"

            output += "\nPrime numbers:\n"

            # Format primes in rows of 10
            for i, prime in enumerate(result):
                if i % 10 == 0 and i > 0:
                    output += "\n"
                output += f"{prime:>6} "

            output += "\n"
            return output

    def _print_validation_summary(self, summary: Dict[str, Any]) -> None:
        """Print validation batch summary."""
        print(f"\nValidation Summary:")
        print(f"Total Numbers: {format_number(summary['total_numbers'])}")
        print(f"Prime Count: {format_number(summary['prime_count'])}")
        print(f"Composite Count: {format_number(summary['composite_count'])}")
        print(f"Invalid Count: {format_number(summary['invalid_count'])}")
        print(f"Prime Percentage: {summary['prime_percentage']:.1f}%")
        print(f"Total Time: {format_time(summary['total_execution_time'])}")
        print(f"Average Time: {format_time(summary['average_execution_time'])}")

        if summary['largest_prime']:
            print(f"Largest Prime: {format_number(summary['largest_prime'])}")

    def _format_benchmark_results(self, results: Dict[str, Any]) -> str:
        """Format comprehensive benchmark results."""
        output = "Comprehensive Benchmark Results\n"
        output += "=" * 35 + "\n\n"

        # Summary
        summary = results['summary']
        output += f"Total Tests: {summary['total_tests']}\n"
        output += f"Passed Tests: {summary['passed_tests']}\n"
        output += f"Pass Rate: {summary['pass_rate']:.1%}\n\n"

        # Algorithm rankings
        if 'algorithm_rankings' in summary:
            rankings = summary['algorithm_rankings']
            output += "Algorithm Rankings (by speed):\n"
            for i, alg in enumerate(rankings['by_speed'], 1):
                avg_time = rankings['average_times'][alg]
                output += f"{i}. {alg}: {format_time(avg_time)}\n"
            output += "\n"

        # Individual comparisons
        for comparison in results['comparisons']:
            output += format_comparison_report(comparison)
            output += "\n" + "-" * 50 + "\n\n"

        return output


def main():
    """Main entry point for the CLI application."""
    cli = CLIInterface()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()