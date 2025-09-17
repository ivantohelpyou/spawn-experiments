# Routinized Experiment Process

## Overview

This document establishes the standard operating procedure for conducting unbiased TDD methodology experiments. The process is designed to eliminate human bias through automation and strict protocols.

## Process Flow

### Phase 1: Experiment Setup (Automated)

#### Standard Setup Command
```bash
# Create new experiment
python setup_experiment.py "experiment-name" \
  --app-type "Application Description" \
  --tech-stack "Technology"

# Example:
python setup_experiment.py "lru-cache-ttl" \
  --app-type "LRU Cache with TTL (Time-To-Live)" \
  --tech-stack "Python"
```

#### Validation Command
```bash
# Validate setup before execution
python validate_experiment.py experiments/NNN-experiment-name/

# Example:
python validate_experiment.py experiments/008-lru-cache-ttl/
```

### Phase 2: Method Assignment (Randomized)

#### Random Assignment Script
```bash
#!/bin/bash
# assign_methods.sh - Random method assignment to prevent bias

METHODS=(
    "1-immediate-implementation"
    "2-specification-driven"
    "3-test-first-development"
    "4-validated-test-development"
)

# Shuffle methods randomly
SHUFFLED=($(shuf -e "${METHODS[@]}"))

echo "Random Method Assignments:"
echo "Agent A: ${SHUFFLED[0]}"
echo "Agent B: ${SHUFFLED[1]}"
echo "Agent C: ${SHUFFLED[2]}"
echo "Agent D: ${SHUFFLED[3]}"

# Log assignments
echo "$(date): Random assignments - A:${SHUFFLED[0]} B:${SHUFFLED[1]} C:${SHUFFLED[2]} D:${SHUFFLED[3]}" >> assignment_log.txt
```

### Phase 3: Agent Execution (Parallel)

#### Execution Template
```bash
# For each assigned method, execute in parallel:

cd experiments/NNN-experiment-name/METHOD-NAME/

# Record start time
echo "$(date): Method execution started" >> TIMING_LOG.txt

# Execute prompt (copy from PROMPT.md exactly)
# [Agent follows PROMPT.md instructions precisely]

# Record completion time
echo "$(date): Method execution completed" >> TIMING_LOG.txt
```

#### Monitoring Checklist
- [ ] No additional guidance provided beyond PROMPT.md
- [ ] No hints about expected outcomes
- [ ] Timing data captured automatically
- [ ] Git commits follow specified patterns
- [ ] No cross-contamination between methods

### Phase 4: Data Collection (Automated)

#### Timing Analysis
```bash
# Extract timing data from all methods
python analyze_timing.py experiments/NNN-experiment-name/
```

#### Code Quality Metrics
```bash
# Generate quality metrics for each method
python analyze_quality.py experiments/NNN-experiment-name/
```

#### Test Coverage Analysis
```bash
# Analyze test coverage where applicable
python analyze_coverage.py experiments/NNN-experiment-name/
```

### Phase 5: Results Analysis (Objective)

#### Quantitative Analysis
- Development time (minutes)
- Lines of code produced
- Cyclomatic complexity
- Test coverage percentage (where applicable)
- Number of commits
- Bug count in initial implementation

#### Qualitative Analysis
- Code readability score (automated)
- Documentation completeness
- Error handling robustness
- Maintainability indicators

#### Statistical Analysis
- Variance across runs
- Confidence intervals
- Significance testing
- Effect size calculations

## Bias Prevention Mechanisms

### 1. Automated Setup
- Eliminates manual configuration errors
- Ensures identical starting conditions
- Removes subjective decisions from setup

### 2. Neutral Language Enforcement
- Automated bias detection in all text
- Standardized terminology
- No quality expectations embedded in names

### 3. Random Assignment
- Prevents cherry-picking favorable methods
- Eliminates assignment bias
- Ensures fair comparison

### 4. Blind Execution
- Agents receive only PROMPT.md instructions
- No context about other methods
- No hints about expected performance

### 5. Objective Measurement
- Automated metric collection
- Standardized evaluation criteria
- Quantitative wherever possible

## Quality Assurance Checkpoints

### Pre-Execution Validation
```bash
# Run before any agent execution
python validate_experiment.py experiments/NNN-experiment-name/
```

Must pass:
- [ ] Directory structure correct
- [ ] Neutral naming verified
- [ ] No bias detected in content
- [ ] Prompts match specifications
- [ ] Metadata complete

### Mid-Execution Monitoring
- [ ] No additional guidance provided
- [ ] Timing logs being written
- [ ] Git commits happening regularly
- [ ] No cross-method contamination

### Post-Execution Analysis
```bash
# Verify data integrity
python verify_results.py experiments/NNN-experiment-name/
```

Must verify:
- [ ] All methods completed
- [ ] Timing data consistent
- [ ] Code quality metrics generated
- [ ] No execution anomalies detected

## Emergency Protocols

### Bias Detection Mid-Experiment
1. **STOP** all affected executions immediately
2. Document the bias source and impact
3. Reset affected methods with corrected setup
4. Note correction in experiment metadata
5. Resume with proper protocols

### Technical Failures
1. Document failure point and cause
2. Preserve existing data
3. Restart from last valid checkpoint
4. Note technical issues in experiment report

### Contamination Between Methods
1. Identify contamination source
2. Assess impact on results validity
3. Consider partial or full experiment restart
4. Document contamination in limitations

## Repeatability Standards

### Experiment Documentation
Each experiment must include:
- Complete setup configuration
- Random assignment log
- Timing data for all phases
- Quality metrics for all methods
- Any deviations from standard protocol

### Version Control
- All scripts versioned
- Setup changes tracked
- Protocol modifications documented
- Rationale for changes recorded

### Replication Package
For each experiment, create:
```
experiments/NNN-experiment-name/
├── REPLICATION_PACKAGE.md
├── setup_config.json
├── assignment_log.txt
├── timing_data.csv
├── quality_metrics.csv
└── analysis_scripts/
```

## Continuous Improvement

### Protocol Updates
1. Identify bias sources or process weaknesses
2. Propose protocol improvements
3. Test improvements on pilot experiments
4. Update standards and scripts
5. Document changes and rationale

### Metric Refinement
- Regular review of measurement validity
- Addition of new objective metrics
- Removal of biased or unreliable measures
- Calibration of quality assessments

### Process Optimization
- Reduce manual steps where possible
- Improve automation reliability
- Enhance bias detection capabilities
- Streamline execution workflows

## Success Criteria

An experiment run is considered successful when:

### Process Integrity
- [ ] Setup validation passed completely
- [ ] No bias detected throughout execution
- [ ] Random assignment properly logged
- [ ] No contamination between methods
- [ ] All timing data captured correctly

### Data Quality
- [ ] All methods completed successfully
- [ ] Quality metrics generated for each method
- [ ] Statistical analysis possible
- [ ] Results internally consistent
- [ ] No technical artifacts affecting results

### Objective Analysis
- [ ] Results reported without interpretation bias
- [ ] Unexpected outcomes highlighted
- [ ] Limitations clearly documented
- [ ] Statistical significance properly assessed
- [ ] Practical significance considered

**Remember: The goal is objective comparison to advance understanding, not to confirm preconceptions about methodology effectiveness.**