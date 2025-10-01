#!/usr/bin/env python3
"""
Story-to-Limerick Converter
Converts prose stories into limericks using llama3.2 via Ollama.
"""

import json
import subprocess
import sys
from typing import Dict, List, Optional


class LimerickConverter:
    """Converts stories into limericks using Ollama."""

    def __init__(self, model: str = "llama3.2"):
        """Initialize the converter with specified model."""
        self.model = model
        self._verify_ollama()

    def _verify_ollama(self) -> None:
        """Verify Ollama is installed and model is available."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError("Ollama is not running or not installed")

            if self.model not in result.stdout:
                print(f"Warning: {self.model} not found. Attempting to pull...")
                subprocess.run(
                    ["ollama", "pull", self.model],
                    timeout=300
                )
        except FileNotFoundError:
            raise RuntimeError("Ollama is not installed. Please install from https://ollama.ai")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Ollama command timed out")

    def _build_prompt(self, story: str) -> str:
        """Build the optimized prompt for limerick generation."""
        prompt = f"""Convert this story into a limerick (5-line poem with AABBA rhyme scheme).

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
        return prompt

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama with the given prompt."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                raise RuntimeError(f"Ollama error: {result.stderr}")

            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError("Ollama generation timed out")

    def _count_syllables(self, word: str) -> int:
        """
        Simple syllable counter (approximate).
        Counts vowel groups as syllables.
        """
        word = word.lower().strip(".,!?;:\"'")
        if not word:
            return 0

        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1

        # Ensure at least 1 syllable
        if syllable_count == 0:
            syllable_count = 1

        return syllable_count

    def _count_line_syllables(self, line: str) -> int:
        """Count syllables in a line."""
        words = line.split()
        return sum(self._count_syllables(word) for word in words)

    def _validate_limerick(self, lines: List[str]) -> Dict[str, any]:
        """
        Validate limerick structure.
        Returns validation result with details.
        """
        validation = {
            "valid": True,
            "issues": [],
            "syllable_counts": []
        }

        # Check line count
        if len(lines) != 5:
            validation["valid"] = False
            validation["issues"].append(f"Expected 5 lines, got {len(lines)}")
            return validation

        # Count syllables for each line
        for i, line in enumerate(lines, 1):
            count = self._count_line_syllables(line)
            validation["syllable_counts"].append(count)

            # Check syllable counts (with some tolerance)
            if i in [1, 2, 5]:  # Long lines
                if count < 7 or count > 10:
                    validation["valid"] = False
                    validation["issues"].append(
                        f"Line {i}: Expected 8-9 syllables, got {count}"
                    )
            else:  # Short lines (3, 4)
                if count < 4 or count > 7:
                    validation["valid"] = False
                    validation["issues"].append(
                        f"Line {i}: Expected 5-6 syllables, got {count}"
                    )

        return validation

    def convert(self, story: str, validate: bool = True) -> Dict[str, any]:
        """
        Convert a story to a limerick.

        Args:
            story: The prose story to convert
            validate: Whether to validate limerick structure

        Returns:
            Dict with limerick, lines, validation, and metadata
        """
        if not story or not story.strip():
            raise ValueError("Story cannot be empty")

        # Build prompt and call LLM
        prompt = self._build_prompt(story)
        llm_output = self._call_ollama(prompt)

        # Parse output into lines
        lines = [line.strip() for line in llm_output.split('\n') if line.strip()]

        # Handle case where LLM returns extra text
        if len(lines) > 5:
            lines = lines[:5]

        # Validate if requested
        validation_result = None
        if validate:
            validation_result = self._validate_limerick(lines)

        # Build result
        result = {
            "limerick": "\n".join(lines),
            "lines": lines,
            "story": story,
            "model": self.model,
            "validation": validation_result
        }

        return result

    def convert_to_json(self, story: str, validate: bool = True) -> str:
        """Convert story to limerick and return as JSON string."""
        result = self.convert(story, validate)
        return json.dumps(result, indent=2)


def main():
    """CLI interface for the limerick converter."""
    if len(sys.argv) < 2:
        print("Usage: python limerick_converter.py <story>")
        print("\nExample:")
        print('  python limerick_converter.py "Once upon a time, a brave knight..."')
        sys.exit(1)

    story = sys.argv[1]

    print("Converting story to limerick...\n")

    converter = LimerickConverter()
    result = converter.convert(story)

    print("LIMERICK:")
    print("=" * 50)
    print(result["limerick"])
    print("=" * 50)

    if result["validation"]:
        print("\nVALIDATION:")
        print(f"Valid: {result['validation']['valid']}")
        print(f"Syllable counts: {result['validation']['syllable_counts']}")
        if result['validation']['issues']:
            print("Issues:")
            for issue in result['validation']['issues']:
                print(f"  - {issue}")

    print("\nJSON Output:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
