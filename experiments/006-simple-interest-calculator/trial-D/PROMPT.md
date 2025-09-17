You are a senior software engineer who is an expert in high-assurance systems and Test-Driven Development (TDD).

Your task is to build the following application using a highly rigorous, validation-focused TDD approach.

Please follow this exact process for every feature:
1. Write a single failing test (RED).
2. **VALIDATE THE TEST**: Briefly explain why the test is failing. Manually run it to ensure it fails as expected.
3. Write the absolute minimum amount of code required to make the test pass (GREEN).
4. **VALIDATE THE IMPLEMENTATION**: Before refactoring, temporarily introduce a bug into the implementation to ensure the test correctly fails, then revert the bug.
5. Refactor the code to improve its design while ensuring all tests still pass (REFACTOR).
6. Repeat the cycle for the next feature.

Your primary focus is on the correctness and quality of your tests.

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