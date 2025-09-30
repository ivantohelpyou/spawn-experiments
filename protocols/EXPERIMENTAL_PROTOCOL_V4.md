# Experimental Protocol V4: Public/Private Branch Management

## Date: 2025-09-25
**Supersedes**: EXPERIMENTAL_PROTOCOL_V3.md

## Key Addition: Public/Private Decision Point

### Phase 0: Experiment Planning & Branch Decision
**MANDATORY FIRST STEP**: Before starting any experiment, ask user:

```
"Should this experiment be public (main branch) or private (private-main branch)?"
```

Based on response:
- **Public**: Work and commit to `main` branch - results will be visible publicly
- **Private**: Work and commit to `private-main` branch - results remain private

### Branch Strategy:
```bash
# For PUBLIC experiments:
git checkout main
git checkout -b experiment-{ID}-method-{N}
# ... work ...
git checkout main
git merge experiment-{ID}-method-{N}
git commit -m "Add: Public experiment {ID}..."

# For PRIVATE experiments:
git checkout private-main
git checkout -b experiment-{ID}-method-{N}
# ... work ...
git checkout private-main
git merge experiment-{ID}-method-{N}
git commit -m "Add: Private experiment {ID}..."
```

## Complete Protocol Flow

### Phase 0: Branch Decision (NEW)
1. **Ask user**: "Should experiment {ID} be public or private?"
2. **Set target branch**: `main` (public) or `private-main` (private)
3. **Document decision**: Include in experiment README

### Phase 1: Initial Setup
1. Create baseline specification and commit to target branch
2. Each method starts from this same committed state
3. No method can see other method implementations

### Phase 2: Method Execution
Each method follows this pattern:
```bash
# 1. Create isolated branch from target branch (main OR private-main)
git checkout {target-branch}
git checkout -b experiment-{ID}-method-{N}

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install only required dependencies
pip install {required-libs}  # e.g., segno

# 4. Work in method folder only
mkdir {N}-{method-name}
cd {N}-{method-name}

# 5. Periodic commits (every major milestone)
git add .
git commit -m "Method {N}: {milestone description}"

# 6. Final commit with complete implementation
git add .
git commit -m "Method {N}: Complete implementation"
```

### Phase 3: Code Capture Requirements
**CRITICAL**: Agents must include ALL generated code inline in responses

### Phase 4: Final Commit to Target Branch
```bash
# Merge to target branch (main OR private-main)
git checkout {target-branch}
git merge experiment-{ID}-method-{N}
git commit -m "Add: Experiment {ID} - {description}

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Phase 5: Post-Experiment Cleanup
After experiment completion, clean up build artifacts and development dependencies:

```bash
# Run cleanup script (removes __pycache__, .pytest_cache, nested venvs, etc.)
./scripts/post-experiment-cleanup.sh experiments/{ID}-{name}

# Or clean entire experiments directory:
./scripts/post-experiment-cleanup.sh
```

**What gets cleaned:**
- Python cache (`__pycache__`, `.pyc`, `.pyo`)
- Test artifacts (`.pytest_cache`, `.coverage`, `htmlcov`)
- Nested venvs (keeps only top-level experiment venvs)
- Editor artifacts (`.vscode`, `.idea`, swap files)
- OS artifacts (`.DS_Store`, `Thumbs.db`)

**What gets preserved:**
- Top-level venvs for active tools/scripts
- Source code and experiment results
- Documentation and reports

## Example Usage

### Public Experiment:
```
User: "Let's run experiment 1.508"
Assistant: "Should experiment 1.508 be public (main branch) or private (private-main branch)?"
User: "Public"
Assistant: [Works on main branch, commits publicly]
```

### Private Experiment:
```
User: "Let's run experiment 1.507.2"
Assistant: "Should experiment 1.507.2 be public (main branch) or private (private-main branch)?"
User: "Private"
Assistant: [Works on private-main branch, keeps results private]
```

## Benefits
1. **User Control**: Explicit choice for each experiment
2. **No Accidents**: Prevents accidental public commits of private research
3. **Clean Separation**: Public/private work clearly separated
4. **Reversibility**: Can still move experiments between branches if needed

## Default Behavior
If user doesn't specify, **always ask** - never assume public or private.