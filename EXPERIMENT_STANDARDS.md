# TDD Experiment Standards & Protocols

## Bias Prevention Protocol

### Core Principle
**All experimental setup must use neutral language that does not suggest quality expectations or bias toward any methodology.**

### Standardized Neutral Naming

#### Directory Names (FIXED - Never Vary)
- `1-immediate-implementation/` - Implementation begins directly
- `2-specification-driven/` - Specification-first approach
- `3-test-first-development/` - Test-driven development
- `4-validated-test-development/` - Enhanced test validation

#### Forbidden Terms
❌ **NEVER USE**: naive, simple, basic, advanced, sophisticated, better, worse, optimal, suboptimal
✅ **USE INSTEAD**: immediate, direct, specification-driven, test-first, validated

### Method Descriptions (Standardized)

#### Method 1: Immediate Implementation
- "Implementation begins directly with coding"
- "Focus on rapid functionality delivery"
- "Organic development approach"

#### Method 2: Specification-Driven
- "Two-phase approach with specification then implementation"
- "Requirements-focused development"
- "Structured planning process"

#### Method 3: Test-First Development
- "Test-driven development with Red-Green-Refactor cycles"
- "Test-first implementation pattern"
- "Incremental feature building"

#### Method 4: Validated Test Development
- "Enhanced test-driven approach with validation procedures"
- "Comprehensive test verification process"
- "Rigorous quality gates"

## Routinized Setup Process

### 1. Automated Setup (Preferred)
```bash
python setup_experiment.py "experiment-name" --app-type "Application Description" --tech-stack "Python"
```

### 2. Manual Setup Checklist
If automation fails, follow this exact sequence:

#### Directory Structure
```
experiments/
└── NNN-experiment-name/
    ├── 1-immediate-implementation/
    ├── 2-specification-driven/
    ├── 3-test-first-development/
    └── 4-validated-test-development/
```

#### Required Files (Each Method Directory)
- `README.md` - Neutral method description
- `PROMPT.md` - Exact agent instructions
- `TIMING_LOG.txt` - Placeholder for timing data
- `.git/` - Initialized repository

#### Experiment-Level Files
- `EXPERIMENT_OVERVIEW.md` - Neutral experiment description
- `experiment_metadata.json` - Machine-readable configuration

### 3. Quality Assurance Checklist

Before launching experiment, verify:

#### ✅ Language Neutrality
- [ ] No bias terms in directory names
- [ ] No quality expectations in descriptions
- [ ] Identical success criteria across methods
- [ ] Neutral prompt language

#### ✅ Structural Consistency
- [ ] All four method directories present
- [ ] Git repositories initialized
- [ ] Required files in each directory
- [ ] Standardized naming convention

#### ✅ Prompt Accuracy
- [ ] Prompts match META_PROMPT_GENERATOR exactly
- [ ] Technology stack correctly substituted
- [ ] Application type correctly substituted
- [ ] No additional instructions added

## Execution Protocol

### Agent Assignment (Random)
```bash
# Generate random method assignment
methods=("1-immediate-implementation" "2-specification-driven" "3-test-first-development" "4-validated-test-development")
shuffled=($(shuf -e "${methods[@]}"))

# Assign agents to randomized methods
echo "Agent 1: ${shuffled[0]}"
echo "Agent 2: ${shuffled[1]}"
echo "Agent 3: ${shuffled[2]}"
echo "Agent 4: ${shuffled[3]}"
```

### Timing Capture
- Automated via Task tool timing
- Manual backup in TIMING_LOG.txt
- Phase transition timestamps
- Completion timestamps

### Commit Protocol
- Frequent commits showing progression
- Descriptive commit messages
- Phase tagging (RED, GREEN, REFACTOR)
- No commit message bias

## Analysis Standards

### Objective Measurement
- Development time (start to working implementation)
- Lines of code / complexity metrics
- Test coverage percentages
- Bug count in initial implementation
- Feature completeness score

### Qualitative Assessment
- Code readability (standardized rubric)
- Maintainability indicators
- Documentation quality
- Error handling robustness

### Bias-Free Reporting
- Report unexpected outcomes
- Question assumptions when results contradict expectations
- Consider context-dependent effectiveness
- Acknowledge limitation of single-trial results

## Validation Checklist

Before each experiment:

### Pre-Execution
- [ ] Used setup_experiment.py or followed manual checklist exactly
- [ ] Verified neutral language throughout
- [ ] Confirmed prompt accuracy via diff against META_PROMPT_GENERATOR
- [ ] Randomized method assignments (if using multiple agents)

### During Execution
- [ ] No additional guidance beyond PROMPT.md
- [ ] No quality hints or suggestions
- [ ] Timing data captured consistently
- [ ] Commit protocols followed

### Post-Execution
- [ ] Results documented objectively
- [ ] Unexpected outcomes highlighted
- [ ] Methodology adherence assessed
- [ ] Bias sources identified and mitigated

## Version Control

This protocol is version 2.0. Changes require:
1. Version number increment
2. Documentation of changes
3. Rationale for modifications
4. Validation with test experiment

## Emergency Protocol Breach

If bias is detected mid-experiment:
1. Stop all affected method executions
2. Document the bias source
3. Reset affected methods with corrected setup
4. Note the correction in experiment report

**Remember: The goal is objective comparison, not confirmation of preconceptions.**