# LRU Cache with TTL - Method 1: Direct Implementation

This directory contains a complete implementation of an LRU (Least Recently Used) Cache with TTL (Time-To-Live) functionality using Python.

## Features

- **O(1) Average Case Operations**: All cache operations (get, put) are O(1) average case
- **Capacity Management**: Automatically removes LRU items when capacity is exceeded
- **TTL Expiration**: Items automatically expire and are removed after their TTL
- **Automatic Cleanup**: Expired items are cleaned up during normal operations
- **Type Flexibility**: Supports any hashable keys and any values
- **Thread-Safe Design**: Single-threaded implementation focused on correctness

## Core Operations

- `put(key, value, ttl_seconds)`: Store item with expiration time
- `get(key)`: Return value if exists and not expired, None otherwise
- `size()`: Get current number of items in cache
- `clear()`: Remove all items from cache
- `keys()`: Get all non-expired keys
- `items()`: Get all non-expired key-value pairs

## Files

### Core Implementation
- **`lru_cache_ttl.py`**: Main LRU Cache with TTL implementation
  - `LRUCacheWithTTL` class with all core functionality
  - `Node` class for doubly linked list implementation
  - Comprehensive error handling and edge case management

### User Interface
- **`cache_ui.py`**: Interactive command-line interface
  - Interactive shell for testing cache functionality
  - Built-in demonstration mode
  - Help system with all available commands

### Demonstration
- **`demo.py`**: Comprehensive demonstration script
  - Shows all cache features in action
  - Performance characteristics demonstration
  - Edge cases and error handling examples

### Testing
- **`test_lru_cache_ttl.py`**: Complete unit test suite
  - Tests for all operations and edge cases
  - Performance verification tests
  - Integration tests with complex scenarios

### Utilities
- **`TIMING_LOG.txt`**: Implementation timing log
- **`README.md`**: This documentation file

## Usage Examples

### Basic Usage

```python
from lru_cache_ttl import LRUCacheWithTTL

# Create cache with capacity of 100
cache = LRUCacheWithTTL(100)

# Store items with different TTLs
cache.put("user:123", {"name": "Alice", "email": "alice@example.com"}, 3600)  # 1 hour
cache.put("session:abc", "active", 1800)  # 30 minutes
cache.put("temp:data", "temporary", 60)   # 1 minute

# Retrieve items
user_data = cache.get("user:123")  # Returns the user dict
session_status = cache.get("session:abc")  # Returns "active"
expired_data = cache.get("nonexistent")  # Returns None

# Check cache state
print(f"Cache size: {cache.size()}")
print(f"All keys: {cache.keys()}")
print(f"Cache full representation: {cache}")
```

### Interactive Testing

```bash
# Run the interactive interface
python cache_ui.py

# Example session:
cache> create 5
cache> put user1 Alice 10
cache> put user2 Bob 20
cache> get user1
cache> status
cache> demo
```

### Running Demonstrations

```bash
# Run comprehensive demonstration
python demo.py

# Run unit tests
python test_lru_cache_ttl.py
```

## Implementation Details

### Data Structure

The implementation uses:
- **Hash Map**: For O(1) key lookups (`self.cache`)
- **Doubly Linked List**: For O(1) insertion/deletion and LRU ordering
- **Dummy Head/Tail Nodes**: Simplify edge cases in linked list operations

### Algorithm Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| `put()` | O(1) average | O(1) |
| `get()` | O(1) average | O(1) |
| `size()` | O(k) where k = expired items | O(1) |
| `clear()` | O(1) | O(1) |
| `keys()` | O(k) where k = expired items | O(n) |
| `items()` | O(k) where k = expired items | O(n) |

### TTL Management

- Items are checked for expiration during `get()` operations
- Expired items are automatically removed during cache operations
- Cleanup happens lazily to maintain O(1) performance for main operations
- TTL is absolute time (based on `time.time()`)

### LRU Eviction

- Most recently accessed items move to the head of the list
- When capacity is exceeded, the tail item (LRU) is removed
- Updates to existing keys refresh their position in the LRU order

## Testing

The test suite includes:
- **Unit Tests**: Individual method testing
- **Integration Tests**: Complex multi-operation scenarios
- **Edge Cases**: Invalid inputs, boundary conditions
- **Performance Tests**: Verification of O(1) characteristics
- **TTL Tests**: Expiration behavior verification
- **LRU Tests**: Eviction order verification

Run tests with:
```bash
python test_lru_cache_ttl.py
```

## Performance Characteristics

- **Memory Usage**: O(n) where n is the number of items in cache
- **Operations**: O(1) average case for put/get operations
- **Cleanup**: Lazy cleanup maintains performance while handling expired items
- **Scalability**: Tested with 1000+ items showing consistent performance

## Error Handling

The implementation handles:
- Invalid capacity (non-positive values)
- Invalid TTL values (non-positive values)
- Non-existent key access (returns None)
- Automatic cleanup of corrupted state

## Thread Safety

This implementation is **not thread-safe**. For concurrent access, external synchronization would be required.

## Design Decisions

1. **Lazy Cleanup**: Expired items are cleaned up during normal operations rather than using background threads
2. **Absolute TTL**: TTL is based on absolute timestamps rather than relative timers
3. **O(1) Priority**: Optimized for O(1) operations over memory efficiency
4. **Comprehensive Error Handling**: Validates inputs and handles edge cases gracefully
5. **Rich Interface**: Provides both basic cache operations and utility methods