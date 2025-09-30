"""
Story-to-Haiku Converter
Method 2: Specification-Driven Development
Experiment 1.608 - Run 4 (Optimized Prompts)

This module provides a function to convert stories into haiku poems using
Ollama LLM integration with optimized prompt engineering for improved quality.

Key Features:
- Enhanced prompt templates with explicit syllable counting
- Comprehensive error handling and validation
- Dependency injection for testing
- Production-ready code quality
- Detailed documentation and type hints
"""

import json
from typing import Optional, Any, Dict


def story_to_haiku(text: str, llm_client: Optional[Any] = None) -> Dict[str, Any]:
    """
    Convert a story or text into a haiku poem using optimized prompts.

    This function uses Ollama (llama3.2) with enhanced prompt engineering
    to generate high-quality haiku poems that capture the essence of input
    stories while adhering to traditional 5-7-5 syllable structure.

    The optimized prompt includes:
    - Explicit syllable counting instructions with examples
    - Clear structural rules (5-7-5 format)
    - Guidance on capturing story essence
    - Concrete example haiku with proper format
    - JSON output specification

    Args:
        text: Input story or paragraph to convert into haiku.
              Must be non-empty string with meaningful content.
        llm_client: Optional LLM client for dependency injection.
                   If None, creates real Ollama client.
                   Used for testing with mocks.

    Returns:
        dict: Structured haiku result with keys:
            - haiku (str): Complete haiku with newline separators
            - lines (list[str]): Three individual haiku lines
            - syllables (list[int]): LLM-reported syllable counts
            - essence (str): Captured theme or core idea
            - valid (bool): True if syllables match [5, 7, 5]

        On error, returns dict with 'error' key and empty values:
            - error (str): Error description
            - haiku (str): Empty string
            - lines (list): Empty list
            - syllables (list): Empty list
            - essence (str): Empty string
            - valid (bool): False

    Raises:
        Exception: If Ollama communication fails (connection errors, timeouts, etc.)

    Examples:
        >>> result = story_to_haiku("A bird flew across the sky")
        >>> print(result['haiku'])
        Wings slice through blue air
        Feathered freedom gliding high
        Sky holds its secrets

        >>> result['valid']
        True

        >>> result = story_to_haiku("")
        >>> 'error' in result
        True
    """
    # Step 1: Input Validation
    validation_error = _validate_input(text)
    if validation_error:
        return _create_error_response(validation_error)

    # Step 2: Initialize LLM Client (with dependency injection support)
    if llm_client is None:
        try:
            import ollama
            llm_client = ollama
        except ImportError as e:
            return _create_error_response(
                f"Failed to import ollama module: {e}. "
                "Please ensure ollama is installed: pip install ollama==0.1.6"
            )

    # Step 3: Build Optimized Prompt
    prompt = _build_optimized_prompt(text)

    # Step 4: Call LLM
    try:
        response = llm_client.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
    except Exception as e:
        raise Exception(f"Ollama communication failed: {e}")

    # Step 5: Parse JSON Response
    llm_content = response['message']['content']
    parsed_data, parse_error = _parse_json_response(llm_content)

    if parse_error:
        return _create_error_response(parse_error)

    # Step 6: Validate Structure
    validation_error = _validate_json_structure(parsed_data)
    if validation_error:
        return _create_error_response(validation_error)

    # Step 7: Extract and Validate Syllables
    lines = parsed_data['lines']
    syllables = parsed_data['syllables']
    essence = parsed_data['essence']

    is_valid = _validate_syllable_structure(syllables)

    # Step 8: Assemble Result
    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllables': syllables,
        'essence': essence,
        'valid': is_valid
    }


def _validate_input(text: str) -> Optional[str]:
    """
    Validate input text.

    Args:
        text: Input text to validate

    Returns:
        Optional[str]: Error message if validation fails, None if valid
    """
    if text is None:
        return "Input text cannot be None"

    if not isinstance(text, str):
        return f"Input text must be a string, got {type(text).__name__}"

    if not text.strip():
        return "Input text cannot be empty or whitespace-only"

    return None


def _build_optimized_prompt(text: str) -> str:
    """
    Build optimized prompt with explicit syllable counting and clear examples.

    This is the key enhancement in Run 4 - a carefully crafted prompt that:
    - Provides explicit syllable counting instructions
    - Shows concrete examples with syllable breakdown
    - Guides essence extraction
    - Specifies exact JSON output format

    Args:
        text: Story text to convert

    Returns:
        str: Complete optimized prompt
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


def _parse_json_response(content: str) -> tuple[Optional[Dict], Optional[str]]:
    """
    Parse JSON response from LLM.

    Args:
        content: Raw response content from LLM

    Returns:
        tuple: (parsed_dict, error_message)
               parsed_dict is None if parsing fails
               error_message is None if parsing succeeds
    """
    try:
        data = json.loads(content)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Failed to parse JSON response: {e}. Response content: {content[:200]}"


def _validate_json_structure(data: Dict) -> Optional[str]:
    """
    Validate that parsed JSON has all required keys and correct types.

    Args:
        data: Parsed JSON data

    Returns:
        Optional[str]: Error message if validation fails, None if valid
    """
    required_keys = ['lines', 'syllables', 'essence']

    # Check for missing keys
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return f"Missing required keys in JSON response: {missing_keys}"

    # Validate 'lines' structure
    lines = data['lines']
    if not isinstance(lines, list):
        return f"'lines' must be a list, got {type(lines).__name__}"

    if len(lines) != 3:
        return f"'lines' must contain exactly 3 elements, got {len(lines)}"

    if not all(isinstance(line, str) for line in lines):
        return "'lines' must contain only strings"

    if any(not line.strip() for line in lines):
        return "'lines' cannot contain empty strings"

    # Validate 'syllables' structure
    syllables = data['syllables']
    if not isinstance(syllables, list):
        return f"'syllables' must be a list, got {type(syllables).__name__}"

    if len(syllables) != 3:
        return f"'syllables' must contain exactly 3 elements, got {len(syllables)}"

    if not all(isinstance(s, int) for s in syllables):
        return "'syllables' must contain only integers"

    if any(s <= 0 for s in syllables):
        return "'syllables' must contain only positive integers"

    # Validate 'essence' structure
    essence = data['essence']
    if not isinstance(essence, str):
        return f"'essence' must be a string, got {type(essence).__name__}"

    if not essence.strip():
        return "'essence' cannot be empty"

    return None


def _validate_syllable_structure(syllables: list[int]) -> bool:
    """
    Validate that syllable counts match traditional 5-7-5 haiku structure.

    Args:
        syllables: List of syllable counts from LLM

    Returns:
        bool: True if syllables are [5, 7, 5], False otherwise
    """
    return syllables == [5, 7, 5]


def _create_error_response(error_message: str) -> Dict[str, Any]:
    """
    Create standardized error response dictionary.

    Args:
        error_message: Description of the error

    Returns:
        dict: Error response with all required keys
    """
    return {
        'error': error_message,
        'haiku': '',
        'lines': [],
        'syllables': [],
        'essence': '',
        'valid': False
    }


# ============================================================================
# Module-level documentation and metadata
# ============================================================================

__version__ = "1.0.0"
__author__ = "Method 2 (Specification-Driven)"
__description__ = "Story-to-haiku converter with optimized prompt engineering"

# Design Principles (Method 2 - Specification-Driven):
# 1. Comprehensive planning before implementation (see docs/technical-spec.md)
# 2. Detailed documentation and inline comments
# 3. Explicit error handling for all edge cases
# 4. Type hints throughout for clarity
# 5. Modular design with helper functions
# 6. Production-ready code quality
# 7. Optimized prompt engineering as core innovation

# Key Innovation for Run 4:
# Enhanced prompt template with:
# - Explicit syllable counting instructions
# - Concrete example haiku with syllable breakdown
# - Clear guidance on capturing story essence
# - Structured JSON format specification
#
# Hypothesis: Better prompts lead to better haiku quality across all metrics
