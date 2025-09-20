"""
Test-Driven Development for Anagram Grouper Function
Following comprehensive test validation process
"""

import unittest
from typing import List
from anagram_grouper import group_anagrams


class TestAnagramGrouper(unittest.TestCase):
    """Comprehensive test suite for anagram grouper function"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    # =================================================================
    # FEATURE 1: Basic Empty Input Handling
    # =================================================================

    def test_empty_list_returns_empty_list(self):
        """
        BEHAVIOR: Empty input should return empty output
        WHY: Function should handle empty edge case gracefully
        FAILURE SCENARIO: Function returns None, raises exception, or returns non-empty list
        """
        result = group_anagrams([])
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_empty_list_returns_correct_type(self):
        """
        BEHAVIOR: Return type must be list even for empty input
        WHY: Consistent return type contract
        FAILURE SCENARIO: Function returns None, dict, or other type
        """
        result = group_anagrams([])
        self.assertIsInstance(result, list)

    # =================================================================
    # FEATURE 2: Single Word Input Handling
    # =================================================================

    def test_single_word_returns_single_group(self):
        """
        BEHAVIOR: Single word input should return list with one group containing that word
        WHY: Maintains consistent list-of-lists structure even for single elements
        FAILURE SCENARIO: Returns flat list, empty list, or multiple groups
        """
        result = group_anagrams(["hello"])
        expected = [["hello"]]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)

    def test_single_word_preserves_original_formatting(self):
        """
        BEHAVIOR: Original word formatting should be preserved in output
        WHY: Function should not modify input strings
        FAILURE SCENARIO: Changes case, strips whitespace, or modifies content
        """
        test_cases = [
            ["Hello"],
            ["  spaced  "],
            ["CAPS"],
            [""],
            ["123"],
            ["special!@#"]
        ]

        for words in test_cases:
            with self.subTest(words=words):
                result = group_anagrams(words)
                self.assertEqual(result, [words])
                self.assertEqual(result[0][0], words[0])  # Original preserved

    def test_single_word_return_structure(self):
        """
        BEHAVIOR: Return structure must be list of lists, not flat list
        WHY: Consistent API contract for all cases
        FAILURE SCENARIO: Returns ["hello"] instead of [["hello"]]
        """
        result = group_anagrams(["test"])
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertEqual(len(result), 1)

    # =================================================================
    # FEATURE 3: Basic Anagram Detection and Grouping
    # =================================================================

    def test_two_anagrams_grouped_together(self):
        """
        BEHAVIOR: Two words that are anagrams should be grouped in same list
        WHY: Core anagram detection functionality
        FAILURE SCENARIO: Returns separate groups, wrong grouping, or flat list
        """
        result = group_anagrams(["listen", "silent"])
        expected = [["listen", "silent"]]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)  # Only one group
        self.assertEqual(len(result[0]), 2)  # Two words in the group

    def test_anagram_detection_case_insensitive(self):
        """
        BEHAVIOR: Anagram detection should be case-insensitive
        WHY: "Listen" and "silent" are anagrams despite different case
        FAILURE SCENARIO: Creates separate groups for different cases
        """
        result = group_anagrams(["Listen", "silent"])
        self.assertEqual(len(result), 1)  # Should be grouped together
        self.assertEqual(len(result[0]), 2)  # Two words in one group

    def test_anagram_preserves_original_case(self):
        """
        BEHAVIOR: Original case should be preserved in output even with case-insensitive detection
        WHY: Function should not modify input strings
        FAILURE SCENARIO: Changes case of original strings
        """
        result = group_anagrams(["Listen", "silent"])
        # Should contain original strings with original case
        self.assertIn("Listen", result[0])
        self.assertIn("silent", result[0])

    def test_non_anagrams_separate_groups(self):
        """
        BEHAVIOR: Words that are not anagrams should be in separate groups
        WHY: Only actual anagrams should be grouped together
        FAILURE SCENARIO: Groups non-anagrams together
        """
        result = group_anagrams(["cat", "dog"])
        self.assertEqual(len(result), 2)  # Two separate groups
        self.assertEqual(len(result[0]), 1)  # Each group has one word
        self.assertEqual(len(result[1]), 1)

    def test_mixed_anagrams_and_non_anagrams(self):
        """
        BEHAVIOR: Mix of anagrams and non-anagrams should be correctly grouped
        WHY: Real-world scenario with complex grouping
        FAILURE SCENARIO: Incorrect grouping, missing words, wrong structure
        """
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])

        # Should have 3 groups: [eat,tea,ate], [tan,nat], [bat]
        self.assertEqual(len(result), 3)

        # Find groups by checking one representative from each expected group
        eat_group = None
        tan_group = None
        bat_group = None

        for group in result:
            if "eat" in group:
                eat_group = group
            elif "tan" in group:
                tan_group = group
            elif "bat" in group:
                bat_group = group

        # Verify each group exists and has correct members
        self.assertIsNotNone(eat_group)
        self.assertIsNotNone(tan_group)
        self.assertIsNotNone(bat_group)

        self.assertEqual(set(eat_group), {"eat", "tea", "ate"})
        self.assertEqual(set(tan_group), {"tan", "nat"})
        self.assertEqual(set(bat_group), {"bat"})

    def test_anagram_order_preservation(self):
        """
        BEHAVIOR: Order of first occurrence should determine group position
        WHY: Predictable output ordering
        FAILURE SCENARIO: Inconsistent or random ordering
        """
        result = group_anagrams(["bat", "eat", "tea"])
        # First group should be the one containing "bat" (first non-anagram)
        # Second group should contain "eat" and "tea" (anagrams appearing later)

        bat_group_index = None
        eat_group_index = None

        for i, group in enumerate(result):
            if "bat" in group:
                bat_group_index = i
            elif "eat" in group:
                eat_group_index = i

        self.assertIsNotNone(bat_group_index)
        self.assertIsNotNone(eat_group_index)
        self.assertLess(bat_group_index, eat_group_index)  # bat group comes first

    # =================================================================
    # FEATURE 4: Comprehensive Edge Cases and Special Characters
    # =================================================================

    def test_empty_strings_are_anagrams(self):
        """
        BEHAVIOR: Empty strings should be grouped together as anagrams
        WHY: Empty strings are technically anagrams of each other
        FAILURE SCENARIO: Empty strings in separate groups
        """
        result = group_anagrams(["", "", "a"])

        # Find the group containing empty strings
        empty_group = None
        a_group = None

        for group in result:
            if "" in group:
                empty_group = group
            elif "a" in group:
                a_group = group

        self.assertIsNotNone(empty_group)
        self.assertIsNotNone(a_group)
        self.assertEqual(empty_group.count(""), 2)  # Two empty strings together
        self.assertEqual(len(a_group), 1)  # "a" in its own group

    def test_whitespace_and_special_characters(self):
        """
        BEHAVIOR: Whitespace and special characters should be considered in anagram detection
        WHY: They are part of the string content
        FAILURE SCENARIO: Ignores special characters or whitespace
        """
        result = group_anagrams(["a!b", "b!a", "ab", "ba"])

        # Should have 2 groups: ["a!b", "b!a"] and ["ab", "ba"]
        self.assertEqual(len(result), 2)

        special_group = None
        regular_group = None

        for group in result:
            if "a!b" in group:
                special_group = group
            elif "ab" in group:
                regular_group = group

        self.assertIsNotNone(special_group)
        self.assertIsNotNone(regular_group)
        self.assertEqual(set(special_group), {"a!b", "b!a"})
        self.assertEqual(set(regular_group), {"ab", "ba"})

    def test_numbers_as_strings(self):
        """
        BEHAVIOR: Numeric strings should be treated like any other strings
        WHY: Function should work with any string content
        FAILURE SCENARIO: Special handling breaks numeric strings
        """
        result = group_anagrams(["123", "321", "132", "456"])

        self.assertEqual(len(result), 2)  # Two groups

        # Find groups
        group_123 = None
        group_456 = None

        for group in result:
            if "123" in group:
                group_123 = group
            elif "456" in group:
                group_456 = group

        self.assertIsNotNone(group_123)
        self.assertIsNotNone(group_456)
        self.assertEqual(set(group_123), {"123", "321", "132"})
        self.assertEqual(set(group_456), {"456"})

    def test_unicode_characters(self):
        """
        BEHAVIOR: Unicode characters should be handled correctly
        WHY: Modern applications need Unicode support
        FAILURE SCENARIO: Unicode breaks sorting or comparison
        """
        result = group_anagrams(["café", "éfac", "test"])

        self.assertEqual(len(result), 2)

        unicode_group = None
        test_group = None

        for group in result:
            if "café" in group:
                unicode_group = group
            elif "test" in group:
                test_group = group

        self.assertIsNotNone(unicode_group)
        self.assertIsNotNone(test_group)
        self.assertEqual(set(unicode_group), {"café", "éfac"})
        self.assertEqual(set(test_group), {"test"})

    def test_very_long_strings(self):
        """
        BEHAVIOR: Function should handle long strings efficiently
        WHY: Performance requirement for large inputs
        FAILURE SCENARIO: Timeout or memory issues with long strings
        """
        long_string1 = "a" * 1000 + "b" * 1000
        long_string2 = "b" * 1000 + "a" * 1000
        short_string = "c"

        result = group_anagrams([long_string1, long_string2, short_string])

        self.assertEqual(len(result), 2)

        long_group = None
        short_group = None

        for group in result:
            if long_string1 in group:
                long_group = group
            elif short_string in group:
                short_group = group

        self.assertIsNotNone(long_group)
        self.assertIsNotNone(short_group)
        self.assertEqual(set(long_group), {long_string1, long_string2})
        self.assertEqual(set(short_group), {short_string})

    def test_duplicate_words(self):
        """
        BEHAVIOR: Duplicate words should all be included in same group
        WHY: All occurrences should be preserved
        FAILURE SCENARIO: Duplicates lost or in wrong groups
        """
        result = group_anagrams(["abc", "bca", "abc", "xyz", "xyz"])

        self.assertEqual(len(result), 2)

        abc_group = None
        xyz_group = None

        for group in result:
            if "abc" in group:
                abc_group = group
            elif "xyz" in group:
                xyz_group = group

        self.assertIsNotNone(abc_group)
        self.assertIsNotNone(xyz_group)
        self.assertEqual(abc_group.count("abc"), 2)  # Two "abc" instances
        self.assertEqual(abc_group.count("bca"), 1)  # One "bca" instance
        self.assertEqual(xyz_group.count("xyz"), 2)  # Two "xyz" instances

    # =================================================================
    # FEATURE 5: Input Validation and Error Handling
    # =================================================================

    def test_non_list_input_raises_type_error(self):
        """
        BEHAVIOR: Non-list input should raise TypeError
        WHY: Function contract specifies list input only
        FAILURE SCENARIO: Accepts invalid input types
        """
        invalid_inputs = [
            "string",
            123,
            None,
            {"a": "b"},
            ("a", "b"),  # tuple
            {"a", "b"},  # set
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError) as context:
                    group_anagrams(invalid_input)

                # Ensure error message is helpful
                error_msg = str(context.exception).lower()
                self.assertIn("list", error_msg)

    def test_non_string_elements_raise_type_error(self):
        """
        BEHAVIOR: List with non-string elements should raise TypeError
        WHY: Function only processes strings
        FAILURE SCENARIO: Silently converts or ignores non-strings
        """
        invalid_lists = [
            ["hello", 123],
            ["hello", ["nested"]],
            [123, 456],
            ["hello", {"key": "value"}],
        ]

        for invalid_list in invalid_lists:
            with self.subTest(input=invalid_list):
                with self.assertRaises(TypeError) as context:
                    group_anagrams(invalid_list)

                error_msg = str(context.exception).lower()
                self.assertIn("string", error_msg)

        # Test None separately since it raises ValueError
        with self.assertRaises(ValueError):
            group_anagrams(["hello", None])

    def test_none_elements_raise_value_error(self):
        """
        BEHAVIOR: None elements should raise ValueError specifically
        WHY: None is a special case that needs specific handling
        FAILURE SCENARIO: Treats None as valid input
        """
        with self.assertRaises(ValueError) as context:
            group_anagrams(["hello", None, "world"])

        error_msg = str(context.exception).lower()
        self.assertIn("none", error_msg)

    def test_mixed_valid_invalid_elements(self):
        """
        BEHAVIOR: Mix of valid and invalid should still raise error
        WHY: All elements must be valid for processing
        FAILURE SCENARIO: Processes valid elements, ignores invalid
        """
        with self.assertRaises(TypeError):
            group_anagrams(["valid", "also_valid", 123])

    def test_empty_list_does_not_raise_error(self):
        """
        BEHAVIOR: Empty list should not raise any errors
        WHY: Empty list is valid input according to specifications
        FAILURE SCENARIO: Raises error for empty list
        """
        try:
            result = group_anagrams([])
            self.assertEqual(result, [])
        except Exception as e:
            self.fail(f"Empty list should not raise error, but got: {e}")

    def test_error_handling_preserves_original_list(self):
        """
        BEHAVIOR: Error should not modify the original input list
        WHY: Function should not have side effects on input
        FAILURE SCENARIO: Input list is modified during validation
        """
        original_list = ["hello", 123, "world"]
        original_copy = original_list.copy()

        with self.assertRaises(TypeError):
            group_anagrams(original_list)

        # Original list should be unchanged
        self.assertEqual(original_list, original_copy)


if __name__ == '__main__':
    unittest.main()