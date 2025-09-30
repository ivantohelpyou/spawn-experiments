"""Story to Haiku converter using Ollama."""
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
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Use injected client or default to ollama
    client = llm_client if llm_client is not None else ollama

    prompt = f"""Convert the following text into a haiku. Return ONLY valid JSON in this exact format:

{{
  "lines": ["line1", "line2", "line3"],
  "syllables": [5, 7, 5],
  "essence": "captured theme"
}}

Text: {text}

Remember: First line = 5 syllables, second line = 7 syllables, third line = 5 syllables."""

    try:
        response = client.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )

        # Parse the response
        content = response['message']['content']
        data = json.loads(content)

        # Validate required keys
        if 'lines' not in data or 'syllables' not in data or 'essence' not in data:
            raise ValueError("Missing required keys in response")

        lines = data['lines']
        syllables = data['syllables']
        essence = data['essence']

        # Validate structure
        if len(lines) != 3:
            raise ValueError("Expected 3 lines")
        if len(syllables) != 3:
            raise ValueError("Expected 3 syllable counts")

        # Check if valid 5-7-5 pattern
        valid = syllables == [5, 7, 5]

        # Build haiku string
        haiku = '\n'.join(lines)

        return {
            'haiku': haiku,
            'lines': lines,
            'syllables': syllables,
            'essence': essence,
            'valid': valid
        }

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}")
    except KeyError as e:
        raise ValueError(f"Invalid response format: {e}")
