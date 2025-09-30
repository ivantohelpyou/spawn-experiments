"""
Story-to-Haiku Converter
Method 3: Test-First Development (TDD)

Implementation written AFTER tests to make them pass.
"""

import json


def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem.

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
        ValueError: If input is empty or invalid
    """
    # Validate input (driven by test_empty_input_raises_error)
    if text is None:
        raise TypeError("Input text cannot be None")

    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real Ollama client if none provided
    if llm_client is None:
        import ollama
        llm_client = ollama

    # Truncate long inputs (driven by test_very_long_input_truncated)
    truncated_text = text[:500] if len(text) > 500 else text

    # Generate haiku with JSON output format (driven by test_prompt_format)
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Story: {truncated_text}
"""

    # Call LLM with llama3.2 model (driven by test_accepts_mock_client)
    response = llm_client.generate(
        model='llama3.2',
        prompt=prompt
    )

    # Parse JSON response (driven by test_handles_malformed_json)
    try:
        haiku_data = json.loads(response['response'].strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from LLM: {e}")

    # Validate structure (driven by test_handles_missing_keys)
    required_keys = ['lines', 'syllables', 'essence']
    for key in required_keys:
        if key not in haiku_data:
            raise ValueError(f"Missing required key in response: {key}")

    lines = haiku_data['lines']
    syllables = haiku_data['syllables']

    # Validate line count (driven by test_handles_wrong_line_count)
    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    # Validate syllable count (driven by test_handles_wrong_syllable_count)
    if len(syllables) != 3:
        raise ValueError(f"Expected 3 syllable counts, got {len(syllables)}")

    # Check if syllables match 5-7-5 (driven by test_validates_syllable_structure)
    valid = syllables == [5, 7, 5]

    # Return structured result (driven by test_parses_json_response)
    return {
        'haiku': '\n'.join(lines),  # Driven by test_haiku_string_format
        'lines': lines,
        'syllables': syllables,
        'essence': haiku_data['essence'],
        'valid': valid
    }