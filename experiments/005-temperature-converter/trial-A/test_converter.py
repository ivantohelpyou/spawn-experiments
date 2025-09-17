import unittest
import subprocess
from converter import convert

class TestConverter(unittest.TestCase):
    def test_celsius_to_celsius(self):
        self.assertEqual(convert(0, "c", "c"), 0.0)

    def test_celsius_to_fahrenheit(self):
        self.assertEqual(convert(0, "c", "f"), 32.0)

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(convert(32, "f", "c"), 0.0)

    def test_celsius_to_kelvin(self):
        self.assertEqual(convert(0, "c", "k"), 273.15)

    def test_kelvin_to_celsius(self):
        self.assertEqual(convert(273.15, "k", "c"), 0.0)

    def test_fahrenheit_to_kelvin(self):
        self.assertEqual(convert(32, "f", "k"), 273.15)

    def test_kelvin_to_fahrenheit(self):
        self.assertEqual(convert(273.15, "k", "f"), 32.0)

    def test_case_insensitivity(self):
        self.assertEqual(convert(0, "C", "c"), 0.0)
        self.assertEqual(convert(0, "Celsius", "c"), 0.0)
        self.assertEqual(convert(0, "c", "F"), 32.0)
        self.assertEqual(convert(0, "c", "Fahrenheit"), 32.0)
        self.assertEqual(convert(0, "c", "K"), 273.15)
        self.assertEqual(convert(0, "c", "Kelvin"), 273.15)

    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            convert(0, "c", "x")
        with self.assertRaises(ValueError):
            convert(0, "x", "c")

    def test_cli_success(self):
        result = subprocess.run(["python3", "converter.py", "32", "f", "c"], capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "0.0")
        self.assertEqual(result.returncode, 0)

    def test_cli_invalid_unit(self):
        result = subprocess.run(["python3", "converter.py", "32", "f", "x"], capture_output=True, text=True)
        self.assertIn("Invalid unit", result.stderr)
        self.assertEqual(result.returncode, 1)

    def test_cli_wrong_number_of_arguments(self):
        result = subprocess.run(["python3", "converter.py", "32", "f"], capture_output=True, text=True)
        self.assertIn("Usage:", result.stderr)
        self.assertEqual(result.returncode, 1)
