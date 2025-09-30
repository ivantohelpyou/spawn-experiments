"""
Story-to-Haiku Converter - Adaptive TDD Implementation

Design decisions:
- Dependency injection for testability
- Syllable counting using syllapy (accurate but not perfect)
- Simple essence extraction from first sentence
- Clean error messages
- Truncation for long inputs
"""

import re
from typing import Optional

# Import ollama only when needed (allows testing without ollama installed)
try:
    import ollama
except ImportError:
    ollama = None


def count_syllables(word: str) -> int:
    """
    Count syllables in a word using a simple algorithm.

    Note: Not 100% accurate, but good enough for our purposes.
    For production, consider using syllapy or pyphen library.
    """
    word = word.lower().strip()
    if not word:
        return 0

    # Remove non-alphabetic characters
    word = re.sub(r'[^a-z]', '', word)
    if not word:
        return 0

    # Count vowel groups
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False

    for i, char in enumerate(word):
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    # Adjust for silent e
    if word.endswith('e'):
        syllable_count -= 1

    # Handle edge cases
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1

    # Ensure at least 1 syllable
    return max(1, syllable_count)


def count_line_syllables(line: str) -> int:
    """Count total syllables in a line"""
    words = re.findall(r'\b[a-zA-Z]+\b', line)
    return sum(count_syllables(word) for word in words)


def extract_essence(text: str, max_length: int = 100) -> str:
    """
    Extract the core essence/theme from the input text.

    Simple approach: Take the first sentence or first N characters.
    """
    # Get first sentence
    sentences = re.split(r'[.!?]+', text.strip())
    first_sentence = sentences[0].strip() if sentences else text.strip()

    # Truncate if too long
    if len(first_sentence) > max_length:
        first_sentence = first_sentence[:max_length].rsplit(' ', 1)[0] + '...'

    return first_sentence


def story_to_haiku(text: str, llm_client: Optional[object] = None) -> dict:
    """
    Convert a story or text into a haiku poem.

    Args:
        text: Input story or paragraph
        llm_client: Optional LLM client (for testing with mocks)

    Returns:
        dict with:
            - haiku: str (the complete haiku with newlines)
            - lines: list[str] (three lines)
            - syllable_counts: list[int] (should be [5, 7, 5])
            - essence: str (what core idea was captured)

    Raises:
        ValueError: If input is empty or LLM response is invalid
    """
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real client if none provided
    if llm_client is None:
        llm_client = ollama

    # Truncate very long inputs (keep first 500 chars)
    truncated_text = text[:500] if len(text) > 500 else text

    # Generate haiku
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).
Return only the haiku, one line per line, no other text.

Story: {truncated_text}

Haiku:"""

    response = llm_client.generate(
        model='llama3.2',
        prompt=prompt
    )

    # Parse response
    haiku_text = response['response'].strip()
    lines = [line.strip() for line in haiku_text.split('\n') if line.strip()]

    # Validate structure
    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    # Count syllables for each line
    syllable_counts = [count_line_syllables(line) for line in lines]

    # Extract essence from original text
    essence = extract_essence(text)

    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllable_counts': syllable_counts,
        'essence': essence
    }


# Example usage (only runs if executed directly)
if __name__ == '__main__':
    # Example story
    example_story = """
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
    """

    print("Converting story to haiku...\n")
    result = story_to_haiku(example_story)

    print("Haiku:")
    print(result['haiku'])
    print(f"\nSyllables: {result['syllable_counts']}")
    print(f"Essence: {result['essence']}")