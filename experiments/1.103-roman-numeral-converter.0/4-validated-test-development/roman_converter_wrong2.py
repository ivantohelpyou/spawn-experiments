"""
Intentionally incorrect implementation #2: No input validation
This implementation lacks proper input validation and error handling
"""


class RomanConverter:
    def __init__(self):
        self.values = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]

    def to_roman(self, num):
        # Missing input validation!
        result = ""
        for value, numeral in self.values:
            count = num // value
            result += numeral * count
            num -= value * count
        return result

    def from_roman(self, roman):
        # Missing input validation!
        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        total = 0
        prev_value = 0

        for char in reversed(roman):
            value = roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        return total