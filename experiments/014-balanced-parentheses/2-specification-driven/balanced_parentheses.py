"""
Balanced Parentheses Checker

A comprehensive implementation for validating balanced brackets, parentheses, and braces
in strings according to the specification in SPECIFICATION.md.
"""

from typing import Dict


def is_balanced(s: str) -> bool:
    """
    Check if brackets in a string are balanced.

    Validates that parentheses (), brackets [], and braces {} are properly
    matched and nested according to the following rules:
    - Every opening bracket has a corresponding closing bracket of the same type
    - Closing brackets appear after their corresponding opening brackets
    - Brackets are properly nested (no interleaving)
    - Opening and closing brackets are of the same type

    Args:
        s (str): Input string to check

    Returns:
        bool: True if brackets are balanced, False otherwise

    Raises:
        TypeError: If input is not a string

    Examples:
        >>> is_balanced("")
        True
        >>> is_balanced("()")
        True
        >>> is_balanced("([{}])")
        True
        >>> is_balanced("([)]")
        False
        >>> is_balanced("(()")
        False
    """
    # Input validation
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    # Define bracket mappings
    opening_brackets = {'(', '[', '{'}
    closing_brackets = {')', ']', '}'}
    bracket_pairs: Dict[str, str] = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    # Stack to track opening brackets
    stack = []

    # Process each character in the string
    for char in s:
        if char in opening_brackets:
            # Push opening bracket onto stack
            stack.append(char)
        elif char in closing_brackets:
            # Check for matching opening bracket
            if not stack:
                # No opening bracket to match with this closing bracket
                return False

            # Pop the most recent opening bracket
            last_opening = stack.pop()

            # Verify it matches the current closing bracket
            if last_opening != bracket_pairs[char]:
                # Bracket type mismatch
                return False
        # Ignore all other characters (non-bracket characters)

    # All brackets are balanced if stack is empty
    # (no unmatched opening brackets remain)
    return len(stack) == 0


def get_balance_info(s: str) -> Dict[str, any]:
    """
    Get detailed information about bracket balance in a string.

    This diagnostic function provides additional information about why
    a string might be unbalanced, useful for debugging and error reporting.

    Args:
        s (str): Input string to analyze

    Returns:
        dict: Dictionary containing:
            - 'is_balanced': bool indicating if string is balanced
            - 'unmatched_opening': list of positions of unmatched opening brackets
            - 'error_position': int position where first error occurred (or -1)
            - 'error_type': str description of the error type

    Raises:
        TypeError: If input is not a string
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected string input, got {type(s).__name__}")

    opening_brackets = {'(', '[', '{'}
    closing_brackets = {')', ']', '}'}
    bracket_pairs = {')': '(', ']': '[', '}': '{'}

    stack = []
    stack_positions = []  # Track positions of opening brackets

    for i, char in enumerate(s):
        if char in opening_brackets:
            stack.append(char)
            stack_positions.append(i)
        elif char in closing_brackets:
            if not stack:
                return {
                    'is_balanced': False,
                    'unmatched_opening': [],
                    'error_position': i,
                    'error_type': f'Unmatched closing bracket "{char}"'
                }

            last_opening = stack.pop()
            stack_positions.pop()

            if last_opening != bracket_pairs[char]:
                return {
                    'is_balanced': False,
                    'unmatched_opening': stack_positions,
                    'error_position': i,
                    'error_type': f'Bracket type mismatch: expected closing for "{last_opening}", got "{char}"'
                }

    is_balanced_result = len(stack) == 0
    return {
        'is_balanced': is_balanced_result,
        'unmatched_opening': stack_positions if not is_balanced_result else [],
        'error_position': -1 if is_balanced_result else stack_positions[0] if stack_positions else -1,
        'error_type': '' if is_balanced_result else f'Unmatched opening brackets: {stack}'
    }


if __name__ == "__main__":
    # Quick demonstration
    test_cases = [
        "",
        "()",
        "([{}])",
        "([)]",
        "(((",
        ")))",
        "hello(world)",
        "a[b{c}d]e"
    ]

    print("Balanced Parentheses Checker Demo")
    print("=" * 40)

    for test in test_cases:
        result = is_balanced(test)
        print(f'"{test}" -> {result}')

        # Show detailed info for unbalanced cases
        if not result:
            info = get_balance_info(test)
            print(f"  Error: {info['error_type']} at position {info['error_position']}")

    print("\nDemo completed successfully!")