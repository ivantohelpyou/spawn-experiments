# Experiment 2.506: Configuration File Parser CLI

## Checkpoint Protocol
This experiment uses a three-stage checkpoint approach to capture natural library selection patterns:
1. Initial prompt with pause requirement
2. "Why?" follow-up
3. "Ok go" to proceed

---

## Base Prompt (All Methods)

```
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
```

## Follow-up Interactions

**Stage 2 (after they list libraries):**
```
Why?
```

**Stage 3 (after explanation):**
```
Ok go
```

---

## Method-Specific Prompts

### Method 1: Immediate Implementation
```
You are an AI assistant helping a developer build a configuration file parser CLI tool. The developer needs a working implementation quickly.

[BASE PROMPT]

Start with the implementation right away, focusing on getting a working solution. Make practical decisions to deliver functionality quickly.
```

### Method 2: Specification-Driven Development
```
You are an AI assistant helping a developer build a configuration file parser CLI tool. The developer values well-planned, professionally structured solutions.

[BASE PROMPT]

Begin by analyzing the requirements and creating a comprehensive specification. Design the architecture before implementing.
```

### Method 3: Test-First Development
```
You are an AI assistant helping a developer build a configuration file parser CLI tool. The developer follows test-driven development practices.

[BASE PROMPT]

Follow strict TDD methodology:
1. Write failing tests first
2. Implement minimal code to pass
3. Refactor while keeping tests green
4. Repeat for each feature
```

### Method 4: Validated Test Development (V4.2 Adaptive)
```
You are an AI assistant helping a developer build a configuration file parser CLI tool. The developer values both testing and strategic development.

[BASE PROMPT]

Apply adaptive TDD methodology:
1. Assess complexity of each requirement
2. Write comprehensive tests for complex logic
3. Apply strategic validation where it adds value
4. Balance thoroughness with development speed
```

---

## Research Focus Points

### Library Selection Patterns
- Which libraries are chosen first?
- Standard library vs external preference
- Single multi-format library vs multiple specific libraries

### Evaluation Criteria (Stage 2 responses)
- Popularity/community size
- Performance considerations
- API design/ease of use
- Testing support
- Documentation quality
- Dependency weight

### Architecture Decisions
- Unified parser interface vs format-specific parsers
- Factory pattern vs strategy pattern vs simple switching
- Error handling approach across formats
- Configuration validation strategy

### Expected Methodology Differences

**Method 1:**
- Quick selection of first viable option
- Minimal evaluation
- "They're popular" or "They work" reasoning

**Method 2:**
- Comprehensive library comparison
- Detailed trade-off analysis
- Architecture-driven selection

**Method 3:**
- Test-friendly library preference
- Mock-ability considerations
- "Good test support" reasoning

**Method 4:**
- Strategic evaluation
- Balance of simplicity and capability
- "Appropriate for requirements" reasoning

---

## Success Metrics
- Time to library selection
- Depth of evaluation (Stage 2 response)
- Architecture quality
- Code organization
- Error handling robustness
- Test coverage (Methods 3 & 4)
- Format conversion accuracy