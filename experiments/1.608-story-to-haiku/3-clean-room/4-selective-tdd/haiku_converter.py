"""
Story to Haiku converter using Ollama with structured JSON output.

Implementation: Adaptive TDD approach
- Direct implementation for simple Ollama setup
- Test-driven for critical JSON parsing and validation
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
    """
    # Use injected client or default to Ollama
    client = llm_client or ollama

    # Construct prompt for structured JSON output
    prompt = f"""Convert the following text into a haiku poem (5-7-5 syllable structure).

Text: {text}

You must respond with ONLY valid JSON in this exact format:
{{
  "lines": ["first line", "second line", "third line"],
  "syllables": [5, 7, 5],
  "essence": "brief description of the captured theme"
}}

Count syllables carefully. Return ONLY the JSON, no other text."""

    try:
        # Call LLM
        response = client.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )

        # Extract content
        content = response['message']['content']

        # Parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return {
                'haiku': '',
                'lines': [],
                'syllables': [],
                'essence': '',
                'valid': False,
                'error': 'Failed to parse JSON response'
            }

        # Validate required keys
        required_keys = ['lines', 'syllables', 'essence']
        if not all(key in data for key in required_keys):
            return {
                'haiku': '',
                'lines': [],
                'syllables': [],
                'essence': '',
                'valid': False,
                'error': 'Missing required keys in JSON'
            }

        # Extract data
        lines = data['lines']
        syllables = data['syllables']
        essence = data['essence']

        # Validate syllable pattern (5-7-5)
        valid = (
            isinstance(syllables, list) and
            len(syllables) == 3 and
            syllables == [5, 7, 5]
        )

        # Format haiku string
        haiku = '\n'.join(lines)

        return {
            'haiku': haiku,
            'lines': lines,
            'syllables': syllables,
            'essence': essence,
            'valid': valid
        }

    except Exception as e:
        return {
            'haiku': '',
            'lines': [],
            'syllables': [],
            'essence': '',
            'valid': False,
            'error': f'Error: {str(e)}'
        }
