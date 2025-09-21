#!/usr/bin/env python3
"""
Demonstration script for the Expression Evaluator

This script showcases the key features and capabilities of the
naive direct approach expression evaluator.
"""

from expression_evaluator import ExpressionEvaluator


def main():
    """Run a comprehensive demonstration of the expression evaluator."""
    print("Expression Evaluator Demonstration")
    print("=" * 50)
    print("Method 1: Naive Direct Approach")
    print("=" * 50)

    evaluator = ExpressionEvaluator()

    # Demonstration expressions with explanations
    demonstrations = [
        ("Basic Arithmetic", [
            ("2 + 3", "Simple addition"),
            ("10 - 4", "Simple subtraction"),
            ("3 * 4", "Simple multiplication"),
            ("15 / 3", "Simple division"),
            ("2 ** 3", "Exponentiation"),
            ("17 % 5", "Modulo operation"),
        ]),

        ("Order of Operations", [
            ("2 + 3 * 4", "Multiplication before addition"),
            ("(2 + 3) * 4", "Parentheses override precedence"),
            ("2 * 3 + 4 / 2", "Multiple operations"),
            ("((2 + 3) * 4) - 1", "Nested parentheses"),
        ]),

        ("Mathematical Functions", [
            ("sqrt(16)", "Square root"),
            ("abs(-5)", "Absolute value"),
            ("round(3.7)", "Rounding"),
            ("max(1, 5, 3, 9, 2)", "Maximum of multiple values"),
            ("min(1, 5, 3, 9, 2)", "Minimum of multiple values"),
        ]),

        ("Trigonometric Functions", [
            ("sin(0)", "Sine of 0"),
            ("cos(0)", "Cosine of 0"),
            ("sin(pi/2)", "Sine of π/2 (90 degrees)"),
            ("cos(pi)", "Cosine of π (180 degrees)"),
            ("tan(pi/4)", "Tangent of π/4 (45 degrees)"),
        ]),

        ("Logarithmic and Exponential", [
            ("log(e)", "Natural logarithm of e"),
            ("log10(100)", "Base-10 logarithm of 100"),
            ("exp(1)", "e^1"),
            ("exp(0)", "e^0"),
        ]),

        ("Using Constants", [
            ("pi", "Value of π"),
            ("e", "Value of e"),
            ("tau", "Value of τ (2π)"),
            ("2 * pi", "Expression with π"),
            ("e ** 2", "e squared"),
        ]),

        ("Complex Expressions", [
            ("sqrt(2**2 + 3**2)", "Pythagorean theorem: √(2² + 3²)"),
            ("sin(pi/6) + cos(pi/3)", "Sum of trigonometric functions"),
            ("(sqrt(5) + 1) / 2", "Golden ratio approximation"),
            ("log(10**3)", "Logarithm property: log(10³)"),
            ("2**(log(8)/log(2))", "Change of base: 2^(log₂(8))"),
        ]),

        ("Practical Examples", [
            ("degrees(pi/4)", "Convert π/4 radians to degrees"),
            ("radians(90)", "Convert 90 degrees to radians"),
            ("pow(1.08, 10)", "Compound interest: 1.08^10"),
            ("sqrt(pow(3,2) + pow(4,2))", "3-4-5 triangle hypotenuse"),
        ]),
    ]

    for category, expressions in demonstrations:
        print(f"\n{category}:")
        print("-" * len(category))

        for expr, description in expressions:
            try:
                result = evaluator.evaluate(expr)
                # Format the result nicely
                if isinstance(result, float):
                    if result.is_integer():
                        result_str = str(int(result))
                    else:
                        result_str = f"{result:.6g}"
                else:
                    result_str = str(result)

                print(f"  {expr:25} = {result_str:15} ({description})")

            except Exception as e:
                print(f"  {expr:25} = ERROR: {e}")

    # Show available functions and constants
    print(f"\nAvailable Functions ({len(evaluator.get_available_functions())}):")
    print("-" * 30)
    functions = evaluator.get_available_functions()
    for func, desc in functions.items():
        print(f"  {func:20} {desc}")

    print(f"\nAvailable Constants ({len(evaluator.get_available_constants())}):")
    print("-" * 30)
    constants = evaluator.get_available_constants()
    for name, value in constants.items():
        print(f"  {name:20} = {value}")

    print("\nFeatures:")
    print("-" * 10)
    print("✓ Basic arithmetic operations (+, -, *, /, %, **)")
    print("✓ Parentheses for grouping and precedence")
    print("✓ Mathematical functions (sqrt, sin, cos, log, etc.)")
    print("✓ Mathematical constants (pi, e, tau)")
    print("✓ Safety validation and error handling")
    print("✓ Interactive CLI interface")
    print("✓ Comprehensive test suite")

    print("\nApproach: Naive Direct Method")
    print("-" * 30)
    print("• Uses Python's eval() with restricted namespace")
    print("• Simple implementation with basic safety measures")
    print("• Good for educational purposes and simple calculations")
    print("• Trade-off: simplicity vs security and performance")

    print("\n" + "=" * 50)
    print("Demonstration complete!")


if __name__ == "__main__":
    main()