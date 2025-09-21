# Anagram Grouper

A comprehensive Python implementation for grouping anagrams together.

## Features

- **Main Function**: `group_anagrams(words)` - Groups anagrams from a list of words
- **Statistics**: `group_anagrams_with_stats(words)` - Provides grouping with statistics
- **Find Anagrams**: `find_anagrams_of_word(target, word_list)` - Find anagrams of a specific word
- **Check Anagrams**: `is_anagram(word1, word2)` - Check if two words are anagrams
- **Case Insensitive**: Handles mixed case input
- **Edge Case Handling**: Empty lists, whitespace, invalid input types
- **Input Validation**: Comprehensive error checking and type validation

## Usage

### Basic Grouping

```python
from anagram_grouper import group_anagrams

words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
result = group_anagrams(words)
print(result)  # [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
```

### With Statistics

```python
from anagram_grouper import group_anagrams_with_stats

result = group_anagrams_with_stats(['eat', 'tea', 'bat'])
print(result['groups'])  # [['eat', 'tea'], ['bat']]
print(result['stats'])   # {'total_words': 3, 'total_groups': 2, ...}
```

### Find Anagrams of Specific Word

```python
from anagram_grouper import find_anagrams_of_word

anagrams = find_anagrams_of_word('eat', ['tea', 'bat', 'ate', 'hello'])
print(anagrams)  # ['ate', 'tea']
```

### Check if Two Words are Anagrams

```python
from anagram_grouper import is_anagram

print(is_anagram('listen', 'silent'))  # True
print(is_anagram('hello', 'world'))    # False
```

## Running the Demo

```bash
python anagram_grouper.py
```

## Running Tests

```bash
python test_anagram_grouper.py
```

## Edge Cases Handled

- Empty input lists
- Single word lists
- Non-string input (raises TypeError)
- Mixed case input
- Whitespace in words
- Duplicate words
- Empty strings and whitespace-only strings

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)