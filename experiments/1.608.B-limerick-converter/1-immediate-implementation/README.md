# Story-to-Limerick Converter
## Method 1: Immediate Implementation

Fast implementation with minimal planning - built to work quickly!

## Overview

Converts prose stories into limericks using llama3.2 via Ollama.

**Limerick Structure:**
- 5 lines total
- AABBA rhyme scheme
- Lines 1, 2, 5: 8-9 syllables
- Lines 3, 4: 5-6 syllables
- Anapestic meter (da-da-DUM rhythm)

## Prerequisites

1. **Python 3.7+**
2. **Ollama** - Install from [https://ollama.ai](https://ollama.ai)
3. **llama3.2 model** - Pull with: `ollama pull llama3.2`

## Installation

No Python packages to install - uses only standard library!

```bash
# Ensure Ollama is running
ollama list

# Pull llama3.2 if not already available
ollama pull llama3.2
```

## Usage

### Command Line

```bash
# Basic usage
python limerick_converter.py "Your story here..."

# Example
python limerick_converter.py "In a small village, a clever fox outsmarted the local hunters by using their own traps against them."
```

### As a Library

```python
from limerick_converter import LimerickConverter

# Create converter
converter = LimerickConverter()

# Convert a story
story = "A programmer stayed up late debugging and found a missing semicolon."
result = converter.convert(story)

# Access the limerick
print(result["limerick"])

# Get JSON output
json_output = converter.convert_to_json(story)
print(json_output)
```

## Output Format

The converter returns a dictionary with:

```python
{
    "limerick": "Full limerick text...",
    "lines": ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
    "story": "Original story",
    "model": "llama3.2",
    "validation": {
        "valid": True,
        "syllable_counts": [9, 8, 5, 6, 9],
        "issues": []
    }
}
```

## Running Tests

```bash
# Run all tests
python test_limerick_converter.py

# Or use unittest directly
python -m unittest test_limerick_converter -v
```

## Features

- **Ollama Integration**: Uses subprocess to call Ollama CLI
- **Syllable Counting**: Approximate syllable counter for validation
- **Structure Validation**: Checks line count and syllable counts
- **JSON Output**: Returns structured data
- **Error Handling**: Validates input and handles Ollama errors
- **CLI Interface**: Simple command-line usage

## Architecture

- **Class-based design**: `LimerickConverter` encapsulates all functionality
- **Subprocess calls**: Direct Ollama CLI integration
- **Prompt template**: Optimized from METHOD_1_PROMPT.md specification
- **Validation**: Built-in limerick structure checking

## Files

- `limerick_converter.py` - Main implementation (248 lines)
- `test_limerick_converter.py` - Unit tests (17 tests)
- `requirements.txt` - Dependencies (none!)
- `README.md` - This file

## Example Output

```bash
$ python limerick_converter.py "A clever fox outsmarted hunters by using their traps."

Converting story to limerick...

LIMERICK:
==================================================
A clever fox, sly as could be,
Turned hunters' own traps into glee,
With cunning and grace,
He'd set up each place,
And feasted while hunters ran free.
==================================================

VALIDATION:
Valid: True
Syllable counts: [9, 9, 5, 6, 9]
```

## Development Notes

This is **Method 1: Immediate Implementation** - built quickly with minimal planning:
- Implementation time: ~10-15 minutes
- Lines of code: ~248 (main) + 276 (tests)
- Test count: 17 tests
- Approach: Code first, iterate later
