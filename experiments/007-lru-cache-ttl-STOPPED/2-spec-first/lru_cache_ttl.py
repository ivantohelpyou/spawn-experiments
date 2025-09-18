"""
LRU Cache with TTL Implementation

This module implements an LRU (Least Recently Used) cache with TTL (Time-To-Live)
functionality as specified in SPECIFICATIONS.md.

Features:
- LRU eviction policy
- Time-based expiration (TTL)
- Thread-safe operations
- O(1) get/put operations
- Configurable capacity
- Performance statistics
"""

import threading
import time
from typing import Any, Dict, Optional, Union


class CacheStats:
    """Statistics tracking for cache performance."""

    def __init__(self) -> None:
        self.hits: int = 0
        self.misses: int = 0
        self.evictions: int = 0
        self.expirations: int = 0
        self.puts: int = 0
        self.deletes: int = 0

    def to_dict(self) -> Dict[str, int]:
        """Return statistics as dictionary."""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'expirations': self.expirations,
            'puts': self.puts,
            'deletes': self.deletes,
            'hit_ratio': self.hits / max(self.hits + self.misses, 1)
        }


class CacheNode:
    """
    Node in the doubly linked list representing a cache entry.

    Attributes:
        key: The cache key
        value: The cached value
        expiration_time: Unix timestamp when item expires (None for no expiration)
        prev: Previous node in linked list
        next: Next node in linked list
    """

    def __init__(self, key: Any = None, value: Any = None,
                 expiration_time: Optional[float] = None) -> None:
        self.key = key
        self.value = value
        self.expiration_time = expiration_time
        self.prev: Optional['CacheNode'] = None
        self.next: Optional['CacheNode'] = None

    def is_expired(self) -> bool:
        """Check if this cache entry has expired."""
        if self.expiration_time is None:
            return False
        return time.time() > self.expiration_time


class LRUCacheWithTTL:
    """
    LRU Cache with TTL (Time-To-Live) support.

    This cache automatically expires items after their TTL period and evicts
    least recently used items when capacity is reached. All operations are
    thread-safe and designed for O(1) performance.

    Example:
        >>> cache = LRUCacheWithTTL(capacity=100)
        >>> cache.put("key1", "value1", ttl_seconds=60)
        True
        >>> cache.get("key1")
        "value1"
        >>> # After 60 seconds...
        >>> cache.get("key1")
        None
    """

    def __init__(self, capacity: int) -> None:
        """
        Initialize LRU Cache with specified capacity.

        Args:
            capacity: Maximum number of items the cache can hold (must be >= 1)

        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")

        self._capacity = capacity
        self._cache: Dict[Any, CacheNode] = {}
        self._stats = CacheStats()

        # Create dummy head and tail nodes for the doubly linked list
        # head.next -> most recently used
        # tail.prev -> least recently used
        self._head = CacheNode()
        self._tail = CacheNode()
        self._head.next = self._tail
        self._tail.prev = self._head

        # Thread safety
        self._lock = threading.RLock()

    def get(self, key: Any) -> Any:
        """
        Retrieve value by key.

        Args:
            key: The cache key to look up

        Returns:
            The cached value, or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                self._stats.misses += 1
                return None

            node = self._cache[key]

            # Check if expired
            if node.is_expired():
                self._remove_node(node)
                del self._cache[key]
                self._stats.misses += 1
                self._stats.expirations += 1
                return None

            # Move to head (mark as most recently used)
            self._move_to_head(node)
            self._stats.hits += 1
            return node.value

    def put(self, key: Any, value: Any, ttl_seconds: Optional[float] = None) -> bool:
        """
        Store key-value pair with optional TTL.

        Args:
            key: The cache key (must be hashable)
            value: The value to store
            ttl_seconds: Time to live in seconds (None for no expiration)

        Returns:
            True if successful

        Raises:
            TypeError: If key is not hashable
            ValueError: If ttl_seconds is negative
        """
        with self._lock:
            # Validate inputs
            try:
                hash(key)
            except TypeError:
                raise TypeError("Cache keys must be hashable")

            if ttl_seconds is not None and ttl_seconds < 0:
                raise ValueError("TTL cannot be negative")

            # Calculate expiration time
            expiration_time = None
            if ttl_seconds is not None:
                expiration_time = time.time() + ttl_seconds

            if key in self._cache:
                # Update existing node
                node = self._cache[key]
                node.value = value
                node.expiration_time = expiration_time
                self._move_to_head(node)
            else:
                # Create new node
                node = CacheNode(key, value, expiration_time)

                # Check if at capacity
                if len(self._cache) >= self._capacity:
                    # Remove least recently used item
                    lru_node = self._tail.prev
                    self._remove_node(lru_node)
                    del self._cache[lru_node.key]
                    self._stats.evictions += 1

                # Add new node
                self._cache[key] = node
                self._add_to_head(node)

            self._stats.puts += 1
            return True

    def delete(self, key: Any) -> bool:
        """
        Remove key from cache.

        Args:
            key: The cache key to remove

        Returns:
            True if key existed and was removed, False otherwise
        """
        with self._lock:
            if key not in self._cache:
                return False

            node = self._cache[key]
            self._remove_node(node)
            del self._cache[key]
            self._stats.deletes += 1
            return True

    def clear(self) -> None:
        """Remove all items from cache."""
        with self._lock:
            self._cache.clear()
            self._head.next = self._tail
            self._tail.prev = self._head

    def size(self) -> int:
        """Return current number of items in cache."""
        with self._lock:
            return len(self._cache)

    def capacity(self) -> int:
        """Return maximum capacity of cache."""
        return self._capacity

    def stats(self) -> Dict[str, Union[int, float]]:
        """Return cache performance statistics."""
        with self._lock:
            return self._stats.to_dict()

    def cleanup_expired(self) -> int:
        """
        Manually clean up expired entries.

        Returns:
            Number of expired entries removed
        """
        with self._lock:
            expired_keys = []
            current_time = time.time()

            for key, node in self._cache.items():
                if node.expiration_time and current_time > node.expiration_time:
                    expired_keys.append(key)

            for key in expired_keys:
                node = self._cache[key]
                self._remove_node(node)
                del self._cache[key]
                self._stats.expirations += 1

            return len(expired_keys)

    def _add_to_head(self, node: CacheNode) -> None:
        """Add node right after head (most recently used position)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node: CacheNode) -> None:
        """Remove node from doubly linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: CacheNode) -> None:
        """Move node to head (mark as most recently used)."""
        self._remove_node(node)
        self._add_to_head(node)

    def __len__(self) -> int:
        """Return current number of items in cache."""
        return self.size()

    def __contains__(self, key: Any) -> bool:
        """Check if key is in cache (and not expired)."""
        return self.get(key) is not None

    def __repr__(self) -> str:
        """Return string representation of cache."""
        return f"LRUCacheWithTTL(capacity={self._capacity}, size={self.size()})"


# Convenience function for simple use cases
def create_cache(capacity: int = 128) -> LRUCacheWithTTL:
    """
    Create an LRU cache with TTL support.

    Args:
        capacity: Maximum number of items (default: 128)

    Returns:
        New LRUCacheWithTTL instance
    """
    return LRUCacheWithTTL(capacity)


if __name__ == "__main__":
    # Basic demonstration
    cache = LRUCacheWithTTL(3)

    # Test basic operations
    print("=== LRU Cache with TTL Demo ===")

    # Add some items
    cache.put("a", "value_a")
    cache.put("b", "value_b", ttl_seconds=2)
    cache.put("c", "value_c")

    print(f"Cache size: {cache.size()}")
    print(f"Get 'a': {cache.get('a')}")
    print(f"Get 'b': {cache.get('b')}")

    # Add one more item to trigger LRU eviction
    cache.put("d", "value_d")
    print(f"After adding 'd', cache size: {cache.size()}")
    print(f"Get 'c' (should be evicted): {cache.get('c')}")

    # Wait for TTL expiration
    print("Waiting for 'b' to expire...")
    time.sleep(2.1)
    print(f"Get 'b' (should be expired): {cache.get('b')}")

    # Show statistics
    print(f"Cache stats: {cache.stats()}")