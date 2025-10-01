#!/bin/bash
# Test Finding 01 - run all methods and see which wins

OUTPUT_FILE="notes/test-finding-01-poetry.md"

cd "$(dirname "$0")/.."

echo "Testing Finding 01 - AI Over-Engineering Patterns"
echo ""

SUMMARY="AI code generators exhibit systematic over-engineering when given vague requirements. Without constraints, they create enterprise-grade solutions for simple tasks, adding unnecessary complexity like rate limiting and batch processing for basic validators."

# Create file
cat > "$OUTPUT_FILE" << EOF
# Test: Finding 01 - AI Over-Engineering Patterns

**Research Summary:**
> ${SUMMARY}

---

EOF

# Generate Haiku
echo "🎋 Running Haiku (top 3 methods)..."
HAIKU_OUTPUT=$(cd experiments/1.608-story-to-haiku && tools/generate-haiku "${SUMMARY}" --run 4 --top 3 2>&1)
echo "$HAIKU_OUTPUT"
echo ""

HAIKU_GOLD=$(echo "$HAIKU_OUTPUT" | sed -n '/🥇 Gold/,/Syllables:/p' | grep -v "Syllables:" | grep -v "🥇 Gold" | grep -v "^-" | sed '/^$/d' | sed 's/^   //')
HAIKU_METHOD=$(echo "$HAIKU_OUTPUT" | grep "🥇 Gold" | sed 's/.*- //')

cat >> "$OUTPUT_FILE" << EOF
## 🥇 Haiku Gold Medal
**Winner:** ${HAIKU_METHOD}

${HAIKU_GOLD}

---

EOF

echo "✓ Haiku winner: ${HAIKU_METHOD}"
echo ""
sleep 2

# Generate Iambic
echo "📜 Running Iambic Pentameter (top 3 methods)..."
IAMBIC_OUTPUT=$(cd experiments/1.608.A-iambic-pentameter && tools/generate-iambic "${SUMMARY}" --top 3 2>&1)
echo "$IAMBIC_OUTPUT"
echo ""

IAMBIC_GOLD=$(echo "$IAMBIC_OUTPUT" | sed -n '/🥇 GOLD:/,/^$/p' | tail -n +3 | sed '/^$/d' | sed '/^=/d')
IAMBIC_METHOD=$(echo "$IAMBIC_OUTPUT" | grep "🥇 GOLD:" | sed 's/.*GOLD: //' | sed 's/ (.*//')

cat >> "$OUTPUT_FILE" << EOF
## 🥇 Iambic Pentameter Gold Medal
**Winner:** ${IAMBIC_METHOD}

${IAMBIC_GOLD}

---

EOF

echo "✓ Iambic winner: ${IAMBIC_METHOD}"
echo ""
sleep 2

# Generate Limerick
echo "🎪 Running Limerick (all 4 methods)..."
LIMERICK_OUTPUT=$(cd experiments/1.608.B-limerick-converter && tools/generate-limerick "${SUMMARY}" --run 1 --all 2>&1)
echo "$LIMERICK_OUTPUT"
echo ""

LIMERICK_GOLD=$(echo "$LIMERICK_OUTPUT" | sed -n '/🥇 Method/,/✓/p' | head -n -1 | tail -n +2 | sed '/^$/d' | sed 's/^   //')
LIMERICK_METHOD=$(echo "$LIMERICK_OUTPUT" | grep "🥇" | head -1 | sed 's/.*🥇 //' | sed 's/Generating.*//' | xargs)

cat >> "$OUTPUT_FILE" << EOF
## 🥇 Limerick Gold Medal
**Winner:** ${LIMERICK_METHOD}

${LIMERICK_GOLD}

---

EOF

echo "✓ Limerick winner: ${LIMERICK_METHOD}"
echo ""

# Summary
echo "================================================"
echo "GOLD MEDAL WINNERS FOR FINDING 01:"
echo "================================================"
echo "🎋 Haiku:  ${HAIKU_METHOD}"
echo "📜 Iambic: ${IAMBIC_METHOD}"
echo "🎪 Limerick: ${LIMERICK_METHOD}"
echo ""
echo "Output saved to: ${OUTPUT_FILE}"
