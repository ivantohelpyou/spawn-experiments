#!/usr/bin/env python3
"""
Roman Numeral Converter - Interactive Demonstration

This script demonstrates the full functionality of the Roman numeral conversion system,
including conversions, validation, error handling, and performance testing.
"""

import time
import random
from roman_numeral_converter import RomanNumeralConverter, int_to_roman, roman_to_int, is_valid_roman


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subheader(title):
    """Print a formatted subheader."""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")


def demo_basic_conversions():
    """Demonstrate basic integer to Roman numeral conversions."""
    print_subheader("Basic Integer to Roman Conversions")

    test_cases = [
        (1, "Basic unit"), (4, "Subtractive IV"), (5, "Basic five"),
        (9, "Subtractive IX"), (10, "Basic ten"), (40, "Subtractive XL"),
        (50, "Basic fifty"), (90, "Subtractive XC"), (100, "Basic hundred"),
        (400, "Subtractive CD"), (500, "Basic five hundred"),
        (900, "Subtractive CM"), (1000, "Basic thousand"),
        (1994, "Complex number"), (3999, "Maximum value")
    ]

    for num, description in test_cases:
        roman = int_to_roman(num)
        print(f"{num:4d} → {roman:12s} ({description})")


def demo_roman_parsing():
    """Demonstrate Roman numeral to integer parsing."""
    print_subheader("Roman Numeral to Integer Conversions")

    test_cases = [
        ("I", "Basic unit"), ("IV", "Subtractive four"), ("V", "Basic five"),
        ("IX", "Subtractive nine"), ("X", "Basic ten"), ("XL", "Subtractive forty"),
        ("L", "Basic fifty"), ("XC", "Subtractive ninety"), ("C", "Basic hundred"),
        ("CD", "Subtractive four hundred"), ("D", "Basic five hundred"),
        ("CM", "Subtractive nine hundred"), ("M", "Basic thousand"),
        ("MCMXCIV", "Complex number"), ("MMMCMXCIX", "Maximum value")
    ]

    for roman, description in test_cases:
        num = roman_to_int(roman)
        print(f"{roman:12s} → {num:4d} ({description})")


def demo_case_insensitivity():
    """Demonstrate case insensitive parsing."""
    print_subheader("Case Insensitive Parsing")

    test_cases = [
        "XIV", "xiv", "XiV", "mcmxciv", "MCMXCIV", "MmMcMxCiX"
    ]

    for roman in test_cases:
        try:
            num = roman_to_int(roman)
            print(f"{roman:12s} → {num:4d}")
        except ValueError as e:
            print(f"{roman:12s} → ERROR: {e}")


def demo_roundtrip_conversion():
    """Demonstrate roundtrip conversion accuracy."""
    print_subheader("Roundtrip Conversion Accuracy")

    test_numbers = [1, 4, 27, 48, 99, 156, 333, 444, 555, 888, 999, 1776, 1994, 2023, 3999]

    print("Original → Roman → Back to Integer")
    for num in test_numbers:
        roman = int_to_roman(num)
        back_to_int = roman_to_int(roman)
        status = "✓" if num == back_to_int else "✗"
        print(f"{num:4d} → {roman:12s} → {back_to_int:4d} {status}")


def demo_validation():
    """Demonstrate input validation."""
    print_subheader("Roman Numeral Validation")

    test_cases = [
        ("XIV", True, "Valid standard numeral"),
        ("MCMXC", True, "Valid complex numeral"),
        ("IIII", False, "Too many consecutive I's"),
        ("VV", False, "Repeated V"),
        ("IL", False, "Invalid subtractive combination"),
        ("ABC", False, "Invalid characters"),
        ("", False, "Empty string"),
        ("XLIXL", False, "Repeated subtractive pattern")
    ]

    for roman, expected, description in test_cases:
        is_valid = is_valid_roman(roman)
        status = "✓" if is_valid == expected else "✗"
        print(f"{roman:8s} → {str(is_valid):5s} {status} ({description})")


def demo_error_handling():
    """Demonstrate comprehensive error handling."""
    print_subheader("Error Handling Examples")

    # Integer conversion errors
    print("Integer to Roman Errors:")
    error_cases = [
        (0, "Zero (below range)"),
        (-5, "Negative number"),
        (4000, "Above range"),
        ("5", "String instead of int"),
        (3.14, "Float instead of int"),
        (True, "Boolean (treated as int in Python)")
    ]

    for invalid_input, description in error_cases:
        try:
            result = int_to_roman(invalid_input)
            print(f"  {str(invalid_input):8s} → {result} (UNEXPECTED SUCCESS)")
        except (TypeError, ValueError) as e:
            print(f"  {str(invalid_input):8s} → {type(e).__name__}: {e}")

    # Roman parsing errors
    print("\nRoman to Integer Errors:")
    error_cases = [
        ("", "Empty string"),
        ("   ", "Whitespace only"),
        ("IIII", "Invalid pattern"),
        ("VX", "Invalid subtractive"),
        ("ABC", "Invalid characters"),
        (42, "Integer instead of string")
    ]

    for invalid_input, description in error_cases:
        try:
            result = roman_to_int(invalid_input)
            print(f"  {str(invalid_input):8s} → {result} (UNEXPECTED SUCCESS)")
        except (TypeError, ValueError) as e:
            print(f"  {str(invalid_input):8s} → {type(e).__name__}: {e}")


def demo_performance():
    """Demonstrate performance benchmarks."""
    print_subheader("Performance Benchmarks")

    # Test integer to Roman performance
    numbers = random.sample(range(1, 4000), 1000)
    start_time = time.time()

    for num in numbers:
        int_to_roman(num)

    int_to_roman_time = time.time() - start_time

    # Test Roman to integer performance
    romans = [int_to_roman(num) for num in random.sample(range(1, 4000), 1000)]
    start_time = time.time()

    for roman in romans:
        roman_to_int(roman)

    roman_to_int_time = time.time() - start_time

    print(f"1000 integer → Roman conversions: {int_to_roman_time*1000:.2f}ms")
    print(f"1000 Roman → integer conversions: {roman_to_int_time*1000:.2f}ms")
    print(f"Total conversion time: {(int_to_roman_time + roman_to_int_time)*1000:.2f}ms")


def demo_complex_examples():
    """Demonstrate complex real-world examples."""
    print_subheader("Complex Real-World Examples")

    examples = [
        (476, "Fall of Western Roman Empire"),
        (800, "Charlemagne crowned Emperor"),
        (1066, "Norman Conquest of England"),
        (1215, "Magna Carta signed"),
        (1453, "Fall of Constantinople"),
        (1492, "Columbus reaches Americas"),
        (1776, "American Declaration of Independence"),
        (1789, "French Revolution begins"),
        (1969, "Moon landing"),
        (2023, "Current year (at time of writing)")
    ]

    print("Historical Dates in Roman Numerals:")
    for year, event in examples:
        roman = int_to_roman(year)
        print(f"{year} AD → {roman:12s} ({event})")


def demo_interactive_mode():
    """Run interactive conversion mode."""
    print_subheader("Interactive Mode")
    print("Enter integers (1-3999) or Roman numerals to convert.")
    print("Type 'quit' to exit interactive mode.")

    while True:
        try:
            user_input = input("\nEnter number or Roman numeral: ").strip()

            if user_input.lower() == 'quit':
                break

            # Try to parse as integer first
            try:
                num = int(user_input)
                roman = int_to_roman(num)
                print(f"  {num} → {roman}")
            except ValueError:
                # Try to parse as Roman numeral
                try:
                    num = roman_to_int(user_input)
                    print(f"  {user_input.upper()} → {num}")
                except ValueError as e:
                    print(f"  Error: {e}")

        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except EOFError:
            print("\nExiting interactive mode...")
            break


def main():
    """Run the complete demonstration."""
    print_header("Roman Numeral Converter - Comprehensive Demonstration")
    print("This demo showcases all features of the specification-driven implementation.")

    # Core functionality demos
    demo_basic_conversions()
    demo_roman_parsing()
    demo_case_insensitivity()
    demo_roundtrip_conversion()

    # Validation and error handling
    demo_validation()
    demo_error_handling()

    # Performance and complex examples
    demo_performance()
    demo_complex_examples()

    # Interactive mode
    print_header("Interactive Conversion")
    demo_interactive_mode()

    print_header("Demo Complete")
    print("Thank you for exploring the Roman Numeral Converter!")
    print("For more details, see SPECIFICATION.md and README.md")


if __name__ == "__main__":
    main()