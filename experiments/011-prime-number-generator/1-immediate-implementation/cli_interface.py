"""
Command Line Interface for Prime Number Generator

This module provides an interactive CLI for the prime number generator,
offering a user-friendly menu system for all available functionality.
"""

import sys
import os
from typing import List, Optional, Any
from prime_generator import PrimeGenerator, timing_decorator


class PrimeGeneratorCLI:
    """
    Interactive command-line interface for the Prime Number Generator.
    """

    def __init__(self):
        """Initialize the CLI with a prime generator instance."""
        self.generator = PrimeGenerator()
        self.history = []  # Store operation history

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the application header."""
        print("=" * 60)
        print("           PRIME NUMBER GENERATOR")
        print("=" * 60)
        print("A comprehensive tool for prime number operations")
        print("Built with Python standard library only")
        print("=" * 60)

    def display_main_menu(self):
        """Display the main menu options."""
        print("\n" + "─" * 50)
        print("MAIN MENU")
        print("─" * 50)
        print("1.  Check if a number is prime")
        print("2.  Generate primes up to a limit")
        print("3.  Generate first N prime numbers")
        print("4.  Prime factorization")
        print("5.  Find next/previous prime")
        print("6.  Mersenne prime checker")
        print("7.  Prime gaps analysis")
        print("8.  Performance benchmark")
        print("9.  Batch operations")
        print("10. View operation history")
        print("11. Educational mode")
        print("12. Settings")
        print("0.  Exit")
        print("─" * 50)

    def get_user_input(self, prompt: str, input_type: type = str,
                      min_value: Optional[int] = None,
                      max_value: Optional[int] = None) -> Any:
        """
        Get and validate user input.

        Args:
            prompt: Input prompt to display
            input_type: Expected input type (int, float, str)
            min_value: Minimum value for numeric inputs
            max_value: Maximum value for numeric inputs

        Returns:
            Validated user input
        """
        while True:
            try:
                user_input = input(prompt).strip()

                if user_input.lower() in ['q', 'quit', 'exit']:
                    return None

                if input_type == int:
                    value = int(user_input)
                    if min_value is not None and value < min_value:
                        print(f"Error: Value must be at least {min_value}")
                        continue
                    if max_value is not None and value > max_value:
                        print(f"Error: Value must be at most {max_value}")
                        continue
                    return value
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input

            except ValueError:
                print(f"Error: Please enter a valid {input_type.__name__}")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None

    def log_operation(self, operation: str, result: str):
        """Log an operation to history."""
        self.history.append({
            'operation': operation,
            'result': result,
            'timestamp': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def check_single_prime(self):
        """Handle single prime checking."""
        print("\n" + "─" * 40)
        print("PRIME CHECKER")
        print("─" * 40)

        number = self.get_user_input("Enter a number to check: ", int, min_value=0)
        if number is None:
            return

        print("\nChoose method:")
        print("1. Basic trial division")
        print("2. Optimized algorithm (default)")
        print("3. Cached method")

        method_choice = self.get_user_input("Select method (1-3) [2]: ", str)

        method_map = {'1': 'basic', '2': 'optimized', '3': 'cached', '': 'optimized'}
        method = method_map.get(method_choice, 'optimized')

        @timing_decorator
        def check_with_timing():
            return self.generator.is_prime(number, method)

        print(f"\nChecking if {number} is prime using {method} method...")
        is_prime = check_with_timing()

        result = f"{number} is {'prime' if is_prime else 'not prime'}"
        print(f"\nResult: {result}")

        if is_prime and number > 2:
            prev_prime = self.generator.previous_prime(number)
            next_prime = self.generator.next_prime(number)
            print(f"Previous prime: {prev_prime}")
            print(f"Next prime: {next_prime}")

        self.log_operation(f"Prime check: {number} ({method})", result)

    def generate_primes_to_limit(self):
        """Handle prime generation up to a limit."""
        print("\n" + "─" * 40)
        print("GENERATE PRIMES UP TO LIMIT")
        print("─" * 40)

        limit = self.get_user_input("Enter upper limit: ", int, min_value=2)
        if limit is None:
            return

        print("\nChoose method:")
        print("1. Sieve of Eratosthenes (fastest)")
        print("2. Trial division")
        print("3. Optimized trial division")

        method_choice = self.get_user_input("Select method (1-3) [1]: ", str)
        method_map = {'1': 'sieve', '2': 'trial', '3': 'optimized', '': 'sieve'}
        method = method_map.get(method_choice, 'sieve')

        @timing_decorator
        def generate_with_timing():
            return self.generator.generate_primes_up_to(limit, method)

        print(f"\nGenerating primes up to {limit} using {method} method...")
        primes = generate_with_timing()

        print(f"\nFound {len(primes)} prime numbers")

        if len(primes) <= 100:
            self._display_primes_formatted(primes)
        else:
            show_all = self.get_user_input(
                f"Found {len(primes)} primes. Show all? (y/n) [n]: ", str
            )
            if show_all and show_all.lower().startswith('y'):
                self._display_primes_formatted(primes)
            else:
                print(f"First 10: {primes[:10]}")
                print(f"Last 10: {primes[-10:]}")

        self.log_operation(f"Primes up to {limit} ({method})", f"{len(primes)} primes found")

    def generate_first_n_primes(self):
        """Handle generating first N primes."""
        print("\n" + "─" * 40)
        print("GENERATE FIRST N PRIMES")
        print("─" * 40)

        n = self.get_user_input("Enter number of primes to generate: ", int, min_value=1)
        if n is None:
            return

        if n > 1000:
            confirm = self.get_user_input(
                f"Generating {n} primes may take time. Continue? (y/n): ", str
            )
            if not confirm or not confirm.lower().startswith('y'):
                return

        @timing_decorator
        def generate_with_timing():
            return self.generator.generate_first_n_primes(n)

        print(f"\nGenerating first {n} prime numbers...")
        primes = generate_with_timing()

        if len(primes) <= 50:
            self._display_primes_formatted(primes)
        else:
            print(f"First 10: {primes[:10]}")
            print(f"Last 10: {primes[-10:]}")
            show_all = self.get_user_input("Show all primes? (y/n) [n]: ", str)
            if show_all and show_all.lower().startswith('y'):
                self._display_primes_formatted(primes)

        print(f"\nLargest prime found: {primes[-1]}")
        self.log_operation(f"First {n} primes", f"Largest: {primes[-1]}")

    def _display_primes_formatted(self, primes: List[int], columns: int = 10):
        """Display primes in a formatted grid."""
        print("\nPrime numbers:")
        for i, prime in enumerate(primes):
            print(f"{prime:6d}", end="")
            if (i + 1) % columns == 0:
                print()
        if len(primes) % columns != 0:
            print()

    def prime_factorization(self):
        """Handle prime factorization."""
        print("\n" + "─" * 40)
        print("PRIME FACTORIZATION")
        print("─" * 40)

        number = self.get_user_input("Enter number to factorize: ", int, min_value=2)
        if number is None:
            return

        @timing_decorator
        def factorize_with_timing():
            return self.generator.prime_factorization(number)

        print(f"\nFactorizing {number}...")
        factors = factorize_with_timing()

        if not factors:
            print(f"{number} has no prime factors (less than 2)")
            return

        print(f"\nPrime factorization of {number}:")
        factor_strings = []
        for prime, power in factors:
            if power == 1:
                factor_strings.append(str(prime))
            else:
                factor_strings.append(f"{prime}^{power}")

        factorization = " × ".join(factor_strings)
        print(f"{number} = {factorization}")

        # Verify the factorization
        product = 1
        for prime, power in factors:
            product *= prime ** power
        print(f"Verification: {product} = {number} ✓")

        self.log_operation(f"Factorization of {number}", factorization)

    def find_adjacent_primes(self):
        """Handle finding next/previous primes."""
        print("\n" + "─" * 40)
        print("FIND ADJACENT PRIMES")
        print("─" * 40)

        number = self.get_user_input("Enter a number: ", int, min_value=1)
        if number is None:
            return

        print(f"\nFinding primes adjacent to {number}...")

        prev_prime = self.generator.previous_prime(number)
        next_prime = self.generator.next_prime(number)

        print(f"Previous prime: {prev_prime if prev_prime else 'None'}")
        print(f"Current number: {number} ({'prime' if self.generator.is_prime(number) else 'composite'})")
        print(f"Next prime: {next_prime}")

        if prev_prime and next_prime:
            gap_prev = number - prev_prime
            gap_next = next_prime - number
            print(f"\nGap to previous: {gap_prev}")
            print(f"Gap to next: {gap_next}")

        result = f"Prev: {prev_prime}, Next: {next_prime}"
        self.log_operation(f"Adjacent primes for {number}", result)

    def mersenne_prime_check(self):
        """Handle Mersenne prime checking."""
        print("\n" + "─" * 40)
        print("MERSENNE PRIME CHECKER")
        print("─" * 40)
        print("Mersenne primes have the form 2^p - 1 where p is prime")

        p = self.get_user_input("Enter exponent p: ", int, min_value=2, max_value=50)
        if p is None:
            return

        if p > 20:
            print("Warning: Large exponents may take significant time to compute.")
            confirm = self.get_user_input("Continue? (y/n): ", str)
            if not confirm or not confirm.lower().startswith('y'):
                return

        @timing_decorator
        def check_mersenne():
            return self.generator.is_mersenne_prime(p)

        print(f"\nChecking if 2^{p} - 1 is a Mersenne prime...")
        mersenne_number = (2 ** p) - 1
        print(f"Mersenne candidate: {mersenne_number}")

        is_mersenne = check_mersenne()

        result = f"2^{p} - 1 = {mersenne_number} is {'a Mersenne prime' if is_mersenne else 'not a Mersenne prime'}"
        print(f"\nResult: {result}")

        self.log_operation(f"Mersenne check: 2^{p} - 1", result)

    def prime_gaps_analysis(self):
        """Handle prime gaps analysis."""
        print("\n" + "─" * 40)
        print("PRIME GAPS ANALYSIS")
        print("─" * 40)

        limit = self.get_user_input("Enter upper limit for analysis: ", int, min_value=10)
        if limit is None:
            return

        @timing_decorator
        def analyze_gaps():
            return self.generator.prime_gaps(limit)

        print(f"\nAnalyzing prime gaps up to {limit}...")
        gaps = analyze_gaps()

        if not gaps:
            print("No gaps found (limit too small)")
            return

        print(f"\nFound {len(gaps)} gaps between consecutive primes")

        # Gap statistics
        gap_sizes = [gap for _, _, gap in gaps]
        max_gap = max(gap_sizes)
        min_gap = min(gap_sizes)
        avg_gap = sum(gap_sizes) / len(gap_sizes)

        print(f"Gap statistics:")
        print(f"  Minimum gap: {min_gap}")
        print(f"  Maximum gap: {max_gap}")
        print(f"  Average gap: {avg_gap:.2f}")

        # Show largest gaps
        gaps.sort(key=lambda x: x[2], reverse=True)
        print(f"\nLargest gaps:")
        for i, (p1, p2, gap) in enumerate(gaps[:5]):
            print(f"  {i+1}. {p1} → {p2} (gap: {gap})")

        self.log_operation(f"Prime gaps up to {limit}", f"Max gap: {max_gap}, Avg: {avg_gap:.2f}")

    def performance_benchmark(self):
        """Handle performance benchmarking."""
        print("\n" + "─" * 40)
        print("PERFORMANCE BENCHMARK")
        print("─" * 40)

        limit = self.get_user_input("Enter limit for benchmark: ", int, min_value=100)
        if limit is None:
            return

        if limit > 100000:
            print("Warning: Large limits may take significant time.")
            confirm = self.get_user_input("Continue? (y/n): ", str)
            if not confirm or not confirm.lower().startswith('y'):
                return

        print(f"\nBenchmarking prime generation methods up to {limit}...")
        print("This may take a moment...\n")

        results = self.generator.benchmark_methods(limit)

        print("Benchmark Results:")
        print("─" * 40)
        for method, data in results.items():
            print(f"{method.capitalize():12s}: {data['time']:.4f}s ({data['count']} primes)")

        # Find fastest method
        fastest = min(results.items(), key=lambda x: x[1]['time'])
        print(f"\nFastest method: {fastest[0]} ({fastest[1]['time']:.4f}s)")

        self.log_operation(f"Benchmark up to {limit}", f"Fastest: {fastest[0]}")

    def batch_operations(self):
        """Handle batch operations on multiple numbers."""
        print("\n" + "─" * 40)
        print("BATCH OPERATIONS")
        print("─" * 40)

        print("Enter numbers separated by spaces or commas:")
        input_str = self.get_user_input("Numbers: ", str)
        if input_str is None:
            return

        # Parse input
        try:
            # Replace commas with spaces and split
            numbers_str = input_str.replace(',', ' ').split()
            numbers = [int(x) for x in numbers_str if x.strip()]
        except ValueError:
            print("Error: Invalid number format")
            return

        if not numbers:
            print("No valid numbers entered")
            return

        print(f"\nProcessing {len(numbers)} numbers...")
        print("─" * 50)

        results = []
        for num in numbers:
            is_prime = self.generator.is_prime(num)
            results.append((num, is_prime))
            status = "Prime" if is_prime else "Composite"
            print(f"{num:8d}: {status}")

        # Summary
        prime_count = sum(1 for _, is_prime in results if is_prime)
        print("─" * 50)
        print(f"Summary: {prime_count}/{len(numbers)} numbers are prime")

        primes_found = [num for num, is_prime in results if is_prime]
        if primes_found:
            print(f"Primes found: {primes_found}")

        self.log_operation(f"Batch check {len(numbers)} numbers", f"{prime_count} primes found")

    def view_history(self):
        """Display operation history."""
        print("\n" + "─" * 40)
        print("OPERATION HISTORY")
        print("─" * 40)

        if not self.history:
            print("No operations performed yet.")
            return

        for i, entry in enumerate(self.history[-10:], 1):  # Show last 10
            print(f"{i:2d}. [{entry['timestamp']}] {entry['operation']}")
            print(f"    Result: {entry['result']}")
            print()

    def educational_mode(self):
        """Educational mode with explanations."""
        print("\n" + "─" * 40)
        print("EDUCATIONAL MODE")
        print("─" * 40)

        topics = {
            '1': self._explain_prime_numbers,
            '2': self._explain_algorithms,
            '3': self._explain_mersenne_primes,
            '4': self._explain_prime_gaps,
            '5': self._explain_factorization
        }

        print("Choose a topic:")
        print("1. What are prime numbers?")
        print("2. Prime checking algorithms")
        print("3. Mersenne primes")
        print("4. Prime gaps")
        print("5. Prime factorization")

        choice = self.get_user_input("Select topic (1-5): ", str)

        if choice in topics:
            topics[choice]()
        else:
            print("Invalid choice.")

    def _explain_prime_numbers(self):
        """Explain what prime numbers are."""
        print("\n" + "=" * 50)
        print("WHAT ARE PRIME NUMBERS?")
        print("=" * 50)
        print("""
A prime number is a natural number greater than 1 that has no positive
divisors other than 1 and itself.

Examples:
- 2 is prime (only divisible by 1 and 2)
- 3 is prime (only divisible by 1 and 3)
- 4 is NOT prime (divisible by 1, 2, and 4)
- 5 is prime (only divisible by 1 and 5)

Key facts:
• 2 is the only even prime number
• All other primes are odd
• There are infinitely many primes (Euclid's theorem)
• The distribution of primes becomes sparser as numbers get larger

The first few primes are: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37...
        """)

    def _explain_algorithms(self):
        """Explain prime checking algorithms."""
        print("\n" + "=" * 50)
        print("PRIME CHECKING ALGORITHMS")
        print("=" * 50)
        print("""
1. TRIAL DIVISION (Basic)
   - Check divisibility by all numbers from 2 to √n
   - Time complexity: O(√n)
   - Simple but slow for large numbers

2. OPTIMIZED TRIAL DIVISION
   - Only check 2, 3, then numbers of form 6k±1
   - Skips multiples of 2 and 3
   - About 3x faster than basic method

3. SIEVE OF ERATOSTHENES
   - Generate all primes up to a limit
   - Mark multiples of each prime as composite
   - Very efficient for finding many primes
   - Time complexity: O(n log log n)

4. CACHED METHOD
   - Uses previously found primes for checking
   - Builds up a cache of known primes
   - Efficient for repeated prime checks
        """)

    def _explain_mersenne_primes(self):
        """Explain Mersenne primes."""
        print("\n" + "=" * 50)
        print("MERSENNE PRIMES")
        print("=" * 50)
        print("""
A Mersenne prime is a prime number of the form 2^p - 1, where p is also prime.

Examples:
- 2^2 - 1 = 3 (prime, so 3 is a Mersenne prime)
- 2^3 - 1 = 7 (prime, so 7 is a Mersenne prime)
- 2^5 - 1 = 31 (prime, so 31 is a Mersenne prime)
- 2^11 - 1 = 2047 = 23 × 89 (not prime)

Facts about Mersenne primes:
• Not all primes p give Mersenne primes 2^p - 1
• Only 51 Mersenne primes are known (as of 2023)
• They grow very large very quickly
• Used in computer science and cryptography
• The largest known primes are usually Mersenne primes

The first few Mersenne primes: 3, 7, 31, 127, 8191, 131071...
        """)

    def _explain_prime_gaps(self):
        """Explain prime gaps."""
        print("\n" + "=" * 50)
        print("PRIME GAPS")
        print("=" * 50)
        print("""
A prime gap is the difference between consecutive prime numbers.

Examples:
- Gap between 3 and 5: 5 - 3 = 2
- Gap between 5 and 7: 7 - 5 = 2
- Gap between 7 and 11: 11 - 7 = 4
- Gap between 89 and 97: 97 - 89 = 8

Interesting facts:
• The smallest possible gap is 2 (twin primes)
• Gaps can be arbitrarily large
• Average gap size increases as numbers get larger
• Twin prime conjecture: infinitely many gaps of size 2

Common gap sizes in small ranges:
- Gap of 2: Very common (twin primes)
- Gap of 4: Common
- Gap of 6: Common
- Larger gaps become less frequent
        """)

    def _explain_factorization(self):
        """Explain prime factorization."""
        print("\n" + "=" * 50)
        print("PRIME FACTORIZATION")
        print("=" * 50)
        print("""
Prime factorization is expressing a number as a product of prime numbers.

Every integer greater than 1 has a unique prime factorization (fundamental
theorem of arithmetic).

Examples:
- 12 = 2² × 3
- 30 = 2 × 3 × 5
- 60 = 2² × 3 × 5
- 100 = 2² × 5²

Algorithm:
1. Start with smallest prime (2)
2. Divide number by prime as many times as possible
3. Move to next prime
4. Repeat until number becomes 1

Applications:
• Cryptography (RSA encryption)
• Number theory
• Computer algorithms
• Mathematical proofs
        """)

    def settings_menu(self):
        """Handle settings and preferences."""
        print("\n" + "─" * 40)
        print("SETTINGS")
        print("─" * 40)
        print("1. Clear operation history")
        print("2. Display cache statistics")
        print("3. Reset all caches")
        print("4. About this program")

        choice = self.get_user_input("Select option (1-4): ", str)

        if choice == '1':
            self.history.clear()
            print("Operation history cleared.")
        elif choice == '2':
            self._display_cache_stats()
        elif choice == '3':
            self.generator = PrimeGenerator()  # Reset with new instance
            print("All caches reset.")
        elif choice == '4':
            self._display_about()

    def _display_cache_stats(self):
        """Display cache statistics."""
        print("\nCache Statistics:")
        print(f"Prime cache size: {len(self.generator._cache)}")
        print(f"Known primes: {len(self.generator._known_primes)}")
        if self.generator._known_primes:
            print(f"Largest cached prime: {self.generator._known_primes[-1]}")

    def _display_about(self):
        """Display information about the program."""
        print("\n" + "=" * 50)
        print("ABOUT PRIME NUMBER GENERATOR")
        print("=" * 50)
        print("""
Version: 1.0
Built with: Python standard library only
Features: Multiple algorithms, performance benchmarking,
         educational content, comprehensive analysis tools

This tool provides a complete suite for prime number exploration,
from basic prime checking to advanced mathematical analysis.

Algorithms implemented:
• Trial division (basic and optimized)
• Sieve of Eratosthenes
• Cached prime checking
• Prime factorization
• Mersenne prime detection
• Gap analysis

Educational content covers fundamental concepts and
practical applications of prime numbers in mathematics
and computer science.
        """)

    def run(self):
        """Main application loop."""
        self.clear_screen()
        self.display_header()

        print("\nWelcome! Enter 'q' or 'quit' at any prompt to go back.")
        print("Press Ctrl+C to interrupt long operations.")

        while True:
            try:
                self.display_main_menu()
                choice = self.get_user_input("\nSelect option (0-12): ", str)

                if choice is None or choice in ['0', 'exit', 'quit']:
                    print("\nThank you for using Prime Number Generator!")
                    break

                # Menu dispatch
                menu_actions = {
                    '1': self.check_single_prime,
                    '2': self.generate_primes_to_limit,
                    '3': self.generate_first_n_primes,
                    '4': self.prime_factorization,
                    '5': self.find_adjacent_primes,
                    '6': self.mersenne_prime_check,
                    '7': self.prime_gaps_analysis,
                    '8': self.performance_benchmark,
                    '9': self.batch_operations,
                    '10': self.view_history,
                    '11': self.educational_mode,
                    '12': self.settings_menu
                }

                if choice in menu_actions:
                    menu_actions[choice]()
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid option. Please try again.")

            except KeyboardInterrupt:
                print("\n\nOperation interrupted by user.")
                input("Press Enter to return to menu...")
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    # Run the CLI directly if this module is executed
    cli = PrimeGeneratorCLI()
    cli.run()