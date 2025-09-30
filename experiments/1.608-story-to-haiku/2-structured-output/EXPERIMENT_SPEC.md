# Experiment 1.608 - Run 2: Story-to-Haiku Converter
## Structured Output with Olympic Judging

**Date**: 2025-09-30

**Run**: 2 of 2 (Structured JSON output + Olympic judging)

**Domain**: 1.6XX - Ollama Integration Functions

**Complexity**: Tier 1 - Simple Function

---

## Problem Statement

Create a Python function that converts a story or paragraph into a haiku (5-7-5 syllable structure) using Ollama (llama3.2), with **structured JSON output** where the LLM self-reports syllable counts.

**Key Changes from Run 1**:
- ✅ LLM returns JSON with self-reported syllable counts
- ✅ No Python syllable counting (learned it's unreliable)
- ✅ Comparison script includes Olympic-style judging system
- ✅ Multiple models judge haiku quality

---

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
            - haiku: str (complete haiku with newlines)
            - lines: list[str] (three lines)
            - syllables: list[int] (LLM-reported counts [5, 7, 5])
            - essence: str (captured theme/idea)
            - valid: bool (whether syllables match 5-7-5)
    """
```

---

## Requirements

### Functional Requirements
1. Accept text input of any reasonable length
2. Use Ollama with llama3.2 to generate JSON-formatted haiku
3. **LLM must self-report syllable counts** (no Python counting!)
4. Parse JSON response into structured format
5. Validate that syllables match [5, 7, 5]
6. Handle edge cases (empty input, malformed JSON, invalid syllables)

### Prompt Requirements

**CRITICAL**: Your prompt must instruct the LLM to return JSON in this exact format:

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

**Example prompt structure**:
```python
prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Story: {truncated_text}
"""
```

### Design Requirements
**Must support dependency injection for testing**:
- Accept optional `llm_client` parameter
- Default to real Ollama when None
- Allow mock injection during tests

### Testing Strategy
**Use mocks during development for fast parallel execution**:
- Tests should inject mock LLM client
- Mock returns pre-defined JSON responses
- Tests validate structure and JSON parsing
- Real Ollama only used in comparison script

---

## Olympic Judging System

**IMPORTANT**: After all 4 methods generate haiku, the comparison script will run an Olympic-style judging phase:

### Judging Process (in comparison script, not your code)

1. **Collect all 4 haiku outputs** from Methods 1-4
2. **Multiple judge models** evaluate the haiku:
   - llama3.2 (the generator - can it judge fairly?)
   - phi3:mini (lightweight, different perspective)
   - gemma2:2b (third perspective)
3. **Scoring criteria**:
   - Adherence to 5-7-5 structure
   - Capture of story essence
   - Poetic quality
   - Imagery and language
4. **Olympic scoring**: Drop highest and lowest, average the rest
5. **Winner declared** with reasoning

**You do NOT need to implement judging** - just make sure your haiku output is good quality for the judges!

---

## Example Usage

### Production Use (Real Ollama)
```python
result = story_to_haiku("""
    In a small village nestled between mountains, an old woman
    tended her garden every morning. She spoke to each plant as
    if they were old friends, sharing stories of seasons past.
""")

print(result)
# {
#   'haiku': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive',
#   'lines': ['Cherry blossoms fall', 'Softly on the quiet pond', 'Spring whispers arrive'],
#   'syllables': [5, 7, 5],
#   'essence': 'Spring\'s gentle transition',
#   'valid': True
# }
```

### Test Use (Mocked)
```python
from unittest.mock import Mock

mock_llm = Mock()
mock_llm.generate.return_value = {
    'response': '''{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring's transition"}'''
}

result = story_to_haiku("Long story...", llm_client=mock_llm)
assert result['valid'] == True
assert result['syllables'] == [5, 7, 5]
```

---

## Test Cases

### Basic Functionality
```python
def test_returns_three_lines():
    # Use mock LLM with JSON response
    result = story_to_haiku("A story about spring")
    assert len(result['lines']) == 3

def test_validates_syllable_structure():
    result = story_to_haiku("A story about winter")
    assert result['syllables'] == [5, 7, 5]
    assert result['valid'] == True

def test_parses_json_response():
    result = story_to_haiku("A story about autumn")
    assert 'lines' in result
    assert 'syllables' in result
    assert 'essence' in result
```

### JSON Parsing
```python
def test_handles_malformed_json():
    # Mock returns invalid JSON
    mock_llm = Mock()
    mock_llm.generate.return_value = {'response': 'not json at all'}

    with pytest.raises(ValueError, match="Invalid JSON"):
        story_to_haiku("test", llm_client=mock_llm)

def test_handles_invalid_syllables():
    # Mock returns wrong syllable counts
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': '{"lines": ["a", "b", "c"], "syllables": [3, 4, 3], "essence": "test"}'
    }

    result = story_to_haiku("test", llm_client=mock_llm)
    assert result['valid'] == False
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

---

## Mock Response Templates

For consistent testing, use these mock JSON responses:

```python
MOCK_HAIKU_RESPONSES = {
    'spring': {
        'response': '{"lines": ["Cherry blossoms fall", "Softly on the quiet pond", "Spring whispers arrive"], "syllables": [5, 7, 5], "essence": "Spring\'s gentle transition"}'
    },
    'winter': {
        'response': '{"lines": ["Silent snow blankets", "Frozen world in crystal white", "Winter dreams deeply"], "syllables": [5, 7, 5], "essence": "Winter\'s quiet beauty"}'
    },
    'autumn': {
        'response': '{"lines": ["Leaves paint gold and red", "Falling gently to the earth", "Autumn bids farewell"], "syllables": [5, 7, 5], "essence": "Autumn\'s colorful goodbye"}'
    },
    'coding': {
        'response': '{"lines": ["Code lines on the screen", "Logic winds through endless loops", "Mind in flow state dances"], "syllables": [5, 7, 5], "essence": "Programming flow state"}'
    }
}
```

---

## Implementation Pattern

```python
import ollama
import json

def story_to_haiku(text: str, llm_client=None) -> dict:
    # Validate input
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")

    # Use real client if none provided
    if llm_client is None:
        llm_client = ollama

    # Truncate long inputs
    truncated_text = text[:500] if len(text) > 500 else text

    # Generate haiku with JSON output format
    prompt = f"""Convert the following story into a haiku (5-7-5 syllable structure).

Return ONLY valid JSON in this exact format (no other text):
{{
  "lines": ["line 1", "line 2", "line 3"],
  "syllables": [5, 7, 5],
  "essence": "core theme"
}}

Story: {truncated_text}
"""

    response = llm_client.generate(
        model='llama3.2',
        prompt=prompt
    )

    # Parse JSON response
    try:
        haiku_data = json.loads(response['response'].strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from LLM: {e}")

    # Validate structure
    required_keys = ['lines', 'syllables', 'essence']
    for key in required_keys:
        if key not in haiku_data:
            raise ValueError(f"Missing required key in response: {key}")

    lines = haiku_data['lines']
    syllables = haiku_data['syllables']

    if len(lines) != 3:
        raise ValueError(f"Expected 3 lines, got {len(lines)}")

    if len(syllables) != 3:
        raise ValueError(f"Expected 3 syllable counts, got {len(syllables)}")

    # Check if syllables match 5-7-5
    valid = syllables == [5, 7, 5]

    return {
        'haiku': '\n'.join(lines),
        'lines': lines,
        'syllables': syllables,
        'essence': haiku_data['essence'],
        'valid': valid
    }
```

---

## Comparison Script (Olympic Judging)

**NOTE**: You don't implement this - it's in the comparison script. But understand what it does:

```python
# After collecting haiku from all 4 methods:
def judge_haiku(story, all_haiku, judge_model='phi3:mini'):
    """Have a judge model rate all 4 haiku."""

    prompt = f"""You are judging 4 haiku generated from this story:
"{story}"

Rate each haiku (1-10) on:
- Adherence to 5-7-5 structure (worth 3 points)
- Capture of story essence (worth 3 points)
- Poetic quality/imagery (worth 4 points)

Haiku 1: {all_haiku[0]}
Haiku 2: {all_haiku[1]}
Haiku 3: {all_haiku[2]}
Haiku 4: {all_haiku[3]}

Return JSON:
{{
  "scores": [score1, score2, score3, score4],
  "winner": N,
  "reasoning": "why this haiku won"
}}
"""

    response = ollama.generate(model=judge_model, prompt=prompt)
    return json.loads(response['response'])

# Get judgments from 3 models
judges = ['llama3.2', 'phi3:mini', 'gemma2:2b']
all_scores = []

for judge in judges:
    judgment = judge_haiku(story, all_haiku, judge)
    all_scores.append(judgment['scores'])

# Olympic scoring: drop highest and lowest for each method
final_scores = []
for method_idx in range(4):
    method_scores = [scores[method_idx] for scores in all_scores]
    method_scores_sorted = sorted(method_scores)
    # Drop highest and lowest
    middle_scores = method_scores_sorted[1:-1]
    final_scores.append(sum(middle_scores) / len(middle_scores))

winner = final_scores.index(max(final_scores)) + 1
print(f"Winner: Method {winner} with score {max(final_scores)}")
```

---

## Success Criteria

### Minimum Viable
- ✅ Accepts text input
- ✅ Returns structured dict with all required keys
- ✅ Parses JSON from LLM
- ✅ Validates syllable structure
- ✅ Integrates with Ollama
- ✅ Passes basic tests with mocks

### Complete Implementation
- ✅ Handles malformed JSON gracefully
- ✅ Validates all required JSON keys
- ✅ Handles edge cases
- ✅ Provides clear error messages
- ✅ Supports dependency injection
- ✅ Includes comprehensive tests
- ✅ Prompt generates valid JSON consistently

### Methodology Comparison Goals
- Show how each methodology approaches JSON parsing
- Compare error handling strategies
- Contrast prompt engineering approaches
- Demonstrate testing of structured outputs

---

## Time Estimates

### Development Time (with mocks)
- Method 1 (Immediate): 2-3 minutes (faster than Run 1, pattern established)
- Method 2 (Specification): 4-5 minutes (less over-engineering expected)
- Method 3 (Test-First): 3-4 minutes (JSON parsing adds clarity)
- Method 4 (Adaptive TDD): 2-3 minutes (will shine with clear structure)

**Parallel execution**: 4-5 minutes total (faster than Run 1)

### Demo Time
- Comparison script with judging: 3-4 minutes (4 generations + 3 judges)
- Code review: 1 minute
- **Total**: Under 5 minutes ✅

---

## Key Improvements from Run 1

1. **Structured Output**: JSON eliminates syllable counting problems
2. **LLM Self-Reporting**: Trust the model's syllable awareness
3. **Olympic Judging**: Multi-model quality evaluation
4. **Clearer Prompts**: Explicit JSON format requirement
5. **Better Error Handling**: JSON parsing failures well-defined
6. **Faster Development**: Patterns established from Run 1

---

## Notes for Demo

### Pre-Demo Setup
1. ✅ Ollama installed and running
2. ✅ llama3.2 model pulled (2GB)
3. ✅ Judge models pulled: phi3:mini (2.2GB), gemma2:2b (1.6GB)
4. ✅ Python environment with ollama package
5. ✅ Test that JSON responses work

### Demo Flow
1. **[0:00-0:30]** Explain Run 2 improvements (JSON, judging)
2. **[0:30-4:00]** Spawn all 4 methods in parallel
3. **[4:00-4:30]** Run comparison + olympic judging
4. **[4:30-5:00]** Announce winner and discuss

### Talking Points
- JSON output solves syllable counting problem
- Olympic judging shows AI evaluating AI
- Multiple models provide diverse perspectives
- Methodology affects code structure, not haiku quality

---

## Related Documents
- [Run 1 Experiment Report](../1-initial-run/EXPERIMENT_REPORT.md)
- [Ollama Experiments Series](../../../docs/OLLAMA_EXPERIMENTS_SERIES.md)
- [Original Experiment Spec](../1-initial-run/EXPERIMENT_SPEC.md)
- [Pre-Experiment Predictions](../1-initial-run/PRE_EXPERIMENT_PREDICTIONS.md)