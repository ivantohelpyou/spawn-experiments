"""
Evaluator service for the Expression Evaluator system.

This module handles the evaluation of Abstract Syntax Trees (AST)
to produce numerical results from mathematical expressions.
"""

import math
import time
from typing import Optional, Dict, Any
try:
    from .models import ExpressionNode, NodeType, VariableContext, EvaluationResult
    from .exceptions import EvaluationError, VariableError, FunctionError
except ImportError:
    from models import ExpressionNode, NodeType, VariableContext, EvaluationResult
    from exceptions import EvaluationError, VariableError, FunctionError


class Evaluator:
    """
    Evaluates Abstract Syntax Trees to produce numerical results.

    The evaluator traverses the AST and performs mathematical operations,
    function calls, and variable substitutions to compute the final result.
    """

    # Maximum recursion depth to prevent stack overflow
    MAX_RECURSION_DEPTH = 1000

    # Maximum execution time in seconds
    MAX_EXECUTION_TIME = 10.0

    def __init__(self, context: Optional[VariableContext] = None):
        """
        Initialize the evaluator.

        Args:
            context: Variable context for evaluation (creates default if not provided)
        """
        self.context = context or VariableContext()
        self.recursion_depth = 0
        self.start_time = 0.0

    def evaluate(self, node: ExpressionNode, variables: Optional[Dict[str, float]] = None) -> EvaluationResult:
        """
        Evaluate an AST to produce a numerical result.

        Args:
            node: Root node of the AST to evaluate
            variables: Optional variable values for this evaluation

        Returns:
            EvaluationResult containing the computed value or error information
        """
        start_time = time.time()
        self.start_time = start_time
        self.recursion_depth = 0

        try:
            # Update context with provided variables
            if variables:
                for name, value in variables.items():
                    self.context.set_variable(name, value)

            # Evaluate the expression
            result = self._evaluate_node(node)
            execution_time = time.time() - start_time

            return EvaluationResult.success_result(result, execution_time)

        except Exception as e:
            execution_time = time.time() - start_time
            error_message = str(e)

            # Add specific error handling for common math errors
            if "division by zero" in error_message.lower():
                error_message = "Division by zero is not allowed"
            elif "domain error" in error_message.lower():
                error_message = "Mathematical domain error (e.g., sqrt of negative number)"
            elif "overflow" in error_message.lower():
                error_message = "Numerical overflow - result too large"

            return EvaluationResult.error_result(error_message, execution_time=execution_time)

    def _evaluate_node(self, node: ExpressionNode) -> float:
        """
        Recursively evaluate a single AST node.

        Args:
            node: The AST node to evaluate

        Returns:
            Numerical result of evaluating the node

        Raises:
            EvaluationError: If evaluation fails
            RecursionError: If recursion depth exceeds limit
            TimeoutError: If execution time exceeds limit
        """
        # Check recursion depth
        self.recursion_depth += 1
        if self.recursion_depth > self.MAX_RECURSION_DEPTH:
            raise EvaluationError("Maximum recursion depth exceeded")

        # Check execution time
        if time.time() - self.start_time > self.MAX_EXECUTION_TIME:
            raise EvaluationError("Execution time limit exceeded")

        try:
            if node.node_type == NodeType.NUMBER:
                return self._evaluate_number(node)
            elif node.node_type == NodeType.VARIABLE:
                return self._evaluate_variable(node)
            elif node.node_type == NodeType.CONSTANT:
                return self._evaluate_constant(node)
            elif node.node_type == NodeType.BINARY_OP:
                return self._evaluate_binary_operation(node)
            elif node.node_type == NodeType.UNARY_OP:
                return self._evaluate_unary_operation(node)
            elif node.node_type == NodeType.FUNCTION_CALL:
                return self._evaluate_function_call(node)
            else:
                raise EvaluationError(f"Unknown node type: {node.node_type}")

        finally:
            self.recursion_depth -= 1

    def _evaluate_number(self, node: ExpressionNode) -> float:
        """Evaluate a number node."""
        if node.value is None:
            raise EvaluationError("Number node has no value")

        try:
            return float(node.value)
        except (ValueError, TypeError) as e:
            raise EvaluationError(f"Invalid number: {node.value}") from e

    def _evaluate_variable(self, node: ExpressionNode) -> float:
        """Evaluate a variable node."""
        if node.value is None:
            raise EvaluationError("Variable node has no name")

        try:
            return self.context.get_variable(str(node.value))
        except VariableError as e:
            raise EvaluationError(str(e)) from e

    def _evaluate_constant(self, node: ExpressionNode) -> float:
        """Evaluate a constant node."""
        if node.value is None:
            raise EvaluationError("Constant node has no name")

        try:
            return self.context.get_variable(str(node.value))
        except VariableError as e:
            raise EvaluationError(str(e)) from e

    def _evaluate_binary_operation(self, node: ExpressionNode) -> float:
        """Evaluate a binary operation node."""
        if not node.left or not node.right:
            raise EvaluationError("Binary operation missing operand(s)")

        if not node.operator:
            raise EvaluationError("Binary operation missing operator")

        # Evaluate operands
        left_value = self._evaluate_node(node.left)
        right_value = self._evaluate_node(node.right)

        # Perform operation
        try:
            if node.operator == '+':
                return left_value + right_value
            elif node.operator == '-':
                return left_value - right_value
            elif node.operator == '*':
                return left_value * right_value
            elif node.operator == '/':
                if right_value == 0:
                    raise EvaluationError("Division by zero")
                return left_value / right_value
            elif node.operator == '//':
                if right_value == 0:
                    raise EvaluationError("Division by zero")
                return left_value // right_value
            elif node.operator == '%':
                if right_value == 0:
                    raise EvaluationError("Modulo by zero")
                return left_value % right_value
            elif node.operator in ('**', '^'):
                # Handle special cases for exponentiation
                if left_value == 0 and right_value < 0:
                    raise EvaluationError("Zero to negative power is undefined")
                if left_value < 0 and not float(right_value).is_integer():
                    raise EvaluationError("Negative base with non-integer exponent")
                return left_value ** right_value
            else:
                raise EvaluationError(f"Unknown binary operator: {node.operator}")

        except (OverflowError, ValueError) as e:
            raise EvaluationError(f"Mathematical error in {node.operator} operation: {str(e)}") from e

    def _evaluate_unary_operation(self, node: ExpressionNode) -> float:
        """Evaluate a unary operation node."""
        if not node.right:
            raise EvaluationError("Unary operation missing operand")

        if not node.operator:
            raise EvaluationError("Unary operation missing operator")

        # Evaluate operand
        operand_value = self._evaluate_node(node.right)

        # Perform operation
        if node.operator == '+':
            return +operand_value
        elif node.operator == '-':
            return -operand_value
        else:
            raise EvaluationError(f"Unknown unary operator: {node.operator}")

    def _evaluate_function_call(self, node: ExpressionNode) -> float:
        """Evaluate a function call node."""
        if not node.value:
            raise EvaluationError("Function call missing function name")

        function_name = str(node.value)

        try:
            function = self.context.get_function(function_name)
        except FunctionError as e:
            raise EvaluationError(str(e)) from e

        # Evaluate arguments
        if node.children is None:
            args = []
        else:
            args = [self._evaluate_node(child) for child in node.children]

        # Call function with arguments
        try:
            result = self._call_function_safely(function, args, function_name)
            return float(result)

        except Exception as e:
            raise EvaluationError(f"Error calling function {function_name}: {str(e)}") from e

    def _call_function_safely(self, function, args, function_name: str) -> float:
        """
        Safely call a function with argument validation.

        Args:
            function: The function to call
            args: List of arguments
            function_name: Name of the function (for error reporting)

        Returns:
            Result of the function call

        Raises:
            EvaluationError: If function call fails
        """
        # Validate argument count for known functions
        expected_args = self._get_expected_arg_count(function_name)
        if expected_args is not None:
            if len(args) != expected_args and expected_args != -1:  # -1 means variable args
                raise EvaluationError(
                    f"Function {function_name} expects {expected_args} argument(s), got {len(args)}"
                )

        # Special handling for functions that may have domain restrictions
        if function_name == 'sqrt' and len(args) == 1:
            if args[0] < 0:
                raise EvaluationError("Square root of negative number")

        elif function_name in ('log', 'log10', 'log2', 'ln') and len(args) >= 1:
            if args[0] <= 0:
                raise EvaluationError("Logarithm of non-positive number")

        elif function_name == 'asin' and len(args) == 1:
            if not (-1 <= args[0] <= 1):
                raise EvaluationError("arcsine domain error: argument must be in [-1, 1]")

        elif function_name == 'acos' and len(args) == 1:
            if not (-1 <= args[0] <= 1):
                raise EvaluationError("arccosine domain error: argument must be in [-1, 1]")

        elif function_name == 'factorial' and len(args) == 1:
            if args[0] < 0 or not float(args[0]).is_integer():
                raise EvaluationError("Factorial requires non-negative integer")

        # Call the function
        try:
            if len(args) == 0:
                return function()
            elif len(args) == 1:
                return function(args[0])
            elif len(args) == 2:
                return function(args[0], args[1])
            else:
                return function(*args)

        except (ValueError, ArithmeticError, OverflowError) as e:
            raise EvaluationError(f"Mathematical error in {function_name}: {str(e)}") from e

    def _get_expected_arg_count(self, function_name: str) -> Optional[int]:
        """
        Get the expected argument count for a function.

        Args:
            function_name: Name of the function

        Returns:
            Expected argument count, or None if unknown, or -1 if variable
        """
        arg_counts = {
            # 0 arguments
            # (none currently)

            # 1 argument
            'abs': 1, 'round': 1, 'int': 1, 'float': 1,
            'sin': 1, 'cos': 1, 'tan': 1,
            'asin': 1, 'acos': 1, 'atan': 1,
            'sinh': 1, 'cosh': 1, 'tanh': 1,
            'log': 1, 'log10': 1, 'log2': 1, 'ln': 1,
            'exp': 1, 'sqrt': 1,
            'ceil': 1, 'floor': 1, 'factorial': 1,
            'degrees': 1, 'radians': 1,

            # 2 arguments
            'atan2': 2, 'pow': 2,

            # Variable arguments
            'min': -1, 'max': -1, 'sum': -1,
        }

        return arg_counts.get(function_name)

    def set_variable(self, name: str, value: float) -> None:
        """Set a variable value in the context."""
        self.context.set_variable(name, value)

    def get_variable(self, name: str) -> float:
        """Get a variable value from the context."""
        return self.context.get_variable(name)

    def clear_variables(self) -> None:
        """Clear all user-defined variables."""
        self.context.variables.clear()

    def get_context(self) -> VariableContext:
        """Get the current variable context."""
        return self.context

    def __str__(self) -> str:
        """String representation of the evaluator."""
        return f"Evaluator(variables={len(self.context.variables)}, depth={self.recursion_depth})"