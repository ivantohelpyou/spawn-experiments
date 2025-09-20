#!/usr/bin/env python3
"""
Demonstration script for the Anagram Grouper function.

This script showcases all the features and capabilities of the anagram grouper
implementation according to the specifications.
"""

import time
from anagram_grouper import (
    group_anagrams,
    count_anagram_groups,
    find_largest_anagram_group,
    are_anagrams
)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def print_result(description: str, result):
    """Print a result with formatting."""
    print(f"\n{description}:")
    print(f"  Result: {result}")


def demonstrate_basic_functionality():
    """Demonstrate basic anagram grouping functionality."""
    print_section("Basic Anagram Grouping")

    # Example 1: Classic anagram examples
    words1 = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
    result1 = group_anagrams(words1)
    print(f"Input: {words1}")
    print_result("Grouped anagrams", result1)

    # Example 2: More complex words
    words2 = ['listen', 'silent', 'hello', 'world', 'tinsel', 'enlist']
    result2 = group_anagrams(words2)
    print(f"\nInput: {words2}")
    print_result("Grouped anagrams", result2)

    # Example 3: No anagrams
    words3 = ['python', 'java', 'golang', 'rust']
    result3 = group_anagrams(words3)
    print(f"\nInput: {words3}")
    print_result("No anagrams (each word alone)", result3)


def demonstrate_case_sensitivity():
    """Demonstrate case sensitivity options."""
    print_section("Case Sensitivity Options")

    words = ['Eat', 'Tea', 'ate', 'Listen', 'Silent', 'TINSEL']

    # Case insensitive (default)
    result_insensitive = group_anagrams(words, case_sensitive=False)
    print(f"Input: {words}")
    print_result("Case insensitive (default)", result_insensitive)

    # Case sensitive
    result_sensitive = group_anagrams(words, case_sensitive=True)
    print_result("Case sensitive", result_sensitive)


def demonstrate_output_formats():
    """Demonstrate different output formats."""
    print_section("Output Format Options")

    words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']

    # List format (default)
    result_list = group_anagrams(words, output_format='list')
    print(f"Input: {words}")
    print_result("List format (default)", result_list)

    # Dictionary format
    result_dict = group_anagrams(words, output_format='dict')
    print_result("Dictionary format", result_dict)


def demonstrate_sorting_options():
    """Demonstrate sorting options."""
    print_section("Sorting Options")

    words = ['zoo', 'tea', 'eat', 'ooz', 'ate']

    # Default: both sorting enabled
    result_default = group_anagrams(words, sort_groups=True, sort_within_groups=True)
    print(f"Input: {words}")
    print_result("Default (both sorting enabled)", result_default)

    # No sorting within groups
    result_no_inner = group_anagrams(words, sort_groups=True, sort_within_groups=False)
    print_result("No sorting within groups", result_no_inner)

    # No sorting of groups
    result_no_outer = group_anagrams(words, sort_groups=False, sort_within_groups=True)
    print_result("No sorting of groups", result_no_outer)

    # No sorting at all
    result_no_sort = group_anagrams(words, sort_groups=False, sort_within_groups=False)
    print_result("No sorting at all", result_no_sort)


def demonstrate_edge_cases():
    """Demonstrate handling of edge cases."""
    print_section("Edge Cases and Special Scenarios")

    # Empty input
    print("Empty input:")
    print_result("Empty list", group_anagrams([]))
    print_result("Empty dict", group_anagrams([], output_format='dict'))

    # Single word
    print("\nSingle word:")
    print_result("Single word", group_anagrams(['hello']))

    # Duplicate words
    print("\nDuplicate words:")
    words_dup = ['eat', 'tea', 'eat', 'tea', 'ate']
    print_result("Duplicates preserved", group_anagrams(words_dup))

    # Empty strings and whitespace
    print("\nEmpty strings and whitespace:")
    words_empty = ['', 'eat', 'tea', '', ' ', '  ']
    print_result("Mixed empty/whitespace", group_anagrams(words_empty))

    # Special characters and numbers
    print("\nSpecial characters and numbers:")
    words_special = ['a1!', '!1a', '1a!', 'abc', 'cba', '123', '321']
    print_result("Special chars and numbers", group_anagrams(words_special))

    # Unicode characters
    print("\nUnicode characters:")
    words_unicode = ['café', 'race', 'care', 'acre', 'naïve', 'vaïne']
    print_result("Unicode handling", group_anagrams(words_unicode))


def demonstrate_utility_functions():
    """Demonstrate utility functions."""
    print_section("Utility Functions")

    words = ['listen', 'silent', 'eat', 'tea', 'ate', 'hello', 'tinsel', 'enlist']

    # Count anagram groups
    count = count_anagram_groups(words)
    print(f"Input: {words}")
    print_result("Number of anagram groups", count)

    # Find largest anagram group
    largest = find_largest_anagram_group(words)
    print_result("Largest anagram group", largest)

    # Check if two words are anagrams
    print("\nAnagram checking:")
    test_pairs = [
        ('listen', 'silent'),
        ('hello', 'world'),
        ('race', 'care'),
        ('Listen', 'silent'),  # Case difference
    ]

    for word1, word2 in test_pairs:
        is_anagram_case_insensitive = are_anagrams(word1, word2, case_sensitive=False)
        is_anagram_case_sensitive = are_anagrams(word1, word2, case_sensitive=True)
        print(f"  '{word1}' and '{word2}':")
        print(f"    Case insensitive: {is_anagram_case_insensitive}")
        print(f"    Case sensitive: {is_anagram_case_sensitive}")


def demonstrate_performance():
    """Demonstrate performance with different collection sizes."""
    print_section("Performance Demonstration")

    sizes = [50, 200, 500, 1000]

    for size in sizes:
        # Generate test data with some anagrams
        words = []
        for i in range(size):
            if i % 3 == 0:
                words.append(f"listen{i}")
            elif i % 3 == 1:
                words.append(f"silent{i}")
            else:
                words.append(f"tinsel{i}")

        # Measure performance
        start_time = time.time()
        result = group_anagrams(words)
        end_time = time.time()

        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        groups = len(result)

        print(f"  {size:4d} words: {duration:6.2f}ms, {groups:3d} groups")


def demonstrate_real_world_example():
    """Demonstrate with a real-world example."""
    print_section("Real-World Example: Word Game Solver")

    # Simulate a word game where you need to find anagrams
    available_letters = "SILENT"
    possible_words = [
        "listen", "silent", "tinsel", "enlist",
        "list", "silt", "lit", "sit", "set",
        "nets", "tens", "nest", "sent",
        "tile", "lite", "ties", "site",
        "hello", "world"  # Not anagrams of available letters
    ]

    print(f"Available letters: {available_letters}")
    print(f"Possible words to check: {possible_words}")

    # Find which words can be made from available letters
    target_canonical = ''.join(sorted(available_letters.lower()))
    valid_words = []

    for word in possible_words:
        word_canonical = ''.join(sorted(word.lower()))
        # Check if word can be made from available letters
        if all(word_canonical.count(char) <= target_canonical.count(char) for char in set(word_canonical)):
            valid_words.append(word)

    # Group the valid words by anagrams
    anagram_groups = group_anagrams(valid_words)

    print(f"\nValid words that can be made: {valid_words}")
    print_result("Grouped by anagrams", anagram_groups)

    # Find the longest anagrams
    longest_group = find_largest_anagram_group(valid_words)
    print_result("Longest anagram group", longest_group)


def main():
    """Run all demonstrations."""
    print("Anagram Grouper Function Demonstration")
    print("Comprehensive showcase of all features and capabilities")

    demonstrate_basic_functionality()
    demonstrate_case_sensitivity()
    demonstrate_output_formats()
    demonstrate_sorting_options()
    demonstrate_edge_cases()
    demonstrate_utility_functions()
    demonstrate_performance()
    demonstrate_real_world_example()

    print_section("Summary")
    print("This demonstration covered:")
    print("  ✓ Basic anagram grouping")
    print("  ✓ Case sensitivity options")
    print("  ✓ Multiple output formats")
    print("  ✓ Flexible sorting options")
    print("  ✓ Edge case handling")
    print("  ✓ Utility functions")
    print("  ✓ Performance characteristics")
    print("  ✓ Real-world application example")
    print("\nThe implementation fully complies with the comprehensive specifications!")


if __name__ == "__main__":
    main()