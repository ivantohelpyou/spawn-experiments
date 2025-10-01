"""Story-to-Limerick Converter using Test-Driven Development."""
import re


class LimerickConverter:
    """Converts stories to limericks with proper AABBA rhyme scheme."""

    def count_syllables(self, word):
        """
        Count syllables in a word using heuristic approach.

        Args:
            word: String to count syllables in

        Returns:
            int: Number of syllables
        """
        word = word.lower().strip()
        word = re.sub(r'[^a-z]', '', word)

        if len(word) == 0:
            return 0

        # Count vowel groups
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            syllable_count -= 1

        # Every word has at least one syllable
        if syllable_count == 0:
            syllable_count = 1

        return syllable_count

    def count_syllables_in_line(self, line):
        """
        Count total syllables in a line.

        Args:
            line: String containing a line of text

        Returns:
            int: Total syllable count
        """
        words = line.split()
        return sum(self.count_syllables(word) for word in words)

    def validate_limerick_structure(self, limerick_lines):
        """
        Validate that a limerick has the correct structure.

        Args:
            limerick_lines: List of strings, each representing a line

        Returns:
            Dict with:
                - valid: bool indicating if structure is valid
                - line_count: int number of lines
                - issues: list of validation issues found
        """
        issues = []
        line_count = len(limerick_lines)

        if line_count != 5:
            issues.append(f'Must have exactly 5 lines, got {line_count}')

        return {
            'valid': len(issues) == 0,
            'line_count': line_count,
            'issues': issues
        }
