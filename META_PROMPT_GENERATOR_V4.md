# TDD in the AI Era: Spawn-Experiments System v4.0 - Baseline Specification Edition

**Purpose**: Enhanced prompting system with baseline specification control for practical methodology comparisons.

**Key Innovation**: Shared baseline specification eliminates requirement interpretation variance, enabling pure methodology effectiveness measurement.

**Version 4.0 Changes**:
- Baseline specification protocol for scope control
- Experimenter approval step before method execution
- Branch isolation with clean main integration
- Focus shift from pathology study to practical workflows

---

## 🔬 Core Experimental Framework

### **Step 0: Baseline Specification Generation**

```
BASELINE SPECIFICATION PROTOCOL:

1. Generate reasonable scope specification for [APPLICATION_TYPE]
2. Present to experimenter for approval/editing
3. Use approved baseline as shared foundation for all methods
4. Optional: Create specification variants (minimal/standard/detailed)

SPECIFICATION FORMAT:
- Core functionality requirements
- Key constraints and boundaries
- Expected input/output behavior
- Essential edge cases to handle
- Explicit exclusions (what NOT to build)

EXPERIMENTER DECISION POINT:
- Approve as-is
- Edit scope up/down
- Create multiple baselines for comparison
```

### **Step 1: Pre-Experiment Predictions**

```
PRE-EXPERIMENT PREDICTION PROTOCOL:

After baseline specification approval, generate methodology predictions:

1. Create experiment folder: experiments/[EXPERIMENT_NUMBER]/
2. Generate PRE_EXPERIMENT_PREDICTIONS.md with:
   - Expected outcomes for each methodology
   - Predicted code volume (lines)
   - Predicted development time
   - Anticipated architectural approaches
   - Methodology winner prediction
   - Potential surprises or challenges

PREDICTION FORMAT:
- Method-specific outcome predictions
- Quantitative estimates (time, lines, complexity)
- Architectural approach expectations
- Overall methodology performance ranking
- Specific areas where methods might struggle/excel

RESEARCH VALUE:
- Captures AI's initial expectations before execution
- Enables prediction accuracy analysis
- Reveals AI biases about methodology effectiveness
- Creates accountability for methodology assumptions
```

### **Enhanced Branch Isolation Protocol** (Add to ALL prompts)

```
IMPORTANT: Create a dedicated branch for your experiment with standardized structure:

git checkout -b exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]

Examples:
- git checkout -b exp-1504-immediate
- git checkout -b exp-1504-specification
- git checkout -b exp-1504-tdd
- git checkout -b exp-1504-adaptive-tdd

REQUIRED FILE STRUCTURE:
experiments/[EXPERIMENT_NUMBER]/[METHOD_DIR]/
├── date_validator.py (or main implementation file)
├── test_*.py (if applicable)
├── README.md (brief method summary)
└── [other method-specific files]

INTEGRATION VERIFICATION:
Before marking complete, verify your branch contains:
- Main implementation file with validate_date() function
- All required dependencies resolved
- Clean commit history with descriptive messages
- No references to other methodology implementations

This ensures:
- Perfect methodology isolation during development
- Clean integration back to main branch
- Consistent file structure for comparison scripts
- Audit trail for scientific rigor
```

### **Atomic Commit Protocol** (Add to ALL prompts)

```
IMPORTANT: Checkpoint your progress with atomic git commits:

After each meaningful step, commit your work:
- git add -A && git commit -m "Specs: [what you defined]"
- git add -A && git commit -m "Impl: [what you built]"
- git add -A && git commit -m "Test: [what you tested]"
- git add -A && git commit -m "Fix: [what you fixed]"
- git add -A && git commit -m "COMPLETE: [solution summary]"

Commit at least every 3 minutes or at major milestones.
This enables progress tracking and clean integration back to main.
```

### **Enhanced Integration Protocol**

```
EXPERIMENT COMPLETION WITH VERIFICATION:

1. PRE-INTEGRATION VERIFICATION on your branch:
   - Verify main implementation file exists and works
   - Run basic functionality test
   - Confirm no cross-method contamination
   - Clean commit history with atomic commits

2. INTEGRATION TO MAIN:
   git checkout main
   git merge --no-ff exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]

   If conflicts occur:
   - DO NOT resolve by copying from other methods
   - Ensure your method's files take precedence in your directory
   - Verify post-merge that your implementation is intact

3. POST-INTEGRATION VERIFICATION:
   - Test that your method's implementation works on main
   - Verify comparison scripts can find your files
   - Run methodology_comparison_demo.py to confirm inclusion

4. BRANCH CLEANUP (optional):
   git branch -d exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]

This ensures:
- No method implementations lost during integration
- Comparison scripts work with all methods
- Scientific integrity maintained through merge process
```

---

## 🔧 Integration Tooling and Verification

### **Pre-Integration Verification Script**

```bash
#!/bin/bash
# verify_experiment_branch.sh - Run before merging to main

EXPERIMENT_NUM=$1
METHOD_NAME=$2
BRANCH_NAME="exp-${EXPERIMENT_NUM}-${METHOD_NAME}"

echo "🔍 Verifying experiment branch: $BRANCH_NAME"

# Check we're on the right branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "$BRANCH_NAME" ]; then
    echo "❌ Not on branch $BRANCH_NAME (currently on $current_branch)"
    exit 1
fi

# Check required files exist
EXPERIMENT_DIR="experiments/$EXPERIMENT_NUM"
METHOD_DIR_MAP=("immediate:1-immediate-implementation" "specification:2-specification-driven" "tdd:3-test-first-development" "adaptive-tdd:4-adaptive-tdd-v41")

for mapping in "${METHOD_DIR_MAP[@]}"; do
    method="${mapping%%:*}"
    dir="${mapping#*:}"
    if [[ "$METHOD_NAME" == *"$method"* ]]; then
        IMPL_FILE="$EXPERIMENT_DIR/$dir/date_validator.py"
        if [ ! -f "$IMPL_FILE" ]; then
            echo "❌ Missing implementation file: $IMPL_FILE"
            exit 1
        fi
        echo "✅ Found implementation: $IMPL_FILE"

        # Test the implementation works
        if python -c "
import sys; sys.path.insert(0, '$EXPERIMENT_DIR/$dir')
import date_validator
result = date_validator.validate_date('02/29/2024')
print('✅ Implementation test passed:', result)
" 2>/dev/null; then
            echo "✅ Implementation functional test passed"
        else
            echo "❌ Implementation functional test failed"
            exit 1
        fi
        break
    fi
done

echo "🎯 Branch verification complete - ready for integration!"
```

### **Post-Integration Verification Script**

```bash
#!/bin/bash
# verify_main_integration.sh - Run after merging to main

EXPERIMENT_NUM=$1

echo "🔍 Verifying main branch integration for experiment $EXPERIMENT_NUM"

cd "experiments/$EXPERIMENT_NUM" || exit 1

# Test all method implementations
methods=("1-immediate-implementation" "2-specification-driven" "3-test-first-development" "4-adaptive-tdd-v41")

for method_dir in "${methods[@]}"; do
    if [ -d "$method_dir" ] && [ -f "$method_dir/date_validator.py" ]; then
        echo "Testing $method_dir..."
        if python -c "
import sys; sys.path.insert(0, '$method_dir')
import date_validator
result = date_validator.validate_date('02/29/2024')
print('✅ $method_dir: test passed')
" 2>/dev/null; then
            echo "✅ $method_dir integration successful"
        else
            echo "❌ $method_dir integration failed"
        fi
    else
        echo "⚠️  $method_dir not implemented"
    fi
done

# Test comparison script works
if [ -f "methodology_comparison_demo.py" ]; then
    echo "Testing comparison script..."
    if python methodology_comparison_demo.py >/dev/null 2>&1; then
        echo "✅ Comparison script working"
    else
        echo "❌ Comparison script failed"
    fi
fi

echo "🎯 Main branch integration verification complete!"
```

### **Automated Post-Experiment Demo Generation**

```bash
#!/bin/bash
# generate_experiment_demo.sh - Create comprehensive demo for completed experiment

EXPERIMENT_NUM=$1
EXPERIMENT_NAME=$2

echo "🚀 Generating comprehensive demo for experiment $EXPERIMENT_NUM"

EXPERIMENT_DIR="experiments/$EXPERIMENT_NUM"
cd "$EXPERIMENT_DIR" || exit 1

# Auto-detect implemented methods
methods=()
method_names=()
if [ -f "1-immediate-implementation/date_validator.py" ]; then
    methods+=("1-immediate-implementation")
    method_names+=("Method 1 (Immediate)")
fi
if [ -f "2-specification-driven/date_validator.py" ]; then
    methods+=("2-specification-driven")
    method_names+=("Method 2 (Specification)")
fi
if [ -f "3-test-first-development/date_validator.py" ]; then
    methods+=("3-test-first-development")
    method_names+=("Method 3 (Pure TDD)")
fi
if [ -f "4-adaptive-tdd-v41/date_validator.py" ]; then
    methods+=("4-adaptive-tdd-v41")
    method_names+=("Method 4 (Adaptive TDD)")
fi

echo "📊 Detected ${#methods[@]} implemented methods: ${method_names[*]}"

# Generate comparison demo script
cat > methodology_comparison_demo.py << 'EOF'
#!/usr/bin/env python3
"""
Auto-generated Methodology Comparison Demo
Automatically tests all available method implementations.
"""

import os
import sys
import subprocess
from pathlib import Path

def find_experiment_directory():
    """Find the experiment directory from any location."""
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # If running from the experiment directory
    if os.path.basename(script_dir).startswith("1."):
        return script_dir

    return script_dir

def get_available_methods(base_dir):
    """Auto-detect available method implementations."""
    methods = {}

    method_dirs = {
        "Method 1 (Immediate)": "1-immediate-implementation",
        "Method 2 (Specification)": "2-specification-driven",
        "Method 3 (Pure TDD)": "3-test-first-development",
        "Method 4 (Adaptive TDD)": "4-adaptive-tdd-v41"
    }

    for method_name, method_dir in method_dirs.items():
        impl_file = os.path.join(base_dir, method_dir, "date_validator.py")
        if os.path.exists(impl_file):
            methods[method_name] = method_dir

    return methods

def test_functionality_equivalence(base_dir, available_methods):
    """Test that all available methods provide equivalent functionality."""
    print("\n" + "="*80)
    print("🧪 FUNCTIONALITY EQUIVALENCE TEST")
    print("="*80)
    print(f"Testing {len(available_methods)} available method implementations...")
    print()

    test_cases = [
        ("02/29/2024", "Valid leap year"),
        ("02/29/2023", "Invalid leap year"),
        ("13/01/2024", "EU format valid"),
        ("01/13/2024", "US format valid"),
        ("", "Empty string"),
        ("not-a-date", "Invalid format")
    ]

    # Create header
    header = f"{'Test Case':<15}"
    for method_name in available_methods.keys():
        method_abbrev = "M" + method_name.split()[1][1]  # M1, M2, M3, M4
        header += f" {method_abbrev:<6}"
    header += " Description"

    print(header)
    print("-" * len(header))

    for test_input, description in test_cases:
        display_input = test_input if test_input else "(empty)"
        results = {}

        for method_name, method_dir in available_methods.items():
            method_path = os.path.join(base_dir, method_dir)

            try:
                test_script = f'''
import sys
sys.path.insert(0, "{method_path}")

test_input = """{test_input}"""
try:
    import date_validator
    result = date_validator.validate_date(test_input)
    print("✓" if result else "✗")
except Exception as e:
    print("Error")
'''

                result = subprocess.run(
                    [sys.executable, "-c", test_script],
                    capture_output=True, text=True, timeout=5
                )

                if result.returncode == 0:
                    results[method_name] = result.stdout.strip()
                else:
                    results[method_name] = "Error"

            except Exception:
                results[method_name] = "N/A"

        # Print results row
        row = f"{display_input:<15}"
        for method_name in available_methods.keys():
            result = results.get(method_name, "N/A")
            row += f" {result:<6}"
        row += f" {description}"
        print(row)

    print(f"\n📊 Successfully tested {len(available_methods)} method implementations!")

def main():
    """Run comprehensive methodology comparison."""
    print("="*80)
    print("🚀 AUTOMATED METHODOLOGY COMPARISON")
    print("="*80)

    base_dir = find_experiment_directory()
    print(f"📂 Experiment directory: {base_dir}")

    available_methods = get_available_methods(base_dir)

    if not available_methods:
        print("❌ No method implementations found!")
        return

    print(f"✅ Found {len(available_methods)} implemented methods:")
    for method_name, method_dir in available_methods.items():
        print(f"   • {method_name}: {method_dir}/")

    test_functionality_equivalence(base_dir, available_methods)

    print("\n" + "="*80)
    print("🎯 METHODOLOGY COMPARISON COMPLETE")
    print("="*80)
    print("✅ All available methods tested successfully!")
    print("📊 Comparison data ready for analysis")

if __name__ == "__main__":
    main()
EOF

# Test the generated demo
echo "🧪 Testing generated comparison demo..."
if python methodology_comparison_demo.py; then
    echo "✅ Demo generation successful!"
else
    echo "❌ Demo generation failed - manual intervention needed"
    exit 1
fi

echo "🎯 Post-experiment demo generation complete!"
```

### **Complete Post-Experiment Protocol**

```
EXPERIMENT COMPLETION WORKFLOW:

1. INDIVIDUAL METHOD COMPLETION:
   - Complete work on your method branch
   - Run pre-integration verification script
   - Merge to main with enhanced integration protocol

2. AUTOMATED DEMO GENERATION:
   bash generate_experiment_demo.sh [EXPERIMENT_NUM] [EXPERIMENT_NAME]

   This automatically:
   - Detects all implemented methods
   - Generates working comparison demo
   - Tests functionality equivalence
   - Validates all methods are accessible

3. EXPERIMENT REPORT ORGANIZATION:
   - Create reports/ folder for detailed analysis files
   - Move specialized reports: performance, development time, prediction analysis
   - Keep main EXPERIMENT_REPORT.md as executive summary
   - Organize structure:
     experiments/[NUM]/
     ├── EXPERIMENT_REPORT.md (executive summary)
     ├── PRE_EXPERIMENT_PREDICTIONS.md
     ├── reports/
     │   ├── PERFORMANCE_ANALYSIS.md
     │   ├── DEVELOPMENT_TIME_ANALYSIS.md
     │   ├── PREDICTION_ANALYSIS.md
     │   └── V4_FRAMEWORK_COMPARISON.md (if applicable)
     └── [method directories...]

4. FINAL VERIFICATION:
   - All method implementations working
   - Comparison demo runs successfully
   - Complete experiment report generated
   - Integration scripts validated

This ensures every experiment produces:
✅ Working implementations for all attempted methods
✅ Automated comparison and testing
✅ Comprehensive analysis and insights
✅ Clean integration without manual file copying

5. SYSTEMATIC DOCUMENTATION UPDATES:
   - Update findings/ documents with new patterns
   - Update FUTURE_EXPERIMENTS_ROADMAP.md with results
   - Update EXPERIMENT_INDEX.md with latest experiment
   - Update README.md if significant breakthroughs
   - Update any domain-specific analysis documents

   Framework Integration Updates:
   - Add experiment to FRAMEWORK_VERSION_LOG.md
   - Update methodology performance summaries
   - Document any framework enhancements discovered
   - Add to methodology selection guidance
```

---

## Enhanced Method Prompts

### **Method 1: Immediate Implementation (Enhanced)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK].

REQUIREMENTS (Baseline Specification):
[APPROVED_BASELINE_SPECIFICATION]

Start coding immediately with minimal planning. Focus on getting something working quickly.

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/1-immediate-implementation/

BRANCH ISOLATION:
git checkout -b exp-[EXPERIMENT_NUMBER]-immediate

ATOMIC COMMIT PROTOCOL:
Commit your progress frequently:
- git add -A && git commit -m "Initial: Starting implementation"
- git add -A && git commit -m "Core: Basic functionality working"
- git add -A && git commit -m "Feature: [specific feature added]"
- git add -A && git commit -m "COMPLETE: Working solution"

Commit every 2-3 minutes or when you complete any working functionality.

Technology: [TECH_STACK]
Show all work including commits.
```

### **Method 2: Human-Reviewed Specification (NEW)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK].

REQUIREMENTS (Baseline Specification):
[APPROVED_BASELINE_SPECIFICATION]

Follow a realistic specification-driven workflow with human oversight.

PROCESS:
1. Create comprehensive implementation specifications
2. [HUMAN REVIEW CHECKPOINT - specifications will be reviewed/edited]
3. Implement against approved specifications with quality discipline

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/2-specification-driven/

BRANCH ISOLATION:
git checkout -b exp-[EXPERIMENT_NUMBER]-specification

ATOMIC COMMIT PROTOCOL:
Track your progress with git commits:
- git add -A && git commit -m "Specs: Implementation approach documented"
- git add -A && git commit -m "Specs: Technical design complete"
- git add -A && git commit -m "Impl: Core structure created"
- git add -A && git commit -m "Impl: [Feature] implemented"
- git add -A && git commit -m "COMPLETE: All requirements met"

Technology: [TECH_STACK]
Show all work including commits.
```

### **Method 3: Test-First Development (Enhanced)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK] using strict TDD.

REQUIREMENTS (Baseline Specification):
[APPROVED_BASELINE_SPECIFICATION]

Follow Red-Green-Refactor with atomic commits:

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/3-test-first-development/

BRANCH ISOLATION:
git checkout -b exp-[EXPERIMENT_NUMBER]-tdd

ATOMIC COMMIT PROTOCOL:
- git add -A && git commit -m "Test: [feature] - RED"  (after writing failing test)
- git add -A && git commit -m "Impl: [feature] - GREEN" (after making test pass)
- git add -A && git commit -m "Refactor: [improvement]" (if refactoring)
- git add -A && git commit -m "COMPLETE: All tests passing"

Each test cycle should be a separate commit.
This creates a clear TDD history.

Technology: [TECH_STACK]
Show all work including commits.
```

### **Method 4: Adaptive TDD V4.1 (ENHANCED)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK].

REQUIREMENTS (Baseline Specification):
[APPROVED_BASELINE_SPECIFICATION]

Follow light planning with adaptive test validation based on complexity:

PROCESS:
1. Brief requirements analysis (5-10 minutes)
2. Identify key test scenarios and edge cases
3. Use TDD to implement against planned requirements
4. Apply test validation ONLY when you encounter:
   - Complex edge cases that could be implemented incorrectly
   - Non-obvious business logic that needs verification
   - Areas where a wrong implementation might still pass naive tests
   - Critical functionality where test quality matters most

ADAPTIVE VALIDATION APPROACH:
- Use your judgment to determine when extra validation adds value
- For straightforward functionality: standard TDD is sufficient
- For complex/critical areas: write intentionally wrong implementations to verify test robustness
- Document your validation decisions in commit messages

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/4-adaptive-tdd-v41/

BRANCH ISOLATION:
git checkout -b exp-[EXPERIMENT_NUMBER]-adaptive-tdd

ATOMIC COMMIT PROTOCOL:
- git add -A && git commit -m "Plan: Requirements analysis complete"
- git add -A && git commit -m "Test: [feature] test written"
- git add -A && git commit -m "Impl: [feature] implementation"
- git add -A && git commit -m "Validation: [area] robustness verified" (when applicable)
- git add -A && git commit -m "COMPLETE: All requirements implemented"

Strategic efficiency through adaptive complexity matching.

Technology: [TECH_STACK]
Show all work including commits.
```

---

## 🚀 Baseline Specification Examples

### **Example: Date Format Validator**

```
GENERATED BASELINE SPECIFICATION:

Core Functionality:
- Accept MM/DD/YYYY and DD/MM/YYYY formats
- Validate date logic (no Feb 30, handle leap years correctly)
- Return boolean valid/invalid result
- Handle basic edge cases (empty strings, malformed input)

Constraints:
- US and European formats only (no other international formats)
- No timezone support required
- No date arithmetic or manipulation
- No date parsing beyond format validation

Expected Behavior:
- "02/29/2024" → valid (leap year)
- "02/29/2023" → invalid (not leap year)
- "13/01/2024" → invalid in MM/DD, valid in DD/MM
- "" → invalid
- "not-a-date" → invalid

Exclusions:
- No internationalization beyond US/EU
- No advanced date libraries unless standard library
- No calendar system complexities
- No performance optimization for large datasets

EXPERIMENTER: [Approve/Edit this scope before proceeding]
```

### **Example: Phone Number Validator**

```
GENERATED BASELINE SPECIFICATION:

Core Functionality:
- Validate US phone number formats
- Accept (555) 123-4567, 555-123-4567, 5551234567 formats
- Return boolean valid/invalid result
- Basic format and length validation

Constraints:
- US numbers only (no international)
- No phone number lookup or carrier validation
- No extension support
- No formatting/normalization output

Expected Behavior:
- "(555) 123-4567" → valid
- "555-123-4567" → valid
- "5551234567" → valid
- "555-123-456" → invalid (too short)
- "555-123-45678" → invalid (too long)

Exclusions:
- No international number support
- No real phone number database validation
- No area code validity checking
- No extension parsing

EXPERIMENTER: [Approve/Edit this scope before proceeding]
```

---

## 📊 Experimental Variations

### **Baseline Specification Variants**

**Minimal Baseline**: Core functionality only
- Essential requirements
- Basic constraints
- Minimal edge cases

**Standard Baseline**: Typical project scope (default)
- Complete functionality description
- Reasonable constraints
- Key edge cases covered

**Detailed Baseline**: Comprehensive requirements
- Extensive functionality specification
- Detailed constraints and exclusions
- Comprehensive edge case coverage

### **Research Questions**
1. How do methodologies perform with identical scope?
2. Which approach handles ambiguity most effectively?
3. What's the optimal specification detail level?
4. How does baseline scope affect methodology choice?

---

## 🎯 Integration with Existing Research

### **Preserving Scientific Rigor**
- **Controlled experiments**: Identical baselines eliminate interpretation variance
- **Quantitative metrics**: Code quality, time, test coverage comparisons
- **Reproducibility**: Baseline specifications enable exact replication

### **Building on Phase 1 Findings**
- **TDD constraint effectiveness**: Validated across domains
- **Specification-driven risks**: Controlled through baseline approval
- **Practical team workflows**: Focus on real-world applicability

---

## 💡 Usage Protocol

### **Standard Experiment Flow**
1. **Generate baseline**: `spawn-experiments` + APPLICATION_TYPE
2. **Review/approve scope**: Experimenter edits generated baseline
3. **Generate predictions**: AI predicts methodology outcomes before execution
4. **Launch parallel execution**: Four methods with identical baseline
5. **Analyze methodology effectiveness**: Compare actual vs predicted results
6. **Clean integration**: Merge completed work back to main

### **Experimenter Commands**
```bash
cd /home/ivan/projects/spawn-experiments
# Say "spawn-experiments" to Claude
# Provide APPLICATION_TYPE and TECH_STACK
# Review and approve generated baseline
# Launch four parallel method executions
# Compare results and integrate to main
```

---

## 🔮 Research Applications

### **For Development Teams**
- **Evidence-based methodology selection** for defined project scopes
- **Process optimization** based on quantified outcomes
- **Quality prediction** through methodology characteristics

### **For Researchers**
- **Methodology effectiveness measurement** with controlled scope
- **Baseline specification optimization** studies
- **Cross-domain validation** of methodology patterns

---

*Version 4.0 transforms spawn-experiments from pathology study to practical methodology optimization, enabling teams to make evidence-based decisions about AI collaboration approaches.*