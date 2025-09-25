# Demo Setup Instructions for 2.505.2

## Prerequisites - UV Venv Approach

Set up a virtual environment and install dependencies:

```bash
cd /home/ivanadamin/spawn-experiments/experiments/2.505.2-severed-branch-timing

# Create virtual environment with uv
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install jsonschema

# Or install from requirements files
uv pip install -r 1-immediate-implementation/requirements.txt
```

## Running the Demo

Once dependencies are installed:

```bash
# Make sure venv is activated
source .venv/bin/activate

# Run full demo with colors
python demo_2505_2.py

# Or run simple demo (no colors)
python simple_demo.py
```

## Expected Results

With dependencies installed:
- **Method 1 (Immediate)**: ✅ WORKING
- **Method 2 (Specification-driven)**: ✅ WORKING
- **Method 3 (TDD)**: ✅ WORKING
- **Method 4 (Adaptive TDD)**: ⚠️ Validates correctly but has exit code issue

## Clean Setup Command Sequence

```bash
cd /home/ivanadamin/spawn-experiments/experiments/2.505.2-severed-branch-timing
uv venv
source .venv/bin/activate
uv pip install jsonschema
python demo_2505_2.py
```

## Dependency Analysis

All 4 implementations correctly depend on the jsonschema library as specified in their requirements.txt files. This is expected behavior - the implementations are working correctly but need their dependencies installed to run.