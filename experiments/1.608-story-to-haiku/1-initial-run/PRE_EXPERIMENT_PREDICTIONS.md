# PRE-EXPERIMENT PREDICTIONS
**Experiment**: 1.608 Story-to-Haiku Converter
**Date**: September 30, 2025
**Baseline**: LLM-powered function that converts stories to haiku using Ollama (llama3.2), with dependency injection for testing

## Methodology Predictions

### Method 1 (Immediate Implementation)
**Expected Outcome**: Quick integration with basic ollama call and minimal parsing
**Predicted Lines**: ~80-120 lines
**Predicted Time**: 2-3 minutes
**Predicted Issues**: May skip syllable validation, minimal error handling, might not use dependency injection
**Architecture**: Single function with direct ollama import, basic string splitting
**Strengths**: Fast to implement, gets working quickly
**Weaknesses**: Likely hardcoded ollama dependency (hard to test), minimal validation, weak error handling

### Method 2 (Specification-Driven)
**Expected Outcome**: Over-engineered solution with extensive prompt engineering documentation
**Predicted Lines**: ~250-400 lines (includes separate prompt templates, validation classes)
**Predicted Time**: 5-7 minutes
**Predicted Issues**: Will likely create abstract LLM client interface, multiple validation layers, extensive configuration
**Architecture**: Multiple classes (HaikuGenerator, SyllableCounter, PromptBuilder, LLMClient interface), configuration files
**Strengths**: Well-documented, highly testable, production-ready architecture
**Weaknesses**: Massive over-engineering for a simple function, scope creep

### Method 3 (Test-First Development)
**Expected Outcome**: Clean implementation driven by test requirements, good use of mocks
**Predicted Lines**: ~120-180 lines (code + tests)
**Predicted Time**: 3-4 minutes
**Predicted Issues**: May discover prompt engineering challenges through test failures, iterative refinement
**Architecture**: Function with dependency injection, clear separation of LLM call vs parsing logic
**Strengths**: Good test coverage with mocks, discovers edge cases naturally
**Weaknesses**: May not optimize prompt on first pass

### Method 4 (Adaptive TDD)
**Expected Outcome**: Balanced approach with strategic testing where it matters
**Predicted Lines**: ~100-150 lines
**Predicted Time**: 3-4 minutes
**Predicted Issues**: Will balance between testing structure vs testing LLM output quality
**Architecture**: Clean function with dependency injection, focused tests on structure not content
**Strengths**: Pragmatic testing strategy, good balance of speed and quality
**Weaknesses**: May defer some edge case handling

## Overall Predictions

### Winner Prediction
**Method 4 (Adaptive TDD)** will likely produce the best solution
- **Rationale**: This problem has clear structural requirements (3 lines, syllable counts) but fuzzy content requirements (poetic quality). Adaptive TDD will test structure rigorously while appropriately deferring LLM quality assessment to manual review
- Method 3 would be close second, but may spend time on tests that don't add value (testing poetic quality)
- Method 2 will massively over-engineer for a Tier 1 function

### Methodology Rankings (Predicted)
1. **Method 4 (Adaptive TDD)** - Best balance for LLM integration
2. **Method 3 (TDD)** - Good structure, may over-test
3. **Method 1 (Immediate)** - Works but hard to test
4. **Method 2 (Specification)** - Severe over-engineering expected

### Expected Surprises
- **Method 1** might skip dependency injection entirely, making it untestable with mocks
- **Method 2** could create 5+ classes for a single function problem
- **Method 3** might waste time trying to write tests for "haiku quality"
- **Method 4** will likely nail the mock strategy immediately

### Common Challenges
- **Dependency injection pattern**: Making ollama mockable during tests
- **Prompt engineering**: Getting consistent 5-7-5 syllable output
- **Response parsing**: Handling varied LLM response formats
- **Syllable counting**: Implementing accurate syllable validation (surprisingly hard)
- **Testing strategy**: What to test with mocks vs what requires real LLM

### Expected Patterns
- All methods should use ollama.generate() with llama3.2 model
- Mock usage will be the key differentiator for parallel execution speed
- Test coverage will vary dramatically (Method 2 > Method 3 > Method 4 > Method 1)
- Code complexity will likely follow: Method 1 < Method 4 < Method 3 << Method 2

## Specific Technical Predictions

### Dependency Injection Implementation
- **Method 1**: No dependency injection - direct `import ollama` (untestable)
- **Method 2**: Abstract LLMClient interface with factory pattern (over-engineered)
- **Method 3**: Function parameter `llm_client=None` with mock examples in tests
- **Method 4**: Function parameter `llm_client=None`, minimal but sufficient

### Mock Strategy
- **Method 1**: No mocks - will call real ollama in tests (slow, breaks parallel execution)
- **Method 2**: Elaborate mock framework with multiple test fixtures
- **Method 3**: unittest.mock.Mock with comprehensive mock scenarios
- **Method 4**: Simple mocks for structure validation, skip content validation

### Syllable Counting
- **Method 1**: May skip syllable validation entirely
- **Method 2**: Will implement full syllable counting algorithm with phoneme dictionary
- **Method 3**: Basic syllable counter driven by test requirements
- **Method 4**: May use simplified heuristic or defer to LLM prompt quality

### Prompt Engineering
- **Method 1**: Simple one-liner prompt
- **Method 2**: Extensive prompt template system with multiple variations
- **Method 3**: Prompt refined through test iterations
- **Method 4**: Good prompt on first try, refined if tests fail

### Error Handling
- **Method 1**: Minimal - might crash on empty input
- **Method 2**: Comprehensive error hierarchy (EmptyInputError, InvalidHaikuError, LLMConnectionError, etc.)
- **Method 3**: Error cases driven by test edge cases (empty input, whitespace, malformed LLM response)
- **Method 4**: Essential errors only (ValueError for empty input)

## Novel Aspects for Ollama Series

### Testing Non-Deterministic Outputs
This is the first experiment exploring **local LLM integration**, which introduces unique challenges:

**Key Insight**: You cannot test LLM output quality deterministically, only structure
- **Method 1**: Will likely ignore this problem
- **Method 2**: Might over-specify with confidence thresholds and quality metrics
- **Method 3**: May struggle initially, then pivot to structure-only tests
- **Method 4**: Will immediately focus on testable structure (line count, format)

### Parallel Execution with Mocks
**Critical for demo success**: Only methods that use mocks can execute in parallel without hitting the Ollama bottleneck

**Prediction**:
- **Method 1**: 2-3 min development + 2-3 min sequential test execution = 4-6 min (slowest)
- **Method 2**: 5-7 min development + instant mock tests = 5-7 min
- **Method 3**: 3-4 min development + instant mock tests = 3-4 min
- **Method 4**: 3-4 min development + instant mock tests = 3-4 min

**Parallel execution window**: Methods 2, 3, 4 can run simultaneously in ~5-7 minutes. Method 1 may lag if it uses real ollama in tests.

### Prompt Quality vs Code Quality
This experiment will reveal how methodologies handle the **prompt engineering** aspect:

**Hypothesis**: Specification-driven (Method 2) will spend disproportionate time on prompt design vs code, while TDD methods will iterate prompts pragmatically.

## Rationale

Story-to-haiku conversion is ideal for this experiment series because:
1. **Clear structure** (3 lines, 5-7-5 syllables) enables meaningful tests
2. **Fuzzy content** (poetic quality) tests methodology pragmatism
3. **LLM integration** requires dependency injection patterns
4. **Mock strategy** is essential for parallel execution (demo constraint)
5. **Audience appeal** - haiku is more engaging than validation functions

This problem should clearly differentiate between:
- Methods that over-test the untestable (poetic quality)
- Methods that under-test the testable (structure)
- Methods that strike the right balance

**Expected pattern**: Adaptive TDD (Method 4) will shine here because it knows what to test (structure) and what to defer (content quality).

## Meta-Prediction: Documentation Quality

Given this is the first Ollama experiment:
- **Method 2** will create extensive documentation about LLM integration patterns (valuable!)
- **Method 3** will have good inline comments and test documentation
- **Method 4** will have minimal but sufficient documentation
- **Method 1** will have minimal documentation

Interestingly, Method 2's documentation might be the most valuable artifact even if the code is over-engineered, as it could inform future Ollama experiments in the 1.6XX series.