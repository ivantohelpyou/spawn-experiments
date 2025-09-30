# Method 4: Adaptive TDD - Story to Haiku Converter

**Implementation Date**: 2025-09-30
**Methodology**: Adaptive Test-Driven Development
**Approach**: Strategic testing - focus effort where it matters most

---

## Adaptive TDD Philosophy

Adaptive TDD is pragmatic test-driven development:
- **Test complex/risky parts** where bugs are likely
- **Skip obvious/simple operations** that don't warrant coverage
- **Balance** testing effort with practical value
- **Achieve** optimal code quality without over-engineering

This is TDD for the real world - smart testing that maximizes ROI.

---

## Testing Strategy

### WHAT WE TESTED (Complex/Risky Areas)

#### 1. JSON Parsing (HIGH RISK)
LLMs can return malformed JSON or unexpected formats:
- Valid JSON parsing
- Malformed JSON handling
- Missing required keys
- Extra whitespace handling

**Why?** JSON parsing is a primary failure point when working with LLMs.

#### 2. Error Handling (COMPLEX)
Input validation and edge cases:
- Empty input rejection
- Whitespace-only input rejection
- Wrong number of lines
- Wrong number of syllable counts

**Why?** Edge cases are where bugs hide. Error handling requires careful thought.

#### 3. Validation Logic (CORE BUSINESS RULE)
Syllable structure validation:
- Correct 5-7-5 structure marked as valid
- Incorrect structure marked as invalid
- Haiku string formatting with newlines

**Why?** This is the core business logic. Getting it wrong defeats the purpose.

#### 4. Dependency Injection (CRITICAL FOR TESTABILITY)
Mock LLM integration:
- Mock client acceptance
- Correct model parameter
- Prompt contains input text
- All required keys in result

**Why?** Without testability, we can't write these other tests!

---

### WHAT WE SKIPPED (Simple/Obvious)

We deliberately did NOT test:
1. **String joining** with `'\n'.join()` - Python stdlib, trivial
2. **Dict construction** - Simple assignments, obvious
3. **Text truncation** - Basic string slicing `text[:500]`
4. **Default parameter** - Trivial `if llm_client is None`
5. **Prompt f-string** - Straightforward string formatting

**Why skip these?** They're:
- Simple operations with no complex logic
- Well-tested Python stdlib features
- Obvious enough that tests add no value
- Would slow development without benefit

---

## Test Results

```
============================================================
ADAPTIVE TDD - Manual Test Suite
============================================================

Running strategic tests (complex/risky areas only):

Test 1: Valid JSON parsing... PASS
Test 2: Malformed JSON handling... PASS
Test 3: Empty input rejection... PASS
Test 4: Whitespace input rejection... PASS
Test 5: Missing required keys... PASS
Test 6: Wrong line count... PASS
Test 7: Wrong syllable count... PASS
Test 8: Invalid syllable structure... PASS
Test 9: Dependency injection... PASS
Test 10: All required keys present... PASS

============================================================
All tests passed!
============================================================
```

**10 strategic tests** covering the complex/risky areas.
**0 tests** for obvious/simple operations.

---

## Implementation Highlights

### Code Structure
- **58 lines** of implementation (excluding imports/docstrings)
- **Clear separation** of concerns with inline comments
- **Strategic comments** marking tested vs untested areas
- **Error messages** designed to be helpful

### Key Design Decisions

1. **Conditional ollama import** - Allows testing without production dependencies
2. **Explicit validation** - Each check has clear error message
3. **Strip whitespace** from JSON before parsing
4. **Simple dict construction** - No over-engineering

### Example Comment Style
```python
# Validate input (tested - error handling is complex)
if not text or not text.strip():
    raise ValueError("Input text cannot be empty")

# Truncate long inputs (not tested - simple string slicing)
truncated_text = text[:500] if len(text) > 500 else text
```

This makes it clear WHY each decision was made.

---

## Files

- **haiku_converter.py** - Main implementation (95 lines)
- **test_haiku_converter.py** - Strategic test suite (160 lines)
- **manual_test.py** - Test runner without pytest dependency (145 lines)
- **README.md** - This documentation

---

## Usage

### With Mock (Testing)
```python
from unittest.mock import Mock
from haiku_converter import story_to_haiku

mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring transition"}'
}

result = story_to_haiku("A story about spring", llm_client=mock_llm)
print(result['haiku'])
# Cherry blossoms fall
# Softly on the quiet pond
# Spring whispers arrive
```

### With Real Ollama (Production)
```python
from haiku_converter import story_to_haiku

result = story_to_haiku("""
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
""")

print(result['haiku'])
print(f"Valid 5-7-5: {result['valid']}")
print(f"Essence: {result['essence']}")
```

---

## Adaptive TDD Benefits

### Speed
- Fast test execution (mocks only, no real LLM calls)
- Quick iteration cycle
- No wasted time testing trivial code

### Quality
- High confidence in complex areas
- Clear error messages
- Robust error handling

### Maintainability
- Tests document important behavior
- Easy to understand what's tested and why
- Simple to add tests for new complex features

### Balance
- Not under-tested (all risky areas covered)
- Not over-tested (no tests for obvious code)
- Optimal effort-to-value ratio

---

## Comparison to Other Methods

### vs Method 1 (Immediate Implementation)
- **More reliable**: Strategic tests catch edge cases
- **Similar speed**: Fast iteration with focused tests

### vs Method 2 (Specification-Driven)
- **Less documentation**: No separate spec document
- **More pragmatic**: Tests instead of exhaustive specs

### vs Method 3 (Test-First TDD)
- **Fewer tests**: Skip obvious operations
- **Better ROI**: Focus effort where it matters
- **Same quality**: Complex areas equally well-tested

---

## Adaptive TDD Summary

**When to use**: Most production code, especially with external dependencies

**Best for**:
- Systems with complex parsing/validation
- Code interacting with unreliable external systems
- Team codebases where maintainability matters
- Projects needing good test coverage without excessive effort

**Not ideal for**:
- Throwaway prototypes
- Trivial scripts with no error handling
- Code with 100% obvious logic

**Philosophy**: Test what matters, skip what doesn't. Pragmatic quality.

---

## Success Metrics

- All 10 strategic tests pass
- JSON parsing robust against LLM variations
- Error handling comprehensive
- Dependency injection enables fast testing
- Implementation clean and maintainable

**Result**: High-quality implementation with optimal test coverage in minimal time.

This is Adaptive TDD - smart testing for the real world.