# Story-to-Iambic-Pentameter Converter

Convert prose stories into Shakespearean verse (iambic pentameter) using llama3.2 via Ollama.

**Method**: Specification-Driven Development
- Comprehensive specs defined first
- Clear interfaces and contracts
- Quality-focused implementation

## Features

- Converts prose text to iambic pentameter (10 syllables per line)
- Maintains semantic meaning during conversion
- Syllable counting with heuristic rules
- Uses llama3.2 via Ollama for LLM processing
- Comprehensive test suite

## Requirements

- Python 3.7+
- Ollama with llama3.2 model installed

## Installation

1. Install Ollama from https://ollama.ai
2. Pull the model:
   ```bash
   ollama pull llama3.2
   ```

## Usage

### Command Line

```bash
python iambic_converter.py "The cat sat on the mat and watched the birds fly."
```

### As a Library

```python
from iambic_converter import IambicConverter

converter = IambicConverter()
prose = "The cat sat on the mat."
poem = converter.convert(prose)
print(poem)
```

## Testing

Run the comprehensive test suite:

```bash
python test_iambic_converter.py
```

Test coverage includes:
- Syllable counting accuracy
- Ollama client functionality (mocked)
- Main converter logic
- Integration tests (if Ollama available)

## Architecture

### Core Classes

- **SyllableCounter**: Counts syllables using heuristic rules
- **OllamaClient**: Handles LLM communication
- **IambicConverter**: Main orchestrator for conversion

### Documentation

- `SPECIFICATIONS.md`: Technical requirements and specifications
- `ARCHITECTURE.md`: Detailed design and architecture
- `README.md`: This file

## Example

**Input:**
```
The cat sat on the mat and looked at the bird.
```

**Output:**
```
The cat did sit upon the mat that day
And gazed upon the bird with watchful eye
```

## Limitations

- Syllable counting is ~90% accurate (English pronunciation is complex)
- Only validates syllable count, not stress pattern
- Requires Ollama to be installed and running
- English only
- Processing time: 5-30 seconds per conversion (LLM-dependent)

## License

MIT License - Feel free to use and modify.
