# Post-Experiment Checklist and Report Protocol

## Problem Statement

Experiments need consistent, comprehensive reports that:
- Summarize results clearly for future reference
- Provide practical testing instructions with appropriate warnings
- Document any protocol violations or issues
- Enable reproducible validation of claims

## Solution: Mandatory Post-Experiment Report Protocol

### Required Report Structure

Every experiment must conclude with an `EXPERIMENT_REPORT.md` that includes:

#### 1. Executive Summary
```markdown
# Experiment NNN: [Project Name] - Methodology Comparison Report

## Executive Summary
- **Objective**: [Clear problem statement]
- **Duration**: [Start - End times]
- **Key Finding**: [One sentence main result]
- **Validity Status**: [Clean/Compromised with explanation]
```

#### 2. Methodology Results (All 4 Approaches)
For each approach, document:
- **Duration**: Actual development time
- **Approach**: Brief methodology description
- **Key Features**: What was implemented
- **Lines of Code**: Approximate count
- **Testing**: What validation was performed
- **Notable**: Standout characteristics

#### 3. Testing Instructions with Warnings

**Critical Section**: Must include practical guidance for reproducing results

```markdown
## Testing Instructions

### Quick Test Candidates (< 30 seconds)
- `experiments/NNN/2-specification-driven/` - Minimal dependencies
- `experiments/NNN/4-validated-test-development/` - Usually clean

### Slow Test Warnings (> 2 minutes)
⚠️ **AVOID for quick testing:**
- `1-immediate-implementation/` - Heavy deps: pandas, matplotlib, nltk
- `3-tdd-approach/` - Package structure may have import issues

### Testing Commands
```bash
# Safe approach
cd experiments/NNN/2-specification-driven
uv run --with-requirements requirements.txt demo.py

# Heavy approach (slow install)
cd experiments/NNN/1-immediate-implementation
uv run --with-requirements requirements.txt multilingual_word_counter.py
# ⚠️ Warning: Will install pandas (~50MB), matplotlib (~30MB), nltk models
```

### Expected Outputs
- Approach 1: [What to expect]
- Approach 2: [What to expect]
- [etc.]
```

#### 4. Development Process Analysis

**Critical Section**: Must include analysis of development session logs

```markdown
## Development Process Analysis

### Session Logs Available
Each approach directory contains `DEVELOPMENT_SESSION.log` with complete development process:
- All commands executed
- File operations and discoveries
- Error/retry cycles
- Component discovery patterns

### Key Analysis Points
- **Component Discovery**: Did approach explore `utils/` directories?
- **Evaluation Process**: How were found components assessed?
- **Integration Decisions**: Evidence of reuse vs. rebuild choices
- **Error Handling**: Recovery patterns and debugging approaches
- **Development Flow**: Sequential vs. iterative implementation patterns

### Example Analysis
```bash
# Component discovery analysis
grep -n "ls utils\|cat utils" experiments/NNN/*/DEVELOPMENT_SESSION.log

# Error recovery patterns
grep -A3 -B3 "Error\|error\|failed" experiments/NNN/*/DEVELOPMENT_SESSION.log

# File creation timeline
grep "nano\|vim\|Edit\|Write" experiments/NNN/*/DEVELOPMENT_SESSION.log
```
```

#### 4. Protocol Compliance Assessment
```markdown
## Protocol Compliance

### Bias Prevention Status
- ✅/❌ **Neutral Naming**: Used required 1-immediate-implementation format
- ✅/❌ **Language Check**: No bias indicators detected
- ✅/❌ **Parallel Execution**: All approaches launched simultaneously

### Issues Detected
- [Any protocol violations]
- [Impact on validity]
- [Recommended corrections]
```

#### 5. Comparative Analysis
```markdown
## Key Comparisons

### Development Speed
1. [Fastest] - X minutes
2. [Second] - Y minutes
[etc.]

### Code Complexity
- **Simplest**: [Approach] - [Lines of code]
- **Most Complex**: [Approach] - [Lines of code]

### Feature Completeness
- **Most Features**: [Approach] - [Feature list]
- **Most Focused**: [Approach] - [Core features only]

### Architectural Quality
- **Best Structure**: [Approach] - [Why]
- **Most Testable**: [Approach] - [Test coverage/quality]
```

#### 6. Practical Recommendations
```markdown
## When to Use Each Approach

### Use Immediate Implementation When:
- [Specific scenarios]
- [Trade-offs to consider]

### Use Specification-Driven When:
- [Specific scenarios]
- [Trade-offs to consider]

[etc. for all 4 approaches]
```

### Mandatory Quality Gates

#### Before Report Completion
- [ ] All 4 approaches documented with timing
- [ ] Testing instructions include dependency warnings
- [ ] Protocol compliance assessed and documented
- [ ] At least one "quick test" path identified
- [ ] All claims are testable/reproducible

#### Testing Instruction Requirements
- **Must include**: Specific commands to reproduce results
- **Must warn**: About heavy dependencies or slow installs
- **Must identify**: At least one fast testing path
- **Must document**: Expected outputs for validation

#### Protocol Violation Handling
- **Any violations**: Must be prominently documented in report
- **Impact assessment**: How violations affect result validity
- **Remediation**: Clear steps to correct issues in future experiments

### Report Quality Standards

#### Dependency Warnings
Every report must categorize approaches by testing speed:
- **Quick (<30s)**: Minimal dependencies, fast validation
- **Medium (30s-2m)**: Moderate setup time
- **Slow (>2m)**: Heavy dependencies, warn users
- **Broken**: Import/setup issues, document problems

#### Example Dependency Warning Format
```markdown
⚠️ **SLOW INSTALL WARNING**:
`1-immediate-implementation/` requires pandas (50MB), matplotlib (30MB), nltk models (100MB+)
Expected install time: 2-5 minutes on first run
Use `2-specification-driven/` for quick testing instead.
```

#### Reproducibility Requirements
- All timing claims must be testable
- All feature claims must be demonstrable
- All architecture claims must be verifiable through inspection
- All comparative statements must be substantiated

## Implementation Template

### Report Generation Command
```markdown
"Generate comprehensive experiment report following design/13_POST_EXPERIMENT_CHECKLIST.md:
- Document all 4 approaches with timing and features
- Include testing instructions with dependency warnings
- Assess protocol compliance and note any violations
- Provide practical recommendations for each methodology
- Ensure all claims are testable and reproducible"
```

### Quality Validation Checklist
- [ ] Executive summary captures key findings
- [ ] All 4 approaches documented consistently
- [ ] Testing warnings prevent user frustration
- [ ] Protocol compliance honestly assessed
- [ ] Comparative analysis is substantiated
- [ ] Practical recommendations are actionable

## Success Criteria

### Report Completeness
- Future researchers can understand results without reading individual approaches
- Users can quickly test claims without dependency surprises
- Protocol violations are transparent and documented
- Methodology trade-offs are clearly articulated

### User Experience
- Clear guidance on which approach to test first
- Accurate warnings about time/resource requirements
- Reproducible validation paths for all claims
- Honest assessment of any experimental issues

## Conclusion

This post-experiment protocol ensures that each experiment concludes with a comprehensive, honest, and practically useful report that serves both research validation and future methodology selection needs.

**Key Innovation**: Mandatory testing warnings prevent user frustration and enable rapid validation of experimental claims while maintaining transparency about any methodological issues.