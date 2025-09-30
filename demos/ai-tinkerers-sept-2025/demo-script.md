# AI Tinkerers Demo Script - September 30, 2025

**Talk:** "Building Working Code Live: Documentation-First AI Development"

**Duration:** 15-20 minutes

---

## Setup Before Demo

- [ ] Terminal ready in `experiments/1.608-story-to-haiku/`
- [ ] YouTube video queued up
- [ ] Fresh directory for git clone
- [ ] VS Code closed (will open fresh during demo)
- [ ] Ollama running (`ollama serve`)
- [ ] Convention City window ready (keep offscreen)

---

## Part 1: Show the Completed Tool (2-3 min)

**Terminal:** `cd experiments/1.608-story-to-haiku`

### Demo the CLI tool:
```bash
tools/generate-haiku "In a small village, an old woman tended her garden every day. One morning, she found a mysterious seed that glowed faintly in the dawn light." --run 4 --top 3
```

### Talking Points:
- "This is a story-to-haiku converter I built using 4 different AI development methodologies"
- "It ranks the implementations by code quality and generates haiku from the top 3"
- **[Wait for output]** "Gold, Silver, Bronze - all from the same story, different methodologies"
- "How different can the same task be? Let's find out..."

---

## Part 2: Play Video + Explain (2-3 min)

**YouTube:** Play 1-2 minute time-lapse

### While video plays:
**First 30 seconds:**
- "This is the actual build - sped up 12x from 48 minutes to under 2 minutes"
- "I ran 4 methodologies in parallel: Immediate Implementation, Specification-Driven, Pure TDD, Adaptive TDD"
- "Same AI model, same task, same me - only difference is HOW I prompted"

**Next 30-60 seconds:**
- "Each method gets isolated branch, clean environment - no cross-contamination"
- "Watch the code quality differences emerge in real-time"
- "Specification-Driven writes more code but gets highest quality score"
- "Olympic judging system: 3 LLM judges score each output"

**Final 30 seconds / After video:**
- "Result: Methodology matters more than model choice"
- "Key finding: Optimized prompts improve BOTH speed (22-36%) AND quality (+1 to +7 points)"

---

## Part 3: Live Build - Limerick Generator (3-4 min)

### Clone the repo:
```bash
# Terminal in fresh directory
git clone https://github.com/ivantohelpyou/spawn-experiments.git
cd spawn-experiments
```

**Talking points:**
- "It's all open source - you can replicate any experiment"
- "Let's build a limerick generator from scratch right now"

### Start the build:
```bash
claude "Run Experiment 1.608.B - Limerick Converter on PRIVATE branch.

TASK: Build a story-to-limerick converter that converts prose into limericks (AABBA rhyme scheme, specific meter). Use llama3.2 via Ollama. Include Olympic judging system (3 LLM judges score each output).

Use META_PROMPT_GENERATOR_V4.md with these methods:
1. Immediate Implementation
2. Specification-Driven
3. Pure TDD
4. Adaptive/Validated TDD

Use optimized prompts (lessons from 1.608 Run 4).

DELIVERABLES:
- 4 complete implementations with tests
- Olympic judging system (3 judges, scoring criteria)
- Working CLI tool: tools/generate-limerick \"Your story\" --run 1 --top 3
- Code quality report
- EXPERIMENT_1608B_COMPLETE_SUMMARY.md

EXECUTE COMPLETELY: Run all 4 methods in parallel, build CLI tool, test with sample story, generate final report. Commit to private-main when complete.

DO NOT STOP for confirmations. Execute the entire experiment end-to-end."
```

**Talking points:**
- "Single command. No manual intervention."
- "It reads META_PROMPT_GENERATOR_V4.md - my methodology framework"
- "Spawns 4 parallel implementations"
- "Builds working CLI tool"
- "Runs test suite"
- "Generates quality report"
- **[It starts running]** "This will take about 15 minutes, so let's look at the code structure while it cooks..."

---

## Part 4: VS Code Walkthrough (5-6 min)

**Open VS Code:** `code experiments/1.608-story-to-haiku`

### Folder Structure Tour:

#### Show: Root level
```
experiments/1.608-story-to-haiku/
├── 1-initial-run/
├── 2-structured-output/
├── 3-clean-room/
├── 4-optimized-prompts/          ← Open this
├── tools/                         ← Working CLI tool
└── EXPERIMENT_1608_COMPLETE_SUMMARY.md
```

**Talking points:**
- "4 runs = 4 different research questions"
- "Each run has 4 methodology implementations"
- "Run 4 tested prompt engineering hypothesis"

#### Show: `4-optimized-prompts/` folder
```
4-optimized-prompts/
├── 1-immediate-implementation/
├── 2-specification-driven/        ← Open this
├── 3-test-first-development/
└── 4-adaptive-tdd/
```

**Talking points:**
- "Clean isolation - no cross-contamination"
- "Each has own environment, own tests"

#### Show: `2-specification-driven/` implementation
**Open files:**
- `SPECIFICATION.md` - "Executable specification, written first"
- `haiku_converter.py` - "Clean implementation following spec"
- `test_haiku_converter.py` - "Comprehensive test suite"
- `IMPLEMENTATION_SUMMARY.md` - "Timestamped development log"

**Talking points:**
- "Specification-Driven: Write spec first, then code"
- "96/100 quality score - highest in the run"
- "More upfront planning = better long-term quality"

#### Show: `1-immediate-implementation/` (contrast)
**Open files:**
- `haiku_converter.py` - "Simpler, more direct"
- `test_haiku_converter.py` - "Basic tests"

**Talking points:**
- "Immediate Implementation: Just build it"
- "78/100 quality score"
- "23% less code but 18 points lower quality"
- "Fast for prototypes, not for production"

#### Show: `tools/generate-haiku`
**Open file:**
- Line 1: Shebang pointing to venv
- Lines 26-38: Default rankings from quality analysis
- Lines 63-120: Ranked generation logic

**Talking points:**
- "Post-experiment: I consolidated the best implementations into a working CLI tool"
- "Runs top 3 methods in quality order"
- "Production-ready code from experimental artifacts"

#### Show: `EXPERIMENT_1608_COMPLETE_SUMMARY.md`
**Scroll to findings:**
- Finding 09: Prompt engineering results
- Methodology transparency section

**Talking points:**
- "22-36% speed improvement from optimized prompts"
- "+1 to +7 code quality points"
- "Research integrity: I document when experimental design changes"
- "Transparency > cherry-picking results"

### Key Metrics to Highlight:
```
Method 2 (Spec-Driven):    96/100 quality, ~220 LOC
Method 4 (Adaptive TDD):   93/100 quality, ~195 LOC
Method 3 (Pure TDD):       85/100 quality, ~185 LOC
Method 1 (Immediate):      78/100 quality, ~155 LOC
```

**Talking points:**
- "Code quality correlates with methodology complexity"
- "But simpler isn't always worse - depends on context"
- "Previous experiments showed Method 2 creating 32X bloat"
- "Context determines optimal methodology"

---

## Part 5: Check Limerick Progress (1-2 min)

**Switch to terminal** where limerick generation is running

**Possible states:**

### If still running:
- "Still going - building 4 complete implementations in parallel"
- "When it finishes: working CLI tool, test suites, quality report"
- "All committed to git automatically"

### If finished:
```bash
cd experiments/1.608.B-limerick-converter
tools/generate-limerick "There once was a coder named Claude..." --top 3
```
- **[Demo the output]** "15 minutes, 4 methodologies, working production code"

---

## Part 6: The Reveal (EXCLUDED FROM WRITTEN SCRIPT)

**[Switch to Convention City window]**
**[Show whatever you want to show]**
**[This part is yours]**

---

## Closing (30 sec)

**Talking points:**
- "Key takeaway: HOW you prompt matters more than WHICH model"
- "Documentation-first approach: Write spec, generate code, validate automatically"
- "Open source: github.com/ivantohelpyou/spawn-experiments"
- "Try it yourself - single command to replicate any experiment"

**Final line:**
- "Questions?"

---

## Backup Content (If Extra Time)

### Research Findings Portfolio:
- **32X Over-Engineering:** Same AI, different method = 6,036 lines vs 187 lines
- **Context Flips Performance:** Method 2 worst (32X bloat) → best (78% reduction) in clean room
- **Component Discovery:** 0% without hints → 100% with "utils/ contains components"

### Technical Details:
- Uses local Ollama (llama3.2) - no API costs
- Git-based isolation ensures no cross-contamination
- Olympic judging: 3 LLM judges with scoring rubric
- Post-experiment cleanup script removes artifacts

---

## Emergency Pivots

### If Claude won't start:
- "I have pre-built experiments we can examine instead"
- Go straight to VS Code walkthrough
- Show completed experiments in detail

### If Ollama isn't running:
- "The build needs a running LLM - but I have completed results"
- Demo the haiku tool with cached results
- Explain architecture from code

### If audience wants deep dive:
- Show META_PROMPT_GENERATOR_V4.md
- Explain methodology framework in detail
- Walk through git history of one implementation

---

## Questions You Might Get

**Q: Why not just use the best methodology every time?**
A: Context matters. Method 2 created 32X bloat in one experiment but was optimal in another. You need to test for your specific domain.

**Q: How do you prevent contamination between methods?**
A: Git branches + isolated venvs + parallel execution. Each method starts from clean committed state, never sees other implementations.

**Q: Can this work with other models?**
A: Yes! Framework is model-agnostic. I use llama3.2 locally for reproducibility and zero API costs.

**Q: What's the practical application?**
A: (1) Methodology guidance for AI coding tools, (2) Prompt optimization validation, (3) Monte Carlo sampling for creative outputs (20% quality boost).

**Q: How long did this research take?**
A: 20+ experiments over ~6 months. Each experiment takes 15-60 minutes to run, then analysis/writeup.

**Q: Are you publishing this academically?**
A: Open science approach - everything's on GitHub with full methodology transparency. Academic publication might come later.

---

## Post-Demo

- [ ] Share link: github.com/ivantohelpyou/spawn-experiments
- [ ] Share YouTube video link
- [ ] Answer questions
- [ ] Network!
