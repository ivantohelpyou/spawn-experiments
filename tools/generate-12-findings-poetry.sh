#!/bin/bash
# Generate poetry for all 12 findings

OUTPUT_FILE="notes/12-findings-poetry-showcase.md"
POETRY_TOOL="tools/generate-poetry"

cd "$(dirname "$0")/.."

echo "Generating poetry for 12 findings..."
echo ""

# Create header
cat > "$OUTPUT_FILE" << 'EOF'
# 12 Findings Poetry Showcase
## All Research Findings as Poetry

Each of the 12 validated findings from spawn-experiments converted into 3 poetry formats:
- 🎋 **Haiku** (5-7-5 syllables)
- 📜 **Iambic Pentameter** (10 syllables/line)
- 🎪 **Limerick** (AABBA rhyme scheme)

All outputs are **gold medal winners** (Method 2: Specification-Driven).

---

EOF

# Finding 01
echo "[1/12] AI Over-Engineering Patterns..."
echo "  → Running generate-poetry..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 01: AI Over-Engineering Patterns

**Research Summary:**
> AI code generators exhibit systematic over-engineering when given vague requirements. Without constraints, they create enterprise-grade solutions for simple tasks, adding unnecessary complexity like rate limiting and batch processing for basic validators.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/01-ai-over-engineering-patterns.md)**

EOF
POETRY_OUTPUT=$($POETRY_TOOL "AI code generators exhibit systematic over-engineering when given vague requirements. Without constraints, they create enterprise-grade solutions for simple tasks, adding unnecessary complexity like rate limiting and batch processing for basic validators.")
echo "  → Poetry tool output captured"
echo "$POETRY_OUTPUT" | grep -E "(Haiku|Iambic|Limerick)" | head -3 | sed 's/^/     DEBUG: /'
echo "$POETRY_OUTPUT" | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "  ✓ Finding 01 complete"
sleep 2

# Finding 02
echo "[2/12] Architectural Convergence Patterns..."
echo "  → Running generate-poetry..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 02: Architectural Convergence Patterns

**Research Summary:**
> Despite starting with different methodologies, AI implementations converge toward similar architectural patterns. Class-based designs with clear separation of concerns emerge naturally, suggesting certain code structures are inherently more discoverable.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/02-architectural-convergence-patterns.md)**

EOF
POETRY_OUTPUT=$($POETRY_TOOL "Despite starting with different methodologies, AI implementations converge toward similar architectural patterns. Class-based designs with clear separation of concerns emerge naturally, suggesting certain code structures are inherently more discoverable.")
echo "  → Poetry tool output captured"
echo "$POETRY_OUTPUT" | grep -E "(Haiku|Iambic|Limerick)" | head -3 | sed 's/^/     DEBUG: /'
echo "$POETRY_OUTPUT" | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "  ✓ Finding 02 complete"
sleep 2

# Finding 03
echo "[3/12] Complexity Matching Principle..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 03: Complexity Matching Principle

**Research Summary:**
> Effective AI-assisted development requires matching methodology complexity to task complexity. Over-engineered approaches waste time on simple tasks, while under-engineered approaches fail on complex systems. The right methodology depends entirely on problem characteristics.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/03-complexity-matching-principle.md)**

EOF
$POETRY_TOOL "Effective AI-assisted development requires matching methodology complexity to task complexity. Over-engineered approaches waste time on simple tasks, while under-engineered approaches fail on complex systems. The right methodology depends entirely on problem characteristics." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 04
echo "[4/12] Component Discovery Breakthrough..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 04: Component Discovery Breakthrough

**Research Summary:**
> Using external code components as references dramatically accelerates AI development. When shown existing implementations, AI tools understand requirements faster and produce better results. Component-guided development reduces iteration cycles significantly.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/04-component-discovery-breakthrough-2505.md)**

EOF
$POETRY_TOOL "Using external code components as references dramatically accelerates AI development. When shown existing implementations, AI tools understand requirements faster and produce better results. Component-guided development reduces iteration cycles significantly." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 05
echo "[5/12] External Library Efficiency..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 05: External Library Efficiency

**Research Summary:**
> External libraries outperform AI-generated implementations by ten to one thousand times. For well-solved problems like date validation, using established libraries provides better performance, fewer bugs, and less maintenance burden than custom AI-generated code.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/05-external-library-efficiency-analysis-2505.md)**

EOF
$POETRY_TOOL "External libraries outperform AI-generated implementations by ten to one thousand times. For well-solved problems like date validation, using established libraries provides better performance, fewer bugs, and less maintenance burden than custom AI-generated code." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 06
echo "[6/12] External vs Internal Components..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 06: External vs Internal Components

**Research Summary:**
> The choice between external libraries and internal implementations depends on problem novelty. Use external libraries for solved problems with mature ecosystems. Build internally for novel problems, domain-specific logic, or when dependencies create more complexity than value.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/06-external-vs-internal-components-2505.md)**

EOF
$POETRY_TOOL "The choice between external libraries and internal implementations depends on problem novelty. Use external libraries for solved problems with mature ecosystems. Build internally for novel problems, domain-specific logic, or when dependencies create more complexity than value." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 07
echo "[7/12] Input Validation Patterns..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 07: Input Validation Patterns

**Research Summary:**
> AI-generated input validation follows predictable patterns across methodologies. All approaches create similar error detection logic, but differ in code organization and test coverage. The validation logic itself remains remarkably consistent.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/07-input-validation-patterns.md)**

EOF
$POETRY_TOOL "AI-generated input validation follows predictable patterns across methodologies. All approaches create similar error detection logic, but differ in code organization and test coverage. The validation logic itself remains remarkably consistent." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 08
echo "[8/12] Selective TDD Discovery..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 08: Selective TDD Discovery

**Research Summary:**
> Strategic test-driven development outperforms uniform approaches. Adaptive TDD focuses testing effort on complex areas while keeping simple code lightweight. This accidental discovery proved more effective than rigidly applying TDD everywhere.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/08-selective-tdd-accidental-discovery.md)**

EOF
$POETRY_TOOL "Strategic test-driven development outperforms uniform approaches. Adaptive TDD focuses testing effort on complex areas while keeping simple code lightweight. This accidental discovery proved more effective than rigidly applying TDD everywhere." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 09
echo "[9/12] Prompt Engineering Force Multiplier..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 09: Prompt Engineering Force Multiplier

**Research Summary:**
> Optimized prompts improve both speed and quality across all methodologies. Better prompts reduced generation time by twenty-two to thirty-six percent while simultaneously improving output quality. Prompt engineering amplifies every development approach.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/09-prompt-engineering-force-multiplier-1608.md)**

EOF
$POETRY_TOOL "Optimized prompts improve both speed and quality across all methodologies. Better prompts reduced generation time by twenty-two to thirty-six percent while simultaneously improving output quality. Prompt engineering amplifies every development approach." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 10
echo "[10/12] Monte Carlo Methodology Sampling..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 10: Monte Carlo Methodology Sampling

**Research Summary:**
> Generating multiple samples and selecting the best produces twenty percent quality improvement. This Monte Carlo approach works across all methodologies, making it a practical production technique for critical code where quality matters more than development speed.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/10-monte-carlo-methodology-sampling-1608.md)**

EOF
$POETRY_TOOL "Generating multiple samples and selecting the best produces twenty percent quality improvement. This Monte Carlo approach works across all methodologies, making it a practical production technique for critical code where quality matters more than development speed." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 11
echo "[11/12] LLM Integration Advantage..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 11: LLM Integration Advantage

**Research Summary:**
> Specification-driven development consistently wins for LLM integration projects. Method two averages ninety-two out of one hundred quality score, outperforming faster methods by ten to eighteen points. Complex systems with external dependencies benefit from upfront design.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/11-llm-integration-specification-advantage.md)**

EOF
$POETRY_TOOL "Specification-driven development consistently wins for LLM integration projects. Method two averages ninety-two out of one hundred quality score, outperforming faster methods by ten to eighteen points. Complex systems with external dependencies benefit from upfront design." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
sleep 2

# Finding 12
echo "[12/12] Problem-Type Performance Variance..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 12: Problem-Type Performance Variance

**Research Summary:**
> No single methodology wins across all problem types. Specification-driven excels at LLM integration but creates thirty-two times code bloat on simple validators. Methodology performance depends on problem complexity profile, not task difficulty alone.

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/12-methodology-performance-by-problem-type.md)**

EOF
$POETRY_TOOL "No single methodology wins across all problem types. Specification-driven excels at LLM integration but creates thirty-two times code bloat on simple validators. Methodology performance depends on problem complexity profile, not task difficulty alone." | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Footer
cat >> "$OUTPUT_FILE" << 'EOF'

## Technical Details

- **Total Findings**: 12
- **Total Poems**: 36 (12 findings × 3 formats)
- **Method**: Specification-Driven (Method 2) - Gold medal winner
- **LLM Model**: llama3.2 (poetry generation)
- **Evaluation**: Claude Sonnet 4.5 (code quality assessment)
- **Generated**: 2025-09-30

---

*Generated by: tools/generate-12-findings-poetry.sh*
EOF

echo ""
echo "✓ Complete! Output written to: $OUTPUT_FILE"
echo "✓ Total: 12 findings × 3 poetry formats = 36 poems"
