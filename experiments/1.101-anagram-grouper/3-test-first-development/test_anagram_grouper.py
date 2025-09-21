import unittest
from typing import List
from anagram_grouper import group_anagrams


class TestAnagramGrouper(unittest.TestCase):
    """Test suite for anagram grouper function following TDD principles."""

    def test_empty_list_returns_empty_list(self):
        """Test that empty input returns empty output."""
        result = group_anagrams([])
        self.assertEqual(result, [])

    def test_single_word_returns_single_group(self):
        """Test that single word returns a list with one group containing that word."""
        result = group_anagrams(["hello"])
        self.assertEqual(result, [["hello"]])

    def test_basic_anagram_grouping(self):
        """Test that basic anagrams are grouped together."""
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        # Sort both result and expected for comparison since order within groups may vary
        result_sorted = [sorted(group) for group in sorted(result, key=lambda x: sorted(x)[0])]
        expected_sorted = [sorted(group) for group in sorted([["eat", "tea", "ate"], ["tan", "nat"], ["bat"]], key=lambda x: sorted(x)[0])]
        self.assertEqual(result_sorted, expected_sorted)

    def test_case_insensitive_grouping(self):
        """Test that anagrams are grouped case-insensitively but preserve original case."""
        result = group_anagrams(["Eat", "tea", "Tea", "ATE"])
        # All should be grouped together since they're anagrams (case-insensitive)
        self.assertEqual(len(result), 1)
        self.assertEqual(sorted(result[0]), ["ATE", "Eat", "Tea", "tea"])

    def test_input_validation_non_list(self):
        """Test that non-list input raises TypeError."""
        with self.assertRaises(TypeError):
            group_anagrams("not a list")

    def test_input_validation_non_string_elements(self):
        """Test that non-string elements raise TypeError."""
        with self.assertRaises(TypeError):
            group_anagrams(["hello", 123, "world"])

    def test_input_validation_none(self):
        """Test that None input raises TypeError."""
        with self.assertRaises(TypeError):
            group_anagrams(None)

    def test_empty_strings(self):
        """Test that empty strings are grouped together."""
        result = group_anagrams(["", "", "hello", ""])
        # Sort for consistent comparison
        result_sorted = sorted([sorted(group) for group in result], key=lambda x: x[0])
        expected_sorted = sorted([sorted(group) for group in [["", "", ""], ["hello"]]], key=lambda x: x[0])
        self.assertEqual(result_sorted, expected_sorted)

    def test_duplicate_words(self):
        """Test that duplicate words are grouped together."""
        result = group_anagrams(["hello", "hello", "world", "hello"])
        # Sort for consistent comparison
        result_sorted = sorted([sorted(group) for group in result], key=lambda x: x[0])
        expected_sorted = sorted([sorted(group) for group in [["hello", "hello", "hello"], ["world"]]], key=lambda x: x[0])
        self.assertEqual(result_sorted, expected_sorted)

    def test_single_characters(self):
        """Test that single characters work correctly."""
        result = group_anagrams(["a", "b", "a", "c", "b"])
        # Sort for consistent comparison
        result_sorted = sorted([sorted(group) for group in result], key=lambda x: x[0])
        expected_sorted = sorted([sorted(group) for group in [["a", "a"], ["b", "b"], ["c"]]], key=lambda x: x[0])
        self.assertEqual(result_sorted, expected_sorted)

    def test_words_with_spaces_and_punctuation(self):
        """Test that spaces and punctuation are handled correctly."""
        result = group_anagrams(["a!b", "b!a", "a b", "b a"])
        # Should group punctuation-based and space-based separately
        self.assertEqual(len(result), 2)
        # Find groups and verify content
        groups = sorted([sorted(group) for group in result], key=lambda x: x[0])
        self.assertIn(["a b", "b a"], groups)
        self.assertIn(["a!b", "b!a"], groups)


if __name__ == '__main__':
    unittest.main()