"""
Intentionally incorrect implementation #1: Incomplete subtractive notation
This implementation fails to handle subtractive cases properly
"""


class RomanConverter:
    def __init__(self):
        self.roman_numerals = [
            (1000, 'M'),
            (500, 'D'),
            (100, 'C'),
            (50, 'L'),
            (10, 'X'),
            (5, 'V'),
            (1, 'I')
        ]

    def to_roman(self, num):
        if not isinstance(num, int):
            raise TypeError("Input must be an integer")
        if num <= 0 or num >= 4000:
            raise ValueError("Number must be between 1 and 3999")

        result = ""
        for value, numeral in self.roman_numerals:
            count = num // value
            result += numeral * count
            num -= value * count
        return result

    def from_roman(self, roman):
        if not isinstance(roman, str):
            raise TypeError("Input must be a string")
        if not roman:
            raise ValueError("Empty string")

        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        total = 0
        prev_value = 0

        for char in reversed(roman):
            if char not in roman_values:
                raise ValueError(f"Invalid Roman numeral character: {char}")

            value = roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        return total