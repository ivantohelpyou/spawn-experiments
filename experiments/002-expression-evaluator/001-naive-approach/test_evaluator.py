#!/usr/bin/env python3
"""
Test script for the Expression Evaluator

This script runs comprehensive tests on the expression evaluator to ensure
it works correctly and handles various edge cases.
"""

import sys
import math
from expression_evaluator import ExpressionEvaluator


def run_tests():
    """Run comprehensive tests on the expression evaluator."""
    evaluator = ExpressionEvaluator()

    # Test cases: (expression, expected_result, description)
    test_cases = [
        # Basic arithmetic
        ("2 + 3", 5, "Basic addition"),
        ("10 - 4", 6, "Basic subtraction"),
        ("3 * 4", 12, "Basic multiplication"),
        ("15 / 3", 5, "Basic division"),
        ("17 % 5", 2, "Modulo operation"),
        ("2 ** 3", 8, "Exponentiation"),

        # Order of operations
        ("2 + 3 * 4", 14, "Multiplication before addition"),
        ("(2 + 3) * 4", 20, "Parentheses override precedence"),
        ("2 * 3 + 4", 10, "Left to right with same precedence"),
        ("2 + 3 * 4 - 1", 13, "Multiple operations"),

        # Parentheses
        ("((2 + 3) * 4)", 20, "Nested parentheses"),
        ("(10 - 5) * (3 + 2)", 25, "Multiple parentheses groups"),

        # Functions
        ("abs(-5)", 5, "Absolute value"),
        ("round(3.7)", 4, "Rounding"),
        ("sqrt(16)", 4, "Square root"),
        ("pow(2, 3)", 8, "Power function"),
        ("max(1, 5, 3)", 5, "Maximum function"),
        ("min(1, 5, 3)", 1, "Minimum function"),

        # Math functions (approximate comparisons needed)
        ("sin(0)", 0, "Sine of 0"),
        ("cos(0)", 1, "Cosine of 0"),
        ("log(e)", 1, "Natural log of e"),
        ("exp(0)", 1, "e^0"),

        # Constants
        ("pi", math.pi, "Pi constant"),
        ("e", math.e, "e constant"),
        ("2 * pi", 2 * math.pi, "Pi in expression"),

        # Complex expressions
        ("sqrt(2**2 + 3**2)", math.sqrt(13), "Pythagorean theorem"),
        ("sin(pi/2)", 1, "Sine of pi/2"),
        ("cos(pi)", -1, "Cosine of pi"),
        ("2**(3+1)", 16, "Exponentiation with parentheses"),

        # Decimal numbers
        ("3.14 + 2.86", 6.0, "Decimal addition"),
        ("1.5 * 2", 3.0, "Decimal multiplication"),
        ("7.5 / 2.5", 3.0, "Decimal division"),

        # Negative numbers
        ("-5 + 3", -2, "Negative number addition"),
        ("5 * -2", -10, "Multiplication with negative"),
        ("(-3) ** 2", 9, "Negative number squared"),
    ]

    # Error test cases: (expression, expected_error_type, description)
    error_cases = [
        ("", ValueError, "Empty expression"),
        ("   ", ValueError, "Whitespace only"),
        ("2 +", SyntaxError, "Incomplete expression"),
        ("2 + + 3", SyntaxError, "Invalid syntax"),
        ("1 / 0", ZeroDivisionError, "Division by zero"),
        ("unknown_function(1)", ValueError, "Unknown function"),
        ("import os", ValueError, "Dangerous import"),
        ("__builtins__", ValueError, "Accessing builtins"),
        ("sqrt(-1)", ValueError, "Square root of negative"),
        ("log(0)", ValueError, "Log of zero"),
    ]

    print("Running Expression Evaluator Tests")
    print("=" * 50)

    # Run successful test cases
    passed = 0
    failed = 0

    print("\nTesting valid expressions:")
    print("-" * 30)

    for expr, expected, description in test_cases:
        try:
            result = evaluator.evaluate(expr)

            # For floating point comparisons, use approximate equality
            if isinstance(expected, float) and isinstance(result, (int, float)):
                if abs(result - expected) < 1e-10:
                    print(f"✓ {description}: {expr} = {result}")
                    passed += 1
                else:
                    print(f"✗ {description}: {expr} = {result}, expected {expected}")
                    failed += 1
            elif result == expected:
                print(f"✓ {description}: {expr} = {result}")
                passed += 1
            else:
                print(f"✗ {description}: {expr} = {result}, expected {expected}")
                failed += 1

        except Exception as e:
            print(f"✗ {description}: {expr} raised {type(e).__name__}: {e}")
            failed += 1

    print(f"\nTesting error cases:")
    print("-" * 30)

    # Run error test cases
    for expr, expected_error, description in error_cases:
        try:
            result = evaluator.evaluate(expr)
            print(f"✗ {description}: {expr} should have raised {expected_error.__name__} but got {result}")
            failed += 1
        except expected_error:
            print(f"✓ {description}: {expr} correctly raised {expected_error.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ {description}: {expr} raised {type(e).__name__} instead of {expected_error.__name__}")
            failed += 1

    # Summary
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("All tests passed! ✓")
        return True
    else:
        print(f"Some tests failed. ✗")
        return False


def demo_features():
    """Demonstrate the key features of the evaluator."""
    evaluator = ExpressionEvaluator()

    print("\nDemonstrating Expression Evaluator Features")
    print("=" * 50)

    demonstrations = [
        "Basic arithmetic: 2 + 3 * 4",
        "Parentheses: (2 + 3) * 4",
        "Functions: sqrt(16) + abs(-5)",
        "Constants: sin(pi/2) + cos(0)",
        "Complex: sqrt(2**2 + 3**2)",
        "Decimals: 3.14159 * 2",
    ]

    for demo in demonstrations:
        expr = demo.split(": ")[1]
        try:
            result = evaluator.evaluate(expr)
            print(f"{demo} = {result}")
        except Exception as e:
            print(f"{demo} = ERROR: {e}")

    print("\nAvailable functions:")
    functions = evaluator.get_available_functions()
    for func, desc in list(functions.items())[:5]:  # Show first 5
        print(f"  {func} - {desc}")
    print(f"  ... and {len(functions) - 5} more")

    print("\nAvailable constants:")
    constants = evaluator.get_available_constants()
    for name, value in constants.items():
        print(f"  {name} = {value}")


if __name__ == "__main__":
    print("Expression Evaluator Test Suite")
    print("=" * 50)

    # Run tests
    success = run_tests()

    # Show demo
    demo_features()

    # Exit with appropriate code
    sys.exit(0 if success else 1)