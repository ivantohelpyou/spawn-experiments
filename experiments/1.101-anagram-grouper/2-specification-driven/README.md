# Anagram Grouper - Specification-Driven Implementation

This directory contains a comprehensive, specification-driven implementation of an anagram grouper function. The development followed a rigorous two-phase approach: detailed specifications first, then complete implementation.

## 📁 Project Structure

```
2-specification-driven/
├── anagram_grouper_specifications.md  # Comprehensive specifications document
├── anagram_grouper.py                 # Main implementation
├── test_anagram_grouper.py           # Comprehensive test suite
├── demo.py                           # Interactive demonstration
└── README.md                         # This file
```

## 🎯 Development Approach

### Phase 1: Comprehensive Specifications
- **Complete feature analysis** - All requirements and edge cases identified
- **API design** - Function signatures and parameter options defined
- **Algorithm planning** - Data structures and approach documented
- **Performance targets** - Specific benchmarks and constraints set
- **Quality standards** - Testing and documentation requirements specified

### Phase 2: Specification-Compliant Implementation
- **Full feature implementation** - All specified features included
- **Comprehensive testing** - Extensive test suite covering all edge cases
- **Performance validation** - Meets all specified performance targets
- **Documentation** - Complete docstrings and examples

## ✨ Key Features

### Core Functionality
- **Anagram Detection**: Groups strings with identical character frequencies
- **Case Sensitivity**: Configurable case-sensitive or case-insensitive grouping
- **Multiple Output Formats**: List of lists or dictionary format
- **Flexible Sorting**: Configurable sorting of groups and within groups
- **Unicode Support**: Proper handling of international characters

### Advanced Features
- **Input Validation**: Comprehensive error checking and helpful error messages
- **Edge Case Handling**: Empty strings, whitespace, duplicates, special characters
- **Performance Optimization**: Efficient algorithms for large datasets
- **Utility Functions**: Additional helper functions for common use cases

## 🚀 Quick Start

### Basic Usage
```python
from anagram_grouper import group_anagrams

# Simple anagram grouping
words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
groups = group_anagrams(words)
print(groups)
# Output: [['ate', 'eat', 'tea'], ['nat', 'tan'], ['bat']]
```

### Advanced Usage
```python
# Case-sensitive grouping with dictionary output
words = ['Eat', 'Tea', 'ate', 'Listen', 'Silent']
result = group_anagrams(
    words,
    case_sensitive=True,
    output_format='dict',
    sort_groups=True
)
print(result)
# Output: {'Eat': ['Eat'], 'Tae': ['Tea'], 'aet': ['ate'], ...}
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Install pytest if needed
pip install pytest

# Run all tests
pytest test_anagram_grouper.py -v

# Run with coverage
pytest test_anagram_grouper.py --cov=anagram_grouper
```

## 🎮 Interactive Demonstration

Run the demonstration script to see all features in action:
```bash
python demo.py
```

This will showcase:
- Basic anagram grouping
- Case sensitivity options
- Output format variations
- Sorting configurations
- Edge case handling
- Utility functions
- Performance characteristics
- Real-world usage example

## 📊 Performance Characteristics

The implementation meets these performance targets:
- **Small collections** (< 100 strings): < 1ms
- **Medium collections** (100-1000 strings): < 100ms
- **Large collections** (1000-10000 strings): < 1s
- **Memory efficiency**: ~2x input size overhead

**Time Complexity**: O(n × m × log(m)) where n = number of strings, m = average string length
**Space Complexity**: O(n × m) for storing results

## 🛠 API Reference

### Main Function
```python
group_anagrams(
    words: Iterable[str],
    case_sensitive: bool = False,
    sort_groups: bool = True,
    sort_within_groups: bool = True,
    output_format: str = 'list'
) -> Union[List[List[str]], Dict[str, List[str]]]
```

### Utility Functions
```python
count_anagram_groups(words, case_sensitive=False) -> int
find_largest_anagram_group(words, case_sensitive=False) -> List[str]
are_anagrams(word1, word2, case_sensitive=False) -> bool
```

## 🔍 Specification Compliance

This implementation fully complies with the comprehensive specifications in `anagram_grouper_specifications.md`, including:

- ✅ All core and advanced features
- ✅ Complete input validation and error handling
- ✅ All edge cases properly handled
- ✅ Performance targets met
- ✅ Unicode and special character support
- ✅ Flexible configuration options
- ✅ Comprehensive test coverage
- ✅ Full documentation

## 🎯 Use Cases

### Word Games
- Scrabble anagram finding
- Word puzzle solving
- Crossword assistance

### Text Analysis
- Linguistic research
- Content analysis
- Data deduplication

### Educational Tools
- Teaching string algorithms
- Demonstrating hash table usage
- Algorithm complexity analysis

## 🔬 Technical Details

### Algorithm Approach
1. **Canonical Form Generation**: Sort characters to create comparable keys
2. **Grouping**: Use dictionary with canonical forms as keys
3. **Unicode Normalization**: Proper handling of international characters
4. **Efficient Sorting**: Built-in Python sorting for optimal performance

### Key Design Decisions
- **Defaultdict**: Efficient grouping without key checking
- **Unicode Normalization**: NFC normalization for consistency
- **Preserving Original Format**: Maintain input case and formatting
- **Configurable Behavior**: Multiple options for different use cases

## 📋 Requirements

- Python 3.6+
- No external dependencies for core functionality
- pytest (for running tests)

## 🤝 Contributing

When contributing to this implementation:
1. Ensure all specifications in `anagram_grouper_specifications.md` are maintained
2. Add comprehensive tests for any new features
3. Update documentation and examples
4. Verify performance characteristics are maintained
5. Follow the established code style and patterns

---

This specification-driven implementation demonstrates how comprehensive upfront planning leads to robust, well-tested, and fully-featured software that meets all requirements.