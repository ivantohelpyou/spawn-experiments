#!/usr/bin/env python3
"""
Performance validation for Roman numeral conversion solutions.
Testing against requirements: <10ms per conversion, 1M+ daily volume.
"""

import time
import statistics
from typing import Tuple, List


# Solution 1: Lookup Table Approach (Most Common)
def int_to_roman_lookup(num: int) -> str:
    """Convert integer to Roman numeral using lookup table."""
    lookup = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    result = ''
    for value, symbol in lookup:
        count, num = divmod(num, value)
        result += symbol * count
    return result


def roman_to_int_lookup(roman: str) -> int:
    """Convert Roman numeral to integer using lookup table."""
    values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    total = 0
    prev_value = 0

    for char in reversed(roman):
        value = values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


# Solution 2: Array-Based Direct Mapping (Performance Optimized)
def int_to_roman_array(num: int) -> str:
    """Convert integer to Roman numeral using array-based mapping."""
    thousands = ['', 'M', 'MM', 'MMM']
    hundreds = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
    tens = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
    ones = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

    return (thousands[num // 1000] +
            hundreds[(num % 1000) // 100] +
            tens[(num % 100) // 10] +
            ones[num % 10])


def roman_to_int_array(roman: str) -> int:
    """Convert Roman numeral to integer using direct array mapping."""
    # Create array for O(1) lookup
    mapping = [0] * 256  # ASCII table size
    mapping[ord('I')] = 1
    mapping[ord('V')] = 5
    mapping[ord('X')] = 10
    mapping[ord('L')] = 50
    mapping[ord('C')] = 100
    mapping[ord('D')] = 500
    mapping[ord('M')] = 1000

    total = 0
    prev_value = 0

    for i in range(len(roman) - 1, -1, -1):
        value = mapping[ord(roman[i])]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


def benchmark_function(func, test_data: List, iterations: int = 1000) -> Tuple[float, float, float]:
    """Benchmark a function with test data."""
    times = []

    for _ in range(iterations):
        start_time = time.perf_counter()
        for data in test_data:
            func(data)
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convert to milliseconds

    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)

    return avg_time, min_time, max_time


def validate_performance_requirements():
    """Validate solutions against performance requirements."""
    print("=" * 60)
    print("ROMAN NUMERAL CONVERSION PERFORMANCE VALIDATION")
    print("=" * 60)
    print(f"Requirements: <10ms per conversion, 1M+ daily volume")
    print()

    # Test data representing typical usage patterns
    test_integers = [1, 4, 9, 27, 48, 59, 93, 141, 163, 402, 575, 911, 1024, 3000, 3999]
    test_romans = [int_to_roman_lookup(i) for i in test_integers]

    iterations = 1000
    operations_per_iteration = len(test_integers)

    print(f"Test Configuration:")
    print(f"- Test data size: {len(test_integers)} conversions per iteration")
    print(f"- Iterations: {iterations}")
    print(f"- Total operations: {iterations * operations_per_iteration}")
    print()

    solutions = [
        ("Lookup Table (int->roman)", int_to_roman_lookup, test_integers),
        ("Lookup Table (roman->int)", roman_to_int_lookup, test_romans),
        ("Array-Based (int->roman)", int_to_roman_array, test_integers),
        ("Array-Based (roman->int)", roman_to_int_array, test_romans),
    ]

    results = []

    for name, func, data in solutions:
        print(f"Testing: {name}")
        avg_time, min_time, max_time = benchmark_function(func, data, iterations)

        # Calculate per-operation time
        per_op_avg = avg_time / operations_per_iteration
        per_op_min = min_time / operations_per_iteration
        per_op_max = max_time / operations_per_iteration

        # Check requirement compliance
        meets_requirement = per_op_avg < 10.0  # <10ms requirement

        print(f"  Average: {avg_time:.3f}ms total ({per_op_avg:.4f}ms per conversion)")
        print(f"  Min:     {min_time:.3f}ms total ({per_op_min:.4f}ms per conversion)")
        print(f"  Max:     {max_time:.3f}ms total ({per_op_max:.4f}ms per conversion)")
        print(f"  Meets <10ms requirement: {'✓' if meets_requirement else '✗'}")
        print()

        results.append({
            'name': name,
            'avg_per_op': per_op_avg,
            'min_per_op': per_op_min,
            'max_per_op': per_op_max,
            'meets_requirement': meets_requirement
        })

    # Summary analysis
    print("=" * 60)
    print("REQUIREMENT ANALYSIS")
    print("=" * 60)

    compliant_solutions = [r for r in results if r['meets_requirement']]

    print(f"Solutions meeting <10ms requirement: {len(compliant_solutions)}/{len(results)}")
    print()

    if compliant_solutions:
        fastest = min(compliant_solutions, key=lambda x: x['avg_per_op'])
        print(f"Fastest compliant solution: {fastest['name']}")
        print(f"  Average time per conversion: {fastest['avg_per_op']:.4f}ms")
        print()

        # Daily volume calculation
        daily_conversions = 1_000_000
        daily_processing_time = (fastest['avg_per_op'] / 1000) * daily_conversions
        print(f"Estimated daily processing time for {daily_conversions:,} conversions:")
        print(f"  {daily_processing_time:.2f} seconds ({daily_processing_time/60:.2f} minutes)")
        print()

        # Concurrency analysis
        max_concurrent = 10.0 / fastest['avg_per_op']  # 10ms budget
        print(f"Theoretical max concurrent conversions within 10ms: {max_concurrent:.1f}")

    return results


def test_correctness():
    """Test correctness of implementations."""
    print("=" * 60)
    print("CORRECTNESS VALIDATION")
    print("=" * 60)

    test_cases = [
        (1, 'I'), (4, 'IV'), (9, 'IX'), (27, 'XXVII'),
        (48, 'XLVIII'), (59, 'LIX'), (93, 'XCIII'),
        (141, 'CXLI'), (163, 'CLXIII'), (402, 'CDII'),
        (575, 'DLXXV'), (911, 'CMXI'), (1024, 'MXXIV'),
        (3000, 'MMM'), (3999, 'MMMCMXCIX')
    ]

    functions = [
        ("Lookup Table", int_to_roman_lookup, roman_to_int_lookup),
        ("Array-Based", int_to_roman_array, roman_to_int_array),
    ]

    all_correct = True

    for func_name, int_to_roman, roman_to_int in functions:
        print(f"Testing {func_name} implementation:")
        correct = 0

        for num, expected_roman in test_cases:
            # Test int to roman
            result_roman = int_to_roman(num)
            roman_correct = result_roman == expected_roman

            # Test roman to int
            result_int = roman_to_int(expected_roman)
            int_correct = result_int == num

            if roman_correct and int_correct:
                correct += 1
            else:
                print(f"  ✗ {num} -> {result_roman} (expected {expected_roman})")
                print(f"    {expected_roman} -> {result_int} (expected {num})")
                all_correct = False

        print(f"  Correct: {correct}/{len(test_cases)} ({'✓' if correct == len(test_cases) else '✗'})")
        print()

    return all_correct


if __name__ == "__main__":
    # Run correctness tests first
    print("Starting validation...")
    print()

    correctness_passed = test_correctness()

    if correctness_passed:
        print("✓ All correctness tests passed. Proceeding with performance validation.")
        print()
        performance_results = validate_performance_requirements()
    else:
        print("✗ Correctness tests failed. Skipping performance validation.")
        performance_results = []

    print("=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)