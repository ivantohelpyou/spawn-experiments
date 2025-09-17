#!/usr/bin/env python3
"""
Naive Direct Approach Expression Evaluator

This is a simple, direct approach to evaluating mathematical expressions.
It uses Python's built-in eval() function with safety restrictions for simplicity.
"""

import re
import math
import operator
from typing import Union, Dict, Any


class ExpressionEvaluator:
    """A naive expression evaluator using restricted eval() approach."""

    def __init__(self):
        """Initialize the evaluator with safe functions and constants."""
        # Safe functions that can be used in expressions
        self.safe_functions = {
            # Basic math functions
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,

            # Math module functions
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'floor': math.floor,
            'ceil': math.ceil,
            'pow': pow,

            # Degree/radian conversion
            'radians': math.radians,
            'degrees': math.degrees,
        }

        # Safe constants
        self.safe_constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
        }

        # Combine functions and constants for eval namespace
        self.safe_namespace = {
            '__builtins__': {},  # Remove all builtins for security
            **self.safe_functions,
            **self.safe_constants
        }

    def validate_expression(self, expression: str) -> bool:
        """
        Validate that the expression contains only safe characters and patterns.

        Args:
            expression: The mathematical expression to validate

        Returns:
            True if expression is considered safe, False otherwise
        """
        # Remove whitespace for checking
        expr = expression.replace(' ', '')

        # Check for dangerous keywords or patterns
        dangerous_patterns = [
            '__', 'import', 'exec', 'eval', 'open', 'file', 'input',
            'raw_input', 'compile', 'globals', 'locals', 'vars',
            'dir', 'getattr', 'setattr', 'delattr', 'hasattr'
        ]

        expr_lower = expr.lower()
        for pattern in dangerous_patterns:
            if pattern in expr_lower:
                return False

        # Only allow safe characters: numbers, operators, parentheses, letters, dots, underscores
        safe_pattern = re.compile(r'^[0-9+\-*/().,a-zA-Z_\s**%]*$')
        if not safe_pattern.match(expression):
            return False

        return True

    def evaluate(self, expression: str) -> Union[float, int]:
        """
        Evaluate a mathematical expression safely.

        Args:
            expression: The mathematical expression to evaluate

        Returns:
            The numerical result of the expression

        Raises:
            ValueError: If the expression is invalid or unsafe
            ZeroDivisionError: If division by zero occurs
            OverflowError: If the result is too large
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")

        # Clean the expression
        expression = expression.strip()

        # Validate the expression
        if not self.validate_expression(expression):
            raise ValueError(f"Expression contains unsafe elements: {expression}")

        try:
            # Use eval with restricted namespace
            result = eval(expression, self.safe_namespace)

            # Ensure result is a number
            if not isinstance(result, (int, float, complex)):
                raise ValueError(f"Expression must evaluate to a number, got {type(result).__name__}")

            # Handle complex numbers (reject them for simplicity)
            if isinstance(result, complex):
                if result.imag != 0:
                    raise ValueError("Complex numbers are not supported")
                result = result.real

            # Check for infinity or NaN
            if isinstance(result, float):
                if math.isinf(result):
                    raise OverflowError("Result is infinite")
                if math.isnan(result):
                    raise ValueError("Result is not a number (NaN)")

            return result

        except ZeroDivisionError:
            raise ZeroDivisionError("Division by zero")
        except OverflowError:
            raise OverflowError("Mathematical overflow occurred")
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e}")
        except NameError as e:
            raise ValueError(f"Unknown function or variable: {e}")
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")

    def get_available_functions(self) -> Dict[str, str]:
        """Return a dictionary of available functions with descriptions."""
        return {
            'abs(x)': 'Absolute value',
            'round(x)': 'Round to nearest integer',
            'min(a,b,...)': 'Minimum value',
            'max(a,b,...)': 'Maximum value',
            'sqrt(x)': 'Square root',
            'sin(x)': 'Sine (radians)',
            'cos(x)': 'Cosine (radians)',
            'tan(x)': 'Tangent (radians)',
            'log(x)': 'Natural logarithm',
            'log10(x)': 'Base-10 logarithm',
            'exp(x)': 'e^x',
            'floor(x)': 'Floor (round down)',
            'ceil(x)': 'Ceiling (round up)',
            'pow(x,y)': 'x raised to power y',
            'radians(x)': 'Convert degrees to radians',
            'degrees(x)': 'Convert radians to degrees',
        }

    def get_available_constants(self) -> Dict[str, float]:
        """Return a dictionary of available constants."""
        return {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
        }


if __name__ == "__main__":
    # Basic test
    evaluator = ExpressionEvaluator()

    test_expressions = [
        "2 + 3 * 4",
        "(1 + 2) * 3",
        "sqrt(16)",
        "sin(pi/2)",
        "2**3",
        "abs(-5)",
        "max(1, 2, 3)",
    ]

    print("Testing Expression Evaluator:")
    print("=" * 40)

    for expr in test_expressions:
        try:
            result = evaluator.evaluate(expr)
            print(f"{expr:15} = {result}")
        except Exception as e:
            print(f"{expr:15} = ERROR: {e}")