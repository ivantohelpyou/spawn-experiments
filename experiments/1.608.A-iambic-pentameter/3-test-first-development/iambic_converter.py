"""
Iambic Pentameter Converter
Converts prose stories into Shakespearean verse
"""

import re


def count_syllables(word):
    """
    Count syllables in a word using vowel-based heuristic

    Args:
        word: String word to count syllables in

    Returns:
        int: Number of syllables in word
    """
    word = word.lower().strip()
    if not word:
        return 0

    # Remove trailing 'e' (silent e)
    if word.endswith('e'):
        word = word[:-1]

    # Count vowel groups
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    # Every word has at least one syllable
    return max(1, syllable_count)
