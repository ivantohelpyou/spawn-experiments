"""
Story-to-Haiku Converter
Method 2: Specification-Driven Implementation

Converts text into haiku poems using Ollama's llama3.2 model with JSON structured output.
The LLM self-reports syllable counts, eliminating need for Python syllable counting.
"""

import json
from typing import Optional

# Import ollama if available (optional for testing with mocks)
try:
    import ollama
except ImportError:
    ollama = None


def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem.

    This function uses Ollama with llama3.2 to generate a haiku from input text.
    The LLM provides structured JSON output including syllable counts, eliminating
    the need for Python-based syllable counting libraries.

    Args:
        text: Input story or paragraph (non-empty string)
        llm_client: Optional LLM client for dependency injection.
                   If None, creates default Ollama client.

    Returns:
        dict containing:
            - haiku: str - Complete haiku with newlines
            - lines: list[str] - Three haiku lines
            - syllables: list[int] - LLM-reported counts [5, 7, 5]
            - essence: str - Captured theme/idea
            - valid: bool - Whether syllables match [5, 7, 5]

    Raises:
        ValueError: If text is empty or whitespace-only
        RuntimeError: If LLM invocation fails
        json.JSONDecodeError: If LLM response is not valid JSON
        KeyError: If required JSON keys are missing
        TypeError: If JSON structure types are incorrect

    Example:
        >>> result = story_to_haiku("The old pond, a frog jumps in, water's sound.")
        >>> print(result['haiku'])
        >>> print(f"Valid 5-7-5: {result['valid']}")
    """

    # Step 1: Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty or whitespace-only")

    # Step 2: Initialize LLM client (use injected client or create default)
    client = llm_client if llm_client is not None else ollama

    # Step 3: Construct prompt with clear JSON format instructions
    prompt = f"""Convert the following text into a haiku poem with exactly 5-7-5 syllable structure.

Text: {text}

Return ONLY valid JSON in this exact format:
{{
  "lines": ["line1", "line2", "line3"],
  "syllables": [5, 7, 5],
  "essence": "brief description of the captured theme"
}}

Count syllables carefully for each line. Return only the JSON, no other text."""

    # Step 4: Invoke LLM with JSON format specification
    try:
        response = client.chat(
            model='llama3.2',
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            format='json'  # Ensure JSON output
        )
    except Exception as e:
        raise RuntimeError(f"LLM invocation failed: {str(e)}") from e

    # Step 5: Extract and parse JSON response
    try:
        response_text = response.message['content']
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Failed to parse LLM response as JSON. Response was: {response_text}",
            e.doc,
            e.pos
        ) from e
    except KeyError as e:
        raise RuntimeError(f"Unexpected response structure from LLM: {response}") from e

    # Step 6: Validate JSON structure and required keys
    required_keys = ['lines', 'syllables', 'essence']
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise KeyError(f"Missing required keys in JSON response: {missing_keys}. Got: {list(data.keys())}")

    # Validate types and structure
    if not isinstance(data['lines'], list):
        raise TypeError(f"'lines' must be a list, got {type(data['lines']).__name__}")

    if len(data['lines']) != 3:
        raise ValueError(f"'lines' must contain exactly 3 elements, got {len(data['lines'])}")

    if not all(isinstance(line, str) for line in data['lines']):
        raise TypeError("All elements in 'lines' must be strings")

    if not isinstance(data['syllables'], list):
        raise TypeError(f"'syllables' must be a list, got {type(data['syllables']).__name__}")

    if len(data['syllables']) != 3:
        raise ValueError(f"'syllables' must contain exactly 3 elements, got {len(data['syllables'])}")

    if not all(isinstance(count, int) for count in data['syllables']):
        raise TypeError("All elements in 'syllables' must be integers")

    if not isinstance(data['essence'], str):
        raise TypeError(f"'essence' must be a string, got {type(data['essence']).__name__}")

    if not data['essence'].strip():
        raise ValueError("'essence' cannot be empty or whitespace-only")

    # Step 7: Validate syllable pattern (5-7-5)
    is_valid = data['syllables'] == [5, 7, 5]

    # Step 8: Construct response with all required fields
    lines = data['lines']
    haiku_text = '\n'.join(lines)

    return {
        'haiku': haiku_text,
        'lines': lines,
        'syllables': data['syllables'],
        'essence': data['essence'],
        'valid': is_valid
    }
