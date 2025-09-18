# Tier 2: Tool-Level Experiments (Walk)

## Experiment Design Philosophy

**Scope**: CLI tools, file processing, composable utilities
**Goal**: Study methodology impact on tool design and user interface decisions
**Duration**: 15-30 minutes per approach
**Output**: Usable command-line tool with file I/O

## Constraint Profile

### Technical Constraints
- **Interface**: Command-line tool (argparse/click)
- **I/O**: File input/output, stdin/stdout support
- **Dependencies**: Standard library + common CLI libraries (argparse, pathlib)
- **Structure**: Multi-module if beneficial, single executable entry point
- **Installation**: `python tool.py` or simple `pip install -e .`

### Specification Format
```
"Build a CLI tool `toolname` that processes [input type] and outputs [output type].
Tool should behave like standard Unix utilities (wc, grep, sort, etc.).
Support file arguments and stdin/stdout. Include --help and error handling."
```

## Experiment List

### 020: Text Statistics Tool (wc-like)
**Tool**: `textstats filename.txt` or `cat file | textstats`
**Requirement**: Count lines, words, characters, paragraphs. Support --lines, --words, --chars flags
**Expected Output**: `  23  145  892 filename.txt` (lines words chars)
**Building On**: Tier 1 word frequency functions
**Complexity**: CLI argument parsing, file handling, output formatting

### 021: Log Parser Tool (grep-like)
**Tool**: `logparse --pattern ERROR --since "2023-01-01" logfile.txt`
**Requirement**: Filter log entries by pattern, date range, severity level
**Expected Output**: Matching log lines with optional timestamps
**Building On**: Tier 1 pattern matching, text processing
**Complexity**: Date parsing, regex handling, streaming large files

### 022: Data Formatter Tool (column-like)
**Tool**: `formatter --input csv --output table data.csv`
**Requirement**: Convert between CSV, TSV, JSON, fixed-width table formats
**Expected Output**: Pretty-printed tables or structured data
**Building On**: Tier 1 text parsing, data structures
**Complexity**: Format detection, alignment algorithms, data validation

### 023: File Deduplicator (uniq-like)
**Tool**: `dedup --method hash --recursive ./directory`
**Requirement**: Find and optionally remove duplicate files by content or name
**Expected Output**: List of duplicate groups with sizes/paths
**Building On**: Tier 1 hashing, comparison algorithms
**Complexity**: File system traversal, hash computation, user confirmation

### 024: Configuration Merger
**Tool**: `confmerge base.json override.json --output merged.json`
**Requirement**: Merge configuration files (JSON/YAML) with conflict resolution
**Expected Output**: Merged configuration file with merge strategies
**Building On**: Tier 1 data structure manipulation
**Complexity**: Deep merging, conflict detection, format support

### 025: Backup Tool
**Tool**: `backup --source ./data --dest ./backup --incremental`
**Requirement**: Create file backups with incremental/differential options
**Expected Output**: Backup archive with manifest of changes
**Building On**: Tier 1 file comparison, hashing
**Complexity**: Change detection, archive creation, restoration

### 026: Password Generator
**Tool**: `passgen --length 16 --rules "upper,lower,digit,symbol" --count 5`
**Requirement**: Generate secure passwords with customizable rules
**Expected Output**: List of passwords meeting specified criteria
**Building On**: Tier 1 random generation, validation
**Complexity**: Character set management, entropy calculation, rule validation

### 027: Code Metrics Tool
**Tool**: `codemetrics --lang python --recursive ./src`
**Requirement**: Analyze code files for lines, complexity, functions, classes
**Expected Output**: Metrics report by file/directory with totals
**Building On**: Tier 1 text parsing, counting algorithms
**Complexity**: Language-specific parsing, metric calculation, reporting

### 028: Network Tester
**Tool**: `nettest --host google.com --port 80,443 --timeout 5`
**Requirement**: Test network connectivity, port accessibility, response times
**Expected Output**: Connection status, latency, success/failure counts
**Building On**: Tier 1 timing, validation functions
**Complexity**: Socket programming, timeout handling, parallel checking

### 029: Directory Organizer
**Tool**: `organize --rules rules.json --dry-run ./downloads`
**Requirement**: Organize files into directories based on customizable rules
**Expected Output**: File movement plan or actual reorganization
**Building On**: Tier 1 pattern matching, classification
**Complexity**: Rule parsing, file type detection, safe operations

## Generative Architecture Integration

### Building Block Reuse
Each tool may leverage functions from Tier 1:
```python
from experiments.010_palindrome.solution import is_palindrome
from experiments.016_word_counter.solution import count_words
```

### Methodology Questions
1. **Composition Patterns**: How do methodologies approach building on existing functions?
2. **Interface Design**: What CLI patterns emerge from different approaches?
3. **Error Handling**: How do methodologies handle file I/O and user errors?
4. **Testing Strategies**: How do approaches test CLI tools vs pure functions?

## Expected Methodology Patterns

### Immediate Implementation
- Quick CLI wrapper around core logic
- Basic argument parsing
- Minimal error handling
- Direct file operations

### Specification-Driven
- Detailed CLI specification first
- Comprehensive argument validation
- Structured error messages
- Modular design for testability

### Test-First Development
- CLI tests using subprocess/mock
- Incremental feature building
- File I/O mocking strategies
- User experience testing

### Validated Test Development
- Wrong CLI design validation
- User error scenario testing
- Performance validation with large files
- Cross-platform compatibility testing

## Success Metrics

### Tool Quality
- Correctness with various inputs
- Performance with large files
- Error handling and user feedback
- Unix-like behavior conformance

### User Experience
- Intuitive command-line interface
- Helpful error messages
- Consistent output formatting
- Documentation quality

### Development Process
- Time to usable tool
- Testing coverage of CLI paths
- Handling of edge cases
- Code organization quality

## Validation Protocol

### Tool Requirements
- Must work as standalone CLI tool
- Must handle files and stdin/stdout
- Must provide useful error messages
- Must include --help documentation

### Testing Standards
- Automated tests for core functionality
- CLI integration tests
- Error condition testing
- Performance verification with representative data

## Research Questions

1. **Architecture Emergence**: How do methodologies naturally structure CLI tools?
2. **User Interface Decisions**: What CLI patterns do different approaches favor?
3. **Error Handling Philosophy**: How do approaches differ in user error management?
4. **Reusability**: How effectively do approaches leverage Tier 1 building blocks?
5. **Testing Complexity**: How do methodologies handle the complexity of testing CLI tools?

## Progression to Tier 3

These CLI tools become **system components** for Tier 3 applications:
- Tools can be orchestrated into workflows
- Proven interfaces can be elevated to APIs
- CLI patterns can inform GUI design
- Performance characteristics guide system architecture

**Next Phase**: Tier 3 experiments combine these tools into full applications with GUIs, APIs, and complex user workflows.