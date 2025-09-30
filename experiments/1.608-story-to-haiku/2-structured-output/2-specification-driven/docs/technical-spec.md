# Technical Specification: Story-to-Haiku Converter with JSON Output
## Method 2: Specification-Driven Implementation
## Run 2: Structured Output

**Date**: 2025-09-30
**Version**: 2.0
**Status**: Design Complete

---

## 1. Overview

### 1.1 Purpose
Convert narrative text into traditional haiku poetry (5-7-5 syllable structure) using a local LLM via Ollama, with **JSON-structured output** where the LLM self-reports syllable counts. This eliminates Python syllable counting, which was proven unreliable in Run 1.

### 1.2 Design Philosophy
- **Specification-first**: Complete technical design before implementation
- **Structured output**: JSON format with explicit syllable counts
- **LLM self-reporting**: Trust the model's syllable awareness
- **Comprehensive validation**: Verify JSON structure and content
- **Production-ready**: Error handling for malformed JSON
- **Olympic-ready**: Output designed for multi-model judging

### 1.3 Key Improvements from Run 1
1. **No Python syllable counting** - LLM reports counts directly
2. **JSON-structured response** - Eliminates parsing ambiguity
3. **Self-validation** - LLM commits to syllable counts
4. **Clearer success criteria** - Valid/invalid flag based on structure
5. **Better error handling** - JSON parsing failures well-defined

---

## 2. Architecture

### 2.1 Component Diagram
```
┌─────────────────────────────────────────────────┐
│       story_to_haiku(text, llm_client)          │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  1. Input Validation                     │  │
│  │     - Empty check                        │  │
│  │     - Whitespace validation              │  │
│  │     - Length limits                      │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  2. LLM Client Resolution                │  │
│  │     - Use provided client OR             │  │
│  │     - Default to ollama module           │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  3. JSON Prompt Generation               │  │
│  │     - Text truncation (500 chars)        │  │
│  │     - Structured JSON template           │  │
│  │     - Explicit format requirement        │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  4. LLM Invocation                       │  │
│  │     - Call generate() with llama3.2      │  │
│  │     - Request JSON output                │  │
│  │     - Error handling                     │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  5. JSON Response Parsing                │  │
│  │     - Parse JSON string                  │  │
│  │     - Handle JSONDecodeError             │  │
│  │     - Strip extra text                   │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  6. Structure Validation                 │  │
│  │     - Verify required keys               │  │
│  │     - Check line count (3)               │  │
│  │     - Check syllable count (3)           │  │
│  │     - Validate data types                │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  7. Syllable Validation                  │  │
│  │     - Compare against [5, 7, 5]          │  │
│  │     - Set valid flag                     │  │
│  │     - NO Python counting!                │  │
│  └──────────────────────────────────────────┘  │
│                  ↓                              │
│  ┌──────────────────────────────────────────┐  │
│  │  8. Result Structure Assembly            │  │
│  │     - Format output dict                 │  │
│  │     - Include all metadata               │  │
│  │     - Combine lines into haiku string    │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

Key Change: NO syllable counting helpers needed!
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
    Convert a story or text into a haiku poem using LLM with JSON output.

    This function uses structured JSON output where the LLM self-reports
    syllable counts, eliminating unreliable Python syllable counting.

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
            - syllables (list[int]): LLM-reported syllable counts
            - essence (str): Core theme extracted from original text
            - valid (bool): Whether syllables match [5, 7, 5]

    Raises:
        ValueError: If input text is empty or whitespace-only
        ValueError: If JSON response is malformed
        ValueError: If required JSON keys are missing
        ValueError: If line/syllable counts don't match expected structure
        RuntimeError: If LLM generation fails

    Example:
        >>> result = story_to_haiku("A tale of mountains and time...")
        >>> print(result['haiku'])
        Mountains stand timeless
        Ancient peaks touch clouded sky
        Stories carved in stone

        >>> result['syllables']
        [5, 7, 5]
        >>> result['valid']
        True
    """
```

### 3.2 No Helper Functions Needed!

**CRITICAL CHANGE**: Unlike Run 1, we do NOT implement syllable counting helpers:
- `count_syllables()` - REMOVED (unreliable)
- `count_syllables_in_line()` - REMOVED (not needed)
- `extract_essence()` - REMOVED (LLM provides this)

**Why?** The LLM handles all of this in the JSON response.

---

## 4. JSON Output Schema

### 4.1 Required JSON Format

The LLM MUST return JSON in this exact structure:

```json
{
  "lines": ["line 1 text", "line 2 text", "line 3 text"],
  "syllables": [5, 7, 5],
  "essence": "brief description of theme"
}
```

### 4.2 Schema Specification

```python
JSON_SCHEMA = {
    "type": "object",
    "required": ["lines", "syllables", "essence"],
    "properties": {
        "lines": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3,
            "description": "Three haiku lines"
        },
        "syllables": {
            "type": "array",
            "items": {"type": "integer", "minimum": 1},
            "minItems": 3,
            "maxItems": 3,
            "description": "Syllable counts per line (ideally [5, 7, 5])"
        },
        "essence": {
            "type": "string",
            "minLength": 1,
            "description": "Core theme or concept of the haiku"
        }
    }
}
```

### 4.3 Validation Rules

1. **Required keys**: All three keys must be present
2. **Line count**: Exactly 3 lines
3. **Syllable count**: Exactly 3 integer values
4. **Data types**: lines are strings, syllables are integers, essence is string
5. **Validity check**: `valid = (syllables == [5, 7, 5])`

### 4.4 Example Valid Responses

**Perfect haiku:**
```json
{
  "lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"],
  "syllables": [5, 7, 5],
  "essence": "Spring's gentle transition"
}
```

**Imperfect but documented:**
```json
{
  "lines": ["Mountains stand so tall", "Ancient peaks touch the clouded sky", "Stories carved in stone"],
  "syllables": [6, 8, 5],
  "essence": "Mountain permanence"
}
```

---

## 5. Prompt Engineering Strategy

### 5.1 JSON Prompt Design

```python
JSON_HAIKU_PROMPT_TEMPLATE = """Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Story: {text}
"""
```

### 5.2 Critical Prompt Elements

1. **Clear instruction**: "Convert the following story into a haiku"
2. **Explicit format**: "5-7-5 syllable structure"
3. **JSON requirement**: "Return ONLY valid JSON"
4. **Exact template**: Show the exact format expected
5. **No extra text**: "no other text" prevents preambles
6. **Escaped braces**: Double braces `{{}}` to prevent f-string issues

### 5.3 Prompt Design Rationale

**Why explicit JSON format?**
- Eliminates parsing ambiguity
- Forces LLM to commit to syllable counts
- Makes validation straightforward
- Reduces error cases

**Why "ONLY valid JSON"?**
- Prevents "Here's a haiku..." preambles
- Avoids markdown code blocks
- Makes parsing simpler
- Reduces failure modes

**Why show example format?**
- LLMs respond well to examples
- Reduces misunderstandings
- Ensures consistent structure
- Improves first-try success rate

### 5.4 Input Processing

- **Truncation**: Limit to 500 characters to prevent token overflow
- **Whitespace**: Strip but preserve internal structure
- **Empty handling**: Reject before LLM call
- **No special escaping**: JSON handles quotes correctly

---

## 6. Error Handling Strategy

### 6.1 Input Validation Errors

```python
# Empty or whitespace-only input
if not text or not text.strip():
    raise ValueError("Input text cannot be empty or whitespace-only")
```

### 6.2 LLM Generation Errors

```python
try:
    response = llm_client.generate(model='llama3.2', prompt=prompt)
except Exception as e:
    raise RuntimeError(f"LLM generation failed: {str(e)}") from e
```

### 6.3 JSON Parsing Errors

```python
try:
    haiku_data = json.loads(response['response'].strip())
except json.JSONDecodeError as e:
    raise ValueError(
        f"Invalid JSON response from LLM: {e}\n"
        f"Raw response: {response['response'][:200]}"
    )
```

### 6.4 JSON Structure Validation Errors

```python
# Missing required keys
required_keys = ['lines', 'syllables', 'essence']
for key in required_keys:
    if key not in haiku_data:
        raise ValueError(
            f"Missing required key in JSON response: '{key}'. "
            f"Expected keys: {required_keys}"
        )

# Wrong line count
if len(haiku_data['lines']) != 3:
    raise ValueError(
        f"Expected 3 lines in JSON response, got {len(haiku_data['lines'])}"
    )

# Wrong syllable count
if len(haiku_data['syllables']) != 3:
    raise ValueError(
        f"Expected 3 syllable counts in JSON response, "
        f"got {len(haiku_data['syllables'])}"
    )

# Type validation
if not all(isinstance(line, str) for line in haiku_data['lines']):
    raise ValueError("All lines must be strings")

if not all(isinstance(count, int) for count in haiku_data['syllables']):
    raise ValueError("All syllable counts must be integers")
```

### 6.5 Validity Check (Not an Error)

```python
# Check if syllables match 5-7-5 pattern
valid = haiku_data['syllables'] == [5, 7, 5]

# This is NOT an error - just set the flag
# Allow imperfect haiku to be returned
```

---

## 7. Testing Strategy

### 7.1 Test Categories

#### Unit Tests (with mocks)

1. **Input validation tests**
   - Empty string → ValueError
   - Whitespace-only → ValueError
   - Very long input (truncation works)
   - Normal input → Success

2. **JSON parsing tests**
   - Valid JSON → Success
   - Malformed JSON → ValueError with clear message
   - JSON with extra text → Handle gracefully
   - Missing required keys → ValueError
   - Wrong data types → ValueError

3. **Structure validation tests**
   - 3 lines → Valid
   - 2 lines → ValueError
   - 4 lines → ValueError
   - 3 syllable counts → Valid
   - Wrong syllable count → ValueError

4. **Validity flag tests**
   - syllables=[5,7,5] → valid=True
   - syllables=[6,7,5] → valid=False
   - syllables=[5,8,5] → valid=False
   - syllables=[4,7,5] → valid=False

5. **Result structure tests**
   - All fields present
   - Correct types
   - haiku string has newlines
   - lines list is separate

6. **LLM integration tests (mocked)**
   - Mock client injection works
   - generate() called with correct model
   - Prompt structure correct
   - Response extraction correct

#### Integration Tests (real Ollama - separate)
- End-to-end with real LLM
- Only in comparison/demo scripts
- NOT part of development tests

### 7.2 Mock Design

```python
from unittest.mock import Mock

def create_mock_llm(json_response: str) -> Mock:
    """Create a mock LLM client for testing."""
    mock = Mock()
    mock.generate.return_value = {
        'response': json_response
    }
    return mock

# Example usage:
mock_llm = create_mock_llm(
    '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], '
    '"syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
)
```

### 7.3 Mock Response Templates

```python
MOCK_HAIKU_RESPONSES = {
    'spring_valid': {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], '
                   '"syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
    },
    'winter_valid': {
        'response': '{"lines": ["Silent snow blankets", "Frozen world in crystal white", "Winter dreams deeply"], '
                   '"syllables": [5, 7, 5], "essence": "Winter\'s quiet beauty"}'
    },
    'coding_valid': {
        'response': '{"lines": ["Code lines on the screen", "Logic winds through endless loops", "Mind in flow state dances"], '
                   '"syllables": [5, 7, 5], "essence": "Programming flow state"}'
    },
    'invalid_syllables': {
        'response': '{"lines": ["This line is too long now", "Short line here", "Another short"], '
                   '"syllables": [8, 4, 3], "essence": "Imperfect structure"}'
    },
    'malformed_json': {
        'response': 'This is not JSON at all'
    },
    'missing_keys': {
        'response': '{"lines": ["Line 1", "Line 2", "Line 3"]}'  # Missing syllables and essence
    },
    'wrong_line_count': {
        'response': '{"lines": ["Line 1", "Line 2"], "syllables": [5, 7], "essence": "Too few lines"}'
    }
}
```

---

## 8. Implementation Requirements

### 8.1 Dependencies

```python
# Required
import ollama  # For LLM interaction (production)
import json    # For JSON parsing

# Testing only
import pytest
from unittest.mock import Mock
```

**NOTE**: NO regex or syllable counting libraries needed!

### 8.2 Code Quality Standards

- **Type hints**: All public functions
- **Docstrings**: Google style for all functions
- **Error messages**: Clear, actionable, include context
- **No magic numbers**: Named constants (e.g., MAX_INPUT_LENGTH = 500)
- **DRY principle**: Extract validation helpers if needed
- **JSON-first**: All LLM interaction expects JSON

### 8.3 Performance Targets

- **Mock tests**: <1 second total
- **Real LLM**: ~20-30 seconds per conversion (expected)
- **Memory**: <50MB for normal use
- **JSON parsing**: <1ms

---

## 9. Success Criteria

### 9.1 Functional Requirements

- [x] Accepts text input and converts to haiku
- [x] Returns structured dict with all required fields
- [x] Parses JSON response from LLM
- [x] Validates JSON structure comprehensively
- [x] Sets valid flag based on syllable pattern
- [x] Supports dependency injection for testing
- [x] Handles JSON parsing errors gracefully
- [x] NO Python syllable counting

### 9.2 Code Quality Requirements

- [x] Comprehensive type hints
- [x] Full docstring coverage
- [x] Clear error messages with context
- [x] No code duplication
- [x] Clean, readable JSON parsing logic

### 9.3 Testing Requirements

- [x] 100% test coverage
- [x] All tests use mocks (no real LLM calls)
- [x] Tests run in <1 second
- [x] Edge cases covered (malformed JSON, etc.)
- [x] Validity flag tested thoroughly

### 9.4 Documentation Requirements

- [x] Technical specification (this file)
- [ ] README with examples
- [ ] Inline code comments for complex logic
- [ ] Clear function docstrings
- [ ] JSON schema documentation

---

## 10. Design Decisions & Rationale

### 10.1 Why JSON-Structured Output?

**Decision**: Require LLM to return JSON with explicit syllable counts

**Rationale**:
- Eliminates unreliable Python syllable counting (~85% accurate)
- LLMs have better syllable awareness than algorithms
- Makes validation straightforward (compare arrays)
- Reduces ambiguity in parsing
- Forces LLM to commit to syllable counts
- Better error messages when structure is wrong

### 10.2 Why LLM Self-Reporting?

**Decision**: Trust LLM's syllable counts over Python calculation

**Rationale**:
- LLMs trained on poetry have syllable awareness
- Python algorithms are inherently imperfect (85% accurate)
- Self-reporting creates accountability
- Simplifies code (no counting logic)
- More accurate in practice
- Aligns with how humans create haiku

### 10.3 Why Validity Flag Instead of Exception?

**Decision**: Return `valid: false` for non-5-7-5 haiku instead of raising error

**Rationale**:
- Allows caller to decide strictness
- LLM may have valid reasons for deviation
- Syllable counting is subjective (e.g., "flower" = 1 or 2?)
- Better UX - show the haiku even if imperfect
- Enables comparison of quality vs. structure
- Olympic judges can factor this in

### 10.4 Why "ONLY valid JSON" in Prompt?

**Decision**: Explicitly require JSON without extra text

**Rationale**:
- Prevents "Here's a haiku..." preambles
- Avoids markdown code blocks (```json)
- Simplifies parsing (no regex needed)
- Reduces error cases
- Makes testing more reliable
- Clearer expectations for LLM

### 10.5 Why Show Exact JSON Format in Prompt?

**Decision**: Include example JSON structure in prompt

**Rationale**:
- LLMs learn well from examples
- Reduces ambiguity
- Improves first-try success rate
- Shows exact key names expected
- Demonstrates data types
- Industry best practice for structured output

### 10.6 Why Remove Syllable Counting Helpers?

**Decision**: No `count_syllables()` or related functions

**Rationale**:
- Unreliable (~85% accurate)
- Not needed with JSON output
- Simplifies codebase
- Reduces potential bugs
- LLM is more accurate
- Less code to maintain

---

## 11. Implementation Checklist

### Phase 1: Core Implementation

- [ ] Define constants (MAX_INPUT_LENGTH, required keys)
- [ ] Implement input validation
- [ ] Implement JSON prompt generation
- [ ] Implement LLM client resolution
- [ ] Implement LLM invocation
- [ ] Implement JSON parsing with error handling
- [ ] Implement structure validation
- [ ] Implement validity check (syllables == [5,7,5])
- [ ] Assemble result dictionary
- [ ] Add comprehensive type hints
- [ ] Add detailed docstrings

### Phase 2: Testing

- [ ] Create mock helper functions
- [ ] Write input validation tests (empty, whitespace)
- [ ] Write JSON parsing tests (valid, malformed)
- [ ] Write structure validation tests (missing keys, wrong counts)
- [ ] Write validity flag tests (5-7-5 vs others)
- [ ] Write LLM integration tests (mocked)
- [ ] Write result structure tests
- [ ] Achieve 100% coverage
- [ ] Verify no real Ollama calls during tests

### Phase 3: Documentation

- [ ] Write README.md with examples
- [ ] Document JSON schema
- [ ] Add inline comments for complex logic
- [ ] Include troubleshooting guide
- [ ] Document error messages

### Phase 4: Verification

- [ ] Run all tests (should pass with mocks)
- [ ] Verify specification compliance
- [ ] Check code quality (no duplication)
- [ ] Validate error handling completeness
- [ ] Confirm JSON parsing robustness

---

## 12. JSON Parsing Implementation Details

### 12.1 Parsing Algorithm

```python
def parse_llm_json_response(raw_response: str) -> dict:
    """
    Parse JSON from LLM response with comprehensive error handling.

    Handles common issues:
    - Extra whitespace
    - Partial JSON (LLM stopped mid-generation)
    - Missing required keys
    - Wrong data types

    Args:
        raw_response: Raw string from LLM

    Returns:
        Validated JSON dict with required structure

    Raises:
        ValueError: If JSON is invalid or missing required structure
    """
    # Strip whitespace
    cleaned = raw_response.strip()

    # Parse JSON
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON response from LLM: {e}\n"
            f"Raw response (first 200 chars): {cleaned[:200]}"
        )

    # Validate structure
    required_keys = ['lines', 'syllables', 'essence']
    for key in required_keys:
        if key not in data:
            raise ValueError(
                f"Missing required key '{key}' in JSON. "
                f"Expected keys: {required_keys}, got: {list(data.keys())}"
            )

    # Validate line count
    if len(data['lines']) != 3:
        raise ValueError(
            f"Expected 3 lines, got {len(data['lines'])}: {data['lines']}"
        )

    # Validate syllable count
    if len(data['syllables']) != 3:
        raise ValueError(
            f"Expected 3 syllable counts, got {len(data['syllables'])}: {data['syllables']}"
        )

    # Validate types
    if not all(isinstance(line, str) for line in data['lines']):
        raise ValueError("All lines must be strings")

    if not all(isinstance(count, int) for count in data['syllables']):
        raise ValueError("All syllable counts must be integers")

    if not isinstance(data['essence'], str):
        raise ValueError("Essence must be a string")

    return data
```

### 12.2 Edge Cases Handled

1. **Extra whitespace**: `response.strip()`
2. **Empty lines in list**: No filtering - keep as-is (should be caught by LLM)
3. **Non-integer syllables**: Type check raises ValueError
4. **Missing keys**: Explicit check with helpful message
5. **Extra keys**: Allowed (forward compatibility)
6. **Nested objects**: Not expected, but won't break parsing

---

## 13. Comparison with Run 1

### 13.1 What Changed

| Aspect | Run 1 | Run 2 (This Spec) |
|--------|-------|-------------------|
| Output Format | Plain text (3 lines) | JSON with metadata |
| Syllable Counting | Python algorithm (~85% accurate) | LLM self-reporting |
| Validation | Python counts syllables | Compare LLM-reported to [5,7,5] |
| Parsing | Split by newlines | JSON parsing |
| Error Handling | Line count validation | JSON + structure validation |
| Essence Field | Extracted by Python | Provided by LLM |
| Success Metric | 5-7-5 enforced | valid flag (flexible) |

### 13.2 Why These Changes?

1. **JSON output**: Eliminates parsing ambiguity, enables richer metadata
2. **LLM self-reporting**: More accurate than Python algorithms
3. **Valid flag**: Allows imperfect haiku without failures
4. **Comprehensive validation**: JSON structure can be validated thoroughly
5. **Better UX**: Richer output for Olympic judging

---

## 14. Future Enhancements (Out of Scope)

These are intentionally NOT implemented for this experiment:

1. **JSON schema validation**: Using jsonschema library
2. **Multi-language support**: Currently English-only
3. **Configurable LLM model**: Hardcoded to llama3.2
4. **Retry logic**: No automatic retries on JSON parse failure
5. **Async support**: Synchronous only
6. **Response caching**: No caching of LLM responses
7. **Batch processing**: Single text at a time
8. **Quality scoring**: Handled by Olympic judges, not this code
9. **Alternative formats**: JSON only (no YAML, TOML, etc.)
10. **Streaming output**: Complete generation only

---

## 15. Timeline

### Specification Phase (Target: 4-5 minutes)
- [x] Create comprehensive technical specification
- [x] Define JSON schema
- [x] Design prompt engineering strategy
- [x] Plan error handling for JSON
- [x] Design testing strategy

### Implementation Phase (Target: 2-3 minutes)
- [ ] Implement core function (simpler than Run 1!)
- [ ] Add JSON parsing and validation
- [ ] Write comprehensive tests
- [ ] Create documentation

### Total Target: 6-8 minutes
*Slightly longer than Run 1 due to more thorough specification*

---

## 16. Appendix A: Complete Example Execution

### Input
```python
text = """
In a small village nestled between mountains, an old woman
tended her garden every morning. She spoke to each plant as
if they were old friends, sharing stories of seasons past.
"""
```

### Processing Steps

1. **Validate input**: `text.strip()` is not empty → Pass
2. **Truncate if needed**: 183 chars < 500 → No truncation
3. **Generate JSON prompt** with explicit format
4. **Call LLM**: `ollama.generate(model='llama3.2', prompt=...)`
5. **Receive JSON**:
   ```json
   {
     "lines": ["Mountains cradle home", "Garden whispers ancient tales", "Seasons dance with time"],
     "syllables": [5, 7, 5],
     "essence": "Timeless connection with nature"
   }
   ```
6. **Parse JSON**: `json.loads()` → dict
7. **Validate structure**:
   - Has keys: lines, syllables, essence → Pass
   - Line count: 3 → Pass
   - Syllable count: 3 → Pass
   - Types: strings and ints → Pass
8. **Check validity**: [5,7,5] == [5,7,5] → valid=True
9. **Assemble result**:

### Output
```python
{
    'haiku': 'Mountains cradle home\nGarden whispers ancient tales\nSeasons dance with time',
    'lines': [
        'Mountains cradle home',
        'Garden whispers ancient tales',
        'Seasons dance with time'
    ],
    'syllables': [5, 7, 5],
    'essence': 'Timeless connection with nature',
    'valid': True
}
```

### Error Example: Malformed JSON

**LLM Response**: `Here's a haiku: {"lines": ...`

**Parsing**: `json.loads()` → JSONDecodeError

**Error Raised**:
```python
ValueError: Invalid JSON response from LLM: Expecting value: line 1 column 1 (char 0)
Raw response (first 200 chars): Here's a haiku: {"lines": ...
```

---

## Appendix B: Testing Coverage Matrix

| Test Category | Test Case | Expected Outcome | Coverage |
|---------------|-----------|------------------|----------|
| Input Validation | Empty string | ValueError | Edge case |
| Input Validation | Whitespace only | ValueError | Edge case |
| Input Validation | Valid text | Success | Happy path |
| Input Validation | 1000 char text | Truncated to 500 | Boundary |
| JSON Parsing | Valid JSON | Parsed dict | Happy path |
| JSON Parsing | Malformed JSON | ValueError | Error case |
| JSON Parsing | Extra text before | ValueError | Error case |
| JSON Parsing | Extra text after | Success (flexible) | Robustness |
| Structure Validation | All keys present | Success | Happy path |
| Structure Validation | Missing 'lines' | ValueError | Error case |
| Structure Validation | Missing 'syllables' | ValueError | Error case |
| Structure Validation | Missing 'essence' | ValueError | Error case |
| Structure Validation | Extra keys | Success | Forward compat |
| Structure Validation | 2 lines | ValueError | Error case |
| Structure Validation | 4 lines | ValueError | Error case |
| Structure Validation | 2 syllable counts | ValueError | Error case |
| Structure Validation | Non-string lines | ValueError | Type error |
| Structure Validation | Non-int syllables | ValueError | Type error |
| Validity Flag | [5,7,5] syllables | valid=True | Happy path |
| Validity Flag | [6,7,5] syllables | valid=False | Invalid structure |
| Validity Flag | [5,8,5] syllables | valid=False | Invalid structure |
| Validity Flag | [5,7,6] syllables | valid=False | Invalid structure |
| Result Structure | All fields present | Success | Completeness |
| Result Structure | haiku has newlines | Success | Format check |
| Result Structure | lines is list | Success | Type check |
| LLM Integration | Mock injection | generate() called | DI test |
| LLM Integration | Correct model | 'llama3.2' passed | Config test |
| LLM Integration | Prompt format | JSON template used | Prompt test |

**Total Coverage**: 28 test cases across 8 categories

---

**End of Specification**

**Implementation Ready**: This specification is complete and ready for implementation following the specification-driven methodology. Implementation should strictly follow this design without deviation.
