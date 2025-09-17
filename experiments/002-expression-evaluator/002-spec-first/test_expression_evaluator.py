"""
Comprehensive test suite for the Expression Evaluator system.

This module contains tests for all components of the expression evaluator,
ensuring correctness, error handling, and performance requirements.
"""

import pytest
import math
import time
from typing import Dict, Any

from .expression_manager import ExpressionManager, evaluate, validate
from .tokenizer import Tokenizer
from .parser import Parser
from .evaluator import Evaluator
from .models import (
    Token, TokenType, ExpressionNode, NodeType, VariableContext,
    EvaluationResult, ValidationResult
)
from .exceptions import (
    ExpressionError, SyntaxError, EvaluationError, VariableError, FunctionError
)


class TestTokenizer:
    """Test cases for the Tokenizer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tokenizer = Tokenizer()

    def test_tokenize_simple_expression(self):
        """Test tokenizing a simple arithmetic expression."""
        tokens = self.tokenizer.tokenize("2 + 3")
        assert len(tokens) == 4  # 2, +, 3, EOF
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "2"
        assert tokens[1].type == TokenType.OPERATOR
        assert tokens[1].value == "+"
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == "3"
        assert tokens[3].type == TokenType.EOF

    def test_tokenize_complex_expression(self):
        """Test tokenizing a complex expression with functions and variables."""
        tokens = self.tokenizer.tokenize("sin(x) + sqrt(y)")
        token_types = [token.type for token in tokens[:-1]]  # Exclude EOF
        expected_types = [
            TokenType.FUNCTION, TokenType.LEFT_PAREN, TokenType.VARIABLE, TokenType.RIGHT_PAREN,
            TokenType.OPERATOR,
            TokenType.FUNCTION, TokenType.LEFT_PAREN, TokenType.VARIABLE, TokenType.RIGHT_PAREN
        ]
        assert token_types == expected_types

    def test_tokenize_scientific_notation(self):
        """Test tokenizing scientific notation numbers."""
        tokens = self.tokenizer.tokenize("1.23e-4 + 5.67E+2")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "1.23e-4"
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == "5.67E+2"

    def test_tokenize_constants(self):
        """Test tokenizing mathematical constants."""
        tokens = self.tokenizer.tokenize("pi + e")
        assert tokens[0].type == TokenType.CONSTANT
        assert tokens[0].value == "pi"
        assert tokens[2].type == TokenType.CONSTANT
        assert tokens[2].value == "e"

    def test_tokenize_operators(self):
        """Test tokenizing all supported operators."""
        expression = "a + b - c * d / e ** f // g % h"
        tokens = self.tokenizer.tokenize(expression)
        operators = [t.value for t in tokens if t.type == TokenType.OPERATOR]
        expected = ['+', '-', '*', '/', '**', '//', '%']
        assert operators == expected

    def test_tokenize_invalid_character(self):
        """Test tokenizing with invalid characters."""
        with pytest.raises(SyntaxError):
            self.tokenizer.tokenize("2 + @ 3")

    def test_validate_unmatched_parentheses(self):
        """Test validation of unmatched parentheses."""
        tokens = self.tokenizer.tokenize("((2 + 3)")
        with pytest.raises(SyntaxError, match="Unmatched opening parenthesis"):
            self.tokenizer.validate_tokens(tokens)

        tokens = self.tokenizer.tokenize("(2 + 3))")
        with pytest.raises(SyntaxError, match="Unmatched closing parenthesis"):
            self.tokenizer.validate_tokens(tokens)


class TestParser:
    """Test cases for the Parser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = Parser()

    def test_parse_simple_arithmetic(self):
        """Test parsing simple arithmetic expressions."""
        ast = self.parser.parse("2 + 3 * 4")
        assert ast.node_type == NodeType.BINARY_OP
        assert ast.operator == "+"
        assert ast.left.value == 2.0
        assert ast.right.operator == "*"

    def test_parse_precedence(self):
        """Test operator precedence parsing."""
        ast = self.parser.parse("2 + 3 * 4")
        # Should be parsed as 2 + (3 * 4), not (2 + 3) * 4
        assert ast.operator == "+"
        assert ast.left.value == 2.0
        assert ast.right.operator == "*"
        assert ast.right.left.value == 3.0
        assert ast.right.right.value == 4.0

    def test_parse_associativity(self):
        """Test operator associativity."""
        # Left associative: 10 - 5 - 2 = (10 - 5) - 2
        ast = self.parser.parse("10 - 5 - 2")
        assert ast.operator == "-"
        assert ast.left.operator == "-"
        assert ast.left.left.value == 10.0
        assert ast.left.right.value == 5.0
        assert ast.right.value == 2.0

        # Right associative: 2 ** 3 ** 2 = 2 ** (3 ** 2)
        ast = self.parser.parse("2 ** 3 ** 2")
        assert ast.operator == "**"
        assert ast.left.value == 2.0
        assert ast.right.operator == "**"
        assert ast.right.left.value == 3.0
        assert ast.right.right.value == 2.0

    def test_parse_parentheses(self):
        """Test parsing with parentheses."""
        ast = self.parser.parse("(2 + 3) * 4")
        assert ast.operator == "*"
        assert ast.left.operator == "+"
        assert ast.right.value == 4.0

    def test_parse_unary_operators(self):
        """Test parsing unary operators."""
        ast = self.parser.parse("-5 + (+3)")
        assert ast.operator == "+"
        assert ast.left.node_type == NodeType.UNARY_OP
        assert ast.left.operator == "-"
        assert ast.left.right.value == 5.0

    def test_parse_function_calls(self):
        """Test parsing function calls."""
        ast = self.parser.parse("sin(x)")
        assert ast.node_type == NodeType.FUNCTION_CALL
        assert ast.value == "sin"
        assert len(ast.children) == 1
        assert ast.children[0].value == "x"

        # Multiple arguments
        ast = self.parser.parse("pow(2, 3)")
        assert ast.node_type == NodeType.FUNCTION_CALL
        assert ast.value == "pow"
        assert len(ast.children) == 2

    def test_parse_variables_and_constants(self):
        """Test parsing variables and constants."""
        ast = self.parser.parse("x + pi")
        assert ast.operator == "+"
        assert ast.left.node_type == NodeType.VARIABLE
        assert ast.left.value == "x"
        assert ast.right.node_type == NodeType.CONSTANT
        assert ast.right.value == "pi"

    def test_parse_syntax_errors(self):
        """Test parsing syntax errors."""
        with pytest.raises(SyntaxError):
            self.parser.parse("2 +")

        with pytest.raises(SyntaxError):
            self.parser.parse("* 3")

        with pytest.raises(SyntaxError):
            self.parser.parse("2 3")  # Missing operator


class TestEvaluator:
    """Test cases for the Evaluator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.evaluator = Evaluator()
        self.parser = Parser()

    def test_evaluate_basic_arithmetic(self):
        """Test evaluating basic arithmetic operations."""
        test_cases = [
            ("2 + 3", 5.0),
            ("10 - 4", 6.0),
            ("3 * 7", 21.0),
            ("15 / 3", 5.0),
            ("17 % 5", 2.0),
            ("2 ** 3", 8.0),
            ("17 // 5", 3.0),
        ]

        for expression, expected in test_cases:
            ast = self.parser.parse(expression)
            result = self.evaluator.evaluate(ast)
            assert result.success
            assert result.value == expected

    def test_evaluate_precedence(self):
        """Test evaluation with operator precedence."""
        ast = self.parser.parse("2 + 3 * 4")
        result = self.evaluator.evaluate(ast)
        assert result.success
        assert result.value == 14.0  # 2 + (3 * 4)

        ast = self.parser.parse("2 * 3 + 4")
        result = self.evaluator.evaluate(ast)
        assert result.success
        assert result.value == 10.0  # (2 * 3) + 4

    def test_evaluate_unary_operators(self):
        """Test evaluating unary operators."""
        ast = self.parser.parse("-5")
        result = self.evaluator.evaluate(ast)
        assert result.success
        assert result.value == -5.0

        ast = self.parser.parse("+7")
        result = self.evaluator.evaluate(ast)
        assert result.success
        assert result.value == 7.0

    def test_evaluate_mathematical_functions(self):
        """Test evaluating mathematical functions."""
        test_cases = [
            ("abs(-5)", 5.0),
            ("sqrt(16)", 4.0),
            ("sin(0)", 0.0),
            ("cos(0)", 1.0),
            ("log(1)", 0.0),
            ("exp(0)", 1.0),
            ("ceil(3.2)", 4.0),
            ("floor(3.8)", 3.0),
        ]

        for expression, expected in test_cases:
            ast = self.parser.parse(expression)
            result = self.evaluator.evaluate(ast)
            assert result.success
            assert abs(result.value - expected) < 1e-10

    def test_evaluate_constants(self):
        """Test evaluating mathematical constants."""
        ast = self.parser.parse("pi")
        result = self.evaluator.evaluate(ast)
        assert result.success
        assert abs(result.value - math.pi) < 1e-10

        ast = self.parser.parse("e")
        result = self.evaluator.evaluate(ast)
        assert result.success
        assert abs(result.value - math.e) < 1e-10

    def test_evaluate_variables(self):
        """Test evaluating expressions with variables."""
        variables = {"x": 5.0, "y": 3.0}
        ast = self.parser.parse("x + y")
        result = self.evaluator.evaluate(ast, variables)
        assert result.success
        assert result.value == 8.0

    def test_evaluate_complex_expression(self):
        """Test evaluating complex expressions."""
        expression = "sin(pi/4) + cos(pi/4)"
        ast = self.parser.parse(expression)
        result = self.evaluator.evaluate(ast)
        assert result.success
        expected = math.sin(math.pi/4) + math.cos(math.pi/4)
        assert abs(result.value - expected) < 1e-10

    def test_evaluate_division_by_zero(self):
        """Test division by zero error handling."""
        ast = self.parser.parse("5 / 0")
        result = self.evaluator.evaluate(ast)
        assert not result.success
        assert "division by zero" in result.error_message.lower()

    def test_evaluate_domain_errors(self):
        """Test mathematical domain errors."""
        # Square root of negative number
        ast = self.parser.parse("sqrt(-1)")
        result = self.evaluator.evaluate(ast)
        assert not result.success

        # Logarithm of zero
        ast = self.parser.parse("log(0)")
        result = self.evaluator.evaluate(ast)
        assert not result.success

    def test_evaluate_undefined_variable(self):
        """Test undefined variable error."""
        ast = self.parser.parse("undefined_var")
        result = self.evaluator.evaluate(ast)
        assert not result.success
        assert "undefined variable" in result.error_message.lower()


class TestExpressionManager:
    """Test cases for the ExpressionManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = ExpressionManager()

    def test_evaluate_expression_success(self):
        """Test successful expression evaluation."""
        result = self.manager.evaluate_expression("2 + 3 * 4")
        assert result.success
        assert result.value == 14.0
        assert result.execution_time > 0

    def test_evaluate_expression_with_variables(self):
        """Test expression evaluation with variables."""
        variables = {"x": 10.0, "y": 5.0}
        result = self.manager.evaluate_expression("x * y", variables)
        assert result.success
        assert result.value == 50.0

    def test_evaluate_expression_syntax_error(self):
        """Test expression evaluation with syntax error."""
        result = self.manager.evaluate_expression("2 +")
        assert not result.success
        assert "error" in result.error_message.lower()

    def test_validate_expression(self):
        """Test expression validation."""
        # Valid expression
        result = self.manager.validate_expression("2 + 3")
        assert result.valid

        # Invalid expression
        result = self.manager.validate_expression("2 +")
        assert not result.valid
        assert len(result.errors) > 0

    def test_variable_management(self):
        """Test variable management operations."""
        # Set and get variables
        self.manager.set_variable("x", 42.0)
        assert self.manager.get_variable("x") == 42.0

        # Get all variables
        variables = self.manager.get_variables()
        assert "x" in variables
        assert variables["x"] == 42.0

        # Clear variables
        self.manager.clear_variables()
        variables = self.manager.get_variables()
        assert "x" not in variables

    def test_batch_evaluation(self):
        """Test batch expression evaluation."""
        expressions = ["2 + 3", "4 * 5", "10 / 2"]
        results = self.manager.evaluate_batch(expressions)

        assert len(results) == 3
        assert all(result.success for result in results)
        assert results[0].value == 5.0
        assert results[1].value == 20.0
        assert results[2].value == 5.0

    def test_caching(self):
        """Test expression result caching."""
        # First evaluation
        result1 = self.manager.evaluate_expression("2 + 3")
        time1 = result1.execution_time

        # Second evaluation (should be cached)
        result2 = self.manager.evaluate_expression("2 + 3")
        time2 = result2.execution_time

        assert result1.value == result2.value
        # Second evaluation should be faster due to caching
        assert time2 <= time1

    def test_statistics(self):
        """Test evaluation statistics."""
        # Reset statistics
        self.manager.reset_statistics()
        stats = self.manager.get_statistics()
        assert stats['total_evaluations'] == 0

        # Perform some evaluations
        self.manager.evaluate_expression("2 + 3")
        self.manager.evaluate_expression("4 * 5")

        stats = self.manager.get_statistics()
        assert stats['total_evaluations'] == 2
        assert stats['total_evaluation_time'] > 0

    def test_function_management(self):
        """Test custom function management."""
        # Add custom function
        def double(x):
            return x * 2

        self.manager.add_function("double", double)
        functions = self.manager.get_functions()
        assert "double" in functions

        # Use custom function
        result = self.manager.evaluate_expression("double(5)")
        assert result.success
        assert result.value == 10.0

        # Remove custom function
        self.manager.remove_function("double")
        functions = self.manager.get_functions()
        assert "double" not in functions


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    def test_evaluate_function(self):
        """Test the evaluate convenience function."""
        result = evaluate("2 + 3")
        assert result == 5.0

        result = evaluate("x * 2", {"x": 10})
        assert result == 20.0

        with pytest.raises(ExpressionError):
            evaluate("2 +")

    def test_validate_function(self):
        """Test the validate convenience function."""
        assert validate("2 + 3") is True
        assert validate("2 +") is False


class TestPerformanceRequirements:
    """Test cases for performance requirements."""

    def test_simple_expression_performance(self):
        """Test that simple expressions evaluate quickly."""
        manager = ExpressionManager()
        expression = "2 + 3 * 4"

        start_time = time.time()
        result = manager.evaluate_expression(expression)
        end_time = time.time()

        assert result.success
        assert end_time - start_time < 0.001  # Less than 1ms

    def test_complex_expression_performance(self):
        """Test performance with complex expressions."""
        manager = ExpressionManager()
        expression = "sin(cos(tan(sqrt(abs(log(exp(pi)))))))"

        start_time = time.time()
        result = manager.evaluate_expression(expression)
        end_time = time.time()

        assert result.success
        assert end_time - start_time < 0.01  # Less than 10ms

    def test_batch_processing_throughput(self):
        """Test batch processing throughput."""
        manager = ExpressionManager()
        expressions = ["2 + 3", "4 * 5", "sin(pi/2)"] * 100  # 300 expressions

        start_time = time.time()
        results = manager.evaluate_batch(expressions)
        end_time = time.time()

        assert all(result.success for result in results)
        throughput = len(expressions) / (end_time - start_time)
        assert throughput > 1000  # More than 1000 expressions per second


class TestErrorHandling:
    """Test cases for comprehensive error handling."""

    def test_input_validation(self):
        """Test input validation."""
        manager = ExpressionManager()

        # Non-string expression
        with pytest.raises(TypeError):
            manager.evaluate_expression(123)

        # Non-dict variables
        with pytest.raises(TypeError):
            manager.evaluate_expression("x", "not_a_dict")

        # Invalid variable name
        with pytest.raises(TypeError):
            manager.evaluate_expression("x", {123: 5})

        # Invalid variable value
        with pytest.raises(TypeError):
            manager.evaluate_expression("x", {"x": "not_a_number"})

    def test_malformed_expressions(self):
        """Test handling of malformed expressions."""
        manager = ExpressionManager()
        malformed_expressions = [
            "",           # Empty
            "   ",        # Whitespace only
            "2 +",        # Incomplete
            "* 3",        # Leading operator
            "2 3",        # Missing operator
            "((2)",       # Unmatched parentheses
            "2))",        # Extra closing parentheses
        ]

        for expression in malformed_expressions:
            result = manager.evaluate_expression(expression)
            assert not result.success

    def test_mathematical_errors(self):
        """Test mathematical error handling."""
        manager = ExpressionManager()
        error_expressions = [
            "1 / 0",      # Division by zero
            "sqrt(-1)",   # Domain error
            "log(0)",     # Domain error
            "0 ** -1",    # Zero to negative power
        ]

        for expression in error_expressions:
            result = manager.evaluate_expression(expression)
            assert not result.success


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])