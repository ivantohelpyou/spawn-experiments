"""
Story-to-Haiku Converter - Test-First Development Implementation

This module converts stories/paragraphs into haiku poems (5-7-5 syllable structure)
using a local LLM via Ollama. Implemented using TDD methodology.

Function signature and behavior designed to pass comprehensive test suite.
"""

import re
from typing import Optional

# Import ollama only when needed (for testing without installation)
try:
    import ollama
except ImportError:
    ollama = None


# Constants
MAX_INPUT_LENGTH = 500  # Truncate input to this length
HAIKU_LINE_COUNT = 3    # Traditional haiku has 3 lines
EXPECTED_SYLLABLES = [5, 7, 5]  # Traditional haiku syllable pattern
DEFAULT_MODEL = 'llama3.2'  # Ollama model to use


def count_syllables(text: str) -> int:
    """
    Count syllables in a text string (word or sentence).

    Uses a simplified algorithm:
    - Count vowel groups (consecutive vowels = 1 syllable)
    - Handle silent 'e' at end of words
    - Special cases for common words
    - Minimum 1 syllable per word

    Args:
        text: Input text (word or sentence)

    Returns:
        Total syllable count
    """
    if not text or not text.strip():
        return 0

    text = text.lower().strip()

    # Remove punctuation
    text = re.sub(r'[^a-z\s]', '', text)

    # Split into words
    words = text.split()

    # Special cases dictionary for common words where algorithm fails
    special_cases = {
        'quiet': 2,
        'the': 1,
        'whispers': 2,
    }

    total_syllables = 0

    for word in words:
        if not word:
            continue

        # Check special cases first
        if word in special_cases:
            total_syllables += special_cases[word]
            continue

        # Count vowel groups
        syllables = 0
        previous_was_vowel = False

        for i, char in enumerate(word):
            is_vowel = char in 'aeiouy'

            if is_vowel and not previous_was_vowel:
                syllables += 1

            previous_was_vowel = is_vowel

        # Handle silent 'e' at end
        if len(word) > 2 and word.endswith('e') and word[-2] not in 'aeiouy':
            syllables = max(1, syllables - 1)

        # Every word has at least 1 syllable
        syllables = max(1, syllables)

        total_syllables += syllables

    return total_syllables


def extract_essence(text: str, max_words: int = 10) -> str:
    """
    Extract the core essence/theme from the input text.

    Args:
        text: Input story text
        max_words: Maximum words to include in essence

    Returns:
        Brief description of the story's essence
    """
    # Remove extra whitespace
    text = ' '.join(text.split())

    # Take first sentence or first N words
    words = text.split()[:max_words]
    essence = ' '.join(words)

    # Clean up
    essence = re.sub(r'[^\w\s]', '', essence)

    if len(text.split()) > max_words:
        essence += "..."

    return essence.strip()


def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem.

    Uses a local LLM (via Ollama) to generate a haiku following the
    traditional 5-7-5 syllable structure.

    Args:
        text: Input story or paragraph
        llm_client: Optional LLM client (for testing with mocks)
                   If None, uses real Ollama client

    Returns:
        dict with:
            - haiku: str (the complete haiku with newlines)
            - lines: list[str] (three lines)
            - syllable_counts: list[int] (should be [5, 7, 5])
            - essence: str (what core idea was captured)

    Raises:
        ValueError: If input is empty or LLM returns invalid format

    Example:
        >>> result = story_to_haiku("The old tree stood in the garden...")
        >>> print(result['haiku'])
        Ancient tree stands tall
        Roots deep in garden's embrace
        Wisdom in each branch
    """
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real Ollama client if none provided
    if llm_client is None:
        llm_client = ollama

    # Truncate long inputs
    truncated_text = text[:MAX_INPUT_LENGTH]

    # Construct prompt for haiku generation
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).
Return only the haiku, one line per line, no other text.

Story: {truncated_text}

Haiku:"""

    # Generate haiku using LLM
    response = llm_client.generate(
        model=DEFAULT_MODEL,
        prompt=prompt
    )

    # Parse response
    haiku_text = response['response'].strip()

    # Split into lines and filter empty ones
    lines = [line.strip() for line in haiku_text.split('\n') if line.strip()]

    # Validate structure
    if len(lines) != HAIKU_LINE_COUNT:
        raise ValueError(f"Expected {HAIKU_LINE_COUNT} lines, got {len(lines)}")

    # Count syllables for each line
    syllable_counts = [count_syllables(line) for line in lines]

    # Extract essence from original text
    essence = extract_essence(text)

    # Return structured result
    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllable_counts': syllable_counts,
        'essence': essence
    }


# Demo usage (if run directly)
if __name__ == "__main__":
    test_story = """
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
    """

    print("Story-to-Haiku Converter - TDD Implementation")
    print("=" * 50)
    print(f"\nInput Story:\n{test_story.strip()}")
    print("\n" + "=" * 50)

    try:
        result = story_to_haiku(test_story)

        print(f"\nGenerated Haiku:")
        print(result['haiku'])
        print(f"\nSyllable Counts: {result['syllable_counts']}")
        print(f"Essence: {result['essence']}")

    except Exception as e:
        print(f"\nError: {e}")
        print("Note: This demo requires Ollama to be running with llama3.2 model")
        print("For testing, use mocked LLM client (see test_haiku_converter.py)")