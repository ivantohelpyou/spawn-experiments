import pytest
from expression_calculator import ExpressionCalculator


class TestBasicNumberEvaluation:
    """Tests for evaluating single numbers (no operations)"""

    def setup_method(self):
        self.calculator = ExpressionCalculator()

    def test_single_positive_integer(self):
        """Test that single positive integers are evaluated correctly"""
        result = self.calculator.evaluate("42")
        assert result == 42.0

    def test_single_positive_decimal(self):
        """Test that single positive decimals are evaluated correctly"""
        result = self.calculator.evaluate("3.14")
        assert result == 3.14

    def test_single_zero(self):
        """Test that zero is evaluated correctly"""
        result = self.calculator.evaluate("0")
        assert result == 0.0

    def test_single_negative_integer(self):
        """Test that single negative integers are evaluated correctly"""
        result = self.calculator.evaluate("-5")
        assert result == -5.0

    def test_single_negative_decimal(self):
        """Test that single negative decimals are evaluated correctly"""
        result = self.calculator.evaluate("-2.5")
        assert result == -2.5

    def test_number_with_leading_whitespace(self):
        """Test that numbers with leading whitespace are handled correctly"""
        result = self.calculator.evaluate("  42")
        assert result == 42.0

    def test_number_with_trailing_whitespace(self):
        """Test that numbers with trailing whitespace are handled correctly"""
        result = self.calculator.evaluate("42  ")
        assert result == 42.0

    def test_number_with_surrounding_whitespace(self):
        """Test that numbers with surrounding whitespace are handled correctly"""
        result = self.calculator.evaluate("  42  ")
        assert result == 42.0


class TestBasicAddition:
    """Tests for basic addition operations"""

    def setup_method(self):
        self.calculator = ExpressionCalculator()

    def test_simple_addition_integers(self):
        """Test addition of two positive integers"""
        result = self.calculator.evaluate("2 + 3")
        assert result == 5.0

    def test_simple_addition_decimals(self):
        """Test addition of two decimal numbers"""
        result = self.calculator.evaluate("2.5 + 1.5")
        assert result == 4.0

    def test_addition_with_negative_numbers(self):
        """Test addition involving negative numbers"""
        result = self.calculator.evaluate("-2 + 5")
        assert result == 3.0

    def test_addition_negative_result(self):
        """Test addition that results in negative number"""
        result = self.calculator.evaluate("3 + (-7)")
        assert result == -4.0

    def test_addition_with_zero(self):
        """Test addition with zero (identity property)"""
        result = self.calculator.evaluate("5 + 0")
        assert result == 5.0

    def test_addition_zero_plus_zero(self):
        """Test adding zero to zero"""
        result = self.calculator.evaluate("0 + 0")
        assert result == 0.0

    def test_addition_with_whitespace(self):
        """Test addition with various whitespace patterns"""
        result = self.calculator.evaluate("  2  +  3  ")
        assert result == 5.0

    def test_addition_no_spaces(self):
        """Test addition without spaces around operator"""
        result = self.calculator.evaluate("2+3")
        assert result == 5.0


class TestOperatorPrecedence:
    """Tests for operator precedence (PEMDAS/BODMAS)"""

    def setup_method(self):
        self.calculator = ExpressionCalculator()

    def test_multiplication_before_addition(self):
        """Test that multiplication has higher precedence than addition"""
        result = self.calculator.evaluate("2 + 3 * 4")
        assert result == 14.0  # Should be 2 + (3 * 4) = 2 + 12 = 14, not (2 + 3) * 4 = 20

    def test_multiplication_before_subtraction(self):
        """Test that multiplication has higher precedence than subtraction"""
        result = self.calculator.evaluate("10 - 2 * 3")
        assert result == 4.0  # Should be 10 - (2 * 3) = 10 - 6 = 4, not (10 - 2) * 3 = 24

    def test_division_before_addition(self):
        """Test that division has higher precedence than addition"""
        result = self.calculator.evaluate("10 + 8 / 2")
        assert result == 14.0  # Should be 10 + (8 / 2) = 10 + 4 = 14, not (10 + 8) / 2 = 9

    def test_division_before_subtraction(self):
        """Test that division has higher precedence than subtraction"""
        result = self.calculator.evaluate("20 - 12 / 3")
        assert result == 16.0  # Should be 20 - (12 / 3) = 20 - 4 = 16, not (20 - 12) / 3 = 2.67

    def test_multiple_operations_same_precedence(self):
        """Test left-to-right evaluation for operations of same precedence"""
        result = self.calculator.evaluate("2 * 3 * 4")
        assert result == 24.0  # Should be (2 * 3) * 4 = 6 * 4 = 24

    def test_complex_precedence_expression(self):
        """Test complex expression with multiple precedence levels"""
        result = self.calculator.evaluate("2 + 3 * 4 - 6 / 2")
        assert result == 11.0  # Should be 2 + (3 * 4) - (6 / 2) = 2 + 12 - 3 = 11

    def test_precedence_with_negative_numbers(self):
        """Test precedence works correctly with negative numbers"""
        result = self.calculator.evaluate("-2 + 3 * 4")
        assert result == 10.0  # Should be -2 + (3 * 4) = -2 + 12 = 10