"""
Iambic Pentameter Converter - Adaptive/Validated TDD Implementation
Converts prose text to Shakespearean verse in iambic pentameter
"""

import re
import json
import subprocess


class SyllableCounter:
    """Counts syllables in English words using rule-based approach"""

    def count(self, word):
        """Count syllables in a word"""
        if not word:
            return 0

        # Remove punctuation
        word = re.sub(r'[^a-zA-Z]', '', word)
        if not word:
            return 0

        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False

        # Count vowel groups
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        # Handle silent 'e' at the end (but not for consonant + 'le')
        if word.endswith('e'):
            if len(word) >= 3 and word[-2:] == 'le' and word[-3] not in vowels:
                # Words like "table", "little" - the 'le' counts as a syllable
                pass
            elif count > 1:
                # Regular silent 'e' like "make", "time"
                count -= 1

        # Handle -ely endings (e before ly is usually silent)
        if len(word) >= 4 and word.endswith('ely') and not word.endswith('eely'):
            if count > 2:  # Need at least 2 to subtract 1
                count -= 1

        # Ensure at least 1 syllable for non-empty words
        return max(count, 1)


class OllamaClient:
    """Client for interacting with Ollama LLM"""

    def __init__(self, model="llama3.2"):
        self.model = model

    def generate(self, prompt):
        """Generate text using Ollama"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return ""
        except FileNotFoundError:
            raise RuntimeError("Ollama is not installed or not in PATH")


class IambicConverter:
    """Main converter for transforming prose to iambic pentameter"""

    def __init__(self):
        self.syllable_counter = SyllableCounter()
        self.ollama = OllamaClient()

    def count_syllables(self, text):
        """Count total syllables in a text string"""
        words = re.findall(r'\b\w+\b', text)
        return sum(self.syllable_counter.count(word) for word in words)

    def convert(self, prose_text):
        """Convert prose text to iambic pentameter"""
        prompt = f"""Convert the following prose text into iambic pentameter.
Iambic pentameter has 10 syllables per line with alternating unstressed/stressed pattern (da-DUM da-DUM da-DUM da-DUM da-DUM).

Prose text:
{prose_text}

Return only the converted iambic pentameter verse, one line per 10 syllables:"""

        result = self.ollama.generate(prompt)
        return result


def main():
    """Command-line interface for the converter"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python iambic_converter.py <prose_text>")
        print("Example: python iambic_converter.py 'The cat sat on the mat'")
        sys.exit(1)

    prose = ' '.join(sys.argv[1:])
    converter = IambicConverter()

    print(f"Input: {prose}")
    print(f"Syllables: {converter.count_syllables(prose)}")
    print("\nConverted to iambic pentameter:")
    print(converter.convert(prose))


if __name__ == '__main__':
    main()
