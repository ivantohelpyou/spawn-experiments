"""
Roman Numeral Converter
Converts integers to Roman numerals and Roman numerals back to integers.
Handles numbers 1-3999.
"""

def int_to_roman(num):
    """Convert integer to Roman numeral."""
    if not 1 <= num <= 3999:
        raise ValueError("Number must be between 1 and 3999")

    # Define mapping from largest to smallest
    values = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    result = ''
    for value, numeral in values:
        count = num // value
        if count:
            result += numeral * count
            num -= value * count

    return result


def roman_to_int(roman):
    """Convert Roman numeral to integer."""
    if not roman:
        raise ValueError("Roman numeral cannot be empty")

    # Define mapping
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    # Process from right to left
    for char in reversed(roman.upper()):
        if char not in roman_values:
            raise ValueError(f"Invalid Roman numeral character: {char}")

        value = roman_values[char]

        # If current value is less than previous, subtract it
        if value < prev_value:
            total -= value
        else:
            total += value

        prev_value = value

    return total


def test_roman_numerals():
    """Basic tests for Roman numeral conversion."""
    print("Testing Roman numeral conversion...")

    # Test cases: (integer, expected_roman)
    test_cases = [
        (1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'),
        (9, 'IX'), (10, 'X'), (11, 'XI'), (19, 'XIX'), (20, 'XX'),
        (40, 'XL'), (50, 'L'), (90, 'XC'), (100, 'C'), (400, 'CD'),
        (500, 'D'), (900, 'CM'), (1000, 'M'), (1994, 'MCMXCIV'),
        (3999, 'MMMCMXCIX')
    ]

    all_passed = True

    for num, expected_roman in test_cases:
        # Test int to roman
        result_roman = int_to_roman(num)
        if result_roman != expected_roman:
            print(f"FAIL: int_to_roman({num}) = {result_roman}, expected {expected_roman}")
            all_passed = False
        else:
            print(f"PASS: {num} -> {result_roman}")

        # Test roman to int
        result_int = roman_to_int(expected_roman)
        if result_int != num:
            print(f"FAIL: roman_to_int({expected_roman}) = {result_int}, expected {num}")
            all_passed = False
        else:
            print(f"PASS: {expected_roman} -> {result_int}")

    # Test edge cases
    try:
        int_to_roman(0)
        print("FAIL: Should raise error for 0")
        all_passed = False
    except ValueError:
        print("PASS: Correctly rejects 0")

    try:
        int_to_roman(4000)
        print("FAIL: Should raise error for 4000")
        all_passed = False
    except ValueError:
        print("PASS: Correctly rejects 4000")

    try:
        roman_to_int("Z")
        print("FAIL: Should raise error for invalid character")
        all_passed = False
    except ValueError:
        print("PASS: Correctly rejects invalid character")

    if all_passed:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")

    return all_passed


if __name__ == "__main__":
    test_roman_numerals()