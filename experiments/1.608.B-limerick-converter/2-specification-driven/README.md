# Story-to-Limerick Converter

## Method 2: Specification-Driven Implementation

A Python-based converter that transforms prose stories into limericks using llama3.2 via Ollama.

## Overview

This implementation follows a **specification-driven development** approach:
1. Create comprehensive technical specifications first
2. Human review/approval of specifications
3. Implement against approved specifications with quality discipline

## Features

- Converts 1-3 paragraph stories into valid 5-line limericks
- Validates AABBA rhyme scheme automatically
- Checks syllable counts (lines 1,2,5: 8-9 syllables; lines 3,4: 5-6 syllables)
- Returns structured JSON output with validation results
- Handles retries for malformed LLM output
- Comprehensive error handling

## Requirements

- Python 3.8+
- Ollama installed and running locally
- llama3.2 model pulled (`ollama pull llama3.2`)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running
ollama serve

# Pull llama3.2 model if not already available
ollama pull llama3.2
```

## Usage

### Basic Usage

```python
from limerick_converter import LimerickConverter

# Initialize converter
converter = LimerickConverter()

# Convert a story
story = """
A brave knight went on a quest to find a magic sword.
After many adventures, he found it in a dragon's cave.
He returned home a hero.
"""

result = converter.convert(story)

# Access the limerick
print(result["limerick"]["text"])

# Check validation results
if result["validation"]["is_valid"]:
    print("Valid limerick!")
else:
    print(f"Issues: {result['validation']}")
```

### Command Line Interface

```bash
# Use default test story
python limerick_converter.py

# Provide custom story
python limerick_converter.py "Your story here..."
```

### Output Format

The converter returns a structured JSON object:

```json
{
  "limerick": {
    "lines": ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
    "text": "Full limerick text with newlines"
  },
  "validation": {
    "is_valid": true,
    "line_count": 5,
    "syllable_counts": [9, 9, 5, 6, 9],
    "syllable_valid": true,
    "rhyme_scheme": {
      "detected": "AABBA",
      "is_valid": true,
      "a_rhymes": ["night", "fight", "delight"],
      "b_rhymes": ["mark", "stark"]
    }
  },
  "metadata": {
    "model": "llama3.2",
    "timestamp": "2025-09-30T19:30:29.355304",
    "story_length": 133,
    "generation_time": 17.9,
    "attempt": 1
  }
}
```

## Architecture

### Components

1. **SyllableCounter**: Heuristic syllable counting for validation
2. **RhymeChecker**: Simple phonetic rhyme detection (AABBA validation)
3. **OutputFormatter**: Structured JSON output generation
4. **LimerickConverter**: Main orchestration class

### Validation

The system validates:
- **Line count**: Must be exactly 5 lines
- **Syllable counts**:
  - Lines 1, 2, 5: 8-9 syllables
  - Lines 3, 4: 5-6 syllables
- **Rhyme scheme**: AABBA pattern
  - Lines 1, 2, 5 must rhyme (A)
  - Lines 3, 4 must rhyme (B)

### Error Handling

- Empty/invalid story input
- Ollama connection failures
- Malformed LLM responses
- Timeout handling
- Automatic retries (up to 3 attempts)

## Limerick Structure

A limerick is a 5-line poem with:
- **Rhyme scheme**: AABBA
- **Meter**: Anapestic (da-da-DUM rhythm)
- **Syllables**:
  - Long lines (1, 2, 5): 8-9 syllables
  - Short lines (3, 4): 5-6 syllables
- **Tone**: Typically humorous or clever

### Example

```
A programmer stayed up at night,    (9 syllables - A rhyme)
Debugging code was their fight,      (8 syllables - A rhyme)
Found one missing mark,              (5 syllables - B rhyme)
A semicolon stark,                   (6 syllables - B rhyme)
Then slept with relief and delight.  (9 syllables - A rhyme)
```

## Configuration

### Custom Model

```python
converter = LimerickConverter(
    model="llama3.2",
    ollama_host="http://localhost:11434"
)
```

### Conversion Parameters

```python
result = converter.convert(
    story=story,
    max_retries=3,    # Retries for malformed output
    timeout=30        # Seconds per Ollama call
)
```

## Limitations

### Known Issues

1. **Syllable counting**: Uses heuristic vowel-based algorithm
   - May misccount some words (e.g., "fire" = 1 or 2?)
   - No phonetic dictionary integration

2. **Rhyme detection**: Simple phonetic matching
   - Based on last 2-3 characters
   - May miss or falsely match some rhymes

3. **LLM variability**: llama3.2 doesn't always produce perfect limericks
   - Syllable counts may be off
   - Rhyme scheme usually correct but not guaranteed

4. **No meter validation**: Cannot check anapestic rhythm
   - Only validates syllables and rhymes
   - Actual meter is up to the LLM

### Future Enhancements

- Phonetic dictionary for accurate syllable/rhyme detection
- Support for multiple LLM models
- Meter validation using NLP stress patterns
- Batch processing
- Web interface
- Async support for scalability

## Testing

See `test_limerick_converter.py` for comprehensive unit tests covering:
- Syllable counting edge cases
- Rhyme detection accuracy
- Prompt building
- Response parsing
- Validation logic
- Full integration tests

## Technical Specification

See `docs/technical-spec.md` for complete technical design documentation.

## License

This is an experimental implementation for research purposes.

## Author

Implementation following Method 2: Specification-Driven Development
Experiment 1.608.B - Limerick Converter
