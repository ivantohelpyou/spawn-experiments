# Anagram Grouper - Detailed Specifications

## 1. Core Functional Requirements

The anagram grouper function must:
- Take a list of strings as input
- Group strings that are anagrams of each other
- Return a list of lists, where each inner list contains anagrams
- Preserve original string casing and spacing in output
- Handle empty strings and single-character strings appropriately

## 2. Function Signature and Interface Design

```python
def group_anagrams(words: List[str]) -> List[List[str]]:
    """
    Groups words that are anagrams of each other.

    Args:
        words: List of strings to group by anagrams

    Returns:
        List of lists, where each inner list contains words that are anagrams

    Raises:
        TypeError: If input is not a list or contains non-string elements
    """
```

## 3. Algorithm Approach and Data Structure Choices

**Primary Algorithm**: Signature-based grouping
- Use sorted characters as anagram signature
- Dictionary mapping signatures to word groups
- Time Complexity: O(n * m log m) where n = number of words, m = average word length
- Space Complexity: O(n * m) for storing all words and signatures

**Data Structures**:
- Input: List[str]
- Internal: Dict[str, List[str]] (signature -> anagram group)
- Output: List[List[str]]

## 4. Input Validation and Edge Case Handling

**Input Validation**:
- Must be a list
- All elements must be strings
- Raise TypeError for invalid inputs

**Edge Cases**:
- Empty list: return empty list
- Single word: return list with single group
- No anagrams: return list of single-word groups
- Duplicate words: group together
- Empty strings: group together
- Single characters: group identical characters

## 5. Performance Requirements and Constraints

**Requirements**:
- Handle up to 10,000 words efficiently
- Support words up to 100 characters
- Memory usage should be reasonable (no excessive duplication)

**Constraints**:
- Case-insensitive anagram detection
- Whitespace and punctuation considered in anagram logic
- Preserve original string formatting in output

## 6. Error Handling and Edge Cases

**Error Conditions**:
- Non-list input: raise TypeError
- Non-string elements: raise TypeError
- None input: raise TypeError

**Edge Cases**:
- Empty list: return []
- List with empty string: return [[""]]
- Single word: return [[word]]
- All words are anagrams: return [all_words]
- No anagrams exist: return [[word] for word in words]

## 7. Expected Behavior with Different Input Types

**Valid Cases**:
- `["eat", "tea", "tan", "ate", "nat", "bat"]` → `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`
- `[""]` → `[[""]]`
- `["a"]` → `[["a"]]`
- `[]` → `[]`
- `["abc", "bca", "cab"]` → `[["abc", "bca", "cab"]]`

**Case Sensitivity**:
- `["Eat", "tea", "Tea"]` → `[["Eat", "tea", "Tea"]]` (case-insensitive grouping)

**Special Characters**:
- `["a!b", "b!a", "ab!"]` → `[["a!b", "b!a", "ab!"]]`
- `["a b", "b a", " ab"]` → `[["a b", "b a"], [" ab"]]` (spaces matter)