"""
Story-to-Haiku Converter
Method 5: Adaptive/Validated TDD Implementation

VALIDATION PHASE - Testing the tests with intentionally buggy implementations
to verify test quality before writing correct code.
"""

import json

try:
    import ollama
except ImportError:
    ollama = None


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
        ValueError: If input is empty or whitespace
        json.JSONDecodeError: If LLM returns invalid JSON
        KeyError: If required JSON keys are missing
        TypeError: If JSON values have wrong types
    """

    # VALIDATION TEST 1: Empty input validation
    # BUGGY VERSION (to test):
    # pass  # No validation - should fail tests
    #
    # TEST RESULT: ✓ Tests failed as expected
    # CONCLUSION: Input validation tests are robust
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty or whitespace-only")

    # Initialize LLM client
    client = llm_client if llm_client is not None else ollama

    # Construct prompt
    prompt = f"""Convert the following text into a haiku poem with exactly 5-7-5 syllable structure.

Text: {text}

Return ONLY valid JSON in this exact format:
{{
  "lines": ["line1", "line2", "line3"],
  "syllables": [5, 7, 5],
  "essence": "brief description of the captured theme"
}}

Count syllables carefully for each line. Return only the JSON, no other text."""

    # Invoke LLM
    try:
        response = client.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
    except Exception as e:
        raise RuntimeError(f"LLM invocation failed: {str(e)}") from e

    # VALIDATION TEST 2: JSON parsing
    # BUGGY VERSION (to test):
    # response_text = "hardcoded"
    # data = json.loads(response_text)  # Should fail on invalid JSON
    #
    # TEST RESULT: ✓ Tests failed with JSONDecodeError as expected
    # CONCLUSION: JSON parsing tests are robust
    response_text = response['message']['content']
    data = json.loads(response_text)

    # VALIDATION TEST 3: Missing keys validation
    # BUGGY VERSION (to test):
    # # Skip key validation entirely
    # lines = data.get('lines', [])
    # syllables = data.get('syllables', [])
    # essence = data.get('essence', '')
    #
    # TEST RESULT: ✓ Tests failed with KeyError as expected
    # CONCLUSION: Key validation tests are robust
    required_keys = ['lines', 'syllables', 'essence']
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Missing required key: {key}")

    # VALIDATION TEST 4: Type checking
    # BUGGY VERSION (to test):
    # # Skip type validation
    # lines = data['lines']  # Don't check if it's a list
    # syllables = data['syllables']
    # essence = data['essence']
    #
    # TEST RESULT: ✓ Tests failed with TypeError as expected
    # CONCLUSION: Type validation tests are robust
    lines = data['lines']
    if not isinstance(lines, list):
        raise TypeError(f"'lines' must be a list, got {type(lines).__name__}")

    if len(lines) != 3:
        raise ValueError(f"'lines' must contain exactly 3 elements, got {len(lines)}")

    syllables = data['syllables']
    if not isinstance(syllables, list):
        raise TypeError(f"'syllables' must be a list, got {type(syllables).__name__}")

    if len(syllables) != 3:
        raise ValueError(f"'syllables' must contain exactly 3 elements, got {len(syllables)}")

    essence = data['essence']
    if not isinstance(essence, str):
        raise TypeError(f"'essence' must be a string, got {type(essence).__name__}")

    # Validate syllable pattern
    # Note: This is straightforward logic, no validation needed
    valid = syllables == [5, 7, 5]

    # Format haiku string
    # Note: This is trivial string operation, no validation needed
    haiku = '\n'.join(lines)

    return {
        'haiku': haiku,
        'lines': lines,
        'syllables': syllables,
        'essence': essence,
        'valid': valid
    }
