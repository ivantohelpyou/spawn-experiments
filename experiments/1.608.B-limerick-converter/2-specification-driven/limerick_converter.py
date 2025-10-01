"""
Story-to-Limerick Converter

Converts prose stories into valid limericks using llama3.2 via Ollama.

Technical Specification: docs/technical-spec.md
"""

import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests


class SyllableCounter:
    """
    Utility class for counting syllables in English text.
    Uses heuristic vowel-based algorithm.
    """

    @staticmethod
    def count_syllables(word: str) -> int:
        """
        Count syllables in a single word using vowel patterns.

        Algorithm:
        1. Convert to lowercase and strip
        2. Remove trailing silent 'e'
        3. Count vowel groups (consecutive vowels = 1 syllable)
        4. Apply special case rules
        5. Ensure minimum of 1 syllable

        Args:
            word: The word to count syllables for

        Returns:
            Number of syllables in the word
        """
        word = word.lower().strip()
        if len(word) == 0:
            return 0

        # Remove trailing silent 'e' (but not if it's the only vowel)
        if word.endswith('e') and len(word) > 2:
            word = word[:-1]

        # Count vowel groups
        vowels = 'aeiouy'
        count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        # Special case: words ending in -le (like "table", "puzzle")
        if len(word) > 2 and word.endswith('le') and word[-3] not in vowels:
            count += 1

        # Ensure at least 1 syllable
        return max(1, count)

    @staticmethod
    def count_line_syllables(line: str) -> int:
        """
        Count total syllables in a line of text.

        Args:
            line: The line of text to count syllables for

        Returns:
            Total syllable count for the line
        """
        # Remove punctuation and split into words
        cleaned = re.sub(r'[^\w\s]', '', line)
        words = cleaned.split()

        total = 0
        for word in words:
            total += SyllableCounter.count_syllables(word)

        return total


class RhymeChecker:
    """
    Utility class for checking rhyme schemes in poetry.
    Uses simple phonetic matching based on word endings.
    """

    @staticmethod
    def _get_last_word(line: str) -> str:
        """
        Extract the last word from a line, removing punctuation.

        Args:
            line: The line to extract from

        Returns:
            The last word, cleaned of punctuation
        """
        # Remove punctuation and get last word
        cleaned = re.sub(r'[^\w\s]', '', line.strip())
        words = cleaned.split()
        if words:
            return words[-1].lower()
        return ""

    @staticmethod
    def _words_rhyme(word1: str, word2: str) -> bool:
        """
        Check if two words rhyme using simple phonetic matching.

        Algorithm:
        1. Extract last 2-3 characters
        2. Compare endings
        3. Return True if at least last 2 characters match

        Args:
            word1: First word
            word2: Second word

        Returns:
            True if words rhyme, False otherwise
        """
        w1 = word1.lower().strip()
        w2 = word2.lower().strip()

        if not w1 or not w2:
            return False

        # Get endings (last 2-3 chars)
        end1 = w1[-3:] if len(w1) >= 3 else w1
        end2 = w2[-3:] if len(w2) >= 3 else w2

        # Check for match (at least 2 chars matching)
        if len(end1) >= 2 and len(end2) >= 2:
            return end1[-2:] == end2[-2:]

        return False

    @staticmethod
    def check_rhyme_scheme(lines: List[str]) -> Dict:
        """
        Check if lines follow AABBA rhyme scheme.

        Args:
            lines: List of 5 lines to check

        Returns:
            Dictionary with rhyme validation results
        """
        if len(lines) != 5:
            return {
                "detected": "INVALID",
                "is_valid": False,
                "a_rhymes": [],
                "b_rhymes": []
            }

        # Get last words from each line
        last_words = [RhymeChecker._get_last_word(line) for line in lines]

        # Check A rhymes (lines 1, 2, 5)
        a_rhymes = [last_words[0], last_words[1], last_words[4]]
        a_valid = (
            RhymeChecker._words_rhyme(last_words[0], last_words[1]) and
            RhymeChecker._words_rhyme(last_words[0], last_words[4])
        )

        # Check B rhymes (lines 3, 4)
        b_rhymes = [last_words[2], last_words[3]]
        b_valid = RhymeChecker._words_rhyme(last_words[2], last_words[3])

        # Determine detected scheme
        detected = "AABBA" if (a_valid and b_valid) else "INVALID"

        return {
            "detected": detected,
            "is_valid": a_valid and b_valid,
            "a_rhymes": a_rhymes,
            "b_rhymes": b_rhymes
        }


class OutputFormatter:
    """
    Utility class for formatting converter output.
    """

    @staticmethod
    def format_output(
        lines: List[str],
        validation: Dict,
        metadata: Dict
    ) -> Dict:
        """
        Format the final output as structured JSON.

        Args:
            lines: The 5 limerick lines
            validation: Validation results
            metadata: Metadata about the conversion

        Returns:
            Structured JSON output dictionary
        """
        return {
            "limerick": {
                "lines": lines,
                "text": "\n".join(lines)
            },
            "validation": validation,
            "metadata": metadata
        }

    @staticmethod
    def format_error(error_type: str, details: str) -> Dict:
        """
        Format an error response.

        Args:
            error_type: Type/category of error
            details: Detailed error message

        Returns:
            Structured error dictionary
        """
        return {
            "error": error_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }


class LimerickConverter:
    """
    Main converter class that orchestrates story-to-limerick conversion.

    Uses llama3.2 via Ollama to generate limericks from prose stories.
    """

    # Optimized prompt template from specification
    PROMPT_TEMPLATE = """Convert this story into a limerick (5-line poem with AABBA rhyme scheme).

LIMERICK RULES:
1. Exactly 5 lines
2. Rhyme scheme: AABBA (lines 1,2,5 rhyme; lines 3,4 rhyme)
3. Syllable counts: Lines 1,2,5 (8-9 syllables), Lines 3,4 (5-6 syllables)
4. Meter: Anapestic (da-da-DUM rhythm)
5. Capture the essence of the story
6. Typically humorous or clever tone

EXAMPLE STRUCTURE:
Line 1: "A programmer stayed up at night," (9 syllables) - A rhyme
Line 2: "Debugging code was their fight," (8 syllables) - A rhyme
Line 3: "Found one missing mark," (5 syllables) - B rhyme
Line 4: "A semicolon stark," (6 syllables) - B rhyme
Line 5: "Then slept with relief and delight." (9 syllables) - A rhyme

STORY:
{story}

INSTRUCTIONS:
1. Read the story and identify its core essence
2. Create a limerick that captures this essence
3. Count syllables carefully (verify each line)
4. Ensure rhyme scheme is perfect AABBA
5. Check meter follows anapestic pattern
6. Make it clever or humorous if possible

Return ONLY the 5 lines of the limerick, one per line, nothing else."""

    def __init__(
        self,
        model: str = "llama3.2",
        ollama_host: str = "http://localhost:11434"
    ):
        """
        Initialize the limerick converter.

        Args:
            model: The Ollama model to use (default: llama3.2)
            ollama_host: Ollama API endpoint (default: http://localhost:11434)
        """
        self.model = model
        self.ollama_host = ollama_host
        self.api_endpoint = f"{ollama_host}/api/generate"

    def _build_prompt(self, story: str) -> str:
        """
        Build the prompt by injecting story into template.

        Args:
            story: The story to convert

        Returns:
            Complete prompt string
        """
        return self.PROMPT_TEMPLATE.format(story=story.strip())

    def _call_ollama(self, prompt: str, timeout: int = 30) -> str:
        """
        Make HTTP request to Ollama API.

        Args:
            prompt: The prompt to send
            timeout: Request timeout in seconds

        Returns:
            Raw response text from LLM

        Raises:
            ConnectionError: If Ollama is not reachable
            TimeoutError: If request times out
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 200
            }
        }

        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.ollama_host}. "
                f"Make sure Ollama is running. Error: {str(e)}"
            )
        except requests.exceptions.Timeout as e:
            raise TimeoutError(
                f"Request to Ollama timed out after {timeout} seconds. "
                f"Error: {str(e)}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Ollama API: {str(e)}")

    def _parse_response(self, response: str) -> List[str]:
        """
        Extract 5 limerick lines from LLM response.

        Handles various response formats:
        - Plain 5 lines
        - Lines with numbering
        - Lines with extra whitespace
        - Lines with markdown formatting

        Args:
            response: Raw LLM response

        Returns:
            List of 5 cleaned lines

        Raises:
            ValueError: If cannot extract exactly 5 lines
        """
        # Split into lines and clean
        raw_lines = response.strip().split('\n')
        cleaned_lines = []

        for line in raw_lines:
            # Remove leading numbers, bullets, markdown
            line = re.sub(r'^\s*\d+[\.)]\s*', '', line)  # Remove "1. " or "1) "
            line = re.sub(r'^\s*[-*]\s*', '', line)       # Remove "- " or "* "
            line = re.sub(r'^\s*>\s*', '', line)          # Remove "> "
            line = line.strip()

            # Skip empty lines
            if line:
                cleaned_lines.append(line)

        # Validate we have exactly 5 lines
        if len(cleaned_lines) != 5:
            raise ValueError(
                f"Expected 5 lines, got {len(cleaned_lines)}. "
                f"Response may be malformed."
            )

        return cleaned_lines

    def _validate_limerick(self, lines: List[str]) -> Dict:
        """
        Comprehensively validate limerick structure.

        Checks:
        1. Line count (must be 5)
        2. Syllable counts (1,2,5: 8-9; 3,4: 5-6)
        3. Rhyme scheme (AABBA)

        Args:
            lines: List of limerick lines

        Returns:
            Dictionary with validation results
        """
        validation = {
            "is_valid": False,
            "line_count": len(lines),
            "syllable_counts": [],
            "syllable_valid": False,
            "rhyme_scheme": {}
        }

        # Check line count
        if len(lines) != 5:
            return validation

        # Check syllables
        syllable_counts = [
            SyllableCounter.count_line_syllables(line)
            for line in lines
        ]
        validation["syllable_counts"] = syllable_counts

        syllable_valid = (
            8 <= syllable_counts[0] <= 9 and
            8 <= syllable_counts[1] <= 9 and
            5 <= syllable_counts[2] <= 6 and
            5 <= syllable_counts[3] <= 6 and
            8 <= syllable_counts[4] <= 9
        )
        validation["syllable_valid"] = syllable_valid

        # Check rhyme scheme
        rhyme_check = RhymeChecker.check_rhyme_scheme(lines)
        validation["rhyme_scheme"] = rhyme_check

        # Overall validity
        validation["is_valid"] = (
            validation["line_count"] == 5 and
            syllable_valid and
            rhyme_check["is_valid"]
        )

        return validation

    def convert(
        self,
        story: str,
        max_retries: int = 3,
        timeout: int = 30
    ) -> Dict:
        """
        Convert a prose story into a limerick.

        Main conversion method that orchestrates the entire pipeline:
        1. Validate input
        2. Build prompt
        3. Call Ollama
        4. Parse response
        5. Validate limerick
        6. Format output

        Args:
            story: The story to convert (1-3 paragraphs)
            max_retries: Maximum retries for malformed output
            timeout: Timeout for each Ollama call

        Returns:
            Structured JSON output with limerick and validation results

        Raises:
            ValueError: If story is invalid
            ConnectionError: If cannot connect to Ollama
            TimeoutError: If requests timeout
        """
        # Input validation
        if not story or not story.strip():
            return OutputFormatter.format_error(
                "ValidationError",
                "Story cannot be empty"
            )

        if len(story) > 5000:
            return OutputFormatter.format_error(
                "ValidationError",
                "Story too long (max 5000 characters)"
            )

        start_time = time.time()

        # Try conversion with retries
        for attempt in range(max_retries):
            try:
                # Build prompt
                prompt = self._build_prompt(story)

                # Call Ollama
                response = self._call_ollama(prompt, timeout)

                # Parse response
                lines = self._parse_response(response)

                # Validate limerick
                validation = self._validate_limerick(lines)

                # Build metadata
                metadata = {
                    "model": self.model,
                    "timestamp": datetime.now().isoformat(),
                    "story_length": len(story),
                    "generation_time": round(time.time() - start_time, 2),
                    "attempt": attempt + 1
                }

                # Format and return output
                return OutputFormatter.format_output(
                    lines,
                    validation,
                    metadata
                )

            except ValueError as e:
                # Parsing error - retry
                if attempt < max_retries - 1:
                    continue
                else:
                    return OutputFormatter.format_error(
                        "ParsingError",
                        f"Failed to parse response after {max_retries} attempts: {str(e)}"
                    )

            except (ConnectionError, TimeoutError) as e:
                # Don't retry connection/timeout errors
                return OutputFormatter.format_error(
                    type(e).__name__,
                    str(e)
                )

            except Exception as e:
                return OutputFormatter.format_error(
                    "UnexpectedError",
                    f"Unexpected error: {str(e)}"
                )

        # Should never reach here, but just in case
        return OutputFormatter.format_error(
            "MaxRetriesExceeded",
            f"Failed to convert story after {max_retries} attempts"
        )


def main():
    """
    Simple CLI interface for testing the converter.
    """
    import sys

    if len(sys.argv) > 1:
        story = " ".join(sys.argv[1:])
    else:
        # Default test story
        story = """
        A young programmer named Alice loved to code late into the night.
        She was working on a complex algorithm when she discovered a subtle bug.
        After hours of debugging, she finally found it was just a missing semicolon.
        """

    print("Story-to-Limerick Converter")
    print("=" * 60)
    print(f"\nStory:\n{story.strip()}\n")
    print("Converting to limerick...\n")

    converter = LimerickConverter()
    result = converter.convert(story)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        print(f"Details: {result['details']}")
    else:
        print("Limerick:")
        print("-" * 60)
        print(result["limerick"]["text"])
        print("-" * 60)
        print(f"\nValidation: {'VALID' if result['validation']['is_valid'] else 'INVALID'}")
        print(f"Syllable counts: {result['validation']['syllable_counts']}")
        print(f"Rhyme scheme: {result['validation']['rhyme_scheme']['detected']}")
        print(f"\nGeneration time: {result['metadata']['generation_time']}s")

    print("\nOutput JSON:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
