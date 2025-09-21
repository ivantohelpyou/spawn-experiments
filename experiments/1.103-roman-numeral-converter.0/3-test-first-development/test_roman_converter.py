#!/usr/bin/env python3
"""
Test-driven development for Roman numeral converter.
Red-Green-Refactor cycle implementation.
"""

import unittest
from roman_converter import RomanConverter


class TestRomanConverter(unittest.TestCase):
    """Test cases for Roman numeral converter using TDD approach."""

    def setUp(self):
        """Set up test fixture."""
        self.converter = RomanConverter()

    def test_convert_1_to_roman(self):
        """Test converting 1 to Roman numeral I."""
        result = self.converter.int_to_roman(1)
        self.assertEqual(result, "I")

    def test_convert_2_to_roman(self):
        """Test converting 2 to Roman numeral II."""
        result = self.converter.int_to_roman(2)
        self.assertEqual(result, "II")

    def test_convert_3_to_roman(self):
        """Test converting 3 to Roman numeral III."""
        result = self.converter.int_to_roman(3)
        self.assertEqual(result, "III")

    def test_convert_4_to_roman(self):
        """Test converting 4 to Roman numeral IV."""
        result = self.converter.int_to_roman(4)
        self.assertEqual(result, "IV")

    def test_convert_5_to_roman(self):
        """Test converting 5 to Roman numeral V."""
        result = self.converter.int_to_roman(5)
        self.assertEqual(result, "V")

    def test_convert_9_to_roman(self):
        """Test converting 9 to Roman numeral IX."""
        result = self.converter.int_to_roman(9)
        self.assertEqual(result, "IX")

    def test_convert_10_to_roman(self):
        """Test converting 10 to Roman numeral X."""
        result = self.converter.int_to_roman(10)
        self.assertEqual(result, "X")

    def test_convert_40_to_roman(self):
        """Test converting 40 to Roman numeral XL."""
        result = self.converter.int_to_roman(40)
        self.assertEqual(result, "XL")

    def test_convert_50_to_roman(self):
        """Test converting 50 to Roman numeral L."""
        result = self.converter.int_to_roman(50)
        self.assertEqual(result, "L")

    def test_convert_90_to_roman(self):
        """Test converting 90 to Roman numeral XC."""
        result = self.converter.int_to_roman(90)
        self.assertEqual(result, "XC")

    def test_convert_100_to_roman(self):
        """Test converting 100 to Roman numeral C."""
        result = self.converter.int_to_roman(100)
        self.assertEqual(result, "C")

    def test_convert_400_to_roman(self):
        """Test converting 400 to Roman numeral CD."""
        result = self.converter.int_to_roman(400)
        self.assertEqual(result, "CD")

    def test_convert_500_to_roman(self):
        """Test converting 500 to Roman numeral D."""
        result = self.converter.int_to_roman(500)
        self.assertEqual(result, "D")

    def test_convert_900_to_roman(self):
        """Test converting 900 to Roman numeral CM."""
        result = self.converter.int_to_roman(900)
        self.assertEqual(result, "CM")

    def test_convert_1000_to_roman(self):
        """Test converting 1000 to Roman numeral M."""
        result = self.converter.int_to_roman(1000)
        self.assertEqual(result, "M")

    def test_convert_complex_number(self):
        """Test converting complex number 1994 to Roman numeral MCMXCIV."""
        result = self.converter.int_to_roman(1994)
        self.assertEqual(result, "MCMXCIV")

    # Roman to Integer conversion tests
    def test_convert_I_to_int(self):
        """Test converting Roman numeral I to integer 1."""
        result = self.converter.roman_to_int("I")
        self.assertEqual(result, 1)

    def test_convert_II_to_int(self):
        """Test converting Roman numeral II to integer 2."""
        result = self.converter.roman_to_int("II")
        self.assertEqual(result, 2)

    def test_convert_III_to_int(self):
        """Test converting Roman numeral III to integer 3."""
        result = self.converter.roman_to_int("III")
        self.assertEqual(result, 3)

    def test_convert_IV_to_int(self):
        """Test converting Roman numeral IV to integer 4."""
        result = self.converter.roman_to_int("IV")
        self.assertEqual(result, 4)

    def test_convert_V_to_int(self):
        """Test converting Roman numeral V to integer 5."""
        result = self.converter.roman_to_int("V")
        self.assertEqual(result, 5)

    def test_convert_IX_to_int(self):
        """Test converting Roman numeral IX to integer 9."""
        result = self.converter.roman_to_int("IX")
        self.assertEqual(result, 9)

    def test_convert_X_to_int(self):
        """Test converting Roman numeral X to integer 10."""
        result = self.converter.roman_to_int("X")
        self.assertEqual(result, 10)

    def test_convert_XL_to_int(self):
        """Test converting Roman numeral XL to integer 40."""
        result = self.converter.roman_to_int("XL")
        self.assertEqual(result, 40)

    def test_convert_L_to_int(self):
        """Test converting Roman numeral L to integer 50."""
        result = self.converter.roman_to_int("L")
        self.assertEqual(result, 50)

    def test_convert_XC_to_int(self):
        """Test converting Roman numeral XC to integer 90."""
        result = self.converter.roman_to_int("XC")
        self.assertEqual(result, 90)

    def test_convert_C_to_int(self):
        """Test converting Roman numeral C to integer 100."""
        result = self.converter.roman_to_int("C")
        self.assertEqual(result, 100)

    def test_convert_CD_to_int(self):
        """Test converting Roman numeral CD to integer 400."""
        result = self.converter.roman_to_int("CD")
        self.assertEqual(result, 400)

    def test_convert_D_to_int(self):
        """Test converting Roman numeral D to integer 500."""
        result = self.converter.roman_to_int("D")
        self.assertEqual(result, 500)

    def test_convert_CM_to_int(self):
        """Test converting Roman numeral CM to integer 900."""
        result = self.converter.roman_to_int("CM")
        self.assertEqual(result, 900)

    def test_convert_M_to_int(self):
        """Test converting Roman numeral M to integer 1000."""
        result = self.converter.roman_to_int("M")
        self.assertEqual(result, 1000)

    def test_convert_complex_roman_to_int(self):
        """Test converting complex Roman numeral MCMXCIV to integer 1994."""
        result = self.converter.roman_to_int("MCMXCIV")
        self.assertEqual(result, 1994)

    # Edge case tests
    def test_boundary_values(self):
        """Test boundary values 1 and 3999."""
        self.assertEqual(self.converter.int_to_roman(1), "I")
        self.assertEqual(self.converter.roman_to_int("I"), 1)
        self.assertEqual(self.converter.int_to_roman(3999), "MMMCMXCIX")
        self.assertEqual(self.converter.roman_to_int("MMMCMXCIX"), 3999)

    def test_roundtrip_conversion(self):
        """Test that int->roman->int returns original value."""
        test_values = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000, 1994, 3999]
        for value in test_values:
            roman = self.converter.int_to_roman(value)
            back_to_int = self.converter.roman_to_int(roman)
            self.assertEqual(back_to_int, value, f"Roundtrip failed for {value}")

    def test_roman_roundtrip_conversion(self):
        """Test that roman->int->roman returns original value."""
        test_romans = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M", "MCMXCIV"]
        for roman in test_romans:
            integer = self.converter.roman_to_int(roman)
            back_to_roman = self.converter.int_to_roman(integer)
            self.assertEqual(back_to_roman, roman, f"Roundtrip failed for {roman}")

    # Error handling tests
    def test_int_to_roman_invalid_input(self):
        """Test error handling for invalid integer input."""
        with self.assertRaises(ValueError):
            self.converter.int_to_roman(0)
        with self.assertRaises(ValueError):
            self.converter.int_to_roman(4000)
        with self.assertRaises(ValueError):
            self.converter.int_to_roman(-1)
        with self.assertRaises(ValueError):
            self.converter.int_to_roman("not_an_int")

    def test_roman_to_int_invalid_input(self):
        """Test error handling for invalid Roman numeral input."""
        with self.assertRaises(ValueError):
            self.converter.roman_to_int(123)
        with self.assertRaises(ValueError):
            self.converter.roman_to_int("INVALID")

    def test_case_insensitive_roman_input(self):
        """Test that Roman numeral input is case insensitive."""
        self.assertEqual(self.converter.roman_to_int("mcmxciv"), 1994)
        self.assertEqual(self.converter.roman_to_int("McmXciV"), 1994)
        self.assertEqual(self.converter.roman_to_int("  MCMXCIV  "), 1994)


if __name__ == "__main__":
    unittest.main()