"""
Expression Manager - Main interface for the Expression Evaluator system.

This module provides the high-level interface for expression evaluation,
coordinating between tokenizer, parser, and evaluator components.
"""

import time
from typing import Optional, Dict, List, Union
try:
    from .models import EvaluationResult, ValidationResult, VariableContext, ExpressionNode
    from .tokenizer import Tokenizer
    from .parser import Parser
    from .evaluator import Evaluator
    from .exceptions import ExpressionError, SyntaxError, EvaluationError, ValidationError
except ImportError:
    from models import EvaluationResult, ValidationResult, VariableContext, ExpressionNode
    from tokenizer import Tokenizer
    from parser import Parser
    from evaluator import Evaluator
    from exceptions import ExpressionError, SyntaxError, EvaluationError, ValidationError


class ExpressionManager:
    """
    High-level interface for mathematical expression evaluation.

    This class orchestrates the entire expression evaluation workflow,
    from tokenization through parsing to evaluation, providing a simple
    API for users while handling all the complexity internally.
    """

    def __init__(self, context: Optional[VariableContext] = None):
        """
        Initialize the expression manager.

        Args:
            context: Optional variable context (creates default if not provided)
        """
        self.context = context or VariableContext()
        self.tokenizer = Tokenizer()
        self.parser = Parser(self.tokenizer)
        self.evaluator = Evaluator(self.context)

        # Performance tracking
        self.evaluation_count = 0
        self.total_evaluation_time = 0.0
        self.cache = {}  # Simple expression cache

    def evaluate_expression(
        self,
        expression: str,
        variables: Optional[Dict[str, float]] = None
    ) -> EvaluationResult:
        """
        Evaluate a mathematical expression.

        Args:
            expression: Mathematical expression string
            variables: Optional variable definitions

        Returns:
            EvaluationResult containing value or error information

        Raises:
            ValueError: If expression is invalid
            TypeError: If variables contain non-numeric values
        """
        start_time = time.time()

        try:
            # Input validation
            if not isinstance(expression, str):
                raise TypeError("Expression must be a string")

            if variables is not None and not isinstance(variables, dict):
                raise TypeError("Variables must be a dictionary")

            # Validate variable values
            if variables:
                for name, value in variables.items():
                    if not isinstance(name, str):
                        raise TypeError(f"Variable name must be string, got {type(name)}")
                    if not isinstance(value, (int, float)):
                        raise TypeError(f"Variable value must be numeric, got {type(value)}")

            # Check cache (simple caching for identical expressions)
            cache_key = (expression, tuple(sorted(variables.items())) if variables else None)
            if cache_key in self.cache:
                cached_result = self.cache[cache_key]
                return EvaluationResult.success_result(
                    cached_result,
                    time.time() - start_time
                )

            # Parse the expression
            try:
                ast = self.parser.parse(expression)
                self.parser.validate_ast(ast)
            except SyntaxError as e:
                return EvaluationResult.error_result(
                    str(e),
                    position=getattr(e, 'position', None),
                    execution_time=time.time() - start_time
                )

            # Evaluate the expression
            result = self.evaluator.evaluate(ast, variables)

            # Cache successful results
            if result.success and len(self.cache) < 1000:  # Limit cache size
                self.cache[cache_key] = result.value

            # Update statistics
            self.evaluation_count += 1
            self.total_evaluation_time += result.execution_time

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            return EvaluationResult.error_result(
                f"Unexpected error: {str(e)}",
                execution_time=execution_time
            )

    def parse_expression(self, expression: str) -> ExpressionNode:
        """
        Parse expression into AST without evaluation.

        Args:
            expression: Mathematical expression string

        Returns:
            Root node of expression AST

        Raises:
            SyntaxError: If expression has syntax errors
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string")

        ast = self.parser.parse(expression)
        self.parser.validate_ast(ast)
        return ast

    def validate_expression(self, expression: str) -> ValidationResult:
        """
        Validate expression syntax without evaluation.

        Args:
            expression: Mathematical expression string

        Returns:
            ValidationResult with success status and errors
        """
        try:
            if not isinstance(expression, str):
                return ValidationResult.invalid_result(["Expression must be a string"])

            if not expression.strip():
                return ValidationResult.invalid_result(["Expression cannot be empty"])

            # Try to parse the expression
            ast = self.parser.parse(expression)
            self.parser.validate_ast(ast)

            return ValidationResult.valid_result()

        except SyntaxError as e:
            return ValidationResult.invalid_result([str(e)])
        except Exception as e:
            return ValidationResult.invalid_result([f"Validation error: {str(e)}"])

    def evaluate_batch(
        self,
        expressions: List[str],
        variables: Optional[Dict[str, float]] = None
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple expressions in batch.

        Args:
            expressions: List of mathematical expression strings
            variables: Optional variable definitions for all expressions

        Returns:
            List of EvaluationResult objects
        """
        if not isinstance(expressions, list):
            raise TypeError("Expressions must be a list")

        results = []
        for expression in expressions:
            result = self.evaluate_expression(expression, variables)
            results.append(result)

        return results

    def set_variable(self, name: str, value: float) -> None:
        """
        Set a variable value.

        Args:
            name: Variable name
            value: Variable value

        Raises:
            TypeError: If name is not string or value is not numeric
        """
        if not isinstance(name, str):
            raise TypeError("Variable name must be a string")
        if not isinstance(value, (int, float)):
            raise TypeError("Variable value must be numeric")

        self.evaluator.set_variable(name, value)
        # Clear cache when variables change
        self.cache.clear()

    def get_variable(self, name: str) -> float:
        """
        Get a variable value.

        Args:
            name: Variable name

        Returns:
            Variable value

        Raises:
            VariableError: If variable is not defined
        """
        return self.evaluator.get_variable(name)

    def clear_variables(self) -> None:
        """Clear all user-defined variables."""
        self.evaluator.clear_variables()
        self.cache.clear()

    def get_variables(self) -> Dict[str, float]:
        """Get all current variables."""
        return self.context.variables.copy()

    def get_constants(self) -> Dict[str, float]:
        """Get all mathematical constants."""
        return self.context.constants.copy()

    def get_functions(self) -> List[str]:
        """Get list of available function names."""
        return list(self.context.functions.keys())

    def add_function(self, name: str, function) -> None:
        """
        Add a custom function.

        Args:
            name: Function name
            function: Callable function

        Raises:
            TypeError: If name is not string or function is not callable
        """
        if not isinstance(name, str):
            raise TypeError("Function name must be a string")
        if not callable(function):
            raise TypeError("Function must be callable")

        self.context.functions[name] = function
        self.cache.clear()

    def remove_function(self, name: str) -> None:
        """
        Remove a custom function.

        Args:
            name: Function name to remove

        Raises:
            KeyError: If function doesn't exist
        """
        if name in self.context.functions:
            del self.context.functions[name]
            self.cache.clear()
        else:
            raise KeyError(f"Function '{name}' not found")

    def get_ast_string(self, expression: str) -> str:
        """
        Get string representation of expression's AST.

        Args:
            expression: Mathematical expression string

        Returns:
            String representation of the AST

        Raises:
            SyntaxError: If expression has syntax errors
        """
        ast = self.parse_expression(expression)
        return self.parser.ast_to_string(ast)

    def clear_cache(self) -> None:
        """Clear the expression cache."""
        self.cache.clear()

    def get_statistics(self) -> Dict[str, Union[int, float]]:
        """
        Get evaluation statistics.

        Returns:
            Dictionary containing statistics
        """
        avg_time = (self.total_evaluation_time / self.evaluation_count
                   if self.evaluation_count > 0 else 0.0)

        return {
            'total_evaluations': self.evaluation_count,
            'total_evaluation_time': self.total_evaluation_time,
            'average_evaluation_time': avg_time,
            'cache_size': len(self.cache),
            'variable_count': len(self.context.variables),
            'function_count': len(self.context.functions)
        }

    def reset_statistics(self) -> None:
        """Reset all statistics."""
        self.evaluation_count = 0
        self.total_evaluation_time = 0.0

    def __str__(self) -> str:
        """String representation of the expression manager."""
        stats = self.get_statistics()
        return (f"ExpressionManager(evaluations={stats['total_evaluations']}, "
                f"variables={stats['variable_count']}, "
                f"functions={stats['function_count']})")

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"ExpressionManager(context={self.context}, "
                f"cache_size={len(self.cache)}, "
                f"evaluations={self.evaluation_count})")


# Convenience functions for simple usage
def evaluate(expression: str, variables: Optional[Dict[str, float]] = None) -> float:
    """
    Convenience function to evaluate a single expression.

    Args:
        expression: Mathematical expression string
        variables: Optional variable definitions

    Returns:
        Numerical result

    Raises:
        ExpressionError: If evaluation fails
    """
    manager = ExpressionManager()
    result = manager.evaluate_expression(expression, variables)

    if result.success:
        return result.value
    else:
        raise ExpressionError(result.error_message)


def validate(expression: str) -> bool:
    """
    Convenience function to validate an expression.

    Args:
        expression: Mathematical expression string

    Returns:
        True if expression is valid, False otherwise
    """
    manager = ExpressionManager()
    result = manager.validate_expression(expression)
    return result.valid