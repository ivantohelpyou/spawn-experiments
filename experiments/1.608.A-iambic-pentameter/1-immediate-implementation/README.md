# Iambic Pentameter Converter

Converts prose stories into Shakespearean verse (iambic pentameter) using llama3.2 via Ollama.

## Features

- Convert prose text to iambic pentameter (10 syllables per line, alternating unstressed/stressed)
- Process single paragraphs or entire stories
- Preserve story structure with paragraph separation
- CLI interface for easy use
- Comprehensive test suite

## Requirements

- Python 3.6+
- Ollama installed locally
- llama3.2 model pulled in Ollama

## Installation

1. Install Ollama:
   ```bash
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh

   # macOS
   brew install ollama
   ```

2. Pull the llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```

3. No Python packages required - uses only standard library

## Usage

### Command Line

Convert text directly:
```bash
python iambic_converter.py "The cat sat on the mat and watched the moon rise."
```

Convert text from a file:
```bash
python iambic_converter.py -f story.txt
```

### Python API

```python
from iambic_converter import IambicConverter

converter = IambicConverter()

# Convert a simple sentence
prose = "The cat sat on the mat."
verse = converter.convert_to_iambic(prose)
print(verse)

# Convert a full story with multiple paragraphs
story = """Once upon a time, there was a cat.

The cat loved to sit on a mat."""

verse = converter.convert_story(story, preserve_paragraphs=True)
print(verse)
```

## Testing

Run the test suite:
```bash
python test_iambic_converter.py
```

All tests use mocks and don't require Ollama running. One integration test is skipped by default.

## How It Works

1. Takes prose text as input
2. Creates a prompt instructing the LLM to convert to iambic pentameter
3. Sends prompt to llama3.2 via Ollama
4. Returns the converted verse

The converter emphasizes:
- 10 syllables per line
- Alternating stress pattern (unstressed/stressed)
- Preserving original meaning
- Using Shakespearean poetic language

## Example

**Input:**
```
The cat sat on the mat and watched the moon rise over the hills.
```

**Output:**
```
The cat did sit upon the mat with grace,
And watched the moon ascend o'er distant hills.
```

## Development Method

Built using Method 1: Immediate Implementation
- Started coding immediately with minimal planning
- Focused on getting functionality working quickly
- Tests added alongside implementation
- Iterative refinement as needed

## License

Experimental code - part of spawn-poetry project
