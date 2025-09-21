# Prime Number Generator - Technical Specifications

## 1. Core Functional Requirements

### Primary Functions
- **Prime Number Validation**: Determine if a given number is prime
- **Prime Number Generation**: Generate prime numbers up to a specified limit
- **Range-based Generation**: Generate prime numbers within a specific range
- **Nth Prime Finding**: Find the nth prime number

### Performance Requirements
- Efficient algorithm for large numbers (up to 1,000,000)
- Memory-efficient storage for generated primes
- Fast validation for repeated checks

## 2. User Stories with Acceptance Criteria

### Story 1: Prime Number Validation
**As a** developer
**I want** to check if a number is prime
**So that** I can validate prime numbers in my applications

**Acceptance Criteria:**
- Given a positive integer, return True if prime, False otherwise
- Handle edge cases: 0, 1, 2, negative numbers
- Raise appropriate exceptions for invalid inputs (non-integers, None)

### Story 2: Generate Primes Up To Limit
**As a** mathematician
**I want** to generate all prime numbers up to a given limit
**So that** I can analyze prime number patterns

**Acceptance Criteria:**
- Given a positive integer limit, return list of all primes <= limit
- Return empty list for limits < 2
- Handle large limits efficiently (up to 1,000,000)

### Story 3: Generate Primes in Range
**As a** researcher
**I want** to find prime numbers within a specific range
**So that** I can focus on particular number intervals

**Acceptance Criteria:**
- Given start and end integers, return primes in [start, end]
- Handle cases where start > end
- Validate that both parameters are positive integers

### Story 4: Find Nth Prime
**As a** student
**I want** to find the nth prime number
**So that** I can solve mathematical problems

**Acceptance Criteria:**
- Given a positive integer n, return the nth prime number
- Handle edge cases: n = 1 (return 2), n <= 0 (raise exception)
- Efficient computation for reasonable values of n (up to 10,000th prime)

## 3. Technical Architecture Overview

### Module Structure
```
prime_generator/
├── __init__.py
├── core.py           # Core prime checking logic
├── generator.py      # Prime generation algorithms
├── validator.py      # Input validation utilities
└── exceptions.py     # Custom exception classes

tests/
├── __init__.py
├── test_core.py      # Unit tests for core functionality
├── test_generator.py # Unit tests for generation algorithms
├── test_validator.py # Unit tests for validation
└── test_integration.py # Integration tests
```

### Class Design
```python
class PrimeChecker:
    """Handles prime number validation"""
    @staticmethod
    def is_prime(n: int) -> bool

class PrimeGenerator:
    """Handles prime number generation"""
    @staticmethod
    def generate_up_to(limit: int) -> List[int]
    @staticmethod
    def generate_in_range(start: int, end: int) -> List[int]
    @staticmethod
    def nth_prime(n: int) -> int
```

## 4. Data Models and Relationships

### Input Data Models
- **Integer**: Primary input type for all operations
- **Range**: Tuple of (start, end) integers for range operations

### Output Data Models
- **Boolean**: Result of prime checking operations
- **List[int]**: Collection of prime numbers
- **Integer**: Single prime number result

### Relationships
- PrimeChecker is used by PrimeGenerator for validation
- All generators depend on core prime checking algorithm
- Validation layer wraps all public interfaces

## 5. API Design

### PrimeChecker API
```python
def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n: Integer to check

    Returns:
        True if n is prime, False otherwise

    Raises:
        TypeError: If n is not an integer
        ValueError: If n is negative
    """
```

### PrimeGenerator API
```python
def generate_up_to(limit: int) -> List[int]:
    """
    Generate all prime numbers up to and including limit.

    Args:
        limit: Upper bound for prime generation

    Returns:
        List of prime numbers <= limit

    Raises:
        TypeError: If limit is not an integer
        ValueError: If limit is negative
    """

def generate_in_range(start: int, end: int) -> List[int]:
    """
    Generate prime numbers in the range [start, end].

    Args:
        start: Lower bound (inclusive)
        end: Upper bound (inclusive)

    Returns:
        List of prime numbers in range

    Raises:
        TypeError: If start or end is not an integer
        ValueError: If start or end is negative, or start > end
    """

def nth_prime(n: int) -> int:
    """
    Find the nth prime number.

    Args:
        n: Position of prime to find (1-indexed)

    Returns:
        The nth prime number

    Raises:
        TypeError: If n is not an integer
        ValueError: If n <= 0
    """
```

## 6. Business Rules and Validation Requirements

### Input Validation Rules
1. **Type Validation**: All numeric inputs must be integers
2. **Range Validation**: All inputs must be non-negative (except where specified)
3. **Logical Validation**: For ranges, start <= end

### Prime Number Business Rules
1. **Definition**: A prime number is a natural number > 1 with exactly two divisors: 1 and itself
2. **Special Cases**:
   - 0 and 1 are not prime by definition
   - 2 is the only even prime number
   - Negative numbers are not considered prime

### Performance Rules
1. **Efficiency**: Use optimized algorithms (Sieve of Eratosthenes for bulk generation)
2. **Memory**: Limit memory usage for large ranges
3. **Caching**: Consider caching for repeated operations

## 7. Error Handling and Edge Cases

### Exception Hierarchy
```python
class PrimeGeneratorError(Exception):
    """Base exception for prime generator errors"""

class InvalidInputError(PrimeGeneratorError):
    """Raised when input validation fails"""

class ComputationError(PrimeGeneratorError):
    """Raised when computation fails or exceeds limits"""
```

### Edge Cases to Handle

#### Prime Checking Edge Cases
- `is_prime(0)` → False
- `is_prime(1)` → False
- `is_prime(2)` → True
- `is_prime(-5)` → ValueError
- `is_prime(3.14)` → TypeError
- `is_prime(None)` → TypeError

#### Generation Edge Cases
- `generate_up_to(0)` → []
- `generate_up_to(1)` → []
- `generate_up_to(2)` → [2]
- `generate_in_range(5, 3)` → ValueError
- `generate_in_range(-2, 5)` → ValueError
- `nth_prime(0)` → ValueError
- `nth_prime(-1)` → ValueError
- `nth_prime(1)` → 2

### Error Messages
- Clear, descriptive error messages
- Include valid input ranges in error messages
- Provide suggestions for fixing invalid inputs

## 8. Testing Strategy

### Unit Testing
- Test each function with valid inputs
- Test all edge cases and error conditions
- Test boundary conditions
- Aim for 100% code coverage

### Integration Testing
- Test interaction between PrimeChecker and PrimeGenerator
- Test end-to-end workflows
- Performance testing with large inputs

### Test Data
- Small primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
- Large primes: 997, 1009, 7919
- Composite numbers: 4, 6, 8, 9, 10, 12, 15, 16
- Edge cases: 0, 1, 2, negative numbers

## 9. Implementation Notes

### Algorithm Selection
- **Trial Division**: For individual prime checking (optimized)
- **Sieve of Eratosthenes**: For generating multiple primes
- **Segmented Sieve**: For large ranges to manage memory

### Optimization Strategies
- Check divisibility by 2 first, then odd numbers only
- Only check divisors up to sqrt(n)
- Use wheel factorization for advanced optimization
- Implement early termination conditions

This specification will guide the TDD implementation process, ensuring all requirements are met through comprehensive testing.