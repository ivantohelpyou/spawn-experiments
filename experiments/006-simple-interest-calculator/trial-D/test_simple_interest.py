import unittest
import sys
from unittest.mock import patch
from io import StringIO
from simple_interest import SimpleInterestCalculator, SimpleInterestApp


class TestSimpleInterestCalculator(unittest.TestCase):

    def test_calculate_simple_interest_basic(self):
        """Test basic simple interest calculation: SI = P × R × T / 100"""
        calculator = SimpleInterestCalculator()
        result = calculator.calculate(principal=1000, rate=5, time=2)
        self.assertEqual(result, 100.0)

    def test_calculate_with_negative_principal_raises_error(self):
        """Test that negative principal raises ValueError"""
        calculator = SimpleInterestCalculator()
        with self.assertRaises(ValueError) as context:
            calculator.calculate(principal=-1000, rate=5, time=2)
        self.assertIn("Principal must be positive", str(context.exception))

    def test_calculate_with_zero_principal_raises_error(self):
        """Test that zero principal raises ValueError"""
        calculator = SimpleInterestCalculator()
        with self.assertRaises(ValueError) as context:
            calculator.calculate(principal=0, rate=5, time=2)
        self.assertIn("Principal must be positive", str(context.exception))

    def test_calculate_with_negative_rate_raises_error(self):
        """Test that negative rate raises ValueError"""
        calculator = SimpleInterestCalculator()
        with self.assertRaises(ValueError) as context:
            calculator.calculate(principal=1000, rate=-5, time=2)
        self.assertIn("Rate must be positive", str(context.exception))

    def test_calculate_with_zero_rate_raises_error(self):
        """Test that zero rate raises ValueError"""
        calculator = SimpleInterestCalculator()
        with self.assertRaises(ValueError) as context:
            calculator.calculate(principal=1000, rate=0, time=2)
        self.assertIn("Rate must be positive", str(context.exception))

    def test_calculate_with_negative_time_raises_error(self):
        """Test that negative time raises ValueError"""
        calculator = SimpleInterestCalculator()
        with self.assertRaises(ValueError) as context:
            calculator.calculate(principal=1000, rate=5, time=-2)
        self.assertIn("Time must be positive", str(context.exception))

    def test_calculate_with_zero_time_raises_error(self):
        """Test that zero time raises ValueError"""
        calculator = SimpleInterestCalculator()
        with self.assertRaises(ValueError) as context:
            calculator.calculate(principal=1000, rate=5, time=0)
        self.assertIn("Time must be positive", str(context.exception))


class TestSimpleInterestApp(unittest.TestCase):

    @patch('builtins.input', side_effect=['1000', '5', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_app_with_valid_inputs(self, mock_stdout, mock_input):
        """Test the command-line interface with valid inputs"""
        app = SimpleInterestApp()
        app.run()
        output = mock_stdout.getvalue()
        # Focus on testing the output we know should be there
        self.assertIn("Simple Interest: $100.00", output)

    @patch('builtins.input', side_effect=['-1000', '1000', '5', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_app_with_invalid_principal_then_valid(self, mock_stdout, mock_input):
        """Test the command-line interface handles invalid input gracefully"""
        app = SimpleInterestApp()
        app.run()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Principal must be positive", output)
        self.assertIn("Simple Interest: $100.00", output)


if __name__ == '__main__':
    unittest.main()