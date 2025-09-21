# Prime Number Generator

A comprehensive prime number toolkit built with Python's standard library only. This application provides both an interactive command-line interface and command-line arguments for batch operations and scripting.

## Features

### Core Algorithms
- **Multiple Prime Checking Methods**: Basic trial division, optimized trial division, and cached checking
- **Sieve of Eratosthenes**: Efficient prime generation for ranges
- **Prime Factorization**: Complete factorization with powers
- **Mersenne Prime Detection**: Check for primes of the form 2^p - 1
- **Prime Gap Analysis**: Analyze spacing between consecutive primes
- **Performance Benchmarking**: Compare algorithm performance

### User Interface
- **Interactive CLI**: Full-featured menu-driven interface
- **Command-Line Arguments**: Batch operations and scripting support
- **Educational Mode**: Built-in explanations of prime number concepts
- **Multiple Output Formats**: List, grid, and count formats
- **Timing Information**: Performance measurement for operations

## Quick Start

### Interactive Mode
```bash
python main.py
```
This launches the full interactive interface with menu options for all features.

### Command-Line Examples
```bash
# Check if a number is prime
python main.py --check 97

# Generate all primes up to 100
python main.py --generate 100

# Get the first 20 prime numbers
python main.py --first 20

# Prime factorization
python main.py --factorize 84

# Check multiple numbers at once
python main.py --batch "2,3,4,17,25,29"

# Find next prime after 50
python main.py --next 50

# Analyze prime gaps up to 100
python main.py --gaps 100

# Check Mersenne prime 2^13-1
python main.py --mersenne 13

# Benchmark algorithms up to 1000
python main.py --benchmark 1000
```

### Advanced Options
```bash
# Use different algorithms
python main.py --generate 1000 --method sieve

# Show timing information
python main.py --first 100 --timing

# Verbose output with extra details
python main.py --check 97 --verbose

# Different output formats
python main.py --generate 50 --format grid
```

## Files Structure

- `main.py` - Main entry point with command-line argument support
- `prime_generator.py` - Core prime number algorithms and utilities
- `cli_interface.py` - Interactive command-line interface
- `README.md` - This documentation file

## Algorithms Implemented

### Prime Checking
1. **Basic Trial Division**: O(√n) complexity, checks all divisors
2. **Optimized Trial Division**: Uses 6k±1 optimization, ~3x faster
3. **Cached Method**: Builds cache of known primes for repeated checks

### Prime Generation
1. **Sieve of Eratosthenes**: Most efficient for generating many primes
2. **Incremental Generation**: Generate first N primes
3. **Range Generation**: All primes up to a given limit

### Special Features
- **Prime Factorization**: Complete factorization with powers
- **Mersenne Prime Testing**: For primes of form 2^p - 1
- **Gap Analysis**: Study spacing between consecutive primes
- **Performance Benchmarking**: Compare different algorithms

## Interactive Features

The interactive mode provides:
- Prime checking with method selection
- Prime generation with various algorithms
- Educational content explaining prime number concepts
- Prime factorization with verification
- Mersenne prime exploration
- Gap analysis with statistics
- Performance benchmarking
- Batch operations
- Operation history tracking
- Settings and cache management

## Educational Content

The application includes built-in educational content covering:
- What are prime numbers?
- Prime checking algorithms and their complexity
- Mersenne primes and their significance
- Prime gaps and their mathematical properties
- Prime factorization and its applications

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Usage Examples

### Programming Interface
```python
from prime_generator import PrimeGenerator

# Create generator instance
gen = PrimeGenerator()

# Check if number is prime
print(gen.is_prime(97))  # True

# Generate primes up to 100
primes = gen.generate_primes_up_to(100)

# Get first 10 primes
first_ten = gen.generate_first_n_primes(10)

# Prime factorization
factors = gen.prime_factorization(60)  # [(2, 2), (3, 1), (5, 1)]
```

### Command-Line Scripting
```bash
# Check primality in a script
if python main.py --check 97 | grep -q "prime"; then
    echo "97 is prime!"
fi

# Generate primes for further processing
python main.py --generate 1000 --format count
```

## Performance

The application includes multiple algorithms optimized for different use cases:
- **Sieve of Eratosthenes**: Best for generating many primes (O(n log log n))
- **Optimized Trial Division**: Best for checking individual numbers
- **Cached Method**: Best for repeated prime checks

Benchmark your specific use case with the `--benchmark` option.

## License

This project is released under the MIT License. Feel free to use, modify, and distribute.

## Contributing

This is a demonstration project showcasing comprehensive prime number functionality using only Python's standard library. Contributions and improvements are welcome!