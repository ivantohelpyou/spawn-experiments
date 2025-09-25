# TDD in the AI Era: Spawn-Experiments System v3.0 - Competition & Atomic Commits Edition

**Purpose**: Enhanced prompting system with atomic git commits and competition simulation capabilities for studying real-world development pressures.

**Key Innovation**: Git-based time manipulation allows injection of competitive pressure at any point in development.

**Version 3.0 Changes**:
- Atomic commit requirements for time-travel capability
- Competition notification system
- Realistic development pressure simulation

## 🔬 Core Experimental Enhancement

### **Public/Private Branch Decision Protocol** (Add to ALL prompts - PHASE 0)

```
CRITICAL FIRST STEP: Before starting any experiment, ask user:

"Should this experiment be public (main branch) or private (private-main branch)?"

Based on response:
- Public: Work and commit to main branch - results will be visible publicly
- Private: Work and commit to private-main branch - results remain private

NEVER assume - always ask first!
```

### **Branch Naming Protocol** (Add to ALL prompts)

```
IMPORTANT: Create a dedicated branch for your experiment from the TARGET BRANCH:

# For PUBLIC experiments:
git checkout main
git checkout -b exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]

# For PRIVATE experiments:
git checkout private-main
git checkout -b exp-[EXPERIMENT_NUMBER]-[METHOD_NAME]

Examples:
- git checkout -b exp-1504-immediate
- git checkout -b exp-1504-specification
- git checkout -b exp-1504-tdd
- git checkout -b exp-1504-validated

This enables clean experiment isolation and proper public/private separation.
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
This enables progress tracking and potential rollback if needed.
Frequent commits are a professional development practice.
```

### **Competition Injection Rollback Procedure**

```
EXPERIMENT ROLLBACK FOR COMPETITION INJECTION:

1. Identify injection point:
   git log exp-[EXPERIMENT_NUMBER]-specification --oneline

2. Find specification completion commit:
   Look for commits like "Specs: Technical design complete"

3. Create injection branch:
   git checkout exp-[EXPERIMENT_NUMBER]-specification
   git checkout -b exp-[EXPERIMENT_NUMBER]-specification-injection

4. Reset to injection point:
   git reset --hard [COMMIT_HASH]

5. Create market update:
   echo "COMPETITOR SHIPPED: [Details]" > MARKET_UPDATE.txt
   git add MARKET_UPDATE.txt
   git commit -m "EXTERNAL: Competition notification"

6. Apply injection prompt (see META_PROMPT_COMPETITION_INJECTION.md)

This procedure enables clean before/after comparison of AI methodology adaptation.
```

---

## Enhanced Method Prompts

### **Method 1: Immediate Implementation (Enhanced)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK].

Start coding immediately with minimal planning. Focus on getting something working quickly.

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/1-immediate-implementation/baseline/

This baseline/ folder structure enables clean competition injection experiments later.

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

### **Method 2: Specification-Driven (Enhanced with Competition Awareness)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK].

Start by creating comprehensive specifications before implementation.

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/2-specification-driven/baseline/

This baseline/ folder structure enables competition injection experiments:
- baseline/ = original comprehensive approach
- unconstrained-injection/ = rapid competitive response (speed focus)
- constrained-injection/ = enterprise-ready competitive response (speed + docs)

ATOMIC COMMIT PROTOCOL:
Track your progress with git commits:
- git add -A && git commit -m "Specs: Requirements analysis complete"
- git add -A && git commit -m "Specs: Technical design documented"
- git add -A && git commit -m "Specs: Test plan defined"
- git add -A && git commit -m "Impl: Core structure created"
- git add -A && git commit -m "Impl: [Feature] implemented"
- git add -A && git commit -m "COMPLETE: All requirements met"

Technology: [TECH_STACK]
Show all work including commits.
```

### **Method 3: Test-First Development (Enhanced)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK] using strict TDD.

Follow Red-Green-Refactor with atomic commits:

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/3-test-first-development/baseline/

This baseline/ folder structure maintains consistency with other methods for comparison experiments.

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

### **Method 4: Validated Test Development (Enhanced)**

```
Build a [APPLICATION_TYPE] using [TECH_STACK] using TDD with test validation.

Follow enhanced TDD with atomic commits:

CONSTRAINTS:
- You may not use the web for this project
- Use only standard library and built-in capabilities
- Work from your existing knowledge

DIRECTORY STRUCTURE:
Create your implementation in:
experiments/[EXPERIMENT_NUMBER]/4-validated-test-development/baseline/

This baseline/ folder structure maintains consistency with other methods for comparison experiments.

ATOMIC COMMIT PROTOCOL:
- git add -A && git commit -m "Test: [feature] test written"
- git add -A && git commit -m "Validate: Wrong impl fails test"
- git add -A && git commit -m "Impl: Correct implementation"
- git add -A && git commit -m "Verify: Test validation complete"
- git add -A && git commit -m "COMPLETE: Validated and working"

Each validation cycle should have distinct commits.

Technology: [TECH_STACK]
Show all work including commits.
```

---

## 🚀 Competition Injection Protocol

### **Step 1: Monitor Progress**
```bash
# Watch all branches for first COMPLETE commit
watch -n 10 'git log --all --oneline | grep COMPLETE'
```

### **Step 2: Identify Interruption Point**
When first method completes, note timestamp:
```bash
COMPLETION_TIME=$(git log --all --grep="COMPLETE" --format="%at" | head -1)
```

### **Step 3: Inject Competition**
For methods still in progress:
```bash
# For each incomplete method branch
git checkout method-X-branch
echo "Competitor completed at $(date)" > COMPETITOR_FINISHED.txt
git add COMPETITOR_FINISHED.txt
git commit -m "NOTIFICATION: Competitor completed"
```

### **Step 4: Modified Continuation Prompt**
```
Continue your implementation.

IMPORTANT: A competitor has completed a working solution!
- Prioritize shipping working code immediately
- Skip non-essential features
- Focus on core functionality only
- Complete within next 5 minutes if possible
```

---

## 🧪 Experimental Variations

### **Competition Context Variants**

#### **Variant A: Startup Race** (Speed wins)
```
"You're in a startup competing with 3 other startups for the same market.
The move-fast competitor just shipped. Ship now or lose market share."
```

#### **Variant B: Contracting Bid** (First working solution wins)
```
"You're one of 4 contractors. Client will accept first working solution.
Another contractor just delivered. You have 5 minutes to submit or lose the contract."
```

#### **Variant C: Internal Hackathon** (Innovation speed)
```
"Company hackathon with 4 teams. First working demo wins.
Team 1 (cowboy coders) just presented. Present something NOW."
```

#### **Variant D: Open Source Race** (First PR gets merged)
```
"4 developers working on same GitHub issue. First clean PR gets merged.
A fast contributor just submitted PR. Submit yours immediately or it's wasted work."
```

### **Competition Timing Variants**

#### **Early Competition** (25% through)
"Competitor finished in 2 minutes! They must have skipped everything non-essential."

#### **Mid Competition** (50% through)
"Competitor just finished with basic solution. You're halfway through specs."

#### **Late Competition** (75% through)
"Competitor beat you by a few minutes. Rush to be second place at least."

#### **No Competition** (Control)
Standard execution without competitive pressure

---

## 📊 Metrics to Track

### **From Git History**
```bash
# Time to completion
git log --format="%at %s" | grep COMPLETE

# Number of commits (development granularity)
git rev-list --count HEAD

# Lines changed per commit (development pace)
git log --stat --oneline

# Time between commits (development rhythm)
git log --format="%at" | awk 'NR>1{print $1-prev} {prev=$1}'
```

### **Competition Response Metrics**
- Code volume before/after notification
- Feature scope change after notification
- Time from notification to completion
- Commit message sentiment change

---

## 🎯 Research Questions

1. **Does competition notification reduce over-engineering?**
   - Hypothesis: >50% reduction in code volume

2. **When is competition pressure most effective?**
   - Early vs. late notification impact

3. **Do different methods respond differently to competition?**
   - TDD vs. Specification response patterns

4. **Does commit frequency correlate with code quality?**
   - Atomic commits as development rhythm indicator

---

## 💡 Future Enhancements

### **Auto-Competition System**
```python
# Automated competition injection
import subprocess
import time

def monitor_and_inject():
    while True:
        if check_for_completion():
            inject_competition_notification()
            break
        time.sleep(30)
```

### **Stress Levels**
- Level 1: "A colleague is also working on this"
- Level 2: "Competitor making good progress"
- Level 3: "Competitor just finished!"
- Level 4: "Multiple competitors already delivered"

### **Market Simulation**
- "Customer wants solution TODAY"
- "Competitor's solution is already in production"
- "You have 10 minutes before the demo"

---

## 📝 Implementation Notes

### **For Next Experiment (1.503 File Path Validator)**

1. Use enhanced prompts with atomic commits
2. Run standard 4-method comparison
3. Monitor git history in real-time
4. Test competition injection on Method 2
5. Compare Method 2 vs Method 2-interrupted

### **Success Indicators**
- Atomic commits working (≥3 commits per method)
- Competition notification acknowledged in commits
- Measurable behavior change after notification
- Reduced over-engineering in Method 2-interrupted

---

## 🔮 Long-term Vision

This enhancement enables:
- **Reproducible pressure studies** via git time-travel
- **A/B testing** of same method with/without competition
- **Psychological research** on AI response to pressure
- **Real-world simulation** of development constraints

The key insight: **Git commits aren't just version control - they're experimental control points for methodology research.**

---

*Version 3.0 builds on 2.0's bias-neutral terminology while adding realistic development pressures through competition simulation and atomic commit protocols.*