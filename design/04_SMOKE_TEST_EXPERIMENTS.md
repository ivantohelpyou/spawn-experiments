# Smoke Test Experiments for TDD Framework

These are minimal experiments designed to validate the experimental framework quickly without significant time investment. Each should take 2-5 minutes per method.

## Experiment Ideas

### 1. Temperature Converter (Recommended First Test)
**Application Type**: Temperature converter
**Tech Stack**: Python
**Complexity**: Minimal (3-4 functions, basic UI)
**Expected Time**: 2-4 minutes per method
**Core Features**:
- Convert between Celsius, Fahrenheit, Kelvin
- Basic input validation
- Simple command-line interface

### 2. Simple Interest Calculator
**Application Type**: Simple interest calculator
**Tech Stack**: Python
**Complexity**: Trivial (1-2 functions)
**Expected Time**: 1-3 minutes per method
**Core Features**:
- Calculate simple interest (Principal × Rate × Time)
- Input validation for positive numbers
- Basic output formatting

### 3. Word Counter
**Application Type**: Word counting utility
**Tech Stack**: Python
**Complexity**: Simple (string processing)
**Expected Time**: 2-4 minutes per method
**Core Features**:
- Count words, characters, lines in text
- Handle file input or direct text input
- Basic statistics output

### 4. Tip Calculator
**Application Type**: Tip calculator
**Tech Stack**: Python
**Complexity**: Minimal (basic math, UI)
**Expected Time**: 2-3 minutes per method
**Core Features**:
- Calculate tip amount and total bill
- Support different tip percentages
- Split bill between multiple people

### 5. BMI Calculator
**Application Type**: BMI calculator
**Tech Stack**: Python
**Complexity**: Trivial (one formula, basic categories)
**Expected Time**: 1-2 minutes per method
**Core Features**:
- Calculate BMI from height and weight
- Categorize BMI (underweight, normal, overweight, obese)
- Support metric and imperial units

## Validation Criteria

### What We're Testing
1. **Framework Functionality**: Do all four methods work as designed?
2. **Time Estimates**: Are our time predictions accurate?
3. **Differentiation**: Do methods produce noticeably different results?
4. **Prompt Quality**: Are our method prompts clear and effective?

### Success Metrics
- **Method 1 (Naive)**: Produces working but basic implementation
- **Method 2 (Spec-First)**: Shows better planning and structure
- **Method 3 (TDD)**: Includes comprehensive tests and better error handling
- **Method 4 (Enhanced TDD)**: Demonstrates test validation and highest quality

### Red Flags
- Methods produce nearly identical results
- Time estimates are wildly off
- Any method fails to produce working code
- Prompts are unclear or lead to confusion

## Quick Validation Protocol

### Phase 1: Single Experiment (30 minutes)
1. Choose Temperature Converter
2. Run all 4 methods back-to-back
3. Compare results immediately
4. Note time taken for each method
5. Identify obvious quality differences

### Phase 2: Framework Refinement (1 hour)
1. Adjust prompts based on Phase 1 results
2. Run Simple Interest Calculator with refined prompts
3. Validate improvements
4. Document lessons learned

### Phase 3: Confidence Building (2 hours)
1. Run 2-3 additional smoke tests
2. Confirm consistent patterns across experiments
3. Validate time estimates
4. Prepare for complex experiments

## Expected Patterns

### Method 1 (Naive) Characteristics
- Minimal error handling
- Basic functionality only
- No tests or minimal testing
- Quick implementation

### Method 2 (Spec-First) Characteristics
- Better structure and planning
- More comprehensive feature set
- Some validation and error handling
- Documentation of requirements

### Method 3 (TDD) Characteristics
- Comprehensive test suite
- Robust error handling
- Clean, refactored code
- Test-driven feature development

### Method 4 (Enhanced TDD) Characteristics
- Validated test quality
- Highest confidence in correctness
- Most maintainable code
- Thorough edge case coverage

## Smoke Test Results Template

### Experiment: [Name]
**Date**: [Date]
**AI Agent**: [Agent Name/Version]

**Method 1 Results**:
- Time: [X] minutes
- Features: [List]
- Quality: [Assessment]
- Issues: [Problems found]

**Method 2 Results**:
- Time: [X] minutes
- Features: [List]
- Quality: [Assessment]
- Issues: [Problems found]

**Method 3 Results**:
- Time: [X] minutes
- Features: [List]
- Quality: [Assessment]
- Issues: [Problems found]

**Method 4 Results**:
- Time: [X] minutes
- Features: [List]
- Quality: [Assessment]
- Issues: [Problems found]

**Overall Assessment**:
- Framework working as expected? [Yes/No]
- Clear differentiation between methods? [Yes/No]
- Time estimates accurate? [Yes/No]
- Ready for complex experiments? [Yes/No]

**Lessons Learned**:
- [Key insights]
- [Prompt improvements needed]
- [Framework adjustments required]

## Next Steps After Smoke Tests

### If Successful
1. Proceed to complex experiments
2. Document validated framework
3. Prepare demo materials
4. Schedule complex experiment sessions

### If Issues Found
1. Refine prompts and methodology
2. Adjust time estimates
3. Clarify method definitions
4. Re-run smoke tests with improvements

### Framework Validation Checklist
- [ ] All methods produce working code
- [ ] Clear quality progression visible
- [ ] Time estimates within 50% of actual
- [ ] Prompts are clear and unambiguous
- [ ] Results are reproducible
- [ ] Framework ready for public demo

---

**Recommendation**: Start with Temperature Converter as it's simple enough to complete quickly but complex enough to show methodology differences.
