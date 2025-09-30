# Technical Specification: Story-to-Haiku Converter
## Method 2: Specification-Driven Implementation

**Version**: 1.0
**Date**: 2025-09-30
**Author**: Method 2 - Specification-Driven Approach

---

## 1. Overview

### 1.1 Purpose
Convert arbitrary text into a haiku poem using Ollama's llama3.2 model with JSON structured output. The LLM self-reports syllable counts, eliminating need for Python syllable counting libraries.

### 1.2 Key Design Principles
1. **Specification-first**: Design before implementation
2. **Dependency injection**: Testable architecture
3. **Comprehensive validation**: Handle all edge cases
4. **Enterprise-ready**: Production-quality error handling
5. **Fast testing**: Mock-based test suite

---

## 2. Architecture

### 2.1 Component Design

```
┌─────────────────────────────────────────┐
│         story_to_haiku()                │
│                                         │
│  1. Input Validation                    │
│  2. LLM Client Resolution               │
│  3. Prompt Construction                 │
│  4. LLM Invocation                      │
│  5. JSON Parsing & Validation           │
│  6. Response Construction               │
└─────────────────────────────────────────┘
```

### 2.2 Data Flow

```
Input Text
    ↓
[Validation] → Error if invalid
    ↓
[LLM Client] → Default or Injected
    ↓
[Prompt] → JSON-formatted request
    ↓
[Ollama] → Generate haiku with metadata
    ↓
[Parse JSON] → Extract structure
    ↓
[Validate] → Check 5-7-5 pattern
    ↓
Output Dict
```

---

## 3. Interface Specification

### 3.1 Function Signature

```python
def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem.

    Args:
        text: Input story or paragraph (non-empty string)
        llm_client: Optional LLM client for dependency injection
                   If None, creates default Ollama client

    Returns:
        dict containing:
            - haiku: str - Complete haiku with newlines
            - lines: list[str] - Three haiku lines
            - syllables: list[int] - LLM-reported counts [5, 7, 5]
            - essence: str - Captured theme/idea
            - valid: bool - Whether syllables match [5, 7, 5]

    Raises:
        ValueError: If text is empty or whitespace-only
        RuntimeError: If LLM invocation fails
        json.JSONDecodeError: If LLM response is not valid JSON
        KeyError: If required JSON keys are missing
    """
```

### 3.2 Expected JSON Response Format

The LLM must return JSON in this exact structure:

```json
{
  "lines": [
    "Cherry blossoms fall",
    "Softly on the quiet pond",
    "Spring whispers arrive"
  ],
  "syllables": [5, 7, 5],
  "essence": "Spring's gentle transition"
}
```

---

## 4. Detailed Requirements

### 4.1 Input Validation
- **MUST** reject empty strings
- **MUST** reject whitespace-only strings
- **MUST** accept any non-empty text
- **SHOULD** handle very long texts (truncate if needed)

### 4.2 LLM Client Management
- **MUST** support dependency injection via `llm_client` parameter
- **MUST** create default Ollama client if `llm_client` is None
- **MUST** use llama3.2 model
- **MUST** configure JSON response format

### 4.3 Prompt Engineering
- **MUST** instruct LLM to return JSON only
- **MUST** specify exact JSON structure
- **MUST** request syllable self-reporting
- **MUST** emphasize 5-7-5 syllable pattern
- **SHOULD** provide clear instructions about essence field

### 4.4 JSON Processing
- **MUST** parse LLM response as JSON
- **MUST** validate presence of required keys: lines, syllables, essence
- **MUST** validate lines is list of 3 strings
- **MUST** validate syllables is list of 3 integers
- **MUST** validate essence is non-empty string
- **SHOULD** provide helpful error messages on validation failure

### 4.5 Syllable Validation
- **MUST** check if syllables match [5, 7, 5] pattern
- **MUST** set valid=True if pattern matches
- **MUST** set valid=False if pattern doesn't match
- **MUST NOT** reject haiku if pattern doesn't match (still return result)

### 4.6 Response Construction
- **MUST** construct haiku string by joining lines with newlines
- **MUST** return all required dictionary keys
- **MUST** maintain exact format specified in interface

---

## 5. Error Handling Strategy

### 5.1 Error Categories

| Error Type | Handling Strategy | User Impact |
|------------|-------------------|-------------|
| Empty input | Raise ValueError immediately | Clear error message |
| LLM failure | Raise RuntimeError with details | Actionable feedback |
| JSON parse error | Raise with LLM response context | Debug information |
| Missing keys | Raise KeyError with specifics | Clear missing field |
| Invalid structure | Raise TypeError with details | Type information |

### 5.2 Error Messages
All error messages **MUST** be:
- Clear and actionable
- Include context (what was expected vs received)
- Help user understand how to fix the issue

---

## 6. Testing Strategy

### 6.1 Test Categories

1. **Unit Tests** (with mocks)
   - Input validation
   - JSON parsing
   - Syllable validation
   - Response construction

2. **Integration Tests** (with mocks)
   - Full function flow
   - Error handling paths
   - Edge cases

3. **Mock Strategy**
   - Mock LLM client returns pre-defined JSON strings
   - Tests run in milliseconds
   - No Ollama dependency for CI/CD

### 6.2 Test Cases

| Test Case | Input | Expected Behavior |
|-----------|-------|-------------------|
| Valid input | Story text + valid mock | Returns complete dict |
| Empty input | "" | Raises ValueError |
| Whitespace input | "   " | Raises ValueError |
| Valid 5-7-5 | Mock [5,7,5] | valid=True |
| Invalid syllables | Mock [4,8,5] | valid=False, still returns |
| Malformed JSON | Mock "{invalid" | Raises JSONDecodeError |
| Missing keys | Mock without "lines" | Raises KeyError |
| Wrong types | Mock with int for lines | Raises TypeError |

### 6.3 Mock Implementation

```python
class MockLLM:
    def __init__(self, response_json):
        self.response_json = response_json

    def chat(self, model, messages, format):
        class MockResponse:
            def __init__(self, content):
                self.message = {'content': content}
        return MockResponse(self.response_json)
```

---

## 7. Implementation Guidelines

### 7.1 Code Structure

```python
# 1. Imports
import json
import ollama

# 2. Main Function
def story_to_haiku(text: str, llm_client=None) -> dict:
    # Step 1: Validate input
    # Step 2: Initialize LLM client
    # Step 3: Construct prompt
    # Step 4: Invoke LLM
    # Step 5: Parse JSON
    # Step 6: Validate structure
    # Step 7: Construct response
    # Step 8: Return result
```

### 7.2 Style Guidelines
- Use type hints throughout
- Document each step with comments
- Keep functions focused (single responsibility)
- Use descriptive variable names
- Follow PEP 8 conventions

### 7.3 Prompt Template

```python
PROMPT_TEMPLATE = """Convert the following text into a haiku poem with exactly 5-7-5 syllable structure.

Text: {text}

Return ONLY valid JSON in this exact format:
{{
  "lines": ["line1", "line2", "line3"],
  "syllables": [5, 7, 5],
  "essence": "brief description of the captured theme"
}}

Count syllables carefully for each line. Return only the JSON, no other text."""
```

---

## 8. Performance Considerations

### 8.1 Latency
- LLM call: ~2-5 seconds (acceptable for this use case)
- JSON parsing: <1ms
- Validation: <1ms
- Total: Dominated by LLM latency

### 8.2 Optimization Opportunities
- Cache LLM client (reuse across calls)
- Implement timeout for LLM calls
- Consider async version for batch processing

---

## 9. Dependencies

### 9.1 Required Packages
```
ollama>=0.1.0
```

### 9.2 Python Version
- Minimum: Python 3.8
- Recommended: Python 3.10+

---

## 10. Success Metrics

### 10.1 Functional Completeness
- ✅ All requirements implemented
- ✅ All error cases handled
- ✅ All tests passing

### 10.2 Code Quality
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Clear error messages
- ✅ PEP 8 compliant

### 10.3 Test Coverage
- ✅ >90% code coverage
- ✅ All edge cases tested
- ✅ Fast test execution (<100ms)

---

## 11. Future Enhancements

### 11.1 Potential Improvements
1. Support for different models (not just llama3.2)
2. Support for different poetry forms (sonnet, limerick, etc.)
3. Async version for batch processing
4. Retry logic with exponential backoff
5. Syllable count verification using external library
6. Support for multi-language haiku

### 11.2 Not in Scope
- Syllable counting in Python (LLM self-reports)
- Complex poetry analysis
- UI/CLI interface (function-level only)
- Database persistence

---

## 12. Appendix

### 12.1 Example Usage

```python
# Basic usage
result = story_to_haiku("The old pond, a frog jumps in, water's sound.")
print(result['haiku'])
print(f"Valid 5-7-5: {result['valid']}")

# With dependency injection (testing)
mock_client = MockLLM('{"lines": ["test", "test", "test"], "syllables": [5,7,5], "essence": "test"}')
result = story_to_haiku("Any text", llm_client=mock_client)
```

### 12.2 References
- Ollama Python SDK: https://github.com/ollama/ollama-python
- JSON Schema Validation: https://json-schema.org/
- Haiku Structure: https://en.wikipedia.org/wiki/Haiku

---

**End of Specification**
