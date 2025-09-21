#!/usr/bin/env python3
"""
Demo script showing the balanced parentheses checker in action.
"""

from balanced_parentheses import is_balanced


def demo_balanced_parentheses():
    """Demonstrate the balanced parentheses checker with various examples."""

    print("=== Balanced Parentheses Checker Demo ===\n")

    test_cases = [
        # Basic cases
        ("", "Empty string"),
        ("()", "Simple parentheses"),
        ("[]", "Simple square brackets"),
        ("{}", "Simple curly braces"),

        # Nested cases
        ("([{}])", "Mixed nested brackets"),
        ("((()))", "Deeply nested parentheses"),
        ("([{()}])", "Complex nesting"),

        # Unbalanced cases
        ("(", "Single opening parenthesis"),
        (")", "Single closing parenthesis"),
        ("([)]", "Crossed brackets"),
        ("(]", "Mismatched types"),
        ("((())", "Missing closing bracket"),

        # With other characters
        ("hello(world)", "Text with parentheses"),
        ("a[b{c}d]e", "Mixed text and brackets"),
        ("function(x, y)", "Function call syntax"),

        # Edge cases
        (")()(", "Wrong order"),
        ("()[]{}()[]", "Multiple balanced pairs"),
        ("([{}]){[()]}", "Complex balanced pattern"),
    ]

    print(f"{'Test Case':<25} {'Result':<8} {'Description'}")
    print("-" * 60)

    for test_string, description in test_cases:
        try:
            result = is_balanced(test_string)
            result_str = "✓ True" if result else "✗ False"
            display_string = f'"{test_string}"' if test_string else '""'
            print(f"{display_string:<25} {result_str:<8} {description}")
        except Exception as e:
            print(f'"{test_string}":<25> Error    {str(e)}')

    print("\n=== Error Handling Demo ===\n")

    error_cases = [
        (None, "None input"),
        (123, "Integer input"),
        (['(', ')'], "List input"),
        ({'brackets': '()'}, "Dictionary input"),
    ]

    for test_input, description in error_cases:
        try:
            result = is_balanced(test_input)
            print(f"{str(test_input):<25} Unexpected: {result}")
        except TypeError as e:
            print(f"{str(test_input):<25} TypeError: {description} correctly handled")
        except Exception as e:
            print(f"{str(test_input):<25} Error: {str(e)}")


if __name__ == "__main__":
    demo_balanced_parentheses()