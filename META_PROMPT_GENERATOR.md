# TDD in the AI Era: Spawn-Experiments System v2.0

**Purpose**: Generate four distinct prompting strategies to compare different software development approaches. Use this system to spawn experiments with prompts for separate remote agents working in parallel repositories.

**Quick Start**: Say "spawn-experiments" to generate prompts for a new methodology comparison study.

**Standard Approach**: Use parallel launch with Task tool for simultaneous execution of all four methods, followed by comprehensive experiment report generation.

**Version 2.0 Changes**: Updated terminology to avoid biasing AI agents with quality expectations. Uses neutral, professional language throughout.

**Important**: This framework tests the hypothesis that more sophisticated methodologies produce better results, but we must remain unbiased and open to results that may challenge this assumption. Future AI models may incorporate advanced practices into simpler approaches, or simpler methods may prove more effective in certain contexts.

## Instructions for Spawning Experiments

Generate four complete prompt sets for building a **[APPLICATION_TYPE]** using **[TECH_STACK]**.

**Usage**: When someone says "spawn-experiments", ask for APPLICATION_TYPE and TECH_STACK, then generate all four prompts below.

### IMPORTANT: Timing Measurement Requirements

**Automated Timing via File Timestamps** (Recommended): Use file creation timestamps to calculate precise development times:

**Implementation**:
- **Start Time**: First file created across all method directories
- **End Time**: Last file created in each method directory
- **Calculation**: `find [method-dir] -type f -exec stat -c "%y %n" {} \; | sort | tail -1`

**Commands for Timing Analysis**:
```bash
# Get experiment start time (earliest file across all methods)
find experiments/[experiment-name]/ -type f -exec stat -c "%y %n" {} \; | sort | head -1

# Get method completion times
find experiments/[experiment-name]/1-immediate-implementation/ -type f -exec stat -c "%y %n" {} \; | sort | tail -1
find experiments/[experiment-name]/2-specification-driven/ -type f -exec stat -c "%y %n" {} \; | sort | tail -1
find experiments/[experiment-name]/3-test-first-development/ -type f -exec stat -c "%y %n" {} \; | sort | tail -1
find experiments/[experiment-name]/4-validated-test-development/ -type f -exec stat -c "%y %n" {} \; | sort | tail -1
```

**Advantages**:
- Objective, reproducible timing without manual intervention
- No timing measurement overhead affecting development flow
- Precise to the second across all methods
- Eliminates human error in timing capture

**Legacy Manual Backup** (if file timestamps unavailable):
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

### For the Spawn-Experiments Command:
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
- **1-immediate-implementation/**: Method 1 implementation
- **2-specification-driven/**: Method 2 implementation
- **3-test-first-development/**: Method 3 implementation
- **4-validated-test-development/**: Method 4 implementation

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
mkdir 1-immediate-implementation 2-specification-driven 3-test-first-development 4-validated-test-development

# Initialize each method directory
cd 1-immediate-implementation && git init
cd ../2-specification-driven && git init
cd ../3-test-first-development && git init
cd ../4-validated-test-development && git init

# Launch each with its generated prompt
# Then compare results across all four methods
```

**Standard Experiment Flow** (Parallel Launch Method):
1. Create new sequentially numbered experiment folder (e.g., `/experiments/010-new-project`)
2. Generate all four prompts using this meta-prompt
3. Set up four method directories within the experiment folder
4. **Launch all four methods in parallel using Task tool** (recommended approach)
   - Use single message with four Task tool calls for simultaneous execution
   - Each agent works independently in its designated directory
   - Monitor progress across all four methods in real-time
5. Wait for all four agents to complete their implementations
6. **Generate comprehensive EXPERIMENT_REPORT.md** comparing all results
7. Analyze results objectively, noting both expected and unexpected outcomes

**Alternative Manual Flow** (Sequential Launch):
- Steps 1-3 same as above
- Launch four separate Claude Code sessions manually
- Navigate each to respective directories and paste corresponding prompts
- Compare results after all complete

This framework provides empirical data about different development approaches in the AI era, allowing for objective comparison of methodologies.

**Experiment Organization**:
- Each run gets a unique experiment folder with sequential numbering (001, 002, 003, etc.)
- All four methods for a single experiment are contained within that folder
- Easy to compare results across methods for the same application
- Historical experiments are preserved for future reference and analysis

**Experimental Bias Warning**:
⚠️ **Critical**: Avoid confirmation bias when interpreting results. While this framework tests whether sophisticated methodologies produce better outcomes, remain open to findings that challenge this assumption. Advanced AI models may naturally incorporate best practices into simpler approaches, making methodology distinctions less relevant. Document all results objectively, especially unexpected outcomes.

## Parallel Launch Implementation

### Using Task Tool for Simultaneous Execution

**Recommended Approach**: Use a single message with four Task tool calls to launch all methods simultaneously:

```bash
# Example parallel launch command structure
Task(subagent_type="general-purpose", description="Method 1 Direct Implementation",
     prompt="[Method 1 prompt] Important: Work in directory /path/to/experiment/1-immediate-implementation/")

Task(subagent_type="general-purpose", description="Method 2 Specification-First",
     prompt="[Method 2 prompt] Important: Work in directory /path/to/experiment/2-specification-driven/")

Task(subagent_type="general-purpose", description="Method 3 TDD Approach",
     prompt="[Method 3 prompt] Important: Work in directory /path/to/experiment/3-test-first-development/")

Task(subagent_type="general-purpose", description="Method 4 Enhanced TDD",
     prompt="[Method 4 prompt] Important: Work in directory /path/to/experiment/4-validated-test-development/")
```

### Benefits of Parallel Launch
- **Fair comparison**: All methods start simultaneously under identical conditions
- **Real-time monitoring**: Observe different approaches progressing in parallel
- **Time accuracy**: Precise timing comparison without scheduling variations
- **Resource utilization**: Maximum efficiency using available AI agent capacity
- **Presentation value**: Dramatic demonstration of methodology differences

## Post-Experiment Analysis

**REQUIRED**: After completing all four methods, create a comprehensive experiment report (`EXPERIMENT_REPORT.md`) in the main experiment folder that includes:

### Required Report Sections
- **Experiment Overview**: Objective, duration, technology stack, application type
- **Methodology Results**: Detailed analysis of each method's performance
- **Quantitative Analysis**: Development speed, feature completeness, code organization
- **Qualitative Insights**: Methodology-specific strengths and characteristics
- **Business Impact Analysis**: Time-to-market, maintainability, user experience
- **Unexpected Findings**: Document surprising or contradictory results
- **Context-Dependent Recommendations**: When to use each methodology
- **Risk Analysis**: Technical debt, requirements creep, over-engineering risks
- **Glossary**: Technical terms accessible to generalist programmers
- **Conclusion**: Key findings and implications for AI-assisted development

### Report Quality Standards
- Objective analysis avoiding confirmation bias
- Data-driven conclusions with specific metrics
- Practical recommendations for different contexts
- Documentation of methodological innovations discovered
- Clear language suitable for both technical and business audiences

## Publication Steps (Final Phase)

After completing the experiment report, perform these critical publication steps to maximize research impact:

### 1. Update Main README
Update the main `README.md` with a newspaper-style headline section featuring the latest experiment:

```markdown
## 📰 LATEST: [Catchy Headline About Key Finding]

**[Experiment XXX: Name](experiments/XXX-name/EXPERIMENT_REPORT.md)** *(Date)*

Brief, engaging summary of the most surprising or impactful finding. Include key metrics (e.g., "Method X achieved Y with 3X less code"). End with a clear verdict or takeaway. [Read the full report →](link)

📊 **[See All Experiment Results →](EXPERIMENT_INDEX.md)**
```

**Headline Writing Tips**:
- Lead with the surprising finding or winner
- Include concrete metrics (3X faster, 75% less code, etc.)
- Make it newsworthy and attention-grabbing
- Keep it factual but engaging

### 2. Update or Create Experiment Index
Maintain `EXPERIMENT_INDEX.md` as the central hub for all experiments:

**Required Sections**:
- **Latest Experiment** (prominently featured at top)
- **All Completed Experiments** (organized by tier)
- **Methodology Performance Summary** (aggregate metrics)
- **Trends and Insights** (emerging patterns)
- **Methodology Selection Guide** (practical recommendations)
- **Next Experiments** (roadmap)

### 3. Update Experiment Count
Update the total experiment count in README's Research Overview section.

### 4. Git Commit Message Format
When committing the experiment, use this format:
```
Experiment XXX: [Name] - [Key Finding]

- Method X: [result]
- Method Y: [result]
- Method Z: [result]
- Method W: [result]

Key insight: [main takeaway]
```

### 5. Social Sharing Preparation
If sharing results externally, prepare:
- **One-line summary**: The headline finding
- **Three bullet points**: Key methodology differences
- **Visual comparison**: Table or metrics summary
- **Link to full report**: For detailed analysis

### Why Publication Matters
These publication steps ensure:
- **Discoverability**: Visitors immediately see latest findings
- **Continuity**: Research builds on previous experiments
- **Accessibility**: Results are easy to navigate and understand
- **Impact**: Findings reach and influence the community
- **Scientific Record**: Proper documentation for replication

**Remember**: The goal is to make the research immediately valuable to practitioners while maintaining scientific rigor. A great experiment hidden in a directory helps no one!