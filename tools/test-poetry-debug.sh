#!/bin/bash
# Test script - runs first 2 findings with debug output

OUTPUT_FILE="notes/test-poetry-debug.md"
POETRY_TOOL="tools/generate-poetry"

cd "$(dirname "$0")/.."

echo "Testing poetry generation with debug output..."
echo ""

# Create header
cat > "$OUTPUT_FILE" << 'EOF'
# Test Poetry Showcase - First 2 Findings

---

EOF

# Finding 01
echo "[1/2] AI Over-Engineering Patterns..."
echo "  → Running generate-poetry..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 01: AI Over-Engineering Patterns

**Research Summary:**
> AI code generators exhibit systematic over-engineering when given vague requirements.

EOF

POETRY_OUTPUT=$($POETRY_TOOL "AI code generators exhibit systematic over-engineering when given vague requirements")
echo "  → Poetry tool returned (exit code: $?)"
echo "  → Checking what was generated:"
echo "$POETRY_OUTPUT" | grep -E "(🎋 Haiku|📜 Iambic|🎪 Limerick)" | sed 's/^/     /'
echo ""
echo "$POETRY_OUTPUT" | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "  ✓ Finding 01 complete"
echo ""
sleep 2

# Finding 02
echo "[2/2] Architectural Convergence Patterns..."
echo "  → Running generate-poetry..."
cat >> "$OUTPUT_FILE" << 'EOF'
## Finding 02: Architectural Convergence Patterns

**Research Summary:**
> Despite starting with different methodologies, AI implementations converge.

EOF

POETRY_OUTPUT=$($POETRY_TOOL "Despite starting with different methodologies, AI implementations converge toward similar architectural patterns")
echo "  → Poetry tool returned (exit code: $?)"
echo "  → Checking what was generated:"
echo "$POETRY_OUTPUT" | grep -E "(🎋 Haiku|📜 Iambic|🎪 Limerick)" | sed 's/^/     /'
echo ""
echo "$POETRY_OUTPUT" | sed -n '/🥇 GOLD MEDAL RESULTS/,/✨ Generated/p' | head -n -1 | sed 's/$/  /' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "  ✓ Finding 02 complete"

echo ""
echo "✓ Test complete! Output written to: $OUTPUT_FILE"
echo ""
echo "Preview of output:"
tail -30 "$OUTPUT_FILE"
