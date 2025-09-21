def is_balanced(s):
    """
    Check if parentheses, brackets, and braces are balanced in a string.

    Args:
        s (str): The string to check

    Returns:
        bool: True if balanced, False otherwise
    """
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    opening = set(pairs.keys())
    closing = set(pairs.values())

    for char in s:
        if char in opening:
            stack.append(char)
        elif char in closing:
            if not stack:
                return False
            if pairs[stack.pop()] != char:
                return False

    return len(stack) == 0


def test_is_balanced():
    """Test cases for the is_balanced function"""

    # Test basic balanced cases
    assert is_balanced("()") == True
    assert is_balanced("[]") == True
    assert is_balanced("{}") == True
    assert is_balanced("()[]{}") == True
    assert is_balanced("([{}])") == True
    assert is_balanced("{[()]}") == True

    # Test unbalanced cases
    assert is_balanced("(") == False
    assert is_balanced(")") == False
    assert is_balanced("([)]") == False
    assert is_balanced("((())") == False
    assert is_balanced("())") == False
    assert is_balanced("{[}]") == False

    # Test empty string
    assert is_balanced("") == True

    # Test strings with other characters
    assert is_balanced("hello(world)") == True
    assert is_balanced("a[b{c}d]e") == True
    assert is_balanced("text(missing") == False
    assert is_balanced("wrong)order") == False

    # Test complex cases
    assert is_balanced("({[]})") == True
    assert is_balanced("([{}])()") == True
    assert is_balanced("((()))") == True
    assert is_balanced("[[[[[]]]]") == False

    print("All tests passed!")


if __name__ == "__main__":
    test_is_balanced()