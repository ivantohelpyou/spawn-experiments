# Prime Number Generator

A comprehensive prime number generation and analysis application built with Python's standard library. This application provides multiple algorithms, validation capabilities, and performance benchmarking for working with prime numbers.

## Features

### Core Functionality
- **Multiple Algorithms**: Sieve of Eratosthenes, Trial Division, and Optimized Trial Division
- **Flexible Generation**: Generate primes up to a limit, first N primes, or primes within a range
- **Prime Validation**: Comprehensive validation with detailed explanations
- **Batch Processing**: Efficient validation of multiple numbers
- **Performance Analysis**: Detailed benchmarking and algorithm comparison

### Algorithm Selection
The application automatically selects the most appropriate algorithm based on input parameters:
- **Small ranges (≤1,000)**: Trial Division
- **Medium ranges (1,000-100,000)**: Optimized Trial Division
- **Large ranges (>100,000)**: Sieve of Eratosthenes

## Installation

No installation required! The application uses only Python's standard library.

### Requirements
- Python 3.7 or higher
- No external dependencies

### Quick Start
```bash
# Clone or download the application
cd prime-number-generator

# Make the main script executable (optional)
chmod +x main.py

# Run the application
python main.py --help
```

## Usage

### Command Line Interface

#### Generate Prime Numbers
```bash
# Generate primes up to 100
python main.py generate --limit 100

# Generate first 50 primes
python main.py generate --count 50

# Generate primes between 100 and 200
python main.py generate --range 100 200

# Use specific algorithm
python main.py generate --limit 1000 --algorithm sieve

# Include performance metrics
python main.py generate --limit 1000 --performance

# Save to file
python main.py generate --limit 1000 --output primes.txt
```

#### Validate Prime Numbers
```bash
# Validate single number
python main.py validate 97

# Validate multiple numbers
python main.py validate 97 98 99 100 101

# Include prime factors for composite numbers
python main.py validate 100 --factors

# Get batch summary statistics
python main.py validate 97 98 99 100 --summary

# JSON output
python main.py validate 97 98 99 --format json
```

#### Performance Benchmarking
```bash
# Quick benchmark comparison
python main.py benchmark --limit 10000

# Compare specific algorithms
python main.py benchmark --limit 10000 --algorithms sieve optimized_trial

# Comprehensive benchmark suite
python main.py benchmark --comprehensive

# Save results to file
python main.py benchmark --comprehensive --output benchmark_results.txt
```

#### Algorithm Information
```bash
# List available algorithms
python main.py algorithms

# Detailed algorithm information
python main.py algorithms --detailed
```

### Programmatic Usage

```python
from core import PrimeGenerator, PrimeValidator
from core import AlgorithmComparator, BenchmarkRunner

# Initialize components
generator = PrimeGenerator()
validator = PrimeValidator()

# Generate primes
primes = generator.generate_primes_up_to(100)
first_20 = generator.generate_first_n_primes(20)
range_primes = generator.generate_primes_in_range(50, 100)

# Validate numbers
result = validator.validate(97, include_factors=True)
print(f"97 is prime: {result.is_prime}")
print(f"Explanation: {result.explanation}")

# Performance comparison
comparator = AlgorithmComparator()
algorithms = {
    'sieve': lambda: generator.generate_primes_up_to(10000, 'sieve'),
    'optimized': lambda: generator.generate_primes_up_to(10000, 'optimized_trial')
}
comparison = comparator.compare_algorithms(algorithms, {'limit': 10000})
```

### Demonstration Mode
```bash
# Run built-in demonstration
python main.py --demo
```

## Architecture

### Project Structure
```
prime-number-generator/
├── main.py                 # Application entry point
├── core/                   # Core functionality
│   ├── algorithms.py       # Prime generation algorithms
│   ├── validators.py       # Prime validation logic
│   ├── performance.py      # Performance monitoring
│   └── __init__.py
├── utils/                  # Utility functions
│   ├── helpers.py          # Helper functions
│   ├── exceptions.py       # Custom exceptions
│   └── __init__.py
├── cli/                    # Command-line interface
│   ├── interface.py        # CLI implementation
│   └── __init__.py
├── SPECIFICATIONS.md       # Detailed specifications
└── README.md              # This file
```

### Core Components

#### Algorithms (`core/algorithms.py`)
- `SieveOfEratosthenes`: Efficient for large ranges
- `TrialDivision`: Simple, memory-efficient
- `OptimizedTrialDivision`: Enhanced with caching
- `PrimeGenerator`: Unified interface with automatic algorithm selection

#### Validators (`core/validators.py`)
- `PrimeValidator`: Single number validation with explanations
- `BatchValidator`: Efficient multiple number validation
- Detailed explanations and prime factorization

#### Performance (`core/performance.py`)
- `PerformanceMonitor`: Execution time and memory tracking
- `AlgorithmComparator`: Side-by-side algorithm comparison
- `BenchmarkRunner`: Standardized performance tests

## Performance Characteristics

### Algorithm Comparison
| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| Sieve of Eratosthenes | O(n log log n) | O(n) | Large ranges |
| Trial Division | O(√n) per number | O(1) | Single numbers |
| Optimized Trial | O(√n) per number | O(√n) | Medium ranges |

### Benchmarks
On a typical modern system:
- Generate primes up to 1,000: < 10ms
- Generate primes up to 100,000: < 1s
- Generate primes up to 1,000,000: < 10s
- Validate large prime (10^9): < 100ms

## Examples

### Basic Generation
```bash
$ python main.py generate --limit 30
Generated primes up to 30
Found 10 prime numbers

Prime numbers:
     2      3      5      7     11     13     17     19     23     29
```

### Validation with Explanations
```bash
$ python main.py validate 97 98 99 100 --factors

Number: 97
Is Prime: True
Explanation: 97 is prime. It has no positive divisors other than 1 and 97.

Number: 98
Is Prime: False
Explanation: 98 is even and greater than 2, so it is divisible by 2 and therefore not prime.
Prime Factors: 2 × 7 × 7

Number: 99
Is Prime: False
Explanation: 99 is not prime. It is divisible by 3 (and 33).
Prime Factors: 3 × 3 × 11

Number: 100
Is Prime: False
Explanation: 100 is even and greater than 2, so it is divisible by 2 and therefore not prime.
Prime Factors: 2 × 2 × 5 × 5
```

### Performance Benchmarking
```bash
$ python main.py benchmark --limit 10000
Algorithm Comparison Report: Algorithm Comparison
================================================

Test Parameters:
  limit: 10000

Results:
  sieve:
    Time: 2.45 ms
    Memory: 45.2 KB
    Results: 1,229 items

  optimized_trial:
    Time: 45.3 ms
    Memory: 12.1 KB
    Results: 1,229 items

  trial_division:
    Time: 123.7 ms
    Memory: 8.5 KB
    Results: 1,229 items

Fastest Algorithm: sieve
Most Memory Efficient: trial_division

Recommendations:
  • Significant performance difference detected. Use 'sieve' for best speed.
  • For large limits, consider using Sieve of Eratosthenes
```

## Error Handling

The application provides comprehensive error handling with clear, actionable error messages:

```bash
# Invalid input
$ python main.py generate --limit -5
Error: limit must be a positive integer, got -5

# Invalid range
$ python main.py generate --range 100 50
Error: Range start (100) must be <= end (50)

# Memory limit exceeded
$ python main.py generate --limit 100000000
Error: Estimated memory usage (100000000 bytes) exceeds limit
```

## Mathematical Background

### Prime Numbers
A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. The sequence of prime numbers begins: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ...

### Algorithms Implemented

#### Sieve of Eratosthenes
An ancient algorithm that finds all primes up to a given limit by iteratively marking composite numbers. Highly efficient for generating all primes in a range.

#### Trial Division
Tests primality by checking divisibility up to √n. Simple and memory-efficient, suitable for testing individual numbers or small ranges.

#### Optimized Trial Division
Enhanced version with pre-computed small primes cache and optimized trial sequence, providing better performance for medium-sized ranges.

## Contributing

This application is part of a specification-driven development experiment. The implementation strictly follows the comprehensive specifications in `SPECIFICATIONS.md`.

### Development Guidelines
- All code uses Python standard library only
- Comprehensive error handling and input validation
- Type hints throughout the codebase
- Detailed docstrings and comments
- Performance-conscious implementation

## License

This project is released under the MIT License.

## Version History

- **v1.0.0**: Initial release with comprehensive prime number generation and analysis capabilities

---

For detailed technical specifications, see [SPECIFICATIONS.md](SPECIFICATIONS.md).