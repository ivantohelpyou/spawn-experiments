# LRU Cache with TTL - Specification-Driven Implementation

This is Method 2 of implementing an LRU Cache with TTL using a specification-driven approach.

## Approach

**Phase 1**: Write comprehensive specifications first
**Phase 2**: Build implementation according to specifications

## Files

- `SPECIFICATIONS.md` - Comprehensive specifications covering all requirements
- `lru_cache_ttl.py` - Complete implementation following specifications
- `test_lru_cache_ttl.py` - Comprehensive test suite (requires pytest)
- `simple_test.py` - Simple test runner without external dependencies
- `demo.py` - Comprehensive demonstration of all features
- `requirements.txt` - Python dependencies
- `TIMING_LOG.txt` - Execution timing log

## Features Implemented

✓ LRU eviction policy with O(1) operations
✓ TTL expiration with configurable timeouts
✓ Thread-safe concurrent access
✓ Performance statistics tracking
✓ Comprehensive error handling
✓ Advanced features (cleanup, TTL queries, etc.)

## Usage

```python
from lru_cache_ttl import LRUCacheWithTTL

# Create cache with capacity 100 and 5-minute default TTL
cache = LRUCacheWithTTL(capacity=100, default_ttl=300.0)

# Basic operations
cache.put("user:123", {"name": "John", "email": "john@example.com"})
user = cache.get("user:123")

# Custom TTL
cache.put("session:abc", "session_data", ttl=1800.0)  # 30 minutes

# Statistics
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate():.1f}%")
```

## Testing

Run the simple tests:
```bash
python simple_test.py
```

Run the comprehensive demo:
```bash
python demo.py
```

Run with pytest (if available):
```bash
pytest test_lru_cache_ttl.py -v
```

## Performance

Achieved performance characteristics:
- Get operations: ~565,000 ops/second
- Put operations: ~426,000 ops/second
- Mixed operations: ~645,000 ops/second
- Thread-safe with 100% success rate under concurrent load