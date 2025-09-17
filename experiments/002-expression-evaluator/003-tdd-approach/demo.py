#!/usr/bin/env python3
"""
Demonstration of the Expression Evaluator built using TDD.

This script shows the complete functionality of the expression evaluator
that was built using strict Test-Driven Development principles.
"""

from expression_evaluator import ExpressionEvaluator


def demo_expression_evaluator():
    """Demonstrate the expression evaluator functionality."""
    evaluator = ExpressionEvaluator()

    print("=" * 60)
    print("EXPRESSION EVALUATOR - TDD IMPLEMENTATION DEMO")
    print("=" * 60)

    # Test cases organized by feature
    test_cases = [
        # Basic arithmetic
        ("Basic Arithmetic", [
            "42",
            "2 + 3",
            "10 - 4",
            "3 * 7",
            "15 / 3",
            "3.5 + 2.1",
        ]),

        # Operator precedence
        ("Operator Precedence", [
            "2 + 3 * 4",
            "10 - 6 / 2",
            "8 / 4 * 2",
            "2 + 3 * 4 - 1",
        ]),

        # Parentheses
        ("Parentheses", [
            "(2 + 3) * 4",
            "20 / (2 + 3)",
            "((2 + 3) * 4) / 2",
            "(2 + 3) * (4 - 1)",
        ]),

        # Advanced features
        ("Advanced Features", [
            "-5 + 3",
            "-(2 + 3)",
            "-(2 + 3) * 4",
            "-(-5)",
            "2 * -3",
            "1e2 + 3",
            "5e-2 * 100",
        ]),

        # Complex expressions
        ("Complex Expressions", [
            "1 + 2 + 3 + 4 + 5",
            "((1 + 2) * (3 + 4)) - ((5 - 2) * (6 / 3))",
            "(((2 + 3) * 4) / (2 + 3))",
            "0.1 + 0.2",
        ]),
    ]

    for category, expressions in test_cases:
        print(f"\n{category}:")
        print("-" * len(category))
        for expr in expressions:
            try:
                result = evaluator.evaluate(expr)
                print(f"  {expr:<30} = {result}")
            except Exception as e:
                print(f"  {expr:<30} = ERROR: {e}")

    # Error handling demonstration
    print(f"\nError Handling:")
    print("-" * 14)
    error_cases = [
        "5 / 0",
        "2 +",
        "+ 3",
        "2 + + 3",
        "(2 + 3",
        "2 + 3)",
        "()",
        "",
        "2 + a",
    ]

    for expr in error_cases:
        try:
            result = evaluator.evaluate(expr)
            print(f"  '{expr}':{' ' * (20 - len(expr))} = {result}")
        except Exception as e:
            print(f"  '{expr}':{' ' * (20 - len(expr))} = ERROR: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    print("TDD Implementation Summary:")
    print("- 4 TDD cycles: RED -> GREEN -> REFACTOR")
    print("- 40 comprehensive test cases")
    print("- Full operator precedence")
    print("- Parentheses support")
    print("- Comprehensive error handling")
    print("- Advanced features (unary minus, scientific notation)")
    print("=" * 60)


if __name__ == "__main__":
    demo_expression_evaluator()