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

## Part 1: The Hook (30 seconds)

**Opening line:**
> "Quick question: If I give Claude the same task twice, how different can the results be?"
>
> **[Pause for effect]**
>
> "Answer: **32 times different.** Same model, same task, just different prompting methodology."
>
> "6,036 lines of code versus 187 lines - for a URL validator."
>
> "Today I'm going to show you why **HOW you prompt matters more than WHICH model you use.**"

---

## Part 2: Show the Completed Tool (2 min)

**Terminal:** `cd experiments/1.608-story-to-haiku`

### Demo the CLI tool:
```bash
tools/generate-haiku "In a small village, an old woman tended her garden every day. One morning, she found a mysterious seed that glowed faintly in the dawn light." --run 4 --top 3
```

### Talking Points:
- "Story-to-haiku converter built with 4 different methodologies"
- "All use the same LLM (llama3.2) for generation"
- **[Wait for output]** "Similar outputs - but radically different CODE underneath"
- "Let me show you how different..."

---

## Part 3: Play Video + The Paradox (2-3 min)

**YouTube:** Play 1-2 minute time-lapse

### While video plays:
**First 30 seconds:**
> "This is 4 methodologies running in parallel on the same task - haiku generation.
>
> Watch what happens when I change ONLY the methodology:
> - Method 1 (Immediate): 'Just build it' → 334 lines, 2 minutes
> - Method 2 (Spec-first): 'Plan then build' → 961 lines, 8 minutes
> - Method 3 (TDD): 'Tests first' → 600 lines, 4 minutes
> - Method 4 (Adaptive): 'Strategic testing' → 706 lines, 9 minutes
>
> Same AI. Same me. **Different code volume, different structure, different approaches.**"

**Next 60 seconds:**
> "Now here's where it gets interesting. LLM projects? Method 2 wins every time.
>
> But simple validation tasks? Method 2 creates **enterprise frameworks nobody asked for**.
>
> That URL validator? Method 2 spontaneously created:
> - Rate limiting system
> - Security scanning framework
> - CLI with JSON/CSV/XML output
> - 25 files across 6 packages
>
> **Nobody asked for ANY of this.** The prompt said 'validate URL format.'
>
> Result: 16 minutes and 6,036 lines of over-engineering.
>
> Method 1 did it in 53 seconds with 398 lines. Both work perfectly.
>
> **The finding: Context determines optimal methodology. There's no universal 'best'.**"

---

## Part 4: Live Build - Limerick Generator (3-4 min)

**Talking points:**
- "It's all open source - you can replicate any experiment"
- "Let's build a limerick generator from scratch right now"
- "I have a demo launcher that handles the entire build"

### Start the build:
```bash
# One command - complete experiment
demos/ai-tinkerers-sept-2025/spawn-demo limerick
```

**What this does:**
- Reads the experiment prompt from `1.608-poetry-series.md`
- Executes the full methodology framework
- Runs 4 methods in parallel (Immediate, Spec-Driven, TDD, Adaptive)
- Builds working CLI tool
- Generates test suites
- Creates quality report
- Auto-commits to git

**Talking points:**
- "Single command. No manual intervention."
- "It reads META_PROMPT_GENERATOR_V4.md - my methodology framework"
- "Spawns 4 parallel implementations"
- **[It starts running]** "This will take about 15 minutes"
- "While it builds, let's look at how the haiku code is structured..."

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

**Final message:**
> "Here's the thing: I didn't run these experiments across different models.
>
> I don't chase model releases. I chase **methodology improvements**.
>
> Because you can't control when Anthropic ships the next version.
>
> But you CAN control how you prompt. Today.
>
> And it turns out? That's where the 32X gains are hiding."

**Three takeaways:**
1. **Methodology beats model** - 32X difference from prompting strategy alone
2. **Context matters** - Same methodology wins OR loses depending on problem type
3. **Measure everything** - Test multiple approaches in parallel to know what actually works

**Resources:**
- "All code, all data, all methodology: github.com/ivantohelpyou/spawn-experiments"
- "Try it yourself. Test your assumptions. **You might be surprised.**"

**Final line:**
> "Questions?"

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
