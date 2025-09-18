# Claude Code Usage Management Protocol

## Problem Statement

Claude Code Pro has **5-hour usage windows** that reset periodically. TDD methodology experiments can consume significant usage, with parallel execution of 4 methodologies being particularly intensive. Failed experiments due to usage limits compromise research validity and waste valuable experimental time.

**Critical Issue**: Experiment 009 (multilingual word counter) nearly exhausted a fresh 5-hour window with parallel execution, indicating that complex experiments may not fit within usage constraints.

## Usage Management Strategy

### **Pre-Experiment Usage Assessment**

#### **Check Available Usage**
Before launching any experiment:
```markdown
"Before we begin, please check your current Claude Code usage status.

TO CHECK USAGE:
- Look for usage indicator in Claude Code interface (if available)
- Check settings/account page for usage information
- Note any recent usage-intensive activities in this session

Please confirm:
- How much time remains in your current 5-hour window?
- When does your next usage window reset?

This experiment will involve parallel execution of 4 methodologies, which is usage-intensive."
```

**Note**: If you're unsure how to check usage, start conservatively and monitor for usage warnings during execution.

#### **Usage Estimation Guidelines**
Based on experiment 009 data:
- **Tier 1 (Functions)**: ~30-60 minutes total (4 parallel * 5-15 min each)
- **Tier 2 (Tools)**: ~60-120 minutes total (4 parallel * 15-30 min each)
- **Tier 3 (Applications)**: ~180-360 minutes total (4 parallel * 45-90 min each)

**Conservative Planning**: Assume upper bounds for usage estimation.

### **Execution Strategy Decision Tree**

#### **✅ Abundant Usage (>3 hours remaining)**
- **Proceed with parallel execution** as designed
- **Session logging active** for all 4 methodologies
- **Full experiment completion** expected

#### **⚠️ Moderate Usage (1-3 hours remaining)**
- **Warn user about potential incompletion**
- **Offer serial execution alternative**
- **Suggest simpler Tier 1 problems** if Tier 2-3 planned

#### **❌ Limited Usage (<1 hour remaining)**
- **Do not start complex experiments**
- **Suggest waiting for usage reset**
- **Offer single methodology trial** if user insists

### **Serial Execution Fallback Protocol**

#### **When to Recommend Serial**
- **Limited usage windows** (<2 hours for Tier 2, <4 hours for Tier 3)
- **User preference** for guaranteed completion
- **Previous parallel failure** in current usage window

#### **Serial Execution Process**
```markdown
"Due to usage constraints, I recommend serial execution:

1. Method 1 (immediate-implementation) - Complete with session logging
2. Method 2 (specification-driven) - Complete with session logging
3. Method 3 (test-first-development) - Complete with session logging
4. Method 4 (validated-test-development) - Complete with session logging

Each method will be completed fully before starting the next.
This ensures partial results if usage limits are reached."
```

#### **Serial Benefits vs. Costs**
**Benefits**:
- **Guaranteed partial completion** if usage runs out
- **Incremental progress** visible throughout
- **Lower peak resource usage**

**Costs**:
- **Loss of parallel timing comparison** (methodologies don't start simultaneously)
- **Potential methodology contamination** (later methods may see earlier results)
- **Extended wall-clock time** for completion

## Mid-Experiment Failure Protocols

### **Failure Detection and Response**

#### **Automated Failure Detection**
Monitor for these signals:
- **Task timeout** without completion
- **Usage limit warnings** from Claude Code
- **Agent non-responsiveness** for extended periods
- **Incomplete session logs** (premature termination)

#### **Immediate Response Protocol**
```markdown
1. **STOP all remaining parallel tasks immediately**
2. **Document failure point and cause** in experiment metadata
3. **Preserve completed work** from successful methodologies
4. **Assess continuation options** based on remaining usage
```

### **Partial Experiment Handling**

#### **Completion Assessment**
Determine experiment validity based on completed methodologies:
- **4/4 complete**: Full experiment success
- **3/4 complete**: Strong results, note limitation in report
- **2/4 complete**: Partial results, compare completed methodologies only
- **1/4 complete**: Insufficient for methodology comparison
- **0/4 complete**: Complete failure, retry with different approach

#### **Partial Result Documentation**
```markdown
## ⚠️ PARTIAL EXPERIMENT - USAGE LIMITATION

**Completion Status**: 2/4 methodologies completed
**Failure Point**: Claude Code usage limit reached during Method 3 execution
**Completed Methods**:
- ✅ 1-immediate-implementation (completed in 12 minutes)
- ✅ 2-specification-driven (completed in 18 minutes)
- ❌ 3-test-first-development (failed at 45% completion)
- ❌ 4-validated-test-development (not started)

**Analysis**: Limited to comparison of immediate vs. specification-driven approaches.
**Recommendation**: Retry with serial execution or wait for usage reset.
```

## Usage Recovery and Continuation

### **5-Hour Reset Handling**

#### **Mid-Experiment Reset**
If usage resets during experiment execution:
- **Continue with remaining methodologies** using fresh usage allowance
- **Document timing discontinuity** in session logs
- **Note reset impact** in final experiment report
- **Maintain experimental isolation** (don't let agents see completed work)

#### **Post-Failure Restart Protocol**
```markdown
"Your Claude Code usage has reset. We can now continue the failed experiment:

CONTINUATION OPTIONS:
1. **Complete remaining methodologies** (3-test-first-development, 4-validated-test-development)
2. **Restart entire experiment** with fresh parallel execution
3. **Switch to serial execution** for guaranteed completion

Previous session data preserved for analysis."
```

### **Cross-Session Experiment Management**

#### **State Preservation**
Between usage windows, preserve:
- **Session logs** from completed methodologies
- **Experiment metadata** and timing information
- **Component curation** decisions and setup
- **Partial results** and intermediate outputs

#### **Continuation Setup**
When resuming after usage reset:
```bash
# Restore experiment state
cd experiments/NNN-experiment-name/
ls */DEVELOPMENT_SESSION.log    # Check completed trials
cat EXPERIMENT_STATUS.md        # Review completion state

# Continue with remaining methodologies
# Ensure identical component environment setup
```

## Usage Optimization Strategies

### **Efficiency Improvements**

#### **Prompt Optimization**
- **Concise problem statements** to reduce token overhead
- **Focused methodology descriptions** without unnecessary detail
- **Efficient session logging** (capture essentials, not everything)

#### **Parallel Execution Optimization**
- **Stagger launches** slightly to avoid peak resource contention
- **Monitor progress** and abort clearly failing methodologies early
- **Use timeouts** to prevent runaway experiments

#### **Component Preparation**
- **Pre-curate components** before starting usage-intensive work
- **Prepare experiment directories** during low-usage periods
- **Validate setup** before launching parallel methodologies

### **Strategic Experiment Selection**

#### **Usage Window Planning**
- **Tier 1 experiments**: Safe for any usage window
- **Tier 2 experiments**: Require >2 hours for parallel execution
- **Tier 3 experiments**: Require >4 hours for parallel execution

#### **Problem Complexity Assessment**
Before selecting experiment:
- **Simple problems** (basic algorithms): Lower usage consumption
- **Complex problems** (full applications): Higher usage consumption
- **Domain familiarity**: Known domains may be more efficient

## User Communication Protocol

### **Usage Warning Template**
```markdown
⚠️ **CLAUDE CODE USAGE WARNING**

This experiment involves parallel execution of 4 methodologies.
**Estimated usage**: [X] hours
**Your current window**: [Y] hours remaining

**Recommendations**:
- ✅ **Proceed with parallel**: If Y > X + 1 hour buffer
- ⚠️ **Consider serial**: If Y < X but Y > X/2
- ❌ **Wait for reset**: If Y < X/2

**Fallback plan**: Serial execution if parallel fails mid-experiment.
```

### **Progress Communication**
During execution, provide usage-aware updates:
```markdown
"Methodology Status Update:
- ✅ Method 1: Complete (15 min)
- 🔄 Method 2: In progress (8 min elapsed)
- ⏳ Method 3: Queued
- ⏳ Method 4: Queued

Estimated remaining: 45 minutes
Usage status: Healthy"
```

## Research Impact Considerations

### **Bias from Usage Constraints**

#### **Potential Biases Introduced**
- **Serial execution** may affect methodology timing comparisons
- **Partial experiments** may favor faster methodologies
- **Usage pressure** may influence methodology selection

#### **Bias Mitigation**
- **Document execution mode** (parallel vs. serial) in all reports
- **Separate analysis** for partial vs. complete experiments
- **Usage impact assessment** in research conclusions
- **Transparent limitation reporting** in methodology comparisons

### **Research Validity**

#### **Valid Research Scenarios**
- **Complete parallel experiments**: Highest validity
- **Complete serial experiments**: Valid with execution mode noted
- **Partial experiments**: Limited validity, useful for methodology subset analysis

#### **Invalid Research Scenarios**
- **Mixed execution modes** within single experiment
- **Incomplete experiments** without proper documentation
- **Usage-influenced methodology modifications**

## Conclusion

Claude Code usage management is **critical for experimental validity**. The protocol ensures:
- **Realistic usage planning** before experiment launch
- **Graceful degradation** when usage constraints hit
- **Preservation of research validity** through proper documentation
- **Strategic experiment selection** based on available resources

**Key Principle**: Better to complete fewer experiments well than to have many incomplete experiments that compromise research conclusions.

**Implementation**: This protocol must be integrated into the spawn-experiments meta prompt to ensure all experiments follow usage-aware planning.