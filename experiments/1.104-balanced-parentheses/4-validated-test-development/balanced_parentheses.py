"""
Correct implementation: Type-aware stack-based balanced parentheses checker
Uses a stack to track opening brackets and ensures proper matching.
"""


def is_balanced(s):
    """
    Check if a string has balanced parentheses, brackets, and braces.

    Args:
        s (str): The string to check for balanced brackets.

    Returns:
        bool: True if all brackets are balanced, False otherwise.

    Raises:
        TypeError: If input is None or not a string.

    Examples:
        >>> is_balanced("()")
        True
        >>> is_balanced("([{}])")
        True
        >>> is_balanced("([)]")
        False
    """
    if s is None:
        raise TypeError("Input cannot be None")

    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    # Stack to keep track of opening brackets
    stack = []

    # Mapping of closing to opening brackets
    bracket_map = {')': '(', ']': '[', '}': '{'}

    # Process each character in the string
    for char in s:
        if char in '([{':
            # Push opening bracket onto stack
            stack.append(char)
        elif char in ')]}':
            # Check for matching opening bracket
            if not stack:
                # Closing bracket without opening bracket
                return False

            # Check if the closing bracket matches the most recent opening bracket
            if stack[-1] != bracket_map[char]:
                # Mismatched bracket types
                return False

            # Remove the matched opening bracket from stack
            stack.pop()
        # Ignore all other characters (letters, numbers, symbols, whitespace)

    # String is balanced if no unmatched opening brackets remain
    return len(stack) == 0