#!/usr/bin/env python3
"""
Comprehensive Roman Numeral Solution Analysis
Performance benchmarking and algorithm comparison for high-volume usage.

Requirements:
- 1,000,000+ conversions per day
- <10ms per conversion
- Concurrent request handling
- Memory efficiency
"""

import time
import random
import threading
import concurrent.futures
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager
import sys
import os

# Add the existing implementations to path
sys.path.append('/home/ivan/projects/spawn-experiments/experiments/1.103-roman-numeral-converter/1-immediate-implementation')
sys.path.append('/home/ivan/projects/spawn-experiments/experiments/1.103-roman-numeral-converter/2-specification-driven')

try:
    import roman_numerals as immediate_impl
    import roman_numeral_converter as spec_driven_impl
except ImportError as e:
    print(f"Warning: Could not import existing implementations: {e}")


@dataclass
class PerformanceResult:
    """Results from performance testing"""
    algorithm_name: str
    total_time: float
    conversions_per_second: float
    avg_time_per_conversion_ns: float
    memory_usage_mb: float
    errors: int

    def meets_requirements(self) -> bool:
        """Check if performance meets the <10ms requirement"""
        avg_time_ms = self.avg_time_per_conversion_ns / 1_000_000
        return avg_time_ms < 10.0


class OptimizedRomanConverter:
    """
    Highly optimized Roman numeral converter using precomputed lookup tables
    and minimized allocations for maximum performance.
    """

    def __init__(self):
        # Precomputed lookup tables for thousands, hundreds, tens, ones
        self.thousands = ['', 'M', 'MM', 'MMM']
        self.hundreds = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
        self.tens = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
        self.ones = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

        # Roman to int mapping for reverse conversion
        self.roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

    def int_to_roman(self, num: int) -> str:
        """Convert integer to Roman using precomputed lookup tables"""
        if not 1 <= num <= 3999:
            raise ValueError("Number must be between 1 and 3999")

        # Extract digits
        thousands_digit = num // 1000
        hundreds_digit = (num % 1000) // 100
        tens_digit = (num % 100) // 10
        ones_digit = num % 10

        # Concatenate using precomputed strings
        return (self.thousands[thousands_digit] +
                self.hundreds[hundreds_digit] +
                self.tens[tens_digit] +
                self.ones[ones_digit])

    def roman_to_int(self, roman: str) -> int:
        """Convert Roman to integer using subtraction logic"""
        if not roman:
            raise ValueError("Roman numeral cannot be empty")

        total = 0
        prev_value = 0

        for char in reversed(roman.upper()):
            if char not in self.roman_values:
                raise ValueError(f"Invalid character: {char}")

            value = self.roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        return total


class ArrayBasedConverter:
    """
    Array-based converter using direct value mappings for performance.
    """

    def __init__(self):
        # Mapping from largest to smallest for greedy conversion
        self.values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        self.numerals = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']

        # Roman to int mapping
        self.roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

    def int_to_roman(self, num: int) -> str:
        """Convert using greedy algorithm with value arrays"""
        if not 1 <= num <= 3999:
            raise ValueError("Number must be between 1 and 3999")

        result = []
        for i, value in enumerate(self.values):
            count = num // value
            if count:
                result.append(self.numerals[i] * count)
                num -= value * count

        return ''.join(result)

    def roman_to_int(self, roman: str) -> int:
        """Convert Roman to integer"""
        if not roman:
            raise ValueError("Roman numeral cannot be empty")

        total = 0
        prev_value = 0

        for char in reversed(roman.upper()):
            if char not in self.roman_values:
                raise ValueError(f"Invalid character: {char}")

            value = self.roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        return total


@contextmanager
def timer():
    """Context manager to measure execution time"""
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    return end - start


class RomanNumeralBenchmark:
    """Comprehensive benchmarking suite for Roman numeral implementations"""

    def __init__(self):
        self.algorithms = {
            'optimized_lookup': OptimizedRomanConverter(),
            'array_based': ArrayBasedConverter(),
        }

        # Add existing implementations if available
        if 'immediate_impl' in globals():
            self.algorithms['immediate_implementation'] = immediate_impl
        if 'spec_driven_impl' in globals():
            self.algorithms['specification_driven'] = spec_driven_impl

    def generate_test_data(self, size: int) -> List[int]:
        """Generate random test data for benchmarking"""
        return [random.randint(1, 3999) for _ in range(size)]

    def benchmark_single_threaded(self, algorithm_name: str, test_data: List[int]) -> PerformanceResult:
        """Benchmark single-threaded performance"""
        algorithm = self.algorithms[algorithm_name]
        errors = 0

        # Measure int_to_roman performance
        start_time = time.perf_counter()

        for num in test_data:
            try:
                if hasattr(algorithm, 'int_to_roman'):
                    roman = algorithm.int_to_roman(num)
                else:
                    # For module-level functions
                    roman = algorithm.int_to_roman(num)
            except Exception:
                errors += 1

        end_time = time.perf_counter()

        total_time = end_time - start_time
        conversions = len(test_data)
        conversions_per_second = conversions / total_time if total_time > 0 else 0
        avg_time_per_conversion_ns = (total_time * 1_000_000_000) / conversions

        return PerformanceResult(
            algorithm_name=algorithm_name,
            total_time=total_time,
            conversions_per_second=conversions_per_second,
            avg_time_per_conversion_ns=avg_time_per_conversion_ns,
            memory_usage_mb=0.0,  # Would need memory profiling for accurate measurement
            errors=errors
        )

    def benchmark_concurrent(self, algorithm_name: str, test_data: List[int], num_threads: int = 4) -> PerformanceResult:
        """Benchmark concurrent performance using ThreadPoolExecutor"""
        algorithm = self.algorithms[algorithm_name]
        errors = 0

        def convert_batch(batch: List[int]) -> int:
            batch_errors = 0
            for num in batch:
                try:
                    if hasattr(algorithm, 'int_to_roman'):
                        roman = algorithm.int_to_roman(num)
                    else:
                        roman = algorithm.int_to_roman(num)
                except Exception:
                    batch_errors += 1
            return batch_errors

        # Split data into batches for concurrent processing
        batch_size = len(test_data) // num_threads
        batches = [test_data[i:i+batch_size] for i in range(0, len(test_data), batch_size)]

        start_time = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(convert_batch, batch) for batch in batches]
            for future in concurrent.futures.as_completed(futures):
                errors += future.result()

        end_time = time.perf_counter()

        total_time = end_time - start_time
        conversions = len(test_data)
        conversions_per_second = conversions / total_time if total_time > 0 else 0
        avg_time_per_conversion_ns = (total_time * 1_000_000_000) / conversions

        return PerformanceResult(
            algorithm_name=f"{algorithm_name}_concurrent",
            total_time=total_time,
            conversions_per_second=conversions_per_second,
            avg_time_per_conversion_ns=avg_time_per_conversion_ns,
            memory_usage_mb=0.0,
            errors=errors
        )

    def run_comprehensive_benchmark(self, test_size: int = 100_000) -> Dict[str, List[PerformanceResult]]:
        """Run comprehensive benchmarks on all algorithms"""
        print(f"Generating {test_size:,} test cases...")
        test_data = self.generate_test_data(test_size)

        results = {}

        for algorithm_name in self.algorithms:
            print(f"\nBenchmarking {algorithm_name}...")

            # Single-threaded benchmark
            single_result = self.benchmark_single_threaded(algorithm_name, test_data)

            # Concurrent benchmark
            concurrent_result = self.benchmark_concurrent(algorithm_name, test_data)

            results[algorithm_name] = [single_result, concurrent_result]

            print(f"  Single-threaded: {single_result.conversions_per_second:,.0f} conversions/sec")
            print(f"  Concurrent: {concurrent_result.conversions_per_second:,.0f} conversions/sec")
            print(f"  Avg time per conversion: {single_result.avg_time_per_conversion_ns:.0f} ns")

        return results

    def analyze_results(self, results: Dict[str, List[PerformanceResult]]) -> None:
        """Analyze and report benchmark results"""
        print("\n" + "="*80)
        print("COMPREHENSIVE PERFORMANCE ANALYSIS")
        print("="*80)

        # Requirements check
        print("\nREQUIREMENT COMPLIANCE (<10ms per conversion):")
        print("-" * 50)

        for algorithm_name, result_list in results.items():
            single_result = result_list[0]
            avg_time_ms = single_result.avg_time_per_conversion_ns / 1_000_000
            compliance = "✓ PASS" if avg_time_ms < 10.0 else "✗ FAIL"
            print(f"{algorithm_name:25s}: {avg_time_ms:8.3f} ms  {compliance}")

        # Performance ranking
        print("\nPERFORMANCE RANKING (Single-threaded):")
        print("-" * 50)

        single_results = [(name, results[0]) for name, results in results.items()]
        single_results.sort(key=lambda x: x[1].conversions_per_second, reverse=True)

        for i, (name, result) in enumerate(single_results, 1):
            print(f"{i}. {name:25s}: {result.conversions_per_second:10,.0f} conversions/sec")

        # Concurrent performance
        print("\nCONCURRENT PERFORMANCE:")
        print("-" * 50)

        concurrent_results = [(name, results[1]) for name, results in results.items()]
        concurrent_results.sort(key=lambda x: x[1].conversions_per_second, reverse=True)

        for i, (name, result) in enumerate(concurrent_results, 1):
            print(f"{i}. {name:25s}: {result.conversions_per_second:10,.0f} conversions/sec")

        # Daily capacity analysis
        print("\nDAILY CAPACITY ANALYSIS (1M+ conversions/day requirement):")
        print("-" * 50)

        seconds_per_day = 24 * 60 * 60
        required_conversions_per_day = 1_000_000

        for algorithm_name, result_list in results.items():
            single_result = result_list[0]
            daily_capacity = single_result.conversions_per_second * seconds_per_day
            capacity_ratio = daily_capacity / required_conversions_per_day

            compliance = "✓ EXCEEDS" if capacity_ratio >= 1.0 else "✗ INSUFFICIENT"

            print(f"{algorithm_name:25s}: {daily_capacity:12,.0f} conversions/day "
                  f"({capacity_ratio:5.1f}x) {compliance}")


def main():
    """Main benchmarking execution"""
    print("Roman Numeral Conversion - Comprehensive Solution Analysis")
    print("=" * 60)
    print("Requirements: 1M+ conversions/day, <10ms per conversion, concurrent handling")
    print()

    benchmark = RomanNumeralBenchmark()

    # Run benchmarks with different test sizes
    for test_size in [10_000, 100_000]:
        print(f"\n{'='*20} TEST SIZE: {test_size:,} {'='*20}")
        results = benchmark.run_comprehensive_benchmark(test_size)
        benchmark.analyze_results(results)


if __name__ == "__main__":
    main()