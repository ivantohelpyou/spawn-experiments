# LRU Cache with TTL - Detailed Specifications

## 1. Core Functional Requirements

### Primary Functions
- **Cache Storage**: Store key-value pairs with automatic eviction
- **LRU Eviction**: Remove least recently used items when cache reaches capacity
- **TTL Expiration**: Automatically expire items after specified time-to-live
- **Size Management**: Enforce maximum cache size limits
- **Access Tracking**: Track item usage for LRU ordering

### Key Operations
- `get(key)`: Retrieve value and mark as recently used
- `put(key, value, ttl=None)`: Store/update value with optional TTL
- `delete(key)`: Remove specific key
- `clear()`: Remove all cached items
- `size()`: Return current cache size
- `capacity()`: Return maximum cache capacity

## 2. User Stories with Acceptance Criteria

### Story 1: Basic Cache Operations
**As a** developer using the cache
**I want** to store and retrieve key-value pairs
**So that** I can cache frequently accessed data

**Acceptance Criteria:**
- Can store a key-value pair
- Can retrieve stored values by key
- Returns None for non-existent keys
- Can update existing keys

### Story 2: LRU Eviction
**As a** developer with limited memory
**I want** automatic eviction of least recently used items
**So that** the cache doesn't exceed memory limits

**Acceptance Criteria:**
- Evicts oldest item when capacity is reached
- Updates access order on get operations
- Updates access order on put operations for existing keys
- Maintains correct order for multiple operations

### Story 3: TTL Expiration
**As a** developer caching time-sensitive data
**I want** items to automatically expire after a specified time
**So that** stale data is not served

**Acceptance Criteria:**
- Items expire after specified TTL seconds
- Expired items return None on get
- Expired items are removed from cache
- TTL can be set per item
- Default TTL can be configured

### Story 4: Cache Management
**As a** developer managing cache state
**I want** to inspect and control cache contents
**So that** I can monitor and maintain the cache

**Acceptance Criteria:**
- Can check current cache size
- Can clear all cache contents
- Can remove specific keys
- Can set maximum capacity

## 3. Technical Architecture Overview

### Components
```
LRUCacheWithTTL
├── DoublyLinkedList (for LRU ordering)
├── HashMap (for O(1) key access)
├── TTLManager (for expiration tracking)
└── CacheNode (for storing data + metadata)
```

### Data Flow
1. **GET**: Check expiration → Update access order → Return value
2. **PUT**: Check capacity → Update/Insert → Set TTL → Update order
3. **Eviction**: Remove LRU node → Clean up references
4. **Expiration**: Background cleanup or lazy removal

## 4. Data Models and Relationships

### CacheNode
```python
class CacheNode:
    key: str
    value: Any
    timestamp: float
    ttl: Optional[float]
    prev: Optional[CacheNode]
    next: Optional[CacheNode]
```

### LRUCacheWithTTL
```python
class LRUCacheWithTTL:
    capacity: int
    default_ttl: Optional[float]
    nodes: Dict[str, CacheNode]
    head: CacheNode  # Most recently used
    tail: CacheNode  # Least recently used
```

## 5. API Design

### Constructor
```python
def __init__(self, capacity: int, default_ttl: Optional[float] = None)
```

### Core Methods
```python
def get(self, key: str) -> Optional[Any]
def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None
def delete(self, key: str) -> bool
def clear(self) -> None
def size(self) -> int
def capacity(self) -> int
```

### Utility Methods
```python
def keys(self) -> List[str]
def values(self) -> List[Any]
def items(self) -> List[Tuple[str, Any]]
def is_expired(self, key: str) -> bool
```

## 6. Business Rules and Validation Requirements

### Capacity Rules
- Capacity must be positive integer (>= 1)
- Cache size cannot exceed capacity
- LRU eviction triggers when at capacity

### TTL Rules
- TTL must be positive number or None
- Item-specific TTL overrides default TTL
- Expired items are treated as non-existent
- TTL is set from current time

### Key Rules
- Keys must be strings
- Keys cannot be empty strings
- Case-sensitive key matching

### Value Rules
- Values can be any Python object
- None is a valid value (distinct from missing key)

## 7. Error Handling and Edge Cases

### Input Validation Errors
- `ValueError`: Invalid capacity (< 1)
- `ValueError`: Invalid TTL (< 0)
- `TypeError`: Non-string keys
- `ValueError`: Empty string keys

### Edge Cases
- **Empty Cache**: get() returns None, size() returns 0
- **Single Item Cache**: Proper LRU behavior with capacity=1
- **Immediate Expiration**: TTL=0 items expire immediately
- **Very Large TTL**: Handle large timestamp values
- **Concurrent Access**: Thread-safety considerations
- **Memory Pressure**: Graceful handling of large objects

### Error Recovery
- Invalid operations don't corrupt cache state
- Partial failures don't leave cache inconsistent
- Clear error messages for debugging

### Performance Considerations
- O(1) get and put operations
- O(1) delete operations
- Lazy expiration cleanup
- Memory efficient node linking

## 8. Testing Strategy

### Unit Test Categories
- **Basic Operations**: get, put, delete, clear
- **LRU Behavior**: Eviction order correctness
- **TTL Functionality**: Expiration timing
- **Edge Cases**: Boundary conditions
- **Error Handling**: Invalid inputs
- **Performance**: Operation complexity

### Integration Test Scenarios
- **Mixed Operations**: Combined get/put/delete sequences
- **Capacity Stress**: Fill and overfill cache
- **TTL Stress**: Multiple items with different TTLs
- **Real-world Usage**: Realistic access patterns

### Test Data Strategies
- **Simple Types**: strings, integers, booleans
- **Complex Types**: lists, dictionaries, custom objects
- **Boundary Values**: capacity limits, TTL edge cases
- **Invalid Inputs**: wrong types, negative values