#!/bin/bash

# Automated Experiment Runner for TDD in the AI Era
# Usage: ./run_experiment.sh <experiment-number> <experiment-name> <application-type> <tech-stack>
# Example: ./run_experiment.sh 003 calculator "calculator app" Python

set -e

EXPERIMENT_NUM=$1
EXPERIMENT_NAME=$2
APPLICATION_TYPE=$3
TECH_STACK=$4

if [ $# -ne 4 ]; then
    echo "Usage: $0 <experiment-number> <experiment-name> <application-type> <tech-stack>"
    echo "Example: $0 003 calculator \"calculator app\" Python"
    exit 1
fi

EXPERIMENT_DIR="experiments/${EXPERIMENT_NUM}-${EXPERIMENT_NAME}"
TIMING_LOG="${EXPERIMENT_DIR}/EXPERIMENT_TIMING.log"

echo "Starting TDD in AI Era Experiment ${EXPERIMENT_NUM}: ${EXPERIMENT_NAME}"
echo "Application Type: ${APPLICATION_TYPE}"
echo "Tech Stack: ${TECH_STACK}"
echo "Experiment Directory: ${EXPERIMENT_DIR}"

# Create experiment structure
mkdir -p "${EXPERIMENT_DIR}"/{1-naive-approach,2-spec-first,3-tdd-approach,4-enhanced-tdd}

# Initialize timing log
echo "=== TDD in AI Era Experiment Timing Log ===" > "${TIMING_LOG}"
echo "Experiment: ${EXPERIMENT_NUM}-${EXPERIMENT_NAME}" >> "${TIMING_LOG}"
echo "Application Type: ${APPLICATION_TYPE}" >> "${TIMING_LOG}"
echo "Tech Stack: ${TECH_STACK}" >> "${TIMING_LOG}"
echo "Started: $(date)" >> "${TIMING_LOG}"
echo "" >> "${TIMING_LOG}"

# Function to run a method with automatic timing
run_method() {
    local method_num=$1
    local method_name=$2
    local prompt_file=$3
    local working_dir="${EXPERIMENT_DIR}/${method_num}-${method_name}"

    echo "=== Method ${method_num}: ${method_name} ===" >> "${TIMING_LOG}"
    echo "Start Time: $(date)" >> "${TIMING_LOG}"

    # Create method-specific timing log
    local method_timing="${working_dir}/TIMING_LOG.txt"
    echo "Method ${method_num} Start: $(date)" > "${method_timing}"

    echo "Starting Method ${method_num}: ${method_name}"
    echo "Working Directory: ${working_dir}"

    # Here you would launch the Task tool with the appropriate prompt
    # For demonstration, we'll just create a placeholder
    echo "# Method ${method_num}: ${method_name}" > "${working_dir}/README.md"
    echo "Started: $(date)" >> "${working_dir}/README.md"
    echo "Application Type: ${APPLICATION_TYPE}" >> "${working_dir}/README.md"
    echo "Tech Stack: ${TECH_STACK}" >> "${working_dir}/README.md"

    # Simulate work time (replace with actual Task tool invocation)
    sleep 2

    echo "Method ${method_num} End: $(date)" >> "${method_timing}"
    echo "End Time: $(date)" >> "${TIMING_LOG}"
    echo "Status: Completed" >> "${TIMING_LOG}"
    echo "" >> "${TIMING_LOG}"

    echo "Completed Method ${method_num}: ${method_name}"
}

# Run all methods (in parallel if desired)
echo "Launching all four methods..."

run_method "1" "naive-approach" "method1.prompt" &
PID1=$!

run_method "2" "spec-first" "method2.prompt" &
PID2=$!

run_method "3" "tdd-approach" "method3.prompt" &
PID3=$!

run_method "4" "enhanced-tdd" "method4.prompt" &
PID4=$!

# Wait for all methods to complete
wait $PID1 $PID2 $PID3 $PID4

# Final timing
echo "=== Experiment Complete ===" >> "${TIMING_LOG}"
echo "Completion Time: $(date)" >> "${TIMING_LOG}"

echo ""
echo "Experiment ${EXPERIMENT_NUM}-${EXPERIMENT_NAME} completed!"
echo "Check ${TIMING_LOG} for detailed timing information"
echo "Method results are in their respective directories under ${EXPERIMENT_DIR}/"

# Generate summary report template
cat > "${EXPERIMENT_DIR}/EXPERIMENT_SUMMARY.md" << EOF
# Experiment ${EXPERIMENT_NUM}: ${EXPERIMENT_NAME}

**Application Type**: ${APPLICATION_TYPE}
**Tech Stack**: ${TECH_STACK}
**Date**: $(date)

## Method Results Summary

### Method 1: Naive Direct Approach
- Directory: \`1-naive-approach/\`
- Status: [TO BE FILLED]
- Key Findings: [TO BE FILLED]

### Method 2: Specification-First Approach
- Directory: \`2-spec-first/\`
- Status: [TO BE FILLED]
- Key Findings: [TO BE FILLED]

### Method 3: TDD Approach
- Directory: \`3-tdd-approach/\`
- Status: [TO BE FILLED]
- Key Findings: [TO BE FILLED]

### Method 4: Enhanced TDD
- Directory: \`4-enhanced-tdd/\`
- Status: [TO BE FILLED]
- Key Findings: [TO BE FILLED]

## Timing Analysis
See \`EXPERIMENT_TIMING.log\` for detailed timing data.

## Next Steps
1. Analyze implementation quality across all methods
2. Compare code metrics and test coverage
3. Document unexpected findings
4. Update comprehensive experiment report
EOF

echo "Summary template created at ${EXPERIMENT_DIR}/EXPERIMENT_SUMMARY.md"