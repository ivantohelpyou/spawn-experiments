# CLI Tool Generator v1
## Post-Experiment Convenience Wrapper Creation

**Purpose**: Generate experiment-specific CLI tools that wrap winning implementations for easy post-experiment usage.

**When to use**: After completing a comparative experiment where multiple methodologies produce implementations with clear quality rankings.

---

## Decision Tree: Should You Create a CLI Tool?

```
Do you have multiple implementations to compare?
├─ NO → Skip CLI tool (single implementation doesn't need ranking wrapper)
└─ YES → Continue

Is there post-experiment usage value? (demos, validation, testing)
├─ NO → Skip CLI tool (direct implementation access is sufficient)
└─ YES → Continue

Are there clear quality rankings from code analysis?
├─ NO → Skip CLI tool (no "winner" to highlight)
└─ YES → CREATE CLI TOOL ✓
```

---

## CLI Tool Template Structure

### 1. Core Components

Every experiment-specific CLI tool should have:

```python
#!/usr/bin/env python3
"""
{Tool Name} - Post-Experiment CLI Tool
Experiment {ID}: {Description}

Runs the top implementations from a specific run and returns ranked results.

Usage:
    {tool-name} {INPUT_ARGS}
    {tool-name} {INPUT_ARGS} --run {RUN_NUM}
    {tool-name} {INPUT_ARGS} --run {RUN_NUM} --top {N}
"""

import sys
import time
import argparse
from pathlib import Path
import importlib.util

# SECTION 1: DEFAULT RANKINGS
# Rankings based on comprehensive code quality analysis
DEFAULT_RANKINGS = {
    {RUN_NUM}: {
        'rankings': [{METHOD_ORDER}],  # Method numbers in quality order
        'scores': [{QUALITY_SCORES}],
        'labels': [{METHOD_LABELS}]
    }
}

# SECTION 2: MODULE LOADING
def load_method(method_num, run_dir):
    """Load a method's implementation from specified run directory."""
    method_dirs = {
        # Map method numbers to directory names
    }
    # Implementation...

# SECTION 3: RANKED EXECUTION
def execute_ranked_{function}({inputs}, run_dir, rankings, num_methods=3):
    """
    Execute {function} from top N methods and return ranked results.

    Returns:
        List of dicts with method info and results
    """
    results = []
    medals = ['🥇 Gold', '🥈 Silver', '🥉 Bronze', '🏅 Runner-up']

    for i, method_num in enumerate(rankings[:num_methods]):
        # Execute and collect results with error handling

    return results

# SECTION 4: DISPLAY
def display_results(results, run_info):
    """Display ranked results in a beautiful format."""
    # Experiment-specific output formatting

# SECTION 5: CLI INTERFACE
def main():
    parser = argparse.ArgumentParser(...)
    parser.add_argument('{primary_input}', ...)
    parser.add_argument('--run', type=int, default={DEFAULT_RUN}, ...)
    parser.add_argument('--top', type=int, default=3, ...)
    parser.add_argument('--all', action='store_true', ...)
    parser.add_argument('--dry-run', action='store_true', ...)
    parser.add_argument('--rankings', type=str, ...)

    args = parser.parse_args()

    # Execute logic...

if __name__ == "__main__":
    sys.exit(main())
```

---

## Generation Process

### Step 1: Gather Experiment Information

**Required Information:**
1. Experiment ID (e.g., "1.608")
2. Experiment name (e.g., "Story-to-Haiku Converter")
3. Default run to use (usually the most recent/comprehensive)
4. Method rankings from code quality report
5. Input format (what user provides)
6. Output format (what gets displayed)

**Extract from:**
- `COMPARATIVE_CODE_QUALITY_REPORT.md` → rankings, scores, labels
- Experiment spec → input/output format
- Implementation files → function signatures

### Step 2: Define CLI Interface

**Primary input argument:**
```python
# Example: Story-to-Haiku
parser.add_argument('story', type=str,
                   help='Story text to convert to haiku')

# Example: Code Refactoring
parser.add_argument('file', type=str,
                   help='Python file to refactor')

# Example: Test Generator
parser.add_argument('function', type=str,
                   help='Function to generate tests for')
```

**Standard arguments (include in all CLI tools):**
```python
parser.add_argument('--run', type=int, default={DEFAULT},
                   help='Run number to use (default: {DEFAULT})')
parser.add_argument('--top', type=int, default=3,
                   help='Number of top methods to run (default: 3 for medals)')
parser.add_argument('--all', action='store_true',
                   help='Run all available methods')
parser.add_argument('--dry-run', action='store_true',
                   help='Show which methods would be run without executing')
parser.add_argument('--rankings', type=str,
                   help='Custom rankings as comma-separated method numbers')
```

### Step 3: Implement Dry-Run Mode

**Purpose**: Let users preview what would execute without requiring dependencies (like Ollama).

```python
if args.dry_run:
    print(f"\n🎯 DRY RUN - Would execute top {num_methods} implementations:")
    print("="*70)

    medals = ['🥇 Gold', '🥈 Silver', '🥉 Bronze', '🏅 Runner-up']

    for i, method_num in enumerate(rankings[:num_methods]):
        medal = medals[i] if i < len(medals) else f"#{i+1}"
        label = labels[i] if i < len(labels) else "Unknown"
        score = scores[i] if i < len(scores) else "?"

        # Check if implementation exists
        exists = "✓" if implementation_exists(method_num) else "✗"

        print(f"\n{medal} - Method {method_num}: {label}")
        print(f"   Quality Score: {score}/100")
        print(f"   Implementation: {exists} {method_path}")

    print("\n💡 To execute, run without --dry-run")
    return 0
```

### Step 4: Add Helpful Error Messages

**Common errors to handle:**
```python
except Exception as e:
    error_msg = str(e)

    # Provide helpful guidance for common issues
    if "'NoneType' object has no attribute 'chat'" in error_msg:
        error_msg = "Ollama not running. Start with: ollama serve"
    elif "Connection refused" in error_msg:
        error_msg = "Cannot connect to service. Check if it's running."
    elif "ModuleNotFoundError" in error_msg:
        error_msg = f"Missing dependency. Install with: pip install {module}"

    results.append({
        'method': method_num,
        'error': error_msg,
        'success': False
    })
```

### Step 5: Create Display Function

**Design principles:**
- Use medals (🥇 🥈 🥉 🏅) for rankings
- Show key metrics (time, quality indicators)
- Format output to fit terminal width (~70 chars)
- Include comparison section for side-by-side viewing

**Example template:**
```python
def display_results(results, run_info):
    """Display ranked results."""
    print("\n" + "="*70)
    print(f"{ICON} {EXPERIMENT_NAME} RESULTS")
    print(f"   Run: {run_info['run_name']} (#{run_info['run_num']})")
    print("="*70)

    for r in results:
        print(f"\n{r['medal']} - Method {r['method']}")
        print("-" * 70)

        if r.get('success'):
            # Display experiment-specific output
            display_{experiment}_output(r['result'])

            # Show metadata
            print(f"\n   Generation time: {r['time']:.2f}s")
        else:
            print(f"   ✗ ERROR: {r.get('error', 'Unknown error')}")

    print("\n" + "="*70)

    # Optional: Show comparison
    successful = [r for r in results if r.get('success')]
    if len(successful) > 1:
        print("\n📊 COMPARISON")
        print("="*70)
        display_comparison(successful)
```

---

## Example: Story-to-Haiku CLI Tool

### Rankings (from code quality report)
```python
DEFAULT_RANKINGS = {
    3: {  # Run 3 (Clean Room)
        'rankings': [2, 5, 3, 4, 1],
        'scores': [95, 88, 78, 80, 73],
        'labels': [
            'Specification-Driven',
            'Adaptive/Validated TDD',
            'Pure TDD',
            'Selective TDD',
            'Immediate Implementation'
        ]
    }
}
```

### CLI Interface
```bash
generate-haiku "In a small village..." --run 3 --top 3
```

### Output Format
```
🎋 HAIKU GENERATION RESULTS
======================================================================

🥇 Gold - Method 2
----------------------------------------------------------------------
   Mountains rise so high
   Above the clouds they whisper
   Secrets of the sky

   Syllables: [5, 7, 5] ✓
   Generation time: 2.34s
```

---

## Experiment-Specific Adaptations

### For Different I/O Types

**File input:**
```python
parser.add_argument('file', type=str, help='Path to input file')
# Validate file exists
if not Path(args.file).exists():
    print(f"❌ Error: File not found: {args.file}")
    return 1
```

**Multiple inputs:**
```python
parser.add_argument('source', type=str, help='Source code')
parser.add_argument('target', type=str, help='Target language')
```

**Optional inputs:**
```python
parser.add_argument('--config', type=str, help='Optional config file')
parser.add_argument('--verbose', action='store_true', help='Verbose output')
```

### For Different Output Types

**Code output:**
```python
def display_code_output(result):
    print("   Generated code:")
    print("   " + "-"*68)
    for line in result['code'].split('\n'):
        print(f"   {line}")
    print("   " + "-"*68)
```

**JSON output:**
```python
def display_json_output(result):
    import json
    print("   Result:")
    print(json.dumps(result['data'], indent=2))
```

**Multiple files:**
```python
def display_files_output(result):
    for filename, content in result['files'].items():
        print(f"\n   📄 {filename}")
        print(f"   {len(content)} lines")
```

---

## CLI Tool Checklist

Before considering the CLI tool complete, verify:

- [ ] **Dry-run mode works** without dependencies
- [ ] **Error messages are helpful** (explain how to fix common issues)
- [ ] **Rankings match code quality report** exactly
- [ ] **All methods load correctly** from their directories
- [ ] **Output is well-formatted** and fits terminal width
- [ ] **Comparison section works** when multiple methods succeed
- [ ] **Help text is clear** (`--help` is useful)
- [ ] **Script is executable** (`chmod +x`)
- [ ] **Shebang is correct** (`#!/usr/bin/env python3`)
- [ ] **README created** explaining usage

---

## CLI Tool Documentation Template

Create a `CLI_TOOL_README.md` alongside the tool:

```markdown
# {Tool Name}

Post-experiment convenience wrapper for using winning implementations.

## Purpose
{Brief description}

## Usage

### Basic Usage
\`\`\`bash
./{tool-name} {INPUT_EXAMPLE}
\`\`\`

### Options
\`\`\`bash
--run {NUM}      # Specify which run to use
--top {NUM}      # Number of top methods (default: 3)
--all            # Run all methods
--dry-run        # Preview without executing
--rankings "..." # Custom rankings
\`\`\`

## Requirements
- {Dependency 1}
- {Dependency 2}

## Rankings
{Explain how rankings are determined}

Default rankings for Run {NUM}:
1. Method {X}: {Name} ({Score}/100) - 🥇
2. Method {Y}: {Name} ({Score}/100) - 🥈
3. Method {Z}: {Name} ({Score}/100) - 🥉

## Output Format
{Show example output}

## When to Use This Tool
{Explain use cases}
```

---

## Integration with Experiment Workflow

### Standard Experiment Process:
```
1. Run experiment → Multiple implementations created
2. Analyze code quality → Rankings determined (COMPARATIVE_CODE_QUALITY_REPORT.md)
3. [OPTIONAL] Create CLI tool → Wrap winning implementations
4. Use for demos → Easy access to best results
```

### When to Create CLI Tool:

**✅ CREATE when:**
- Comparative experiment (multiple methodologies)
- Post-experiment usage is valuable
- Clear quality rankings exist
- Tool provides meaningful convenience

**❌ SKIP when:**
- Single methodology (no comparison)
- No anticipated post-experiment usage
- Quality differences negligible
- Direct access preferred

---

## CLI Tool Naming Convention

**Pattern**: `{verb}-{noun}` or `{experiment-short-name}`

**Examples:**
- `generate-haiku` (Experiment 1.608: Story-to-Haiku)
- `refactor-code` (Experiment 2.xxx: Code Refactoring)
- `generate-tests` (Experiment 3.xxx: Test Generation)
- `convert-format` (Experiment 4.xxx: Format Conversion)

**Location**: Place in experiment root directory
```
experiments/
  1.608-story-to-haiku/
    generate-haiku          ← CLI tool
    CLI_TOOL_README.md      ← Documentation
    1-initial-run/
    2-structured-output/
    3-clean-room/
      COMPARATIVE_CODE_QUALITY_REPORT.md  ← Source of rankings
```

---

## Example Prompt for CLI Tool Creation

**After completing code quality analysis**, use this prompt:

```
Create a post-experiment CLI tool for experiment {ID} that:

1. Wraps the top {N} implementations based on code quality rankings
2. Takes input: {describe input format}
3. Returns output: {describe output format}
4. Displays results with medal rankings (🥇 🥈 🥉)
5. Includes --dry-run mode
6. Provides helpful error messages

Rankings from code quality report:
- Method {X}: {Name} ({Score}/100)
- Method {Y}: {Name} ({Score}/100)
- Method {Z}: {Name} ({Score}/100)

Use the CLI_TOOL_GENERATOR_V1.md template.
```

---

## Maintenance and Updates

### When Rankings Change:
```python
# Update DEFAULT_RANKINGS in the CLI tool
DEFAULT_RANKINGS = {
    {RUN_NUM}: {
        'rankings': [{NEW_ORDER}],
        'scores': [{NEW_SCORES}],
        'labels': [{NEW_LABELS}]
    }
}
```

### When Adding New Runs:
```python
# Add new run to run_dirs mapping
run_dirs = {
    1: "1-initial-run",
    2: "2-structured-output",
    3: "3-clean-room",
    4: "4-new-run"  # ← Add here
}

# Add rankings for new run
DEFAULT_RANKINGS = {
    # ... existing runs ...
    4: {  # ← Add here
        'rankings': [...],
        'scores': [...],
        'labels': [...]
    }
}
```

---

## Advanced Features (Optional)

### Parallel Execution
```python
from concurrent.futures import ThreadPoolExecutor

def execute_parallel(methods, story, run_dir):
    with ThreadPoolExecutor(max_workers=len(methods)) as executor:
        futures = {
            executor.submit(execute_method, m, story, run_dir): m
            for m in methods
        }
        # Collect results...
```

### Caching Results
```python
import hashlib
import json
from pathlib import Path

def cache_result(input_hash, result):
    cache_dir = Path.home() / '.cache' / 'experiment-1.608'
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{input_hash}.json"
    cache_file.write_text(json.dumps(result))

def get_cached_result(input_hash):
    cache_file = Path.home() / '.cache' / 'experiment-1.608' / f"{input_hash}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    return None
```

### Configuration File
```python
# Support ~/.config/experiment-1.608/config.json
{
    "default_run": 3,
    "default_top": 3,
    "preferred_methods": [2, 5, 3],
    "cache_enabled": true
}
```

---

## Testing Your CLI Tool

### Test Cases:

1. **Basic execution**:
   ```bash
   ./tool-name "basic input"
   ```

2. **Dry-run mode**:
   ```bash
   ./tool-name "input" --dry-run
   ```

3. **Different runs**:
   ```bash
   ./tool-name "input" --run 1
   ./tool-name "input" --run 2
   ./tool-name "input" --run 3
   ```

4. **Top N methods**:
   ```bash
   ./tool-name "input" --top 1
   ./tool-name "input" --top 2
   ./tool-name "input" --top 5
   ```

5. **All methods**:
   ```bash
   ./tool-name "input" --all
   ```

6. **Custom rankings**:
   ```bash
   ./tool-name "input" --rankings "1,2,3,4,5"
   ```

7. **Error handling**:
   ```bash
   # Test with service down
   # Test with missing files
   # Test with invalid input
   ```

---

## Version History

- **v1.0** (2025-09-30): Initial CLI Tool Generator template
  - Core structure defined
  - Standard arguments established
  - Error handling patterns documented
  - Example (Story-to-Haiku) provided

---

**Next Steps After Creating CLI Tool:**

1. ✅ Test all modes (basic, dry-run, custom rankings)
2. ✅ Verify error messages are helpful
3. ✅ Create CLI_TOOL_README.md documentation
4. ✅ Make script executable (`chmod +x`)
5. ✅ Add to experiment documentation
6. ⏭️ Optional: Demo in presentation/showcase

