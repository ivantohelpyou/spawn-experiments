# LRU Cache with TTL - Comprehensive Specifications

## Project Overview
This document provides comprehensive specifications for a Least Recently Used (LRU) Cache with Time-To-Live (TTL) functionality implemented in Python.

## 1. Features and Requirements

### 1.1 Core Features
- **LRU Eviction Policy**: Automatically remove least recently used items when cache reaches capacity
- **TTL Support**: Items expire automatically after a specified time duration
- **Thread Safety**: Support concurrent access from multiple threads
- **Configurable Capacity**: Set maximum number of items the cache can hold
- **Real-time Cleanup**: Expired items are removed automatically on access
- **Statistics Tracking**: Monitor cache hits, misses, and evictions

### 1.2 Functional Requirements
- **FR-001**: Cache shall store key-value pairs with configurable TTL
- **FR-002**: Cache shall evict least recently used items when at capacity
- **FR-003**: Cache shall expire items automatically when TTL is reached
- **FR-004**: Cache shall provide O(1) average time complexity for get/put operations
- **FR-005**: Cache shall support customizable default TTL for all items
- **FR-006**: Cache shall allow per-item TTL override
- **FR-007**: Cache shall provide statistics on cache performance
- **FR-008**: Cache shall be thread-safe for concurrent operations

### 1.3 Non-Functional Requirements
- **NFR-001**: Performance - Get/Put operations must be O(1) average case
- **NFR-002**: Memory - Cache must not exceed configured memory limits
- **NFR-003**: Reliability - Cache must handle edge cases gracefully
- **NFR-004**: Usability - Simple and intuitive API design
- **NFR-005**: Maintainability - Clean, well-documented code structure

## 2. User Stories and Use Cases

### 2.1 User Stories

**US-001: Basic Cache Operations**
- As a developer, I want to store and retrieve data from the cache
- So that I can improve application performance by avoiding expensive computations

**US-002: Automatic Expiration**
- As a developer, I want cache items to expire automatically
- So that stale data doesn't persist in the cache indefinitely

**US-003: Capacity Management**
- As a developer, I want the cache to automatically remove old items when full
- So that memory usage stays within acceptable limits

**US-004: Performance Monitoring**
- As a developer, I want to monitor cache performance metrics
- So that I can optimize cache configuration and usage

**US-005: Thread Safety**
- As a developer, I want to use the cache safely in multi-threaded applications
- So that data integrity is maintained under concurrent access

### 2.2 Use Cases

**UC-001: Web Application Session Cache**
- Cache user session data with 30-minute TTL
- Automatic cleanup of expired sessions
- LRU eviction when memory limits reached

**UC-002: API Response Cache**
- Cache external API responses for 5 minutes
- Reduce API calls and improve response times
- Handle cache misses gracefully

**UC-003: Database Query Cache**
- Cache expensive database query results
- Set TTL based on data update frequency
- Evict old queries when cache is full

## 3. Technical Architecture

### 3.1 Architecture Overview
The LRU Cache with TTL will be implemented using a combination of:
- **HashMap (dict)**: For O(1) key-value storage and lookup
- **Doubly Linked List**: For O(1) LRU ordering maintenance
- **Priority Queue/Timer**: For efficient TTL expiration handling
- **Threading Locks**: For thread safety

### 3.2 Core Components

#### 3.2.1 CacheNode
```python
class CacheNode:
    - key: Any
    - value: Any
    - expiry_time: float
    - prev: CacheNode
    - next: CacheNode
```

#### 3.2.2 LRUCacheWithTTL
```python
class LRUCacheWithTTL:
    - capacity: int
    - default_ttl: float
    - cache: Dict[Any, CacheNode]
    - head: CacheNode (dummy)
    - tail: CacheNode (dummy)
    - lock: threading.RLock
    - stats: CacheStats
```

#### 3.2.3 CacheStats
```python
class CacheStats:
    - hits: int
    - misses: int
    - evictions: int
    - expirations: int
    - total_operations: int
```

### 3.3 Algorithm Design

#### 3.3.1 Get Operation
1. Acquire lock
2. Check if key exists in cache
3. If exists, check TTL expiration
4. If expired, remove and return None
5. If valid, move to head (mark as recently used)
6. Update statistics
7. Release lock and return value

#### 3.3.2 Put Operation
1. Acquire lock
2. Check if key already exists
3. If exists, update value and move to head
4. If new key and at capacity, evict LRU item
5. Create new node and add to head
6. Set expiry time
7. Update statistics
8. Release lock

#### 3.3.3 Expiration Cleanup
1. Periodically scan for expired items
2. Remove expired nodes from both cache dict and linked list
3. Update statistics
4. Background thread or lazy cleanup on access

## 4. Data Models and Relationships

### 4.1 Data Structures

#### 4.1.1 Primary Data Structure
- **Cache Dictionary**: `{key: CacheNode}` - O(1) lookup
- **Doubly Linked List**: Maintains LRU order
  - Head: Most recently used
  - Tail: Least recently used

#### 4.1.2 Node Relationships
```
[Head Dummy] <-> [Node1] <-> [Node2] <-> [Node3] <-> [Tail Dummy]
     ^                                                      ^
Most Recently Used                                Least Recently Used
```

#### 4.1.3 Time Management
- **Expiry Time**: Absolute timestamp when item expires
- **TTL**: Relative time duration from insertion/update
- **Current Time**: System time for expiration checks

### 4.2 Memory Model
- Cache nodes contain references, not copies
- Doubly linked list for efficient insertion/deletion
- Minimal memory overhead per cache entry
- Configurable maximum memory usage

## 5. Business Rules and Constraints

### 5.1 Business Rules

**BR-001: Capacity Enforcement**
- Cache must never exceed specified capacity
- When at capacity, LRU item must be evicted before adding new item
- Capacity must be positive integer

**BR-002: TTL Behavior**
- Items with expired TTL are considered non-existent
- Accessing expired item triggers automatic removal
- TTL of 0 or negative means no expiration
- Default TTL applies to items without specific TTL

**BR-003: LRU Ordering**
- Recently accessed items move to head of queue
- Both get and put operations update recency
- Eviction always removes least recently used item

**BR-004: Thread Safety**
- All operations must be atomic
- No race conditions in multi-threaded environment
- Consistent state during concurrent access

### 5.2 Constraints

**C-001: Performance Constraints**
- Get operation: O(1) average time complexity
- Put operation: O(1) average time complexity
- Memory usage: O(n) where n is capacity

**C-002: Input Constraints**
- Keys must be hashable types
- Values can be any Python object
- TTL must be non-negative number (seconds)
- Capacity must be positive integer

**C-003: System Constraints**
- Python 3.6+ required for ordered dictionaries
- Threading support required for concurrent access
- System time must be monotonic for TTL accuracy

**C-004: Error Handling Constraints**
- Invalid inputs must raise appropriate exceptions
- Cache must remain in consistent state after errors
- No silent failures or data corruption

### 5.3 Edge Cases

**EC-001: Empty Cache**
- Get from empty cache returns None
- Statistics reflect no hits/misses appropriately

**EC-002: Single Item Cache**
- Capacity of 1 works correctly
- LRU behavior still applies

**EC-003: Zero TTL**
- Items with TTL=0 never expire
- Useful for permanent cache entries

**EC-004: System Clock Changes**
- Handle daylight saving time transitions
- Robust against system clock adjustments

**EC-005: Memory Pressure**
- Graceful handling when system memory is low
- Configurable memory limits respected

## 6. API Specification

### 6.1 Constructor
```python
def __init__(self, capacity: int, default_ttl: float = 0)
```

### 6.2 Core Methods
```python
def get(self, key: Any) -> Any
def put(self, key: Any, value: Any, ttl: float = None) -> None
def delete(self, key: Any) -> bool
def clear(self) -> None
def size(self) -> int
def is_empty(self) -> bool
```

### 6.3 Statistics Methods
```python
def get_stats(self) -> CacheStats
def reset_stats(self) -> None
def hit_rate(self) -> float
```

### 6.4 Maintenance Methods
```python
def cleanup_expired(self) -> int
def set_default_ttl(self, ttl: float) -> None
def get_remaining_ttl(self, key: Any) -> float
```

This specification provides the foundation for implementing a robust, efficient, and well-tested LRU Cache with TTL functionality.