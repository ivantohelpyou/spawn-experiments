#!/usr/bin/env python3
"""
Quick performance test for roman numeral conversion libraries
Testing response time requirement: <10ms per conversion
High-volume usage: 1,000,000+ conversions per day
"""

import time
import statistics
from typing import List, Tuple, Callable

def test_native_implementation():
    """Simple native implementation for baseline comparison"""

    def int_to_roman(num: int) -> str:
        """Convert integer to roman numeral"""
        values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

        result = ""
        for i, value in enumerate(values):
            count = num // value
            result += numerals[i] * count
            num %= value
        return result

    def roman_to_int(s: str) -> int:
        """Convert roman numeral to integer"""
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0

        for char in reversed(s):
            value = roman_map[char]
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        return result

    return int_to_roman, roman_to_int

def benchmark_conversion(to_roman_func: Callable, from_roman_func: Callable,
                        test_numbers: List[int], iterations: int = 1000) -> Tuple[float, float]:
    """Benchmark conversion functions"""

    # Test int to roman conversion
    start_time = time.perf_counter()
    for _ in range(iterations):
        for num in test_numbers:
            to_roman_func(num)
    int_to_roman_time = (time.perf_counter() - start_time) / (iterations * len(test_numbers))

    # Convert test numbers to roman for reverse testing
    roman_numbers = [to_roman_func(num) for num in test_numbers]

    # Test roman to int conversion
    start_time = time.perf_counter()
    for _ in range(iterations):
        for roman in roman_numbers:
            from_roman_func(roman)
    roman_to_int_time = (time.perf_counter() - start_time) / (iterations * len(roman_numbers))

    return int_to_roman_time, roman_to_int_time

def main():
    # Test data - representative numbers for real-world usage
    test_numbers = [1, 5, 10, 50, 100, 500, 1000, 1994, 2023, 3999]

    print("Roman Numeral Conversion Performance Test")
    print("=" * 50)
    print(f"Testing with {len(test_numbers)} numbers: {test_numbers}")
    print(f"Target: <10ms per conversion")
    print()

    # Test native implementation
    print("Testing Native Implementation...")
    int_to_roman, roman_to_int = test_native_implementation()

    # Validate correctness first
    print("Validation:")
    for num in [1, 5, 10, 50, 100, 500, 1000, 1994, 2023, 3999]:
        roman = int_to_roman(num)
        back_to_int = roman_to_int(roman)
        print(f"  {num} -> {roman} -> {back_to_int} {'✓' if num == back_to_int else '✗'}")

    print("\nPerformance Results:")

    # Run performance tests
    int_to_roman_time, roman_to_int_time = benchmark_conversion(
        int_to_roman, roman_to_int, test_numbers, 1000
    )

    print(f"Native Implementation:")
    print(f"  Int to Roman: {int_to_roman_time*1000:.6f}ms per conversion")
    print(f"  Roman to Int: {roman_to_int_time*1000:.6f}ms per conversion")
    print(f"  Meets <10ms requirement: {'✓' if max(int_to_roman_time*1000, roman_to_int_time*1000) < 10 else '✗'}")

    # Test library availability
    print("\nLibrary Availability Check:")

    libraries_to_test = [
        'roman',
        'roman_numerals',
        'RomanPy',
        'roman_numerals_converter'
    ]

    available_libraries = []
    for lib in libraries_to_test:
        try:
            __import__(lib)
            available_libraries.append(lib)
            print(f"  {lib}: ✓ Available")
        except ImportError:
            print(f"  {lib}: ✗ Not installed")

    if not available_libraries:
        print("\nNo external libraries installed for comparison.")
        print("Install with: pip install roman roman-numerals RomanPy")

    print("\nConclusion:")
    print("Native implementation provides sub-millisecond performance,")
    print("easily meeting the <10ms requirement for high-volume usage.")

if __name__ == "__main__":
    main()