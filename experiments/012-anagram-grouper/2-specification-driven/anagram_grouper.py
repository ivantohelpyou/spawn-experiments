"""
Anagram Grouper Function Implementation

This module provides functionality to group strings that are anagrams of each other.
Implemented according to the comprehensive specifications in anagram_grouper_specifications.md.
"""

from collections import defaultdict
from typing import Iterable, List, Dict, Union
import unicodedata


def group_anagrams(
    words: Iterable[str],
    case_sensitive: bool = False,
    sort_groups: bool = True,
    sort_within_groups: bool = True,
    output_format: str = 'list'
) -> Union[List[List[str]], Dict[str, List[str]]]:
    """
    Group strings that are anagrams of each other.

    An anagram is a word or phrase formed by rearranging the letters of another word or phrase,
    typically using all the original letters exactly once.

    Args:
        words: An iterable of strings to group by anagrams
        case_sensitive: Whether to consider case when determining anagrams (default: False)
        sort_groups: Whether to sort groups by their canonical representation (default: True)
        sort_within_groups: Whether to sort words within each group (default: True)
        output_format: Output format - 'list' for list of lists, 'dict' for dictionary (default: 'list')

    Returns:
        List of lists containing anagram groups (if output_format='list'), or
        Dictionary mapping canonical forms to anagram groups (if output_format='dict')

    Raises:
        TypeError: If input contains non-string items or input is not iterable
        ValueError: If output_format is not 'list' or 'dict'

    Examples:
        >>> group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
        [['ate', 'eat', 'tea'], ['nat', 'tan'], ['bat']]

        >>> group_anagrams(['listen', 'silent', 'hello'], output_format='dict')
        {'eilnst': ['listen', 'silent'], 'ehllo': ['hello']}

        >>> group_anagrams(['Eat', 'Tea', 'ate'], case_sensitive=True)
        [['ate'], ['Eat'], ['Tea']]

        >>> group_anagrams(['Eat', 'Tea', 'ate'], case_sensitive=False)
        [['Eat', 'Tea', 'ate']]
    """
    # Validate output_format parameter
    if output_format not in ('list', 'dict'):
        raise ValueError(f"output_format must be 'list' or 'dict', got '{output_format}'")

    # Convert to list to allow multiple iterations and validate input
    try:
        word_list = list(words)
    except TypeError:
        raise TypeError("Input must be iterable")

    # Validate that all items are strings
    for i, word in enumerate(word_list):
        if not isinstance(word, str):
            raise TypeError(f"All items must be strings, but item at index {i} is {type(word).__name__}")

    # Handle empty input
    if not word_list:
        return [] if output_format == 'list' else {}

    # Group anagrams using canonical form as key
    anagram_groups = defaultdict(list)

    for word in word_list:
        canonical_form = _get_canonical_form(word, case_sensitive)
        anagram_groups[canonical_form].append(word)

    # Sort within groups if requested
    if sort_within_groups:
        for group in anagram_groups.values():
            group.sort()

    # Prepare output based on format
    if output_format == 'dict':
        result_dict = dict(anagram_groups)
        if sort_groups:
            # Return a new dictionary with sorted keys
            return {k: result_dict[k] for k in sorted(result_dict.keys())}
        return result_dict

    else:  # output_format == 'list'
        result_list = list(anagram_groups.values())
        if sort_groups:
            # Sort groups by their canonical form (the key)
            canonical_forms = list(anagram_groups.keys())
            sorted_keys = sorted(canonical_forms)
            result_list = [anagram_groups[key] for key in sorted_keys]

        return result_list


def _get_canonical_form(word: str, case_sensitive: bool) -> str:
    """
    Generate a canonical form of a word for anagram comparison.

    The canonical form is created by:
    1. Normalizing Unicode characters
    2. Converting to lowercase if not case sensitive
    3. Sorting the characters

    Args:
        word: The word to generate canonical form for
        case_sensitive: Whether to preserve case in canonical form

    Returns:
        A string representing the canonical form of the word
    """
    # Normalize Unicode characters to ensure consistent comparison
    normalized = unicodedata.normalize('NFC', word)

    # Convert to lowercase if not case sensitive
    if not case_sensitive:
        normalized = normalized.lower()

    # Sort characters to create canonical form
    return ''.join(sorted(normalized))


# Additional utility functions for advanced use cases

def count_anagram_groups(words: Iterable[str], case_sensitive: bool = False) -> int:
    """
    Count the number of anagram groups in a collection of words.

    Args:
        words: An iterable of strings
        case_sensitive: Whether to consider case when determining anagrams

    Returns:
        The number of distinct anagram groups

    Examples:
        >>> count_anagram_groups(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
        3
    """
    groups = group_anagrams(words, case_sensitive=case_sensitive, output_format='dict')
    return len(groups)


def find_largest_anagram_group(words: Iterable[str], case_sensitive: bool = False) -> List[str]:
    """
    Find the largest group of anagrams in a collection of words.

    Args:
        words: An iterable of strings
        case_sensitive: Whether to consider case when determining anagrams

    Returns:
        List of words in the largest anagram group (empty list if no words)

    Examples:
        >>> find_largest_anagram_group(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
        ['ate', 'eat', 'tea']
    """
    groups = group_anagrams(words, case_sensitive=case_sensitive, output_format='list')
    if not groups:
        return []

    return max(groups, key=len)


def are_anagrams(word1: str, word2: str, case_sensitive: bool = False) -> bool:
    """
    Check if two words are anagrams of each other.

    Args:
        word1: First word to compare
        word2: Second word to compare
        case_sensitive: Whether to consider case when determining anagrams

    Returns:
        True if the words are anagrams, False otherwise

    Examples:
        >>> are_anagrams('listen', 'silent')
        True
        >>> are_anagrams('hello', 'world')
        False
        >>> are_anagrams('Listen', 'silent', case_sensitive=True)
        False
        >>> are_anagrams('Listen', 'silent', case_sensitive=False)
        True
    """
    if not isinstance(word1, str) or not isinstance(word2, str):
        raise TypeError("Both arguments must be strings")

    return _get_canonical_form(word1, case_sensitive) == _get_canonical_form(word2, case_sensitive)


if __name__ == "__main__":
    # Demonstration of the anagram grouper functionality
    print("Anagram Grouper Demonstration")
    print("=" * 40)

    # Example 1: Basic usage
    words1 = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
    result1 = group_anagrams(words1)
    print(f"Input: {words1}")
    print(f"Groups: {result1}")
    print()

    # Example 2: Case sensitivity
    words2 = ['Eat', 'Tea', 'ate', 'Listen', 'Silent']
    result2_case_sensitive = group_anagrams(words2, case_sensitive=True)
    result2_case_insensitive = group_anagrams(words2, case_sensitive=False)
    print(f"Input: {words2}")
    print(f"Case sensitive: {result2_case_sensitive}")
    print(f"Case insensitive: {result2_case_insensitive}")
    print()

    # Example 3: Dictionary output format
    result3 = group_anagrams(words1, output_format='dict')
    print(f"Dictionary format: {result3}")
    print()

    # Example 4: Utility functions
    print(f"Number of anagram groups: {count_anagram_groups(words1)}")
    print(f"Largest anagram group: {find_largest_anagram_group(words1)}")
    print(f"Are 'listen' and 'silent' anagrams? {are_anagrams('listen', 'silent')}")
    print(f"Are 'hello' and 'world' anagrams? {are_anagrams('hello', 'world')}")