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

### **Branch Isolation Protocol** (Add to ALL prompts)

```
IMPORTANT: Create a dedicated branch for your experiment:

git checkout -b exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]

Examples:
- git checkout -b exp-1504-immediate
- git checkout -b exp-1504-specification
- git checkout -b exp-1504-tdd
- git checkout -b exp-1504-validated

This enables:
- Clean experiment isolation
- Main branch protection
- Easy comparison between methods
- Clean integration when complete
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

### **Integration Protocol**

```
EXPERIMENT COMPLETION:

1. Complete work on feature branch
2. Create comprehensive experiment report
3. Merge back to main with clean summary commit
4. Keep branches for historical analysis

git checkout main
git merge --no-ff exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]
git commit -m "Complete: [EXPERIMENT_NUMBER] [METHOD_NAME] methodology"
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

### **Method 4: Specification-Guided TDD (NEW)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK].

REQUIREMENTS (Baseline Specification):
[APPROVED_BASELINE_SPECIFICATION]

Follow light planning followed by TDD implementation:

PROCESS:
1. Brief requirements analysis (5-10 minutes)
2. Identify key test scenarios and edge cases
3. Use TDD to implement against planned requirements

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/4-specification-guided-tdd/

BRANCH ISOLATION:
git checkout -b exp-[EXPERIMENT_NUMBER]-guided-tdd

ATOMIC COMMIT PROTOCOL:
- git add -A && git commit -m "Plan: Requirements analysis complete"
- git add -A && git commit -m "Test: [feature] test written"
- git add -A && git commit -m "Impl: [feature] implementation"
- git add -A && git commit -m "COMPLETE: All requirements implemented"

Balance planning efficiency with implementation discipline.

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
3. **Launch parallel execution**: Four methods with identical baseline
4. **Analyze methodology effectiveness**: Pure process comparison
5. **Clean integration**: Merge completed work back to main

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