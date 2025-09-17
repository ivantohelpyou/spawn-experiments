# Experiment 002b: Expression Evaluator (pytest Framework)

## Purpose
This experiment tests whether the choice of testing framework (pytest vs unittest) affects the outcomes of TDD-based methodologies.

## Framework Bias Testing
- **Control**: Experiment 002 (Expression Evaluator with unittest)
- **Test**: Experiment 002b (Expression Evaluator with pytest)
- **Variable**: Testing framework only
- **Hypothesis**: Framework choice should have minimal impact on methodology effectiveness

## Experiment Details
- **AI Agent**: Claude 3.5 Sonnet (Anthropic)
- **Problem Domain**: Mathematical expression evaluation
- **Methods to Test**: Method 3 (TDD) and Method 4 (Enhanced TDD)
- **Testing Framework**: pytest

## Problem Specification
Build a mathematical expression evaluator that can:
- Parse and evaluate mathematical expressions
- Handle operator precedence (+, -, *, /, ^, parentheses)
- Support floating-point numbers
- Provide clear error messages for invalid expressions
- Handle edge cases (division by zero, malformed expressions, etc.)

## Comparison Criteria
Will compare against unittest version on:
- Development time/iterations
- Test coverage achieved
- Code quality metrics
- Bug detection effectiveness
- Final feature completeness
- Test readability and maintainability

## Directory Structure
- `003-tdd-pytest/` - TDD approach using pytest
- `004-enhanced-tdd-pytest/` - Enhanced TDD approach using pytest
- `FRAMEWORK_COMPARISON.md` - Detailed comparison with unittest version

## Status
- [ ] Method 3 (TDD with pytest) - Pending
- [ ] Method 4 (Enhanced TDD with pytest) - Pending
- [ ] Comparative analysis - Pending

---

**Note**: This experiment is part of the framework bias testing protocol to ensure our methodology comparisons are not skewed by testing framework choice.
