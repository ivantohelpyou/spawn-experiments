"""
Story-to-Haiku Converter - Adaptive TDD Implementation

This implementation follows the Adaptive TDD methodology:
- Strategic tests for complex/risky areas (JSON parsing, validation, errors)
- No tests for obvious/simple operations (string joining, dict building)
- Focus effort where it matters most for quality and maintainability
"""

import json

try:
    import ollama
except ImportError:
    # ollama is only needed for production use, not for testing with mocks
    ollama = None


def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem using LLM with structured JSON output.

    Args:
        text: Input story or paragraph
        llm_client: Optional LLM client (for testing with mocks)

    Returns:
        dict with:
            - haiku: str (complete haiku with newlines)
            - lines: list[str] (three lines)
            - syllables: list[int] (LLM-reported counts [5, 7, 5])
            - essence: str (captured theme/idea)
            - valid: bool (whether syllables match 5-7-5)

    Raises:
        ValueError: If input is empty/whitespace-only or LLM returns invalid JSON
    """
    # Validate input (tested - error handling is complex)
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real Ollama client if none provided (not tested - trivial default)
    if llm_client is None:
        llm_client = ollama

    # Truncate long inputs (not tested - simple string slicing)
    truncated_text = text[:500] if len(text) > 500 else text

    # Build prompt with explicit JSON format requirements (not tested - straightforward f-string)
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Story: {truncated_text}
"""

    # Call LLM (tested - dependency injection is critical for testability)
    response = llm_client.generate(
        model='llama3.2',
        prompt=prompt
    )

    # Parse JSON response (tested - risky, LLM might return malformed JSON)
    try:
        haiku_data = json.loads(response['response'].strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from LLM: {e}")

    # Validate required keys (tested - complex validation logic)
    required_keys = ['lines', 'syllables', 'essence']
    for key in required_keys:
        if key not in haiku_data:
            raise ValueError(f"Missing required key in response: {key}")

    lines = haiku_data['lines']
    syllables = haiku_data['syllables']

    # Validate structure (tested - error handling is important)
    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    if len(syllables) != 3:
        raise ValueError(f"Expected 3 syllable counts, got {len(syllables)}")

    # Validate syllable pattern (tested - core business rule)
    valid = syllables == [5, 7, 5]

    # Build result dict (not tested - trivial dict construction)
    return {
        'haiku': '\n'.join(lines),  # Not tested - string join is stdlib
        'lines': lines,
        'syllables': syllables,
        'essence': haiku_data['essence'],
        'valid': valid
    }