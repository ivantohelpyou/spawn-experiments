# LRU Cache with TTL - Specification-First Implementation

This directory contains a complete implementation of an LRU Cache with TTL (Time-To-Live) functionality, developed using a specification-first approach.

## Project Structure

- `SPECIFICATIONS.md` - Comprehensive specifications document defining all requirements
- `lru_cache_ttl.py` - Complete implementation of the LRU Cache with TTL
- `test_lru_cache_ttl.py` - Comprehensive test suite covering all specifications
- `requirements.txt` - Python dependencies
- `TIMING_LOG.txt` - Development timeline tracking
- `README.md` - This documentation file

## Features

- **LRU Eviction Policy**: Automatically evicts least recently used items when capacity is reached
- **TTL Support**: Items expire automatically after specified time periods
- **Thread Safety**: All operations are thread-safe for concurrent access
- **High Performance**: O(1) get/put operations using hash map + doubly linked list
- **Configurable Capacity**: Set maximum cache size at initialization
- **Statistics Tracking**: Monitor cache performance with detailed metrics
- **Comprehensive Error Handling**: Proper validation and error reporting

## Usage

### Basic Usage

```python
from lru_cache_ttl import LRUCacheWithTTL

# Create cache with capacity of 100 items
cache = LRUCacheWithTTL(100)

# Store items (with optional TTL)
cache.put("key1", "value1")                    # No expiration
cache.put("key2", "value2", ttl_seconds=60)    # Expires in 60 seconds

# Retrieve items
value1 = cache.get("key1")  # Returns "value1"
value2 = cache.get("key2")  # Returns "value2" or None if expired

# Delete items
cache.delete("key1")

# Get cache information
print(f"Cache size: {cache.size()}")
print(f"Cache capacity: {cache.capacity()}")
print(f"Cache stats: {cache.stats()}")
```

### Convenience Function

```python
from lru_cache_ttl import create_cache

# Create cache with default capacity (128)
cache = create_cache()

# Or with custom capacity
cache = create_cache(capacity=500)
```

## Installation and Testing

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests
python -m pytest test_lru_cache_ttl.py -v

# Run with coverage
python -m pytest test_lru_cache_ttl.py --cov=lru_cache_ttl -v

# Run specific test class
python -m pytest test_lru_cache_ttl.py::TestBasicOperations -v
```

### Run Demo

```bash
python lru_cache_ttl.py
```

## Implementation Approach

This implementation was developed using a specification-first methodology:

1. **Phase 1 - Specifications**: Created comprehensive specifications document covering:
   - Features and requirements
   - User stories and use cases
   - Technical architecture
   - Data models and relationships
   - Business rules and constraints

2. **Phase 2 - Implementation**: Built the complete application according to specifications:
   - Implemented all specified features
   - Created comprehensive test suite
   - Verified implementation matches specifications
   - Ensured high performance and thread safety

## Architecture

The cache uses a hybrid data structure combining:

- **Hash Map**: Provides O(1) key lookup
- **Doubly Linked List**: Maintains LRU order with O(1) insertion/removal
- **TTL Management**: Tracks expiration times for automatic cleanup
- **Thread Safety**: Uses RLock for concurrent access protection

## Performance Characteristics

- **Get Operation**: O(1) average time complexity
- **Put Operation**: O(1) average time complexity
- **Delete Operation**: O(1) average time complexity
- **Space Complexity**: O(n) where n = number of cached items
- **Thread Safety**: Supports concurrent access with minimal contention

## Design Decisions

- **Lazy Expiration**: Items are checked for expiration on access (not background cleanup)
- **LRU + TTL Priority**: TTL expiration takes precedence over LRU eviction
- **Thread Safety**: All operations are thread-safe by default
- **Standard Library Only**: No external dependencies (except pytest for testing)

## Development Timeline

See `TIMING_LOG.txt` for development timing information.

## Testing Coverage

The test suite covers:

- ✅ All core functionality (LRU eviction, TTL expiration)
- ✅ Edge cases and error conditions
- ✅ Thread safety under concurrent access
- ✅ Performance characteristics
- ✅ All user stories and use cases from specifications
- ✅ Integration scenarios combining LRU + TTL
- ✅ Stress testing with high load

## License

This implementation is provided for educational and demonstration purposes.