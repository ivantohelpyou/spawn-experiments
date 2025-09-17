# Algorithmic TDD Experiments

## Design Principles

These experiments focus on **algorithmic challenges** with **unambiguous specifications** that are:
- Mathematically or logically precise (no semantic interpretation needed)
- Difficult to implement correctly without tests
- Rich in edge cases that naive approaches will miss
- Demonstrable with clear pass/fail criteria

## Tier 1: Prime Algorithmic Challenges

### 1. **LRU Cache with TTL (Time-To-Live)**

**Specification**: Implement a Least Recently Used cache that also expires items after a specified time.

**Requirements**:
- `put(key, value, ttl_seconds)` - Store item with expiration
- `get(key)` - Return value if exists and not expired, None otherwise
- `capacity` - Maximum number of items (constructor parameter)
- When capacity exceeded, remove LRU item
- When items expire, they are automatically removed on next access
- All operations must be O(1) average case

**Edge Cases**:
- Items expiring while being the most recently used
- Multiple items expiring simultaneously
- Clock rollover (if using timestamps)
- Zero TTL values
- Negative TTL values
- Accessing expired items
- Eviction during expiration cleanup

**Why Difficult**: Combines two complex algorithms (LRU + TTL), timing edge cases, O(1) constraint

---

### 2. **Interval Merging with Gaps**

**Specification**: Given intervals `[start, end]`, merge overlapping intervals and return both merged intervals and the gaps between them.

**Input**: `[(1,3), (6,9), (8,12), (15,18)]`
**Output**:
- Merged: `[(1,3), (6,12), (15,18)]`
- Gaps: `[(4,5), (13,14)]`

**Requirements**:
- Handle unsorted input
- Handle identical intervals
- Handle touching intervals (e.g., (1,3) and (4,6) don't merge, but (1,3) and (3,5) do)
- Handle single-point intervals
- Handle negative numbers
- Handle floating-point intervals
- Return gaps only within the range of input intervals

**Edge Cases**:
- Empty input
- Single interval
- All intervals overlap into one
- No gaps (consecutive intervals)
- Intervals with same start or end points
- Floating-point precision issues

**Why Difficult**: Multiple sorting and merging logic, boundary condition handling

---

### 3. **Sliding Window Rate Limiter**

**Specification**: Implement a rate limiter using sliding window algorithm.

**Requirements**:
- `allow_request(user_id, timestamp)` - Returns True if request allowed, False if rate limited
- `requests_per_window` - Maximum requests allowed (constructor parameter)
- `window_size_seconds` - Time window size (constructor parameter)
- Use sliding window (not fixed window)
- Clean up old requests automatically
- Support multiple users simultaneously

**Edge Cases**:
- Requests exactly at window boundaries
- Burst requests at start of window
- Clock skew (timestamps going backwards)
- Very large timestamps
- Concurrent requests for same user
- Memory cleanup for inactive users

**Why Difficult**: Time-based algorithms, sliding window logic, memory management

---

### 4. **Expression Evaluator with Precedence**

**Specification**: Evaluate mathematical expressions with proper operator precedence and parentheses.

**Requirements**:
- Support: `+`, `-`, `*`, `/`, `^` (exponentiation), `()` (parentheses)
- Proper precedence: `^` > `*`,`/` > `+`,`-`
- Left-to-right associativity except `^` (right-to-left)
- Handle negative numbers: `-5 + 3`
- Handle floating-point numbers
- Return precise decimal results

**Edge Cases**:
- Nested parentheses: `((2 + 3) * 4)`
- Negative numbers: `-5 * -3`
- Division by zero
- Invalid expressions: `2 + + 3`, `2 3`, `(2 + 3`
- Empty expressions
- Whitespace handling
- Very large numbers
- Floating-point precision

**Why Difficult**: Parsing, precedence rules, associativity, error handling

---

### 5. **Consistent Hashing Ring**

**Specification**: Implement consistent hashing for distributed systems.

**Requirements**:
- `add_node(node_id)` - Add server node to ring
- `remove_node(node_id)` - Remove server node from ring
- `get_node(key)` - Return node responsible for key
- `virtual_nodes` - Number of virtual nodes per physical node (constructor parameter)
- Minimize key redistribution when nodes are added/removed
- Uniform key distribution across nodes

**Edge Cases**:
- Single node in ring
- All nodes removed
- Adding duplicate nodes
- Removing non-existent nodes
- Hash collisions
- Empty keys
- Very large number of virtual nodes

**Why Difficult**: Hash ring algorithms, virtual node management, distribution uniformity

## Tier 2: Solid Algorithmic Challenges

### 6. **Trie with Prefix Counting**
- Auto-complete with frequency tracking
- Prefix search with wildcards
- Memory-efficient implementation

### 7. **Bloom Filter with False Positive Rate**
- Configurable false positive rate
- Multiple hash functions
- Optimal bit array sizing

### 8. **Skip List Implementation**
- Probabilistic data structure
- O(log n) search, insert, delete
- Level generation algorithms

### 9. **Circular Buffer with Overflow Strategies**
- Fixed-size buffer
- Multiple overflow strategies (overwrite, block, expand)
- Thread-safety considerations

### 10. **Merkle Tree Builder**
- Binary tree of hashes
- Efficient verification
- Handle odd number of leaves

## Evaluation Criteria

### Correctness Metrics
- **Functional Tests**: All specified requirements work
- **Edge Case Coverage**: Handles boundary conditions
- **Error Handling**: Graceful failure modes
- **Performance**: Meets algorithmic complexity requirements

### Code Quality Metrics
- **Readability**: Clear variable names, logical structure
- **Maintainability**: Modular design, separation of concerns
- **Documentation**: Clear comments and docstrings
- **Test Coverage**: Comprehensive test suite

### Methodology Effectiveness
- **Test-First Development**: Evidence of TDD red-green-refactor cycles
- **Incremental Development**: Building complexity gradually
- **Refactoring Quality**: Clean code after green phase
- **Validation Rigor**: Test quality and edge case discovery

## Implementation Strategy

### For Live Demos
1. **Start Simple**: Begin with core algorithm
2. **Add Complexity**: Introduce edge cases progressively
3. **Show Failures**: Demonstrate where naive approaches break
4. **Highlight Differences**: Clear methodology comparison points

### For Deep Analysis
1. **Full Implementation**: Complete all requirements
2. **Comprehensive Testing**: Cover all edge cases
3. **Performance Analysis**: Measure algorithmic complexity
4. **Maintenance Simulation**: Add new features to test extensibility

---

**Recommended Starting Point**: Expression Evaluator or Interval Merging - both have clear specifications and obvious failure modes for naive approaches.
