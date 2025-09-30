# Architecture Design: Simple Interest Calculator

## System Architecture

### Architecture Pattern
**Modular Function-Based Architecture**
- Single Python module with focused functions
- Separation of concerns between input, validation, calculation, and output
- Simple, linear execution flow suitable for CLI application

### Component Overview
```
┌─────────────────────────────────────────┐
│           Main Application              │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │     Input Handler Module        │    │
│  │  - get_user_input()            │    │
│  │  - validate_positive_number()  │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │   Calculation Module            │    │
│  │  - calculate_simple_interest()  │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │     Output Module               │    │
│  │  - format_currency()           │    │
│  │  - display_result()            │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │     Main Controller             │    │
│  │  - main()                      │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## Interface Specifications

### Function Interfaces

#### 1. Input Handler Module

##### `get_user_input(prompt: str) -> float`
**Purpose**: Get and validate numeric input from user

**Parameters**:
- `prompt (str)`: The message to display to the user
**Returns**:
- `float`: Valid positive number entered by user
**Behavior**:
- Displays prompt to user
- Reads user input
- Validates input is numeric and positive
- Re-prompts on invalid input
- Returns validated number as float

##### `validate_positive_number(value: str) -> tuple[bool, float]`
**Purpose**: Validate that input string is a positive number

**Parameters**:
- `value (str)`: String input to validate
**Returns**:
- `tuple[bool, float]`: (is_valid, parsed_value)
**Behavior**:
- Attempts to convert string to float
- Checks if value is positive (> 0)
- Returns validation status and parsed value

#### 2. Calculation Module

##### `calculate_simple_interest(principal: float, rate: float, time: float) -> float`
**Purpose**: Calculate simple interest using the standard formula

**Parameters**:
- `principal (float)`: Principal amount in dollars
- `rate (float)`: Interest rate as percentage
- `time (float)`: Time period in years
**Returns**:
- `float`: Calculated simple interest amount
**Formula**: `Simple Interest = Principal × (Rate / 100) × Time`

#### 3. Output Module

##### `format_currency(amount: float) -> str`
**Purpose**: Format numeric amount as currency string

**Parameters**:
- `amount (float)`: Numeric amount to format
**Returns**:
- `str`: Formatted currency string (e.g., "$123.45")
**Behavior**:
- Rounds to 2 decimal places
- Adds dollar sign prefix
- Ensures exactly 2 decimal places are shown

##### `display_result(interest: float) -> None`
**Purpose**: Display the calculated result to user

**Parameters**:
- `interest (float)`: Calculated simple interest amount
**Returns**: None

**Behavior**:
- Formats interest as currency
- Displays result with "Simple Interest: " prefix

#### 4. Main Controller

##### `main() -> None`
**Purpose**: Main application entry point and controller

**Parameters**: None

**Returns**: None

**Behavior**:
- Orchestrates the complete user interaction flow
- Calls input functions to gather user data
- Calls calculation function to compute result
- Calls output function to display result

## Data Flow

### Input Data Flow
```
User Input → String Validation → Type Conversion → Range Validation → Float Value
```

### Processing Data Flow
```
Principal (float) ┐
Rate (float)      ├→ calculate_simple_interest() → Simple Interest (float)
Time (float)      ┘
```

### Output Data Flow
```
Simple Interest (float) → format_currency() → Display String → Console Output
```

## Error Handling Strategy

### Input Validation Errors
- **Type Errors**: Catch ValueError during float conversion
- **Value Errors**: Check for positive values after conversion
- **Recovery**: Re-prompt user until valid input is provided

### Error Message Standards
- Clear, specific error messages
- Indicate what type of input is expected
- Maintain consistent tone and format

## Module Dependencies

### Standard Library Dependencies
- `sys`: For potential exit handling (if needed)
- No external dependencies required

### Internal Dependencies
- All functions are independent and can be tested in isolation
- Main function coordinates all other functions
- No circular dependencies

## Testing Strategy

### Unit Testing Approach
- Test each function independently
- Mock user input for input functions
- Test edge cases and error conditions
- Verify calculation accuracy with known values

### Test Cases Categories
1. **Valid Input Tests**: Standard positive numbers
2. **Invalid Input Tests**: Negative, zero, non-numeric values
3. **Calculation Tests**: Verify formula accuracy
4. **Formatting Tests**: Currency output format
5. **Integration Tests**: Complete user flow simulation

## File Structure

```
simple_interest_calculator.py
├── Input Handler Functions
├── Calculation Functions
├── Output Functions
├── Main Controller Function
└── Entry Point (if __name__ == "__main__")
```

## Performance Considerations

### Computational Complexity
- All operations are O(1) - constant time
- No loops or recursive operations in core logic
- Input validation loops only until valid input provided

### Memory Usage
- Minimal memory footprint
- No data structures beyond simple variables
- No persistent state maintained