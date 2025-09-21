def is_balanced(s):
    """Check if parentheses are balanced in the given string.

    Supports three types of brackets: (), [], {}
    Returns True if all brackets are properly matched and nested.
    """
    stack = []
    # Define bracket pairs for easy lookup
    closing_to_opening = {')': '(', ']': '[', '}': '{'}
    opening_brackets = '([{'

    for char in s:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_to_opening:
            if not stack:
                return False
            opening = stack.pop()
            if opening != closing_to_opening[char]:
                return False

    return len(stack) == 0