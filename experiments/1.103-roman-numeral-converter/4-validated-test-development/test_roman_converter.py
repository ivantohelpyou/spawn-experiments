import unittest
from roman_converter import RomanConverter


class TestRomanConverter(unittest.TestCase):
    def setUp(self):
        self.converter = RomanConverter()

    # Tests for integer to Roman numeral conversion
    def test_single_digits_to_roman(self):
        """Test single digit conversions"""
        self.assertEqual(self.converter.to_roman(1), "I")
        self.assertEqual(self.converter.to_roman(2), "II")
        self.assertEqual(self.converter.to_roman(3), "III")
        self.assertEqual(self.converter.to_roman(4), "IV")
        self.assertEqual(self.converter.to_roman(5), "V")
        self.assertEqual(self.converter.to_roman(6), "VI")
        self.assertEqual(self.converter.to_roman(7), "VII")
        self.assertEqual(self.converter.to_roman(8), "VIII")
        self.assertEqual(self.converter.to_roman(9), "IX")

    def test_tens_to_roman(self):
        """Test tens conversions"""
        self.assertEqual(self.converter.to_roman(10), "X")
        self.assertEqual(self.converter.to_roman(20), "XX")
        self.assertEqual(self.converter.to_roman(30), "XXX")
        self.assertEqual(self.converter.to_roman(40), "XL")
        self.assertEqual(self.converter.to_roman(50), "L")
        self.assertEqual(self.converter.to_roman(60), "LX")
        self.assertEqual(self.converter.to_roman(70), "LXX")
        self.assertEqual(self.converter.to_roman(80), "LXXX")
        self.assertEqual(self.converter.to_roman(90), "XC")

    def test_hundreds_to_roman(self):
        """Test hundreds conversions"""
        self.assertEqual(self.converter.to_roman(100), "C")
        self.assertEqual(self.converter.to_roman(200), "CC")
        self.assertEqual(self.converter.to_roman(300), "CCC")
        self.assertEqual(self.converter.to_roman(400), "CD")
        self.assertEqual(self.converter.to_roman(500), "D")
        self.assertEqual(self.converter.to_roman(600), "DC")
        self.assertEqual(self.converter.to_roman(700), "DCC")
        self.assertEqual(self.converter.to_roman(800), "DCCC")
        self.assertEqual(self.converter.to_roman(900), "CM")

    def test_thousands_to_roman(self):
        """Test thousands conversions"""
        self.assertEqual(self.converter.to_roman(1000), "M")
        self.assertEqual(self.converter.to_roman(2000), "MM")
        self.assertEqual(self.converter.to_roman(3000), "MMM")

    def test_complex_numbers_to_roman(self):
        """Test complex number conversions"""
        self.assertEqual(self.converter.to_roman(11), "XI")
        self.assertEqual(self.converter.to_roman(27), "XXVII")
        self.assertEqual(self.converter.to_roman(48), "XLVIII")
        self.assertEqual(self.converter.to_roman(59), "LIX")
        self.assertEqual(self.converter.to_roman(93), "XCIII")
        self.assertEqual(self.converter.to_roman(141), "CXLI")
        self.assertEqual(self.converter.to_roman(163), "CLXIII")
        self.assertEqual(self.converter.to_roman(402), "CDII")
        self.assertEqual(self.converter.to_roman(575), "DLXXV")
        self.assertEqual(self.converter.to_roman(911), "CMXI")
        self.assertEqual(self.converter.to_roman(1024), "MXXIV")
        self.assertEqual(self.converter.to_roman(3000), "MMM")

    def test_subtractive_cases_to_roman(self):
        """Test specific subtractive notation cases"""
        self.assertEqual(self.converter.to_roman(4), "IV")
        self.assertEqual(self.converter.to_roman(9), "IX")
        self.assertEqual(self.converter.to_roman(40), "XL")
        self.assertEqual(self.converter.to_roman(90), "XC")
        self.assertEqual(self.converter.to_roman(400), "CD")
        self.assertEqual(self.converter.to_roman(900), "CM")
        self.assertEqual(self.converter.to_roman(444), "CDXLIV")
        self.assertEqual(self.converter.to_roman(999), "CMXCIX")

    def test_historical_dates_to_roman(self):
        """Test historical dates and significant numbers"""
        self.assertEqual(self.converter.to_roman(1066), "MLXVI")  # Battle of Hastings
        self.assertEqual(self.converter.to_roman(1492), "MCDXCII")  # Columbus
        self.assertEqual(self.converter.to_roman(1776), "MDCCLXXVI")  # Declaration of Independence
        self.assertEqual(self.converter.to_roman(1984), "MCMLXXXIV")  # Orwell's novel
        self.assertEqual(self.converter.to_roman(2024), "MMXXIV")  # Recent year

    def test_boundary_values_to_roman(self):
        """Test boundary values"""
        self.assertEqual(self.converter.to_roman(1), "I")  # Minimum
        self.assertEqual(self.converter.to_roman(3999), "MMMCMXCIX")  # Maximum

    # Tests for Roman numeral to integer conversion
    def test_single_symbols_from_roman(self):
        """Test single Roman symbol conversions"""
        self.assertEqual(self.converter.from_roman("I"), 1)
        self.assertEqual(self.converter.from_roman("V"), 5)
        self.assertEqual(self.converter.from_roman("X"), 10)
        self.assertEqual(self.converter.from_roman("L"), 50)
        self.assertEqual(self.converter.from_roman("C"), 100)
        self.assertEqual(self.converter.from_roman("D"), 500)
        self.assertEqual(self.converter.from_roman("M"), 1000)

    def test_additive_cases_from_roman(self):
        """Test additive notation cases"""
        self.assertEqual(self.converter.from_roman("II"), 2)
        self.assertEqual(self.converter.from_roman("III"), 3)
        self.assertEqual(self.converter.from_roman("VI"), 6)
        self.assertEqual(self.converter.from_roman("VII"), 7)
        self.assertEqual(self.converter.from_roman("VIII"), 8)
        self.assertEqual(self.converter.from_roman("XI"), 11)
        self.assertEqual(self.converter.from_roman("XII"), 12)
        self.assertEqual(self.converter.from_roman("XV"), 15)
        self.assertEqual(self.converter.from_roman("XX"), 20)
        self.assertEqual(self.converter.from_roman("XXX"), 30)
        self.assertEqual(self.converter.from_roman("LX"), 60)
        self.assertEqual(self.converter.from_roman("LXX"), 70)
        self.assertEqual(self.converter.from_roman("LXXX"), 80)
        self.assertEqual(self.converter.from_roman("CC"), 200)
        self.assertEqual(self.converter.from_roman("CCC"), 300)
        self.assertEqual(self.converter.from_roman("DC"), 600)
        self.assertEqual(self.converter.from_roman("DCC"), 700)
        self.assertEqual(self.converter.from_roman("DCCC"), 800)
        self.assertEqual(self.converter.from_roman("MM"), 2000)
        self.assertEqual(self.converter.from_roman("MMM"), 3000)

    def test_subtractive_cases_from_roman(self):
        """Test subtractive notation cases"""
        self.assertEqual(self.converter.from_roman("IV"), 4)
        self.assertEqual(self.converter.from_roman("IX"), 9)
        self.assertEqual(self.converter.from_roman("XL"), 40)
        self.assertEqual(self.converter.from_roman("XC"), 90)
        self.assertEqual(self.converter.from_roman("CD"), 400)
        self.assertEqual(self.converter.from_roman("CM"), 900)

    def test_complex_roman_numbers(self):
        """Test complex Roman numeral conversions"""
        self.assertEqual(self.converter.from_roman("XLVIII"), 48)
        self.assertEqual(self.converter.from_roman("LIX"), 59)
        self.assertEqual(self.converter.from_roman("XCIII"), 93)
        self.assertEqual(self.converter.from_roman("CXLI"), 141)
        self.assertEqual(self.converter.from_roman("CLXIII"), 163)
        self.assertEqual(self.converter.from_roman("CDII"), 402)
        self.assertEqual(self.converter.from_roman("DLXXV"), 575)
        self.assertEqual(self.converter.from_roman("CMXI"), 911)
        self.assertEqual(self.converter.from_roman("MXXIV"), 1024)
        self.assertEqual(self.converter.from_roman("CDXLIV"), 444)
        self.assertEqual(self.converter.from_roman("CMXCIX"), 999)

    def test_historical_dates_from_roman(self):
        """Test historical dates from Roman"""
        self.assertEqual(self.converter.from_roman("MLXVI"), 1066)
        self.assertEqual(self.converter.from_roman("MCDXCII"), 1492)
        self.assertEqual(self.converter.from_roman("MDCCLXXVI"), 1776)
        self.assertEqual(self.converter.from_roman("MCMLXXXIV"), 1984)
        self.assertEqual(self.converter.from_roman("MMXXIV"), 2024)

    def test_boundary_values_from_roman(self):
        """Test boundary values from Roman"""
        self.assertEqual(self.converter.from_roman("I"), 1)
        self.assertEqual(self.converter.from_roman("MMMCMXCIX"), 3999)

    # Round-trip tests
    def test_round_trip_conversion(self):
        """Test that converting to Roman and back gives original number"""
        test_numbers = [1, 4, 5, 9, 10, 27, 48, 59, 93, 141, 163, 402, 575,
                       911, 1024, 1066, 1492, 1776, 1984, 2024, 3999]

        for num in test_numbers:
            roman = self.converter.to_roman(num)
            converted_back = self.converter.from_roman(roman)
            self.assertEqual(num, converted_back,
                           f"Round trip failed for {num}: {roman} -> {converted_back}")

    # Edge cases and error handling
    def test_invalid_integer_input(self):
        """Test invalid integer inputs"""
        with self.assertRaises(ValueError):
            self.converter.to_roman(0)

        with self.assertRaises(ValueError):
            self.converter.to_roman(-1)

        with self.assertRaises(ValueError):
            self.converter.to_roman(4000)

        with self.assertRaises(TypeError):
            self.converter.to_roman("42")

        with self.assertRaises(TypeError):
            self.converter.to_roman(3.14)

    def test_invalid_roman_input(self):
        """Test invalid Roman numeral inputs"""
        invalid_romans = [
            "",  # Empty string
            "IIII",  # Invalid repetition
            "VV",  # V cannot be repeated
            "LL",  # L cannot be repeated
            "DD",  # D cannot be repeated
            "VX",  # Invalid subtraction
            "LC",  # Invalid subtraction
            "DM",  # Invalid subtraction
            "IL",  # Invalid subtraction (I can only precede V and X)
            "IC",  # Invalid subtraction
            "IM",  # Invalid subtraction
            "XD",  # Invalid subtraction (X can only precede L and C)
            "XM",  # Invalid subtraction
            "IVX",  # Invalid pattern
            "IXV",  # Invalid pattern
            "XCL",  # Invalid pattern
            "XLC",  # Invalid pattern
            "CDM",  # Invalid pattern
            "CMD",  # Invalid pattern
            "ABC",  # Invalid characters
            "123",  # Numbers
            "ivx",  # Lowercase
            "MMMM",  # Too many Ms
        ]

        for invalid_roman in invalid_romans:
            with self.assertRaises(ValueError, msg=f"Should reject '{invalid_roman}'"):
                self.converter.from_roman(invalid_roman)

    def test_case_sensitivity(self):
        """Test that Roman numerals are case-sensitive (uppercase only)"""
        with self.assertRaises(ValueError):
            self.converter.from_roman("iv")

        with self.assertRaises(ValueError):
            self.converter.from_roman("Iv")

        with self.assertRaises(ValueError):
            self.converter.from_roman("iV")

    def test_type_validation(self):
        """Test type validation for inputs"""
        with self.assertRaises(TypeError):
            self.converter.from_roman(123)

        with self.assertRaises(TypeError):
            self.converter.from_roman(None)

        with self.assertRaises(TypeError):
            self.converter.from_roman(["IV"])


if __name__ == "__main__":
    unittest.main()