"""
Roman Numeral Conversion System

A comprehensive implementation for bidirectional conversion between integers and Roman numerals
for the range 1-3999, following classical Roman numeral rules.

This module provides functions to convert integers to Roman numerals and Roman numerals back
to integers with full validation and error handling.
"""

import re
from typing import Dict, List, Tuple


class RomanNumeralConverter:
    """
    Roman numeral conversion system implementing bidirectional conversion
    between integers (1-3999) and Roman numerals.

    This class follows classical Roman numeral rules including proper subtractive
    notation and validates all inputs according to the specification.
    """

    # Mapping for integer to Roman conversion (descending order)
    # Includes subtractive combinations for efficient conversion
    _INT_TO_ROMAN_MAP: List[Tuple[int, str]] = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    # Mapping for Roman to integer conversion
    _ROMAN_TO_INT_MAP: Dict[str, int] = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    # Valid subtractive combinations
    _SUBTRACTIVE_MAP: Dict[str, int] = {
        'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900
    }

    # Regex pattern for valid Roman numerals
    _VALID_ROMAN_PATTERN = re.compile(
        r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    )

    def __init__(self):
        """Initialize the Roman numeral converter."""
        pass

    def int_to_roman(self, num: int) -> str:
        """
        Convert an integer to Roman numeral.

        Args:
            num (int): Integer between 1 and 3999 inclusive

        Returns:
            str: Roman numeral representation

        Raises:
            TypeError: If num is not an integer
            ValueError: If num is outside the valid range [1, 3999]

        Examples:
            >>> converter = RomanNumeralConverter()
            >>> converter.int_to_roman(1994)
            'MCMXCIV'
            >>> converter.int_to_roman(58)
            'LVIII'
        """
        self._validate_integer_input(num)

        result = []
        remaining = num

        for value, numeral in self._INT_TO_ROMAN_MAP:
            count = remaining // value
            if count:
                result.append(numeral * count)
                remaining %= value

        return ''.join(result)

    def roman_to_int(self, roman: str) -> int:
        """
        Convert a Roman numeral to integer.

        Args:
            roman (str): Valid Roman numeral string

        Returns:
            int: Integer value between 1 and 3999

        Raises:
            TypeError: If roman is not a string
            ValueError: If roman is not a valid Roman numeral

        Examples:
            >>> converter = RomanNumeralConverter()
            >>> converter.roman_to_int('MCMXCIV')
            1994
            >>> converter.roman_to_int('lviii')
            58
        """
        self._validate_roman_input(roman)

        # Normalize to uppercase
        roman = roman.upper().strip()

        # Check if it matches the valid pattern
        if not self._VALID_ROMAN_PATTERN.match(roman):
            raise ValueError(f"Invalid Roman numeral: {roman}")

        result = 0
        i = 0

        # Process subtractive combinations first
        while i < len(roman) - 1:
            two_char = roman[i:i+2]
            if two_char in self._SUBTRACTIVE_MAP:
                result += self._SUBTRACTIVE_MAP[two_char]
                i += 2
            else:
                result += self._ROMAN_TO_INT_MAP[roman[i]]
                i += 1

        # Process the last character if not part of a subtractive combination
        if i < len(roman):
            result += self._ROMAN_TO_INT_MAP[roman[i]]

        # Validate the result is in range
        if result < 1 or result > 3999:
            raise ValueError(f"Invalid Roman numeral: {roman}")

        return result

    def is_valid_roman(self, roman: str) -> bool:
        """
        Check if a string is a valid Roman numeral.

        Args:
            roman (str): String to validate

        Returns:
            bool: True if valid, False otherwise

        Examples:
            >>> converter = RomanNumeralConverter()
            >>> converter.is_valid_roman('XIV')
            True
            >>> converter.is_valid_roman('IIII')
            False
        """
        try:
            self._validate_roman_input(roman)
            roman = roman.upper().strip()
            return bool(self._VALID_ROMAN_PATTERN.match(roman))
        except (TypeError, ValueError):
            return False

    def _validate_integer_input(self, num: int) -> None:
        """
        Validate integer input for conversion.

        Args:
            num: Input to validate

        Raises:
            TypeError: If num is not an integer
            ValueError: If num is outside valid range
        """
        # Check for bool first since bool is a subclass of int in Python
        if isinstance(num, bool) or not isinstance(num, int):
            raise TypeError(f"Expected integer, got {type(num).__name__}")

        if num < 1 or num > 3999:
            raise ValueError(f"Integer must be between 1 and 3999, got: {num}")

    def _validate_roman_input(self, roman: str) -> None:
        """
        Validate Roman numeral string input.

        Args:
            roman: Input to validate

        Raises:
            TypeError: If roman is not a string
            ValueError: If roman is empty or contains invalid characters
        """
        if not isinstance(roman, str):
            raise TypeError(f"Expected string, got {type(roman).__name__}")

        if not roman or not roman.strip():
            raise ValueError("Roman numeral cannot be empty")

        # Check for invalid characters
        normalized = roman.upper().strip()
        valid_chars = set('IVXLCDM')
        if not all(char in valid_chars for char in normalized):
            raise ValueError(f"Invalid Roman numeral: {roman}")


# Convenience functions for direct use
def int_to_roman(num: int) -> str:
    """
    Convert an integer to Roman numeral.

    Args:
        num (int): Integer between 1 and 3999 inclusive

    Returns:
        str: Roman numeral representation

    Raises:
        TypeError: If num is not an integer
        ValueError: If num is outside the valid range [1, 3999]

    Examples:
        >>> int_to_roman(1994)
        'MCMXCIV'
        >>> int_to_roman(58)
        'LVIII'
    """
    converter = RomanNumeralConverter()
    return converter.int_to_roman(num)


def roman_to_int(roman: str) -> int:
    """
    Convert a Roman numeral to integer.

    Args:
        roman (str): Valid Roman numeral string

    Returns:
        int: Integer value between 1 and 3999

    Raises:
        TypeError: If roman is not a string
        ValueError: If roman is not a valid Roman numeral

    Examples:
        >>> roman_to_int('MCMXCIV')
        1994
        >>> roman_to_int('lviii')
        58
    """
    converter = RomanNumeralConverter()
    return converter.roman_to_int(roman)


def is_valid_roman(roman: str) -> bool:
    """
    Check if a string is a valid Roman numeral.

    Args:
        roman (str): String to validate

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> is_valid_roman('XIV')
        True
        >>> is_valid_roman('IIII')
        False
    """
    converter = RomanNumeralConverter()
    return converter.is_valid_roman(roman)


if __name__ == "__main__":
    # Example usage and basic testing
    converter = RomanNumeralConverter()

    # Test some conversions
    test_cases = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000, 1994, 3999]

    print("Integer to Roman conversions:")
    for num in test_cases:
        roman = converter.int_to_roman(num)
        back_to_int = converter.roman_to_int(roman)
        print(f"{num:4d} → {roman:12s} → {back_to_int:4d} ✓" if num == back_to_int else f"{num:4d} → {roman:12s} → {back_to_int:4d} ✗")

    print("\nRoman to Integer conversions:")
    roman_cases = ['I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'XC', 'C', 'CD', 'D', 'CM', 'M', 'MCMXCIV', 'MMMCMXCIX']

    for roman in roman_cases:
        num = converter.roman_to_int(roman)
        back_to_roman = converter.int_to_roman(num)
        print(f"{roman:12s} → {num:4d} → {back_to_roman:12s} ✓" if roman == back_to_roman else f"{roman:12s} → {num:4d} → {back_to_roman:12s} ✗")