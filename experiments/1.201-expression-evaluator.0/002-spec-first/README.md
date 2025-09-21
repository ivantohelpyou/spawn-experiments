# Expression Evaluator - Specification-First Implementation

A comprehensive mathematical expression parsing and evaluation system built using the specification-first approach. This implementation strictly follows the detailed specifications outlined in `SPECIFICATIONS.md`.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Command Line Interface](#command-line-interface)
- [Examples](#examples)
- [Testing](#testing)
- [Architecture](#architecture)
- [Performance](#performance)
- [Contributing](#contributing)

## Overview

The Expression Evaluator is a Python-based mathematical expression parsing and evaluation system designed to handle complex mathematical expressions with support for various operators, functions, and variables. The system provides both programmatic API access and command-line interface for evaluating mathematical expressions safely and efficiently.

This implementation follows a specification-first approach, where comprehensive specifications were written before any code implementation, ensuring a well-designed and thoroughly planned system.

## Features

### Core Features
- **Basic Arithmetic Operations**: `+`, `-`, `*`, `/`, `%`, `//`, `**`
- **Mathematical Functions**: `sin`, `cos`, `tan`, `log`, `sqrt`, `abs`, and many more
- **Mathematical Constants**: `pi`, `e`, `tau`, `inf`
- **Variable Support**: Define and use variables in expressions
- **Parentheses Support**: Proper handling of nested parentheses
- **Expression Validation**: Comprehensive syntax checking
- **Error Handling**: Detailed error messages with position information
- **Command-Line Interface**: Interactive and batch processing modes
- **Performance Optimization**: Caching and efficient evaluation

### Advanced Features
- **Custom Functions**: Add your own mathematical functions
- **Batch Processing**: Evaluate multiple expressions efficiently
- **AST Generation**: Access to Abstract Syntax Tree representation
- **Performance Statistics**: Track evaluation metrics
- **Scientific Notation**: Support for scientific number format
- **High Precision**: Configurable decimal precision

## Installation

Since this is a self-contained implementation, simply ensure you have Python 3.8 or later:

```bash
python --version  # Should be 3.8+
```

For testing, install pytest:
```bash
pip install pytest
```

## Quick Start

### Basic Usage

```python
from expression_manager import evaluate

# Simple arithmetic
result = evaluate("2 + 3 * 4")
print(result)  # 14.0

# Mathematical functions
result = evaluate("sin(pi/2)")
print(result)  # 1.0

# Variables
result = evaluate("sqrt(x**2 + y**2)", {"x": 3, "y": 4})
print(result)  # 5.0
```

### Using ExpressionManager

```python
from expression_manager import ExpressionManager

manager = ExpressionManager()

# Set persistent variables
manager.set_variable("radius", 5.0)
manager.set_variable("height", 10.0)

# Evaluate expressions
volume = manager.evaluate_expression("pi * radius**2 * height")
print(f"Volume: {volume.value:.2f}")

# Batch processing
expressions = ["2 + 3", "sin(pi/4)", "sqrt(2)"]
results = manager.evaluate_batch(expressions)
for expr, result in zip(expressions, results):
    print(f"{expr} = {result.value:.6f}")
```

## API Reference

### ExpressionManager Class

The main interface for expression evaluation.

#### Methods

**`evaluate_expression(expression: str, variables: Dict[str, float] = None) -> EvaluationResult`**
- Evaluate a mathematical expression
- Returns: `EvaluationResult` with value or error information

**`validate_expression(expression: str) -> ValidationResult`**
- Validate expression syntax without evaluation
- Returns: `ValidationResult` with validation status

**`parse_expression(expression: str) -> ExpressionNode`**
- Parse expression into Abstract Syntax Tree
- Returns: Root node of the AST

**`set_variable(name: str, value: float) -> None`**
- Set a variable value

**`get_variable(name: str) -> float`**
- Get a variable value

**`clear_variables() -> None`**
- Clear all user-defined variables

### Convenience Functions

**`evaluate(expression: str, variables: Dict[str, float] = None) -> float`**
- Quick expression evaluation
- Raises: `ExpressionError` on failure

**`validate(expression: str) -> bool`**
- Quick expression validation
- Returns: `True` if valid, `False` otherwise

## Command Line Interface

The system includes a comprehensive CLI for interactive and batch processing.

### Basic Usage

```bash
# Evaluate single expression
python -m cli "2 + 3 * 4"

# Interactive mode
python -m cli --interactive

# Process file
python -m cli --file expressions.txt

# Use variables
python -m cli "x + y" --variables x=5 y=10
```

### CLI Options

```
usage: cli.py [-h] [--interactive | --file FILE] [--variables VARIABLES]
              [--precision PRECISION] [--format {decimal,scientific,engineering}]
              [--verbose] [--validate-only] [--show-ast] [--version]
              [expression]

Mathematical Expression Evaluator

positional arguments:
  expression            Mathematical expression to evaluate

optional arguments:
  -h, --help            show this help message and exit
  --interactive, -i     Start interactive mode
  --file FILE, -f FILE  File containing expressions to evaluate
  --variables VARIABLES, --vars VARIABLES, -v VARIABLES
                        Define variables (format: VAR=VALUE)
  --precision PRECISION, -p PRECISION
                        Number of decimal places for output (default: 6)
  --format {decimal,scientific,engineering}
                        Output format (default: decimal)
  --verbose             Enable verbose output
  --validate-only       Only validate expressions without evaluating
  --show-ast            Show Abstract Syntax Tree
  --version             show program's version number and exit
```

### Interactive Mode

```
>>> 2 + 3 * 4
14

>>> x = 10
x = 10

>>> sqrt(x)
3.162278

>>> :vars
Variables:
  x = 10
Constants:
  e = 2.718282
  pi = 3.141593
  tau = 6.283185

>>> :quit
```

## Examples

See `examples.py` for comprehensive usage examples including:

- Basic arithmetic and mathematical functions
- Variable management and custom functions
- Batch processing and performance optimization
- Scientific computing applications
- Error handling demonstrations

Run examples:
```bash
python examples.py
```

## Testing

The system includes a comprehensive test suite covering all components.

### Running Tests

```bash
# Run all tests
python -m pytest test_expression_evaluator.py -v

# Run specific test class
python -m pytest test_expression_evaluator.py::TestTokenizer -v

# Run with coverage
python -m pytest test_expression_evaluator.py --cov=. --cov-report=html
```

### Test Coverage

The test suite includes:
- Unit tests for all components (Tokenizer, Parser, Evaluator)
- Integration tests for ExpressionManager
- Performance requirement validation
- Error handling verification
- Edge case testing

## Architecture

The system follows a layered architecture:

```
┌─────────────────────────────────────┐
│           User Interface            │
│     (CLI, API, Web Interface)       │
├─────────────────────────────────────┤
│        Application Layer            │
│   (Expression Manager, Validators)  │
├─────────────────────────────────────┤
│           Core Engine               │
│    (Parser, Evaluator, AST)        │
├─────────────────────────────────────┤
│        Foundation Layer             │
│   (Tokenizer, Math Functions)      │
└─────────────────────────────────────┘
```

### Components

1. **Tokenizer**: Lexical analysis - converts expression strings into tokens
2. **Parser**: Syntax analysis - builds Abstract Syntax Trees from tokens
3. **Evaluator**: Executes AST to produce numerical results
4. **ExpressionManager**: High-level interface coordinating all components
5. **CLI**: Command-line interface for user interaction

## Performance

The system is designed to meet specific performance requirements:

### Performance Metrics
- Simple expressions (< 50 chars): < 1ms
- Complex expressions (50-500 chars): < 10ms
- Very complex expressions (500-1000 chars): < 100ms
- Batch processing: > 1000 expressions per second

### Optimization Features
- Expression result caching
- Efficient AST evaluation
- Memory usage optimization
- Configurable execution limits

### Performance Testing

```python
# Test simple expression performance
import time
from expression_manager import ExpressionManager

manager = ExpressionManager()
start = time.time()
result = manager.evaluate_expression("2 + 3 * 4")
end = time.time()

print(f"Time: {end - start:.6f} seconds")  # Should be < 0.001s
```

## Error Handling

The system provides comprehensive error handling with detailed messages:

### Error Types
- **Syntax Errors**: Invalid expression syntax
- **Evaluation Errors**: Mathematical domain errors (division by zero, etc.)
- **Variable Errors**: Undefined variables
- **Function Errors**: Unknown functions or incorrect arguments
- **Validation Errors**: Expression validation failures

### Error Information
- Clear error messages
- Position information where applicable
- Suggestions for fixing common errors
- Error codes for programmatic handling

## Contributing

This implementation follows the specification-first approach. Any contributions should:

1. First update the specifications if new features are proposed
2. Ensure all tests pass
3. Maintain performance requirements
4. Follow the existing code style and architecture
5. Include comprehensive documentation

## Specification Compliance

This implementation strictly adheres to the specifications outlined in `SPECIFICATIONS.md`. All features, requirements, and constraints defined in the specifications have been implemented and tested.

### Compliance Checklist
- ✅ All functional requirements (FR001-FR010)
- ✅ All non-functional requirements (NFR001-NFR005)
- ✅ All business rules and constraints
- ✅ API specifications
- ✅ Performance requirements
- ✅ Security considerations
- ✅ Error handling requirements

---

*This Expression Evaluator implementation demonstrates the power of the specification-first approach, resulting in a well-designed, thoroughly tested, and highly maintainable mathematical expression evaluation system.*