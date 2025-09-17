"""
Test-Driven Development tests for Expression Evaluator

This file contains tests written BEFORE implementation to guide development.
Following strict TDD: RED -> GREEN -> REFACTOR
"""

import unittest
from expression_evaluator import ExpressionEvaluator


class TestBasicArithmetic(unittest.TestCase):
    """Test basic arithmetic operations - TDD Cycle 1"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.evaluator = ExpressionEvaluator()

    def test_evaluate_single_number(self):
        """Test evaluating a single number."""
        result = self.evaluator.evaluate("42")
        self.assertEqual(result, 42.0)

    def test_evaluate_addition(self):
        """Test simple addition operation."""
        result = self.evaluator.evaluate("2 + 3")
        self.assertEqual(result, 5.0)

    def test_evaluate_subtraction(self):
        """Test simple subtraction operation."""
        result = self.evaluator.evaluate("10 - 4")
        self.assertEqual(result, 6.0)

    def test_evaluate_multiplication(self):
        """Test simple multiplication operation."""
        result = self.evaluator.evaluate("3 * 7")
        self.assertEqual(result, 21.0)

    def test_evaluate_division(self):
        """Test simple division operation."""
        result = self.evaluator.evaluate("15 / 3")
        self.assertEqual(result, 5.0)

    def test_evaluate_floating_point_numbers(self):
        """Test operations with floating point numbers."""
        result = self.evaluator.evaluate("3.5 + 2.1")
        self.assertAlmostEqual(result, 5.6, places=4)  # Handle floating point precision

    def test_evaluate_negative_numbers(self):
        """Test operations with negative numbers."""
        result = self.evaluator.evaluate("-5 + 3")
        self.assertEqual(result, -2.0)


class TestOperatorPrecedence(unittest.TestCase):
    """Test operator precedence - TDD Cycle 2"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.evaluator = ExpressionEvaluator()

    def test_multiplication_precedence_over_addition(self):
        """Test that multiplication has higher precedence than addition."""
        result = self.evaluator.evaluate("2 + 3 * 4")
        self.assertEqual(result, 14.0)  # Should be 2 + (3 * 4) = 14, not (2 + 3) * 4 = 20

    def test_division_precedence_over_subtraction(self):
        """Test that division has higher precedence than subtraction."""
        result = self.evaluator.evaluate("10 - 6 / 2")
        self.assertEqual(result, 7.0)  # Should be 10 - (6 / 2) = 7, not (10 - 6) / 2 = 2

    def test_left_to_right_same_precedence(self):
        """Test left-to-right evaluation for operators of same precedence."""
        result = self.evaluator.evaluate("8 / 4 * 2")
        self.assertEqual(result, 4.0)  # Should be (8 / 4) * 2 = 4, not 8 / (4 * 2) = 1

    def test_complex_precedence(self):
        """Test complex expression with multiple precedence levels."""
        result = self.evaluator.evaluate("2 + 3 * 4 - 1")
        self.assertEqual(result, 13.0)  # Should be 2 + (3 * 4) - 1 = 13


class TestParentheses(unittest.TestCase):
    """Test parentheses handling - TDD Cycle 2"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.evaluator = ExpressionEvaluator()

    def test_simple_parentheses(self):
        """Test basic parentheses override precedence."""
        result = self.evaluator.evaluate("(2 + 3) * 4")
        self.assertEqual(result, 20.0)  # Should be (2 + 3) * 4 = 20

    def test_parentheses_with_division(self):
        """Test parentheses with division."""
        result = self.evaluator.evaluate("20 / (2 + 3)")
        self.assertEqual(result, 4.0)  # Should be 20 / (2 + 3) = 4

    def test_nested_parentheses(self):
        """Test nested parentheses."""
        result = self.evaluator.evaluate("((2 + 3) * 4) / 2")
        self.assertEqual(result, 10.0)  # Should be ((2 + 3) * 4) / 2 = 10

    def test_multiple_parentheses_groups(self):
        """Test multiple separate parentheses groups."""
        result = self.evaluator.evaluate("(2 + 3) * (4 - 1)")
        self.assertEqual(result, 15.0)  # Should be (2 + 3) * (4 - 1) = 5 * 3 = 15


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases - TDD Cycle 3"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.evaluator = ExpressionEvaluator()

    def test_division_by_zero(self):
        """Test division by zero raises appropriate error."""
        with self.assertRaises(ZeroDivisionError):
            self.evaluator.evaluate("5 / 0")

    def test_incomplete_expression_trailing_operator(self):
        """Test incomplete expression with trailing operator."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("2 +")

    def test_incomplete_expression_leading_operator(self):
        """Test incomplete expression with leading operator."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("+ 3")

    def test_consecutive_operators(self):
        """Test consecutive operators raise error."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("2 + + 3")

    def test_unmatched_opening_parenthesis(self):
        """Test unmatched opening parenthesis."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("(2 + 3")

    def test_unmatched_closing_parenthesis(self):
        """Test unmatched closing parenthesis."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("2 + 3)")

    def test_empty_parentheses(self):
        """Test empty parentheses."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("()")

    def test_empty_expression(self):
        """Test empty expression."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("")

    def test_whitespace_only_expression(self):
        """Test whitespace-only expression."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("   ")

    def test_invalid_characters(self):
        """Test invalid characters in expression."""
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("2 + a")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases - TDD Cycle 3"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.evaluator = ExpressionEvaluator()

    def test_whitespace_handling(self):
        """Test expressions with various whitespace."""
        result = self.evaluator.evaluate("  2   +   3  ")
        self.assertEqual(result, 5.0)

    def test_large_numbers(self):
        """Test very large numbers."""
        result = self.evaluator.evaluate("1000000 + 2000000")
        self.assertEqual(result, 3000000.0)

    def test_very_small_numbers(self):
        """Test very small decimal numbers."""
        result = self.evaluator.evaluate("0.001 + 0.002")
        self.assertAlmostEqual(result, 0.003, places=6)

    def test_zero_operations(self):
        """Test operations with zero."""
        self.assertEqual(self.evaluator.evaluate("0 + 5"), 5.0)
        self.assertEqual(self.evaluator.evaluate("5 - 0"), 5.0)
        self.assertEqual(self.evaluator.evaluate("0 * 5"), 0.0)

    def test_single_zero(self):
        """Test single zero."""
        result = self.evaluator.evaluate("0")
        self.assertEqual(result, 0.0)

    def test_deeply_nested_parentheses(self):
        """Test deeply nested parentheses."""
        result = self.evaluator.evaluate("(((2 + 3) * 4) / (2 + 3))")
        self.assertEqual(result, 4.0)


class TestAdvancedFeatures(unittest.TestCase):
    """Test advanced features - TDD Cycle 4"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.evaluator = ExpressionEvaluator()

    def test_unary_minus_with_parentheses(self):
        """Test unary minus with parentheses."""
        result = self.evaluator.evaluate("-(2 + 3)")
        self.assertEqual(result, -5.0)

    def test_unary_minus_complex(self):
        """Test complex expressions with unary minus."""
        result = self.evaluator.evaluate("-(2 + 3) * 4")
        self.assertEqual(result, -20.0)

    def test_multiple_unary_minus(self):
        """Test multiple unary minus operations."""
        result = self.evaluator.evaluate("-(-5)")
        self.assertEqual(result, 5.0)

    def test_unary_minus_in_multiplication(self):
        """Test unary minus in multiplication."""
        result = self.evaluator.evaluate("2 * -3")
        self.assertEqual(result, -6.0)

    def test_scientific_notation_basic(self):
        """Test basic scientific notation."""
        result = self.evaluator.evaluate("1e2 + 3")
        self.assertEqual(result, 103.0)

    def test_scientific_notation_negative_exponent(self):
        """Test scientific notation with negative exponent."""
        result = self.evaluator.evaluate("5e-2 * 100")
        self.assertAlmostEqual(result, 5.0, places=6)

    def test_floating_point_precision(self):
        """Test floating point precision handling."""
        result = self.evaluator.evaluate("0.1 + 0.2")
        self.assertAlmostEqual(result, 0.3, places=10)

    def test_long_expression_chain(self):
        """Test very long expression chains."""
        result = self.evaluator.evaluate("1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10")
        self.assertEqual(result, 55.0)

    def test_complex_nested_expression(self):
        """Test complex nested expressions."""
        result = self.evaluator.evaluate("((1 + 2) * (3 + 4)) - ((5 - 2) * (6 / 3))")
        self.assertEqual(result, 15.0)  # ((1+2)*(3+4)) - ((5-2)*(6/3)) = (3*7) - (3*2) = 21 - 6 = 15


if __name__ == '__main__':
    unittest.main()