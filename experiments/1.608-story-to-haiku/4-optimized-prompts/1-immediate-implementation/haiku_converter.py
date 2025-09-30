"""
Story to Haiku Converter - Method 1: Immediate Implementation
Uses optimized prompt engineering for improved haiku quality.
"""

import json
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
    """
    # Handle edge case: empty input
    if not text or not text.strip():
        return {
            "haiku": "",
            "lines": [],
            "syllables": [],
            "essence": "",
            "valid": False
        }

    # Optimized prompt with explicit syllable counting instructions
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

    # Use injected client for testing, or real Ollama
    if llm_client:
        response = llm_client.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        content = response['message']['content']
    else:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        content = response['message']['content']

    # Parse JSON response
    try:
        # Extract JSON from response (handle cases where LLM adds extra text)
        json_start = content.find('{')
        json_end = content.rfind('}') + 1

        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON found in response")

        json_str = content[json_start:json_end]
        parsed = json.loads(json_str)

        # Validate required keys
        required_keys = ['lines', 'syllables', 'essence']
        for key in required_keys:
            if key not in parsed:
                raise KeyError(f"Missing required key: {key}")

        # Extract and validate data
        lines = parsed['lines']
        syllables = parsed['syllables']
        essence = parsed['essence']

        # Validate structure
        if not isinstance(lines, list) or len(lines) != 3:
            raise ValueError("Lines must be a list of 3 strings")

        if not isinstance(syllables, list) or len(syllables) != 3:
            raise ValueError("Syllables must be a list of 3 integers")

        # Check if syllables match 5-7-5 pattern
        valid = syllables == [5, 7, 5]

        # Construct complete haiku
        haiku = '\n'.join(lines)

        return {
            "haiku": haiku,
            "lines": lines,
            "syllables": syllables,
            "essence": essence,
            "valid": valid
        }

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Handle malformed JSON or missing keys
        return {
            "haiku": "",
            "lines": [],
            "syllables": [],
            "essence": f"Error parsing response: {str(e)}",
            "valid": False
        }
