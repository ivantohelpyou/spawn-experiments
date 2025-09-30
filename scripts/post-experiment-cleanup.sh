#!/bin/bash
#
# Post-Experiment Cleanup Script
# Remove build artifacts, test cache, and nested venvs after experiments complete
#
# Usage: ./scripts/post-experiment-cleanup.sh [experiment-dir]
#        If no experiment-dir specified, cleans entire experiments/ directory
#

set -e

# Determine target directory
TARGET_DIR="${1:-experiments}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Error: Directory not found: $TARGET_DIR"
    exit 1
fi

echo "🧹 Post-Experiment Cleanup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Target: $TARGET_DIR"
echo ""

# Function to count and remove
cleanup_items() {
    local pattern="$1"
    local description="$2"
    local find_type="$3"

    if [ "$find_type" = "d" ]; then
        count=$(find "$TARGET_DIR" -type d -name "$pattern" 2>/dev/null | wc -l)
    else
        count=$(find "$TARGET_DIR" -type f -name "$pattern" 2>/dev/null | wc -l)
    fi

    if [ "$count" -gt 0 ]; then
        echo "  Removing $count $description..."
        find "$TARGET_DIR" -type "$find_type" -name "$pattern" -exec rm -rf {} + 2>/dev/null || true
    else
        echo "  ✓ No $description found"
    fi
}

# 1. Python cache directories
echo "📦 Python Cache & Bytecode"
cleanup_items "__pycache__" "__pycache__ directories" "d"
cleanup_items "*.pyc" ".pyc files" "f"
cleanup_items "*.pyo" ".pyo files" "f"

# 2. Test artifacts
echo ""
echo "🧪 Test Artifacts"
cleanup_items ".pytest_cache" ".pytest_cache directories" "d"
cleanup_items ".coverage" ".coverage files" "f"
cleanup_items "htmlcov" "htmlcov directories" "d"
cleanup_items ".tox" ".tox directories" "d"

# 3. Nested venvs (keep only top-level experiment venvs)
echo ""
echo "🐍 Virtual Environments (Nested Only)"

# Find all venvs
all_venvs=$(find "$TARGET_DIR" -type d -name "venv" -o -type d -name ".venv" 2>/dev/null)

if [ -z "$all_venvs" ]; then
    echo "  ✓ No venvs found"
else
    # Identify top-level venvs (direct children of experiment directories)
    # Pattern: experiments/1.XXX-name/venv
    top_level_venvs=$(echo "$all_venvs" | grep -E "experiments/[^/]+/\.?venv$" || true)

    # Nested venvs are everything else
    nested_count=0

    while IFS= read -r venv_path; do
        if [ -z "$venv_path" ]; then
            continue
        fi

        # Check if this is a top-level venv
        if echo "$top_level_venvs" | grep -q "^$venv_path$"; then
            echo "  ⚡ Keeping top-level: $venv_path"
        else
            echo "  🗑️  Removing nested: $venv_path"
            rm -rf "$venv_path"
            ((nested_count++))
        fi
    done <<< "$all_venvs"

    echo ""
    echo "  Removed $nested_count nested venv(s)"
fi

# 4. Editor/IDE artifacts
echo ""
echo "📝 Editor Artifacts"
cleanup_items ".vscode" ".vscode directories" "d"
cleanup_items ".idea" ".idea directories" "d"
cleanup_items "*.swp" "vim swap files" "f"
cleanup_items "*.swo" "vim swap files" "f"
cleanup_items "*~" "backup files" "f"

# 5. OS artifacts
echo ""
echo "💾 OS Artifacts"
cleanup_items ".DS_Store" ".DS_Store files" "f"
cleanup_items "Thumbs.db" "Thumbs.db files" "f"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Cleanup complete!"
echo ""
echo "💡 Note: Top-level venvs were preserved for active tools/scripts"
echo "   To remove a specific venv: rm -rf experiments/1.XXX-name/venv"
echo ""
