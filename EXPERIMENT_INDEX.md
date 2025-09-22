# Experiment Index - Complete Reports (Hierarchical Numbering)

> **NEW**: Reorganized with hierarchical numbering system (T.DCC.V format)
> See [EXPERIMENT_NUMBERING_SYSTEM.md](EXPERIMENT_NUMBERING_SYSTEM.md) for complete mapping

## Latest Experiment

### 🆕 **[1.502 - URL Validator](experiments/1.502-url-validator/EXPERIMENT_REPORT.md)** (September 21, 2025)
**Tier 1 Function** | Input Validation Domain | Python | 16 minutes parallel execution

**REVOLUTIONARY FINDINGS:**
- **Method 2** created **6,036 lines** vs Method 3's **187 lines** - **32.3X OVER-ENGINEERING!** 🚨
- **Largest complexity explosion** in our research - enterprise framework for simple validation
- **Spontaneous features**: SSRF protection, rate limiting, CLI with JSON/CSV/XML, IPv6, IDN - NONE requested!
- **Method 3 (TDD)** completed in 3.5 minutes with minimal viable solution

**Winner**: Method 3 (TDD) - 187 lines achieving identical functionality to 6,036-line enterprise framework

*Pattern escalation confirmed: Email (3.6X) → URL (32.3X) complexity multiplier growth*

---

## All Completed Experiments

### Tier 1: Functions (Pure Algorithms)

#### [1.101 - Anagram Grouper](experiments/1.101-anagram-grouper/EXPERIMENT_REPORT.md) *(Legacy: 012)*
*September 20, 2025 | String Processing*
- **Problem**: Group words that are anagrams of each other
- **Focus**: Hash key strategy and grouping logic
- **Best Method**: Method 3 (TDD) - Clean, efficient, well-tested
- **Surprising Finding**: Method 2 produced 3x more code than necessary
- **📺 [Interactive Demo](experiments/1.101-anagram-grouper/methodology_comparison_demo.py)** - Shows 3X code difference live

#### [1.102 - Multilingual Word Counter](experiments/1.102-multilingual-word-counter/EXPERIMENT_REPORT.md) *(Legacy: 009)*
*September 2025 | String Processing*
- **Problem**: Count words with language detection
- **Focus**: Text processing and I18N
- **Status**: ✅ Completed

#### [1.103 - Roman Numeral Converter](experiments/1.103-roman-numeral-converter/EXPERIMENT_REPORT.md) *(Legacy: 013)*
*September 2025 | String Processing*
- **Problem**: Bidirectional Roman numeral conversion
- **Focus**: Mapping strategies and edge cases
- **Status**: ✅ Completed - Fastest TDD at 3m 37s

#### [1.104 - Balanced Parentheses](experiments/1.104-balanced-parentheses/EXPERIMENT_REPORT.md) *(Legacy: 014)*
*September 2025 | String Processing*
- **Problem**: Validate balanced parentheses in text
- **Focus**: Stack operations and character matching
- **Status**: ✅ Completed

#### [1.201 - Expression Evaluator](experiments/1.201-expression-evaluator/EXPERIMENT_REPORT.md) *(Legacy: 002)*
*June 2025 | Mathematical Operations*
- **Problem**: Mathematical expression parser
- **Duration**: 35 minutes total
- **Status**: ✅ Valid results

#### [1.203 - Temperature Converter](experiments/1.203-temperature-converter/) *(Legacy: 005)*
*July 2025 | Mathematical Operations*
- **Problem**: Convert between temperature scales
- **Type**: Smoke test for methodology validation
- **Status**: ✅ Valid baseline

#### [1.204 - Simple Interest Calculator](experiments/1.204-simple-interest-calculator/EXPERIMENT_REPORT.md) *(Legacy: 006)*
*July 2025 | Mathematical Operations*
- **Problem**: Financial calculation tool
- **Type**: Smoke test for methodology validation
- **Status**: ✅ Valid baseline

#### [1.205 - Prime Number Generator](experiments/1.205-prime-number-generator/EXPERIMENT_REPORT.md) *(Legacy: 011)*
*September 2025 | Mathematical Operations*
- **Problem**: Generate prime numbers efficiently
- **Focus**: Algorithm optimization and performance
- **Status**: ✅ Completed

#### [1.302 - LRU Cache with TTL](experiments/1.302-lru-cache-ttl/EXPERIMENT_REPORT.md) *(Legacy: 008)*
*August 2025 | Data Structures*
- **Problem**: Implement cache with time-to-live
- **Focus**: Data structures and performance
- **Best Method**: Method 2 - Fastest with quality (6m 35s)
- **Key Finding**: Methods converged on similar implementations

#### [1.402 - Unicode Password Manager](experiments/1.402-unicode-password-manager/) *(Legacy: 001)*
*Early 2025 | Security Applications*
- **Problem**: Full password management application
- **Status**: ✅ Completed (pre-methodology framework)

#### [1.501 - Email Validator](experiments/1.501-email-validator/EXPERIMENT_REPORT.md)
*September 21, 2025 | Input Validation*
- **Problem**: Validate email addresses with RFC compliance
- **Best Method**: Method 3 (TDD) - 3.6X less code than Method 1
- **Key Finding**: Unconstrained AI spontaneously over-engineers validation
- **Surprising**: Method 1 created 4 validation levels unprompted
- **📺 [Interactive Demo](experiments/1.501-email-validator/simple_robustness_demo.py)** - Shows security vulnerabilities live

#### [1.502 - URL Validator](experiments/1.502-url-validator/EXPERIMENT_REPORT.md)
*September 21, 2025 | Input Validation*
- **Problem**: Validate URL format and accessibility
- **Best Method**: Method 3 (TDD) - 32.3X less code than Method 2!
- **Key Finding**: Largest over-engineering factor observed
- **Shocking**: Method 2 built enterprise security framework unprompted
- **📺 [Interactive Demo](experiments/1.502-url-validator/methodology_comparison_demo.py)** - Shows 32X complexity explosion live

### Summary

**Total Completed Experiments**: 12
- **String Processing (1.1XX)**: 4 experiments
- **Mathematical Operations (1.2XX)**: 4 experiments
- **Data Structures (1.3XX)**: 1 experiment
- **Security/Cryptography (1.4XX)**: 1 experiment
- **Input Validation (1.5XX)**: 2 experiments ✅

---

## 📺 Interactive Demos

Experience methodology differences live! These demo scripts can be run from the project root to see real-time comparisons:

### Available Demos:
- **[Anagram Grouper Demo](experiments/1.101-anagram-grouper/methodology_comparison_demo.py)**
  ```bash
  python experiments/1.101-anagram-grouper/methodology_comparison_demo.py
  ```
  Shows dramatic 3X code size difference between TDD and specification-driven approaches

- **[Email Validator Security Demo](experiments/1.501-email-validator/simple_robustness_demo.py)**
  ```bash
  python experiments/1.501-email-validator/simple_robustness_demo.py
  ```
  Reveals 7 security vulnerabilities in Method 1's permissive validation

### Demo Features:
- ✅ **Live comparison** of all four methodologies
- ✅ **Interactive output** perfect for presentations
- ✅ **Concrete evidence** of methodology differences
- ✅ **Run from anywhere** - project root or experiment directory

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
- **1.501** - Email Validator ✅ **Completed** (TDD Winner)
- **1.502** - URL Validator
- **1.503** - File Path Validator
- **1.504** - Date Format Validator
- **1.505** - Phone Number Validator

#### Tier 2 - CLI Tools (2.XXX)
- **2.501** - Password Manager CLI (reuses 1.4XX components)
- **2.201** - Number Theory Calculator (reuses 1.204, 1.205)
- **2.102** - Text Analysis Tool (reuses 1.101, 1.102)
- **2.202** - Code Structure Validator (reuses 1.104)
- **2.401** - File Statistics Tool (baseline - minimal reuse)

#### Tier 3 - Applications (3.XXX)
- **3.101** - Personal Knowledge Manager
- **3.201** - Project Dashboard
- **3.401** - Personal Finance Tracker
- **3.301** - System Monitor
- **3.102** - Document Processor

---

*Last Updated: September 21, 2025*