# Competition Injection Meta-Prompt System

**Purpose**: Inject competitive pressure into already-running methodologies via git rollback and continuation
**Key Principle**: We're interrupting existing methodologies, not creating competition-aware ones

---

## 📋 Pre-Experiment: Standard Prompts + Atomic Commits

Use standard META_PROMPT_GENERATOR.md (v2) with ONE addition to all methods:

```
DEVELOPMENT PRACTICE:
Commit your progress frequently for version control:
- After completing any meaningful unit of work
- At least every 3 minutes
- Use clear commit messages: "Specs: [what]", "Impl: [what]", "Test: [what]"

Example commits:
- git add -A && git commit -m "Specs: Defined validation requirements"
- git add -A && git commit -m "Impl: Added format checking"
- git add -A && git commit -m "Test: Edge case coverage"
- git add -A && git commit -m "COMPLETE: All requirements met"
```

**Note**: No mention of competition, just professional git practices.

---

## 🎯 Competition Injection Prompts (Post-Interruption)

### **Universal Injection Prompt** (For Any Method)

```
Continue your implementation from the current state.

IMPORTANT UPDATE: You just learned that another developer has completed and
shipped a working solution for this problem. They used a rapid prototyping
approach and delivered in [X] minutes.

The client has accepted their solution. They value speed to market over
comprehensive features.

You have 5 minutes to deliver something or your work provides no value.

Immediate actions:
1. Abandon any non-essential work
2. Focus only on core functionality
3. Ship the simplest working solution
4. Commit with message: "PIVOT: Responding to competition"
```

---

## 🔧 Method-Specific Injection Variants

### **For Method 2 (Specification-Driven)**

```
Continue from your current specifications.

BREAKING: A competitor just shipped while you were writing specs. They took a
"code first, document later" approach and the client accepted their solution.

Your comprehensive specifications are now academic unless you deliver working
code in the next 5 minutes.

Immediate pivot:
- Stop all specification work
- Implement only what you've already specified
- Skip any unspecified features
- git commit -m "PIVOT: Specs abandoned, implementing core only"
```

### **For Method 3 (TDD)**

```
Continue your test-driven development.

UPDATE: A competitor using "cowboy coding" just delivered a working solution
without any tests. The client accepted it immediately.

While your tests are valuable for long-term quality, you need working code
NOW or you lose this opportunity.

Adjustment:
- Implement just enough to pass current tests
- Skip writing any new tests
- Focus on shipping working code
- git commit -m "PIVOT: Shipping current test coverage only"
```

### **For Method 4 (Validated TDD)**

```
Continue your validated test development.

ALERT: A move-fast competitor shipped a basic solution while you were
validating test quality. The client has already accepted their work.

Your test validation is admirable but the window is closing. Ship what
you have working in the next 5 minutes.

Response required:
- Stop test validation immediately
- Implement solutions for existing tests only
- Skip any unvalidated functionality
- git commit -m "PIVOT: Validation stopped, shipping current functionality"
```

---

## ⏰ Timing-Based Injection Variants

### **Early Interruption** (25% progress)
```
COMPETITOR UPDATE: Another developer just finished in record time!
They must have skipped everything except bare essentials.
You're only [X] minutes in - radically simplify your approach NOW.
```

### **Mid Interruption** (50% progress)
```
COMPETITOR UPDATE: While you were working on [current task], a competitor
shipped a complete solution. You're halfway through your planned approach.
Salvage what you can and ship immediately.
```

### **Late Interruption** (75% progress)
```
COMPETITOR UPDATE: A faster developer just beat you to market. You're close
to finishing but they've already won the primary contract.
Complete only what's working and ship for potential second place.
```

---

## 📊 Injection Protocol

### **Step 1: Monitor Baseline Execution**
```bash
# Watch all method branches
watch -n 30 'git log --all --oneline --graph --since="10 minutes ago"'

# Note when first method completes
Method_1_complete_time: 2m30s
Method_2_last_commit_before: 2m15s at commit abc123
```

### **Step 2: Prepare Injection**
```bash
# Switch to target method branch
git checkout method-2-specification

# Find commit just before competitor completion
git log --oneline --before="2m30s"

# Reset to that commit
git reset --hard abc123
```

### **Step 3: Inject Competition Signal**
```bash
# Create competition marker
echo "Competitor finished at 2m30s" > COMPETITOR_ALERT.txt
echo "You have 5 minutes to ship" >> COMPETITOR_ALERT.txt
git add COMPETITOR_ALERT.txt
git commit -m "EXTERNAL: Competition notification injected"
```

### **Step 4: Launch Continuation Task**
```
Use the appropriate injection prompt above based on:
- Which method is being interrupted
- When in their process they're being interrupted
- What they were working on at interruption
```

---

## 📈 Response Patterns to Measure

### **Expected Behavioral Changes**

**Before Injection**:
- Methodical progress
- Comprehensive implementation
- Feature completeness focus

**After Injection**:
- Rapid simplification
- Feature abandonment
- Speed prioritization

### **Commit Message Sentiment**

**Pre-injection**:
- "Specs: Added error handling section"
- "Impl: Created validation framework"
- "Test: Coverage for edge cases"

**Post-injection**:
- "PIVOT: Abandoning framework"
- "RUSH: Basic functionality only"
- "SHIP: Minimum viable solution"

---

## 🎮 Experimental Controls

### **Variables to Track**
- Time of injection
- Method being interrupted
- Work in progress at interruption
- Response time to pivot
- Code abandoned vs shipped
- Quality degradation (if any)

### **Control Conditions**
- **Baseline**: No interruption
- **Early**: Interrupt at 25% progress
- **Mid**: Interrupt at 50% progress
- **Late**: Interrupt at 75% progress

---

## 🚨 Important Constraints

### **DO NOT**:
- Mention competition in initial prompts
- Create "competition-aware" methodology variants
- Change core methodology definitions
- Inject before sufficient baseline progress

### **DO**:
- Let methods develop naturally first
- Inject at realistic interruption points
- Measure genuine pivot response
- Preserve methodology integrity

---

## 💡 Research Value

This approach enables us to study:
- **Adaptability**: Can AI methodologies pivot under pressure?
- **Momentum**: How hard is it to change course mid-development?
- **Simplification**: Does competition cure over-engineering?
- **Quality Trade-offs**: What gets sacrificed for speed?

The key innovation: Using git as a time machine to create controlled interruption experiments while preserving methodology comparison integrity.

---

*This injection system is separate from META_PROMPT_GENERATOR.md to maintain clean separation between baseline methodology prompts and experimental interventions.*