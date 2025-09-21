import unittest
from balanced_parentheses import is_balanced


class TestBalancedParentheses(unittest.TestCase):

    def test_empty_string_is_balanced(self):
        """Empty string should be considered balanced"""
        self.assertTrue(is_balanced(""))

    def test_single_pair_parentheses(self):
        """Single pair of parentheses should be balanced"""
        self.assertTrue(is_balanced("()"))

    def test_single_opening_parenthesis_is_unbalanced(self):
        """Single opening parenthesis should be unbalanced"""
        self.assertFalse(is_balanced("("))

    def test_single_closing_parenthesis_is_unbalanced(self):
        """Single closing parenthesis should be unbalanced"""
        self.assertFalse(is_balanced(")"))

    def test_wrong_order_parentheses_is_unbalanced(self):
        """Wrong order parentheses should be unbalanced"""
        self.assertFalse(is_balanced(")("))

    def test_square_brackets_balanced(self):
        """Single pair of square brackets should be balanced"""
        self.assertTrue(is_balanced("[]"))

    def test_square_brackets_unbalanced(self):
        """Unmatched square brackets should be unbalanced"""
        self.assertFalse(is_balanced("["))
        self.assertFalse(is_balanced("]"))

    def test_curly_braces_balanced(self):
        """Single pair of curly braces should be balanced"""
        self.assertTrue(is_balanced("{}"))

    def test_curly_braces_unbalanced(self):
        """Unmatched curly braces should be unbalanced"""
        self.assertFalse(is_balanced("{"))
        self.assertFalse(is_balanced("}"))

    def test_nested_parentheses_balanced(self):
        """Nested parentheses should be balanced"""
        self.assertTrue(is_balanced("(())"))
        self.assertTrue(is_balanced("((()))"))

    def test_nested_parentheses_unbalanced(self):
        """Nested parentheses should detect unbalanced cases"""
        self.assertFalse(is_balanced("(()"))
        self.assertFalse(is_balanced("())"))

    def test_multiple_pairs_balanced(self):
        """Multiple separate pairs should be balanced"""
        self.assertTrue(is_balanced("()()"))
        self.assertTrue(is_balanced("()[]{}"))
        self.assertTrue(is_balanced("()()()(())"))

    def test_mixed_bracket_types_balanced(self):
        """Mixed bracket types should be balanced when properly nested"""
        self.assertTrue(is_balanced("([{}])"))
        self.assertTrue(is_balanced("{[()]}"))
        self.assertTrue(is_balanced("[({})]"))

    def test_mixed_bracket_types_unbalanced(self):
        """Mixed bracket types should detect mismatched types"""
        self.assertFalse(is_balanced("([)]"))
        self.assertFalse(is_balanced("{[}]"))
        self.assertFalse(is_balanced("[(])}"))


if __name__ == "__main__":
    unittest.main()