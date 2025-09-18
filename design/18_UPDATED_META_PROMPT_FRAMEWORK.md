# Updated Meta Prompt Framework for Discovered Components

## Integration with Generative Architecture

The meta prompt framework now supports the **discovered components** approach while maintaining experimental integrity and bias prevention protocols.

## Meta Prompt Template Structure

### Required Opening Sequence
```markdown
"I understand you want to compare TDD methodologies for [PROJECT DESCRIPTION].

EXPERIMENTAL SETUP CONFIRMATION:
I will create 4 parallel agents using these EXACT protocols:

✓ Neutral naming: 1-immediate-implementation, 2-specification-driven, 3-test-first-development, 4-validated-test-development
✓ No bias language: No quality indicators (naive/advanced/optimal) or expectation statements
✓ Parallel execution: All 4 methodologies launched simultaneously
✓ Equal conditions: Identical starting prompts and timing mechanisms
✓ No explicit component guidance: Agents discover existing codebase components naturally

Proceed with bias-neutral parallel experiment? (Y/N)"
```

### User Confirmation Gate
**MANDATORY**: Must receive explicit "Y" or "Yes" before proceeding.
- Any other response triggers protocol review
- Agent cannot proceed without clear confirmation

### Post-Confirmation Execution
```markdown
"Creating 4 parallel agents with identical starting conditions.
Each agent will receive the same problem specification with no mention of existing components.
Natural discovery of ./utils/ components will be measured as part of methodology behavior.

IMPORTANT: Each experiment directory will auto-generate DEVELOPMENT_SESSION.log capturing complete development process for analysis."
```

## Component Environment Setup

### Directory Structure (Pre-Experiment)
```
project/
├── experiments/
│   ├── 010-palindrome/
│   ├── 020-textstats/
│   └── ...
├── utils/
│   ├── functions/           # Tier 1 outputs go here
│   │   ├── word_counter.py
│   │   ├── palindrome.py
│   │   └── ...
│   └── tools/              # Tier 2 outputs go here
│       ├── textstats.py
│       ├── logparse.py
│       └── ...
└── design/
```

### Component Population Protocol
1. **After Tier 1**: Copy best implementations to `./utils/functions/`
2. **After Tier 2**: Copy best tools to `./utils/tools/`
3. **No documentation**: Let agents discover organically
4. **No explicit references**: In experiment prompts

## Prompt Specification Format

### Standard Problem Specification (Clean)
```markdown
"Implement a [DESCRIPTION OF TOOL/FUNCTION/APPLICATION].

Requirements:
- [Specific functional requirements]
- [Performance or quality criteria]
- [Interface specifications]
- [Testing requirements]

Use your assigned methodology: [METHODOLOGY NAME]
Time limit: [DURATION]
Output working implementation with appropriate testing."
```

### What NOT to Include
- ❌ "You may use existing components"
- ❌ "Check the utils/ directory"
- ❌ "Leverage any available functions"
- ❌ Any mention of component discovery

### What IS Allowed
- ✅ Standard problem requirements
- ✅ Technology constraints (stdlib only, etc.)
- ✅ Interface specifications
- ✅ Quality criteria

## Discovery Measurement Protocol

### Automatic Tracking
Monitor agent behavior for:
- **File exploration**: Did agent examine `./utils/` directories?
- **Component evaluation**: Did agent inspect available implementations?
- **Integration decisions**: Did agent choose to use, modify, or ignore components?
- **Implementation strategy**: How did discovery affect approach?

### Component Usage Detection
```python
# Automatic detection of:
from utils.functions.word_counter import count_words
from utils.tools.textstats import TextStatsEngine

# Vs. novel implementations:
def count_words(text):  # Built from scratch
```

### Research Data Collection
- **Discovery Timeline**: When did agent find components?
- **Evaluation Process**: How did agent assess component quality?
- **Integration Method**: How were components incorporated?
- **Architecture Impact**: How did discovery influence design decisions?

## Bias Prevention Integration

### Component Placement Neutrality
- **No quality indicators**: Don't label components as "good" or "proven"
- **Uniform naming**: Standard filename conventions only
- **No documentation bias**: Basic docstrings only, no quality claims
- **Equal accessibility**: All components equally discoverable

### Methodology Isolation
- **Independent environments**: Each methodology runs in separate working directory
- **No cross-contamination**: Agents cannot see other trial outputs
- **Identical starting conditions**: Same component ecosystem for all
- **Natural behavior**: No artificial prompting toward component usage

## Expected Behavioral Patterns

### Immediate Implementation
- **Likely behavior**: Build quickly, may miss component discovery
- **Discovery pattern**: If found, quick integration without extensive evaluation
- **Integration style**: Direct usage with minimal modification

### Specification-Driven
- **Likely behavior**: Systematic codebase exploration before implementation
- **Discovery pattern**: Thorough evaluation of component quality and fit
- **Integration style**: Careful integration with specification compliance

### Test-First Development
- **Likely behavior**: Incremental discovery during implementation cycles
- **Discovery pattern**: Test-driven evaluation of component reliability
- **Integration style**: Component testing before integration

### Validated Test Development
- **Likely behavior**: Component validation against requirements
- **Discovery pattern**: Systematic component quality assessment
- **Integration style**: Wrong implementation testing to validate component choice

## Success Metrics

### Discovery Effectiveness
- **Exploration Rate**: Percentage of methodologies that discover components
- **Evaluation Quality**: Depth of component assessment before use
- **Integration Success**: How cleanly components are incorporated
- **Architecture Impact**: How discovery influences system design

### Methodology Authenticity
- **Natural Behavior**: Do patterns match expected methodology characteristics?
- **Decision Quality**: Are component usage decisions well-reasoned?
- **Implementation Consistency**: Do approaches maintain methodology integrity?

## Validation Framework

### Component Quality Standards
- **Functional Correctness**: Components must work as documented
- **Interface Clarity**: Clear usage patterns and examples
- **Test Coverage**: Components must be thoroughly tested
- **Documentation**: Basic docstrings explaining purpose and usage

### Discovery Environment Consistency
- **Equal Access**: All methodologies have identical component access
- **No Bias Signals**: Component presentation is methodology-neutral
- **Authentic Conditions**: Discovery process mirrors real development scenarios

## Research Value

### Authentic Development Insights
This framework provides unprecedented insight into:
- **Natural Discovery Patterns**: How methodologies organically explore codebases
- **Component Evaluation**: What criteria drive reuse vs. rebuild decisions
- **Integration Strategies**: How methodologies incorporate existing work
- **Architecture Evolution**: How component availability influences system design

### Methodology Differentiation
Different approaches will reveal:
- **Exploration Behaviors**: Systematic vs. opportunistic component discovery
- **Quality Assessment**: How methodologies evaluate component fitness
- **Integration Philosophy**: Reuse vs. rebuild decision patterns
- **System Architecture**: How discovery influences overall design choices

## Conclusion

This updated meta prompt framework preserves experimental integrity while enabling study of realistic development scenarios with existing codebases. By removing explicit component guidance while maintaining discoverable environments, we can observe authentic methodology behaviors in conditions that mirror real software development projects.