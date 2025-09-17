# Independent Experiment Protocol Using Augment CLI

## Problem Statement
AI agents with context awareness cannot perform truly independent experiments because they retain knowledge from previous approaches. This contaminates methodology comparisons.

## Solution: Isolated Repository Approach
*Note: This protocol describes one potential approach for achieving independence. Other AI tools may have different capabilities for parallel execution.*

### Core Concept
Create four separate repositories, each containing only:
1. The problem statement
2. Method-specific prompts
3. No knowledge of other approaches

Use Augment CLI to execute each experiment in complete isolation.

## Repository Structure

### Master Repository: `tdd-demo`
Contains:
- Experimental design documentation
- Problem specifications
- Evaluation criteria
- Results compilation scripts
- This protocol document

### Method Repositories (4 separate repos):
- `tdd-method-1-naive`
- `tdd-method-2-spec-first` 
- `tdd-method-3-tdd`
- `tdd-method-4-enhanced-tdd`

Each method repo contains ONLY:
- `README.md` - Problem statement and method instructions
- `PROMPT.md` - Exact prompt for the AI agent
- Empty workspace for implementation

## Implementation Protocol

### Phase 1: Repository Setup
```bash
# Create four isolated repositories
mkdir tdd-method-1-naive && cd tdd-method-1-naive && git init
mkdir tdd-method-2-spec-first && cd tdd-method-2-spec-first && git init
mkdir tdd-method-3-tdd && cd tdd-method-3-tdd && git init
mkdir tdd-method-4-enhanced-tdd && cd tdd-method-4-enhanced-tdd && git init
```

### Phase 2: Problem Distribution
For each experiment (e.g., "Unicode Password Manager"):

1. **Create identical problem statements** in each repo's README.md
2. **Add method-specific prompts** in each repo's PROMPT.md
3. **Ensure no cross-contamination** - no references to other methods
4. **Version control each repo** independently

### Phase 3: Execution
```bash
# Execute each method in isolation using Augment CLI
cd tdd-method-1-naive
augment --prompt "$(cat PROMPT.md)" --workspace .

cd ../tdd-method-2-spec-first  
augment --prompt "$(cat PROMPT.md)" --workspace .

cd ../tdd-method-3-tdd
augment --prompt "$(cat PROMPT.md)" --workspace .

cd ../tdd-method-4-enhanced-tdd
augment --prompt "$(cat PROMPT.md)" --workspace .
```

### Phase 4: Results Compilation
```bash
# Copy results back to master repo for analysis
cp tdd-method-1-naive/* tdd-demo/experiments/001-unicode-password-manager/method-1-naive/
cp tdd-method-2-spec-first/* tdd-demo/experiments/001-unicode-password-manager/method-2-spec-first/
# etc.
```

## Prompt Templates

### Method 1: Naive Approach
```markdown
# Problem: [PROBLEM_DESCRIPTION]

Build a [APPLICATION_TYPE] using [TECH_STACK].

Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]

Please implement this application. Focus on getting it working quickly.
```

### Method 2: Specification-First
```markdown
# Problem: [PROBLEM_DESCRIPTION]

Build a [APPLICATION_TYPE] using [TECH_STACK].

Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2] 
- [REQUIREMENT_3]

Please follow this approach:
1. First, write detailed specifications for all components
2. Design the architecture and interfaces
3. Then implement according to your specifications
4. Include validation and error handling
```

### Method 3: TDD Approach
```markdown
# Problem: [PROBLEM_DESCRIPTION]

Build a [APPLICATION_TYPE] using [TECH_STACK].

Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]

Please use Test-Driven Development:
1. Write a failing test (RED)
2. Write minimal code to make it pass (GREEN)
3. Refactor the code while keeping tests passing (REFACTOR)
4. Repeat for each feature

Follow strict TDD discipline throughout.
```

### Method 4: Enhanced TDD
```markdown
# Problem: [PROBLEM_DESCRIPTION]

Build a [APPLICATION_TYPE] using [TECH_STACK].

Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]

Please use Enhanced Test-Driven Development:
1. Write a failing test (RED)
2. VALIDATE the test by ensuring it fails for the right reasons
3. Write minimal code to make it pass (GREEN)
4. VALIDATE the test actually catches bugs by breaking the code
5. Refactor while keeping tests passing (REFACTOR)
6. Repeat for each feature

Focus on test quality and validation throughout.
```

## Execution Checklist

### Pre-Execution
- [ ] Four isolated repositories created
- [ ] Identical problem statements in each repo
- [ ] Method-specific prompts prepared
- [ ] No cross-references between repos
- [ ] Clean workspace in each repo

### During Execution
- [ ] Execute methods in random order (not 1-2-3-4)
- [ ] Use same Augment CLI version for all
- [ ] Document execution time for each
- [ ] Capture all outputs and intermediate steps
- [ ] No human intervention during execution

### Post-Execution
- [ ] Copy all results to master repo
- [ ] Run comparative analysis
- [ ] Document any execution issues
- [ ] Archive method repos for reproducibility

## Advantages of This Approach

### True Independence
- Each AI agent sees only the problem and method instructions
- No contamination from other approaches
- No progressive learning effects
- Pure methodology comparison

### Reproducibility
- Exact prompts preserved
- Execution environment documented
- Results can be independently verified
- Method repos can be shared for replication

### Scalability
- Easy to add new methods
- Can test different AI agents
- Can vary problem complexity
- Can test framework variations (unittest vs pytest)

## Limitations

### Setup Overhead
- Requires creating and managing multiple repos
- More complex execution process
- Results compilation step needed

### Augment CLI Dependencies
- Requires Augment CLI access
- May have different behavior than interactive sessions
- Command-line limitations vs full IDE integration

### Evaluation Complexity
- Results in different formats/structures
- May need normalization for comparison
- Harder to do real-time analysis

## Success Metrics

### Independence Verification
- No references to other methods in generated code
- No evidence of cross-contamination in approach
- Methodology adherence matches prompt instructions

### Quality Comparison
- Objective metrics (test coverage, complexity, bugs)
- Functionality completeness
- Code quality and maintainability
- Development time and iterations

## Next Steps

1. **Test the protocol** with a simple experiment (temperature converter)
2. **Refine prompts** based on initial results
3. **Automate the process** with scripts
4. **Scale to complex experiments** once validated

---

**This protocol enables truly independent methodology comparisons by eliminating AI context contamination through repository isolation.**
