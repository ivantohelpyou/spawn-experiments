You are a senior software engineer.

Your task is to build the following application.

Please follow this exact process:
1. First, write detailed technical specifications for all components of the application.
2. After you have written the specifications, design the architecture and interfaces for the application.
3. Finally, implement the application according to your own specifications. Ensure your implementation includes robust validation and error handling.

Here are the high-level requirements:
---
# Simple Interest Calculator

Build a simple interest calculator application in Python.

## Core Features

- Calculate simple interest using the formula: Simple Interest = Principal × Rate × Time
- Input validation for positive numbers (principal, rate, time must be > 0)
- Basic output formatting showing the calculated interest amount
- Command-line interface for user interaction

## Requirements

- Accept principal amount (in dollars)
- Accept interest rate (as percentage, e.g., 5 for 5%)
- Accept time period (in years)
- Display calculated simple interest
- Handle invalid inputs gracefully
- Provide clear user prompts and formatted output

## Expected Behavior

```
Enter principal amount: 1000
Enter interest rate (%): 5
Enter time period (years): 2
Simple Interest: $100.00
```

The application should be simple, functional, and handle basic error cases.