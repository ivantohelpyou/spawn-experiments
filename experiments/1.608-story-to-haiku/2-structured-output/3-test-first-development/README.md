# Method 3: Test-First Development (TDD)

**Classic TDD**: Write ALL tests FIRST (using mocks), then implement to make tests pass.

## Approach

1. **RED Phase**: Write comprehensive tests BEFORE implementation
   - Used pytest framework with unittest.mock
   - Defined expected behavior through test cases
   - All tests initially fail (no implementation exists)

2. **GREEN Phase**: Implement minimum code to pass all tests
   - Implementation driven by test requirements
   - Each feature exists because a test demanded it
   - Code comments trace back to specific tests

3. **REFACTOR Phase**: Clean up while maintaining green tests
   - Tests act as safety net for refactoring
   - Can confidently improve code structure

## Test Strategy

### Test Organization (15 tests total)

**TestBasicFunctionality** (4 tests)
- Three line haiku structure
- Syllable validation (5-7-5)
- JSON response parsing
- Haiku string formatting

**TestJSONParsing** (5 tests)
- Malformed JSON handling
- Invalid syllable counts
- Missing required keys
- Wrong line counts
- Wrong syllable counts

**TestEdgeCases** (4 tests)
- Empty input validation
- Whitespace-only input
- Very long input truncation
- None input handling

**TestDependencyInjection** (2 tests)
- Mock client acceptance
- Prompt format validation

## Key Files

- `test_haiku_converter.py` - Written FIRST (defines behavior)
- `haiku_converter.py` - Written SECOND (implements behavior)
- `demo.py` - Demonstrates real Ollama integration

## Running Tests

```bash
# Run all tests with verbose output
venv/bin/pytest test_haiku_converter.py -v

# Run specific test class
venv/bin/pytest test_haiku_converter.py::TestBasicFunctionality -v

# Run with coverage
venv/bin/pytest test_haiku_converter.py --cov=haiku_converter
```

## Demo with Real Ollama

```bash
# Make sure Ollama is running and llama3.2 is available
ollama pull llama3.2

# Run demo
venv/bin/python demo.py
```

## TDD Benefits Demonstrated

1. **Clear Requirements**: Tests document expected behavior
2. **Design by Contract**: Function signature driven by tests
3. **Regression Safety**: Can refactor with confidence
4. **Fast Feedback**: Mocked tests run in milliseconds
5. **Comprehensive Coverage**: 15 tests cover all edge cases
6. **Dependency Injection**: Testability built into design

## Implementation Highlights

- **Every feature traced to a test**: Comments show which test drove each decision
- **Minimal implementation**: Only code needed to pass tests
- **Error handling**: Comprehensive based on test requirements
- **Validation**: Input, JSON structure, syllable counts all validated
- **Mock-friendly design**: LLM client injection enables fast testing

## Test Results

```
============================== test session starts ==============================
collected 15 items

test_haiku_converter.py::TestBasicFunctionality::test_returns_three_lines PASSED
test_haiku_converter.py::TestBasicFunctionality::test_validates_syllable_structure PASSED
test_haiku_converter.py::TestBasicFunctionality::test_parses_json_response PASSED
test_haiku_converter.py::TestBasicFunctionality::test_haiku_string_format PASSED
test_haiku_converter.py::TestJSONParsing::test_handles_malformed_json PASSED
test_haiku_converter.py::TestJSONParsing::test_handles_invalid_syllables PASSED
test_haiku_converter.py::TestJSONParsing::test_handles_missing_keys PASSED
test_haiku_converter.py::TestJSONParsing::test_handles_wrong_line_count PASSED
test_haiku_converter.py::TestJSONParsing::test_handles_wrong_syllable_count PASSED
test_haiku_converter.py::TestEdgeCases::test_empty_input_raises_error PASSED
test_haiku_converter.py::TestEdgeCases::test_whitespace_only_raises_error PASSED
test_haiku_converter.py::TestEdgeCases::test_very_long_input_truncated PASSED
test_haiku_converter.py::TestEdgeCases::test_none_input_raises_error PASSED
test_haiku_converter.py::TestDependencyInjection::test_accepts_mock_client PASSED
test_haiku_converter.py::TestDependencyInjection::test_prompt_format PASSED

============================== 15 passed in 0.02s ==============================
```

## Time Tracking

- **Test Writing**: ~3 minutes (15 comprehensive tests)
- **Implementation**: ~2 minutes (driven by tests)
- **Verification**: ~1 minute (all tests pass)
- **Total**: ~6 minutes (including setup)

## TDD Philosophy

> "Test-first code is born tested." - Kent Beck

In TDD, tests are not an afterthought - they are the specification. The implementation emerges naturally from the requirements expressed in tests. This method demonstrates that clear tests lead to clean, correct implementations.