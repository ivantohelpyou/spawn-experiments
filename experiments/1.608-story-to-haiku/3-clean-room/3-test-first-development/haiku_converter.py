"""
Story to Haiku Converter
Converts text into haiku using Ollama LLM with structured JSON output.
"""

import json
from typing import Optional


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

    # Handle empty input
    if not text or not text.strip():
        return {
            'haiku': '',
            'lines': [],
            'syllables': [],
            'essence': '',
            'valid': False,
            'error': 'Empty input text'
        }

    # Create prompt for LLM
    prompt = f"""Convert the following text into a haiku (5-7-5 syllable structure).

Text: {text}

Return your response as JSON in this exact format:
{{
  "lines": ["first line", "second line", "third line"],
  "syllables": [5, 7, 5],
  "essence": "the captured theme or idea"
}}

Count syllables carefully and report the actual counts. The haiku should follow the traditional 5-7-5 syllable pattern."""

    # Use real Ollama client if none provided
    if llm_client is None:
        try:
            import ollama
            llm_client = ollama
        except ImportError:
            return {
                'haiku': '',
                'lines': [],
                'syllables': [],
                'essence': '',
                'valid': False,
                'error': 'Ollama not available'
            }

    # Call LLM
    try:
        response = llm_client.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            format='json'
        )

        # Extract JSON content
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
                'error': 'Invalid JSON response from LLM'
            }

        # Validate required keys
        required_keys = ['lines', 'syllables', 'essence']
        if not all(key in data for key in required_keys):
            return {
                'haiku': '',
                'lines': data.get('lines', []),
                'syllables': data.get('syllables', []),
                'essence': data.get('essence', ''),
                'valid': False,
                'error': 'Missing required JSON keys'
            }

        # Extract data
        lines = data['lines']
        syllables = data['syllables']
        essence = data['essence']

        # Validate syllable pattern
        valid = syllables == [5, 7, 5]

        # Create haiku string
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
            'error': f'Error calling LLM: {str(e)}'
        }
