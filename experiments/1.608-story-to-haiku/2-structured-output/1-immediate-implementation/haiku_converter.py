import ollama
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
    """
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real client if none provided
    if llm_client is None:
        llm_client = ollama

    # Truncate long inputs
    truncated_text = text[:500] if len(text) > 500 else text

    # Generate haiku with JSON output format
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Important: Count syllables carefully and report the actual counts for each line.

Story: {truncated_text}
"""

    response = llm_client.generate(
        model='llama3.2',
        prompt=prompt
    )

    # Parse JSON response
    response_text = response['response'].strip()

    # Try to extract JSON if LLM added extra text
    if not response_text.startswith('{'):
        # Find first { and last }
        start = response_text.find('{')
        end = response_text.rfind('}')
        if start != -1 and end != -1:
            response_text = response_text[start:end+1]

    try:
        haiku_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from LLM: {e}")

    # Validate structure
    required_keys = ['lines', 'syllables', 'essence']
    for key in required_keys:
        if key not in haiku_data:
            raise ValueError(f"Missing required key in response: {key}")

    lines = haiku_data['lines']
    syllables = haiku_data['syllables']

    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    if len(syllables) != 3:
        raise ValueError(f"Expected 3 syllable counts, got {len(syllables)}")

    # Check if syllables match 5-7-5
    valid = syllables == [5, 7, 5]

    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllables': syllables,
        'essence': haiku_data['essence'],
        'valid': valid
    }