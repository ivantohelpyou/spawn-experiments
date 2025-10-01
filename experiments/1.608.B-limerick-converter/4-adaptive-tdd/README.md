# Limerick Converter - Adaptive TDD Implementation

Convert prose stories into limericks using llama3.2 via Ollama. Built with Adaptive Test-Driven Development methodology.

## Features

- Converts prose stories to limericks (5-line poems with AABBA rhyme scheme)
- Validates limerick structure (syllable counts and rhyme scheme)
- Returns JSON output with validation results
- Comprehensive test suite with adaptive validation cycles

## Requirements

- Python 3.8+
- Ollama running locally with llama3.2 model
- Dependencies listed in `requirements.txt`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Ollama is running:
```bash
ollama serve
```

3. Pull llama3.2 model if not already available:
```bash
ollama pull llama3.2
```

## Usage

### Basic Usage

```python
from limerick_converter import LimerickConverter

# Create converter
converter = LimerickConverter()

# Convert a story
story = """
A programmer stayed up all night debugging their code.
They finally found the bug - a missing semicolon.
Relieved, they went to sleep.
"""

result = converter.convert(story)
print(result)
```

### Output Format

The converter returns JSON with the following structure:

```json
{
  "limerick": {
    "text": "Full limerick as text",
    "lines": ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
  },
  "story": "Original story",
  "validation": {
    "valid": true,
    "errors": [],
    "syllable_counts": [9, 8, 5, 6, 9]
  }
}
```

### Custom Model

```python
converter = LimerickConverter(model_name="llama3.1")
```

## Limerick Structure

A valid limerick must have:
- Exactly 5 lines
- AABBA rhyme scheme (lines 1, 2, 5 rhyme; lines 3, 4 rhyme)
- Syllable counts:
  - Lines 1, 2, 5: 8-9 syllables
  - Lines 3, 4: 5-6 syllables
- Anapestic meter (da-da-DUM rhythm)

## Development

### Running Tests

```bash
pytest test_limerick_converter.py -v
```

### Test Coverage

The test suite includes:
- Input validation tests
- Syllable counting tests (with validation cycles)
- Rhyme detection tests (with validation cycles)
- Limerick structure validation tests (with validation cycles)
- Integration tests for the converter

### Adaptive TDD Methodology

This implementation was built using Adaptive TDD:

1. **RED**: Write failing tests for all functionality
2. **VALIDATE** (Adaptive): For complex logic, write intentionally buggy implementations to verify tests catch bugs
3. **GREEN**: Implement correct functionality after validation
4. **REFACTOR**: Clean up code while maintaining passing tests

Validation cycles were performed for:
- Syllable counting algorithm
- Rhyme detection logic
- Limerick structure validation
- Input validation

## API Reference

### `validate_story_input(story: str) -> str`
Validates and cleans input story.

### `count_syllables(text: str) -> int`
Counts syllables in text, handling silent 'e' and consecutive vowels.

### `extract_rhyme_sounds(text: str) -> str`
Extracts rhyme sound from text (last word's ending).

### `check_rhyme_scheme(text1: str, text2: str) -> bool`
Checks if two texts rhyme (case-insensitive).

### `validate_limerick_structure(lines: List[str]) -> Dict[str, Any]`
Validates limerick structure (line count, syllables, rhyme scheme).

### `LimerickConverter.convert(story: str) -> str`
Converts story to limerick, returns JSON string.

## License

MIT
