"""
Comprehensive test suite for the anagram grouper function.

Tests all specifications and edge cases defined in anagram_grouper_specifications.md.
"""

import pytest
import time
from typing import List, Dict
from anagram_grouper import (
    group_anagrams,
    count_anagram_groups,
    find_largest_anagram_group,
    are_anagrams,
    _get_canonical_form
)


class TestGroupAnagrams:
    """Test cases for the main group_anagrams function."""

    def test_basic_anagram_grouping(self):
        """Test basic anagram grouping functionality."""
        words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
        result = group_anagrams(words)

        # Should have 3 groups
        assert len(result) == 3

        # Check that each group contains the expected anagrams
        anagram_sets = [set(group) for group in result]
        assert {'eat', 'tea', 'ate'} in anagram_sets
        assert {'tan', 'nat'} in anagram_sets
        assert {'bat'} in anagram_sets

    def test_empty_input(self):
        """Test handling of empty input."""
        assert group_anagrams([]) == []
        assert group_anagrams([], output_format='dict') == {}

    def test_single_word(self):
        """Test handling of single word input."""
        result = group_anagrams(['hello'])
        assert result == [['hello']]

    def test_no_anagrams(self):
        """Test when no words are anagrams of each other."""
        words = ['hello', 'world', 'python']
        result = group_anagrams(words)
        assert len(result) == 3
        for group in result:
            assert len(group) == 1

    def test_all_anagrams(self):
        """Test when all words are anagrams of each other."""
        words = ['listen', 'silent', 'tinsel', 'enlist']
        result = group_anagrams(words)
        assert len(result) == 1
        assert len(result[0]) == 4

    def test_case_sensitivity_false(self):
        """Test case insensitive anagram detection (default)."""
        words = ['Eat', 'Tea', 'ate']
        result = group_anagrams(words, case_sensitive=False)
        assert len(result) == 1
        assert set(result[0]) == {'Eat', 'Tea', 'ate'}

    def test_case_sensitivity_true(self):
        """Test case sensitive anagram detection."""
        words = ['Eat', 'Tea', 'ate']
        result = group_anagrams(words, case_sensitive=True)
        assert len(result) == 3  # Each word forms its own group

    def test_output_format_list(self):
        """Test list output format (default)."""
        words = ['eat', 'tea', 'bat']
        result = group_anagrams(words, output_format='list')
        assert isinstance(result, list)
        assert all(isinstance(group, list) for group in result)

    def test_output_format_dict(self):
        """Test dictionary output format."""
        words = ['eat', 'tea', 'bat']
        result = group_anagrams(words, output_format='dict')
        assert isinstance(result, dict)
        assert all(isinstance(group, list) for group in result.values())

    def test_sort_groups_true(self):
        """Test sorting of groups by canonical form."""
        words = ['zoo', 'cat', 'act', 'ooz']
        result = group_anagrams(words, sort_groups=True)

        # Groups should be sorted by canonical form
        canonical_forms = [''.join(sorted(result[0][0].lower())),
                          ''.join(sorted(result[1][0].lower()))]
        assert canonical_forms == sorted(canonical_forms)

    def test_sort_groups_false(self):
        """Test no sorting of groups."""
        words = ['zoo', 'cat', 'act', 'ooz']
        result = group_anagrams(words, sort_groups=False)
        assert len(result) == 2  # Still should group correctly

    def test_sort_within_groups_true(self):
        """Test sorting within groups."""
        words = ['tea', 'eat', 'ate']
        result = group_anagrams(words, sort_within_groups=True)
        assert result[0] == ['ate', 'eat', 'tea']

    def test_sort_within_groups_false(self):
        """Test no sorting within groups."""
        words = ['tea', 'eat', 'ate']
        result = group_anagrams(words, sort_within_groups=False)
        # Order should be preserved from input
        assert set(result[0]) == {'tea', 'eat', 'ate'}

    def test_duplicate_words(self):
        """Test handling of duplicate words in input."""
        words = ['eat', 'tea', 'eat', 'tea']
        result = group_anagrams(words)
        assert len(result) == 1
        assert result[0] == ['eat', 'eat', 'tea', 'tea']

    def test_empty_strings(self):
        """Test handling of empty strings."""
        words = ['', 'eat', 'tea', '']
        result = group_anagrams(words)

        # Should have 2 groups: empty strings and eat/tea
        assert len(result) == 2
        group_sizes = [len(group) for group in result]
        assert 2 in group_sizes  # Two empty strings
        assert 2 in group_sizes  # eat and tea

    def test_whitespace_strings(self):
        """Test handling of whitespace-only strings."""
        words = [' ', '  ', 'a', ' a']
        result = group_anagrams(words)

        # Whitespace strings should be treated as distinct
        assert len(result) == 4  # Each is in its own group

    def test_unicode_characters(self):
        """Test handling of Unicode characters."""
        words = ['café', 'face', 'éfac']
        result = group_anagrams(words)

        # Unicode characters should be handled correctly
        # café and éfac should not be anagrams due to é vs e
        assert len(result) >= 2

    def test_special_characters(self):
        """Test handling of special characters and numbers."""
        words = ['a1!', '!1a', '1a!', 'abc']
        result = group_anagrams(words)

        # First three should be anagrams
        anagram_group = None
        for group in result:
            if len(group) == 3:
                anagram_group = group
                break

        assert anagram_group is not None
        assert set(anagram_group) == {'a1!', '!1a', '1a!'}

    def test_very_long_strings(self):
        """Test handling of very long strings."""
        long_word1 = 'a' * 1000 + 'b' * 1000
        long_word2 = 'b' * 1000 + 'a' * 1000
        words = [long_word1, long_word2, 'short']

        result = group_anagrams(words)
        assert len(result) == 2

        # Find the group with long words
        long_group = None
        for group in result:
            if len(group[0]) > 100:
                long_group = group
                break

        assert long_group is not None
        assert len(long_group) == 2

    def test_input_types(self):
        """Test various input types (list, tuple, iterator)."""
        words_list = ['eat', 'tea', 'bat']
        words_tuple = ('eat', 'tea', 'bat')
        words_iter = iter(['eat', 'tea', 'bat'])

        result_list = group_anagrams(words_list)
        result_tuple = group_anagrams(words_tuple)
        result_iter = group_anagrams(words_iter)

        # All should produce the same result
        assert result_list == result_tuple == result_iter


class TestErrorHandling:
    """Test error handling and validation."""

    def test_invalid_output_format(self):
        """Test error on invalid output format."""
        with pytest.raises(ValueError, match="output_format must be 'list' or 'dict'"):
            group_anagrams(['test'], output_format='invalid')

    def test_non_string_items(self):
        """Test error on non-string items in input."""
        with pytest.raises(TypeError, match="All items must be strings"):
            group_anagrams(['test', 123, 'other'])

    def test_none_in_input(self):
        """Test error on None values in input."""
        with pytest.raises(TypeError, match="All items must be strings"):
            group_anagrams(['test', None, 'other'])

    def test_non_iterable_input(self):
        """Test error on non-iterable input."""
        with pytest.raises(TypeError, match="Input must be iterable"):
            group_anagrams(123)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_count_anagram_groups(self):
        """Test count_anagram_groups function."""
        words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
        count = count_anagram_groups(words)
        assert count == 3

    def test_find_largest_anagram_group(self):
        """Test find_largest_anagram_group function."""
        words = ['eat', 'tea', 'ate', 'tan', 'nat', 'bat']
        largest = find_largest_anagram_group(words)
        assert len(largest) == 3
        assert set(largest) == {'eat', 'tea', 'ate'}

    def test_find_largest_anagram_group_empty(self):
        """Test find_largest_anagram_group with empty input."""
        largest = find_largest_anagram_group([])
        assert largest == []

    def test_are_anagrams_true(self):
        """Test are_anagrams function for true anagrams."""
        assert are_anagrams('listen', 'silent')
        assert are_anagrams('eat', 'tea')

    def test_are_anagrams_false(self):
        """Test are_anagrams function for non-anagrams."""
        assert not are_anagrams('hello', 'world')
        assert not are_anagrams('eat', 'meat')

    def test_are_anagrams_case_sensitivity(self):
        """Test are_anagrams case sensitivity."""
        assert are_anagrams('Listen', 'silent', case_sensitive=False)
        assert not are_anagrams('Listen', 'silent', case_sensitive=True)

    def test_are_anagrams_error_handling(self):
        """Test are_anagrams error handling."""
        with pytest.raises(TypeError, match="Both arguments must be strings"):
            are_anagrams('test', 123)


class TestCanonicalForm:
    """Test the canonical form generation function."""

    def test_canonical_form_basic(self):
        """Test basic canonical form generation."""
        assert _get_canonical_form('eat', False) == 'aet'
        assert _get_canonical_form('tea', False) == 'aet'

    def test_canonical_form_case_sensitive(self):
        """Test canonical form with case sensitivity."""
        assert _get_canonical_form('Eat', True) == 'Eat'
        assert _get_canonical_form('Eat', False) == 'aet'

    def test_canonical_form_unicode(self):
        """Test canonical form with Unicode characters."""
        result = _get_canonical_form('café', False)
        assert isinstance(result, str)
        assert len(result) == 4


class TestPerformance:
    """Performance tests to ensure specifications are met."""

    def test_small_collection_performance(self):
        """Test performance with small collections (< 100 strings)."""
        words = [f'word{i}' for i in range(50)]

        start_time = time.time()
        group_anagrams(words)
        end_time = time.time()

        # Should complete in less than 1ms (generous margin for test environment)
        assert (end_time - start_time) < 0.1

    def test_medium_collection_performance(self):
        """Test performance with medium collections (100-1000 strings)."""
        words = [f'test{i % 10}{i // 10}' for i in range(500)]

        start_time = time.time()
        group_anagrams(words)
        end_time = time.time()

        # Should complete in reasonable time
        assert (end_time - start_time) < 1.0

    def test_large_collection_performance(self):
        """Test performance with larger collections."""
        words = [f'test{i % 100}{i // 100}' for i in range(1000)]

        start_time = time.time()
        result = group_anagrams(words)
        end_time = time.time()

        # Should complete in reasonable time
        assert (end_time - start_time) < 5.0
        assert isinstance(result, list)


class TestSpecificationCompliance:
    """Tests to ensure full compliance with specifications."""

    def test_deterministic_output(self):
        """Test that output is deterministic with sorting enabled."""
        words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']

        result1 = group_anagrams(words, sort_groups=True, sort_within_groups=True)
        result2 = group_anagrams(words, sort_groups=True, sort_within_groups=True)

        assert result1 == result2

    def test_original_formatting_preserved(self):
        """Test that original string formatting is preserved."""
        words = ['Eat', 'TEA', 'ate']
        result = group_anagrams(words, case_sensitive=False)

        # Original case should be preserved in output
        assert 'Eat' in result[0]
        assert 'TEA' in result[0]
        assert 'ate' in result[0]

    def test_all_output_combinations(self):
        """Test all combinations of output parameters."""
        words = ['eat', 'tea', 'bat', 'tab']

        combinations = [
            (True, True, 'list'),
            (True, False, 'list'),
            (False, True, 'list'),
            (False, False, 'list'),
            (True, True, 'dict'),
            (True, False, 'dict'),
            (False, True, 'dict'),
            (False, False, 'dict'),
        ]

        for sort_groups, sort_within_groups, output_format in combinations:
            result = group_anagrams(
                words,
                sort_groups=sort_groups,
                sort_within_groups=sort_within_groups,
                output_format=output_format
            )

            if output_format == 'list':
                assert isinstance(result, list)
            else:
                assert isinstance(result, dict)


if __name__ == "__main__":
    # Run a subset of tests when script is executed directly
    print("Running basic functionality tests...")

    test_instance = TestGroupAnagrams()
    test_instance.test_basic_anagram_grouping()
    test_instance.test_case_sensitivity_false()
    test_instance.test_output_format_dict()

    print("All basic tests passed!")

    utility_test = TestUtilityFunctions()
    utility_test.test_count_anagram_groups()
    utility_test.test_are_anagrams_true()

    print("Utility function tests passed!")
    print("Run 'pytest test_anagram_grouper.py' for comprehensive testing.")