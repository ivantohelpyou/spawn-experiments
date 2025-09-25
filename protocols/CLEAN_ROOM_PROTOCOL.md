# Clean Room Protocol for Severed Branch Experimental Setup

## Safety-First Approach for Method Isolation

**Purpose**: Create completely isolated experimental environments using severed git branches while maintaining safety.

## Pre-Flight Safety Checks

### 1. Environment Verification
```bash
# Check we're in spawn-experiments
if [[ "$PWD" != */spawn-experiments/* ]]; then
    echo "❌ ERROR: Not in spawn-experiments directory!"
    echo "Current: $PWD"
    exit 1
fi
echo "✅ Location verified: spawn-experiments"
```

### 2. Clean Git State
```bash
# Ensure no uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ ERROR: Working tree not clean!"
    echo "Commit or stash changes first:"
    git status
    exit 1
fi
echo "✅ Git state clean"
```

### 3. Branch Safety Check
```bash
# Prevent accidental wipe of main branches
current_branch=$(git branch --show-current)
if [[ "$current_branch" == "main" || "$current_branch" == "private-main" ]]; then
    echo "❌ ERROR: Cannot wipe contents on main branches!"
    echo "Current branch: $current_branch"
    exit 1
fi
echo "✅ Safe branch: $current_branch"
```

### 4. Isolation Verification
```bash
# Verify branch indicates experimental isolation
if [[ "$current_branch" != *"isolated"* && "$current_branch" != *"method-"* ]]; then
    echo "❌ ERROR: Branch name doesn't indicate isolation!"
    echo "Branch should contain 'isolated' or 'method-'"
    echo "Current: $current_branch"
    exit 1
fi
echo "✅ Isolation confirmed: $current_branch"
```

## Safe Cleanup Procedure

### 5. Controlled Wipe
```bash
echo "🧹 Beginning safe cleanup on branch: $current_branch"

# Remove git-tracked files
git rm -rf . 2>/dev/null || true
echo "✅ Removed tracked files"

# Remove hidden files (safe pattern - avoids . and ..)
find . -name ".[!.]*" -exec rm -rf {} + 2>/dev/null || true
echo "✅ Removed hidden files"

# Remove visible files
rm -rf * 2>/dev/null || true
echo "✅ Removed visible files"

# Verify cleanup
if [[ $(ls -la | wc -l) -eq 3 ]]; then  # Only . and .. should remain
    echo "✅ Clean room achieved"
else
    echo "⚠️  Cleanup verification:"
    ls -la
fi
```

## Complete Severed Branch Setup

### Full Safe Protocol
```bash
#!/bin/bash
set -e  # Exit on any error

# 1. SAFETY CHECKS
source clean_room_checks.sh  # Include all safety checks above

# 2. PREPARE METHOD PACKAGE
mkdir -p method-package/
cp baseline_specification.md method-package/
# Add any method-specific files needed

# 3. STASH PACKAGE
git add method-package/
git stash push -m "Method isolated environment package"

# 4. CREATE SEVERED BRANCH
git checkout --orphan method-1-isolated

# 5. SAFE CLEANUP (with all checks above)
source clean_room_protocol.sh

# 6. RESTORE PACKAGE
git stash pop
mv method-package/* . 2>/dev/null || true
rmdir method-package/ 2>/dev/null || true

# 7. COMMIT CLEAN ENVIRONMENT
git add .
git commit -m "Method 1: Clean isolated environment - ready for agent"

echo "🎯 Severed branch ready: $(git branch --show-current)"
echo "📁 Contents:"
ls -la
```

## Emergency Recovery

### If Something Goes Wrong
```bash
# Immediate abort - return to safe branch
git checkout private-main

# Delete problematic isolated branch
git branch -D method-1-isolated 2>/dev/null || true

# Recover stash if needed
git stash list
git stash pop  # if package is still stashed
```

## Usage for Methods 1&2

```bash
# Method 1 setup
./setup_severed_branch.sh method-1-isolated "1-immediate-implementation"

# Method 2 setup
./setup_severed_branch.sh method-2-isolated "2-specification-driven"
```

This protocol ensures **zero risk** to main branches while creating perfect experimental isolation.