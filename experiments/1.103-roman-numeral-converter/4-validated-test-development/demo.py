#!/usr/bin/env python3
"""
Demonstration of the Roman numeral converter with comprehensive test validation
"""

from roman_converter import RomanConverter


def main():
    converter = RomanConverter()

    print("=== Roman Numeral Converter Demo ===\n")

    # Test some conversions
    test_numbers = [1, 4, 9, 27, 48, 99, 444, 999, 1066, 1492, 1776, 1984, 2024, 3999]

    print("Integer to Roman conversions:")
    print("=" * 30)
    for num in test_numbers:
        roman = converter.to_roman(num)
        print(f"{num:4d} -> {roman}")

    print("\nRoman to Integer conversions:")
    print("=" * 30)
    test_romans = ["I", "IV", "IX", "XLVIII", "XCIX", "CDXLIV", "CMXCIX",
                   "MLXVI", "MCDXCII", "MDCCLXXVI", "MCMLXXXIV", "MMXXIV", "MMMCMXCIX"]

    for roman in test_romans:
        num = converter.from_roman(roman)
        print(f"{roman:>10} -> {num}")

    print("\nRound-trip validation:")
    print("=" * 25)
    for num in [42, 127, 555, 1337, 2999]:
        roman = converter.to_roman(num)
        back_to_int = converter.from_roman(roman)
        status = "✓" if num == back_to_int else "✗"
        print(f"{num} -> {roman} -> {back_to_int} {status}")

    print("\nError handling examples:")
    print("=" * 25)

    # Test invalid inputs
    invalid_tests = [
        ("Zero", lambda: converter.to_roman(0)),
        ("Negative", lambda: converter.to_roman(-5)),
        ("Too large", lambda: converter.to_roman(4000)),
        ("String input to to_roman", lambda: converter.to_roman("42")),
        ("Empty string", lambda: converter.from_roman("")),
        ("Invalid chars", lambda: converter.from_roman("ABC")),
        ("Invalid pattern", lambda: converter.from_roman("IIII")),
        ("Invalid subtractive", lambda: converter.from_roman("IC")),
        ("Lowercase", lambda: converter.from_roman("iv")),
    ]

    for test_name, test_func in invalid_tests:
        try:
            result = test_func()
            print(f"{test_name:25}: Unexpected success - {result}")
        except (ValueError, TypeError) as e:
            print(f"{test_name:25}: Correctly rejected - {type(e).__name__}")
        except Exception as e:
            print(f"{test_name:25}: Unexpected error - {type(e).__name__}")


if __name__ == "__main__":
    main()