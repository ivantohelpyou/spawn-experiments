"""Story-to-Limerick Converter using Test-Driven Development."""
import re
import subprocess


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

    def generate_limerick(self, story):
        """
        Generate a limerick from a story using Ollama LLM.

        Args:
            story: String containing the story to convert

        Returns:
            Dict with:
                - limerick: string of complete limerick
                - lines: list of 5 lines
        """
        prompt = f"""Convert this story into a limerick (5-line poem with AABBA rhyme scheme).

LIMERICK RULES:
1. Exactly 5 lines
2. Rhyme scheme: AABBA (lines 1,2,5 rhyme; lines 3,4 rhyme)
3. Syllable counts: Lines 1,2,5 (8-9 syllables), Lines 3,4 (5-6 syllables)
4. Meter: Anapestic (da-da-DUM rhythm)
5. Capture the essence of the story
6. Typically humorous or clever tone

STORY:
{story}

Return ONLY the 5 lines of the limerick, one per line, nothing else."""

        # Call Ollama using subprocess
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse output
        limerick_text = result.stdout.strip()
        lines = [line.strip() for line in limerick_text.split('\n') if line.strip()]

        # Take first 5 lines
        final_lines = lines[:5]

        return {
            'limerick': '\n'.join(final_lines),
            'lines': final_lines
        }
