"""
Anagram Grouper Function Implementation
Developed using Test-Driven Development with comprehensive validation
"""

from typing import List


def group_anagrams(words: List[str]) -> List[List[str]]:
    """
    Groups anagrams together from a list of words.

    Args:
        words: List of strings to group by anagrams

    Returns:
        List of lists, where each inner list contains anagrams of each other

    Raises:
        TypeError: If input is not a list or contains non-string elements
        ValueError: If input contains None values
    """
    # FEATURE 5 - GREEN: Input validation
    # Check if input is a list
    if not isinstance(words, list):
        raise TypeError(f"Input must be a list, got {type(words).__name__}")

    # FEATURE 1 - GREEN: Handle empty input
    if not words:
        return []

    # Validate all elements are strings
    for i, word in enumerate(words):
        if word is None:
            raise ValueError(f"Input cannot contain None values at index {i}")
        if not isinstance(word, str):
            raise TypeError(f"All elements must be strings, got {type(word).__name__} at index {i}")

    # FEATURE 3 - GREEN: Correct anagram grouping implementation
    from collections import defaultdict
    groups = defaultdict(list)

    for word in words:
        # Create case-insensitive anagram key by sorting lowercase characters
        key = ''.join(sorted(word.lower()))
        # Preserve original word formatting in the group
        groups[key].append(word)

    # Return groups in order of first occurrence
    return list(groups.values())