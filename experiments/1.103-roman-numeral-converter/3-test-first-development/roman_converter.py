#!/usr/bin/env python3
"""
Roman numeral converter implementation using TDD approach.
"""


class RomanConverter:
    """Converts between integers and Roman numerals."""

    def __init__(self):
        """Initialize the converter with Roman numeral mappings."""
        # Ordered list for int-to-roman conversion (largest to smallest)
        self._int_to_roman_values = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]

        # Dictionary for roman-to-int conversion
        self._roman_to_int_values = {}
        for value, numeral in self._int_to_roman_values:
            self._roman_to_int_values[numeral] = value

    def int_to_roman(self, num):
        """Convert integer to Roman numeral.

        Args:
            num (int): Integer to convert (1-3999)

        Returns:
            str: Roman numeral representation
        """
        if not isinstance(num, int) or num < 1 or num > 3999:
            raise ValueError("Input must be an integer between 1 and 3999")

        result = ""
        for value, numeral in self._int_to_roman_values:
            count = num // value
            result += numeral * count
            num -= value * count

        return result

    def roman_to_int(self, roman):
        """Convert Roman numeral to integer.

        Args:
            roman (str): Roman numeral to convert

        Returns:
            int: Integer representation
        """
        if not isinstance(roman, str):
            raise ValueError("Input must be a string")

        roman = roman.upper().strip()
        result = 0
        i = 0

        while i < len(roman):
            # Check for two-character combinations first
            if i + 1 < len(roman) and roman[i:i+2] in self._roman_to_int_values:
                result += self._roman_to_int_values[roman[i:i+2]]
                i += 2
            # Then check for single characters
            elif roman[i] in self._roman_to_int_values:
                result += self._roman_to_int_values[roman[i]]
                i += 1
            else:
                raise ValueError(f"Invalid Roman numeral character: {roman[i]}")

        return result