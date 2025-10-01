"""
Limerick Converter - Story to Limerick conversion using llama3.2 via Ollama.
Implementation following Adaptive TDD methodology.
"""

import re
import json
import requests
from typing import List, Dict, Any


def validate_story_input(story: str) -> str:
    """
    Validate and clean story input.

    Args:
        story: Input story text

    Returns:
        Cleaned story text

    Raises:
        ValueError: If story is invalid
    """
    # Check for empty or whitespace-only strings
    if not story or not story.strip():
        raise ValueError("Story cannot be empty")

    cleaned = story.strip()

    # Check minimum length (after cleaning)
    if len(cleaned) < 10:
        raise ValueError("Story too short (minimum 10 characters)")

    return cleaned


def count_syllables(text: str) -> int:
    """
    Count syllables in text using improved algorithm.
    Handles silent 'e', consecutive vowels, and 'y' as vowel.

    Args:
        text: Text to count syllables in

    Returns:
        Number of syllables
    """
    if not text:
        return 0

    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())

    # Split into words
    words = text.split()
    total = 0

    for word in words:
        if not word:
            continue

        # Count vowel groups (consecutive vowels = 1 syllable)
        # Treat 'y' as vowel when not at start
        syllables = 0
        previous_was_vowel = False

        for i, char in enumerate(word):
            # 'y' is a vowel if not at the start of word
            is_vowel = char in 'aeiou' or (char == 'y' and i > 0)
            if is_vowel and not previous_was_vowel:
                syllables += 1
            previous_was_vowel = is_vowel

        # Handle silent 'e' at end of word (but not for words ending in 'le' after consonant)
        if len(word) > 2 and word.endswith('e') and syllables > 1:
            # Check if the 'e' is truly silent
            # Don't subtract for consonant + 'le' patterns (table, little, etc.)
            if word[-2] not in 'aeiou' and not (word.endswith('le') and len(word) > 2 and word[-3] not in 'aeiou'):
                syllables -= 1

        # Every word has at least 1 syllable
        syllables = max(1, syllables)

        total += syllables

    return total


def extract_rhyme_sounds(text: str) -> str:
    """
    Extract rhyme sound from text (last word's ending).
    Takes the vowel sound and everything after it from the last syllable.

    Args:
        text: Text to extract rhyme from

    Returns:
        Rhyme sound (lowercase)
    """
    # Get last word
    words = re.sub(r'[^a-zA-Z\s]', '', text).split()
    if not words:
        return ""

    last_word = words[-1].lower()

    # Find the last vowel and take from there to end
    # This captures the rhyming portion
    for i in range(len(last_word) - 1, -1, -1):
        if last_word[i] in 'aeiou':
            return last_word[i:]

    # If no vowel found, return last 2-3 chars
    return last_word[-3:] if len(last_word) >= 3 else last_word


def check_rhyme_scheme(text1: str, text2: str) -> bool:
    """
    Check if two texts rhyme (case-insensitive).

    Args:
        text1: First text
        text2: Second text

    Returns:
        True if they rhyme, False otherwise
    """
    rhyme1 = extract_rhyme_sounds(text1).lower()
    rhyme2 = extract_rhyme_sounds(text2).lower()

    # Check if they match (case-insensitive)
    return rhyme1 == rhyme2 and rhyme1 != ""


def validate_limerick_structure(lines: List[str]) -> Dict[str, Any]:
    """
    Validate limerick structure (5 lines, AABBA rhyme, syllable counts).

    Args:
        lines: List of limerick lines

    Returns:
        Dictionary with validation results
    """
    errors = []

    # Check line count
    if len(lines) != 5:
        errors.append(f"Limerick must have exactly 5 lines (got {len(lines)})")
        return {
            "valid": False,
            "errors": errors,
            "syllable_counts": []
        }

    # Count syllables for each line
    syllable_counts = [count_syllables(line) for line in lines]

    # Check syllable requirements
    # Lines 1, 2, 5 should have 8-9 syllables
    # Lines 3, 4 should have 5-6 syllables
    if not (8 <= syllable_counts[0] <= 9):
        errors.append(f"Line 1 should have 8-9 syllables (got {syllable_counts[0]})")
    if not (8 <= syllable_counts[1] <= 9):
        errors.append(f"Line 2 should have 8-9 syllables (got {syllable_counts[1]})")
    if not (5 <= syllable_counts[2] <= 6):
        errors.append(f"Line 3 should have 5-6 syllables (got {syllable_counts[2]})")
    if not (5 <= syllable_counts[3] <= 6):
        errors.append(f"Line 4 should have 5-6 syllables (got {syllable_counts[3]})")
    if not (8 <= syllable_counts[4] <= 9):
        errors.append(f"Line 5 should have 8-9 syllables (got {syllable_counts[4]})")

    # Check AABBA rhyme scheme
    # Lines 1, 2, 5 should rhyme (A)
    # Lines 3, 4 should rhyme (B)
    if not check_rhyme_scheme(lines[0], lines[1]):
        errors.append("Lines 1 and 2 must rhyme (A rhyme)")
    if not check_rhyme_scheme(lines[0], lines[4]):
        errors.append("Lines 1 and 5 must rhyme (A rhyme)")
    if not check_rhyme_scheme(lines[2], lines[3]):
        errors.append("Lines 3 and 4 must rhyme (B rhyme)")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "syllable_counts": syllable_counts
    }


class LimerickConverter:
    """Main converter class for story-to-limerick conversion."""

    def __init__(self, model_name: str = "llama3.2", ollama_url: str = "http://localhost:11434"):
        """Initialize converter with model settings."""
        self.model_name = model_name
        self.ollama_url = ollama_url

    def _build_prompt(self, story: str) -> str:
        """Build prompt for LLM."""
        return f"""Convert this story into a limerick (5-line poem with AABBA rhyme scheme).

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

    def _parse_response(self, response: str) -> List[str]:
        """Parse LLM response to extract limerick lines."""
        # Split into lines and filter empty ones
        lines = [line.strip() for line in response.split('\n') if line.strip()]

        # Try to find exactly 5 consecutive non-empty lines
        # Look for the limerick in the response
        if len(lines) >= 5:
            # Find the best sequence of 5 lines (longest average length)
            best_start = 0
            best_avg_len = 0

            for i in range(len(lines) - 4):
                five_lines = lines[i:i+5]
                avg_len = sum(len(l) for l in five_lines) / 5
                if avg_len > best_avg_len:
                    best_avg_len = avg_len
                    best_start = i

            return lines[best_start:best_start+5]

        return lines[:5] if lines else []

    def _format_output(self, lines: List[str], story: str) -> str:
        """Format output as JSON with validation."""
        validation = validate_limerick_structure(lines)

        output = {
            "limerick": {
                "text": "\n".join(lines),
                "lines": lines
            },
            "story": story,
            "validation": validation
        }

        return json.dumps(output, indent=2)

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API."""
        url = f"{self.ollama_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

        return response.json()["response"]

    def convert(self, story: str) -> str:
        """
        Convert story to limerick.

        Args:
            story: Input story text

        Returns:
            JSON string with limerick and validation
        """
        # Validate input
        clean_story = validate_story_input(story)

        # Build prompt
        prompt = self._build_prompt(clean_story)

        # Call LLM
        response = self._call_ollama(prompt)

        # Parse response
        lines = self._parse_response(response)

        # Format and return
        return self._format_output(lines, clean_story)
