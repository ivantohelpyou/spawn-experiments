# Experiment Index - Complete Reports (Hierarchical Numbering)

> **NEW**: Reorganized with hierarchical numbering system (T.DCC format)
> See [EXPERIMENT_NUMBERING_SYSTEM.md](EXPERIMENT_NUMBERING_SYSTEM.md) for complete mapping

## Latest Experiment

### 🆕 **[1.101 - Anagram Grouper](experiments/012-anagram-grouper/EXPERIMENT_REPORT.md)** (September 20, 2025)
**Tier 1 Function** | String Processing Domain | Python | 8 minutes parallel execution

**Key Findings:**
- **Method 3 (TDD)** achieved best code efficiency: 401 lines vs Method 2's 1,440 lines
- **Method 1** fastest at ~1 minute, naturally discovered useful features
- **Method 4's test validation** caught subtle bugs early, proving its value
- **Specification explosion risk**: Method 2 over-engineered a simple problem by 3x

**Winner**: Method 3 (TDD) - Best balance of speed, quality, and maintainability for algorithmic problems

*Legacy: 012-anagram-grouper*

---

## All Completed Experiments

### Tier 1: Functions (Pure Algorithms)

#### [1.101 - Anagram Grouper](experiments/012-anagram-grouper/EXPERIMENT_REPORT.md) *(Legacy: 012)*
*September 20, 2025 | String Processing*
- **Problem**: Group words that are anagrams of each other
- **Focus**: Hash key strategy and grouping logic
- **Best Method**: Method 3 (TDD) - Clean, efficient, well-tested
- **Surprising Finding**: Method 2 produced 3x more code than necessary

#### [1.204 - Prime Number Generator](experiments/011-prime-number-generator/EXPERIMENT_REPORT.md) *(Legacy: 011)*
*September 2025 | Mathematical Operations*
- **Problem**: Generate prime numbers efficiently
- **Focus**: Algorithm optimization and performance
- **Status**: ✅ Completed

#### [1.401 - Password Generator](experiments/010-password-generator/) *(Legacy: 010)*
*September 2025 | Security & Cryptography*
- **Problem**: Generate secure passwords with requirements
- **Focus**: Security and randomness
- **Status**: ✅ Completed

#### [1.205 - Roman Numeral Converter](experiments/013-roman-numeral-converter/) *(Legacy: 013)*
*September 2025 | Mathematical Operations*
- **Problem**: Bidirectional Roman numeral conversion
- **Focus**: Mapping strategies and edge cases
- **Status**: ✅ Completed - Fastest TDD at 3m 37s

#### [1.102 - Balanced Parentheses](experiments/014-balanced-parentheses/) *(Legacy: 014)*
*September 2025 | String Processing*
- **Problem**: Validate balanced parentheses in text
- **Focus**: Stack operations and character matching
- **Status**: ✅ Completed

### Tier 2: CLI Tools

#### [2.101 - Multilingual Word Counter](experiments/009-multilingual-word-counter/) *(Legacy: 009)*
*Date TBD | Text Processing Tools*
- **Problem**: Count words with language detection
- **Status**: ⚠️ BIAS VIOLATION - Needs rerun

#### [1.302 - LRU Cache with TTL](experiments/008-lru-cache-ttl/) *(Legacy: 008)*
*August 2025 | Data Structures*
- **Problem**: Implement cache with time-to-live
- **Focus**: Data structures and performance
- **Best Method**: Method 2 - Fastest with quality (6m 35s)
- **Key Finding**: Methods converged on similar implementations

#### [1.301 - LRU Cache with TTL (STOPPED)](experiments/007-lru-cache-ttl-STOPPED/) *(Legacy: 007)*
*September 2025 | Data Structures*
- **Problem**: Same as 1.302 but hit resource constraints
- **Status**: ❌ STOPPED - Methods 3&4 hit token limits

### Tier 3: Applications

#### [1.203 - Simple Interest Calculator](experiments/006-simple-interest-calculator/) *(Legacy: 006)*
*July 2025 | Mathematical Operations*
- **Problem**: Financial calculation tool
- **Type**: Smoke test for methodology validation
- **Status**: ✅ Valid baseline

#### [1.201 - Expression Evaluator](experiments/002-expression-evaluator/) *(Legacy: 002)*
*June 2025 | Mathematical Operations*
- **Problem**: Mathematical expression parser
- **Duration**: 35 minutes total
- **Status**: ✅ Valid results

#### [3.501 - Unicode Password Manager](experiments/001-unicode-password-manager/) *(Legacy: 001)*
*Early 2025 | Security Applications*
- **Problem**: Full password management application
- **Status**: ✅ Completed (pre-methodology framework)

---

## Methodology Performance Summary

### Speed Rankings (Average)
1. **Method 1** (Immediate): Consistently fastest
2. **Method 2** (Specification): Fast with planning overhead
3. **Method 3** (TDD): Moderate speed, high quality
4. **Method 4** (Validated): Slowest but highest confidence

### Code Quality Rankings
1. **Method 3** (TDD): Cleanest, most maintainable
2. **Method 4** (Validated): Well-tested, validated
3. **Method 2** (Specification): Comprehensive but verbose
4. **Method 1** (Immediate): Functional but less structured

### Test Coverage Rankings
1. **Method 4** (Validated): Most comprehensive with validation
2. **Method 2** (Specification): Extensive test suites
3. **Method 3** (TDD): Essential coverage
4. **Method 1** (Immediate): Basic testing

---

## Trends and Insights

### Emerging Patterns
1. **TDD produces cleanest code** with minimal overhead for simple problems
2. **Specification-driven risks over-engineering** on Tier 1 problems
3. **Test validation (Method 4)** consistently catches subtle bugs
4. **Immediate implementation** naturally discovers practical features

### Methodology Selection Guide

**Use Method 1 (Immediate) when:**
- Prototyping or exploring
- Time is critical
- Problem is well-understood

**Use Method 2 (Specification) when:**
- Complex business requirements
- Team collaboration needed
- Building APIs or libraries

**Use Method 3 (TDD) when:**
- Standard development tasks
- Code quality matters
- Refactoring existing code

**Use Method 4 (Validated) when:**
- Mission-critical systems
- Security is paramount
- Test quality essential

---

## Next Experiments

### Planned Experiments

#### Tier 1 - Input Validation Domain (1.5XX)
- **1.501** - Email Validator
- **1.502** - URL Validator
- **1.503** - File Path Validator
- **1.504** - Date Format Validator
- **1.505** - Phone Number Validator

#### Tier 2 - CLI Tools (2.XXX)
- **2.501** - Password Manager CLI (reuses 1.401)
- **2.201** - Number Theory Calculator (reuses 1.204, 1.205)
- **2.102** - Text Analysis Tool (reuses 1.101, 1.102)
- **2.202** - Code Structure Validator (reuses 1.102)
- **2.401** - File Statistics Tool (baseline - minimal reuse)

#### Tier 3 - Applications (3.XXX)
- **3.101** - Personal Knowledge Manager
- **3.201** - Project Dashboard
- **3.401** - Personal Finance Tracker
- **3.301** - System Monitor
- **3.102** - Document Processor

---

*Last Updated: September 20, 2025*