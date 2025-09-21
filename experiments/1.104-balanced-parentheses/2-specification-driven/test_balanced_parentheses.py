"""
Comprehensive Test Suite for Balanced Parentheses Checker

Tests all requirements, edge cases, and scenarios defined in SPECIFICATION.md
"""

import unittest
import time
from balanced_parentheses import is_balanced, get_balance_info


class TestBalancedParentheses(unittest.TestCase):
    """Test suite for balanced parentheses checker."""

    def setUp(self):
        """Set up test fixtures."""
        self.start_time = time.time()

    def tearDown(self):
        """Clean up after tests."""
        elapsed = time.time() - self.start_time
        if elapsed > 0.1:  # Flag slow tests
            print(f"\n{self._testMethodName} took {elapsed:.3f}s")

    # =====================================================
    # BASIC FUNCTIONALITY TESTS
    # =====================================================

    def test_empty_string(self):
        """Test empty string is considered balanced."""
        self.assertTrue(is_balanced(""))

    def test_single_bracket_types_valid(self):
        """Test single matched pairs of each bracket type."""
        self.assertTrue(is_balanced("()"))
        self.assertTrue(is_balanced("[]"))
        self.assertTrue(is_balanced("{}"))

    def test_single_bracket_types_invalid(self):
        """Test single unmatched brackets."""
        self.assertFalse(is_balanced("("))
        self.assertFalse(is_balanced(")"))
        self.assertFalse(is_balanced("["))
        self.assertFalse(is_balanced("]"))
        self.assertFalse(is_balanced("{"))
        self.assertFalse(is_balanced("}"))

    def test_simple_matched_pairs(self):
        """Test simple sequences of matched pairs."""
        self.assertTrue(is_balanced("()[]{}"))
        self.assertTrue(is_balanced("()()()"))
        self.assertTrue(is_balanced("[][][][]"))
        self.assertTrue(is_balanced("{}{}{}"))

    def test_simple_unmatched_cases(self):
        """Test simple unmatched bracket scenarios."""
        self.assertFalse(is_balanced("(]"))
        self.assertFalse(is_balanced("[}"))
        self.assertFalse(is_balanced("{)"))
        self.assertFalse(is_balanced(")("))
        self.assertFalse(is_balanced("]("))
        self.assertFalse(is_balanced("}{"))

    # =====================================================
    # NESTING TESTS
    # =====================================================

    def test_proper_nesting_scenarios(self):
        """Test various proper nesting patterns."""
        # Simple nesting
        self.assertTrue(is_balanced("([])"))
        self.assertTrue(is_balanced("{[]}"))
        self.assertTrue(is_balanced("({})"))

        # Complex nesting
        self.assertTrue(is_balanced("([{}])"))
        self.assertTrue(is_balanced("{[()]}"))
        self.assertTrue(is_balanced("({[()]}[])"))

        # Deep nesting
        self.assertTrue(is_balanced("(((())))"))
        self.assertTrue(is_balanced("[[[[]]]]"))
        self.assertTrue(is_balanced("{{{{}}}}"))

        # Mixed deep nesting
        self.assertTrue(is_balanced("([{([{}])}])"))

    def test_invalid_nesting_patterns(self):
        """Test invalid nesting scenarios."""
        # Interleaving brackets
        self.assertFalse(is_balanced("([)]"))
        self.assertFalse(is_balanced("{[}]"))
        self.assertFalse(is_balanced("({)}"))

        # Cross-over patterns
        self.assertFalse(is_balanced("[(])"))
        self.assertFalse(is_balanced("{(})"))

        # Complex invalid nesting
        self.assertFalse(is_balanced("([{])})"))
        self.assertFalse(is_balanced("{[(})]"))

    def test_incomplete_nesting(self):
        """Test incomplete bracket sequences."""
        self.assertFalse(is_balanced("(["))
        self.assertFalse(is_balanced("([{"))
        self.assertFalse(is_balanced("([{}"))
        self.assertFalse(is_balanced("([{}]"))

    # =====================================================
    # EDGE CASE TESTS
    # =====================================================

    def test_non_bracket_characters(self):
        """Test strings containing non-bracket characters."""
        self.assertTrue(is_balanced("hello world"))
        self.assertTrue(is_balanced("hello(world)"))
        self.assertTrue(is_balanced("a[b]c"))
        self.assertTrue(is_balanced("x{y}z"))
        self.assertTrue(is_balanced("func(arg1, arg2)"))
        self.assertTrue(is_balanced("array[index]"))
        self.assertTrue(is_balanced("object{key: value}"))

        # Mixed content with invalid brackets
        self.assertFalse(is_balanced("hello(world"))
        self.assertFalse(is_balanced("array[index"))
        self.assertFalse(is_balanced("object{key: value"))

    def test_multiple_consecutive_pairs(self):
        """Test multiple consecutive bracket pairs."""
        self.assertTrue(is_balanced("()()()()()"))
        self.assertTrue(is_balanced("[][][][][][]"))
        self.assertTrue(is_balanced("{}{}{}{}{}"))
        self.assertTrue(is_balanced("()[]{}()[]{}"))

    def test_complex_mixed_scenarios(self):
        """Test complex scenarios with mixed bracket types and content."""
        self.assertTrue(is_balanced("if (condition) { statements[0] }"))
        self.assertTrue(is_balanced("func(params[0], {key: value})"))
        self.assertTrue(is_balanced("matrix[row][col] = {x: (a + b)}"))

        self.assertFalse(is_balanced("if (condition { statements[0] }"))
        self.assertFalse(is_balanced("func(params[0}, {key: value})"))

    # =====================================================
    # ERROR CONDITION TESTS
    # =====================================================

    def test_unmatched_opening_brackets(self):
        """Test strings with unmatched opening brackets."""
        self.assertFalse(is_balanced("((("))
        self.assertFalse(is_balanced("[[["))
        self.assertFalse(is_balanced("{{{"))
        self.assertFalse(is_balanced("({["))

    def test_unmatched_closing_brackets(self):
        """Test strings with unmatched closing brackets."""
        self.assertFalse(is_balanced(")))"))
        self.assertFalse(is_balanced("]]]"))
        self.assertFalse(is_balanced("}}}"))
        self.assertFalse(is_balanced(")}]"))

    def test_wrong_order_brackets(self):
        """Test brackets in wrong order."""
        self.assertFalse(is_balanced(")("))
        self.assertFalse(is_balanced("]("))
        self.assertFalse(is_balanced("}{"))
        self.assertFalse(is_balanced(")()"))
        self.assertFalse(is_balanced("][]"))
        self.assertFalse(is_balanced("}{}"))

    def test_type_conflict_scenarios(self):
        """Test bracket type conflicts."""
        self.assertFalse(is_balanced("(]"))
        self.assertFalse(is_balanced("[)"))
        self.assertFalse(is_balanced("{)"))
        self.assertFalse(is_balanced("(}"))
        self.assertFalse(is_balanced("[}"))
        self.assertFalse(is_balanced("{]"))

    # =====================================================
    # INPUT VALIDATION TESTS
    # =====================================================

    def test_invalid_input_types(self):
        """Test that non-string inputs raise TypeError."""
        with self.assertRaises(TypeError):
            is_balanced(None)

        with self.assertRaises(TypeError):
            is_balanced(123)

        with self.assertRaises(TypeError):
            is_balanced([])

        with self.assertRaises(TypeError):
            is_balanced({})

        with self.assertRaises(TypeError):
            is_balanced(True)

    # =====================================================
    # PERFORMANCE TESTS
    # =====================================================

    def test_large_string_performance(self):
        """Test performance with large strings."""
        # Create a large balanced string
        large_balanced = "(" * 1000 + ")" * 1000
        start_time = time.time()
        result = is_balanced(large_balanced)
        elapsed = time.time() - start_time

        self.assertTrue(result)
        self.assertLess(elapsed, 0.1, "Performance test failed: took too long")

        # Create a large unbalanced string
        large_unbalanced = "(" * 1000 + ")" * 999
        start_time = time.time()
        result = is_balanced(large_unbalanced)
        elapsed = time.time() - start_time

        self.assertFalse(result)
        self.assertLess(elapsed, 0.1, "Performance test failed: took too long")

    def test_deep_nesting_performance(self):
        """Test performance with deeply nested brackets."""
        # Create deeply nested brackets
        deep_nested = "(" * 500 + ")" * 500
        start_time = time.time()
        result = is_balanced(deep_nested)
        elapsed = time.time() - start_time

        self.assertTrue(result)
        self.assertLess(elapsed, 0.1, "Deep nesting performance test failed")

    # =====================================================
    # DIAGNOSTIC FUNCTION TESTS
    # =====================================================

    def test_get_balance_info_valid_cases(self):
        """Test get_balance_info function with valid cases."""
        info = get_balance_info("()")
        self.assertTrue(info['is_balanced'])
        self.assertEqual(info['unmatched_opening'], [])
        self.assertEqual(info['error_position'], -1)
        self.assertEqual(info['error_type'], '')

        info = get_balance_info("")
        self.assertTrue(info['is_balanced'])

    def test_get_balance_info_invalid_cases(self):
        """Test get_balance_info function with invalid cases."""
        # Unmatched closing bracket
        info = get_balance_info(")")
        self.assertFalse(info['is_balanced'])
        self.assertEqual(info['error_position'], 0)
        self.assertIn('Unmatched closing bracket', info['error_type'])

        # Type mismatch
        info = get_balance_info("(]")
        self.assertFalse(info['is_balanced'])
        self.assertEqual(info['error_position'], 1)
        self.assertIn('Bracket type mismatch', info['error_type'])

        # Unmatched opening brackets
        info = get_balance_info("((")
        self.assertFalse(info['is_balanced'])
        self.assertEqual(len(info['unmatched_opening']), 2)

    def test_get_balance_info_input_validation(self):
        """Test get_balance_info input validation."""
        with self.assertRaises(TypeError):
            get_balance_info(None)

        with self.assertRaises(TypeError):
            get_balance_info(123)


class TestSpecificationCompliance(unittest.TestCase):
    """Tests to verify compliance with specification requirements."""

    def test_algorithm_time_complexity(self):
        """Verify O(n) time complexity by measuring scaling."""
        sizes = [100, 200, 400, 800]
        times = []

        for size in sizes:
            test_string = "(" * (size // 2) + ")" * (size // 2)
            start_time = time.time()
            is_balanced(test_string)
            elapsed = time.time() - start_time
            times.append(elapsed)

        # Verify that time doesn't scale worse than linearly
        # (allowing for some measurement noise)
        for i in range(1, len(times)):
            ratio = times[i] / times[i-1]
            size_ratio = sizes[i] / sizes[i-1]
            self.assertLess(ratio, size_ratio * 3,
                          f"Time complexity appears worse than linear: {ratio} vs {size_ratio}")

    def test_all_specification_examples(self):
        """Test all examples mentioned in the specification."""
        # Valid cases from spec
        valid_cases = [
            "",
            "()",
            "()[]{}",
            "([{}])",
            "({[()]}[])",
            "(((())))",
            "hello(world)",
            "a[b{c}d]e",
            "hello world"
        ]

        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(is_balanced(case), f"Expected '{case}' to be balanced")

        # Invalid cases from spec
        invalid_cases = [
            "(",
            ")",
            "(((",
            ")))",
            ")(",
            "([)]",
            "(]",
            "([",
            "hello(world"
        ]

        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(is_balanced(case), f"Expected '{case}' to be unbalanced")


def run_comprehensive_tests():
    """Run all tests and provide a summary report."""
    print("Running Comprehensive Balanced Parentheses Tests")
    print("=" * 50)

    # Create test suite
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTest(unittest.makeSuite(TestBalancedParentheses))
    suite.addTest(unittest.makeSuite(TestSpecificationCompliance))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=None)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")

    return success


if __name__ == "__main__":
    # Run comprehensive tests
    success = run_comprehensive_tests()

    # Run basic functionality demo
    print("\n" + "=" * 50)
    print("BASIC FUNCTIONALITY DEMO")
    print("=" * 50)

    demo_cases = [
        ("", "Empty string"),
        ("()", "Simple parentheses"),
        ("([{}])", "Complex nesting"),
        ("([)]", "Invalid interleaving"),
        ("(()", "Unmatched opening"),
        (")))", "Unmatched closing"),
        ("hello(world)", "Text with brackets")
    ]

    for test_string, description in demo_cases:
        result = is_balanced(test_string)
        print(f"{description:20} '{test_string}' -> {result}")

    exit(0 if success else 1)