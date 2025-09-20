from typing import List, Dict
from collections import defaultdict


def group_anagrams(words: List[str]) -> List[List[str]]:
    """
    Groups words that are anagrams of each other.

    Args:
        words: List of strings to group by anagrams

    Returns:
        List of lists, where each inner list contains words that are anagrams

    Raises:
        TypeError: If input is not a list or contains non-string elements

    Examples:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

        >>> group_anagrams([])
        []
    """
    _validate_input(words)

    if not words:
        return []

    anagram_groups = _build_anagram_groups(words)
    return list(anagram_groups.values())


def _validate_input(words: List[str]) -> None:
    """Validate that input is a list of strings."""
    if words is None:
        raise TypeError("Input cannot be None")

    if not isinstance(words, list):
        raise TypeError("Input must be a list")

    for word in words:
        if not isinstance(word, str):
            raise TypeError("All elements must be strings")


def _build_anagram_groups(words: List[str]) -> Dict[str, List[str]]:
    """Build dictionary mapping anagram signatures to word groups."""
    anagram_groups = defaultdict(list)

    for word in words:
        signature = _create_anagram_signature(word)
        anagram_groups[signature].append(word)

    return anagram_groups


def _create_anagram_signature(word: str) -> str:
    """Create anagram signature by sorting characters case-insensitively."""
    return ''.join(sorted(word.lower()))