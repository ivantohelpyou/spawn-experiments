# LRU Cache with TTL - Comprehensive Specifications

## 1. Core Functional Requirements

### Primary Requirements
- **LRU (Least Recently Used) Eviction**: Remove the least recently accessed item when cache reaches capacity
- **TTL (Time-To-Live) Expiration**: Automatically expire items after a specified time duration
- **Thread-Safe Operations**: Ensure safe concurrent access (for future extensibility)
- **Configurable Capacity**: Set maximum number of items the cache can hold
- **Configurable Default TTL**: Set default expiration time for items

### Secondary Requirements
- **Memory Efficient**: Minimize memory overhead per cached item
- **Fast Operations**: O(1) get, put, and delete operations
- **Automatic Cleanup**: Remove expired items during operations
- **Statistics**: Track cache hits, misses, and evictions

## 2. User Stories with Acceptance Criteria

### Story 1: Cache Initialization
**As a** developer
**I want** to create a cache with specified capacity and default TTL
**So that** I can store and retrieve data with automatic expiration and eviction

**Acceptance Criteria:**
- Given capacity = 3 and default_ttl = 60 seconds
- When I create a cache
- Then the cache should be empty with capacity 3 and default TTL 60s
- And the cache should accept valid capacity (positive integer)
- And the cache should accept valid TTL (positive number or None)

### Story 2: Basic Put/Get Operations
**As a** developer
**I want** to store and retrieve values by key
**So that** I can cache frequently accessed data

**Acceptance Criteria:**
- Given an empty cache
- When I put("key1", "value1")
- Then get("key1") should return "value1"
- And the item should be marked as most recently used
- When I get a non-existent key
- Then it should return None or raise KeyError

### Story 3: LRU Eviction
**As a** developer
**I want** old items to be automatically removed when cache is full
**So that** memory usage stays within limits

**Acceptance Criteria:**
- Given a cache with capacity 2 containing ["a", "b"]
- When I put("c", "value_c")
- Then "a" should be evicted (least recently used)
- And cache should contain ["b", "c"]
- And get("a") should return None

### Story 4: TTL Expiration
**As a** developer
**I want** items to automatically expire after their TTL
**So that** stale data is not served

**Acceptance Criteria:**
- Given an item with TTL of 1 second
- When I wait for 1.1 seconds
- Then get() should return None (item expired)
- And the item should be removed from cache
- When I access an item before expiration
- Then it should return the value and update "recently used" status

### Story 5: Custom TTL per Item
**As a** developer
**I want** to set different TTL values for different items
**So that** I can have fine-grained control over expiration

**Acceptance Criteria:**
- Given a cache with default TTL of 60 seconds
- When I put("key1", "value1", ttl=30)
- Then "key1" should expire after 30 seconds, not 60
- When I put("key2", "value2") without TTL
- Then "key2" should use default TTL of 60 seconds

## 3. Technical Architecture Overview

### Core Components
1. **LRUCacheWithTTL**: Main cache class
2. **CacheNode**: Internal node structure for doubly-linked list
3. **TTLManager**: Handles expiration tracking and cleanup
4. **CacheStats**: Statistics tracking (optional)

### Data Structures
- **HashMap**: O(1) key-to-node mapping
- **Doubly Linked List**: O(1) LRU ordering maintenance
- **Heap/Timeline**: Efficient TTL expiration tracking

### Algorithm Complexity
- **Get Operation**: O(1) average case
- **Put Operation**: O(1) average case
- **Delete Operation**: O(1) average case
- **Cleanup Operation**: O(k) where k = expired items

## 4. Data Models and Relationships

### CacheNode Model
```python
class CacheNode:
    key: str
    value: Any
    expiry_time: float  # Unix timestamp
    prev: CacheNode
    next: CacheNode
```

### Cache Internal State
```python
class LRUCacheWithTTL:
    capacity: int
    default_ttl: Optional[float]
    cache_map: Dict[str, CacheNode]  # Key -> Node mapping
    head: CacheNode  # Dummy head (most recent)
    tail: CacheNode  # Dummy tail (least recent)
    current_size: int
```

### Relationships
- **1:1** - Each key maps to exactly one cache node
- **Doubly Linked** - Each node points to prev/next for LRU ordering
- **Time-based** - Each node has expiry_time for TTL management

## 5. API Design

### Primary Interface
```python
class LRUCacheWithTTL:
    def __init__(self, capacity: int, default_ttl: Optional[float] = None)
    def get(self, key: str) -> Optional[Any]
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None
    def delete(self, key: str) -> bool
    def clear(self) -> None
    def size(self) -> int
    def keys(self) -> List[str]
    def is_expired(self, key: str) -> bool
```

### Extended Interface (Statistics)
```python
def get_stats(self) -> Dict[str, int]
def reset_stats(self) -> None
```

### Method Behaviors
- **get()**: Returns value if exists and not expired, None otherwise
- **put()**: Adds/updates item, evicts LRU if needed, applies TTL
- **delete()**: Removes item immediately, returns success status
- **clear()**: Removes all items
- **size()**: Returns current number of non-expired items

## 6. Business Rules and Validation Requirements

### Input Validation
1. **Capacity**: Must be positive integer (>= 1)
2. **TTL**: Must be positive number or None
3. **Keys**: Must be non-empty strings
4. **Values**: Can be any Python object

### Cache Behavior Rules
1. **Expiration Check**: Performed on every get() operation
2. **LRU Update**: Triggered on both get() and put() operations
3. **Eviction Order**: Expired items evicted before LRU eviction
4. **Capacity Enforcement**: Strict - never exceed specified capacity
5. **Time Precision**: Use time.time() with floating-point precision

### Edge Case Rules
1. **Capacity 1**: Should work correctly (single-item cache)
2. **TTL 0**: Items expire immediately (cache disabled)
3. **TTL None**: Items never expire (LRU-only cache)
4. **Duplicate Keys**: Updates existing item, refreshes LRU position
5. **Concurrent Access**: Must be thread-safe for future extensions

## 7. Error Handling and Edge Cases

### Expected Exceptions
```python
class CacheError(Exception): pass
class CacheCapacityError(CacheError): pass
class CacheTTLError(CacheError): pass
class CacheKeyError(CacheError): pass
```

### Error Scenarios
1. **Invalid Capacity**: Raise CacheCapacityError for capacity <= 0
2. **Invalid TTL**: Raise CacheTTLError for negative TTL
3. **Invalid Key**: Raise CacheKeyError for None or empty string keys
4. **Memory Pressure**: Graceful degradation, not exceptions

### Edge Cases to Test
1. **Empty Cache**: All operations on empty cache
2. **Single Item Cache**: Capacity = 1 scenarios
3. **Immediate Expiration**: TTL = 0 or very small values
4. **Large TTL**: TTL > reasonable values (years)
5. **Clock Changes**: System time adjustments
6. **Rapid Access**: High-frequency get/put operations
7. **Mixed TTL**: Items with different expiration times
8. **Boundary Conditions**: Exactly at capacity, exactly at TTL

### Performance Edge Cases
1. **Large Capacity**: Cache with 10,000+ items
2. **Many Expired Items**: Cleanup efficiency
3. **Frequent Evictions**: LRU performance under pressure
4. **Long-running Cache**: Memory leak prevention

## 8. Quality Assurance Requirements

### Test Coverage Requirements
- **Unit Tests**: 100% line coverage for core logic
- **Integration Tests**: End-to-end scenarios
- **Performance Tests**: O(1) operation verification
- **Stress Tests**: High load and edge case testing

### Quality Gates
1. All tests must pass
2. No memory leaks in long-running tests
3. Performance benchmarks must meet O(1) complexity
4. Error handling must be comprehensive
5. Documentation must be complete and accurate

This specification serves as the foundation for our rigorous Test-Driven Development process with comprehensive test validation.