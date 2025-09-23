#!/usr/bin/env python3
"""
Performance comparison between native implementation and roman library
Testing response time requirement: <10ms per conversion
"""

import time
import statistics
import sys
sys.path.insert(0, './test_env/lib/python3.12/site-packages')

try:
    import roman
    ROMAN_AVAILABLE = True
except ImportError:
    ROMAN_AVAILABLE = False

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

def benchmark_conversion(to_roman_func, from_roman_func, test_numbers, iterations=1000):
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
        for roman_num in roman_numbers:
            from_roman_func(roman_num)
    roman_to_int_time = (time.perf_counter() - start_time) / (iterations * len(roman_numbers))

    return int_to_roman_time, roman_to_int_time

def main():
    # Test data - representative numbers for real-world usage
    test_numbers = [1, 5, 10, 50, 100, 500, 1000, 1994, 2023, 3999]

    print("Roman Numeral Library Performance Comparison")
    print("=" * 55)
    print(f"Testing with {len(test_numbers)} numbers: {test_numbers}")
    print(f"Target: <10ms per conversion")
    print()

    results = []

    # Test native implementation
    print("1. Native Implementation")
    int_to_roman, roman_to_int = test_native_implementation()

    # Validate correctness
    validation_pass = True
    for num in test_numbers[:5]:  # Quick validation
        roman_str = int_to_roman(num)
        back_to_int = roman_to_int(roman_str)
        if num != back_to_int:
            validation_pass = False
            break

    if validation_pass:
        int_to_roman_time, roman_to_int_time = benchmark_conversion(
            int_to_roman, roman_to_int, test_numbers, 1000
        )

        print(f"   Int to Roman: {int_to_roman_time*1000:.6f}ms per conversion")
        print(f"   Roman to Int: {roman_to_int_time*1000:.6f}ms per conversion")
        max_time = max(int_to_roman_time*1000, roman_to_int_time*1000)
        print(f"   Meets <10ms: {'✓' if max_time < 10 else '✗'}")

        results.append(("Native", max_time, "✓" if max_time < 10 else "✗"))
    else:
        print("   ✗ Validation failed")

    print()

    # Test roman library if available
    if ROMAN_AVAILABLE:
        print("2. Roman Library (PyPI)")

        # Validate correctness
        validation_pass = True
        try:
            for num in test_numbers[:5]:  # Quick validation
                roman_str = roman.toRoman(num)
                back_to_int = roman.fromRoman(roman_str)
                if num != back_to_int:
                    validation_pass = False
                    break
        except Exception as e:
            print(f"   ✗ Library error: {e}")
            validation_pass = False

        if validation_pass:
            int_to_roman_time, roman_to_int_time = benchmark_conversion(
                roman.toRoman, roman.fromRoman, test_numbers, 1000
            )

            print(f"   Int to Roman: {int_to_roman_time*1000:.6f}ms per conversion")
            print(f"   Roman to Int: {roman_to_int_time*1000:.6f}ms per conversion")
            max_time = max(int_to_roman_time*1000, roman_to_int_time*1000)
            print(f"   Meets <10ms: {'✓' if max_time < 10 else '✗'}")

            results.append(("Roman Library", max_time, "✓" if max_time < 10 else "✗"))
        else:
            print("   ✗ Validation failed")
    else:
        print("2. Roman Library: Not available")

    print()
    print("Summary:")
    print("-" * 40)
    for name, max_time, meets_req in results:
        print(f"{name:15} | {max_time:8.6f}ms | {meets_req}")

    print()
    print("Recommendation:")
    if results:
        fastest = min(results, key=lambda x: x[1])
        print(f"Fastest: {fastest[0]} ({fastest[1]:.6f}ms)")

        if all(result[2] == "✓" for result in results):
            print("All implementations meet the <10ms requirement.")
            print("Choose based on other factors (maintenance, features, dependencies).")
        else:
            passing = [r for r in results if r[2] == "✓"]
            if passing:
                print(f"Use {passing[0][0]} - meets performance requirements.")
            else:
                print("None meet the <10ms requirement. Consider optimization.")

if __name__ == "__main__":
    main()