You are a senior software engineer.

Your task is to build the following application.

Please follow this exact process:
1.  First, write detailed technical specifications for all components of the application.
2.  After you have written the specifications, design the architecture and interfaces for the application.
3.  Finally, implement the application according to your own specifications. Ensure your implementation includes robust validation and error handling.

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