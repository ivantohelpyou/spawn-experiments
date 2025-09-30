# Experiment 1.608: Story-to-Haiku Converter

**Date**: 2025-09-30

**Domain**: 1.6XX - Ollama Integration Functions

**Complexity**: Tier 1 - Simple Function

**Demo**: AI Tinkerers Seattle - September 30, 2025

---

## Problem Statement

Create a Python function that converts a story or paragraph into a haiku (5-7-5 syllable structure) using a local LLM via Ollama.

## Function Signature

```python
def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem.

    Args:
        text: Input story or paragraph
        llm_client: Optional LLM client (for testing with mocks)

    Returns:
        dict with:
            - haiku: str (the complete haiku with newlines)
            - lines: list[str] (three lines)
            - syllable_counts: list[int] (should be [5, 7, 5])
            - essence: str (what core idea was captured)
    """
```

## Requirements

### Functional Requirements
1. Accept text input of any reasonable length
2. Use Ollama with llama3.2 model to generate haiku
3. Parse the LLM response into structured format
4. Validate syllable counts (5-7-5 pattern)
5. Handle edge cases (empty input, very long input)

### Design Requirements
**CRITICAL**: Must support dependency injection for testing
- Accept optional `llm_client` parameter
- Default to real Ollama when None
- Allow mock injection during tests

### Testing Strategy
**Use mocks during development for fast parallel execution**:
- Tests should inject mock LLM client
- Mock returns pre-defined haiku responses
- Tests validate structure, not poetic quality
- Real Ollama only used in comparison script

## Example Usage

### Production Use (Real Ollama)
```python
result = story_to_haiku("""
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
""")

print(result['haiku'])
# Output:
# Mountains cradle home
# Garden whispers ancient tales
# Seasons dance with time
```

### Test Use (Mocked)
```python
from unittest.mock import Mock

mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Mountains cradle home\nGarden whispers ancient tales\nSeasons dance with time'
}

result = story_to_haiku("Long story...", llm_client=mock_llm)
assert result['syllable_counts'] == [5, 7, 5]
```

## Test Cases

### Basic Functionality
```python
def test_returns_three_lines():
    # Use mock LLM
    result = story_to_haiku("A story about spring")
    assert len(result['lines']) == 3

def test_validates_syllable_structure():
    result = story_to_haiku("A story about winter")
    assert result['syllable_counts'] == [5, 7, 5]

def test_includes_complete_haiku_string():
    result = story_to_haiku("A story about autumn")
    assert '\n' in result['haiku']
    assert result['haiku'].count('\n') == 2
```

### Edge Cases
```python
def test_empty_input_raises_error():
    with pytest.raises(ValueError):
        story_to_haiku("")

def test_very_long_input_truncated():
    long_story = "word " * 1000
    result = story_to_haiku(long_story)
    # Should handle gracefully

def test_whitespace_only_raises_error():
    with pytest.raises(ValueError):
        story_to_haiku("   \n\n   ")
```

### LLM Integration
```python
def test_uses_provided_llm_client():
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': 'Test haiku line one\nTest haiku line two longer\nTest haiku line three'
    }

    story_to_haiku("test", llm_client=mock_llm)

    # Verify mock was called
    mock_llm.generate.assert_called_once()
```

## Mock Response Templates

For consistent testing, use these mock responses:

```python
MOCK_HAIKU_RESPONSES = {
    'spring': {
        'response': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive'
    },
    'winter': {
        'response': 'Silent snow blankets\nFrozen world in crystal white\nWinter dreams deeply'
    },
    'autumn': {
        'response': 'Leaves paint gold and red\nFalling gently to the earth\nAutumn bids farewell'
    },
    'coding': {
        'response': 'Code lines on the screen\nLogic winds through endless loops\nMind in flow state dances'
    }
}
```

## Ollama Integration Pattern

```python
import ollama

def story_to_haiku(text: str, llm_client=None) -> dict:
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real client if none provided
    if llm_client is None:
        llm_client = ollama

    # Generate haiku
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).
Return only the haiku, one line per line, no other text.

Story: {text[:500]}  # Truncate long inputs

Haiku:"""

    response = llm_client.generate(
        model='llama3.2',
        prompt=prompt
    )

    # Parse response
    haiku_text = response['response'].strip()
    lines = [line.strip() for line in haiku_text.split('\n') if line.strip()]

    # Validate structure
    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    # Count syllables (simplified - actual implementation would be more robust)
    syllable_counts = [count_syllables(line) for line in lines]

    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllable_counts': syllable_counts,
        'essence': extract_essence(text)  # Optional helper
    }
```

## Comparison Script

After all 4 methods complete, run this script with **real Ollama** to demonstrate:

```python
# methodology_comparison_demo.py
import time
from importlib import import_module

TEST_STORIES = [
    "In a small village between mountains, an old woman tended her garden...",
    "A young programmer sat late at night, debugging code that refused to work...",
    "The ocean waves crashed against ancient cliffs, carved by millennia..."
]

print("=== Story-to-Haiku Methodology Comparison ===\n")

for method_num in [1, 2, 3, 4]:
    print(f"\n--- Method {method_num} ---")
    module = import_module(f"{method_num}-*")  # Import method implementation

    for i, story in enumerate(TEST_STORIES, 1):
        print(f"\nStory {i}:")
        start = time.time()
        result = module.story_to_haiku(story)  # Real Ollama call
        elapsed = time.time() - start

        print(result['haiku'])
        print(f"Syllables: {result['syllable_counts']}")
        print(f"Time: {elapsed:.1f}s")
```

## Success Criteria

### Minimum Viable
- ✅ Accepts text input
- ✅ Returns 3-line structure
- ✅ Integrates with Ollama
- ✅ Passes basic tests with mocks

### Complete Implementation
- ✅ Validates syllable counts
- ✅ Handles edge cases
- ✅ Provides clean error messages
- ✅ Supports dependency injection
- ✅ Includes comprehensive tests

### Methodology Comparison Goals
- Show how each methodology approaches LLM integration
- Compare prompt engineering strategies
- Contrast testing approaches
- Demonstrate code organization differences

## Time Estimates

### Development Time (with mocks)
- Method 1 (Immediate): 2-3 minutes
- Method 2 (Specification): 4-5 minutes
- Method 3 (Test-First): 3-4 minutes
- Method 4 (Adaptive TDD): 3-4 minutes

**Parallel execution**: 4-5 minutes total

### Demo Time (real Ollama)
- Comparison script: 2-3 minutes (4 methods × 1 story × ~20s each)
- Code review: 1-2 minutes
- **Total**: Under 5 minutes

## Notes for Demo

### Pre-Demo Setup
1. ✅ Ollama installed and running
2. ✅ llama3.2 model pulled (2GB)
3. ✅ Python environment with ollama package
4. ✅ Test that Ollama responds (<30s)

### Demo Flow
1. **[0:00-0:30]** Explain the problem
2. **[0:30-4:00]** Spawn all 4 methods in parallel
3. **[4:00-4:30]** Show code differences
4. **[4:30-5:00]** Run comparison with real Ollama
5. **[5:00+]** Discuss results

### Talking Points
- Mocking enables parallel execution
- Each methodology handles LLM integration differently
- Testing non-deterministic outputs requires different strategies
- Real AI integration proven at the end

---

## Related Documents
- [Ollama Experiments Series](../../../docs/OLLAMA_EXPERIMENTS_SERIES.md)
- [Experiment Numbering System](../../../docs/EXPERIMENT_NUMBERING_SYSTEM.md)
- [Contributing Guide](../../../CONTRIBUTING.md)