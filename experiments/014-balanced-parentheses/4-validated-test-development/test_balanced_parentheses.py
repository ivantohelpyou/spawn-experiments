"""
Comprehensive test suite for balanced parentheses checker.
Tests cover all balanced/unbalanced cases for (), [], {} pairs with edge cases.
This test suite is designed to validate implementation quality through systematic testing.
"""

import unittest
from balanced_parentheses import is_balanced


class TestBalancedParentheses(unittest.TestCase):
    """Test cases for balanced parentheses checker with comprehensive coverage."""

    def test_empty_string(self):
        """Empty string should be considered balanced."""
        assert is_balanced("") == True

    def test_single_character_strings(self):
        """Single characters should be unbalanced."""
        assert is_balanced("(") == False
        assert is_balanced(")") == False
        assert is_balanced("[") == False
        assert is_balanced("]") == False
        assert is_balanced("{") == False
        assert is_balanced("}") == False

    def test_simple_balanced_pairs(self):
        """Simple balanced pairs should return True."""
        assert is_balanced("()") == True
        assert is_balanced("[]") == True
        assert is_balanced("{}") == True

    def test_simple_unbalanced_pairs(self):
        """Simple unbalanced pairs should return False."""
        assert is_balanced(")(") == False
        assert is_balanced("][") == False
        assert is_balanced("}{") == False

    def test_mismatched_pairs(self):
        """Mismatched bracket types should return False."""
        assert is_balanced("(]") == False
        assert is_balanced("(}") == False
        assert is_balanced("[)") == False
        assert is_balanced("[}") == False
        assert is_balanced("{)") == False
        assert is_balanced("{]") == False

    def test_nested_balanced_pairs(self):
        """Nested balanced pairs should return True."""
        assert is_balanced("([])") == True
        assert is_balanced("({})") == True
        assert is_balanced("([{}])") == True
        assert is_balanced("({[]})") == True
        assert is_balanced("((()))") == True
        assert is_balanced("[[[]]]") == True
        assert is_balanced("{{{}}}") == True

    def test_nested_unbalanced_pairs(self):
        """Nested unbalanced pairs should return False."""
        assert is_balanced("([)]") == False
        assert is_balanced("({)}") == False
        assert is_balanced("([}])") == False
        assert is_balanced("({])") == False
        assert is_balanced("((())") == False
        assert is_balanced("[[[]") == False
        assert is_balanced("{{{}}") == False

    def test_multiple_balanced_pairs(self):
        """Multiple balanced pairs in sequence should return True."""
        assert is_balanced("()[]") == True
        assert is_balanced("(){}") == True
        assert is_balanced("[]{}") == True
        assert is_balanced("()[]{}") == True
        assert is_balanced("([]){}") == True
        assert is_balanced("()[]{}()") == True

    def test_multiple_unbalanced_pairs(self):
        """Multiple unbalanced pairs should return False."""
        assert is_balanced("()[") == False
        assert is_balanced("(){") == False
        assert is_balanced("[}{") == False
        assert is_balanced("()[]{}(") == False
        assert is_balanced("([]){}]") == False

    def test_complex_nested_structures(self):
        """Complex nested structures should be properly evaluated."""
        assert is_balanced("([{()}])") == True
        assert is_balanced("([{()}]){[]}") == True
        assert is_balanced("([{()}]){[()]}") == True
        assert is_balanced("([{()}]){[()]}{()}") == True
        assert is_balanced("((([{}])))") == True

    def test_complex_unbalanced_structures(self):
        """Complex unbalanced structures should return False."""
        assert is_balanced("([{()}])") == True  # This should be True, correcting...
        assert is_balanced("([{()}])") == True  # Let me add actual unbalanced ones
        assert is_balanced("([{()]}])") == False  # Extra bracket
        assert is_balanced("([{()}]){[]") == False  # Missing closing
        assert is_balanced("([{()}]){[()]}]") == False  # Extra closing
        assert is_balanced("([{()}]){[()]}{()") == False  # Missing closing
        assert is_balanced("((([{}]))") == False  # Missing closing paren

    def test_only_opening_brackets(self):
        """Strings with only opening brackets should return False."""
        assert is_balanced("(((") == False
        assert is_balanced("[[[") == False
        assert is_balanced("{{{") == False
        assert is_balanced("([{") == False

    def test_only_closing_brackets(self):
        """Strings with only closing brackets should return False."""
        assert is_balanced(")))") == False
        assert is_balanced("]]]") == False
        assert is_balanced("}}}") == False
        assert is_balanced(")]}") == False

    def test_alternating_brackets(self):
        """Alternating bracket patterns should be properly evaluated."""
        assert is_balanced("()()()") == True
        assert is_balanced("[][]") == True
        assert is_balanced("{}{}{}") == True
        assert is_balanced("()[]{}" ) == True
        assert is_balanced("())(") == False
        assert is_balanced("[])(") == False

    def test_deeply_nested_same_type(self):
        """Deeply nested brackets of same type should work."""
        assert is_balanced("(((())))") == True
        assert is_balanced("[[[[]]]]") == True
        assert is_balanced("{{{{}}}}") == True
        assert is_balanced("(((()))") == False
        assert is_balanced("[[[[]]") == False
        assert is_balanced("{{{{}}") == False

    def test_edge_case_patterns(self):
        """Edge case patterns that might trip up incorrect implementations."""
        assert is_balanced(")()(") == False  # Starts with closing
        assert is_balanced("(()") == False   # Unmatched at end
        assert is_balanced("())") == False   # Unmatched at end
        assert is_balanced("(()(") == False  # Multiple unmatched
        assert is_balanced("()()(") == False # Last one unmatched
        assert is_balanced("())(()") == False # Middle mismatch

    def test_mixed_complex_patterns(self):
        """Complex patterns mixing all bracket types."""
        assert is_balanced("([{}])") == True
        assert is_balanced("([{}]){()}") == True
        assert is_balanced("([{}]){()}[]") == True
        assert is_balanced("([{}]){()}[]{()}") == True
        assert is_balanced("([{}])({)[}]") == False  # Crossed brackets
        assert is_balanced("([{}]){()}[{()}") == False  # Missing closing
        assert is_balanced("([{}]){()}[]{()}}") == False  # Extra closing

    def test_stress_patterns(self):
        """Stress test patterns to validate robust implementation."""
        # Long balanced sequence
        long_balanced = "(" * 100 + ")" * 100
        assert is_balanced(long_balanced) == True

        # Long unbalanced sequence
        long_unbalanced = "(" * 100 + ")" * 99
        assert is_balanced(long_unbalanced) == False

        # Mixed long balanced
        mixed_long = "([{" * 10 + "}])" * 10
        assert is_balanced(mixed_long) == True

        # Mixed long unbalanced
        mixed_long_unbalanced = "([{" * 10 + "}])" * 9 + "([{"
        assert is_balanced(mixed_long_unbalanced) == False


class TestNonBracketCharacters(unittest.TestCase):
    """Test cases with non-bracket characters to ensure they're ignored properly."""

    def test_letters_with_balanced_brackets(self):
        """Letters should be ignored, only brackets matter."""
        assert is_balanced("a(b)c") == True
        assert is_balanced("hello[world]") == True
        assert is_balanced("test{case}") == True
        assert is_balanced("a(b[c{d}e]f)g") == True

    def test_letters_with_unbalanced_brackets(self):
        """Letters should be ignored, unbalanced brackets should still fail."""
        assert is_balanced("a(b") == False
        assert is_balanced("hello[world") == False
        assert is_balanced("test{case") == False
        assert is_balanced("a(b[c{d}e]f") == False

    def test_numbers_and_symbols(self):
        """Numbers and symbols should be ignored."""
        assert is_balanced("1(2)3") == True
        assert is_balanced("$[%]&") == True
        assert is_balanced("!(test)@") == True
        assert is_balanced("1(2") == False
        assert is_balanced("$[%") == False

    def test_only_non_bracket_characters(self):
        """Strings with no brackets should return True."""
        assert is_balanced("hello") == True
        assert is_balanced("123") == True
        assert is_balanced("!@#$%^&*") == True
        assert is_balanced("") == True

    def test_whitespace_with_brackets(self):
        """Whitespace should be ignored."""
        assert is_balanced(" ( ) ") == True
        assert is_balanced(" [ ] ") == True
        assert is_balanced(" { } ") == True
        assert is_balanced(" ( [ { } ] ) ") == True
        assert is_balanced(" ( [ ") == False
        assert is_balanced(" ) ] ") == False


class TestParameterValidation(unittest.TestCase):
    """Test cases for parameter validation and error handling."""

    def test_none_input(self):
        """None input should raise TypeError or return False."""
        with self.assertRaises(TypeError):
            is_balanced(None)

    def test_non_string_input(self):
        """Non-string input should raise TypeError."""
        with self.assertRaises(TypeError):
            is_balanced(123)

        with self.assertRaises(TypeError):
            is_balanced(['(', ')'])

        with self.assertRaises(TypeError):
            is_balanced({'brackets': '()'})


if __name__ == '__main__':
    unittest.main()