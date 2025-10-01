# Generate-Iambic CLI Tool

Post-experiment convenience wrapper for using winning implementations.

## Purpose

After completing Experiment 1.608.A with 4 implementation methodologies, this CLI tool provides a simple interface to:
1. Run the top-ranked implementations (based on code quality analysis)
2. Display results with medal rankings (🥇 Gold, 🥈 Silver, 🥉 Bronze)
3. Compare outputs side-by-side
4. Show iambic pentameter accuracy scoring

## Usage

### Basic Usage (Top 3 Methods)
```bash
./generate-iambic "Your prose text here"
```

### Specify Number of Methods
```bash
# Test top 2 methods
./generate-iambic "The old woman found a seed" --top 2

# Test all 4 methods
./generate-iambic "Once upon a time in a village" --top 4
```

## Requirements

- **Ollama must be running**: `ollama serve`
- **Model must be pulled**: `ollama pull llama3.2`

**For Olympic judging (optional):**
```bash
ollama pull llama3.2  # Meta (generator + judge)
ollama pull phi3:mini # Microsoft (judge)
ollama pull gemma2:2b # Google (judge)
```

## How Rankings Are Determined

Rankings are based on comprehensive code quality analysis from CODE_QUALITY_REPORT.md:

**Default Quality Order:**
1. **Method 2**: Specification-Driven (88/100) - 🥇 Gold
2. **Method 4**: Adaptive TDD (83/100) - 🥈 Silver
3. **Method 1**: Immediate Implementation (78/100) - 🥉 Bronze
4. **Method 3**: Pure TDD (72/100) - 4th place

### Quality Evaluation Categories:
- Code Structure (20%)
- Error Handling (20%)
- Testing (20%)
- Documentation (15%)
- Maintainability (15%)
- Performance (10%)

## Accuracy Scoring

The tool scores each output based on iambic pentameter accuracy:
- **Target**: 10 syllables per line
- **Flexible range**: 9-11 syllables (allows minor variance)
- **Scoring**: Percentage of lines within valid syllable range

## Output Format

```
================================================================================
📝 IAMBIC PENTAMETER GENERATOR
================================================================================

Input: Your prose text here

Running top 3 implementations...

🔧 Specification-Driven... ✓ (100% accuracy)
🔧 Adaptive TDD... ✓ (80% accuracy)
🔧 Immediate Implementation... ✓ (60% accuracy)

================================================================================
🏅 RANKED RESULTS
================================================================================

🥇 GOLD: Specification-Driven (100% accuracy)
--------------------------------------------------------------------------------
In twilight's hush, where shadows softly fall,
Amidst her garden's verdant, secret keep,
An ancient crone, with wrinkled hands did enthrall
A mystic seed, whose origin doth sleep.
Its secrets hidden, like the dawn's first light

🥈 SILVER: Adaptive TDD (80% accuracy)
--------------------------------------------------------------------------------
[Second-place output...]

🥉 BRONZE: Immediate Implementation (60% accuracy)
--------------------------------------------------------------------------------
[Third-place output...]
```

## Method Differences

### Method 2 (Specification-Driven) - 🥇 Winner
- **Strengths**: Production-ready architecture, comprehensive error handling, extensive test suite (25+ tests)
- **Code**: 657 LOC total (120 impl + 537 tests)
- **Time**: ~8 minutes
- **Best For**: Production LLM integrations

### Method 4 (Adaptive TDD) - 🥈 Runner-up
- **Strengths**: Validated test quality, strategic complexity matching
- **Code**: 248 LOC total (121 impl + 127 tests)
- **Time**: ~8 minutes
- **Best For**: Balanced quality and maintainability

### Method 1 (Immediate Implementation) - 🥉 Fast
- **Strengths**: Rapid development, functional baseline
- **Code**: 290 LOC total (129 impl + 161 tests)
- **Time**: ~10 minutes
- **Best For**: Prototypes and quick demos

### Method 3 (Pure TDD) - 4th place
- **Strengths**: Minimal implementation
- **Code**: 72 LOC total (39 impl + 33 tests)
- **Time**: ~5 minutes
- **Note**: Incomplete implementation (may fail on some inputs)

## Troubleshooting

### Method 1 Fails
Method 1 (Immediate Implementation) may fail on some inputs due to API differences. This is expected - the tool will skip it and show results from working methods.

### Low Accuracy Scores
The syllable counting is approximate. Even "low" accuracy (60-80%) often produces valid iambic pentameter - the scorer is conservative.

### No Results
Ensure Ollama is running:
```bash
ollama serve
```

And llama3.2 is available:
```bash
ollama pull llama3.2
```

## Experiment Integration

```
1. Run Experiment 1.608.A → 4 implementations created
2. Analyze code quality → Rankings: M2 (88), M4 (83), M1 (78), M3 (72)
3. Create CLI tool → Wrap top implementations
4. Use for demos → Easy access to best results
```

This CLI tool is a **post-experiment artifact** making the winning implementations easily accessible for demonstrations and validation.

---

**Experiment**: 1.608.A - Iambic Pentameter Converter
**Date**: 2025-09-30
**Tool Version**: 1.0
**Model**: llama3.2 via Ollama
