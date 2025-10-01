# Spawn-Experiments: AI Development Methodology Research

```
Four methods build code
Same task, different approach—
Which path will you choose?
```

**Systematic research on how methodology choices affect AI-assisted code generation**

---

## 🎯 Latest: Poetry Generator Series (1.608.X)

**NEW:** LLM-powered poetry generators demonstrating methodology impact on creative AI features

### Story-to-Haiku Converter (1.608)
```bash
cd experiments/1.608-story-to-haiku
tools/generate-haiku "Your story here" --run 4
```

### Story-to-Iambic-Pentameter Converter (1.608.A)
```bash
cd experiments/1.608.A-iambic-pentameter
tools/generate-iambic "Your story here" --run 1
```

### Story-to-Limerick Converter (1.608.B)
```bash
cd experiments/1.608.B-limerick-converter
tools/generate-limerick "Your story here" --run 1 --all
```

**[📹 Watch the demo](https://youtu.be/DJv20yyvSqY)** (Haiku & Iambic)

**What we built:**
- Story → Poetry converters (Haiku, Iambic Pentameter, Limericks) using LLMs (llama3.2)
- Olympic judging system (3 diverse LLM judges: llama3.2, phi3:mini, gemma2:2b)
- Working CLI tools with ranked output
- 12 complete implementations (4 methodologies × 3 poetry types)

**Key discoveries from this series:**
1. **[LLM Integration: Specification-Driven Advantage](findings/11-llm-integration-specification-advantage.md)** - Method 2 consistently wins for LLM projects (92/100 avg), outperforming faster methods by 10-18 points
2. **[Prompt Engineering as Force Multiplier](findings/09-prompt-engineering-force-multiplier-1608.md)** - Optimized prompts improved speed by 22-36% AND quality by 1-7 points across ALL methodologies
3. **[Monte Carlo Methodology Sampling](findings/10-monte-carlo-methodology-sampling-1608.md)** - Generate N samples, pick best → 20% quality improvement (applicable production technique)

**[→ Read 1.608 Summary](experiments/1.608-story-to-haiku/EXPERIMENT_1608_COMPLETE_SUMMARY.md)** | **[→ Read 1.608.A Summary](experiments/1.608.A-iambic-pentameter/EXPERIMENT_1608A_COMPLETE_SUMMARY.md)** | **[→ Read 1.608.B Summary](experiments/1.608.B-limerick-converter/EXPERIMENT_1608B_COMPLETE_SUMMARY.md)**

---

## 🔬 What is spawn-experiments?

A research framework testing how different development methodologies affect AI code generation outcomes. We run the same task through 4 different methodologies and measure:
- Development speed
- Code quality
- Lines of code
- Test coverage
- Runtime performance

**The Four Methodologies:**

| Method | Approach | Speed | Best For |
|--------|----------|-------|----------|
| **Method 1** | Immediate Implementation | Fastest (2-3m) | Simple tasks, prototypes, creative outputs |
| **Method 2** | Full Specification First | Slowest (8-16m) | Complex systems, documentation-heavy projects |
| **Method 3** | Test-Driven Development | Moderate (3-5m) | Well-defined algorithms, quality balance |
| **Method 4** | Adaptive TDD | Adaptive (4-6m) | Production code, validated quality |

---

## 📊 Methodology Performance Leaderboard

**Which methodology wins depends on the problem type:**

### LLM Integration Projects (1.6XX series)
| Rank | Method | Avg Score | Speed | Winner |
|------|--------|-----------|-------|--------|
| 🥇 | **Method 2: Specification-Driven** | 92/100 | 7-8 min | Haiku, Iambic |
| 🥈 | Method 4: Adaptive TDD | 88/100 | 8-9 min | - |
| 🥉 | Method 3: Pure TDD | 78.5/100 | 4-5 min | - |
| 4 | Method 1: Immediate | 78/100 | 2-10 min | - |

**Why M2 Wins**: LLM projects need comprehensive error handling (7+ failure modes), clean abstraction layers, and documented prompt templates. Specification phase forces upfront design.

**Use M2 when**: Production LLM integration, complex error scenarios, prompt engineering critical

---

### Simple Input Validation (1.5XX series)
| Rank | Method | Performance | Speed | Winner |
|------|--------|-------------|-------|--------|
| 🥇 | **Method 4: Adaptive TDD** | 1M+ val/sec | 4-6 min | Date validator |
| 🥈 | Method 1: Immediate | 559K val/sec | 3-4 min | - |
| 🥉 | Method 3: Pure TDD | Working | 3-6 min | - |
| ⚠️ | Method 2: Spec-Driven | 32X bloat risk | 7-16 min | Over-engineered |

**Why M4 Wins**: Adaptive TDD matches complexity to problem - simple tasks get simple solutions with strategic validation where needed.

**Why M2 Fails**: Creates enterprise frameworks (rate limiting, security scanning, multi-package architecture) for simple tasks. 32.3X code bloat on URL validator.

**Use M1 when**: Rapid prototyping, throwaway code
**Use M4 when**: Production-quality simple validators

---

### Key Insights
- **No universal winner** - Context determines optimal methodology
- **LLM projects ≠ Algorithmic tasks** - Different complexity profiles
- **Method 2 paradox**: Best for complex projects, worst for simple ones
- **Adaptive TDD (M4)**: Emerging as versatile production choice

---

## 🏆 Major Research Findings

### 1. **LLM Integration: Specification-Driven Methodology Wins** ⭐ NEW
Across LLM integration projects, **Method 2 (Specification-Driven) consistently achieves highest quality** (92/100 avg)
- Outperforms faster methods by 10-18 points
- Superior error handling (19-20/20 vs 10-16/20)
- Better architecture for complex LLM interactions
- **[Full Analysis](findings/11-llm-integration-specification-advantage.md)**

### 2. **Methodology Creates 32X Code Differences**
Same AI model, same task, different methodology = **32.3X code bloat** (URL validator: 6,036 lines vs 187 lines)

**Finding:** HOW you prompt matters more than WHICH model you use
- [32X Over-Engineering Discovery](experiments/1.502-url-validator/EXPERIMENT_REPORT.md)

### 3. **Context Flips Methodology Performance**
Revolutionary finding from multi-run experiments:
- **Baseline:** Method 2 creates 32X bloat (worst)
- **Clean Room:** Same Method 2 achieves 78% reduction (best)
- **Implication:** No universal "best" - context determines winner

### 4. **Component Discovery Requires Guidance**
- **0% discovery rate** without hints (AI never explores utils/ folders)
- **100% discovery rate** with simple prompt: "utils/ contains components you may use"
- [Component Discovery Research](experiments/2.505.1-guided-component-discovery/EXPERIMENT_REPORT.md)

### 5. **Prompt Engineering is Universal Force Multiplier**
From 1.608 research: Optimized prompts improve BOTH speed AND quality across ALL methodologies
- 22-36% faster development time
- +1 to +7 code quality points
- [Full Analysis](findings/09-prompt-engineering-force-multiplier-1608.md)

### 6. **Monte Carlo Sampling for LLM Outputs**
Generate N samples → evaluate → pick best = 20% quality improvement
- Practical production technique
- Works for any high-variance creative task
- [Implementation Guide](findings/10-monte-carlo-methodology-sampling-1608.md)

---

## 📊 Research Portfolio

**Completed Experiments:** 20+
**Validated Findings:** 10
**Domains Covered:**
- Input Validation (7 experiments)
- String Processing (4 experiments)
- LLM Integration (4 runs, 1.608)
- CLI Tools & Component Discovery
- System Architecture

**[→ View All Findings](findings/README.md)**

---

## 🚀 Try It Yourself

### Run the Haiku Generator
```bash
# Clone the repo
git clone https://github.com/ivantohelpyou/spawn-experiments.git
cd spawn-experiments/experiments/1.608-story-to-haiku

# Generate haiku with top-performing methods
tools/generate-haiku "In a small village, an old woman tended her garden..." --run 4

# See verbose output with scores
tools/generate-haiku "Your story here" --run 4 --verbose

# Try all 4 methodologies
tools/generate-haiku "Your story here" --run 4 --all
```

### Replicate the Research

Use our methodology framework to run your own experiments:

1. **[META_PROMPT_GENERATOR_V4.md](META_PROMPT_GENERATOR_V4.md)** - Complete 4-methodology framework
2. **[CLI_TOOL_GENERATOR_V1.md](CLI_TOOL_GENERATOR_V1.md)** - CLI-specific prompting techniques
3. **[EXPERIMENT_STANDARDS.md](EXPERIMENT_STANDARDS.md)** - Research protocols

---

## 🎤 AI Tinkerers Seattle - September 30, 2025

**Talk:** "Building Working Code Live: Documentation-First AI Development"

Live demonstration of spawn-experiments methodology using Claude models:
- Executable specifications
- Parallel code/test generation
- Real-time validation
- Code-like prompting techniques

**[View Demo Materials](experiments/1.608-story-to-haiku/)**

---

## 📈 Evidence & Validation

All experiments follow rigorous protocols:
- ✅ **Parallel execution** - All methods run simultaneously (no cherry-picking)
- ✅ **Isolated environments** - No cross-contamination
- ✅ **Quantitative metrics** - Time, LOC, complexity, performance measured
- ✅ **Multi-run validation** - Context variation studies reveal dependencies
- ✅ **Statistical rigor** - Only validated findings published

**Research Integrity:** We document failures and mark unvalidated hypotheses clearly. See [findings](findings/) for transparent methodology.

---

## 💡 Practical Implications

**For Developers:**
- Match methodology to task complexity and context
- Simple tasks need simple solutions (avoid over-engineering)
- Optimize prompts first - universal 20-30% improvement
- Use Monte Carlo sampling for high-value creative outputs

**For AI Researchers:**
- Methodology guidance > model selection for predictable outcomes
- Context creates non-intuitive performance inversions
- Component discovery needs explicit architectural awareness
- Validate findings statistically before publishing

**For Product Teams:**
- Best-of-N sampling improves creative output quality by ~20%
- Documentation-first approach reduces rework and improves maintainability
- Parallel methodology testing reveals optimal approach for your domain

---

## 🔗 Resources

**Core Documentation:**
- [All Experiments Index](docs/EXPERIMENT_INDEX.md)
- [Research History](docs/EXPERIMENT_HISTORY.md)
- [Validated Findings](findings/README.md)
- [Methodology Framework](META_PROMPT_GENERATOR_V4.md)

**Notable Experiments:**
- [1.608 Story-to-Haiku](experiments/1.608-story-to-haiku/) - LLM integration showcase ⭐
- [1.502 URL Validator Multi-Run](experiments/1.502-url-validator/EXPERIMENT_REPORT.md) - 32X methodology differences
- [2.505.1 Component Discovery](experiments/2.505.1-guided-component-discovery/EXPERIMENT_REPORT.md) - 0% → 100% with guidance
- [1.504 Date Format Validator](experiments/1.504-date-format-validator/EXPERIMENT_REPORT.md) - Adaptive TDD optimal balance

---

## 🤝 Contributing

This is an open research project. We welcome:
- Replication studies
- New experiment domains
- Methodology refinements
- Feedback on findings

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📝 Citation

If you use this methodology or findings in your work:

```
Schneider, I. (2025). spawn-experiments: Systematic Research on AI Development Methodologies.
GitHub repository: https://github.com/ivantohelpyou/spawn-experiments
```

---

**Latest Update:** September 30, 2025 - Added Experiment 1.608.A (Iambic Pentameter), Finding #11 (LLM Integration Methodology), and Performance Leaderboard

**Status:** Active research - new experiments added regularly

**Contact:** Presenting at AI Tinkerers meetups and conferences
