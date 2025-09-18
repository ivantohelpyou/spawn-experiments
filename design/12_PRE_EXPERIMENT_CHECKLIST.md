# Pre-Experiment Checklist and Confirmation Protocol

## Problem Statement

Experiment 009 violated bias prevention protocols despite having a meta prompt, due to:
- Gap between meta prompt and actual execution
- No explicit confirmation of bias-neutral setup
- Missing parallel execution confirmation
- No pre-launch validation checkpoint

## Solution: Mandatory Confirmation Protocol

### Meta Prompt Enhancement Requirements

The meta prompt must include these **mandatory confirmation steps**:

#### Usage Assessment and Consolidated Confirmation
```
"I understand the objective is to [restate project].

CLAUDE CODE USAGE CHECK:
Before proceeding, please confirm:
- How much time remains in your current 5-hour Claude Code usage window?
- This experiment requires approximately [X] hours for parallel execution

EXPERIMENTAL SETUP CONFIRMATION:
I will create 4 parallel agents using these EXACT protocols:

✓ Neutral naming: 1-immediate-implementation, 2-specification-driven, 3-test-first-development, 4-validated-test-development
✓ No bias language: No quality indicators (naive/advanced/optimal) or expectation statements
✓ Parallel execution: All 4 methodologies launched simultaneously (if sufficient usage)
✓ Serial fallback: Available if usage constraints require it
✓ Equal conditions: Identical starting prompts and timing mechanisms
✓ No explicit component guidance: Agents discover existing codebase components naturally
✓ Session logging: Complete development process capture

Execution plan based on usage:
- [✅/⚠️/❌] Parallel execution recommended/possible/not recommended

Proceed with bias-neutral experiment? (Y/N)"
```

### User Confirmation Requirements

**MANDATORY**: User must explicitly confirm setup before proceeding:
- Cannot proceed without explicit "Y" or "Yes" response
- Any "N" or unclear response triggers protocol review
- Must restart checklist if setup is rejected

### Enforcement Mechanisms

#### Meta Prompt Template Structure
```
1. OBJECTIVE_RESTATEMENT
2. CONSOLIDATED_PROTOCOL_CONFIRMATION
3. USER_EXPLICIT_APPROVAL_REQUIRED
4. BEGIN_EXPERIMENT (only after confirmation)
```

#### Fallback Protections
- If any confirmation step is skipped → STOP and restart checklist
- If biased language detected → STOP and request protocol review
- If parallel execution not configured → STOP and correct setup
- If user approval not explicit → STOP and request clear confirmation

### Protocol Integration Points

#### Meta Prompt Generator Integration
- Embed checklist directly in meta prompt template
- Cannot generate experiment without confirmation protocol
- Template validation ensures all checkpoints included

#### Validation Script Integration
- `validate_experiment.py` runs automatically during checklist
- Real-time bias detection during confirmation phase
- Immediate feedback on protocol compliance

#### Documentation Integration
- Each experiment must record confirmation responses
- Compliance verification in experiment metadata
- Audit trail for protocol adherence

## Implementation Examples

### Compliant Meta Prompt Opening
```
"I understand you want to compare TDD methodologies for [PROJECT].

BIAS PREVENTION CONFIRMATION REQUIRED:
I will use these exact neutral terms:
- 1-immediate-implementation
- 2-specification-driven
- 3-test-first-development
- 4-validated-test-development

No quality judgments (naive/advanced/optimal) will be used.
Confirm bias-neutral setup? (Y/N)"
```

### Non-Compliant Example (Triggers Stop)
```
"I'll compare naive vs sophisticated approaches..."
→ STOP: Bias language detected. Review protocol requirements.
```

## Retrospective Analysis: Experiment 009 Failures

### What Went Wrong
1. **No explicit confirmation step** - Agent proceeded without user validation
2. **Terminology slippage** - "naive" crept in despite meta prompt awareness
3. **No real-time validation** - Bias accumulated without detection
4. **Manual execution** - Parallel launch required user reminder

### Prevention Mechanisms
1. **Mandatory confirmation gates** - Cannot proceed without explicit approval
2. **Real-time bias monitoring** - Detect and stop on first violation
3. **Automated parallel setup** - Default to simultaneous execution
4. **Audit trail** - Record all confirmation responses

## Success Criteria

### Experiment Launch Checklist
- [ ] User confirms project objective understanding
- [ ] User confirms bias-neutral naming convention
- [ ] User confirms parallel execution setup
- [ ] User confirms pre-launch validation passed
- [ ] User provides explicit "GO" approval
- [ ] All confirmations recorded in experiment metadata

### Quality Gates
- **Zero tolerance** for bias language in experimental setup
- **Mandatory parallel execution** for all methodology comparisons
- **Complete audit trail** from checklist through execution
- **Automatic validation** integrated into confirmation flow

## Conclusion

This protocol transforms experiment launch from an assumed-correct process to an explicitly-validated, user-confirmed setup that prevents bias introduction through oversight or automation gaps.

**Key Innovation**: Shifting from "trust the meta prompt" to "confirm each critical decision" ensures human oversight of bias-sensitive setup decisions while maintaining experimental rigor.

**Next Action**: Update meta prompt generator to include mandatory confirmation protocol and integrate validation scripts into the confirmation flow.