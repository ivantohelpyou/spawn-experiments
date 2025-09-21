"""
Example usage of the Expression Evaluator system.

This module demonstrates various ways to use the expression evaluator,
from simple calculations to advanced features like custom functions
and batch processing.
"""

from expression_manager import ExpressionManager, evaluate, validate
from models import VariableContext
import math


def basic_usage_examples():
    """Demonstrate basic usage of the expression evaluator."""
    print("=== Basic Usage Examples ===")

    # Simple arithmetic
    print("1. Simple arithmetic:")
    print(f"   2 + 3 * 4 = {evaluate('2 + 3 * 4')}")
    print(f"   (2 + 3) * 4 = {evaluate('(2 + 3) * 4')}")
    print(f"   2 ** 3 ** 2 = {evaluate('2 ** 3 ** 2')}")
    print()

    # Mathematical functions
    print("2. Mathematical functions:")
    print(f"   sin(pi/2) = {evaluate('sin(pi/2)')}")
    print(f"   sqrt(16) = {evaluate('sqrt(16)')}")
    print(f"   log(e) = {evaluate('log(e)')}")
    print(f"   abs(-5) = {evaluate('abs(-5)')}")
    print()

    # Variables
    print("3. Using variables:")
    variables = {"x": 10, "y": 5}
    print(f"   With x=10, y=5:")
    print(f"   x + y = {evaluate('x + y', variables)}")
    print(f"   x * y = {evaluate('x * y', variables)}")
    print(f"   sqrt(x^2 + y^2) = {evaluate('sqrt(x**2 + y**2)', variables)}")
    print()


def advanced_usage_examples():
    """Demonstrate advanced usage features."""
    print("=== Advanced Usage Examples ===")

    # Using ExpressionManager for more control
    manager = ExpressionManager()

    # Setting persistent variables
    print("1. Persistent variables:")
    manager.set_variable("radius", 5.0)
    manager.set_variable("height", 10.0)

    # Calculate volume and surface area of cylinder
    volume = manager.evaluate_expression("pi * radius**2 * height")
    surface_area = manager.evaluate_expression("2 * pi * radius * (radius + height)")

    print(f"   Cylinder with radius=5, height=10:")
    print(f"   Volume = {volume.value:.2f}")
    print(f"   Surface Area = {surface_area.value:.2f}")
    print()

    # Batch processing
    print("2. Batch processing:")
    expressions = [
        "2 + 3",
        "sin(pi/4)",
        "sqrt(2)",
        "log(10)",
        "e**2"
    ]

    results = manager.evaluate_batch(expressions)
    for expr, result in zip(expressions, results):
        if result.success:
            print(f"   {expr} = {result.value:.6f}")
        else:
            print(f"   {expr} = ERROR: {result.error_message}")
    print()

    # Custom functions
    print("3. Custom functions:")

    def celsius_to_fahrenheit(c):
        """Convert Celsius to Fahrenheit."""
        return c * 9/5 + 32

    def quadratic_formula(a, b, c):
        """Calculate discriminant of quadratic equation."""
        return b**2 - 4*a*c

    manager.add_function("c_to_f", celsius_to_fahrenheit)
    manager.add_function("discriminant", quadratic_formula)

    temp_result = manager.evaluate_expression("c_to_f(25)")
    disc_result = manager.evaluate_expression("discriminant(1, -5, 6)")

    print(f"   25°C in Fahrenheit = {temp_result.value}°F")
    print(f"   Discriminant of x² - 5x + 6 = {disc_result.value}")
    print()


def validation_examples():
    """Demonstrate expression validation."""
    print("=== Validation Examples ===")

    test_expressions = [
        "2 + 3",           # Valid
        "sin(pi/2)",       # Valid
        "2 +",             # Invalid - incomplete
        "* 3",             # Invalid - leading operator
        "sqrt(-1)",        # Valid syntax, but domain error
        "undefined_var",   # Valid syntax, but undefined variable
    ]

    manager = ExpressionManager()

    for expr in test_expressions:
        # Syntax validation
        validation = manager.validate_expression(expr)
        print(f"   '{expr}':")
        print(f"     Syntax: {'Valid' if validation.valid else 'Invalid'}")

        if not validation.valid:
            print(f"     Errors: {'; '.join(validation.errors)}")
        else:
            # Try evaluation to check for runtime errors
            result = manager.evaluate_expression(expr)
            if result.success:
                print(f"     Evaluation: {result.value}")
            else:
                print(f"     Runtime Error: {result.error_message}")
        print()


def performance_examples():
    """Demonstrate performance characteristics."""
    print("=== Performance Examples ===")

    manager = ExpressionManager()

    # Simple expression performance
    result = manager.evaluate_expression("2 + 3 * 4")
    print(f"1. Simple expression timing:")
    print(f"   Expression: '2 + 3 * 4'")
    print(f"   Result: {result.value}")
    print(f"   Time: {result.execution_time:.6f} seconds")
    print()

    # Complex expression performance
    complex_expr = "sin(cos(tan(sqrt(abs(log(exp(pi)))))))"
    result = manager.evaluate_expression(complex_expr)
    print(f"2. Complex expression timing:")
    print(f"   Expression: '{complex_expr}'")
    print(f"   Result: {result.value:.6f}")
    print(f"   Time: {result.execution_time:.6f} seconds")
    print()

    # Caching demonstration
    print("3. Caching demonstration:")
    expr = "sqrt(sin(pi/4)**2 + cos(pi/4)**2)"

    # First evaluation
    result1 = manager.evaluate_expression(expr)
    print(f"   First evaluation: {result1.execution_time:.6f} seconds")

    # Second evaluation (cached)
    result2 = manager.evaluate_expression(expr)
    print(f"   Second evaluation: {result2.execution_time:.6f} seconds")
    print(f"   Speedup: {result1.execution_time / result2.execution_time:.1f}x")
    print()

    # Statistics
    stats = manager.get_statistics()
    print("4. Overall statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.6f}")
        else:
            print(f"   {key}: {value}")
    print()


def error_handling_examples():
    """Demonstrate error handling capabilities."""
    print("=== Error Handling Examples ===")

    manager = ExpressionManager()

    error_cases = [
        ("1 / 0", "Division by zero"),
        ("sqrt(-1)", "Domain error"),
        ("log(0)", "Logarithm of zero"),
        ("undefined_var", "Undefined variable"),
        ("sin()", "Wrong number of arguments"),
        ("2 +", "Syntax error"),
        ("((2)", "Unmatched parentheses"),
    ]

    for expr, description in error_cases:
        result = manager.evaluate_expression(expr)
        print(f"   {description}:")
        print(f"     Expression: '{expr}'")
        print(f"     Error: {result.error_message}")
        print()


def scientific_computing_example():
    """Demonstrate scientific computing capabilities."""
    print("=== Scientific Computing Example ===")

    manager = ExpressionManager()

    # Physics: projectile motion calculations
    print("1. Projectile Motion Calculator:")
    print("   Given: initial velocity = 20 m/s, angle = 45°, gravity = 9.81 m/s²")

    # Set variables
    manager.set_variable("v0", 20)      # initial velocity (m/s)
    manager.set_variable("angle", 45)   # launch angle (degrees)
    manager.set_variable("g", 9.81)     # gravity (m/s²)

    # Convert angle to radians and calculate components
    theta_rad = manager.evaluate_expression("radians(angle)")
    v0x = manager.evaluate_expression("v0 * cos(radians(angle))")
    v0y = manager.evaluate_expression("v0 * sin(radians(angle))")

    print(f"   Initial velocity components:")
    print(f"     v0x = {v0x.value:.2f} m/s")
    print(f"     v0y = {v0y.value:.2f} m/s")

    # Calculate flight time, max height, and range
    flight_time = manager.evaluate_expression("2 * v0 * sin(radians(angle)) / g")
    max_height = manager.evaluate_expression("(v0 * sin(radians(angle)))**2 / (2 * g)")
    range_distance = manager.evaluate_expression("v0**2 * sin(2 * radians(angle)) / g")

    print(f"   Results:")
    print(f"     Flight time = {flight_time.value:.2f} seconds")
    print(f"     Maximum height = {max_height.value:.2f} meters")
    print(f"     Range = {range_distance.value:.2f} meters")
    print()

    # Chemistry: ideal gas law
    print("2. Ideal Gas Law Calculator:")
    print("   PV = nRT, solve for different variables")

    # Gas constant (L·atm/(mol·K))
    manager.set_variable("R", 0.08206)

    # Given conditions
    conditions = [
        {"P": 1.0, "V": 22.4, "n": 1.0, "solve": "T"},
        {"P": 2.0, "T": 298, "n": 0.5, "solve": "V"},
        {"V": 10.0, "T": 273, "P": 1.5, "solve": "n"},
    ]

    for condition in conditions:
        for var, val in condition.items():
            if var != "solve":
                manager.set_variable(var, val)

        solve_var = condition["solve"]
        if solve_var == "T":
            result = manager.evaluate_expression("P * V / (n * R)")
            print(f"     Given P={condition['P']}, V={condition['V']}, n={condition['n']}")
            print(f"     Temperature T = {result.value:.1f} K")
        elif solve_var == "V":
            result = manager.evaluate_expression("n * R * T / P")
            print(f"     Given P={condition['P']}, T={condition['T']}, n={condition['n']}")
            print(f"     Volume V = {result.value:.2f} L")
        elif solve_var == "n":
            result = manager.evaluate_expression("P * V / (R * T)")
            print(f"     Given P={condition['P']}, V={condition['V']}, T={condition['T']}")
            print(f"     Amount n = {result.value:.3f} mol")
    print()


def interactive_example():
    """Demonstrate how to create an interactive calculator."""
    print("=== Interactive Calculator Example ===")
    print("This would typically run as an interactive session.")
    print("Here's what the interaction might look like:")
    print()

    # Simulate interactive session
    manager = ExpressionManager()

    simulated_inputs = [
        "2 + 3 * 4",
        "x = 10",
        "y = 5",
        "x + y",
        "sqrt(x**2 + y**2)",
        "sin(pi/4) + cos(pi/4)",
    ]

    for input_expr in simulated_inputs:
        print(f">>> {input_expr}")

        # Handle variable assignment
        if "=" in input_expr and not any(op in input_expr for op in ["==", "!=", "<=", ">="]):
            var_name, value_expr = input_expr.split("=", 1)
            var_name = var_name.strip()
            value_result = manager.evaluate_expression(value_expr.strip())
            if value_result.success:
                manager.set_variable(var_name, value_result.value)
                print(f"{var_name} = {value_result.value}")
            else:
                print(f"Error: {value_result.error_message}")
        else:
            # Regular expression evaluation
            result = manager.evaluate_expression(input_expr)
            if result.success:
                print(f"{result.value}")
            else:
                print(f"Error: {result.error_message}")
        print()


def main():
    """Run all examples."""
    print("Expression Evaluator - Example Usage")
    print("=" * 50)
    print()

    basic_usage_examples()
    advanced_usage_examples()
    validation_examples()
    performance_examples()
    error_handling_examples()
    scientific_computing_example()
    interactive_example()

    print("All examples completed!")


if __name__ == "__main__":
    main()