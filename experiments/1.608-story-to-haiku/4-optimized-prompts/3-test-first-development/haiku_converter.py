"""
Story to Haiku Converter - Method 3: Pure TDD / Test-First Development

Implementation created AFTER tests were written, following TDD principles.
Focus: Clean, minimal code that makes tests pass.

Run 4: Using optimized prompts with explicit syllable counting instructions.
"""

import json
import ollama


def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem using optimized prompts.

    This implementation follows Test-Driven Development (TDD):
    - Tests were written first to define expected behavior
    - Implementation written to satisfy test requirements
    - Clean, minimal code with no unnecessary complexity

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
        ValueError: If input is empty, JSON is malformed, or structure is invalid
    """
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use provided client or create real Ollama client
    client = llm_client if llm_client is not None else ollama

    # Build optimized prompt with explicit syllable instructions
    prompt = _build_optimized_prompt(text)

    # Call LLM with JSON format
    response = client.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}],
        format='json'
    )

    # Extract response content
    response_text = response.message['content']

    # Parse JSON response
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")

    # Validate required keys
    required_keys = {'lines', 'syllables', 'essence'}
    if not required_keys.issubset(data.keys()):
        missing = required_keys - data.keys()
        raise ValueError(f"Missing required keys in LLM response: {missing}")

    # Validate structure
    lines = data['lines']
    syllables = data['syllables']

    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines in haiku, got {len(lines)}")

    if len(syllables) != 3:
        raise ValueError(f"Expected 3 syllable counts, got {len(syllables)}")

    # Validate syllable pattern (5-7-5)
    valid = syllables == [5, 7, 5]

    # Format haiku as string with newlines
    haiku_text = '\n'.join(lines)

    # Return structured result
    return {
        'haiku': haiku_text,
        'lines': lines,
        'syllables': syllables,
        'essence': data['essence'],
        'valid': valid
    }


def _build_optimized_prompt(text: str) -> str:
    """
    Build an optimized prompt with explicit syllable counting instructions.

    This is a Run 4 enhancement - refined prompt engineering to improve
    haiku quality through clearer instructions.

    Key optimizations:
    - Explicit syllable counting instructions for each line
    - Clear example with syllable breakdown
    - Guidance on essence extraction
    - Structured JSON format specification

    Args:
        text: The story text to convert

    Returns:
        Optimized prompt string
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
- First line must have exactly 5 syllables
- Second line must have exactly 7 syllables
- Third line must have exactly 5 syllables

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

ESSENCE EXTRACTION:
- Identify the core emotion, theme, or image from the story
- Distill the story's essence into a single vivid moment or feeling
- Capture what makes this story meaningful

Now create your haiku, returning ONLY valid JSON in the format above."""

    return prompt
