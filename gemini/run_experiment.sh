#!/bin/bash

# Rigorous, Anonymized Experiment Orchestration Script
#
# This script automates the setup for running the four development methodology trials
# according to the final, fully-anonymized protocol. It ensures that the agent
# remains completely "blind" to the experimental conditions.

set -e

# --- Configuration ---
EXPERIMENTS_DIR="experiments"
METHODOLOGIES=(
    "method-1-naive"
    "method-2-spec-first"
    "method-3-tdd"
    "method-4-enhanced-tdd"
)
ANON_DIRS=(
    "trial-A"
    "trial-B"
    "trial-C"
    "trial-D"
)

# --- Prompt Templates (as direct, unbiased instructions) ---

read -r -d '' NAIVE_PROMPT_TEMPLATE <<'EOF'
You are a senior software engineer.

Your task is to build the following application. Focus on getting a working version done as quickly as possible.

Here are the specifications:
---
%s
EOF

read -r -d '' SPEC_FIRST_PROMPT_TEMPLATE <<'EOF'
You are a senior software engineer.

Your task is to build the following application.

Please follow this exact process:
1.  First, write detailed technical specifications for all components of the application.
2.  After you have written the specifications, design the application's architecture and interfaces.
3.  Finally, implement the application according to your own specifications. Ensure your implementation includes robust validation and error handling.

Here are the high-level requirements:
---
%s
EOF

read -r -d '' TDD_PROMPT_TEMPLATE <<'EOF'
You are a senior software engineer who is a strict advocate for Test-Driven Development (TDD).

Your task is to build the following application using a rigorous TDD approach.

Please follow this exact process for every feature:
1.  Write a single failing test (RED).
2.  Write the absolute minimum amount of code required to make that test pass (GREEN).
3.  Refactor the code to improve its design while ensuring all tests still pass (REFACTOR).
4.  Repeat the cycle for the next feature.

Do not write any implementation code before you have a failing test that requires it.

Here are the high-level requirements:
---
%s
EOF

read -r -d '' ENHANCED_TDD_PROMPT_TEMPLATE <<'EOF'
You are a senior software engineer who is an expert in high-assurance systems and Test-Driven Development (TDD).

Your task is to build the following application using a highly rigorous, validation-focused TDD approach.

Please follow this exact process for every feature:
1.  Write a single failing test (RED).
2.  **VALIDATE THE TEST**: Briefly explain why the test is failing. Manually run it to ensure it fails as expected.
3.  Write the absolute minimum amount of code required to make the test pass (GREEN).
4.  **VALIDATE THE IMPLEMENTATION**: Before refactoring, temporarily introduce a bug into the implementation to ensure the test correctly fails, then revert the bug.
5.  Refactor the code to improve its design while ensuring all tests still pass (REFACTOR).
6.  Repeat the cycle for the next feature.

Your primary focus is on the correctness and quality of your tests.

Here are the high-level requirements:
---
%s
EOF

PROMPT_TEMPLATES=(
    "$NAIVE_PROMPT_TEMPLATE"
    "$SPEC_FIRST_PROMPT_TEMPLATE"
    "$TDD_PROMPT_TEMPLATE"
    "$ENHANCED_TDD_PROMPT_TEMPLATE"
)

# --- Script Logic ---

# 1. Validate Input
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <experiment_dir_name> <path_to_specs_file>"
    echo "Example: $0 004-todo-app-react specs/todo-app.md"
    exit 1
fi

EXPERIMENT_NAME=$1
SPECS_FILE=$2

if [ ! -f "$SPECS_FILE" ]; then
    echo "Error: Specifications file not found at '$SPECS_FILE'"
    exit 1
fi

# 2. Create Directories
# Note: The script is in /gemini, so paths are relative to the project root.
PROJECT_ROOT=".."
FULL_EXPERIMENT_DIR="${PROJECT_ROOT}/${EXPERIMENTS_DIR}/${EXPERIMENT_NAME}"
echo "Creating new experiment directory: ${FULL_EXPERIMENT_DIR}"
mkdir -p "$FULL_EXPERIMENT_DIR"

# 3. Randomize and Map Methodologies
# Using `shuf` for randomization. The `-i` flag specifies a range.
RANDOM_INDICES=$(shuf -i 0-3)
MANIFEST="{"

# 4. Read Specs and Generate Prompts in Anonymized Dirs
i=0
for ANON_DIR in "${ANON_DIRS[@]}"; do
    # Get the randomly assigned methodology for this trial
    METHOD_INDEX=$(echo "$RANDOM_INDICES" | sed -n "$((i+1))p")
    METHODOLOGY="${METHODOLOGIES[$METHOD_INDEX]}"
    TEMPLATE="${PROMPT_TEMPLATES[$METHOD_INDEX]}"

    TRIAL_DIR="${FULL_EXPERIMENT_DIR}/${ANON_DIR}"
    PROMPT_FILE="${TRIAL_DIR}/PROMPT.md"

    echo "  -> Creating directory and prompt for ${ANON_DIR} (mapped to ${METHODOLOGY})"
    mkdir -p "$TRIAL_DIR"
    
    SPECS_CONTENT=$(cat "$SPECS_FILE")
    printf "$TEMPLATE" "$SPECS_CONTENT" > "$PROMPT_FILE"

    # Add to manifest
    if [ $i -gt 0 ]; then
        MANIFEST=", ${MANIFEST}"
    fi
    MANIFEST="${MANIFEST}\n  \"${ANON_DIR}\": \"${METHODOLOGY}\""

    i=$((i+1))
done

MANIFEST="${MANIFEST}\n}"
MANIFEST_FILE="${FULL_EXPERIMENT_DIR}/manifest.json"
echo -e "$MANIFEST" > "$MANIFEST_FILE"
echo "  -> Created manifest.json for investigator."

# 5. Print Execution Instructions
ABSOLUTE_PATH=$(cd "$FULL_EXPERIMENT_DIR" && pwd)
echo ""
echo "✅ Experiment setup complete for '${EXPERIMENT_NAME}'."

echo ""
echo "---"
echo "🔴 CRITICAL PROTOCOL: To ensure scientific validity, you must run each of the following trials in a separate, new, and independent chat session. The agent must be kept blind to the experimental context."
echo "---"

echo ""
echo "Execution Instructions:"

for ANON_DIR in "${ANON_DIRS[@]}"; do
    echo "--- Trial: ${ANON_DIR} ---"
    echo "1. Start a new, clean chat session with the agent."
    echo "2. Give the agent this EXACT initial instruction (copy and paste):
"
    echo "   Your only authorized working directory for this session is ${ABSOLUTE_PATH}/${ANON_DIR}. You must not, under any circumstances, access any file or directory outside of this path. Your entire task is contained within this directory. Start by reading the PROMPT.md file and follow the instructions within it."
    echo ""
done

echo "Happy experimenting!"
