# Hierarchical Experiment Numbering System

## System Overview

**Format**: `T.DCC` where:
- **T** = Tier (1=Functions, 2=CLI Tools, 3=Applications, 4=Special Studies)
- **D** = Domain (see categories below)
- **CC** = Sequential number within domain (01, 02, 03...)

## Domain Categories (Dewey-Inspired)

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
- **4.4XX - Modification Matrix**: Studies of code evolution patterns
- **4.9XX - Miscellaneous Research**: Other research initiatives

## Legacy Mapping Table

| Current | New Number | Domain | Description |
|---------|------------|---------|-------------|
| 001 | 3.501 | Security Apps | Unicode Password Manager |
| 002 | 1.201 | Mathematical | Expression Evaluator |
| 004 | 4.201 | Replication | Expression Evaluator Pytest (STOPPED) |
| 005 | 1.202 | Mathematical | Temperature Converter |
| 006 | 1.203 | Mathematical | Simple Interest Calculator |
| 007 | 1.301 | Data Structures | LRU Cache with TTL (STOPPED) |
| 008 | 1.302 | Data Structures | LRU Cache with TTL |
| 009 | 2.101 | Text Processing | Multilingual Word Counter |
| 010 | 1.401 | Security/Crypto | Password Generator |
| 011 | 1.204 | Mathematical | Prime Number Generator |
| 012 | 1.101 | String Processing | Anagram Grouper |
| 013 | 1.205 | Mathematical | Roman Numeral Converter |
| 014 | 1.102 | String Processing | Balanced Parentheses |

## Future Experiment Planning

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
- **2.202** - Code Validator (reuses 1.102)
- **2.502** - Cipher Tool (reuses 1.401, 1.205)

### Tier 3 Applications
- **3.101** - Personal Knowledge Manager
- **3.201** - Project Dashboard
- **3.401** - Personal Finance Tracker
- **3.301** - System Monitor
- **3.102** - Document Processor

## Implementation Notes

### Backward Compatibility
- Keep existing directory names as-is initially
- Add symlinks with new names pointing to old directories
- Update all documentation to reference new numbers
- Eventually migrate directory names (Phase 2)

### Directory Structure
```
experiments/
├── 1.101-anagram-grouper/           # New name
│   └── [existing structure]
├── 012-anagram-grouper/             # Old name (symlink to above)
├── 1.102-balanced-parentheses/      # New name
├── 014-balanced-parentheses/        # Old name (symlink to above)
└── ...
```

### Benefits of New System
1. **No renumbering needed** - infinite insertions possible
2. **Domain clustering** - related experiments grouped together
3. **Tier visibility** - complexity level immediately apparent
4. **Professional organization** - academic-style numbering
5. **Future extensibility** - supports sub-experiments (1.101.1, 1.101.2)

## Migration Strategy

### Phase 1: Documentation Update (Immediate)
- Update all markdown files to use new numbers
- Create this mapping document
- Update README, roadmap, experiment index

### Phase 2: Directory Migration (Future)
- Create new directory names
- Move content to new directories
- Update symlinks for backward compatibility
- Update any hardcoded paths

### Phase 3: Legacy Cleanup (Long-term)
- Remove old symlinks after transition period
- Archive legacy references
- Full adoption of new system