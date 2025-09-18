# Gemini Shell Agent Experiment

This folder contains experimental tools for running TDD methodology experiments directly from the shell using Google's Gemini AI API.

## Purpose

This was an experimental approach to automate the methodology comparison process by scripting interactions with AI agents directly from the command line, rather than using interactive Claude sessions.

## Files

- **`setup_experiment.py`** - Automated experiment environment setup
  - Creates standardized directory structure for 4 methods
  - Generates method-specific prompt templates
  - Initializes git repositories for each approach
  - Uses neutral naming to prevent bias (method_a, method_b, etc.)

- **`validate_experiment.py`** - Results validation and analysis
  - Compares code quality metrics across methods
  - Validates adherence to methodology protocols
  - Generates standardized experiment reports

- **`run_experiment.sh`** - Shell orchestration script
  - Coordinates the full experiment lifecycle
  - Manages parallel execution of different methods
  - Collects timing and performance data

## Experimental Approach

This shell-based approach aimed to:
1. **Reduce human bias** by automating agent interactions
2. **Increase reproducibility** through scripted execution
3. **Enable batch processing** of multiple experiments
4. **Standardize data collection** across all methodology comparisons

## Current Status

This approach was exploratory and is not actively used. The main TDD demo uses interactive Claude sessions via the `spawn-experiments` workflow instead.

## Relationship to Main Project

While these tools aren't currently used, they represent an alternative automation approach that could be revisited for:
- Large-scale methodology studies
- Batch experiment processing
- API-based agent orchestration
- Reproducible research protocols

## Usage (Historical)

```bash
# Setup experiment for a todo app
python setup_experiment.py --app "todo-list" --tech "Python Flask"

# Run all four methods
./run_experiment.sh experiments/009-todo-list

# Validate results
python validate_experiment.py experiments/009-todo-list
```

**Note**: These scripts were designed for Gemini API integration but could be adapted for other AI providers.