"""
Correct Roman numeral converter implementation with comprehensive validation
Supports the range 1-3999 with proper subtractive notation
"""
import re


class RomanConverter:
    def __init__(self):
        # Roman numeral values in descending order with subtractive cases
        self.values = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]

        # Roman numeral character values
        self.roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        # Valid Roman numeral pattern (enforces proper structure)
        self.valid_pattern = re.compile(
            r'^M{0,3}'           # 0-3 thousands
            r'(CM|CD|D?C{0,3})'  # hundreds
            r'(XC|XL|L?X{0,3})'  # tens
            r'(IX|IV|V?I{0,3})$' # ones
        )

    def to_roman(self, num):
        """Convert integer to Roman numeral"""
        # Input validation
        if not isinstance(num, int):
            raise TypeError("Input must be an integer")
        if num <= 0 or num >= 4000:
            raise ValueError("Number must be between 1 and 3999")

        result = ""
        for value, numeral in self.values:
            count = num // value
            result += numeral * count
            num -= value * count

        return result

    def from_roman(self, roman):
        """Convert Roman numeral to integer"""
        # Input validation
        if not isinstance(roman, str):
            raise TypeError("Input must be a string")
        if not roman:
            raise ValueError("Empty string")

        # Check for valid characters
        for char in roman:
            if char not in self.roman_values:
                raise ValueError(f"Invalid Roman numeral character: {char}")

        # Check if the Roman numeral follows valid pattern
        if not self.valid_pattern.match(roman):
            raise ValueError(f"Invalid Roman numeral pattern: {roman}")

        # Convert using subtractive notation logic
        total = 0
        prev_value = 0

        for char in reversed(roman):
            value = self.roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        # Additional validation: ensure the conversion round-trips correctly
        # This catches invalid patterns that might pass the regex but are still wrong
        if self.to_roman(total) != roman:
            raise ValueError(f"Invalid Roman numeral: {roman}")

        return total