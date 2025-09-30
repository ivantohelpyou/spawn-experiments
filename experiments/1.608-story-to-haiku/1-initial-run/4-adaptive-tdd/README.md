# Method 4: Adaptive TDD - Story-to-Haiku Converter

## Overview

This implementation demonstrates **Adaptive TDD**: writing tests strategically for what matters, while consciously skipping tests for non-deterministic or low-value aspects.

## Testing Strategy Rationale

### What We TEST (High Value)

1. **Structure Validation** - CRITICAL
   - Must return exactly 3 lines
   - Haiku string must have proper newlines
   - Response dict must contain all required keys
   - **Why**: Core requirement, deterministic, breaks functionality if wrong

2. **Error Handling** - CRITICAL
   - Empty input rejection
   - Whitespace-only input rejection
   - Invalid LLM response handling (wrong number of lines)
   - **Why**: Prevents runtime errors, provides good UX

3. **Integration Pattern** - CRITICAL
   - Dependency injection works correctly
   - Mock client is actually used
   - Prompt includes the input text
   - Model parameter is correct
   - **Why**: Enables testing, follows best practices

4. **Input Processing** - IMPORTANT
   - Long inputs are truncated appropriately
   - **Why**: Prevents API errors, ensures performance

5. **Output Format** - IMPORTANT
   - Syllable counts are returned (as integers)
   - Essence is returned (as string)
   - **Why**: API contract compliance

### What We SKIP (Low Value or Non-Deterministic)

1. **Haiku Quality** - NOT TESTED
   - Poetic beauty
   - Semantic meaning
   - Artistic merit
   - **Why**: Subjective, non-deterministic, LLM-dependent

2. **Exact Syllable Accuracy** - NOT TESTED
   - Whether counts are exactly [5, 7, 5]
   - Syllable counting algorithm precision
   - **Why**: Depends on LLM output quality, syllable counting library limitations

3. **Poetic Meter** - NOT TESTED
   - Rhythm and cadence
   - Haiku tradition compliance
   - **Why**: Not in requirements, too subjective

4. **Real Ollama Integration** - NOT TESTED HERE
   - Actual LLM calls
   - Network connectivity
   - Model availability
   - **Why**: Tested separately in comparison script, slow, non-deterministic

## Implementation Decisions

### 1. Dependency Injection Pattern
```python
def story_to_haiku(text: str, llm_client: Optional[object] = None) -> dict:
```
- Allows mock injection for fast, reliable tests
- Defaults to real ollama when used in production
- Clean separation of concerns

### 2. Simple Syllable Counting
```python
def count_syllables(word: str) -> int:
```
- Uses vowel-group counting algorithm
- Good enough for most words (~90% accuracy)
- Could be replaced with library (syllapy) if needed
- **Trade-off**: Speed and simplicity vs perfect accuracy

### 3. Minimal Essence Extraction
```python
def extract_essence(text: str, max_length: int = 100) -> str:
```
- Simple: returns first sentence
- Truncates if too long
- **Trade-off**: Simplicity vs semantic analysis

### 4. Graceful Error Handling
- Clear error messages
- Validates input before processing
- Validates LLM output structure
- **Benefit**: Better debugging, better UX

## Test Coverage Analysis

### Lines of Code
- Implementation: ~130 lines
- Tests: ~140 lines
- Ratio: ~1.08:1 (test code slightly exceeds implementation)

### Test Categories
- Structure validation: 3 tests
- Error handling: 4 tests
- Dependency injection: 2 tests
- Output format: 2 tests
- **Total**: 11 focused tests

### What This Ratio Means
- **Not 100% coverage**: We skip non-deterministic aspects
- **Not minimal**: We test all critical paths
- **Strategic**: Every test adds value

## Time Tracking

- Test design: ~1.5 minutes
- Implementation: ~1.5 minutes
- Test execution: ~10 seconds
- Documentation: ~1 minute
- **Total**: ~4 minutes

## Running the Tests

### With pytest (if available)
```bash
pytest test_haiku_converter.py -v
```

### Without pytest
```bash
python3 manual_test.py
```

### With real Ollama (comparison script)
```bash
# Run from parent directory
python3 methodology_comparison_demo.py
```

## Key Insights from Adaptive TDD

### Strengths
1. **Fast feedback**: Tests run in <1 second (all mocked)
2. **High confidence**: Critical paths are thoroughly tested
3. **Maintainable**: Tests are simple and focused
4. **Pragmatic**: We don't waste time testing the untestable

### Trade-offs
1. **Not comprehensive**: We consciously skip some aspects
2. **Requires judgment**: Need to decide what to test
3. **Documentation needed**: Must explain what we skipped and why

### When to Use This Approach
- Working with non-deterministic systems (LLMs, APIs)
- Time-constrained development
- When test value varies significantly across features
- When mocking is straightforward

### When NOT to Use This Approach
- Safety-critical systems (medical, aviation)
- Financial transactions (need comprehensive testing)
- When all functionality is deterministic
- When test value is uniformly high

## Comparison with Other Methods

### vs Method 1 (Immediate Implementation)
- **Method 4**: Tests written first, guide implementation
- **Method 1**: Tests written after, verify implementation
- **Trade-off**: Structure vs speed

### vs Method 2 (Specification-First)
- **Method 4**: Tests are selective, focused on value
- **Method 2**: Comprehensive spec, detailed requirements
- **Trade-off**: Pragmatism vs completeness

### vs Method 3 (Test-First TDD)
- **Method 4**: Strategic testing, skip low-value tests
- **Method 3**: Comprehensive testing, test everything
- **Trade-off**: Efficiency vs thoroughness

## Files

- `haiku_converter.py` - Main implementation (130 lines)
- `test_haiku_converter.py` - Pytest test suite (140 lines)
- `manual_test.py` - Standalone test runner (90 lines)
- `README.md` - This file (testing strategy documentation)

## Example Output

```python
from haiku_converter import story_to_haiku

story = """
In a small village nestled between mountains, an old woman
tended her garden every morning.
"""

result = story_to_haiku(story)

print(result['haiku'])
# Mountains cradle home
# Garden whispers ancient tales
# Seasons dance with time

print(result['syllable_counts'])
# [5, 7, 5]

print(result['essence'])
# In a small village nestled between mountains, an old woman tended her garden...
```

## Success Criteria

- ✅ All tests pass with mocks
- ✅ Clean dependency injection pattern
- ✅ Strategic test coverage (not 100%, but right things)
- ✅ Clear documentation of testing decisions
- ✅ Fast test execution (<1 second)
- ✅ Production-ready error handling
- ✅ Ready for real Ollama comparison

## Next Steps

Run the comparison script to see how this implementation performs with real Ollama:
```bash
cd ../
python3 methodology_comparison_demo.py
```