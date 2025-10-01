# Limerick Converter - Test-First Development (Method 3)

Converts prose stories into limericks using Test-Driven Development methodology.

## Overview

This implementation follows strict TDD (Test-Driven Development) with RED-GREEN-REFACTOR cycles. Each feature was built by:
1. Writing a failing test (RED)
2. Implementing minimal code to pass (GREEN)
3. Refactoring if needed (REFACTOR)

## Features

- Story-to-limerick conversion using Ollama's llama3.2 model
- Limerick structure validation (5 lines)
- Syllable counting for verification
- AABBA rhyme scheme support

## Requirements

- Python 3.8+
- Ollama installed and running
- llama3.2 model: `ollama pull llama3.2`

No external Python packages required (uses only standard library).

## Usage

### Basic Usage

```python
from limerick_converter import LimerickConverter

converter = LimerickConverter()

story = "A young programmer stayed up all night debugging code, finally finding a missing semicolon at 3am."

result = converter.generate_limerick(story)

print(result['limerick'])
print(f"\nLines: {result['lines']}")
```

### Validating Limerick Structure

```python
limerick_lines = [
    "A programmer stayed up at night,",
    "Debugging code was their fight,",
    "Found one missing mark,",
    "A semicolon stark,",
    "Then slept with relief and delight."
]

validation = converter.validate_limerick_structure(limerick_lines)
print(f"Valid: {validation['valid']}")
print(f"Issues: {validation['issues']}")
```

### Counting Syllables

```python
# Count syllables in a word
count = converter.count_syllables("beautiful")  # Returns: 3

# Count syllables in a line
line_count = converter.count_syllables_in_line("A programmer stayed up at night")  # Returns: 9
```

## Running Tests

```bash
python test_limerick_converter.py -v
```

## TDD Commit History

This implementation follows strict TDD with atomic commits:

1. **RED**: Test for limerick structure validation
2. **GREEN**: Implement structure validation  
3. **RED**: Test for syllable counting
4. **GREEN**: Implement syllable counting
5. **RED**: Test for Ollama LLM integration
6. **GREEN**: Implement Ollama LLM integration

## Implementation Details

- Uses heuristic syllable counting (vowel groups)
- Calls Ollama via subprocess
- Returns structured JSON with limerick and lines
- Validates 5-line structure

## Limerick Rules

- Exactly 5 lines
- Rhyme scheme: AABBA
- Syllables: Lines 1,2,5 (8-9), Lines 3,4 (5-6)
- Meter: Anapestic (da-da-DUM)

## Files

- `limerick_converter.py` - Main implementation
- `test_limerick_converter.py` - Test suite
- `requirements.txt` - Dependencies (none)
- `README.md` - This file
