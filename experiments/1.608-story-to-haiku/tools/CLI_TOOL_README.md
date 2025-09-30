# Generate-Haiku CLI Tool

Post-experiment convenience wrapper for using winning implementations.

## Purpose

After completing an experiment with multiple implementation methodologies, this CLI tool provides a simple interface to:
1. Run the top-ranked implementations (based on code quality analysis)
2. Display results with medal rankings (🥇 Gold, 🥈 Silver, 🥉 Bronze)
3. Compare outputs side-by-side

## Usage

### Basic Usage
```bash
./generate-haiku "Your story text here"
```

### Specify Run and Number of Methods
```bash
# Use Run 3 results, test top 2 methods
./generate-haiku "Mountains rise high above the clouds" --run 3 --top 2

# Use Run 3 results, test all methods
./generate-haiku "Cherry blossoms fall" --run 3 --all
```

### Dry Run (see what would be executed)
```bash
./generate-haiku "Sample text" --dry-run
```

Output:
```
🎯 DRY RUN - Would execute top 3 implementations:
======================================================================

🥇 Gold - Method 2: Specification-Driven
   Quality Score: 95/100
   Implementation: ✓ 2-specification-driven

🥈 Silver - Method 5: Adaptive/Validated TDD
   Quality Score: 88/100
   Implementation: ✓ 5-adaptive-tdd

🥉 Bronze - Method 3: Pure TDD
   Quality Score: 78/100
   Implementation: ✓ 3-test-first-development
```

### Custom Rankings
```bash
# Override default rankings with your own order
./generate-haiku "Text" --rankings "1,3,2,4,5"
```

## Requirements

- **Ollama must be running**: `ollama serve`
- **Model must be pulled**: `ollama pull llama3.2`

## How Rankings Are Determined

Rankings are based on comprehensive code quality analysis across 6 categories:
- Code Structure (20%)
- Error Handling (20%)
- Testing (20%)
- Documentation (15%)
- Maintainability (15%)
- Performance (10%)

Default rankings for Run 3 (Clean Room):
1. **Method 2**: Specification-Driven (95/100) - 🥇 Gold
2. **Method 5**: Adaptive/Validated TDD (88/100) - 🥈 Silver
3. **Method 3**: Pure TDD (78/100) - 🥉 Bronze
4. **Method 4**: Selective TDD (80/100) - 🏅 Runner-up
5. **Method 1**: Immediate Implementation (73/100)

See `COMPARATIVE_CODE_QUALITY_REPORT.md` in the run directory for detailed analysis.

## Output Format

```
======================================================================
🎋 HAIKU GENERATION RESULTS
   Run: 3-clean-room (#3)
======================================================================

🥇 Gold - Method 2
----------------------------------------------------------------------
   Mountains rise so high
   Above the clouds they whisper
   Secrets of the sky

   Syllables: [5, 7, 5] ✓
   Essence: Mountain majesty and mystery
   Generation time: 2.34s

🥈 Silver - Method 5
----------------------------------------------------------------------
   High above the peaks
   Clouds embrace the mountain tops
   Silent watchers wait

   Syllables: [5, 7, 5] ✓
   Essence: Mountains as eternal guardians
   Generation time: 2.56s

...
```

## Experiment-Specific Design

This CLI tool is **experiment-specific** (1.608 Story-to-Haiku) because:

1. **Input/Output varies by experiment**: This takes story text → haiku
2. **Rankings are run-specific**: Different runs may have different quality outcomes
3. **Comparative experiments benefit most**: Single-method experiments don't need rankings

### Adapting for Other Experiments

To create a similar tool for another comparative experiment:

1. **Copy this script** as a template
2. **Update rankings** dictionary with your experiment's results
3. **Modify input/output** handling for your experiment's interface
4. **Update display** functions for your experiment's output format

Example for a different experiment:
```python
# For experiment 2.xyz - Code Refactoring Tool
DEFAULT_RANKINGS = {
    1: {  # Run 1 rankings
        'rankings': [3, 1, 4, 2],  # Method order by quality
        'scores': [92, 87, 85, 78],
        'labels': ['TDD Approach', 'Immediate', 'Specification-Driven', 'Hybrid']
    }
}
```

## When to Create a CLI Tool

✅ **Create CLI tool when:**
- Experiment compares multiple methodologies
- Post-experiment usage is valuable (demo, testing, validation)
- Clear "winner" emerges from quality analysis
- Tool provides convenience over running individual implementations

❌ **Skip CLI tool when:**
- Single methodology experiment (no comparison)
- No post-experiment usage anticipated
- Quality differences are negligible
- Direct implementation access is preferred

## Integration with Experiment Workflow

```
1. Run experiment → Multiple implementations created
2. Analyze code quality → Rankings determined
3. Create CLI tool → Wrap winning implementations
4. Use for demos → Easy access to best results
```

The CLI tool is a **post-experiment artifact** that makes the best implementations easily accessible.

---

**Experiment**: 1.608 - Story-to-Haiku Converter
**Date**: 2025-09-30
**Tool Version**: 1.0
