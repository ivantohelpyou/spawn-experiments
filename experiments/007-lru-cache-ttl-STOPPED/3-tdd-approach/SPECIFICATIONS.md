# LRU Cache with TTL - Detailed Specifications

## 1. Core Functional Requirements

### Primary Features
- **LRU (Least Recently Used) Cache**: Implement a cache that evicts the least recently used items when capacity is exceeded
- **TTL (Time-To-Live) Support**: Each cached item should have a configurable expiration time
- **Thread-Safe Operations**: All cache operations must be thread-safe for concurrent access
- **Configurable Capacity**: Maximum number of items the cache can hold

### Core Operations
- `put(key, value, ttl=None)`: Store a key-value pair with optional TTL
- `get(key)`: Retrieve a value by key, updating its position in LRU order
- `delete(key)`: Remove a specific key-value pair
- `clear()`: Remove all cached items
- `size()`: Return current number of items in cache
- `capacity()`: Return maximum capacity of cache

## 2. User Stories with Acceptance Criteria

### Story 1: Basic Cache Operations
**As a developer, I want to store and retrieve values from the cache so that I can improve application performance.**

**Acceptance Criteria:**
- When I put a key-value pair, it should be stored in the cache
- When I get a key that exists, it should return the value
- When I get a key that doesn't exist, it should return None
- When I delete a key, it should be removed from the cache
- When I clear the cache, all items should be removed

### Story 2: LRU Eviction
**As a developer, I want the cache to automatically remove least recently used items when full so that memory usage is controlled.**

**Acceptance Criteria:**
- When cache is at capacity and I add a new item, the least recently used item should be evicted
- When I access an existing item, it should become the most recently used
- When I update an existing item, it should become the most recently used

### Story 3: TTL Expiration
**As a developer, I want cached items to automatically expire after a specified time so that stale data is not returned.**

**Acceptance Criteria:**
- When I put an item with TTL, it should expire after the specified time
- When I get an expired item, it should return None and remove the item
- When I put an item without TTL, it should not expire automatically
- Expired items should not count towards cache size

### Story 4: Cache Information
**As a developer, I want to know the current state of the cache so that I can monitor and debug my application.**

**Acceptance Criteria:**
- I should be able to get the current number of items in the cache
- I should be able to get the maximum capacity of the cache
- Cache operations should be efficient and performant

## 3. Technical Architecture Overview

### Components
1. **LRUCacheWithTTL**: Main cache class
2. **CacheNode**: Internal node structure for doubly-linked list
3. **TTLManager**: Handles expiration logic
4. **LRUManager**: Handles least-recently-used ordering

### Design Patterns
- **Strategy Pattern**: For different eviction strategies
- **Observer Pattern**: For TTL expiration notifications
- **Decorator Pattern**: For thread-safety

### Data Structures
- **Hash Table**: For O(1) key lookup
- **Doubly Linked List**: For O(1) LRU operations
- **Priority Queue**: For TTL expiration management

## 4. Data Models and Relationships

### CacheNode
```python
class CacheNode:
    key: Any
    value: Any
    expires_at: Optional[float]
    prev: Optional[CacheNode]
    next: Optional[CacheNode]
    access_time: float
```

### LRUCacheWithTTL
```python
class LRUCacheWithTTL:
    capacity: int
    cache: Dict[Any, CacheNode]
    head: CacheNode  # Most recently used
    tail: CacheNode  # Least recently used
    lock: threading.RLock
```

### Relationships
- Cache maintains hash table pointing to nodes
- Nodes form doubly-linked list for LRU ordering
- Each node contains expiration timestamp
- Thread lock ensures atomic operations

## 5. API Design

### Class Constructor
```python
def __init__(self, capacity: int = 100):
    """
    Initialize LRU cache with TTL support

    Args:
        capacity: Maximum number of items to store

    Raises:
        ValueError: If capacity <= 0
    """
```

### Core Methods
```python
def put(self, key: Any, value: Any, ttl: Optional[int] = None) -> None:
    """
    Store a key-value pair with optional TTL

    Args:
        key: Cache key
        value: Value to store
        ttl: Time-to-live in seconds (None for no expiration)
    """

def get(self, key: Any) -> Any:
    """
    Retrieve value by key, updating LRU position

    Args:
        key: Cache key

    Returns:
        Value if found and not expired, None otherwise
    """

def delete(self, key: Any) -> bool:
    """
    Remove a key-value pair

    Args:
        key: Cache key

    Returns:
        True if key existed, False otherwise
    """

def clear(self) -> None:
    """Remove all cached items"""

def size(self) -> int:
    """Get current number of items"""

def capacity(self) -> int:
    """Get maximum capacity"""
```

## 6. Business Rules and Validation Requirements

### Capacity Rules
- Cache capacity must be greater than 0
- Cannot store more items than capacity
- When full, least recently used item is evicted

### TTL Rules
- TTL must be non-negative if specified
- TTL of 0 means immediate expiration
- Items without TTL never expire automatically
- Expired items are treated as non-existent

### Key Rules
- Keys can be any hashable type
- None keys are allowed
- Empty string keys are allowed

### Value Rules
- Values can be any type including None
- Storing None as a value is different from key not existing

### Access Rules
- Getting a key updates its LRU position
- Putting an existing key updates both value and LRU position
- Deleting a non-existent key is safe (no error)

## 7. Error Handling and Edge Cases

### Error Conditions
- **Invalid Capacity**: Raise ValueError for capacity <= 0
- **Invalid TTL**: Raise ValueError for negative TTL values
- **Thread Safety**: Handle concurrent access without data corruption

### Edge Cases

#### Cache Full Scenarios
- Adding to full cache evicts LRU item
- Accessing item in full cache updates LRU without eviction
- Multiple rapid additions handle evictions correctly

#### TTL Edge Cases
- Item expires between put and get operations
- Item expires during get operation
- Multiple items expire simultaneously
- Clock adjustments don't break TTL logic

#### Concurrent Access Edge Cases
- Multiple threads accessing same key
- One thread adding while another evicts
- Multiple threads clearing cache simultaneously
- Rapid get/put operations on same keys

#### Boundary Conditions
- Cache with capacity 1
- Cache operations on empty cache
- Operations after clear()
- Very large TTL values
- TTL precision at millisecond level

### Performance Requirements
- Get operations: O(1) average time complexity
- Put operations: O(1) average time complexity
- Delete operations: O(1) average time complexity
- Memory usage: O(capacity) space complexity
- Thread contention: Minimal locking overhead

### Cleanup and Maintenance
- Expired items cleaned up lazily on access
- Optional background cleanup thread
- Memory deallocation handled properly
- No memory leaks from circular references