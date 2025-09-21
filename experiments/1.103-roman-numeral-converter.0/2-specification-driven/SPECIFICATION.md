# Roman Numeral Conversion System Specification

## 1. Overview

This specification defines a bidirectional Roman numeral conversion system that converts integers to Roman numerals and Roman numerals back to integers for the range 1-3999.

## 2. Requirements

### 2.1 Functional Requirements

#### 2.1.1 Integer to Roman Numeral Conversion
- **Input**: Integer in range [1, 3999]
- **Output**: Valid Roman numeral string representation
- **Behavior**: Convert the input integer to its corresponding Roman numeral using standard Roman numeral rules

#### 2.1.2 Roman Numeral to Integer Conversion
- **Input**: Valid Roman numeral string
- **Output**: Integer in range [1, 3999]
- **Behavior**: Parse the Roman numeral string and return its integer value

### 2.2 Non-Functional Requirements
- **Performance**: Conversions should complete in O(1) time complexity
- **Memory**: Minimal memory footprint using efficient data structures
- **Reliability**: 100% accuracy for all valid inputs within the specified range
- **Maintainability**: Clean, readable code with comprehensive documentation

## 3. Roman Numeral System Rules

### 3.1 Basic Symbols
| Symbol | Value |
|--------|-------|
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

### 3.2 Combination Rules
- Symbols are generally written in descending order of value
- When a smaller symbol appears before a larger one, it represents subtraction
- Only specific subtractive combinations are valid:
  - I can be subtracted from V (4) and X (9)
  - X can be subtracted from L (40) and C (90)
  - C can be subtracted from D (400) and M (900)

### 3.3 Repetition Rules
- I, X, C, and M can be repeated up to 3 consecutive times
- V, L, and D are never repeated
- No more than 3 consecutive identical symbols are allowed

### 3.4 Valid Subtractive Combinations
| Combination | Value | Description |
|-------------|-------|-------------|
| IV          | 4     | 5 - 1       |
| IX          | 9     | 10 - 1      |
| XL          | 40    | 50 - 10     |
| XC          | 90    | 100 - 10    |
| CD          | 400   | 500 - 100   |
| CM          | 900   | 1000 - 100  |

## 4. Input Validation Rules

### 4.1 Integer Input Validation
- Must be a positive integer
- Must be in range [1, 3999]
- No decimal numbers, strings, or other data types accepted

### 4.2 Roman Numeral Input Validation
- Must be a non-empty string
- Must contain only valid Roman numeral characters (I, V, X, L, C, D, M)
- Must follow proper Roman numeral formation rules
- Case-insensitive input accepted, but output should be uppercase
- Must not exceed the value 3999 when converted to integer

### 4.3 Invalid Roman Numeral Patterns
The following patterns are considered invalid:
- More than 3 consecutive identical symbols: "IIII", "XXXX", "CCCC", "MMMM"
- Invalid subtractive combinations: "IL", "IC", "ID", "IM", "VX", "VL", "VC", "VD", "VM", "XD", "XM", "LC", "LD", "LM", "DM"
- Repeated subtractive combinations: "IXIX", "XLXL", "CDCD"
- Symbols in wrong order: "IXXI" (should be "XXI")

## 5. Edge Cases

### 5.1 Boundary Values
- **Minimum value**: 1 → "I"
- **Maximum value**: 3999 → "MMMCMXCIX"

### 5.2 Special Cases
- **Numbers ending in 4**: 14 → "XIV", 24 → "XXIV", 444 → "CDXLIV"
- **Numbers ending in 9**: 19 → "XIX", 29 → "XXIX", 999 → "CMXCIX"
- **Round hundreds**: 100 → "C", 500 → "D", 900 → "CM"
- **Round thousands**: 1000 → "M", 2000 → "MM", 3000 → "MMM"

### 5.3 Complex Numbers
- **1994**: "MCMXCIV" (multiple subtractive combinations)
- **3888**: "MMMDCCCLXXXVIII" (maximum repetitions)
- **1776**: "MDCCLXXVI" (common historical date)

## 6. Error Handling

### 6.1 Input Type Errors
- **TypeError**: Raised when input is not the expected type (int for int_to_roman, str for roman_to_int)
- **Message**: Clear description of expected input type

### 6.2 Value Range Errors
- **ValueError**: Raised when integer input is outside [1, 3999] range
- **Message**: "Integer must be between 1 and 3999, got: {value}"

### 6.3 Invalid Roman Numeral Errors
- **ValueError**: Raised when Roman numeral string is invalid
- **Message**: "Invalid Roman numeral: {input}"

### 6.4 Empty Input Errors
- **ValueError**: Raised when Roman numeral string is empty or whitespace
- **Message**: "Roman numeral cannot be empty"

## 7. API Specification

### 7.1 Function Signatures

```python
def int_to_roman(num: int) -> str:
    """
    Convert an integer to Roman numeral.

    Args:
        num (int): Integer between 1 and 3999 inclusive

    Returns:
        str: Roman numeral representation

    Raises:
        TypeError: If num is not an integer
        ValueError: If num is outside the valid range [1, 3999]
    """

def roman_to_int(roman: str) -> int:
    """
    Convert a Roman numeral to integer.

    Args:
        roman (str): Valid Roman numeral string

    Returns:
        int: Integer value between 1 and 3999

    Raises:
        TypeError: If roman is not a string
        ValueError: If roman is not a valid Roman numeral
    """
```

### 7.2 Class-Based API (Alternative)

```python
class RomanNumeralConverter:
    """Roman numeral conversion system."""

    def to_roman(self, num: int) -> str:
        """Convert integer to Roman numeral."""

    def to_int(self, roman: str) -> int:
        """Convert Roman numeral to integer."""

    def is_valid_roman(self, roman: str) -> bool:
        """Check if a string is a valid Roman numeral."""
```

## 8. Test Cases

### 8.1 Valid Integer to Roman Conversions
| Input | Expected Output |
|-------|----------------|
| 1     | "I"            |
| 4     | "IV"           |
| 5     | "V"            |
| 9     | "IX"           |
| 10    | "X"            |
| 40    | "XL"           |
| 50    | "L"            |
| 90    | "XC"           |
| 100   | "C"            |
| 400   | "CD"           |
| 500   | "D"            |
| 900   | "CM"           |
| 1000  | "M"            |
| 1994  | "MCMXCIV"      |
| 3999  | "MMMCMXCIX"    |

### 8.2 Valid Roman to Integer Conversions
| Input         | Expected Output |
|---------------|----------------|
| "I"           | 1              |
| "IV"          | 4              |
| "V"           | 5              |
| "IX"          | 9              |
| "X"           | 10             |
| "XL"          | 40             |
| "L"           | 50             |
| "XC"          | 90             |
| "C"           | 100            |
| "CD"          | 400            |
| "D"           | 500            |
| "CM"          | 900            |
| "M"           | 1000           |
| "MCMXCIV"     | 1994           |
| "MMMCMXCIX"   | 3999           |

### 8.3 Case Insensitivity Tests
| Input         | Expected Output |
|---------------|----------------|
| "i"           | 1              |
| "iv"          | 4              |
| "mcmxciv"     | 1994           |
| "MmMcMxCiX"   | 3999           |

### 8.4 Error Test Cases

#### 8.4.1 Invalid Integer Inputs
| Input | Expected Error | Error Message |
|-------|----------------|---------------|
| 0     | ValueError     | "Integer must be between 1 and 3999, got: 0" |
| -1    | ValueError     | "Integer must be between 1 and 3999, got: -1" |
| 4000  | ValueError     | "Integer must be between 1 and 3999, got: 4000" |
| "5"   | TypeError      | "Expected integer, got str" |
| 3.14  | TypeError      | "Expected integer, got float" |

#### 8.4.2 Invalid Roman Numeral Inputs
| Input    | Expected Error | Error Message |
|----------|----------------|---------------|
| ""       | ValueError     | "Roman numeral cannot be empty" |
| "   "    | ValueError     | "Roman numeral cannot be empty" |
| "IIII"   | ValueError     | "Invalid Roman numeral: IIII" |
| "VV"     | ValueError     | "Invalid Roman numeral: VV" |
| "IL"     | ValueError     | "Invalid Roman numeral: IL" |
| "ABC"    | ValueError     | "Invalid Roman numeral: ABC" |
| 42       | TypeError      | "Expected string, got int" |

## 9. Performance Requirements

### 9.1 Time Complexity
- **int_to_roman**: O(1) - bounded by constant number of symbol mappings
- **roman_to_int**: O(n) where n is the length of Roman numeral string (max 15 characters)

### 9.2 Space Complexity
- **int_to_roman**: O(1) - uses fixed-size lookup tables
- **roman_to_int**: O(1) - uses fixed-size symbol value mappings

### 9.3 Benchmark Targets
- Convert 1000 random integers to Roman numerals: < 50ms
- Convert 1000 random Roman numerals to integers: < 100ms
- Memory usage: < 1KB for all static data structures

## 10. Implementation Strategy

### 10.1 Integer to Roman Conversion Algorithm
1. Use a mapping of values to Roman numeral symbols in descending order
2. Include subtractive combinations (900→CM, 400→CD, etc.) in the mapping
3. Iterate through the mapping, subtracting values and appending symbols
4. Continue until the input number is reduced to zero

### 10.2 Roman to Integer Conversion Algorithm
1. Create a mapping of Roman symbols to their integer values
2. Include subtractive combinations in the mapping for efficient parsing
3. Iterate through the Roman numeral string, identifying patterns
4. Sum the values, handling subtractive cases correctly
5. Validate the result against formatting rules

### 10.3 Validation Strategy
1. **Type checking**: Verify input types before processing
2. **Range checking**: Ensure integers are within [1, 3999]
3. **Format validation**: Use regex or pattern matching for Roman numerals
4. **Logical validation**: Verify Roman numerals follow formation rules

## 11. Quality Assurance

### 11.1 Testing Strategy
- **Unit tests**: Individual function testing with comprehensive test cases
- **Integration tests**: End-to-end conversion roundtrip testing
- **Property-based testing**: Ensure int_to_roman(roman_to_int(x)) == x
- **Edge case testing**: Boundary values and error conditions
- **Performance testing**: Benchmark against requirements

### 11.2 Code Quality Standards
- **Type hints**: Full type annotation for all functions
- **Docstrings**: Comprehensive documentation for all public methods
- **Error messages**: Clear, descriptive error messages for all failure cases
- **Code coverage**: 100% line and branch coverage
- **Static analysis**: Pass mypy type checking and linting

### 11.3 Acceptance Criteria
1. All test cases pass without errors
2. Performance meets specified benchmarks
3. Code coverage reaches 100%
4. Type checking passes without warnings
5. All edge cases handled correctly
6. Error messages are user-friendly and informative

## 12. Future Enhancements

### 12.1 Extended Range Support
- Support for numbers beyond 3999 using overline notation
- Unicode support for proper overline rendering

### 12.2 Historical Variations
- Support for medieval Roman numeral variations
- Alternative subtraction rules used in different periods

### 12.3 Formatting Options
- Lowercase output option
- Additive-only notation (IIII instead of IV)
- Custom separators or spacing

---

**Document Version**: 1.0
**Last Updated**: 2025-09-20
**Author**: Specification-Driven Development Process