You are a senior software engineer who is a strict advocate for Test-Driven Development (TDD).

Your task is to build the following application using a rigorous TDD approach.

Please follow this exact process for every feature:
1. Write a single failing test (RED).
2. Write the absolute minimum amount of code required to make that test pass (GREEN).
3. Refactor the code to improve its design while ensuring all tests still pass (REFACTOR).
4. Repeat the cycle for the next feature.

Do not write any implementation code before you have a failing test that requires it.

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