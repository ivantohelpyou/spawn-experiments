# Experiment 1.608 - Run 3: Story-to-Haiku Converter
## Clean Room Run (No Prior Context)

**Date**: 2025-09-30

**Run**: 3 of 3 (Clean room conditions - testing context effects)

**Domain**: 1.6XX - Ollama Integration Functions

**Complexity**: Tier 1 - Simple Function

---

## Purpose of Run 3

This is a **clean room run** to test if prior context from Run 1 and Run 2 affects methodology performance.

**Hypothesis**: Method 2 (Specification-Driven) might perform better without contamination from previous runs.

**Differences from Run 2**:
- Same spec, same requirements
- Fresh directory structure
- No reference to previous implementations
- Tests context-dependent performance variations

---

## Problem Statement

Create a Python function that converts a story or paragraph into a haiku (5-7-5 syllable structure) using Ollama (llama3.2), with **structured JSON output** where the LLM self-reports syllable counts.

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
- ✅ Passes basic tests with mocks

### Complete Implementation
- ✅ Handles malformed JSON gracefully
- ✅ Validates all required JSON keys
- ✅ Handles edge cases
- ✅ Provides clear error messages
- ✅ Supports dependency injection
- ✅ Includes comprehensive tests

---

## Related Documents
- [Run 2 Experiment Spec](../2-structured-output/EXPERIMENT_SPEC.md)
- [Ollama Experiments Series](../../../docs/OLLAMA_EXPERIMENTS_SERIES.md)
