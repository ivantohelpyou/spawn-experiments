# Tier 1: Function-Level Experiments (Crawl)

## Experiment Design Philosophy

**Scope**: Pure algorithmic problems, single functions, stdlib only
**Goal**: Isolate methodology differences without architectural complexity
**Duration**: 5-15 minutes per approach
**Output**: Single function with comprehensive tests

## Constraint Profile

### Technical Constraints
- **Dependencies**: Python standard library only
- **Structure**: Single module, single primary function
- **Input/Output**: Function parameters and return values only
- **Testing**: pytest with stdlib assertions

### Specification Format
```
"Implement a function `function_name(params) -> return_type` that [clear requirement].
Use only Python standard library. Include comprehensive tests."
```

## Experiment List

### 010: Palindrome Detector
**Function**: `is_palindrome(text: str) -> bool`
**Requirement**: Return True if text reads same forwards/backwards, ignoring case and non-alphanumeric
**Test Cases**: "A man a plan a canal Panama", "race a car", "Madam", ""
**Complexity**: String manipulation, normalization logic

### 011: Prime Number Generator
**Function**: `generate_primes(limit: int) -> List[int]`
**Requirement**: Return all prime numbers up to (and including) limit
**Test Cases**: limit=10 → [2,3,5,7], limit=1 → [], limit=2 → [2]
**Complexity**: Algorithm choice (sieve vs trial division), optimization

### 012: Anagram Grouper
**Function**: `group_anagrams(words: List[str]) -> List[List[str]]`
**Requirement**: Group words that are anagrams of each other
**Test Cases**: ["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"],["tan","nat"],["bat"]]
**Complexity**: Hash key strategy, grouping logic

### 013: Roman Numeral Converter
**Function**: `int_to_roman(num: int) -> str`
**Requirement**: Convert integer (1-3999) to Roman numeral
**Test Cases**: 1994 → "MCMXCIV", 58 → "LVIII", 9 → "IX"
**Complexity**: Mapping strategy, edge cases

### 014: Balanced Parentheses Checker
**Function**: `is_balanced(expression: str) -> bool`
**Requirement**: Check if parentheses/brackets/braces are properly balanced
**Test Cases**: "{[()]}" → True, "([)]" → False, "" → True
**Complexity**: Stack management, character matching

### 015: Longest Common Subsequence
**Function**: `lcs_length(str1: str, str2: str) -> int`
**Requirement**: Return length of longest common subsequence
**Test Cases**: "ABCDGH", "AEDFHR" → 3 ("ADH")
**Complexity**: Dynamic programming vs recursive approach

### 016: Word Frequency Counter
**Function**: `count_words(text: str) -> Dict[str, int]`
**Requirement**: Count frequency of each word (case-insensitive, alphanumeric only)
**Test Cases**: "Hello world! Hello." → {"hello": 2, "world": 1}
**Complexity**: Text normalization, counting strategy

### 017: Binary Tree Traversal
**Function**: `inorder_traversal(root: TreeNode) -> List[int]`
**Requirement**: Return inorder traversal of binary tree (with provided TreeNode class)
**Test Cases**: Tree [1,null,2,3] → [1,3,2]
**Complexity**: Recursion vs iteration, tree structure handling

### 018: Rate Limiter
**Function**: `RateLimiter.__init__(max_calls: int, window_seconds: int)` + `allow_request() -> bool`
**Requirement**: Allow max_calls requests per window_seconds
**Test Cases**: 3 calls/5 seconds → [True,True,True,False,False, wait 5s, True]
**Complexity**: Time window management, state tracking

### 019: Merge Intervals
**Function**: `merge_intervals(intervals: List[List[int]]) -> List[List[int]]`
**Requirement**: Merge overlapping intervals
**Test Cases**: [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]
**Complexity**: Sorting strategy, overlap detection

## Expected Methodology Patterns

### Immediate Implementation
- Direct algorithmic approach
- Minimal error handling
- Basic test coverage
- Quick to working solution

### Specification-Driven
- Detailed function docstrings
- Comprehensive edge case analysis
- Systematic implementation
- Extensive test planning

### Test-First Development
- Red-Green-Refactor cycles
- Incremental feature building
- Test-driven edge case discovery
- Emergent algorithm optimization

### Validated Test Development
- Wrong implementation validation
- Test adequacy verification
- Multiple algorithm attempts
- Systematic test strengthening

## Success Metrics

### Code Quality
- Correctness on all test cases
- Edge case handling
- Code clarity and readability
- Performance characteristics

### Development Process
- Time to first working solution
- Number of iterations/refinements
- Test coverage achieved
- Bug discovery patterns

### Methodology Expression
- How each approach naturally handles the constraint
- Problem decomposition strategies
- Testing strategies employed
- Optimization decisions made

## Validation Protocol

### Function Requirements
- Must pass all specified test cases
- Must handle edge cases appropriately
- Must use only standard library
- Must be importable and testable

### Comparison Fairness
- Identical problem specifications across approaches
- Same time constraints
- Same technology limitations
- Same success criteria

## Research Questions

1. **Speed vs Quality**: Which methodologies produce working solutions fastest vs highest quality?
2. **Edge Case Discovery**: Which approaches naturally find and handle edge cases better?
3. **Algorithm Choice**: Do methodologies influence algorithm selection patterns?
4. **Test Coverage**: Which approaches achieve better test coverage naturally?
5. **Refactoring Patterns**: How do methodologies differ in optimization approaches?

## Progression to Tier 2

These function-level implementations become **building blocks** for Tier 2 tool-level experiments:
- Functions can be imported and composed
- Proven algorithms can be reused
- Testing strategies can be elevated
- Architecture patterns can emerge

**Next Phase**: Tier 2 experiments use these functions as components in larger tools, enabling study of composition and integration methodologies.