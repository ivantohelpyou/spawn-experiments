# Technical Specification: Story-to-Haiku Converter
## Method 2: Specification-Driven Implementation

**Date**: 2025-09-30
**Version**: 1.0
**Status**: Design Complete

---

## 1. Overview

### 1.1 Purpose
Convert narrative text into traditional haiku poetry (5-7-5 syllable structure) using a local LLM via Ollama, with production-quality error handling and comprehensive testing support.

### 1.2 Design Philosophy
- **Specification-first**: Complete technical design before implementation
- **Clean architecture**: Clear separation of concerns
- **Dependency injection**: Testable with mocks, deployable with real LLM
- **Robust error handling**: Graceful degradation and clear error messages
- **Production-ready**: Logging, validation, and edge case handling

---

## 2. Architecture

### 2.1 Component Diagram
```
┌─────────────────────────────────────────────┐
│         story_to_haiku(text, llm_client)    │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  1. Input Validation                 │  │
│  │     - Empty check                    │  │
│  │     - Whitespace validation          │  │
│  │     - Length limits                  │  │
│  └──────────────────────────────────────┘  │
│                  ↓                          │
│  ┌──────────────────────────────────────┐  │
│  │  2. LLM Client Resolution            │  │
│  │     - Use provided client OR         │  │
│  │     - Default to ollama module       │  │
│  └──────────────────────────────────────┘  │
│                  ↓                          │
│  ┌──────────────────────────────────────┐  │
│  │  3. Prompt Generation                │  │
│  │     - Text truncation (500 chars)    │  │
│  │     - Structured prompt              │  │
│  │     - Clear instructions             │  │
│  └──────────────────────────────────────┘  │
│                  ↓                          │
│  ┌──────────────────────────────────────┐  │
│  │  4. LLM Invocation                   │  │
│  │     - Call generate()                │  │
│  │     - Error handling                 │  │
│  └──────────────────────────────────────┘  │
│                  ↓                          │
│  ┌──────────────────────────────────────┐  │
│  │  5. Response Parsing                 │  │
│  │     - Extract lines                  │  │
│  │     - Strip whitespace               │  │
│  │     - Validate count                 │  │
│  └──────────────────────────────────────┘  │
│                  ↓                          │
│  ┌──────────────────────────────────────┐  │
│  │  6. Syllable Validation              │  │
│  │     - Count per line                 │  │
│  │     - Verify 5-7-5 pattern           │  │
│  └──────────────────────────────────────┘  │
│                  ↓                          │
│  ┌──────────────────────────────────────┐  │
│  │  7. Result Structure                 │  │
│  │     - Format output dict             │  │
│  │     - Include metadata               │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘

Helper Functions:
- count_syllables(word: str) -> int
- extract_essence(text: str) -> str
```

### 2.2 Module Structure
```
2-specification-driven/
├── docs/
│   └── technical-spec.md          # This file
├── haiku_converter.py             # Main implementation
├── test_haiku_converter.py        # Comprehensive tests
└── README.md                      # User documentation
```

---

## 3. Interface Specification

### 3.1 Primary Function

```python
def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem using LLM.

    This function uses dependency injection to support both production
    use (real Ollama) and testing (mocked LLM client).

    Args:
        text (str): Input story or paragraph to convert.
                   Must be non-empty after stripping whitespace.
                   Will be truncated to 500 characters for LLM processing.

        llm_client (optional): LLM client with generate() method.
                              If None, uses ollama module.
                              For testing, pass a mock object.

    Returns:
        dict: Structured haiku result containing:
            - haiku (str): Complete haiku with newline separators
            - lines (list[str]): Three haiku lines as separate strings
            - syllable_counts (list[int]): Syllable count per line [5, 7, 5]
            - essence (str): Core concept extracted from original text

    Raises:
        ValueError: If input text is empty or whitespace-only
        ValueError: If LLM returns invalid number of lines
        RuntimeError: If LLM generation fails

    Example:
        >>> result = story_to_haiku("A tale of mountains and time...")
        >>> print(result['haiku'])
        Mountains stand timeless
        Ancient peaks touch clouded sky
        Stories carved in stone

        >>> result['syllable_counts']
        [5, 7, 5]
    """
```

### 3.2 Helper Functions

#### count_syllables(word: str) -> int
```python
def count_syllables(word: str) -> int:
    """
    Count syllables in a word using vowel-cluster algorithm.

    Algorithm:
    1. Convert to lowercase
    2. Remove trailing 'e' (unless word ends in 'le')
    3. Count vowel groups (consecutive vowels = 1 syllable)
    4. Minimum 1 syllable per word

    Args:
        word (str): Single word to analyze

    Returns:
        int: Estimated syllable count (1 or greater)

    Accuracy: ~85% on common English words
    Known limitations: Handles most cases but not perfect

    Examples:
        >>> count_syllables("mountain")
        2
        >>> count_syllables("beautiful")
        3
        >>> count_syllables("sky")
        1
    """
```

#### extract_essence(text: str) -> str
```python
def extract_essence(text: str) -> str:
    """
    Extract core concept from input text for metadata.

    Simple algorithm:
    1. Take first 50 characters
    2. Find last complete word
    3. Add ellipsis if truncated

    Args:
        text (str): Original input text

    Returns:
        str: Brief summary of input (max ~50 chars)

    Example:
        >>> extract_essence("A long story about mountains and valleys...")
        "A long story about mountains and valleys..."
    """
```

---

## 4. Prompt Engineering Strategy

### 4.1 Prompt Design
```python
HAIKU_PROMPT_TEMPLATE = """Convert the following story into a haiku (5-7-5 syllable structure).
Return only the haiku, one line per line, no other text.

Story: {text}

Haiku:"""
```

### 4.2 Design Rationale
1. **Clear instruction**: "Convert the following story into a haiku"
2. **Explicit format**: "5-7-5 syllable structure"
3. **Output constraint**: "Return only the haiku, one line per line, no other text"
4. **Structured layout**: Clear Story/Haiku sections
5. **No preamble needed**: llama3.2 handles this well

### 4.3 Input Processing
- **Truncation**: Limit to 500 characters to prevent token overflow
- **Whitespace**: Strip but preserve internal structure
- **Empty handling**: Reject before LLM call

### 4.4 Expected Output Format
```
First line of haiku
Second line is longer here
Third line completes it
```

No markdown, no extra text, no explanations.

---

## 5. Error Handling Strategy

### 5.1 Input Validation Errors
```python
# Empty or whitespace-only input
if not text or not text.strip():
    raise ValueError("Input text cannot be empty or whitespace-only")

# Clear, actionable error messages
```

### 5.2 LLM Generation Errors
```python
try:
    response = llm_client.generate(...)
except Exception as e:
    raise RuntimeError(f"LLM generation failed: {str(e)}") from e
```

### 5.3 Parsing Errors
```python
lines = [line.strip() for line in haiku_text.split('\n') if line.strip()]

if len(lines) != 3:
    raise ValueError(
        f"Expected 3 haiku lines, got {len(lines)}. "
        f"LLM response may be malformed."
    )
```

### 5.4 Syllable Validation
```python
# Count but don't enforce strict validation
# LLMs are ~80% accurate on syllable counting
syllable_counts = [count_syllables_in_line(line) for line in lines]

# Return counts for caller to validate if needed
# Don't raise exception - allow approximate haiku
```

---

## 6. Testing Strategy

### 6.1 Test Categories

#### Unit Tests (with mocks)
1. **Input validation tests**
   - Empty string
   - Whitespace-only
   - Very long input (truncation)
   - Normal input

2. **LLM integration tests**
   - Mock client injection
   - Verify generate() called correctly
   - Correct model passed
   - Prompt structure

3. **Response parsing tests**
   - Valid 3-line response
   - Extra whitespace
   - Extra blank lines
   - Invalid line counts

4. **Syllable counting tests**
   - Simple words
   - Complex words
   - Edge cases

5. **Result structure tests**
   - All fields present
   - Correct types
   - Newline formatting

#### Integration Tests (real Ollama - separate script)
- End-to-end with real LLM
- Only run during demo/comparison
- Not part of development test suite

### 6.2 Mock Design
```python
from unittest.mock import Mock

def create_mock_llm(haiku_response: str) -> Mock:
    """Create a mock LLM client for testing."""
    mock = Mock()
    mock.generate.return_value = {
        'response': haiku_response
    }
    return mock

# Example usage:
mock_llm = create_mock_llm(
    'Cherry blossoms fall\n'
    'Softly on the quiet pond\n'
    'Spring whispers arrive'
)
```

### 6.3 Test Data
```python
MOCK_HAIKU_RESPONSES = {
    'spring': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive',
    'winter': 'Silent snow blankets\nFrozen world in crystal white\nWinter dreams deeply',
    'autumn': 'Leaves paint gold and red\nFalling gently to the earth\nAutumn bids farewell',
    'coding': 'Code lines on the screen\nLogic winds through endless loops\nMind in flow state dances',
}
```

---

## 7. Implementation Requirements

### 7.1 Dependencies
```python
# Required
import ollama  # For LLM interaction (production)
import re      # For syllable counting

# Testing only
import pytest
from unittest.mock import Mock
```

### 7.2 Code Quality Standards
- **Type hints**: All public functions
- **Docstrings**: Google style for all functions
- **Error messages**: Clear and actionable
- **No magic numbers**: Named constants
- **DRY principle**: Extract helpers where appropriate

### 7.3 Performance Targets
- **Mock tests**: <1 second total
- **Real LLM**: ~20 seconds per conversion (expected)
- **Memory**: <50MB for normal use

---

## 8. Syllable Counting Algorithm

### 8.1 Implementation Approach
Use vowel-cluster counting (80-90% accurate):

```python
def count_syllables(word: str) -> int:
    """Count syllables using vowel clustering."""
    word = word.lower().strip()
    if not word:
        return 0

    # Remove trailing 'e' (unless word ends in 'le')
    if word.endswith('e') and not word.endswith('le'):
        word = word[:-1]

    # Count vowel groups
    vowels = 'aeiouy'
    count = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            count += 1
        previous_was_vowel = is_vowel

    return max(1, count)  # Minimum 1 syllable

def count_syllables_in_line(line: str) -> int:
    """Count total syllables in a line."""
    # Remove punctuation, split into words
    words = re.findall(r'\b[a-z]+\b', line.lower())
    return sum(count_syllables(word) for word in words)
```

### 8.2 Accuracy Notes
- ~85% accurate on common English words
- Known issues: Silent letters, compound words
- Good enough for validation, not perfect
- LLM is typically more accurate than this algorithm

---

## 9. Success Criteria

### 9.1 Functional Requirements
- [ ] Accepts text input and converts to haiku
- [ ] Returns structured dict with all required fields
- [ ] Validates 5-7-5 syllable structure
- [ ] Supports dependency injection for testing
- [ ] Handles edge cases gracefully

### 9.2 Code Quality Requirements
- [ ] Comprehensive type hints
- [ ] Full docstring coverage
- [ ] Clear error messages
- [ ] No code duplication

### 9.3 Testing Requirements
- [ ] 100% test coverage
- [ ] All tests use mocks (no real LLM calls)
- [ ] Tests run in <1 second
- [ ] Edge cases covered

### 9.4 Documentation Requirements
- [ ] Technical specification (this file)
- [ ] README with examples
- [ ] Inline code comments where needed
- [ ] Clear function docstrings

---

## 10. Design Decisions & Rationale

### 10.1 Why Dependency Injection?
**Decision**: Accept optional `llm_client` parameter
**Rationale**:
- Enables fast, parallel development with mocks
- Allows testing without running Ollama
- Follows SOLID principles (Dependency Inversion)
- Makes code more maintainable

### 10.2 Why Truncate at 500 Characters?
**Decision**: Limit input to 500 chars before LLM
**Rationale**:
- Haiku captures essence, not full details
- Prevents token limits
- Faster generation
- LLM can focus on core concepts

### 10.3 Why Not Enforce Strict Syllable Validation?
**Decision**: Return counts but don't raise error
**Rationale**:
- Syllable counting is inherently imperfect (~85% accurate)
- LLM may be more accurate than our algorithm
- Allows caller to decide strictness
- Fails gracefully rather than rejecting valid haiku

### 10.4 Why Simple Syllable Algorithm?
**Decision**: Vowel-cluster method vs. dictionary lookup
**Rationale**:
- No external dependencies
- Fast execution
- Good enough for validation (85% accurate)
- Dictionary would add complexity and size

### 10.5 Why Extract Essence?
**Decision**: Include essence field in return dict
**Rationale**:
- Provides context for the haiku
- Useful for logging/debugging
- Helps trace conversion process
- Minimal overhead

---

## 11. Implementation Checklist

### Phase 1: Core Implementation
- [ ] Implement `count_syllables(word)`
- [ ] Implement `count_syllables_in_line(line)`
- [ ] Implement `extract_essence(text)`
- [ ] Implement `story_to_haiku(text, llm_client)`
- [ ] Add input validation
- [ ] Add error handling
- [ ] Add type hints and docstrings

### Phase 2: Testing
- [ ] Create mock helper functions
- [ ] Write input validation tests
- [ ] Write LLM integration tests (mocked)
- [ ] Write parsing tests
- [ ] Write syllable counting tests
- [ ] Write result structure tests
- [ ] Achieve 100% coverage

### Phase 3: Documentation
- [ ] Write README.md
- [ ] Add usage examples
- [ ] Document edge cases
- [ ] Add architecture diagram

### Phase 4: Verification
- [ ] Run all tests (should pass with mocks)
- [ ] Verify no real Ollama calls during tests
- [ ] Check code quality (linting)
- [ ] Verify specification compliance

---

## 12. Future Enhancements (Out of Scope)

These are intentionally NOT implemented for this experiment:

1. **Better syllable counting**: Use pyphen or pronouncing library
2. **Multi-language support**: Currently English-only
3. **Configurable LLM model**: Hardcoded to llama3.2
4. **Retry logic**: No automatic retries on LLM failure
5. **Async support**: Synchronous only
6. **Caching**: No caching of LLM responses
7. **Batch processing**: Single text at a time
8. **Quality scoring**: No haiku quality metrics

---

## 13. Timeline

### Specification Phase (Target: 2-3 minutes)
- [x] Create technical specification
- [x] Define architecture
- [x] Design interfaces
- [x] Plan testing strategy

### Implementation Phase (Target: 2-3 minutes)
- [ ] Implement core functions
- [ ] Add error handling
- [ ] Write comprehensive tests
- [ ] Create documentation

### Total Target: 5-7 minutes

---

## Appendix A: Example Execution Flow

### Input
```python
text = """
In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as
if they were old friends, sharing stories of seasons past.
"""
```

### Processing Steps
1. Validate: `text.strip()` is not empty → Pass
2. Truncate: 183 chars < 500 → No truncation needed
3. Generate prompt with text
4. Call `llm_client.generate(model='llama3.2', prompt=...)`
5. Parse response: Split by newlines, strip whitespace
6. Validate: Count lines → 3 lines → Pass
7. Count syllables: [5, 7, 5]
8. Extract essence: "In a small village nestled between mountains..."
9. Return structured dict

### Output
```python
{
    'haiku': 'Mountains cradle home\nGarden whispers ancient tales\nSeasons dance with time',
    'lines': [
        'Mountains cradle home',
        'Garden whispers ancient tales',
        'Seasons dance with time'
    ],
    'syllable_counts': [5, 7, 5],
    'essence': 'In a small village nestled between mountains...'
}
```

---

**End of Specification**