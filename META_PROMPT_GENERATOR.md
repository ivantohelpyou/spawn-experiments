# TDD in the AI Era: Meta-Prompt Generator v2.0

**Purpose**: Generate four distinct prompting strategies to compare different software development approaches. Use this artifact to generate prompts for separate remote agents working in parallel repositories.

**Version 2.0 Changes**: Updated terminology to avoid biasing AI agents with quality expectations. Uses neutral, professional language throughout.

**Important**: This framework tests the hypothesis that more sophisticated methodologies produce better results, but we must remain unbiased and open to results that may challenge this assumption. Future AI models may incorporate advanced practices into simpler approaches, or simpler methods may prove more effective in certain contexts.

## Instructions for Prompt Generation

Generate four complete prompt sets for building a **[APPLICATION_TYPE]** using **[TECH_STACK]**.

### IMPORTANT: Timing Measurement Requirements

**Automated Timing**: The controlling agent will automatically record timestamps when launching each method agent and upon completion. No manual timestamp commands are required in the method prompts.

**Implementation**: Use the Task tool's natural timing capabilities combined with bash commands to capture:
- Method start time: Recorded when Task tool is invoked
- Method end time: Recorded when Task tool completes
- Phase transitions: Can be captured through intermediate agent reports

**Timing Data Storage**: All timing data will be automatically written to a `TIMING_LOG.txt` file in each method directory.

**Manual Backup** (if needed): Each method prompt may optionally include simple timing commands, but automation should be the primary approach:
```bash
echo "$(date): Starting implementation" >> TIMING_LOG.txt
echo "$(date): Implementation complete" >> TIMING_LOG.txt
```

---

## Method 1: Direct Implementation Approach

### Generate this prompt:
```
"Build a [APPLICATION_TYPE] using [TECH_STACK].

Make it fully functional with all the features you think it should have. Include a user interface and all necessary functionality."
```

**Research Interest**: How does this approach perform in terms of development speed, feature completeness, code quality, and maintainability?

---

## Method 2: Specification-First Implementation

### Generate this prompt:
```
"First, write comprehensive specifications for a [APPLICATION_TYPE], then build the complete application.

Phase 1 - Specifications:
- List all features and requirements
- Define user stories and use cases
- Outline the technical architecture
- Specify data models and relationships
- Document business rules and constraints

Phase 2 - Implementation:
- Build the application according to the specifications
- Include all specified features
- Use [TECH_STACK] as the technology stack
- Ensure the final product matches the specifications

Provide both the specifications document and the complete implementation."
```

**Research Interest**: How does upfront specification affect development time, implementation accuracy, and final code quality?

---

## Method 3: Test-Driven Implementation

### Generate this prompt:
```
"Create a [APPLICATION_TYPE] using Test-Driven Development principles. Follow this exact process:

PHASE 1 - SPECIFICATIONS:
Write detailed specifications including:
1. Core functional requirements
2. User stories with acceptance criteria
3. Technical architecture overview
4. Data models and relationships
5. API design (if applicable)
6. Business rules and validation requirements
7. Error handling and edge cases

PHASE 2 - TDD IMPLEMENTATION:
Using the specifications above, implement using strict TDD:

FOR EACH FEATURE:
1. **RED**: Write failing tests first
   - Unit tests for individual components
   - Integration tests for component interactions
   - Edge case and error condition tests
   - Tests should describe expected behavior clearly

2. **GREEN**: Write minimal implementation code
   - Only enough code to make tests pass
   - No additional functionality beyond what tests require

3. **REFACTOR**: Clean up code while keeping tests green
   - Improve structure and readability
   - Remove duplication
   - Maintain test coverage

STRICT RULES:
- NO implementation code before tests
- Tests must fail before writing implementation
- Each commit should follow Red-Green-Refactor cycle
- Start with simplest features first

Technology: [TECH_STACK]
Show your work: display tests, show them failing, then show implementation."
```

**Research Interest**: How does the TDD cycle affect code quality, development time, and confidence in correctness?

---

## Method 4: Test-Driven Implementation with Validation

### Generate this prompt:
```
"Create a [APPLICATION_TYPE] using Test-Driven Development with comprehensive test validation. Follow this rigorous process:

PHASE 1 - SPECIFICATIONS:
[Same as Method 3 - copy specification requirements]

PHASE 2 - TEST-DRIVEN DEVELOPMENT WITH VALIDATION:

FOR EACH FEATURE, FOLLOW THIS COMPREHENSIVE CYCLE:

1. **RED**: Write failing tests
   - Write comprehensive test cases first
   - Include unit, integration, and edge case tests
   - Make tests descriptive and behavior-focused

2. **TEST VALIDATION** (Critical Step):
   Before writing implementation, validate your tests:

   a) **Explain Each Test**:
      - What specific behavior does this test verify?
      - What would happen if the implementation was wrong?
      - Does this test actually test what it claims to test?

   b) **Test the Tests**:
      - Write obviously incorrect implementation that should fail
      - Verify tests catch common mistakes in this domain
      - Ensure tests fail for the RIGHT reasons
      - Example: If testing addition, ensure test fails when function does subtraction

   c) **Test Quality Checklist**:
      - Are assertions specific and meaningful?
      - Do tests cover positive AND negative scenarios?
      - Would these tests catch realistic bugs?
      - Are there obvious ways tests could pass incorrectly?

3. **GREEN**: Write correct implementation
   - Only after test validation passes
   - Write minimal code to make tests pass
   - Verify all tests pass for correct reasons

4. **REFACTOR**: Improve code quality
   - Clean up implementation while tests stay green
   - Ensure test suite remains robust

5. **QUALITY GATES**: Before moving to next feature
   - Run full test suite
   - Verify test coverage is appropriate
   - Confirm error handling works correctly
   - Validate integration points function properly

ENHANCED RULES:
- NEVER write implementation before test validation
- Always demonstrate test validation step
- Show incorrect implementation failing tests
- Explain why each test matters
- Start with absolute simplest feature

Technology: [TECH_STACK]
Show all work: failing tests, test validation, correct implementation, passing tests."
```

**Research Interest**: How does test validation affect development time, test effectiveness, and overall code reliability?

---

## Meta-Prompt Usage Instructions

### For the Coding Agent:
```
"Generate four separate, complete prompts based on the methods above for building a [APPLICATION_TYPE] using [TECH_STACK].

Each prompt should be:
1. Self-contained and complete
2. Ready to send to a separate remote agent
3. Tailored for the specific method's approach
4. Include all necessary context and instructions

Provide:
- Method 1 Prompt: [Complete prompt text]
- Method 2 Prompt: [Complete prompt text]
- Method 3 Prompt: [Complete prompt text]
- Method 4 Prompt: [Complete prompt text]

Each prompt should be copy-paste ready for launching separate development sessions."
```

### For Repository Setup:
Each experiment run creates a new folder in `/experiments` with sequential numbering in `nnn-<experiment-name>` format (e.g., `001-todo-app`, `002-expression-evaluator`, `003-calculator`, etc.). Use the next available number in sequence.

Within each experiment folder, create separate method directories:
- **1-naive-approach/**: Method 1 implementation
- **2-spec-first/**: Method 2 implementation
- **3-tdd-approach/**: Method 3 implementation
- **4-enhanced-tdd/**: Method 4 implementation

Each method directory contains:
- **README.md**: Method description and approach
- **Initial commit**: Empty project structure
- **Remote agent instructions**: The generated prompt
- **Success criteria**: How to evaluate the method's effectiveness

### Evaluation Metrics Across Methods:

**Code Quality**:
- Test coverage percentage
- Cyclomatic complexity
- Code duplication

**Functionality**:
- Feature completeness vs requirements
- Bug count in initial implementation
- Error handling robustness

**Development Process**:
- Time to first working version (measured with actual timestamps)
- Number of iterations needed
- Adherence to stated methodology

**Maintainability**:
- Code readability scores
- Documentation quality
- Ease of adding new features

---

## Example Usage:

```bash
# Terminal commands for demo setup (use next sequential number)
mkdir -p experiments/002-expression-evaluator
cd experiments/002-expression-evaluator

# Create four separate method directories
mkdir 1-naive-approach 2-spec-first 3-tdd-approach 4-enhanced-tdd

# Initialize each method directory
cd 1-naive-approach && git init
cd ../2-spec-first && git init
cd ../3-tdd-approach && git init
cd ../4-enhanced-tdd && git init

# Launch each with its generated prompt
# Then compare results across all four methods
```

**Demo Flow**:
1. Create new sequentially numbered experiment folder (e.g., `/experiments/002-expression-evaluator`)
2. Generate all four prompts using this meta-prompt
3. Set up four method directories within the experiment folder
4. Launch four parallel development sessions in their respective directories
5. Compare results in real-time during presentation
6. Create comprehensive experiment report with findings analysis
7. Analyze results objectively, noting both expected and unexpected outcomes

This framework provides empirical data about different development approaches in the AI era, allowing for objective comparison of methodologies.

**Experiment Organization**:
- Each run gets a unique experiment folder with sequential numbering (001, 002, 003, etc.)
- All four methods for a single experiment are contained within that folder
- Easy to compare results across methods for the same application
- Historical experiments are preserved for future reference and analysis

**Experimental Bias Warning**:
⚠️ **Critical**: Avoid confirmation bias when interpreting results. While this framework tests whether sophisticated methodologies produce better outcomes, remain open to findings that challenge this assumption. Advanced AI models may naturally incorporate best practices into simpler approaches, making methodology distinctions less relevant. Document all results objectively, especially unexpected outcomes.

**Post-Experiment Analysis**:
After completing all four methods, create a comprehensive experiment report (`EXPERIMENT_REPORT.md`) in the main experiment folder that includes:
- Development time comparison and analysis
- Code quality metrics across all methods
- Feature implementation comparison
- Software engineering insights and findings
- Risk analysis and business impact assessment
- Recommendations for different project types
- Categorized glossary of technical terms for generalist programmers
- Objective documentation of any unexpected or contradictory results