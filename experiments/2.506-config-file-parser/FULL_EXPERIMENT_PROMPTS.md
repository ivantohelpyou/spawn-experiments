# Experiment 2.506: Configuration File Parser CLI - Full Prompts

## Experiment Protocol
**Three-Stage Checkpoint Approach:**
1. Initial implementation with library pause requirement
2. "Why?" follow-up to capture reasoning
3. "Ok go" to proceed with implementation

**APPLICATION_TYPE**: Configuration File Parser CLI
**TECH_STACK**: Python with multi-format support (YAML, JSON, INI, TOML)
**EXPERIMENT_NUMBER**: 2.506

---

## Method 1: Immediate Implementation

```
You are an AI assistant helping a developer create a configuration file parser CLI tool. The developer needs a working solution quickly.

IMPORTANT: Create a dedicated branch for your experiment:
git checkout -b exp-2506-immediate

Build a configuration file parser CLI that supports YAML, JSON, INI, and TOML formats.

Requirements:
- Parse config files in any of the four formats
- Auto-detect format based on file extension
- Convert between formats (e.g., yaml to json)
- Validate config structure
- Support nested configurations
- Pretty-print output
- Handle errors gracefully

Important: Before installing or using any external libraries, please pause and list what you plan to use.

LIBRARY CONSTRAINTS:
- Use well-established libraries only (>1000 GitHub stars or in standard library)
- Stick to parsing/config libraries (no web frameworks, ML libraries, etc.)
- Common choices: pyyaml, toml, configparser, json, dynaconf, omegaconf, pydantic
- Avoid exotic or unmaintained packages

LIBRARY INSTALLATION PROTOCOL:
When you proceed with external libraries:
1. Create a virtual environment: python -m venv venv
2. Activate it: source venv/bin/activate
3. Install your chosen libraries: pip install [libraries]
4. Generate requirements.txt: pip freeze > requirements.txt

REQUIRED FILE STRUCTURE:
experiments/2.506-config-file-parser/1-immediate-implementation/
├── config_parser.py (or your chosen name - place ALL files here)
├── test_*.py (if you create tests)
├── requirements.txt (if external libraries used)
└── README.md (brief implementation summary)

Start with the implementation right away, focusing on getting a working solution. Make practical decisions to deliver functionality quickly.

IMPORTANT: Checkpoint your progress with atomic git commits:
- git add -A && git commit -m "Impl: [what you built]"
- git add -A && git commit -m "Fix: [what you fixed]"
- git add -A && git commit -m "COMPLETE: Config parser with multi-format support"

Commit at least every 3 minutes or at major milestones.
```

---

## Method 2: Specification-Driven Development

```
You are an AI assistant helping a developer create a configuration file parser CLI tool. The developer values well-planned, professionally structured solutions.

IMPORTANT: Create a dedicated branch for your experiment:
git checkout -b exp-2506-specification

Build a configuration file parser CLI that supports YAML, JSON, INI, and TOML formats.

Requirements:
- Parse config files in any of the four formats
- Auto-detect format based on file extension
- Convert between formats (e.g., yaml to json)
- Validate config structure
- Support nested configurations
- Pretty-print output
- Handle errors gracefully

Important: Before installing or using any external libraries, please pause and list what you plan to use.

LIBRARY CONSTRAINTS:
- Use well-established libraries only (>1000 GitHub stars or in standard library)
- Stick to parsing/config libraries (no web frameworks, ML libraries, etc.)
- Common choices: pyyaml, toml, configparser, json, dynaconf, omegaconf, pydantic
- Avoid exotic or unmaintained packages

LIBRARY INSTALLATION PROTOCOL:
When you proceed with external libraries:
1. Create a virtual environment: python -m venv venv
2. Activate it: source venv/bin/activate
3. Install your chosen libraries: pip install [libraries]
4. Generate requirements.txt: pip freeze > requirements.txt

REQUIRED FILE STRUCTURE:
experiments/2.506-config-file-parser/2-specification-driven/
├── config_parser.py (or your chosen name - place ALL files here)
├── test_*.py (if you create tests)
├── requirements.txt (if external libraries used)
├── SPECIFICATION.md (your detailed design)
└── README.md (brief implementation summary)

Begin by analyzing the requirements and creating a comprehensive specification. Design the architecture before implementing. Document your design decisions and component structure.

IMPORTANT: Checkpoint your progress with atomic git commits:
- git add -A && git commit -m "Specs: [what you defined]"
- git add -A && git commit -m "Impl: [what you built]"
- git add -A && git commit -m "Test: [what you tested]"
- git add -A && git commit -m "COMPLETE: Specification-driven config parser"

Commit at least every 3 minutes or at major milestones.
```

---

## Method 3: Test-First Development (Pure TDD)

```
You are an AI assistant helping a developer create a configuration file parser CLI tool. The developer follows strict test-driven development practices.

IMPORTANT: Create a dedicated branch for your experiment:
git checkout -b exp-2506-tdd

Build a configuration file parser CLI that supports YAML, JSON, INI, and TOML formats.

Requirements:
- Parse config files in any of the four formats
- Auto-detect format based on file extension
- Convert between formats (e.g., yaml to json)
- Validate config structure
- Support nested configurations
- Pretty-print output
- Handle errors gracefully

Important: Before installing or using any external libraries, please pause and list what you plan to use.

LIBRARY CONSTRAINTS:
- Use well-established libraries only (>1000 GitHub stars or in standard library)
- Stick to parsing/config libraries (no web frameworks, ML libraries, etc.)
- Common choices: pyyaml, toml, configparser, json, dynaconf, omegaconf, pydantic
- Avoid exotic or unmaintained packages

LIBRARY INSTALLATION PROTOCOL:
When you proceed with external libraries:
1. Create a virtual environment: python -m venv venv
2. Activate it: source venv/bin/activate
3. Install your chosen libraries: pip install [libraries]
4. Generate requirements.txt: pip freeze > requirements.txt

REQUIRED FILE STRUCTURE:
experiments/2.506-config-file-parser/3-test-first-development/
├── config_parser.py (implementation after tests)
├── test_*.py (WRITE TESTS FIRST)
├── requirements.txt (if external libraries used)
└── README.md (brief TDD process summary)

Follow strict TDD methodology:
1. Write failing tests first for each requirement
2. Implement minimal code to pass tests
3. Refactor while keeping tests green
4. Repeat for each feature

Start with the simplest test case and build incrementally.

IMPORTANT: Checkpoint your progress with atomic git commits:
- git add -A && git commit -m "Test: [failing test for feature]"
- git add -A && git commit -m "Impl: [code to pass test]"
- git add -A && git commit -m "Refactor: [improvement made]"
- git add -A && git commit -m "COMPLETE: TDD config parser"

Commit after each red-green-refactor cycle.
```

---

## Method 4: Validated Test Development (V4.2 Adaptive TDD)

```
You are an AI assistant helping a developer create a configuration file parser CLI tool. The developer values both testing and strategic development using the V4.2 Adaptive TDD approach.

IMPORTANT: Create a dedicated branch for your experiment:
git checkout -b exp-2506-adaptive-tdd

Build a configuration file parser CLI that supports YAML, JSON, INI, and TOML formats.

Requirements:
- Parse config files in any of the four formats
- Auto-detect format based on file extension
- Convert between formats (e.g., yaml to json)
- Validate config structure
- Support nested configurations
- Pretty-print output
- Handle errors gracefully

Important: Before installing or using any external libraries, please pause and list what you plan to use.

LIBRARY CONSTRAINTS:
- Use well-established libraries only (>1000 GitHub stars or in standard library)
- Stick to parsing/config libraries (no web frameworks, ML libraries, etc.)
- Common choices: pyyaml, toml, configparser, json, dynaconf, omegaconf, pydantic
- Avoid exotic or unmaintained packages

LIBRARY INSTALLATION PROTOCOL:
When you proceed with external libraries:
1. Create a virtual environment: python -m venv venv
2. Activate it: source venv/bin/activate
3. Install your chosen libraries: pip install [libraries]
4. Generate requirements.txt: pip freeze > requirements.txt

REQUIRED FILE STRUCTURE:
experiments/2.506-config-file-parser/4-adaptive-tdd-v42/
├── config_parser.py (strategic implementation)
├── test_*.py (strategic test coverage)
├── requirements.txt (if external libraries used)
├── VALIDATION_STRATEGY.md (document your approach)
└── README.md (brief adaptive TDD summary)

Apply V4.2 Adaptive TDD methodology:
1. Assess complexity of each requirement
2. Write comprehensive tests for complex parsing logic
3. Apply strategic validation where it adds value
4. Balance thoroughness with development speed
5. Focus testing on format conversion accuracy and edge cases

Use your judgment to determine where testing provides maximum value.

IMPORTANT: Checkpoint your progress with atomic git commits:
- git add -A && git commit -m "Strategy: [validation approach]"
- git add -A && git commit -m "Test: [strategic test cases]"
- git add -A && git commit -m "Impl: [strategic implementation]"
- git add -A && git commit -m "Validate: [validation performed]"
- git add -A && git commit -m "COMPLETE: Adaptive TDD config parser"

Commit at strategic checkpoints based on complexity.
```

---

## Checkpoint Interaction Protocol

### Stage 2 Response (After Library List)
When each method lists their planned libraries, respond with:
```
Why?
```

### Stage 3 Response (After Explanation)
After they explain their reasoning, respond with:
```
Ok go
```

---

## Expected Checkpoint Patterns

### Method 1 Expected
**Stage 1:** "I'll use pyyaml, json (built-in), configparser (built-in), and toml"
**Stage 2 Response:** "They're common and will work quickly"
**Stage 3:** Proceeds with rapid implementation

### Method 2 Expected
**Stage 1:** "After analyzing requirements, I plan to use: [detailed library list with versions]"
**Stage 2 Response:** "Based on my specification analysis... [comprehensive reasoning]"
**Stage 3:** Proceeds with architected solution

### Method 3 Expected
**Stage 1:** "For TDD, I'll use pytest, pyyaml, toml, and configparser"
**Stage 2 Response:** "These libraries have good testing support and clear APIs"
**Stage 3:** Proceeds with test-first cycles

### Method 4 Expected
**Stage 1:** "Strategic selection: [balanced library choices]"
**Stage 2 Response:** "Balancing complexity, features, and maintainability..."
**Stage 3:** Proceeds with adaptive approach

---

## Post-Experiment Analysis

After all four methods complete:

1. **Library Selection Analysis**
   - Which libraries were chosen by each method?
   - Common selections vs unique choices
   - Standard library vs external preference

2. **Reasoning Pattern Analysis**
   - Depth of evaluation in Stage 2 responses
   - Criteria mentioned (popularity, testing, performance, etc.)
   - Methodology-specific reasoning patterns

3. **Architecture Comparison**
   - Unified vs separate parser implementations
   - Error handling approaches
   - Code organization patterns

4. **Create methodology_comparison_demo.py**
   - Show library choices side-by-side
   - Compare reasoning depth
   - Demonstrate architecture differences

---

## Integration Verification

After experiment completion:

```bash
# Verify all methods are properly structured
ls -la experiments/2.506-config-file-parser/*/config_parser.py

# Test each implementation
python experiments/2.506-config-file-parser/1-immediate-implementation/config_parser.py
python experiments/2.506-config-file-parser/2-specification-driven/config_parser.py
python experiments/2.506-config-file-parser/3-test-first-development/config_parser.py
python experiments/2.506-config-file-parser/4-adaptive-tdd-v42/config_parser.py
```