# CLI Tool Usage Guide
## `generate-haiku` - Story-to-Haiku Generator

**Tool**: Convenience wrapper for running top haiku implementations

**Location**: `tools/generate-haiku`

**Requires**: Ollama running with llama3.2 model

---

## Quick Start

```bash
# Basic usage (Run 4, top 3 methods)
tools/generate-haiku "Your story text here" --run 4

# Verbose output (detailed)
tools/generate-haiku "Your story text here" --run 4 --verbose

# Run all 4 methods
tools/generate-haiku "Your story text here" --run 4 --all

# Dry run (preview without running)
tools/generate-haiku "Your story text here" --run 4 --dry-run
```

---

## Installation & Requirements

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from: https://ollama.com
```

### 2. Pull llama3.2 Model

```bash
ollama pull llama3.2
```

### 3. Start Ollama Server

```bash
# In a separate terminal
ollama serve
```

### 4. Verify Python Environment

```bash
# From experiment root
cd /home/ivanadamin/spawn-experiments/experiments/1.608-story-to-haiku

# If venv doesn't exist, create it
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install ollama
```

---

## Command-Line Options

### Required

```bash
story               Story text to convert to haiku (quoted)
```

### Optional

```bash
--run N            Run number to use (1-4, default: 3)
--top N            Number of top methods to run (default: 3 for medals)
--all              Run all available methods in the run
--verbose, -v      Show detailed information including full haiku text
--dry-run          Preview which methods would run without executing
--rankings         Custom rankings as comma-separated method numbers
                   Example: --rankings "2,4,3,1"
```

---

## Usage Examples

### Example 1: Basic Usage (Run 4, Top 3)

```bash
tools/generate-haiku "The cherry blossoms fell gently on the still pond" --run 4
```

**Output**:
```
🥇 Gold - Method 2
   Blossoms gently fall
   Softly on still pond's face
   Spring's fleeting kiss

   Syllables: [5, 7, 5] ✓
   Essence: Nature's gentle dance
   Generation time: 7.42s
```

---

### Example 2: Verbose Mode

```bash
tools/generate-haiku "An ancient temple sits atop a misty mountain" --run 4 --verbose
```

**Output** (includes verbose details):
```
🥇 Gold - Method 2
   Misty peak ascends
   Ancient temple stands tall
   Wisdom's gentle slope

   Syllables: [5, 7, 5] ✓
   Essence: The timeless refuge
   Generation time: 7.49s

   📊 Verbose Details:
      Valid structure: True
      Line count: 3
      Syllable counts: [5, 7, 5]
      Total syllables: 17
      Full haiku text:
      [complete haiku shown]
```

---

### Example 3: All Methods

```bash
tools/generate-haiku "Autumn leaves fall" --run 4 --all
```

Runs all 4 methods (not just top 3).

---

### Example 4: Dry Run (Preview)

```bash
tools/generate-haiku "Test story" --run 4 --dry-run
```

**Output**:
```
🎯 DRY RUN - Would execute top 3 implementations:
🥇 Gold - Method 2: Specification-Driven
   Quality Score: 96/100
   Implementation: ✓ 2-specification-driven

🥈 Silver - Method 4: Adaptive/Validated TDD
   Quality Score: 93/100
   Implementation: ✓ 4-adaptive-tdd

🥉 Bronze - Method 3: Pure TDD
   Quality Score: 85/100
   Implementation: ✓ 3-test-first-development
```

---

### Example 5: Custom Rankings

```bash
tools/generate-haiku "Story text" --run 4 --rankings "1,3,2,4"
```

Override default quality rankings with custom order.

---

## Understanding Output

### Medal Rankings

Based on code quality scores from comparative analysis:

- 🥇 **Gold**: Highest quality implementation (Method 2, 96/100)
- 🥈 **Silver**: Second highest (Method 4, 93/100)
- 🥉 **Bronze**: Third highest (Method 3, 85/100)
- **Runner-up**: Fourth place (Method 1, 78/100)

### Haiku Output

Each haiku shows:
- **Lines**: The three lines of the haiku
- **Syllables**: Self-reported syllable counts from LLM
- **Validation**: ✓ or ✗ for 5-7-5 structure
- **Essence**: Captured theme from the story
- **Generation time**: How long it took to generate

### Verbose Details

With `--verbose` flag, also shows:
- Valid structure boolean
- Line count
- Syllable counts array
- Total syllables
- Full haiku text (formatted)

---

## Run Selection

### Run 4 (Optimized Prompts) - **RECOMMENDED**

**Best for**: Most recent, optimized prompt engineering
**Methods**: 4 (Immediate, Specification-Driven, Pure TDD, Adaptive TDD)

**Speed**: Fastest (22-36% improvement over Run 3)

**Quality**: Highest (all methods improved)

```bash
tools/generate-haiku "Story" --run 4
```

### Run 3 (Clean Room)

**Best for**: Maximum method diversity
**Methods**: 5 (includes Selective TDD)

**Quality**: Good baseline

```bash
tools/generate-haiku "Story" --run 3
```

### Run 2 (Structured Output)

**Best for**: Testing structured JSON approach
**Methods**: 4

```bash
tools/generate-haiku "Story" --run 2
```

### Run 1 (Initial)

**Best for**: Original baseline implementation
**Methods**: 4

```bash
tools/generate-haiku "Story" --run 1
```

---

## Troubleshooting

### "Ollama not running"

**Problem**: CLI can't connect to Ollama

**Solution**:
```bash
# Start Ollama in separate terminal
ollama serve

# Or check if running
ps aux | grep ollama
```

---

### "Module not found: ollama"

**Problem**: Python ollama package not installed

**Solution**:
```bash
source venv/bin/activate
pip install ollama
```

---

### "Run directory not found"

**Problem**: Invalid run number or directory missing

**Solution**:
```bash
# Check available runs
ls -la | grep '^d' | grep -E '[0-9]-'

# Use correct run number (1-4)
tools/generate-haiku "Story" --run 4
```

---

### Method returns error

**Problem**: JSON parsing failure from LLM

**Explanation**: Sometimes the LLM returns incomplete JSON or adds extra text. This is normal and doesn't affect other methods.

**No action needed**: CLI shows which methods succeeded. Run again if needed.

---

## Performance Tips

### Faster Generation

1. **Use fewer methods**:
   ```bash
   tools/generate-haiku "Story" --run 4 --top 1  # Only top method
   ```

2. **Use Run 4** (optimized prompts are faster)

3. **Warm up Ollama first**:
   ```bash
   # Run once to warm up
   tools/generate-haiku "test" --run 4 --top 1

   # Then run real queries (will be faster)
   tools/generate-haiku "Real story" --run 4
   ```

### Better Quality

1. **Use verbose mode** to see full details
2. **Run all methods** and compare:
   ```bash
   tools/generate-haiku "Story" --run 4 --all
   ```
3. **Use Run 4** for optimized prompts

---

## Advanced Usage

### Compare Across Runs

```bash
# Run 3 (baseline)
tools/generate-haiku "Story" --run 3 > run3_output.txt

# Run 4 (optimized)
tools/generate-haiku "Story" --run 4 > run4_output.txt

# Compare
diff run3_output.txt run4_output.txt
```

### Batch Processing

```bash
#!/bin/bash
# generate_batch.sh

stories=(
    "Cherry blossoms fall"
    "Mountain temple sits"
    "Ocean waves crash"
)

for story in "${stories[@]}"; do
    echo "=== Generating haiku for: $story ==="
    tools/generate-haiku "$story" --run 4
    echo ""
done
```

---

## Example Session

```bash
# 1. Start Ollama
ollama serve &

# 2. Activate environment
source venv/bin/activate

# 3. Generate haiku
tools/generate-haiku "The old fisherman cast his net at dawn" --run 4 --verbose

# Output:
# 🥇 Gold - Method 2
#    Dawn breaks the silence
#    Old fisherman casts his net
#    Ocean's gift awaits
#
#    Syllables: [5, 7, 5] ✓
#    Essence: The patient ritual of fishing at dawn
#    Generation time: 7.2s
#
#    📊 Verbose Details:
#       Valid structure: True
#       Total syllables: 17
#       ...

# 4. Try different story
tools/generate-haiku "Autumn leaves dance in the wind" --run 4

# 5. Compare all methods
tools/generate-haiku "Winter snowflakes fall" --run 4 --all
```

---

## Related Commands

### Olympic Judging

For aesthetic quality evaluation (3 judge models):

```bash
python olympic_judging_demo.py --run 4
```

This runs all methods and has 3 different LLM models judge the haiku quality.

### Direct Method Testing

To test a specific method implementation:

```bash
cd 4-optimized-prompts/2-specification-driven
source ../../venv/bin/activate
python -c "
from haiku_converter import story_to_haiku
result = story_to_haiku('Your story here')
print(result['haiku'])
"
```

---

## CLI Design Principles

1. **User-friendly**: Clear output with medals and formatting
2. **Flexible**: Multiple options for different use cases
3. **Helpful errors**: Clear messages guide users to solutions
4. **Fast feedback**: Dry-run mode previews without running
5. **Verbose option**: Detailed info when needed

---

## Version History

- **v1.0**: Initial CLI tool (Run 3 support)
- **v1.1**: Added Run 4 support, verbose mode, improved rankings

---

## Support

For issues or questions:
- Check troubleshooting section above
- Review experiment documentation in run directories
- See `/home/ivanadamin/spawn-experiments/experiments/1.608-story-to-haiku/README.md`

---

**Tool**: `generate-haiku`

**Version**: 1.1

**Date**: 2025-09-30

**Experiment**: 1.608 - Story-to-Haiku Converter
