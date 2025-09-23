#!/usr/bin/env python3
"""
Performance comparison including existing Python libraries.
"""

import time
import statistics
from typing import Tuple, List

# Import the popular roman library
import roman

# Import our custom implementations
from performance_validation import (
    int_to_roman_lookup, roman_to_int_lookup,
    int_to_roman_array, roman_to_int_array,
    benchmark_function
)


def benchmark_library_solutions():
    """Compare performance of library vs custom implementations."""
    print("=" * 70)
    print("LIBRARY VS CUSTOM IMPLEMENTATION PERFORMANCE COMPARISON")
    print("=" * 70)
    print(f"Requirements: <10ms per conversion, 1M+ daily volume")
    print()

    # Test data
    test_integers = [1, 4, 9, 27, 48, 59, 93, 141, 163, 402, 575, 911, 1024, 3000, 3999]
    test_romans = [roman.toRoman(i) for i in test_integers]

    iterations = 1000
    operations_per_iteration = len(test_integers)

    print(f"Test Configuration:")
    print(f"- Test data size: {len(test_integers)} conversions per iteration")
    print(f"- Iterations: {iterations}")
    print(f"- Total operations: {iterations * operations_per_iteration}")
    print()

    # Test all solutions
    solutions = [
        ("roman library (int->roman)", roman.toRoman, test_integers),
        ("roman library (roman->int)", roman.fromRoman, test_romans),
        ("Custom Lookup (int->roman)", int_to_roman_lookup, test_integers),
        ("Custom Lookup (roman->int)", roman_to_int_lookup, test_romans),
        ("Custom Array (int->roman)", int_to_roman_array, test_integers),
        ("Custom Array (roman->int)", roman_to_int_array, test_romans),
    ]

    results = []

    for name, func, data in solutions:
        print(f"Testing: {name}")
        try:
            avg_time, min_time, max_time = benchmark_function(func, data, iterations)

            # Calculate per-operation time
            per_op_avg = avg_time / operations_per_iteration
            per_op_min = min_time / operations_per_iteration
            per_op_max = max_time / operations_per_iteration

            # Check requirement compliance
            meets_requirement = per_op_avg < 10.0

            print(f"  Average: {avg_time:.3f}ms total ({per_op_avg:.4f}ms per conversion)")
            print(f"  Min:     {min_time:.3f}ms total ({per_op_min:.4f}ms per conversion)")
            print(f"  Max:     {max_time:.3f}ms total ({per_op_max:.4f}ms per conversion)")
            print(f"  Meets <10ms requirement: {'✓' if meets_requirement else '✗'}")

            results.append({
                'name': name,
                'avg_per_op': per_op_avg,
                'min_per_op': per_op_min,
                'max_per_op': per_op_max,
                'meets_requirement': meets_requirement
            })

        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                'name': name,
                'avg_per_op': float('inf'),
                'min_per_op': float('inf'),
                'max_per_op': float('inf'),
                'meets_requirement': False
            })

        print()

    # Analysis
    print("=" * 70)
    print("COMPREHENSIVE ANALYSIS")
    print("=" * 70)

    # Group by conversion type
    int_to_roman_results = [r for r in results if 'int->roman' in r['name']]
    roman_to_int_results = [r for r in results if 'roman->int' in r['name']]

    print("INTEGER TO ROMAN CONVERSION:")
    int_to_roman_sorted = sorted(int_to_roman_results, key=lambda x: x['avg_per_op'])
    for i, result in enumerate(int_to_roman_sorted, 1):
        if result['meets_requirement']:
            print(f"  {i}. {result['name']}: {result['avg_per_op']:.4f}ms ✓")
        else:
            print(f"  {i}. {result['name']}: {result['avg_per_op']:.4f}ms ✗")

    print()
    print("ROMAN TO INTEGER CONVERSION:")
    roman_to_int_sorted = sorted(roman_to_int_results, key=lambda x: x['avg_per_op'])
    for i, result in enumerate(roman_to_int_sorted, 1):
        if result['meets_requirement']:
            print(f"  {i}. {result['name']}: {result['avg_per_op']:.4f}ms ✓")
        else:
            print(f"  {i}. {result['name']}: {result['avg_per_op']:.4f}ms ✗")

    print()

    # Overall recommendations
    all_compliant = [r for r in results if r['meets_requirement']]
    if all_compliant:
        fastest_overall = min(all_compliant, key=lambda x: x['avg_per_op'])
        print(f"FASTEST OVERALL: {fastest_overall['name']}")
        print(f"  Performance: {fastest_overall['avg_per_op']:.4f}ms per conversion")

        # Performance margin analysis
        margin = (10.0 - fastest_overall['avg_per_op']) / 10.0 * 100
        print(f"  Performance margin: {margin:.1f}% under requirement")

    return results


def test_library_correctness():
    """Test correctness of the roman library."""
    print("=" * 70)
    print("LIBRARY CORRECTNESS VALIDATION")
    print("=" * 70)

    test_cases = [
        (1, 'I'), (4, 'IV'), (9, 'IX'), (27, 'XXVII'),
        (48, 'XLVIII'), (59, 'LIX'), (93, 'XCIII'),
        (141, 'CXLI'), (163, 'CLXIII'), (402, 'CDII'),
        (575, 'DLXXV'), (911, 'CMXI'), (1024, 'MXXIV'),
        (3000, 'MMM'), (3999, 'MMMCMXCIX')
    ]

    print("Testing roman library implementation:")
    correct = 0

    for num, expected_roman in test_cases:
        try:
            # Test int to roman
            result_roman = roman.toRoman(num)
            roman_correct = result_roman == expected_roman

            # Test roman to int
            result_int = roman.fromRoman(expected_roman)
            int_correct = result_int == num

            if roman_correct and int_correct:
                correct += 1
            else:
                print(f"  ✗ {num} -> {result_roman} (expected {expected_roman})")
                print(f"    {expected_roman} -> {result_int} (expected {num})")

        except Exception as e:
            print(f"  ✗ Error with {num}/{expected_roman}: {e}")

    success_rate = correct / len(test_cases) * 100
    print(f"  Correct: {correct}/{len(test_cases)} ({success_rate:.1f}%) {'✓' if correct == len(test_cases) else '✗'}")
    print()

    return correct == len(test_cases)


if __name__ == "__main__":
    print("Starting comprehensive library comparison...")
    print()

    # Test library correctness first
    library_correct = test_library_correctness()

    if library_correct:
        print("✓ Library correctness validated. Proceeding with performance comparison.")
        print()
        results = benchmark_library_solutions()
    else:
        print("✗ Library correctness issues detected.")

    print("=" * 70)
    print("COMPARISON COMPLETE")
    print("=" * 70)