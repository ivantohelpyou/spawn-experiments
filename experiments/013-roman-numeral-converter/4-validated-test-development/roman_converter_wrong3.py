"""
Intentionally incorrect implementation #3: Wrong conversion logic
This implementation has incorrect logic for Roman numeral parsing
"""


class RomanConverter:
    def __init__(self):
        self.values = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]

    def to_roman(self, num):
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
        if not isinstance(roman, str):
            raise TypeError("Input must be a string")
        if not roman:
            raise ValueError("Empty string")

        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        total = 0
        # Wrong logic: just add all values without considering order
        for char in roman:
            if char not in roman_values:
                raise ValueError(f"Invalid Roman numeral character: {char}")
            total += roman_values[char]

        return total