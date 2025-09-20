#!/usr/bin/env python3
"""
Simple tests for the anagram grouper functionality.

Run this file to verify that all functions work correctly.
"""

import sys
from anagram_grouper import (
    group_anagrams,
    group_anagrams_with_stats,
    find_anagrams_of_word,
    is_anagram,
    normalize_word,
    validate_input
)


def test_normalize_word():
    """Test the normalize_word function."""
    print("Testing normalize_word...")

    assert normalize_word("listen") == "eilnst"
    assert normalize_word("LISTEN") == "eilnst"
    assert normalize_word("  Listen  ") == "eilnst"
    assert normalize_word("abc") == "abc"
    assert normalize_word("") == ""

    # Test error handling
    try:
        normalize_word(123)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass

    print("✓ normalize_word tests passed")


def test_validate_input():
    """Test the validate_input function."""
    print("Testing validate_input...")

    assert validate_input(['a', 'b', 'c']) == ['a', 'b', 'c']
    assert validate_input(['  a  ', '', 'b', '   ']) == ['a', 'b']
    assert validate_input([]) == []

    # Test error handling
    try:
        validate_input("not a list")
        assert False, "Should have raised TypeError"
    except TypeError:
        pass

    try:
        validate_input(['a', 123, 'b'])
        assert False, "Should have raised TypeError"
    except TypeError:
        pass

    print("✓ validate_input tests passed")


def test_group_anagrams():
    """Test the main group_anagrams function."""
    print("Testing group_anagrams...")

    # Basic test
    result = group_anagrams(['eat', 'tea', 'bat', 'ate'])
    expected = [['ate', 'eat', 'tea'], ['bat']]
    assert result == expected, f"Expected {expected}, got {result}"

    # Empty list
    assert group_anagrams([]) == []

    # Single word
    assert group_anagrams(['hello']) == [['hello']]

    # No anagrams
    assert group_anagrams(['a', 'b', 'c']) == [['a'], ['b'], ['c']]

    # Case insensitive
    result = group_anagrams(['Listen', 'Silent'])
    assert len(result) == 1 and len(result[0]) == 2

    # Duplicates
    result = group_anagrams(['eat', 'tea', 'eat'])
    expected = [['eat', 'eat', 'tea']]
    assert result == expected

    print("✓ group_anagrams tests passed")


def test_group_anagrams_with_stats():
    """Test the group_anagrams_with_stats function."""
    print("Testing group_anagrams_with_stats...")

    result = group_anagrams_with_stats(['eat', 'tea', 'bat'])

    assert 'groups' in result
    assert 'stats' in result
    assert result['stats']['total_words'] == 3
    assert result['stats']['total_groups'] == 2
    assert result['stats']['largest_group_size'] == 2
    assert result['stats']['single_word_groups'] == 1
    assert result['stats']['multi_word_groups'] == 1

    print("✓ group_anagrams_with_stats tests passed")


def test_find_anagrams_of_word():
    """Test the find_anagrams_of_word function."""
    print("Testing find_anagrams_of_word...")

    result = find_anagrams_of_word('eat', ['tea', 'bat', 'ate', 'hello'])
    expected = ['ate', 'tea']
    assert result == expected, f"Expected {expected}, got {result}"

    # No anagrams
    result = find_anagrams_of_word('hello', ['world', 'test'])
    assert result == []

    # Word not included in its own anagrams
    result = find_anagrams_of_word('eat', ['eat', 'tea', 'ate'])
    expected = ['ate', 'tea']
    assert result == expected

    print("✓ find_anagrams_of_word tests passed")


def test_is_anagram():
    """Test the is_anagram function."""
    print("Testing is_anagram...")

    assert is_anagram('listen', 'silent') == True
    assert is_anagram('hello', 'world') == False
    assert is_anagram('eat', 'tea') == True

    # Same word should return False
    assert is_anagram('hello', 'hello') == False
    assert is_anagram('Hello', 'hello') == False

    # Case insensitive
    assert is_anagram('Listen', 'Silent') == True

    # Invalid input
    assert is_anagram(123, 'test') == False
    assert is_anagram('test', None) == False

    print("✓ is_anagram tests passed")


def run_all_tests():
    """Run all tests."""
    print("Running anagram grouper tests...\n")

    try:
        test_normalize_word()
        test_validate_input()
        test_group_anagrams()
        test_group_anagrams_with_stats()
        test_find_anagrams_of_word()
        test_is_anagram()

        print("\n🎉 All tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)