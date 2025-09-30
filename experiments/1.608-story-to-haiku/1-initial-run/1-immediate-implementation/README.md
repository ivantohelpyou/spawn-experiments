# Story-to-Haiku Converter - Method 1: Immediate Implementation

**Method**: Jump straight into coding with minimal planning
**Time**: ~3 minutes
**Approach**: Get it working FAST

## Usage

```python
from haiku_converter import story_to_haiku

# With real Ollama (requires ollama installed and running)
result = story_to_haiku("""
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
""")

print(result['haiku'])
print(f"Syllables: {result['syllable_counts']}")
```

## With Mock LLM (for testing)

```python
from unittest.mock import Mock
from haiku_converter import story_to_haiku

# Create mock
mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive'
}

# Use mock
result = story_to_haiku("A story about spring", llm_client=mock_llm)
print(result['haiku'])
```

## Run Tests

```bash
python run_tests.py
```

## Features

- Converts stories to haikus using Ollama/llama3.2
- Counts syllables (approximate algorithm)
- Validates 3-line structure
- Handles edge cases (empty input, long text)
- Supports dependency injection for testing

## Implementation Notes

**What worked:**
- Immediate coding got a working solution quickly
- Simple syllable counter (good enough for demo)
- Mock-based testing works great for fast iteration

**Decisions made:**
- Used simplified syllable counting (not perfect but fast to implement)
- Truncate long inputs at 500 chars
- Extract "essence" as first 5 words (quick and simple)
- Minimal error handling (just what's needed)

**Time breakdown:**
- Core function: 1 minute
- Syllable counter: 1 minute
- Tests: 1 minute
- Fixes/polish: ~30 seconds
- **Total: ~3 minutes**