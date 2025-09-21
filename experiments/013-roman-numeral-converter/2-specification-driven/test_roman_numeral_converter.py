"""
Comprehensive test suite for Roman Numeral Converter

Tests all functionality specified in the SPECIFICATION.md document including:
- Valid conversions in both directions
- Error handling and validation
- Edge cases and boundary conditions
- Case insensitivity
- Performance requirements
"""

import pytest
import time
import random
from roman_numeral_converter import RomanNumeralConverter, int_to_roman, roman_to_int, is_valid_roman


class TestRomanNumeralConverter:
    """Test suite for RomanNumeralConverter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = RomanNumeralConverter()

    def test_int_to_roman_basic_symbols(self):
        """Test conversion of basic Roman numeral symbols."""
        test_cases = [
            (1, 'I'), (5, 'V'), (10, 'X'), (50, 'L'),
            (100, 'C'), (500, 'D'), (1000, 'M')
        ]
        for num, expected in test_cases:
            assert self.converter.int_to_roman(num) == expected

    def test_int_to_roman_subtractive_combinations(self):
        """Test conversion of subtractive combinations."""
        test_cases = [
            (4, 'IV'), (9, 'IX'), (40, 'XL'), (90, 'XC'),
            (400, 'CD'), (900, 'CM')
        ]
        for num, expected in test_cases:
            assert self.converter.int_to_roman(num) == expected

    def test_int_to_roman_complex_numbers(self):
        """Test conversion of complex numbers."""
        test_cases = [
            (14, 'XIV'), (24, 'XXIV'), (444, 'CDXLIV'),
            (19, 'XIX'), (29, 'XXIX'), (999, 'CMXCIX'),
            (1994, 'MCMXCIV'), (3888, 'MMMDCCCLXXXVIII'),
            (1776, 'MDCCLXXVI')
        ]
        for num, expected in test_cases:
            assert self.converter.int_to_roman(num) == expected

    def test_int_to_roman_boundary_values(self):
        """Test boundary values."""
        assert self.converter.int_to_roman(1) == 'I'
        assert self.converter.int_to_roman(3999) == 'MMMCMXCIX'

    def test_roman_to_int_basic_symbols(self):
        """Test parsing of basic Roman numeral symbols."""
        test_cases = [
            ('I', 1), ('V', 5), ('X', 10), ('L', 50),
            ('C', 100), ('D', 500), ('M', 1000)
        ]
        for roman, expected in test_cases:
            assert self.converter.roman_to_int(roman) == expected

    def test_roman_to_int_subtractive_combinations(self):
        """Test parsing of subtractive combinations."""
        test_cases = [
            ('IV', 4), ('IX', 9), ('XL', 40), ('XC', 90),
            ('CD', 400), ('CM', 900)
        ]
        for roman, expected in test_cases:
            assert self.converter.roman_to_int(roman) == expected

    def test_roman_to_int_complex_numbers(self):
        """Test parsing of complex Roman numerals."""
        test_cases = [
            ('XIV', 14), ('XXIV', 24), ('CDXLIV', 444),
            ('XIX', 19), ('XXIX', 29), ('CMXCIX', 999),
            ('MCMXCIV', 1994), ('MMMDCCCLXXXVIII', 3888),
            ('MDCCLXXVI', 1776)
        ]
        for roman, expected in test_cases:
            assert self.converter.roman_to_int(roman) == expected

    def test_roman_to_int_case_insensitivity(self):
        """Test case insensitive parsing."""
        test_cases = [
            ('i', 1), ('iv', 4), ('mcmxciv', 1994),
            ('MmMcMxCiX', 3999), ('XiV', 14)
        ]
        for roman, expected in test_cases:
            assert self.converter.roman_to_int(roman) == expected

    def test_roman_to_int_whitespace_handling(self):
        """Test handling of whitespace in input."""
        test_cases = [
            ('  XIV  ', 14), ('\tXIV\t', 14), ('\nXIV\n', 14)
        ]
        for roman, expected in test_cases:
            assert self.converter.roman_to_int(roman) == expected

    def test_roundtrip_conversion(self):
        """Test that int→roman→int produces the original number."""
        test_numbers = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000, 1994, 3999]
        test_numbers.extend(random.sample(range(1, 4000), 100))  # 100 random numbers

        for num in test_numbers:
            roman = self.converter.int_to_roman(num)
            back_to_int = self.converter.roman_to_int(roman)
            assert back_to_int == num, f"Roundtrip failed: {num} → {roman} → {back_to_int}"

    def test_int_to_roman_invalid_types(self):
        """Test error handling for invalid input types in int_to_roman."""
        invalid_inputs = ["5", 3.14, None, [], {}, True]
        for invalid_input in invalid_inputs:
            with pytest.raises(TypeError, match="Expected integer"):
                self.converter.int_to_roman(invalid_input)

    def test_int_to_roman_invalid_ranges(self):
        """Test error handling for out-of-range integers."""
        invalid_ranges = [0, -1, -100, 4000, 5000, 10000]
        for invalid_num in invalid_ranges:
            with pytest.raises(ValueError, match="Integer must be between 1 and 3999"):
                self.converter.int_to_roman(invalid_num)

    def test_roman_to_int_invalid_types(self):
        """Test error handling for invalid input types in roman_to_int."""
        invalid_inputs = [42, 3.14, None, [], {}, True]
        for invalid_input in invalid_inputs:
            with pytest.raises(TypeError, match="Expected string"):
                self.converter.roman_to_int(invalid_input)

    def test_roman_to_int_empty_strings(self):
        """Test error handling for empty strings."""
        empty_inputs = ["", "   ", "\t", "\n"]
        for empty_input in empty_inputs:
            with pytest.raises(ValueError, match="Roman numeral cannot be empty"):
                self.converter.roman_to_int(empty_input)

    def test_roman_to_int_invalid_characters(self):
        """Test error handling for invalid characters."""
        invalid_inputs = ["ABC", "XIV2", "X Y", "XIV!", "123"]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError, match="Invalid Roman numeral"):
                self.converter.roman_to_int(invalid_input)

    def test_roman_to_int_invalid_patterns(self):
        """Test error handling for invalid Roman numeral patterns."""
        invalid_patterns = [
            "IIII",      # More than 3 consecutive I's
            "XXXX",      # More than 3 consecutive X's
            "CCCC",      # More than 3 consecutive C's
            "MMMM",      # More than 3 consecutive M's (> 3999)
            "VV",        # Repeated V
            "LL",        # Repeated L
            "DD",        # Repeated D
            "IL",        # Invalid subtractive combination
            "IC",        # Invalid subtractive combination
            "ID",        # Invalid subtractive combination
            "IM",        # Invalid subtractive combination
            "VX",        # Invalid subtractive combination
            "VL",        # Invalid subtractive combination
            "VC",        # Invalid subtractive combination
            "VD",        # Invalid subtractive combination
            "VM",        # Invalid subtractive combination
            "XD",        # Invalid subtractive combination
            "XM",        # Invalid subtractive combination
            "LC",        # Invalid subtractive combination
            "LD",        # Invalid subtractive combination
            "LM",        # Invalid subtractive combination
            "DM",        # Invalid subtractive combination
        ]
        for invalid_pattern in invalid_patterns:
            with pytest.raises(ValueError, match="Invalid Roman numeral"):
                self.converter.roman_to_int(invalid_pattern)

    def test_is_valid_roman(self):
        """Test the is_valid_roman method."""
        valid_cases = ['I', 'IV', 'V', 'IX', 'X', 'XIV', 'MCMXCIV', 'MMMCMXCIX']
        invalid_cases = ['', 'IIII', 'VV', 'IL', 'ABC', 42, None]

        for valid_roman in valid_cases:
            assert self.converter.is_valid_roman(valid_roman) is True

        for invalid_roman in invalid_cases:
            assert self.converter.is_valid_roman(invalid_roman) is False

    def test_performance_int_to_roman(self):
        """Test performance of integer to Roman conversion."""
        numbers = random.sample(range(1, 4000), 1000)
        start_time = time.time()

        for num in numbers:
            self.converter.int_to_roman(num)

        end_time = time.time()
        elapsed = end_time - start_time

        # Should complete 1000 conversions in less than 50ms (reasonable)
        assert elapsed < 0.05, f"Performance test failed: {elapsed:.4f}s for 1000 conversions"

    def test_performance_roman_to_int(self):
        """Test performance of Roman to integer conversion."""
        # Generate 1000 Roman numerals
        romans = [self.converter.int_to_roman(num) for num in random.sample(range(1, 4000), 1000)]
        start_time = time.time()

        for roman in romans:
            self.converter.roman_to_int(roman)

        end_time = time.time()
        elapsed = end_time - start_time

        # Should complete 1000 conversions in less than 100ms (reasonable)
        assert elapsed < 0.1, f"Performance test failed: {elapsed:.4f}s for 1000 conversions"


class TestConvenienceFunctions:
    """Test suite for convenience functions."""

    def test_int_to_roman_function(self):
        """Test standalone int_to_roman function."""
        assert int_to_roman(1994) == 'MCMXCIV'
        assert int_to_roman(58) == 'LVIII'

        with pytest.raises(TypeError):
            int_to_roman("5")

        with pytest.raises(ValueError):
            int_to_roman(0)

    def test_roman_to_int_function(self):
        """Test standalone roman_to_int function."""
        assert roman_to_int('MCMXCIV') == 1994
        assert roman_to_int('lviii') == 58

        with pytest.raises(TypeError):
            roman_to_int(42)

        with pytest.raises(ValueError):
            roman_to_int('')

    def test_is_valid_roman_function(self):
        """Test standalone is_valid_roman function."""
        assert is_valid_roman('XIV') is True
        assert is_valid_roman('IIII') is False
        assert is_valid_roman(42) is False


class TestSpecificationCompliance:
    """Test compliance with specification requirements."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = RomanNumeralConverter()

    def test_all_specification_examples(self):
        """Test all examples from the specification document."""
        # Integer to Roman examples from spec
        spec_int_to_roman = [
            (1, "I"), (4, "IV"), (5, "V"), (9, "IX"), (10, "X"),
            (40, "XL"), (50, "L"), (90, "XC"), (100, "C"),
            (400, "CD"), (500, "D"), (900, "CM"), (1000, "M"),
            (1994, "MCMXCIV"), (3999, "MMMCMXCIX")
        ]

        for num, expected in spec_int_to_roman:
            assert self.converter.int_to_roman(num) == expected

        # Roman to Integer examples from spec
        spec_roman_to_int = [
            ("I", 1), ("IV", 4), ("V", 5), ("IX", 9), ("X", 10),
            ("XL", 40), ("L", 50), ("XC", 90), ("C", 100),
            ("CD", 400), ("D", 500), ("CM", 900), ("M", 1000),
            ("MCMXCIV", 1994), ("MMMCMXCIX", 3999)
        ]

        for roman, expected in spec_roman_to_int:
            assert self.converter.roman_to_int(roman) == expected

        # Case insensitivity examples from spec
        spec_case_insensitive = [
            ("i", 1), ("iv", 4), ("mcmxciv", 1994), ("MmMcMxCiX", 3999)
        ]

        for roman, expected in spec_case_insensitive:
            assert self.converter.roman_to_int(roman) == expected

    def test_error_message_compliance(self):
        """Test that error messages match specification."""
        # Test integer range error messages
        with pytest.raises(ValueError, match="Integer must be between 1 and 3999, got: 0"):
            self.converter.int_to_roman(0)

        with pytest.raises(ValueError, match="Integer must be between 1 and 3999, got: -1"):
            self.converter.int_to_roman(-1)

        with pytest.raises(ValueError, match="Integer must be between 1 and 3999, got: 4000"):
            self.converter.int_to_roman(4000)

        # Test type error messages
        with pytest.raises(TypeError, match="Expected integer, got str"):
            self.converter.int_to_roman("5")

        with pytest.raises(TypeError, match="Expected integer, got float"):
            self.converter.int_to_roman(3.14)

        with pytest.raises(TypeError, match="Expected string, got int"):
            self.converter.roman_to_int(42)

        # Test Roman numeral validation errors
        with pytest.raises(ValueError, match="Roman numeral cannot be empty"):
            self.converter.roman_to_int("")

        with pytest.raises(ValueError, match="Roman numeral cannot be empty"):
            self.converter.roman_to_int("   ")

        with pytest.raises(ValueError, match="Invalid Roman numeral: IIII"):
            self.converter.roman_to_int("IIII")

        with pytest.raises(ValueError, match="Invalid Roman numeral: IL"):
            self.converter.roman_to_int("IL")

    def test_boundary_value_compliance(self):
        """Test boundary values as specified."""
        # Minimum value
        assert self.converter.int_to_roman(1) == "I"
        assert self.converter.roman_to_int("I") == 1

        # Maximum value
        assert self.converter.int_to_roman(3999) == "MMMCMXCIX"
        assert self.converter.roman_to_int("MMMCMXCIX") == 3999


if __name__ == "__main__":
    pytest.main([__file__, "-v"])