# Technical Specifications: Simple Interest Calculator

## Overview
A command-line Python application that calculates simple interest using the formula: Simple Interest = Principal × Rate × Time.

## Functional Requirements

### FR1: Simple Interest Calculation
- **Description**: Calculate simple interest using the standard formula
- **Formula**: Simple Interest = Principal × Rate × Time
- **Input**: Principal (dollars), Rate (percentage), Time (years)
- **Output**: Calculated simple interest amount

### FR2: Input Validation
- **Principal Amount**: Must be a positive number (> 0)
- **Interest Rate**: Must be a positive number (> 0), entered as percentage
- **Time Period**: Must be a positive number (> 0), in years
- **Data Types**: Accept both integers and floating-point numbers

### FR3: User Interface
- **Interface Type**: Command-line interface (CLI)
- **Input Method**: Sequential prompts for each parameter
- **Output Format**: Display result with proper currency formatting ($XXX.XX)

### FR4: Error Handling
- **Invalid Input Types**: Handle non-numeric inputs gracefully
- **Invalid Values**: Handle negative or zero values
- **User Experience**: Provide clear error messages and allow retry

## Non-Functional Requirements

### NFR1: Usability
- Clear and intuitive prompts
- Formatted output with currency symbol
- Graceful error handling with helpful messages

### NFR2: Reliability
- Input validation prevents calculation errors
- Robust error handling prevents application crashes

### NFR3: Maintainability
- Clean, readable code structure
- Modular design for easy testing and modification

## Technical Requirements

### TR1: Programming Language
- **Language**: Python 3.x
- **Standard Library**: Use built-in modules only (no external dependencies)

### TR2: Input/Output Specifications
- **Input Format**: Numeric values (int or float)
- **Output Format**: Currency format with 2 decimal places
- **Error Messages**: Clear, user-friendly text

### TR3: Calculation Specifications
- **Precision**: Use Python's built-in float precision
- **Rate Conversion**: Convert percentage input to decimal (divide by 100)
- **Rounding**: Round final result to 2 decimal places for currency display

## Validation Rules

### VR1: Principal Amount
- Must be numeric (int or float)
- Must be greater than 0
- No upper limit specified

### VR2: Interest Rate
- Must be numeric (int or float)
- Must be greater than 0
- Input as percentage (e.g., 5 for 5%)
- Converted to decimal for calculation (5% → 0.05)

### VR3: Time Period
- Must be numeric (int or float)
- Must be greater than 0
- Unit: years (can accept fractional years)

## Error Scenarios

### ES1: Invalid Input Type
- **Scenario**: User enters non-numeric value
- **Response**: Display error message, prompt for re-entry

### ES2: Invalid Input Value
- **Scenario**: User enters negative or zero value
- **Response**: Display validation error, prompt for re-entry

### ES3: Empty Input
- **Scenario**: User presses Enter without input
- **Response**: Treat as invalid input, prompt for re-entry

## Expected User Flow

1. Application starts
2. Prompt for principal amount
3. Validate input, re-prompt if invalid
4. Prompt for interest rate
5. Validate input, re-prompt if invalid
6. Prompt for time period
7. Validate input, re-prompt if invalid
8. Calculate simple interest
9. Display formatted result
10. Application ends

## Output Format Specification

```
Simple Interest: $XXX.XX
```

Where XXX.XX represents the calculated amount formatted as currency with exactly 2 decimal places.