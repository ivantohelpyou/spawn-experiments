import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from simple_interest import calculate_simple_interest, main


class TestSimpleInterest(unittest.TestCase):

    def test_calculate_simple_interest_basic(self):
        """Test basic simple interest calculation: SI = Principal × Rate × Time"""
        principal = 1000
        rate = 5  # 5%
        time = 2  # 2 years
        expected_interest = 100.0  # 1000 × 0.05 × 2 = 100

        result = calculate_simple_interest(principal, rate, time)
        self.assertEqual(result, expected_interest)

    def test_calculate_simple_interest_decimal_values(self):
        """Test simple interest calculation with decimal values"""
        principal = 1500.50
        rate = 4.25  # 4.25%
        time = 1.5  # 1.5 years
        expected_interest = 1500.50 * 0.0425 * 1.5  # 95.656875

        result = calculate_simple_interest(principal, rate, time)
        self.assertAlmostEqual(result, expected_interest, places=6)

    def test_negative_principal_raises_error(self):
        """Test that negative principal raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_interest(-1000, 5, 2)

    def test_zero_principal_raises_error(self):
        """Test that zero principal raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_interest(0, 5, 2)

    def test_negative_rate_raises_error(self):
        """Test that negative rate raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_interest(1000, -5, 2)

    def test_zero_rate_raises_error(self):
        """Test that zero rate raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_interest(1000, 0, 2)

    def test_negative_time_raises_error(self):
        """Test that negative time raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_interest(1000, 5, -2)

    def test_zero_time_raises_error(self):
        """Test that zero time raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_simple_interest(1000, 5, 0)


class TestCommandLineInterface(unittest.TestCase):

    @patch('builtins.input', side_effect=['1000', '5', '2'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function_basic_flow(self, mock_stdout, mock_input):
        """Test the main function with valid inputs"""
        main()
        output = mock_stdout.getvalue()

        # Check that prompts are displayed
        self.assertIn('Enter principal amount:', output)
        self.assertIn('Enter interest rate (%):', output)
        self.assertIn('Enter time period (years):', output)

        # Check that result is displayed with proper formatting
        self.assertIn('Simple Interest: $100.00', output)

    @patch('builtins.input', side_effect=['abc'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function_invalid_principal_input(self, mock_stdout, mock_input):
        """Test the main function with invalid principal input"""
        main()
        output = mock_stdout.getvalue()

        # Check that error message is displayed
        self.assertIn('Invalid input', output)

    @patch('builtins.input', side_effect=['-1000', '5', '2'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function_negative_principal_input(self, mock_stdout, mock_input):
        """Test the main function with negative principal input"""
        main()
        output = mock_stdout.getvalue()

        # Check that error message is displayed
        self.assertIn('must be greater than 0', output)


if __name__ == '__main__':
    unittest.main()