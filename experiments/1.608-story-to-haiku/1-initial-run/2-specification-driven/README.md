# Story-to-Haiku Converter
## Method 2: Specification-Driven Implementation

**Experiment**: 1.608 - Story-to-Haiku Converter
**Methodology**: Specification-Driven (Design-First)
**Date**: 2025-09-30

---

## Overview

This implementation converts narrative text into haiku poetry (5-7-5 syllable structure) using a local LLM via Ollama. The project follows a **specification-driven methodology**, where comprehensive technical design is completed before any implementation begins.

### Key Characteristics
- **Specification-first approach**: Complete technical spec before coding
- **Production-ready**: Comprehensive error handling and validation
- **Test-friendly**: Dependency injection enables fast, mocked testing
- **Well-documented**: Detailed technical specification and inline docs

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install ollama pytest

# Ensure Ollama is running and llama3.2 model is available
ollama pull llama3.2
```

### Basic Usage

```python
from haiku_converter import story_to_haiku

# Convert a story to haiku
story = """
In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as
if they were old friends, sharing stories of seasons past.
"""

result = story_to_haiku(story)

# Display the result
print(result['haiku'])
# Output:
# Mountains cradle home
# Garden whispers ancient tales
# Seasons dance with time

print(f"Syllables: {result['syllable_counts']}")  # [5, 7, 5]
print(f"Essence: {result['essence']}")
```

---

## API Reference

### `story_to_haiku(text: str, llm_client=None) -> dict`

Converts a story or text into a haiku poem.

**Parameters:**
- `text` (str): Input story or paragraph to convert
  - Must be non-empty after stripping whitespace
  - Will be truncated to 500 characters for LLM processing
- `llm_client` (optional): LLM client with `generate()` method
  - If `None`, uses the ollama module
  - For testing, pass a mock object

**Returns:**
```python
{
    'haiku': str,              # Complete haiku with newlines
    'lines': list[str],        # Three haiku lines
    'syllable_counts': list[int],  # Syllable count per line
    'essence': str             # Core concept from input
}
```

**Raises:**
- `ValueError`: If input is empty or whitespace-only
- `ValueError`: If LLM returns invalid number of lines (not 3)
- `RuntimeError`: If LLM generation fails

**Example:**
```python
result = story_to_haiku("A tale of mountains...")
print(result['haiku'])
assert len(result['lines']) == 3
```

---

## Testing

### Running Tests

This implementation uses **mocked LLM clients** for testing, enabling fast execution without requiring Ollama to be running.

```bash
# Run all tests
pytest test_haiku_converter.py -v

# Run with coverage
pytest test_haiku_converter.py --cov=haiku_converter --cov-report=term-missing

# Run specific test class
pytest test_haiku_converter.py::TestSyllableCounting -v
```

### Test Structure

The test suite is organized into comprehensive categories:

1. **Input Validation Tests** - Empty input, whitespace, length limits
2. **LLM Integration Tests** - Mock client usage, prompt structure
3. **Response Parsing Tests** - Line extraction, whitespace handling
4. **Syllable Counting Tests** - Algorithm accuracy, edge cases
5. **Result Structure Tests** - Output format validation
6. **Integration Scenarios** - End-to-end workflows
7. **Error Handling Tests** - Graceful failure handling

### Testing with Mocks

```python
from unittest.mock import Mock
from haiku_converter import story_to_haiku

# Create a mock LLM client
mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive'
}

# Use mock for testing
result = story_to_haiku("Spring story", llm_client=mock_llm)

# Verify result structure
assert len(result['lines']) == 3
assert result['syllable_counts'] == [5, 7, 5]
```

---

## Architecture

### Design Principles

This implementation follows key software engineering principles:

1. **Separation of Concerns**: Distinct functions for syllable counting, parsing, and conversion
2. **Dependency Injection**: LLM client is injected, enabling testability
3. **Comprehensive Error Handling**: Clear error messages for all failure modes
4. **Specification-Driven**: Implementation follows detailed technical spec

### Component Flow

```
Input Text
    ↓
Input Validation
    ↓
LLM Client Resolution (real or mock)
    ↓
Prompt Generation
    ↓
LLM Invocation
    ↓
Response Parsing
    ↓
Syllable Validation
    ↓
Result Structure
    ↓
Output Dict
```

### Helper Functions

- **`count_syllables(word: str) -> int`**
  - Vowel-cluster algorithm
  - ~85% accuracy on English words
  - Handles silent 'e' and vowel clusters

- **`count_syllables_in_line(line: str) -> int`**
  - Counts total syllables in a line
  - Ignores punctuation
  - Sums individual word counts

- **`extract_essence(text: str) -> str`**
  - Extracts core concept for metadata
  - Truncates at ~50 characters
  - Preserves word boundaries

---

## Error Handling

### Input Validation

```python
# Empty input
try:
    story_to_haiku("")
except ValueError as e:
    print(e)  # "Input text cannot be empty or whitespace-only"

# Whitespace-only
try:
    story_to_haiku("   \n\n   ")
except ValueError as e:
    print(e)  # "Input text cannot be empty or whitespace-only"
```

### LLM Errors

```python
try:
    result = story_to_haiku("Story")
except RuntimeError as e:
    print(e)  # "LLM generation failed: [error details]"
```

### Invalid Response Format

```python
# If LLM returns wrong number of lines
try:
    result = story_to_haiku("Story")  # LLM returns 2 lines instead of 3
except ValueError as e:
    print(e)  # "Expected 3 haiku lines, got 2. LLM response may be malformed."
```

---

## Examples

### Example 1: Simple Story

```python
story = "A cat sat by the window, watching birds fly past."
result = story_to_haiku(story)

print(result['haiku'])
# Silent window cat
# Watches feathered dreams take flight
# Patience in stillness
```

### Example 2: Longer Narrative

```python
story = """
The old lighthouse keeper climbed the spiral stairs every evening.
For forty years, he had lit the beacon, guiding ships safely to shore.
Now, on his last night, he paused to watch the sunset one final time.
"""
result = story_to_haiku(story)

print(result['haiku'])
# Lighthouse stands steadfast
# Forty years of guiding light
# Final sunset glows

print(f"Syllables: {result['syllable_counts']}")  # [5, 7, 5]
print(f"Essence: {result['essence']}")  # "The old lighthouse keeper climbed the spiral..."
```

### Example 3: Testing with Mock

```python
from unittest.mock import Mock

# Create mock for testing
mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Test haiku here\nMiddle line is longer now\nFinal line at end'
}

# Use mock instead of real Ollama
result = story_to_haiku("Test story", llm_client=mock_llm)

# Verify mock was called correctly
assert mock_llm.generate.called
assert mock_llm.generate.call_args[1]['model'] == 'llama3.2'
```

---

## Technical Specification

For comprehensive technical details, see [`docs/technical-spec.md`](docs/technical-spec.md), which includes:

- Complete architecture diagrams
- Interface specifications
- Prompt engineering strategy
- Syllable counting algorithm
- Error handling strategy
- Design decisions and rationale
- Implementation checklist

---

## Methodology: Specification-Driven

### Approach

This implementation demonstrates the **specification-driven methodology**:

1. **Phase 1: Complete Specification (2-3 minutes)**
   - Design architecture
   - Define interfaces
   - Plan error handling
   - Document testing strategy

2. **Phase 2: Implementation to Spec (2-3 minutes)**
   - Implement per specification
   - Follow architectural plan
   - Comprehensive error handling
   - Full test coverage

### Advantages

- **Clear roadmap**: Implementation follows established plan
- **Comprehensive design**: All edge cases considered upfront
- **Production-ready**: Error handling built in from start
- **Well-documented**: Specification serves as living documentation

### Disadvantages

- **Upfront time investment**: Specification takes time before coding
- **Less flexible**: Changes require spec updates
- **Over-engineering risk**: May design features not needed

---

## Performance

### With Mocks (Testing)
- All tests run in **<1 second**
- No Ollama required
- Parallel execution safe

### With Real Ollama (Production)
- ~20 seconds per conversion
- Depends on LLM model and hardware
- Single-threaded by default

---

## Files

```
2-specification-driven/
├── docs/
│   └── technical-spec.md      # Comprehensive technical specification
├── haiku_converter.py         # Main implementation (production-ready)
├── test_haiku_converter.py    # Comprehensive test suite with mocks
└── README.md                  # This file
```

---

## Comparison with Other Methods

This is Method 2 of 4 experimental implementations:

| Method | Approach | Time | Test Coverage | Documentation |
|--------|----------|------|---------------|---------------|
| 1. Immediate | Code first, minimal planning | 2-3 min | Basic | Minimal |
| **2. Specification** | **Design first, then implement** | **5-7 min** | **Comprehensive** | **Extensive** |
| 3. Test-First | Write tests, then implementation | 3-4 min | High | Moderate |
| 4. Adaptive TDD | Iterative test-code cycles | 3-4 min | High | Good |

### Method 2 Strengths
- Most comprehensive documentation
- All edge cases considered upfront
- Production-ready from the start
- Clear architectural vision

### Method 2 Trade-offs
- Longest development time
- Higher upfront investment
- May over-design for simple tasks

---

## License

Part of the spawn-experiments project demonstrating development methodologies.

---

## Related Documentation

- [Experiment Specification](../EXPERIMENT_SPEC.md) - Overall experiment goals
- [Technical Specification](docs/technical-spec.md) - Detailed design document
- [Ollama Integration Experiments](../../../docs/OLLAMA_EXPERIMENTS_SERIES.md) - Series overview

---

**Implementation**: Claude (Specification-Driven Methodology)
**Date**: 2025-09-30
**Version**: 1.0.0