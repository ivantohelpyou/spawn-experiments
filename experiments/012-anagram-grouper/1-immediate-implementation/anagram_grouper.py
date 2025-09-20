#!/usr/bin/env python3
"""
Anagram Grouper - A comprehensive solution for grouping anagrams

This module provides functionality to group words that are anagrams of each other.
Anagrams are words formed by rearranging the letters of another word, using all
the original letters exactly once.

Example:
    ['eat', 'tea', 'tan', 'ate', 'nat', 'bat'] ->
    [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
"""

from collections import defaultdict
from typing import List, Dict, Any, Union


def normalize_word(word: str) -> str:
    """
    Normalize a word for anagram comparison by converting to lowercase
    and sorting its characters.

    Args:
        word (str): The word to normalize

    Returns:
        str: The normalized word with sorted characters

    Example:
        >>> normalize_word("Listen")
        "eilnst"
        >>> normalize_word("Silent")
        "eilnst"
    """
    if not isinstance(word, str):
        raise TypeError(f"Expected string, got {type(word).__name__}")

    return ''.join(sorted(word.lower().strip()))


def validate_input(words: Any) -> List[str]:
    """
    Validate and clean the input list of words.

    Args:
        words: Input to validate (should be a list of strings)

    Returns:
        List[str]: Cleaned list of valid string words

    Raises:
        TypeError: If input is not a list or contains non-string items

    Example:
        >>> validate_input(['eat', 'tea', 'bat'])
        ['eat', 'tea', 'bat']
        >>> validate_input(['eat', '', '  ', 'tea'])
        ['eat', 'tea']
    """
    if not isinstance(words, list):
        raise TypeError(f"Expected list, got {type(words).__name__}")

    validated_words = []
    for i, word in enumerate(words):
        if not isinstance(word, str):
            raise TypeError(f"Item at index {i} is not a string: {type(word).__name__}")

        # Skip empty strings and strings with only whitespace
        cleaned_word = word.strip()
        if cleaned_word:
            validated_words.append(cleaned_word)

    return validated_words


def group_anagrams(words: List[str]) -> List[List[str]]:
    """
    Group words that are anagrams of each other.

    This function takes a list of words and returns a list of lists, where each
    inner list contains words that are anagrams of each other. The grouping is
    case-insensitive and ignores leading/trailing whitespace.

    Args:
        words (List[str]): List of words to group

    Returns:
        List[List[str]]: List of anagram groups, each group is a list of words

    Raises:
        TypeError: If input is not a list or contains non-string items

    Example:
        >>> group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

        >>> group_anagrams(['Listen', 'Silent', 'Enlist'])
        [['Listen', 'Silent', 'Enlist']]

        >>> group_anagrams([])
        []
    """
    # Validate input
    validated_words = validate_input(words)

    # Handle edge case: empty list
    if not validated_words:
        return []

    # Group words by their normalized form
    anagram_groups: Dict[str, List[str]] = defaultdict(list)

    for word in validated_words:
        try:
            normalized = normalize_word(word)
            anagram_groups[normalized].append(word)
        except TypeError as e:
            # This shouldn't happen after validation, but just in case
            raise TypeError(f"Error processing word '{word}': {e}")

    # Convert to list of lists and sort for consistent output
    result = list(anagram_groups.values())

    # Sort each group alphabetically (case-insensitive) for consistent output
    for group in result:
        group.sort(key=str.lower)

    # Sort groups by the first word in each group for consistent output
    result.sort(key=lambda group: group[0].lower())

    return result


def group_anagrams_with_stats(words: List[str]) -> Dict[str, Union[List[List[str]], Dict[str, int]]]:
    """
    Group anagrams and provide additional statistics.

    Args:
        words (List[str]): List of words to group

    Returns:
        Dict containing:
            - 'groups': List of anagram groups
            - 'stats': Dictionary with statistics (total_words, total_groups, etc.)

    Example:
        >>> result = group_anagrams_with_stats(['eat', 'tea', 'bat'])
        >>> result['groups']
        [['eat', 'tea'], ['bat']]
        >>> result['stats']
        {'total_words': 3, 'total_groups': 2, 'largest_group_size': 2, 'single_word_groups': 1}
    """
    groups = group_anagrams(words)

    stats = {
        'total_words': len(validate_input(words)),
        'total_groups': len(groups),
        'largest_group_size': max(len(group) for group in groups) if groups else 0,
        'single_word_groups': sum(1 for group in groups if len(group) == 1),
        'multi_word_groups': sum(1 for group in groups if len(group) > 1)
    }

    return {
        'groups': groups,
        'stats': stats
    }


def find_anagrams_of_word(target_word: str, word_list: List[str]) -> List[str]:
    """
    Find all anagrams of a specific target word from a list of words.

    Args:
        target_word (str): The word to find anagrams for
        word_list (List[str]): List of words to search through

    Returns:
        List[str]: List of words that are anagrams of the target word

    Example:
        >>> find_anagrams_of_word('eat', ['tea', 'bat', 'ate', 'tab'])
        ['tea', 'ate']
    """
    if not isinstance(target_word, str):
        raise TypeError(f"target_word must be a string, got {type(target_word).__name__}")

    validated_list = validate_input(word_list)
    target_normalized = normalize_word(target_word)

    anagrams = []
    for word in validated_list:
        if word.lower().strip() != target_word.lower().strip():  # Don't include the word itself
            if normalize_word(word) == target_normalized:
                anagrams.append(word)

    return sorted(anagrams, key=str.lower)


def is_anagram(word1: str, word2: str) -> bool:
    """
    Check if two words are anagrams of each other.

    Args:
        word1 (str): First word
        word2 (str): Second word

    Returns:
        bool: True if the words are anagrams, False otherwise

    Example:
        >>> is_anagram('listen', 'silent')
        True
        >>> is_anagram('hello', 'world')
        False
    """
    if not isinstance(word1, str) or not isinstance(word2, str):
        return False

    # Words are anagrams if they have the same normalized form
    # but are not the same word (case-insensitive)
    return (normalize_word(word1) == normalize_word(word2) and
            word1.lower().strip() != word2.lower().strip())


def demo():
    """
    Demonstrate the anagram grouper functionality with various examples.
    """
    print("=== Anagram Grouper Demo ===\n")

    # Basic example
    print("1. Basic Example:")
    words1 = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
    result1 = group_anagrams(words1)
    print(f"Input: {words1}")
    print(f"Output: {result1}")
    print()

    # Case insensitive example
    print("2. Case Insensitive Example:")
    words2 = ['Listen', 'Silent', 'Enlist', 'Hello', 'World']
    result2 = group_anagrams(words2)
    print(f"Input: {words2}")
    print(f"Output: {result2}")
    print()

    # Example with whitespace and duplicates
    print("3. Example with Whitespace and Edge Cases:")
    words3 = ['  eat  ', 'tea', '', 'ate', '   ', 'tea', 'bat']
    result3 = group_anagrams(words3)
    print(f"Input: {words3}")
    print(f"Output: {result3}")
    print()

    # Statistics example
    print("4. Example with Statistics:")
    result4 = group_anagrams_with_stats(words1)
    print(f"Input: {words1}")
    print(f"Groups: {result4['groups']}")
    print(f"Stats: {result4['stats']}")
    print()

    # Find anagrams of specific word
    print("5. Find Anagrams of Specific Word:")
    target = 'eat'
    word_list = ['tea', 'bat', 'ate', 'tab', 'hello', 'world']
    anagrams = find_anagrams_of_word(target, word_list)
    print(f"Find anagrams of '{target}' in {word_list}")
    print(f"Result: {anagrams}")
    print()

    # Check if two words are anagrams
    print("6. Check if Two Words are Anagrams:")
    pairs = [('listen', 'silent'), ('hello', 'world'), ('eat', 'tea')]
    for word1, word2 in pairs:
        result = is_anagram(word1, word2)
        print(f"'{word1}' and '{word2}' are anagrams: {result}")
    print()

    # Edge cases
    print("7. Edge Cases:")
    edge_cases = [
        [],
        ['single'],
        ['a', 'b', 'c'],
        ['same', 'same', 'same']
    ]

    for case in edge_cases:
        result = group_anagrams(case)
        print(f"Input: {case} -> Output: {result}")


if __name__ == "__main__":
    demo()