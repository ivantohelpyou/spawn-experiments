# Hierarchical Experiment Numbering System

## System Overview

**Format**: `T.DCC.V` where:
- **T** = Tier (1=Functions, 2=CLI Tools, 3=Applications, 4=Special Studies)
- **D** = Domain (see categories below)
- **CC** = Sequential number within domain (01, 02, 03...)
- **V** = Version (0=original, 1=first re-run, 2=second re-run, etc.)

## Research Domain Categories

### Tier 1: Functions (1.X)
- **1.1XX - String Processing**: Text manipulation, parsing, encoding
- **1.2XX - Mathematical Operations**: Number theory, calculations, conversions
- **1.3XX - Data Structures**: Algorithms for organizing and accessing data
- **1.4XX - Security & Cryptography**: Password generation, hashing, validation
- **1.5XX - Input Validation**: Pattern matching, format checking
- **1.9XX - Miscellaneous Functions**: Uncategorized algorithms

### Tier 2: CLI Tools (2.X)
- **2.1XX - Text Processing Tools**: Analysis, formatting, transformation
- **2.2XX - Development Tools**: Code analysis, build utilities, testing
- **2.3XX - System Utilities**: File management, monitoring, configuration
- **2.4XX - Data Tools**: Format conversion, parsing, validation
- **2.5XX - Security Tools**: Password management, encryption utilities
- **2.9XX - Miscellaneous Tools**: Uncategorized CLI applications

### Tier 3: Applications (3.X)
- **3.1XX - Productivity Apps**: Note-taking, task management, organization
- **3.2XX - Development Apps**: IDEs, dashboards, project management
- **3.3XX - System Apps**: Monitoring, administration, configuration
- **3.4XX - Data Apps**: Analysis, visualization, reporting
- **3.5XX - Security Apps**: Authentication, monitoring, audit tools
- **3.9XX - Miscellaneous Apps**: Uncategorized full applications

### Tier 4: Special Studies (4.X)
- **4.1XX - Methodology Comparisons**: Cross-tier analysis studies
- **4.2XX - Replication Studies**: Validation of previous experiments
- **4.3XX - Meta-Research**: Studies about the research process itself

## Versioning System

### Base Version (T.DCC.0)
The original implementation of an experiment using the current methodology framework.

### Re-run Versions (T.DCC.1, T.DCC.2, ...)
Subsequent versions for:
- **Methodology Evolution**: Testing improved prompts or frameworks
- **Validation Studies**: Confirming results with different conditions
- **Environmental Changes**: Re-running as AI capabilities improve
- **Bias Detection**: Multiple runs to check consistency
- **Replication Research**: Independent validation of findings

### Version Documentation
Each version should document:
- **Purpose**: Why this version was created
- **Changes**: What differs from previous version
- **Conditions**: Any environmental or methodological changes
- **Comparison**: Results compared to base version

### Examples
- `1.401.0` - Original password generator experiment
- `1.401.1` - Re-run with improved timing measurement protocol
- `1.401.2` - Validation study with different AI model
- `4.201.0` - Replication study of 1.401.0 results
- **4.4XX - Modification Matrix**: Studies of code evolution patterns
- **4.9XX - Miscellaneous Research**: Other research initiatives

## Current Experiment Mapping

| Legacy | New Number | Domain | Description |
|---------|------------|---------|-------------|
| 002 | 1.201 | Mathematical | Expression Evaluator |
| 006 | 1.203 | Mathematical | Simple Interest Calculator |
| 007 | 1.301 | Data Structures | LRU Cache with TTL (STOPPED) |
| 008 | 1.302 | Data Structures | LRU Cache with TTL |
| 009 | 2.101 | Text Processing | Multilingual Word Counter |
| 010 | 1.401 | Security/Crypto | Password Generator |
| 011 | 1.204 | Mathematical | Prime Number Generator |
| 012 | 1.101 | String Processing | Anagram Grouper |
| 013 | 1.205 | Mathematical | Roman Numeral Converter |
| 014 | 1.102 | String Processing | Balanced Parentheses |

## Benefits of Hierarchical System

1. **No renumbering needed** - infinite insertions possible (e.g., 1.115 between 1.101 and 1.204)
2. **Domain clustering** - related experiments grouped together
3. **Tier visibility** - complexity level immediately apparent
4. **Professional organization** - academic-style numbering
5. **Future extensibility** - supports sub-experiments (1.101.1, 1.101.2)

## Future Research Planning

### Immediate Tier 1 Extensions (1.5XX - Input Validation)
- **1.501** - Email Validator
- **1.502** - URL Validator
- **1.503** - File Path Validator
- **1.504** - Date Format Validator
- **1.505** - Phone Number Validator

### Tier 2 CLI Tools (Strategic Component Reuse)
- **2.501** - Password Manager CLI (reuses 1.401)
- **2.201** - Number Theory Calculator (reuses 1.204, 1.205)
- **2.102** - Text Analysis Tool (reuses 1.101, 1.102)
- **2.202** - Code Structure Validator (reuses 1.102)
- **2.401** - File Statistics Tool (baseline - minimal reuse)

### Tier 3 Applications
- **3.101** - Personal Knowledge Manager
- **3.201** - Project Dashboard
- **3.401** - Personal Finance Tracker
- **3.301** - System Monitor
- **3.102** - Document Processor

## Usage Guidelines

### For Documentation
- Always reference experiments by new number: "1.101 - Anagram Grouper"
- Include legacy number in parentheses for transition: "1.101 (012)"
- Use domain context: "String Processing experiment 1.101"

### For New Experiments
- Choose appropriate tier (1=Function, 2=Tool, 3=App)
- Select domain category (1.1XX=String, 1.2XX=Math, etc.)
- Use next available number in sequence
- Consider sub-experiments for variations (1.101.1, 1.101.2)

### For Component Discovery Research
- Numbers reveal natural reuse opportunities
- 2.XXX tools should discover relevant 1.XXX functions
- 3.XXX apps should discover both 1.XXX and 2.XXX components
- Track cross-tier component adoption patterns

## Implementation Notes

### Backward Compatibility
- Legacy directory names remain unchanged
- Documentation shows both numbers during transition
- All existing links continue working
- Gradual migration to new system

### Directory Structure
Current directories maintain legacy names with new number references in documentation:
```
experiments/
├── 012-anagram-grouper/     # Referenced as 1.101
├── 013-roman-numeral-converter/  # Referenced as 1.205
├── 014-balanced-parentheses/     # Referenced as 1.102
└── ...
```

Future experiments can use new naming:
```
experiments/
├── 1.501-email-validator/
├── 2.501-password-manager-cli/
└── 3.101-knowledge-manager/
```

This hierarchical system provides infinite extensibility while maintaining clear organization and professional presentation of the research framework.