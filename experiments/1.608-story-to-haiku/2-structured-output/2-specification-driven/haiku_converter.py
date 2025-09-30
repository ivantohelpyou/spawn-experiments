"""
Story-to-Haiku Converter with JSON Structured Output
Method 2: Specification-Driven Implementation
Run 2: Structured Output

This module converts narrative text into haiku poetry using Ollama LLM
with JSON-structured output where the LLM self-reports syllable counts.
"""

import json
from typing import Optional, Dict, List, Any


# Constants
MAX_INPUT_LENGTH = 500
REQUIRED_JSON_KEYS = ['lines', 'syllables', 'essence']
EXPECTED_LINE_COUNT = 3
EXPECTED_SYLLABLE_COUNT = 3
TARGET_SYLLABLE_PATTERN = [5, 7, 5]


def story_to_haiku(text: str, llm_client: Optional[Any] = None) -> Dict[str, Any]:
    """
    Convert a story or text into a haiku poem using LLM with JSON output.

    This function uses structured JSON output where the LLM self-reports
    syllable counts, eliminating unreliable Python syllable counting.

    Args:
        text: Input story or paragraph to convert.
              Must be non-empty after stripping whitespace.
              Will be truncated to 500 characters for LLM processing.

        llm_client: LLM client with generate() method.
                   If None, uses ollama module.
                   For testing, pass a mock object.

    Returns:
        dict: Structured haiku result containing:
            - haiku (str): Complete haiku with newline separators
            - lines (list[str]): Three haiku lines as separate strings
            - syllables (list[int]): LLM-reported syllable counts
            - essence (str): Core theme extracted from original text
            - valid (bool): Whether syllables match [5, 7, 5]

    Raises:
        ValueError: If input text is empty or whitespace-only
        ValueError: If JSON response is malformed
        ValueError: If required JSON keys are missing
        ValueError: If line/syllable counts don't match expected structure
        RuntimeError: If LLM generation fails

    Example:
        >>> result = story_to_haiku("A tale of mountains and time...")
        >>> print(result['haiku'])
        Mountains stand timeless
        Ancient peaks touch clouded sky
        Stories carved in stone

        >>> result['syllables']
        [5, 7, 5]
        >>> result['valid']
        True
    """
    # Step 1: Input Validation
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty or whitespace-only")

    # Step 2: LLM Client Resolution
    if llm_client is None:
        import ollama
        llm_client = ollama

    # Step 3: Prepare Input
    truncated_text = text[:MAX_INPUT_LENGTH] if len(text) > MAX_INPUT_LENGTH else text
    truncated_text = truncated_text.strip()

    # Step 4: Generate JSON Prompt
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Story: {truncated_text}
"""

    # Step 5: Invoke LLM
    try:
        response = llm_client.generate(
            model='llama3.2',
            prompt=prompt
        )
    except Exception as e:
        raise RuntimeError(f"LLM generation failed: {str(e)}") from e

    # Step 6: Parse JSON Response
    raw_response = response['response'].strip()
    haiku_data = _parse_json_response(raw_response)

    # Step 7: Validate JSON Structure
    _validate_json_structure(haiku_data)

    # Step 8: Check Syllable Validity
    valid = haiku_data['syllables'] == TARGET_SYLLABLE_PATTERN

    # Step 9: Assemble Result
    result = {
        'haiku': '\n'.join(haiku_data['lines']),
        'lines': haiku_data['lines'],
        'syllables': haiku_data['syllables'],
        'essence': haiku_data['essence'],
        'valid': valid
    }

    return result


def _parse_json_response(raw_response: str) -> Dict[str, Any]:
    """
    Parse JSON from LLM response with comprehensive error handling.

    Handles common issues:
    - Extra whitespace
    - Invalid JSON syntax
    - Malformed responses

    Args:
        raw_response: Raw string from LLM

    Returns:
        Parsed JSON dict

    Raises:
        ValueError: If JSON is invalid
    """
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        # Provide helpful error message with context
        preview = raw_response[:200] if len(raw_response) > 200 else raw_response
        raise ValueError(
            f"Invalid JSON response from LLM: {e}\n"
            f"Raw response (first 200 chars): {preview}"
        )

    return data


def _validate_json_structure(data: Dict[str, Any]) -> None:
    """
    Validate JSON structure matches expected schema.

    Checks:
    - Required keys present
    - Correct number of lines
    - Correct number of syllable counts
    - Correct data types

    Args:
        data: Parsed JSON dict

    Raises:
        ValueError: If structure is invalid
    """
    # Check required keys
    missing_keys = [key for key in REQUIRED_JSON_KEYS if key not in data]
    if missing_keys:
        raise ValueError(
            f"Missing required keys in JSON response: {missing_keys}. "
            f"Expected keys: {REQUIRED_JSON_KEYS}, got: {list(data.keys())}"
        )

    # Validate 'lines' field
    lines = data['lines']
    if not isinstance(lines, list):
        raise ValueError(
            f"'lines' must be a list, got {type(lines).__name__}"
        )

    if len(lines) != EXPECTED_LINE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_LINE_COUNT} lines in JSON response, "
            f"got {len(lines)}: {lines}"
        )

    if not all(isinstance(line, str) for line in lines):
        raise ValueError(
            "All lines must be strings. "
            f"Got types: {[type(line).__name__ for line in lines]}"
        )

    # Validate 'syllables' field
    syllables = data['syllables']
    if not isinstance(syllables, list):
        raise ValueError(
            f"'syllables' must be a list, got {type(syllables).__name__}"
        )

    if len(syllables) != EXPECTED_SYLLABLE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_SYLLABLE_COUNT} syllable counts in JSON response, "
            f"got {len(syllables)}: {syllables}"
        )

    if not all(isinstance(count, int) for count in syllables):
        raise ValueError(
            "All syllable counts must be integers. "
            f"Got types: {[type(count).__name__ for count in syllables]}"
        )

    # Validate 'essence' field
    essence = data['essence']
    if not isinstance(essence, str):
        raise ValueError(
            f"'essence' must be a string, got {type(essence).__name__}"
        )

    if not essence.strip():
        raise ValueError("'essence' cannot be empty or whitespace-only")


# Module-level docstring and exports
__all__ = ['story_to_haiku']