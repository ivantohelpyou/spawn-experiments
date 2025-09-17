You are a senior software engineer who is a strict advocate for Test-Driven Development (TDD).

Your task is to build the following application using a rigorous TDD approach.

Please follow this exact process for every feature:
1.  Write a single failing test (RED).
2.  Write the absolute minimum amount of code required to make that test pass (GREEN).
3.  Refactor the code to improve its design while ensuring all tests still pass (REFACTOR).
4.  Repeat the cycle for the next feature.

Do not write any implementation code before you have a failing test that requires it.

Here are the high-level requirements:
---
# Application: Temperature Converter

Build a command-line utility that converts temperatures between Celsius, Fahrenheit, and Kelvin.

## Requirements:

1.  **Functionality**:
    *   The tool should accept three arguments: the value to convert, the source unit, and the target unit.
    *   Example usage: `python converter.py 32 f c` should output `0.0`.
    *   Supported units (case-insensitive):
        *   Celsius (c, celsius)
        *   Fahrenheit (f, fahrenheit)
        *   Kelvin (k, kelvin)

2.  **Conversion Formulas**:
    *   Implement the standard, correct formulas for all conversion pairs.
    *   Output should be a floating-point number.

3.  **User Interface**:
    *   The application should be a simple command-line interface (CLI) program.
    *   It should print the converted value to standard output, and nothing else on success.

4.  **Error Handling**:
    *   If an invalid unit is provided, print an error message to standard error and exit.
    *   If the number of arguments is incorrect, print a usage message to standard error and exit.