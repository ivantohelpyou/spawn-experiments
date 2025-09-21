# Prime Number Generator - Test-Driven Development Implementation

A comprehensive prime number generator implemented using strict Test-Driven Development (TDD) principles with Python standard library only.

## Overview

This project demonstrates a complete TDD implementation cycle, following the Red-Green-Refactor methodology for every feature. The implementation provides efficient algorithms for prime number generation and validation with comprehensive error handling and optimization.

## Features

### Core Functionality
- **Prime Number Validation**: Determine if a given number is prime
- **Bulk Prime Generation**: Generate all primes up to a specified limit using Sieve of Eratosthenes
- **Range-based Generation**: Generate primes within a specific range
- **Nth Prime Finding**: Find the nth prime number with optimized upper bound estimation

### Advanced Features
- Optimized algorithms (6k±1 optimization for prime checking)
- Comprehensive error handling with custom exceptions
- Input validation for all functions
- Performance optimization for large numbers
- Mathematical property verification (twin primes, gaps analysis)

## TDD Implementation Process

### Phase 1: Specifications
Created detailed specifications including:
- Core functional requirements
- User stories with acceptance criteria
- Technical architecture overview
- API design
- Business rules and validation requirements
- Error handling and edge cases

### Phase 2: TDD Implementation

#### Strict Red-Green-Refactor Cycle
For each feature:

1. **RED**: Write failing tests first
   - Unit tests for individual components
   - Integration tests for component interactions
   - Edge case and error condition tests

2. **GREEN**: Write minimal implementation code
   - Only enough code to make tests pass
   - No additional functionality beyond test requirements

3. **REFACTOR**: Clean up code while keeping tests green
   - Improve structure and readability
   - Add documentation
   - Optimize algorithms
   - Maintain 100% test coverage

#### Implementation Order
1. Core prime checking functionality (7 tests)
2. Prime number generator with bulk generation (16 tests)
3. Integration tests for component interaction (8 tests)

## Project Structure

```
prime_generator/
├── __init__.py          # Package initialization and exports
├── core.py              # Core prime checking logic (PrimeChecker)
├── generator.py         # Prime generation algorithms (PrimeGenerator)
└── exceptions.py        # Custom exception classes

tests/
├── __init__.py
├── test_core.py         # Unit tests for core functionality
├── test_generator.py    # Unit tests for generation algorithms
└── test_integration.py  # Integration tests

specifications.md        # Detailed technical specifications
demo.py                 # Comprehensive demonstration script
README.md               # This documentation
```

## API Reference

### PrimeChecker

```python
@staticmethod
def is_prime(n: int) -> bool:
    """Check if a number is prime using optimized trial division."""
```

### PrimeGenerator

```python
@staticmethod
def generate_up_to(limit: int) -> List[int]:
    """Generate all prime numbers up to and including limit."""

@staticmethod
def generate_in_range(start: int, end: int) -> List[int]:
    """Generate prime numbers in the range [start, end]."""

@staticmethod
def nth_prime(n: int) -> int:
    """Find the nth prime number."""
```

## Usage Examples

```python
from prime_generator import PrimeChecker, PrimeGenerator

# Check if a number is prime
PrimeChecker.is_prime(17)  # True
PrimeChecker.is_prime(18)  # False

# Generate primes up to a limit
primes = PrimeGenerator.generate_up_to(30)
# Result: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

# Generate primes in a range
range_primes = PrimeGenerator.generate_in_range(10, 20)
# Result: [11, 13, 17, 19]

# Find the nth prime
tenth_prime = PrimeGenerator.nth_prime(10)
# Result: 29
```

## Running the Code

### Run the Demo
```bash
python demo.py
```

### Run All Tests
```bash
python -m unittest discover tests -v
```

### Run Specific Test Modules
```bash
python -m unittest tests.test_core -v
python -m unittest tests.test_generator -v
python -m unittest tests.test_integration -v
```

## Test Coverage

- **Total Tests**: 31 tests
- **Unit Tests**: 23 tests (core + generator functionality)
- **Integration Tests**: 8 tests (component interaction and workflows)
- **Coverage**: 100% of implemented functionality
- **Test Types**:
  - Functionality tests
  - Edge case tests
  - Error handling tests
  - Performance regression tests
  - Mathematical property verification

## Algorithm Details

### Prime Checking (PrimeChecker.is_prime)
- Optimized trial division with 6k±1 optimization
- Early termination for special cases (≤3, even numbers, multiples of 3)
- Only checks divisors up to √n
- Time Complexity: O(√n)

### Bulk Generation (PrimeGenerator.generate_up_to)
- Sieve of Eratosthenes algorithm
- Memory efficient for large limits
- Time Complexity: O(n log log n)
- Space Complexity: O(n)

### Nth Prime Finding (PrimeGenerator.nth_prime)
- Uses prime number theorem for upper bound estimation
- Applies bulk generation with estimated bounds
- Automatic bound adjustment if needed
- Optimized for common use cases

## Error Handling

Comprehensive error handling with custom exceptions:

- **TypeError**: For non-integer inputs
- **ValueError**: For negative numbers, invalid ranges, or invalid positions
- **Clear error messages**: With suggestions for valid inputs

## Performance Characteristics

Based on demo results:
- Generate 1,229 primes up to 10,000: ~1.3ms
- Find 1000th prime (7919): ~1.3ms
- Check large prime (982,451,653): ~0.8ms
- All operations complete well within performance requirements

## TDD Benefits Demonstrated

1. **Comprehensive Test Coverage**: Every line of code written was driven by a failing test
2. **Robust Error Handling**: All edge cases identified and handled through test-first approach
3. **Clean Architecture**: Modular design emerged naturally from test requirements
4. **Refactoring Safety**: Extensive test suite enables confident code improvements
5. **Documentation by Tests**: Tests serve as executable specification
6. **Performance Assurance**: Performance regression tests prevent degradation

## Mathematical Properties Verified

- Twin primes identification (primes differing by 2)
- Prime gap analysis
- Verification that 2 is the only even prime
- Consistency between different generation methods
- Large-scale mathematical correctness (100th prime = 541)

## Technology Stack

- **Language**: Python 3.x
- **Libraries**: Standard library only (no external dependencies)
- **Testing**: unittest (built-in testing framework)
- **Algorithms**: Sieve of Eratosthenes, optimized trial division

## Development Methodology

This project strictly followed TDD principles:
- No implementation code written before tests
- All tests must fail before implementation
- Minimal code to pass tests
- Refactoring only after tests pass
- Continuous test execution to maintain green state

The result is a robust, well-tested, and maintainable prime number generator that demonstrates the power of Test-Driven Development.