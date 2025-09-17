# Expression Evaluator - Naive Direct Approach

A simple mathematical expression evaluator implemented using Python's `eval()` function with safety restrictions.

## Overview

This implementation uses a "naive direct approach" where we leverage Python's built-in `eval()` function but restrict it to a safe namespace containing only mathematical functions and constants. This approach is simple but functional for basic mathematical expressions.

## Features

- **Basic arithmetic**: `+`, `-`, `*`, `/`, `%`, `**` (exponentiation)
- **Parentheses**: For grouping and precedence control
- **Mathematical functions**: `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, etc.
- **Constants**: `pi`, `e`, `tau`
- **Safety validation**: Prevents dangerous code execution
- **Interactive CLI**: User-friendly command-line interface
- **Error handling**: Comprehensive error messages

## Files

- `expression_evaluator.py` - Core evaluator class
- `calculator_cli.py` - Interactive command-line interface
- `test_evaluator.py` - Comprehensive test suite
- `README.md` - This documentation

## Usage

### Interactive Calculator

Run the CLI for an interactive experience:

```bash
python calculator_cli.py
```

This provides a user-friendly interface with:
- Expression evaluation
- Command history
- Help system
- Available functions and constants

### Programmatic Usage

```python
from expression_evaluator import ExpressionEvaluator

evaluator = ExpressionEvaluator()

# Basic arithmetic
result = evaluator.evaluate("2 + 3 * 4")  # Returns 14

# Functions
result = evaluator.evaluate("sqrt(16)")   # Returns 4.0

# Constants
result = evaluator.evaluate("sin(pi/2)")  # Returns 1.0
```

### Running Tests

Execute the test suite to verify functionality:

```bash
python test_evaluator.py
```

## Supported Operations

### Arithmetic Operators
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `%` Modulo
- `**` Exponentiation

### Functions
- `abs(x)` - Absolute value
- `round(x)` - Round to nearest integer
- `min(a,b,...)` - Minimum value
- `max(a,b,...)` - Maximum value
- `sqrt(x)` - Square root
- `sin(x)` - Sine (radians)
- `cos(x)` - Cosine (radians)
- `tan(x)` - Tangent (radians)
- `log(x)` - Natural logarithm
- `log10(x)` - Base-10 logarithm
- `exp(x)` - e^x
- `floor(x)` - Floor (round down)
- `ceil(x)` - Ceiling (round up)
- `pow(x,y)` - x raised to power y
- `radians(x)` - Convert degrees to radians
- `degrees(x)` - Convert radians to degrees

### Constants
- `pi` - π (3.14159...)
- `e` - Euler's number (2.71828...)
- `tau` - τ = 2π (6.28318...)

## Examples

```python
# Basic arithmetic
2 + 3 * 4           # = 14
(1 + 2) * 3         # = 9

# Functions
sqrt(16)            # = 4.0
abs(-5)             # = 5
max(1, 2, 3)        # = 3

# Trigonometry
sin(pi/2)           # = 1.0
cos(0)              # = 1.0

# Complex expressions
sqrt(2**2 + 3**2)   # = 3.605551275463989
2**(3+1)            # = 16
```

## Safety Features

The evaluator includes several safety measures:

1. **Restricted namespace**: Only mathematical functions and constants are available
2. **Input validation**: Dangerous patterns and keywords are blocked
3. **Character filtering**: Only safe mathematical characters are allowed
4. **Error handling**: Comprehensive error messages for invalid inputs
5. **No builtins**: All Python built-in functions are disabled

## Limitations

As a naive approach, this evaluator has some limitations:

1. **Security**: Still uses `eval()` which has inherent risks
2. **Performance**: Not optimized for complex or repeated evaluations
3. **Features**: Limited compared to full mathematical parsers
4. **Extensibility**: Difficult to add custom functions or operators

## Development Approach

This implementation prioritizes:
- **Simplicity**: Minimal code complexity
- **Functionality**: Core mathematical operations
- **Safety**: Basic security measures
- **Usability**: Clear interface and error messages

For production use or advanced features, consider implementing a proper recursive descent parser or using a mathematical expression library.