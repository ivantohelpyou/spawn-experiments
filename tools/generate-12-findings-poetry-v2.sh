#!/bin/bash
# Generate poetry for all 12 findings - showing actual GOLD winners

OUTPUT_FILE="notes/12-findings-poetry-showcase.md"

cd "$(dirname "$0")/.."

echo "Generating poetry for 12 findings (running all methods, showing gold winners)..."
echo ""

# Create header
cat > "$OUTPUT_FILE" << 'EOF'
# 12 Findings Poetry Showcase
## All Research Findings as Poetry

Each of the 12 validated findings from spawn-experiments converted into 3 poetry formats:
- 🎋 **Haiku** (5-7-5 syllables)
- 📜 **Iambic Pentameter** (10 syllables/line)
- 🎪 **Limerick** (AABBA rhyme scheme)

**Note**: Each format runs multiple methodologies and shows the **GOLD medal winner** based on accuracy/quality.

---

EOF

# Array of findings
declare -a SUMMARIES=(
    "AI code generators exhibit systematic over-engineering when given vague requirements. Without constraints, they create enterprise-grade solutions for simple tasks, adding unnecessary complexity like rate limiting and batch processing for basic validators."
    "Despite starting with different methodologies, AI implementations converge toward similar architectural patterns. Class-based designs with clear separation of concerns emerge naturally, suggesting certain code structures are inherently more discoverable."
    "Effective AI-assisted development requires matching methodology complexity to task complexity. Over-engineered approaches waste time on simple tasks, while under-engineered approaches fail on complex systems. The right methodology depends entirely on problem characteristics."
    "Using external code components as references dramatically accelerates AI development. When shown existing implementations, AI tools understand requirements faster and produce better results. Component-guided development reduces iteration cycles significantly."
    "External libraries outperform AI-generated implementations by ten to one thousand times. For well-solved problems like date validation, using established libraries provides better performance, fewer bugs, and less maintenance burden than custom AI-generated code."
    "The choice between external libraries and internal implementations depends on problem novelty. Use external libraries for solved problems with mature ecosystems. Build internally for novel problems, domain-specific logic, or when dependencies create more complexity than value."
    "AI-generated input validation follows predictable patterns across methodologies. All approaches create similar error detection logic, but differ in code organization and test coverage. The validation logic itself remains remarkably consistent."
    "Strategic test-driven development outperforms uniform approaches. Adaptive TDD focuses testing effort on complex areas while keeping simple code lightweight. This accidental discovery proved more effective than rigidly applying TDD everywhere."
    "Optimized prompts improve both speed and quality across all methodologies. Better prompts reduced generation time by twenty-two to thirty-six percent while simultaneously improving output quality. Prompt engineering amplifies every development approach."
    "Generating multiple samples and selecting the best produces twenty percent quality improvement. This Monte Carlo approach works across all methodologies, making it a practical production technique for critical code where quality matters more than development speed."
    "Specification-driven development consistently wins for LLM integration projects. Method two averages ninety-two out of one hundred quality score, outperforming faster methods by ten to eighteen points. Complex systems with external dependencies benefit from upfront design."
    "No single methodology wins across all problem types. Specification-driven excels at LLM integration but creates thirty-two times code bloat on simple validators. Methodology performance depends on problem complexity profile, not task difficulty alone."
)

declare -a TITLES=(
    "AI Over-Engineering Patterns"
    "Architectural Convergence Patterns"
    "Complexity Matching Principle"
    "Component Discovery Breakthrough"
    "External Library Efficiency"
    "External vs Internal Components"
    "Input Validation Patterns"
    "Selective TDD Discovery"
    "Prompt Engineering Force Multiplier"
    "Monte Carlo Methodology Sampling"
    "LLM Integration Advantage"
    "Problem-Type Performance Variance"
)

declare -a LINKS=(
    "01-ai-over-engineering-patterns.md"
    "02-architectural-convergence-patterns.md"
    "03-complexity-matching-principle.md"
    "04-component-discovery-breakthrough-2505.md"
    "05-external-library-efficiency-analysis-2505.md"
    "06-external-vs-internal-components-2505.md"
    "07-input-validation-patterns.md"
    "08-selective-tdd-accidental-discovery.md"
    "09-prompt-engineering-force-multiplier-1608.md"
    "10-monte-carlo-methodology-sampling-1608.md"
    "11-llm-integration-specification-advantage.md"
    "12-methodology-performance-by-problem-type.md"
)

for i in {0..11}; do
    NUM=$((i+1))
    PADDED=$(printf "%02d" $NUM)

    echo "[${NUM}/12] ${TITLES[$i]}..."

    # Add finding header
    cat >> "$OUTPUT_FILE" << EOF
## Finding ${PADDED}: ${TITLES[$i]}

**Research Summary:**
> ${SUMMARIES[$i]}

**[→ Read full finding](https://github.com/ivantohelpyou/spawn-experiments/blob/main/findings/${LINKS[$i]})**

EOF

    # Generate Haiku
    echo "  → Haiku..."
    HAIKU_OUTPUT=$(cd experiments/1.608-story-to-haiku && tools/generate-haiku "${SUMMARIES[$i]}" --run 4 --top 3 2>&1)
    HAIKU_GOLD=$(echo "$HAIKU_OUTPUT" | sed -n '/🥇 Gold/,/Syllables:/p' | grep -v "Syllables:" | grep -v "🥇 Gold" | grep -v "^-" | sed '/^$/d' | sed 's/^   //' | sed 's/$/  /')
    HAIKU_METHOD=$(echo "$HAIKU_OUTPUT" | grep "🥇 Gold" | sed 's/.*- //' | sed 's/🥇 Gold - //')

    cat >> "$OUTPUT_FILE" << EOF
### 🥇 Haiku Gold Medal
**Winner:** ${HAIKU_METHOD}

EOF
    echo "$HAIKU_GOLD" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    # Generate Iambic
    echo "  → Iambic Pentameter..."
    IAMBIC_OUTPUT=$(cd experiments/1.608.A-iambic-pentameter && tools/generate-iambic "${SUMMARIES[$i]}" --top 3 2>&1)
    IAMBIC_GOLD=$(echo "$IAMBIC_OUTPUT" | sed -n '/🥇 GOLD:/,/^$/p' | tail -n +3 | sed '/^$/d' | sed '/^=/d' | sed 's/$/  /')
    IAMBIC_METHOD=$(echo "$IAMBIC_OUTPUT" | grep "🥇 GOLD:" | sed 's/.*GOLD: //' | sed 's/ (.*//')

    cat >> "$OUTPUT_FILE" << EOF
### 🥇 Iambic Pentameter Gold Medal
**Winner:** ${IAMBIC_METHOD}

EOF
    echo "$IAMBIC_GOLD" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    # Generate Limerick
    echo "  → Limerick..."
    LIMERICK_OUTPUT=$(cd experiments/1.608.B-limerick-converter && tools/generate-limerick "${SUMMARIES[$i]}" --run 1 --all 2>&1)
    LIMERICK_GOLD=$(echo "$LIMERICK_OUTPUT" | sed -n '/🥇 Method 2/,/✓/p' | grep -v "🥇" | grep -v "Generating" | grep -v "✓" | sed '/^$/d' | sed 's/^   //' | sed 's/$/  /')
    LIMERICK_METHOD=$(echo "$LIMERICK_OUTPUT" | grep "🥇" | head -1 | sed 's/.*🥇 //' | sed 's/Generating.*//' | xargs)

    cat >> "$OUTPUT_FILE" << EOF
### 🥇 Limerick Gold Medal
**Winner:** ${LIMERICK_METHOD}

EOF
    echo "$LIMERICK_GOLD" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    echo "  ✓ Complete"
    sleep 2
done

# Footer
cat >> "$OUTPUT_FILE" << 'EOF'

## Technical Details

- **Total Findings**: 12
- **Total Poems**: 36 (12 findings × 3 formats)
- **Methodology**: Each format runs multiple methods, shows gold medal winner
- **LLM Model**: llama3.2 (poetry generation)
- **Judging**: Accuracy-based (syllable counts, rhyme schemes, meter)
- **Generated**: 2025-09-30

---

*Generated by: tools/generate-12-findings-poetry-v2.sh*
EOF

echo ""
echo "✓ Complete! Output written to: $OUTPUT_FILE"
echo "✓ Total: 12 findings × 3 poetry formats = 36 poems"
echo "✓ Each poem is the gold medal winner from running multiple methodologies"
