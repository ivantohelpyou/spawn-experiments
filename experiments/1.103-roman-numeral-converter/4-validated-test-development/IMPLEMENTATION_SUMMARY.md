# Roman Numeral Converter - TDD with Systematic Test Validation

## Overview
This implementation demonstrates a rigorous test-driven development approach with systematic test validation for a Roman numeral converter supporting the range 1-3999.

## Key Features Implemented

### Core Functionality
- **Bidirectional conversion**: Integer ↔ Roman numeral
- **Full range support**: 1 to 3999 (standard Roman numeral range)
- **Proper subtractive notation**: IV, IX, XL, XC, CD, CM
- **Comprehensive validation**: Input type checking, range validation, pattern validation

### Test-Driven Development Process

#### 1. Comprehensive Test Suite (185 individual test cases)
- **Single digit conversions**: 1-9
- **Tens conversions**: 10, 20, 30, 40, 50, 60, 70, 80, 90
- **Hundreds conversions**: 100, 200, 300, 400, 500, 600, 700, 800, 900
- **Thousands conversions**: 1000, 2000, 3000
- **Complex number conversions**: Multi-digit combinations
- **Historical dates**: 1066, 1492, 1776, 1984, 2024
- **Boundary values**: 1 (minimum), 3999 (maximum)
- **Round-trip validation**: Ensures conversion consistency
- **Edge cases and error handling**: Invalid inputs, type validation

#### 2. Test Validation Process
Created four intentionally incorrect implementations to validate test quality:

**Wrong Implementation #1**: Incomplete subtractive notation
- Missing subtractive cases (IV, IX, XL, XC, CD, CM)
- **Tests caught**: 8 failures in subtractive notation tests

**Wrong Implementation #2**: No input validation
- Missing type checking and range validation
- **Tests caught**: TypeError and ValueError validation failures

**Wrong Implementation #3**: Incorrect conversion logic
- Wrong Roman-to-integer parsing (additive instead of subtractive)
- **Tests caught**: Subtractive notation and round-trip test failures

**Wrong Implementation #4**: Insufficient validation
- Accepts invalid Roman patterns (IIII, VV, etc.)
- **Tests caught**: Invalid input validation test failures

#### 3. Correct Implementation Features

**Input Validation**:
- Type checking (int for to_roman, str for from_roman)
- Range validation (1-3999)
- Character validation (valid Roman numerals only)
- Pattern validation using regex
- Round-trip validation for additional security

**Conversion Logic**:
- Greedy algorithm for integer-to-Roman conversion
- Subtractive notation handling for Roman-to-integer conversion
- Proper handling of all standard Roman numeral patterns

**Error Handling**:
- TypeError for incorrect input types
- ValueError for out-of-range numbers
- ValueError for invalid Roman numeral patterns
- Detailed error messages for debugging

## Files Created

### Core Implementation
- `roman_converter.py`: Main converter class with full functionality
- `test_roman_converter.py`: Comprehensive test suite (19 test methods)

### Test Validation
- `roman_converter_wrong1.py`: Incomplete subtractive notation
- `roman_converter_wrong2.py`: No input validation
- `roman_converter_wrong3.py`: Wrong conversion logic
- `roman_converter_wrong4.py`: Insufficient validation

### Demonstration
- `demo.py`: Interactive demonstration of converter functionality

## Test Results

**Final Test Suite**: All 19 tests pass (100% success rate)
**Wrong Implementation Validation**: All 4 incorrect implementations properly caught by tests

```
Ran 19 tests in 0.003s
OK
```

## Key Technical Decisions

1. **Regex Pattern Validation**: Used comprehensive regex to enforce proper Roman numeral structure
2. **Round-trip Validation**: Additional check to ensure converted values can be converted back correctly
3. **Comprehensive Error Messages**: Detailed feedback for invalid inputs
4. **Greedy Algorithm**: Efficient conversion using value-symbol pairs in descending order

## Test Coverage Analysis

The test suite validates:
- ✅ All single Roman numeral symbols (I, V, X, L, C, D, M)
- ✅ All subtractive notation cases (IV, IX, XL, XC, CD, CM)
- ✅ Complex multi-digit combinations
- ✅ Boundary conditions (1, 3999)
- ✅ Historical and practical examples
- ✅ Round-trip conversion consistency
- ✅ Input validation and error handling
- ✅ Type safety and security

## Conclusion

This implementation demonstrates the effectiveness of test-driven development with systematic test validation. By creating intentionally incorrect implementations first, we verified that our test suite is comprehensive and capable of catching real-world errors. The final implementation passes all tests and provides robust, secure Roman numeral conversion with excellent error handling.