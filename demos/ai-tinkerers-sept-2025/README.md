# AI Tinkerers Seattle - September 30, 2025

**Talk:** "Building Working Code Live: Documentation-First AI Development"

## Demo Materials

### 1. Video Walkthrough
**1.608.4 Story-to-Haiku Converter Build** (1-2 minute time-lapse)
- Full implementation from start to finish (48min → 1-2min)
- Shows all 4 methodologies in parallel
- Olympic judging system demonstration

📺 **YouTube:** [Link coming soon]

### 2. Live Demo Commands
**[1.608 Poetry Series Experiments](1.608-poetry-series.md)**
- Single-command execution (no stops)
- Three variations: Iambic Pentameter, Limericks, Terza Rima
- Ready to run live on stage

### 3. Key Experiment
**[Experiment 1.608: Story-to-Haiku Converter](../../experiments/1.608-story-to-haiku/)**
- Complete 4-run series with validated findings
- Working CLI tool
- Code quality analysis

### 4. Validated Findings
- **[Finding 09: Prompt Engineering Force Multiplier](../../findings/09-prompt-engineering-force-multiplier-1608.md)** - 22-36% speed improvement + quality gains
- **[Finding 10: Monte Carlo Methodology Sampling](../../findings/10-monte-carlo-methodology-sampling-1608.md)** - 20% quality improvement via best-of-N

## Quick Start

Try the haiku generator:
```bash
cd experiments/1.608-story-to-haiku
tools/generate-haiku "Your story here" --run 4 --top 3
```

Run a complete poetry experiment:
```bash
# See 1.608-poetry-series.md for full commands
claude "Run Experiment 1.608.B - Limerick Converter..."
```

## Talk Outline

1. **Problem**: AI code generation is unpredictable
2. **Hypothesis**: Methodology choice affects outcomes more than model choice
3. **Evidence**: 32X code differences, context flips performance
4. **Demo**: Live build of poetry converter with 4 methodologies
5. **Results**: Validated findings on prompt engineering and sampling

## Resources

- **Methodology Framework**: [META_PROMPT_GENERATOR_V4.md](../../META_PROMPT_GENERATOR_V4.md)
- **Research Portfolio**: [All Findings](../../findings/README.md)
- **Experiment Index**: [Complete List](../../docs/EXPERIMENT_INDEX.md)

---

**Repository**: https://github.com/ivantohelpyou/spawn-experiments

**Contact**: Presenting at AI Tinkerers meetups and conferences
