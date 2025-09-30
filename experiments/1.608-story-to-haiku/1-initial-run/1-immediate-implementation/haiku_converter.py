"""Story to Haiku Converter - Method 1: Immediate Implementation"""

try:
    import ollama
except ImportError:
    ollama = None


def count_syllables(word):
    """Quick syllable counter - simplified approach"""
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")

    if not word:
        return 0

    count = 0
    prev_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel

    # Handle silent e
    if len(word) > 2 and word.endswith('e') and count > 1:
        count -= 1

    # Minimum one syllable
    if count < 1:
        count = 1

    return count


def count_line_syllables(line):
    """Count syllables in a line of text"""
    words = line.split()
    return sum(count_syllables(word) for word in words)


def story_to_haiku(text: str, llm_client=None) -> dict:
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
    """
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real Ollama if no client provided
    if llm_client is None:
        llm_client = ollama

    # Truncate long inputs
    text_input = text.strip()[:500]

    # Create prompt
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).
Return only the haiku, one line per line, no other text.

Story: {text_input}

Haiku:"""

    # Generate haiku
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

    # Count syllables
    syllable_counts = [count_line_syllables(line) for line in lines]

    # Extract essence (first few words of story)
    essence_words = text_input.split()[:5]
    essence = ' '.join(essence_words) + '...'

    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllable_counts': syllable_counts,
        'essence': essence
    }