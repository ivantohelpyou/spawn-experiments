# Future Experiments Roadmap - Hierarchical System (T.DCC)

> **LATEST**: Experiment 010-password-generator completed with 4-method comparison
> **Results**: Method timing validated - 1m17s (immediate) to 9m20s (validated TDD)

> **NEW**: Reorganized with hierarchical numbering system (T.DCC format)
> See [EXPERIMENT_NUMBERING_SYSTEM.md](EXPERIMENT_NUMBERING_SYSTEM.md) for complete mapping

## Current Status

### Completed Experiments (New Numbering)
1. **1.201** - Expression Evaluator (Math/Parsing) - 35 min total
2. **1.203** - Simple Interest Calculator (Basic Math/CLI) - Smoke test
3. **1.301** - LRU Cache with TTL (Data Structures) - ❌ **STOPPED** - Methods 3&4 hit token limits, incomplete
4. **1.302** - LRU Cache with TTL (Data Structures/Performance) - ✅ **COMPLETE** - 6-13 min per method, successful parallel execution
5. **2.101** - Multilingual Word Counter (Text Processing/I18N) - ⚠️ **BIAS VIOLATION** - needs rerun per protocols
6. **1.401** - Password Generator (Security/Crypto) - ✅ **COMPLETE** - Tier 1 validation
7. **1.204** - Prime Number Generator (Mathematical) - ✅ **COMPLETE** - methodology comparison successful
8. **1.101** - Anagram Grouper (String Processing) - ✅ **COMPLETE** - TDD won with 3X less code
9. **1.205** - Roman Numeral Converter (Mathematical) - ✅ **COMPLETE** - fastest TDD at 3m 37s
10. **1.102** - Balanced Parentheses (String Processing) - ✅ **COMPLETE** - Tier 1 series concluded

*Legacy numbers: 002→1.201, 006→1.203, 007→1.301, 008→1.302, 009→2.101, 010→1.401, 011→1.204, 012→1.101, 013→1.205, 014→1.102*

### Key Insights Discovered
- **Time Convergence**: Most methods complete in 8-14 minutes regardless of approach
- **Parallel Launch Success**: Simultaneous execution proven feasible (009)
- **Resource Constraints Impact**: Token limits significantly affected Methods 3&4 in 007
- **TDD Efficiency on Simple Problems**: Methods 3&4 produce cleaner, more efficient code for Tier 1 algorithms
- **Specification Explosion Risk**: Method 2 over-engineers simple problems (012: 1,440 vs 401 lines)
- **Test Validation Innovation**: Method 4's test validation methodology catches subtle bugs early
- **Methodology Selection Context-Dependent**: Different approaches optimal for different complexity tiers
- **AI Resource Usage Patterns**: TDD approaches require more tool interactions (54 vs 29 in 007)

## New Experimental Framework: Three-Tier System

Based on lessons learned, future experiments follow a **crawl-walk-run** progression:

### **Tier 1: Functions (010-019) - CRAWL**
**Scope**: Pure algorithmic problems, single functions, stdlib only
**Duration**: 5-15 minutes per approach (30-60 min total parallel)
**Claude Code Usage**: ✅ **Safe for any usage window**
**Purpose**: Isolate methodology differences without architectural complexity
**Status**: ✅ **COMPLETE** - Series 010-014 finished

#### Completed Tier 1 Experiments
- **1.401 - Password Generator**: ✅ Cryptographic randomness, character set manipulation
- **1.204 - Prime Number Generator**: ✅ Algorithm choice and optimization
- **1.101 - Anagram Grouper**: ✅ Hash key strategy and grouping logic - **TDD Winner**
- **1.205 - Roman Numeral Converter**: ✅ Mapping strategy and edge cases - **Fastest TDD**
- **1.102 - Balanced Parentheses**: ✅ Stack management and character matching

#### Planned Tier 1 Extensions - Input Validation Domain (1.5XX)
**Purpose**: Bridge gap between pure algorithms and CLI tools for better composability
- **1.501 - Email Validator**: Email address format validation
- **1.502 - URL Validator**: URL format and accessibility validation
- **1.503 - File Path Validator**: Path format and existence validation
- **1.504 - Date Format Validator**: Date parsing and validation patterns
- **1.505 - Phone Number Validator**: International phone number formats

### **Tier 2: CLI Tools (020-029) - WALK**
**Scope**: Command-line utilities, file I/O, composable tools
**Duration**: 15-30 minutes per approach (60-120 min total parallel)
**Claude Code Usage**: ⚠️ **Requires >2 hours remaining** (based on 007 resource analysis)
**Purpose**: Study interface design and component composition
**Components Available**: Discoverable functions from Tier 1 (010-014)
**Innovation**: Component discovery research - natural reuse vs. rebuild patterns

#### Planned Tier 2 Experiments (Strategic Component Alignment)
- **2.501 - Password Manager CLI**: Natural reuse of 1.401 password generation
- **2.201 - Number Theory Calculator**: Strategic reuse of 1.204 primes, 1.205 numerals
- **2.102 - Text Analysis Tool**: Natural reuse of 1.101 anagram grouping
- **2.202 - Code Structure Validator**: Strategic reuse of 1.102 parentheses matching
- **2.401 - File Statistics Tool**: Pure CLI tool with minimal component dependencies (baseline)

#### Component Discovery Research Framework
**Key Questions**: Which methodologies naturally discover and reuse existing components?
**Measurement**: Discovery rates, reuse depth, integration strategies by methodology
**Environment**: Components placed in discoverable locations without explicit guidance

### **Tier 3: Applications (030-039) - RUN**
**Scope**: Full applications with GUIs, APIs, persistence
**Duration**: 45-90 minutes per approach (180-360 min total parallel)
**Claude Code Usage**: ❌ **Requires >4 hours remaining** (based on 007 token analysis)
**Purpose**: Study complex system architecture and integration
**Components Available**: Functions (Tier 1) + Tools (Tier 2) discoverable
**Resource Planning**: Account for higher tool usage in Methods 3&4 (up to 54 interactions vs 29)

#### Planned Tier 3 Experiments
- **3.101 - Personal Knowledge Manager**: Note-taking with search and tagging
- **3.201 - Project Dashboard**: Development metrics and build monitoring
- **3.401 - Personal Finance Tracker**: Expense tracking with budgets and reports
- **3.301 - System Monitor**: Resource monitoring with alerts and history
- **3.102 - Document Processor**: Batch format conversion and workflow automation

## Discovered Components Research

### Key Innovation
Study **organic component discovery** patterns without explicit guidance:
- Components placed in `./utils/functions/` and `./utils/tools/`
- No mention in experiment prompts
- Natural exploration and reuse decisions measured
- Authentic development environment simulation

### Research Questions
1. **Discovery Patterns**: Which methodologies naturally explore existing codebases?
2. **Evaluation Criteria**: How do approaches assess found components for fitness?
3. **Integration Strategies**: What drives reuse vs. rebuild decisions?
4. **Architecture Influence**: How does component availability affect system design?

## Experimental Improvements

### Bias Prevention
- **Neutral naming enforced**: 1-immediate-implementation, 2-specification-driven, etc.
- **Language monitoring**: No quality indicators (naive/advanced/optimal)
- **Pre-experiment confirmation**: User validates bias-neutral setup
- **Post-experiment reporting**: Standard testing instructions with warnings

### Quality Improvements
- **Testing warnings**: Flag slow dependencies (pandas, heavy ML libs)
- **Quick test paths**: Always identify fast validation approach
- **Protocol compliance**: Transparent documentation of any violations
- **Reproducibility**: Clear instructions for result validation

## Priority Execution Plan

### Phase 1: Tier 1 Foundation (Next 2-3 months)
Execute experiments 010-014 to build function library and establish baseline methodology patterns.

### Phase 2: Tier 2 Composition (Following 2-3 months)
Execute experiments 020-024 to study tool composition and interface design with available function components.

### Phase 3: Tier 3 Integration (Final phase)
Execute experiments 030-034 to analyze complex system architecture with full component ecosystem.

## Success Metrics

### Quantitative
- **Component reuse rates** across methodologies and tiers
- **Development speed** with and without available components
- **Quality metrics** (correctness, test coverage, maintainability)
- **Architecture complexity** measures

### Qualitative
- **Natural discovery patterns** for existing components
- **Integration strategy differences** between methodologies
- **Methodology consistency** across complexity tiers
- **Realistic development behavior** patterns

## Expected Outcomes

1. **Methodology Scaling**: How approaches adapt across complexity levels
2. **Component Utilization**: Which methodologies naturally leverage existing work
3. **Architecture Emergence**: What design patterns emerge from generative development
4. **Development Efficiency**: Cumulative benefits of building block availability

This tiered approach addresses the scope ambiguity problem while providing unprecedented insight into realistic development scenarios with existing codebases.

## Future Organizational Improvements

### Hierarchical Numbering System (Proposed)
**Problem**: Current sequential numbering (010, 011, 012...) requires renumbering when inserting experiments
**Solution**: Dewey Decimal-inspired system allowing infinite extensions without renumbering

#### Proposed Structure
- **Tier 1 Functions**: 1.001, 1.002, 1.003, etc.
- **Tier 2 CLI Tools**: 2.001, 2.002, 2.003, etc.
- **Tier 3 Applications**: 3.001, 3.002, 3.003, etc.
- **Special Studies**: 4.001 (methodology comparisons), 5.001 (replication studies), etc.

#### Benefits
- **Extensible**: Insert 1.015 between 1.001 and 1.002 if needed
- **Categorical**: Tier immediately visible from number
- **Future-proof**: Supports sub-categories (1.001.1, 1.001.2 for variations)
- **Legacy Mapping**: Current 010-014 → 1.001-1.005

#### Implementation Status
- **Phase 1**: ✅ **COMPLETE** - All documentation updated with new numbering system
- **Phase 2**: 🔄 **OPTIONAL** - Directory symlinks for backward compatibility (future)
- **Phase 3**: ✅ **ACTIVE** - All future experiments use new numbering format
- **Phase 4**: 📚 **FUTURE** - Physical directory migration (low priority)

#### Backward Compatibility Guide
**All legacy experiment references remain valid:**
- Directory names unchanged (experiments/012-anagram-grouper/)
- Legacy numbers in documentation show mapping (012 → 1.101)
- GitHub links and bookmarks continue working
- Gradual transition - no breaking changes

**Quick Reference Card:**
```
002 → 1.201 | 006 → 1.203 | 007 → 1.301 | 008 → 1.302 | 009 → 2.101
010 → 1.401 | 011 → 1.204 | 012 → 1.101 | 013 → 1.205 | 014 → 1.102
```