# META_PROMPT_GENERATOR_MODIFICATION - Code Modification Experiment Framework

**Purpose**: Generate standardized modification prompts for testing artifact modifiability across different development methodologies

## Core Research Question

Which development methodology (1-4) produces code artifacts that are most effectively modified by AI agents in subsequent iterations?

## Modification Task Categories

### 1. Feature Addition Prompts

```
You are working with an existing [PROBLEM_TYPE] implementation at [PATH].

Add the following feature without breaking existing functionality:
[FEATURE_DESCRIPTION]

Requirements:
- Maintain all existing tests passing
- Add appropriate tests for the new feature
- Follow the existing code style and patterns
- Document your changes appropriately

Time your work and note when you achieve:
1. Understanding of existing code
2. First successful modification
3. All tests passing
```

### 2. Behavior Change Prompts

```
You are working with an existing [PROBLEM_TYPE] implementation at [PATH].

Modify the behavior to:
[BEHAVIOR_CHANGE]

This is an intentional breaking change. Update all affected tests to reflect the new expected behavior.

Requirements:
- Update implementation to match new behavior
- Fix all tests to expect new behavior
- Ensure no unintended side effects
- Maintain code quality

Time your work and report total duration.
```

### 3. Bug Fix Prompts

```
You are working with an existing [PROBLEM_TYPE] implementation at [PATH].

Users have reported the following issue:
[BUG_DESCRIPTION]

Requirements:
- Diagnose the root cause
- Fix the bug with minimal code changes
- Add test(s) that would have caught this bug
- Ensure no regression in other functionality

Time your work and note:
- Time to locate the bug
- Time to implement fix
- Time to add comprehensive tests
```

### 4. Refactoring Prompts

```
You are working with an existing [PROBLEM_TYPE] implementation at [PATH].

Refactor the code to:
[REFACTORING_GOAL]

Requirements:
- No functional changes (all tests must pass unchanged)
- Improve code structure/readability/maintainability
- Follow [PATTERN] design pattern if specified
- Document architectural decisions

Time your work and report total duration.
```

### 5. Performance Optimization Prompts

```
You are working with an existing [PROBLEM_TYPE] implementation at [PATH].

Optimize the implementation for:
[PERFORMANCE_METRIC]

Requirements:
- Maintain all existing functionality
- Demonstrate performance improvement
- Keep code readable and maintainable
- Update tests if needed for new implementation

Time your work and measure performance before/after.
```

## Specific Modification Tasks for Roman Numeral Converter (Experiment 013)

### Feature Addition: Vinculum Support
```
Add support for Roman numerals beyond 3999 using vinculum notation (overline for ×1000).
For example: V̄ = 5000, X̄ = 10000, L̄ = 50000

Since overlines are hard to type, use parentheses to indicate vinculum:
- (V) = 5000
- (X) = 10000
- (L) = 50000
- (IV) = 4000
- etc.

Support range should extend to 3,999,999.
```

### Behavior Change: Strict Validation Mode
```
Add a 'strict' parameter that when True:
- Rejects lowercase input (currently accepts)
- Rejects repeated characters beyond classical limits (no IIII, only IV)
- Enforces proper subtractive notation order
- Returns specific error messages for each validation failure

Default behavior (strict=False) should remain unchanged.
```

### Bug Fix: Edge Case Handling
```
Users report that the converter accepts invalid Roman numerals like:
- "IIV" (should be III)
- "VV" (should be X)
- "MMMMM" (exceeds maximum)

Fix validation to properly reject these while maintaining performance.
```

### Refactoring: Strategy Pattern
```
Refactor to use Strategy pattern:
- Create RomanNumeralStrategy interface/base class
- Implement ClassicalStrategy (current 1-3999)
- Prepare for VinculumStrategy (extended range)
- Allow strategy injection for different conversion rules
```

### Performance Optimization: Caching
```
Add memoization/caching for frequently converted values.
Benchmark shows 80% of conversions are for values under 100.
Optimize for this use case while maintaining correctness.
```

## Experimental Protocol

### Phase 1: Baseline Measurement
1. Apply each modification to all 4 methodology outputs
2. Use fresh AI agent context for each modification
3. Record timing and quality metrics
4. No access to original development prompts

### Phase 2: Cross-Methodology Analysis
1. Compare modification times across methodologies
2. Identify which artifacts agents reference most
3. Measure bug introduction rates
4. Analyze test adaptation patterns

### Phase 3: Pattern Recognition
1. Which methodology consistently enables fastest modifications?
2. Do certain modification types favor certain methodologies?
3. How does test coverage affect modification confidence?
4. What documentation actually gets used?

## Measurement Framework

### Quantitative Metrics
- **Time to first edit**: How long before the agent makes its first code change?
- **Total modification time**: Complete time from start to passing tests
- **File access patterns**: Which files are read and in what order?
- **Test modifications**: How many tests needed updating?
- **Bug introduction rate**: New bugs introduced during modification
- **Code quality delta**: Complexity/maintainability change

### Qualitative Assessments
- **Confidence indicators**: Does the agent express uncertainty?
- **Exploration patterns**: How does the agent navigate the codebase?
- **Documentation usage**: Which docs/comments prove helpful?
- **Error recovery**: How does the agent handle mistakes?

## Bias Prevention Protocols

### Neutral Language Requirements
- Never use quality indicators (good/bad/better/worse)
- Don't mention methodology origins
- Present all modifications as equally valid requests
- Avoid leading questions about difficulty

### Standardization Controls
- Identical prompts for each methodology's artifacts
- Same AI model for all modifications
- Fresh context (no conversation history)
- Randomized execution order

## Example Execution Pattern

```python
# For each completed Tier 1 experiment:
experiments = ["010-password-generator", "011-prime-number", "012-anagram", "013-roman"]

for experiment in experiments:
    for modification in ["feature", "behavior", "bugfix", "refactor", "optimize"]:
        for method in ["1-immediate", "2-specification", "3-test-first", "4-validated"]:
            # Launch fresh agent with modification prompt
            # Measure and record results
            # No cross-contamination between runs
```

## Expected Outcomes

### Hypothesis 1: T2D2 Superiority
Methods 3 & 4 (test-driven) will enable fastest modifications due to:
- Comprehensive test coverage providing safety net
- Tests as executable documentation
- Clear behavioral contracts

### Hypothesis 2: Documentation Overhead
Method 2's extensive documentation may actually slow modifications if:
- Agents must parse prose to understand intent
- Documentation is out of sync with code
- Specifications over-constrain solution space

### Hypothesis 3: Modification-Type Dependency
- Feature additions favor comprehensive tests (Methods 3 & 4)
- Refactoring favors minimal coupling (Method 1)
- Bug fixes favor detailed documentation (Method 2)
- Performance optimization favors clean baselines (Method 1)

## Research Impact

### For AI Development Practices
- Evidence-based guidance on artifact optimization
- Quantitative data on documentation value
- Test coverage ROI for AI modification

### For Tool Development
- Inform AI agent design for code modification
- Identify helpful metadata and patterns
- Guide code generation strategies

### For Methodology Evolution
- Shift from "human-readable" to "AI-modifiable" code
- New quality metrics for AI-maintained systems
- Evolution of development practices for AI-first world

## Implementation Timeline

1. **Week 1**: Finalize modification prompts and measurement framework
2. **Week 2**: Run pilot study on Experiment 013 (Roman Numerals)
3. **Week 3**: Refine based on pilot results
4. **Week 4**: Full rollout across all Tier 1 experiments
5. **Week 5**: Analysis and report generation
6. **Week 6**: Publication and community feedback

## Success Criteria

- Clear statistical significance in modification times
- Reproducible patterns across problem types
- Actionable insights for development teams
- Community validation of findings

---

*This framework enables systematic study of code modifiability in the post-T2D2 era, where AI agents are primary code maintainers rather than human developers.*