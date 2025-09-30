"""
Story-to-Haiku Converter using Ollama with optimized prompts.

Method 4: Adaptive/Validated TDD
- Test-first approach with validation cycles
- Comprehensive error handling
- Optimized prompt engineering for better syllable accuracy
"""

import json
import re
from typing import Optional
import ollama


def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem using optimized prompts.

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
        ValueError: If input is invalid or LLM response cannot be parsed
    """
    # Validate input
    if text is None or not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use provided client or default to Ollama
    client = llm_client if llm_client is not None else ollama

    # Create optimized prompt with explicit syllable instructions
    prompt = _create_optimized_prompt(text)

    # Call LLM
    response = client.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract and parse JSON response
    response_text = response.message.content
    haiku_data = _parse_json_response(response_text)

    # Validate structure
    _validate_haiku_structure(haiku_data)

    # Build return dictionary
    result = {
        "haiku": "\n".join(haiku_data["lines"]),
        "lines": haiku_data["lines"],
        "syllables": haiku_data["syllables"],
        "essence": haiku_data["essence"],
        "valid": _validate_syllable_counts(haiku_data["syllables"])
    }

    return result


def _create_optimized_prompt(text: str) -> str:
    """
    Create optimized prompt with explicit syllable counting instructions.

    This prompt is designed to improve haiku quality through:
    1. Clear syllable counting rules
    2. Example with syllable breakdown
    3. Structured JSON output format
    4. Guidance on essence extraction
    """
    prompt = f"""You are a skilled haiku poet. Convert the following story into a traditional haiku.

STORY:
{text}

HAIKU STRUCTURE RULES:
- Line 1: Exactly 5 syllables
- Line 2: Exactly 7 syllables
- Line 3: Exactly 5 syllables
- Capture the essence of the story in a single vivid moment

SYLLABLE COUNTING:
- Count each syllable carefully (e.g., "beautiful" = beau-ti-ful = 3 syllables)
- Verify your counts before finalizing
- Each line MUST have the exact syllable count specified

EXAMPLE FORMAT:
Story: "On a foggy morning, an old fisherman cast his net into the sea"
Haiku:
{{
  "lines": [
    "Fog wraps the shoreline",
    "Old hands cast nets through the mist",
    "Sea holds its secrets"
  ],
  "syllables": [5, 7, 5],
  "essence": "The timeless ritual of fishing in mysterious morning fog"
}}

Now create your haiku, returning ONLY valid JSON in the format above."""

    return prompt


def _parse_json_response(response_text: str) -> dict:
    """
    Parse JSON from LLM response, handling extra text.

    Args:
        response_text: Raw response from LLM

    Returns:
        Parsed JSON dictionary

    Raises:
        ValueError: If JSON cannot be parsed
    """
    # Try to parse directly first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from text
    # Look for content between curly braces
    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # If still fails, raise error
    raise ValueError(f"Failed to parse JSON from response: {response_text[:200]}")


def _validate_haiku_structure(haiku_data: dict) -> None:
    """
    Validate that haiku data has all required keys and correct structure.

    Args:
        haiku_data: Parsed haiku dictionary

    Raises:
        ValueError: If structure is invalid
    """
    # Check required keys
    required_keys = ["lines", "syllables", "essence"]
    for key in required_keys:
        if key not in haiku_data:
            raise ValueError(f"Missing required key: {key}")

    # Validate lines
    if not isinstance(haiku_data["lines"], list):
        raise ValueError("'lines' must be a list")

    if len(haiku_data["lines"]) != 3:
        raise ValueError(f"Expected 3 lines, got {len(haiku_data['lines'])}")

    # Validate syllables
    if not isinstance(haiku_data["syllables"], list):
        raise ValueError("'syllables' must be a list")

    if len(haiku_data["syllables"]) != 3:
        raise ValueError(f"Expected 3 syllable counts, got {len(haiku_data['syllables'])}")

    # Validate essence
    if not isinstance(haiku_data["essence"], str):
        raise ValueError("'essence' must be a string")


def _validate_syllable_counts(syllables: list[int]) -> bool:
    """
    Check if syllable counts match the 5-7-5 pattern.

    Args:
        syllables: List of syllable counts

    Returns:
        True if pattern is [5, 7, 5], False otherwise
    """
    return syllables == [5, 7, 5]
