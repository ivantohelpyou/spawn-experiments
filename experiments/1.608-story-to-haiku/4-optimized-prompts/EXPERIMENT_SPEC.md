# Experiment 1.608 - Run 4: Story-to-Haiku Converter
## Optimized Prompts Run (Refined Prompt Engineering)

**Date**: 2025-09-30

**Run**: 4 of 4 (Prompt optimization - testing refined LLM instructions)

**Domain**: 1.6XX - Ollama Integration Functions

**Complexity**: Tier 1 - Simple Function

---

## Purpose of Run 4

This is an **optimized prompts run** to test if refined prompt engineering improves haiku quality across all methodologies.

**Hypothesis**: Better-crafted prompts with clearer instructions about syllable counting, poetic essence, and haiku structure will produce higher quality results across all methods.

**Differences from Run 3**:
- Same spec, same requirements
- Enhanced prompt templates with explicit syllable instructions
- Clearer guidance on capturing story essence
- More structured JSON output instructions
- Tests if prompt quality affects methodology performance

---

## Problem Statement

Create a Python function that converts a story or paragraph into a haiku (5-7-5 syllable structure) using Ollama (llama3.2), with **structured JSON output** where the LLM self-reports syllable counts, using **optimized prompt engineering**.

---

## Function Signature

```python
def story_to_haiku(text: str, llm_client=None) -> dict:
    """
    Convert a story or text into a haiku poem using optimized prompts.

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

### Optimized Prompt Requirements

**CRITICAL - Enhanced Prompt Engineering**: Your prompt must be carefully crafted to:

1. **Explicitly instruct syllable counting**:
   - "Count syllables carefully for each line"
   - "First line must have exactly 5 syllables"
   - "Second line must have exactly 7 syllables"
   - "Third line must have exactly 5 syllables"

2. **Guide essence extraction**:
   - "Identify the core emotion, theme, or image from the story"
   - "Distill the story's essence into a single vivid moment or feeling"

3. **Provide clear examples**:
   - Include example haiku with syllable breakdown
   - Show expected JSON format with annotations

4. **Structured output format**:
```json
{
  "lines": [
    "Cherry blossoms fall",
    "Softly on the quiet pond",
    "Spring whispers arrive"
  ],
  "syllables": [5, 7, 5],
  "essence": "Spring's gentle transition from winter to renewal"
}
```

### Example Optimized Prompt Template

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

## Success Criteria

### Minimum Viable
- ✅ Accepts text input
- ✅ Returns structured dict with all required keys
- ✅ Parses JSON from LLM
- ✅ Validates syllable structure
- ✅ Integrates with Ollama
- ✅ Uses optimized prompt template
- ✅ Passes basic tests with mocks

### Complete Implementation
- ✅ Handles malformed JSON gracefully
- ✅ Validates all required JSON keys
- ✅ Handles edge cases
- ✅ Provides clear error messages
- ✅ Supports dependency injection
- ✅ Includes comprehensive tests
- ✅ **Demonstrates improved haiku quality vs Run 3**

---

## Research Questions

1. **Does prompt quality affect all methodologies equally?**
   - Or do some methods benefit more from better prompts?

2. **Does better prompt engineering improve haiku aesthetic quality?**
   - Will Olympic judging scores improve for Run 4 vs Run 3?

3. **Does prompt complexity affect development time?**
   - Do optimized prompts take longer to craft?

4. **Does method ranking change with better prompts?**
   - Will Method 2 still win? Will gaps narrow or widen?

---

## Related Documents
- [Run 3 Experiment Spec](../3-clean-room/EXPERIMENT_SPEC.md)
- [Meta Prompt Generator V4](/home/ivanadamin/spawn-experiments/META_PROMPT_GENERATOR_V4.md)
- [Ollama Experiments Series](../../../docs/OLLAMA_EXPERIMENTS_SERIES.md)
