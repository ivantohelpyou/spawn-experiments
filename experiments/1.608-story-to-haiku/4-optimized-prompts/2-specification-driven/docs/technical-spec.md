# Technical Specification: Story-to-Haiku Converter
## Method 2: Specification-Driven Development
### Experiment 1.608 - Run 4 (Optimized Prompts)

**Date**: 2025-09-30

**Version**: 1.0

**Method**: Specification-Driven (Comprehensive Planning First)

---

## 1. Executive Summary

This document provides a comprehensive technical specification for implementing a story-to-haiku converter using Ollama LLM integration with optimized prompt engineering. The specification follows Method 2's principle of detailed planning before implementation.

**Key Innovation**: Enhanced prompt templates with explicit syllable counting instructions, clear examples, and structured guidance to improve haiku quality over Run 3.

---

## 2. System Architecture

### 2.1 High-Level Design

```
┌─────────────────┐
│  User Input     │
│  (Story Text)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  story_to_haiku()                       │
│  ┌───────────────────────────────────┐  │
│  │ 1. Input Validation               │  │
│  │ 2. Prompt Construction (Optimized)│  │
│  │ 3. LLM Invocation (Ollama)        │  │
│  │ 4. JSON Response Parsing          │  │
│  │ 5. Syllable Validation            │  │
│  │ 6. Result Structuring             │  │
│  └───────────────────────────────────┘  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Structured     │
│  Haiku Output   │
│  (Dict)         │
└─────────────────┘
```

### 2.2 Component Breakdown

#### Component 1: Input Validator
- **Purpose**: Validate and sanitize input text
- **Inputs**: Raw text string
- **Outputs**: Validated text or error
- **Error Conditions**: Empty string, None, whitespace-only

#### Component 2: Optimized Prompt Builder
- **Purpose**: Construct enhanced prompt with explicit instructions
- **Key Features**:
  - Explicit syllable counting guidance
  - Clear structural rules (5-7-5)
  - Example haiku with syllable breakdown
  - Essence extraction guidance
  - JSON format specification
- **Inputs**: Validated text
- **Outputs**: Fully-formed prompt string

#### Component 3: LLM Interface
- **Purpose**: Communicate with Ollama API
- **Dependency Injection**: Accept optional llm_client parameter
- **Default Behavior**: Create Ollama client if none provided
- **Mock Support**: Use injected client during testing
- **Model**: llama3.2
- **Format**: JSON mode

#### Component 4: JSON Parser
- **Purpose**: Parse and validate LLM response
- **Required Keys**: lines, syllables, essence
- **Validation**:
  - Valid JSON structure
  - All required keys present
  - Correct data types
  - Lines is list of 3 strings
  - Syllables is list of 3 integers
  - Essence is non-empty string

#### Component 5: Syllable Validator
- **Purpose**: Validate 5-7-5 structure
- **Inputs**: Syllable list from LLM
- **Outputs**: Boolean validity flag
- **Validation**: Must be exactly [5, 7, 5]

#### Component 6: Result Assembler
- **Purpose**: Create standardized output dictionary
- **Output Structure**:
```python
{
    "haiku": str,          # Complete haiku with newlines
    "lines": list[str],    # Three lines
    "syllables": list[int],# [5, 7, 5] (LLM-reported)
    "essence": str,        # Captured theme/idea
    "valid": bool          # Whether syllables match 5-7-5
}
```

---

## 3. Optimized Prompt Engineering

### 3.1 Prompt Template Structure

The optimized prompt includes:

1. **Role Assignment**: "You are a skilled haiku poet"
2. **Story Context**: Clear presentation of input text
3. **Structural Rules**: Explicit 5-7-5 requirements with emphasis
4. **Syllable Counting Guide**:
   - Examples of syllable breakdown
   - Instruction to verify counts
5. **Essence Capture Guidance**:
   - "Capture the essence in a single vivid moment"
   - Focus on emotion, theme, or core image
6. **Concrete Example**:
   - Sample story input
   - Expected haiku output
   - Proper JSON formatting
7. **Output Format Specification**: JSON-only instruction

### 3.2 Complete Prompt Template

```
You are a skilled haiku poet. Convert the following story into a traditional haiku.

STORY:
{text}

HAIKU STRUCTURE RULES:
- Line 1: Exactly 5 syllables
- Line 2: Exactly 7 syllables
- Line 3: Exactly 5 syllables
- Capture the essence of the story in a single vivid moment

SYLLABLE COUNTING:
- Count each syllable carefully (e.g., "beautiful" = beau-ti-ful = 3 syllables)
- Verify your counts before finalizing

EXAMPLE FORMAT:
Story: "On a foggy morning, an old fisherman cast his net into the sea"
Haiku:
{
  "lines": [
    "Fog wraps the shoreline",
    "Old hands cast nets through the mist",
    "Sea holds its secrets"
  ],
  "syllables": [5, 7, 5],
  "essence": "The timeless ritual of fishing in mysterious morning fog"
}

Now create your haiku, returning ONLY valid JSON in the format above.
```

### 3.3 Improvements Over Run 3

| Aspect | Run 3 | Run 4 (Optimized) |
|--------|-------|-------------------|
| Syllable Instructions | Generic | Explicit with examples |
| Structure Guidance | Basic mention | Clear rules with emphasis |
| Examples | None or minimal | Complete example provided |
| Essence Guidance | Implied | Explicit instruction |
| Format Specification | JSON request | JSON format with example |

---

## 4. Error Handling Strategy

### 4.1 Error Categories

#### Category 1: Input Errors
- **Error**: Empty or None input
- **Response**: Return error dict with descriptive message
- **Recovery**: Not applicable (user error)

#### Category 2: LLM Communication Errors
- **Error**: Ollama connection failure, timeout
- **Response**: Raise descriptive exception
- **Recovery**: Retry logic (optional enhancement)

#### Category 3: JSON Parsing Errors
- **Error**: Malformed JSON, missing keys
- **Response**: Return error dict with parse details
- **Recovery**: Attempt to extract partial data (optional)

#### Category 4: Validation Errors
- **Error**: Invalid syllable counts, wrong structure
- **Response**: Include in output with valid=False
- **Recovery**: Return data as-is with validity flag

### 4.2 Error Response Format

```python
{
    "error": str,          # Error description
    "haiku": "",           # Empty string
    "lines": [],           # Empty list
    "syllables": [],       # Empty list
    "essence": "",         # Empty string
    "valid": False         # Always False for errors
}
```

---

## 5. Testing Strategy

### 5.1 Test Architecture

**Philosophy**: Use mocks for fast, parallel test execution during development. Real Ollama only used in final comparison.

```
┌──────────────────────────┐
│   Test Suite             │
│  ┌────────────────────┐  │
│  │ Mock LLM Client    │  │ ← Injected during tests
│  └────────────────────┘  │
│  ┌────────────────────┐  │
│  │ story_to_haiku()   │  │
│  └────────────────────┘  │
│  ┌────────────────────┐  │
│  │ Assertions         │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

### 5.2 Test Cases

#### Test 1: Valid Haiku Generation
- **Input**: Sample story
- **Mock Response**: Valid JSON with 5-7-5 structure
- **Assertions**:
  - All keys present
  - Haiku string formatted correctly
  - Lines list has 3 elements
  - Syllables list is [5, 7, 5]
  - valid=True

#### Test 2: Invalid Syllable Counts
- **Input**: Sample story
- **Mock Response**: JSON with incorrect syllables [4, 8, 5]
- **Assertions**:
  - Data parsed correctly
  - valid=False
  - Syllables match mock response

#### Test 3: Malformed JSON
- **Input**: Sample story
- **Mock Response**: Invalid JSON string
- **Assertions**:
  - Error dict returned
  - error key contains descriptive message
  - valid=False

#### Test 4: Missing JSON Keys
- **Input**: Sample story
- **Mock Response**: JSON missing "essence" key
- **Assertions**:
  - Error dict returned
  - Error describes missing key
  - valid=False

#### Test 5: Empty Input
- **Input**: Empty string
- **Mock Response**: Not called
- **Assertions**:
  - Error dict returned immediately
  - Error describes empty input
  - valid=False

#### Test 6: Whitespace-Only Input
- **Input**: "   \n\t  "
- **Mock Response**: Not called
- **Assertions**:
  - Error dict returned
  - Error describes empty input
  - valid=False

#### Test 7: Real Ollama Integration
- **Input**: Sample story
- **Mock Response**: None (uses real Ollama)
- **Assertions**:
  - Successful communication
  - Response structure valid
  - (Note: Run separately, not in main suite)

### 5.3 Mock Implementation

```python
class MockLLMClient:
    def __init__(self, response_data):
        self.response_data = response_data
        self.call_count = 0

    def chat(self, model, messages, format):
        self.call_count += 1
        return {
            'message': {
                'content': json.dumps(self.response_data)
            }
        }
```

---

## 6. Data Structures

### 6.1 Input Structure

```python
# Function parameter
text: str  # Story or paragraph to convert
llm_client: Optional[Any]  # Optional mock/real LLM client
```

### 6.2 LLM Response Structure (Expected)

```python
{
    "lines": [str, str, str],      # Three haiku lines
    "syllables": [int, int, int],  # Syllable counts
    "essence": str                 # Captured theme
}
```

### 6.3 Output Structure

```python
{
    "haiku": str,              # Formatted haiku (lines joined with \n)
    "lines": [str, str, str],  # Individual lines
    "syllables": [int, int, int],  # Syllable counts [5, 7, 5]
    "essence": str,            # Story essence/theme
    "valid": bool              # True if syllables are [5, 7, 5]
}
```

### 6.4 Error Structure

```python
{
    "error": str,              # Error description
    "haiku": "",               # Empty
    "lines": [],               # Empty
    "syllables": [],           # Empty
    "essence": "",             # Empty
    "valid": False             # Always False
}
```

---

## 7. Implementation Details

### 7.1 Function Signature

```python
def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem using optimized prompts.

    This function uses Ollama (llama3.2) with enhanced prompt engineering
    to generate high-quality haiku poems that capture the essence of input
    stories while adhering to traditional 5-7-5 syllable structure.

    Args:
        text: Input story or paragraph to convert into haiku.
              Must be non-empty string with meaningful content.
        llm_client: Optional LLM client for dependency injection.
                   If None, creates real Ollama client.
                   Used for testing with mocks.

    Returns:
        dict: Structured haiku result with keys:
            - haiku (str): Complete haiku with newline separators
            - lines (list[str]): Three individual haiku lines
            - syllables (list[int]): LLM-reported syllable counts
            - essence (str): Captured theme or core idea
            - valid (bool): True if syllables match [5, 7, 5]

        On error, returns dict with 'error' key and empty values.

    Raises:
        Exception: If Ollama communication fails (connection errors, etc.)

    Examples:
        >>> result = story_to_haiku("A bird flew across the sky")
        >>> print(result['haiku'])
        Wings slice through blue air
        Feathered freedom gliding high
        Sky holds its secrets

        >>> result['valid']
        True
    """
```

### 7.2 Key Implementation Notes

1. **Input Validation First**: Always validate before LLM call
2. **Dependency Injection**: Support both real and mock clients
3. **Explicit Error Handling**: Try-except at each stage
4. **Structured Logging**: Clear error messages for debugging
5. **Type Hints**: Use type annotations for clarity
6. **Docstrings**: Comprehensive documentation

### 7.3 Dependencies

```
ollama==0.1.6    # Ollama Python client
pytest==7.4.3    # Testing framework
```

---

## 8. Quality Metrics

### 8.1 Code Quality

- **Test Coverage**: >90% line coverage
- **Documentation**: Comprehensive docstrings
- **Type Hints**: All public functions annotated
- **Error Handling**: All edge cases covered
- **Code Style**: PEP 8 compliant

### 8.2 Functional Quality

- **Haiku Validity**: Target >80% valid 5-7-5 structure
- **Aesthetic Quality**: Improved Olympic judging scores vs Run 3
- **Response Time**: <5 seconds per conversion
- **Error Rate**: <5% JSON parsing failures

---

## 9. Future Enhancements

### 9.1 Potential Improvements

1. **Retry Logic**: Automatic retry on JSON parse failures
2. **Fallback Parsing**: Extract partial data from malformed responses
3. **Prompt A/B Testing**: Compare multiple prompt variations
4. **Caching**: Cache results for identical inputs
5. **Streaming**: Support streaming responses for long inputs
6. **Multi-Model**: Support multiple LLM backends

### 9.2 Out of Scope (Current Implementation)

- Python-based syllable counting (spec requires LLM counting)
- Post-processing to fix syllable counts (preserve LLM output)
- Multiple haiku generation (single output only)
- Language support beyond English

---

## 10. Acceptance Criteria

### 10.1 Minimum Viable Product

- ✅ Accepts text input and returns structured dict
- ✅ Uses optimized prompt template from spec
- ✅ Integrates with Ollama (llama3.2)
- ✅ Parses JSON responses correctly
- ✅ Validates syllable structure
- ✅ Handles basic errors gracefully
- ✅ Passes test suite with mocks
- ✅ Supports dependency injection

### 10.2 Complete Implementation

- ✅ All edge cases handled
- ✅ Comprehensive error messages
- ✅ Full test coverage (>90%)
- ✅ Production-ready code quality
- ✅ Clear documentation
- ✅ Improved haiku quality vs Run 3
- ✅ Implementation summary documented

---

## 11. Design Decisions

### 11.1 Key Decisions

| Decision | Rationale |
|----------|-----------|
| LLM syllable counting | Spec requirement; tests LLM accuracy |
| Dependency injection | Enables fast mock testing |
| Return dict not exception | Better error handling UX |
| Optimized prompt template | Hypothesis: Better prompts = better haiku |
| JSON-only response | Structured, parseable output |
| No retry logic | Keep initial implementation simple |

### 11.2 Trade-offs

| Choice | Benefit | Cost |
|--------|---------|------|
| Mock-based testing | Fast parallel execution | Doesn't test real LLM |
| Detailed prompt | Better haiku quality | Longer token usage |
| Explicit examples | Clearer LLM guidance | More verbose prompt |
| Dict return format | Flexible error handling | Requires key checking |

---

## 12. Implementation Checklist

- [ ] Create project directory structure
- [ ] Create technical specification (this document)
- [ ] Implement story_to_haiku() function
- [ ] Implement optimized prompt builder
- [ ] Implement JSON parser
- [ ] Implement validation logic
- [ ] Create mock LLM client
- [ ] Write comprehensive test suite (6+ tests)
- [ ] Create requirements.txt
- [ ] Create README.md
- [ ] Create IMPLEMENTATION_SUMMARY.md
- [ ] Run test suite and verify >90% coverage
- [ ] Document design decisions
- [ ] Prepare for Olympic judging comparison

---

## 13. References

- [Experiment Spec](../EXPERIMENT_SPEC.md)
- [Run 3 Implementation](../../3-clean-room/)
- [Meta Prompt Generator V4](/home/ivanadamin/spawn-experiments/META_PROMPT_GENERATOR_V4.md)
- [Haiku Poetry Guidelines](https://en.wikipedia.org/wiki/Haiku)

---

**END OF SPECIFICATION**

*This specification follows Method 2 (Specification-Driven) principles: comprehensive planning before implementation, detailed documentation, and production-ready design.*
