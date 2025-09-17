"""
LRU Cache with TTL Implementation

A thread-safe Least Recently Used (LRU) cache with Time-To-Live (TTL) functionality.
Implements O(1) average case performance for get/put operations using a combination
of hash table and doubly linked list.
"""

import threading
import time
from typing import Any, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class CacheStats:
    """Statistics tracking for cache performance monitoring."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    total_operations: int = 0

    def hit_rate(self) -> float:
        """Calculate cache hit rate as percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.hits / self.total_operations) * 100.0

    def reset(self) -> None:
        """Reset all statistics to zero."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0
        self.total_operations = 0


class CacheNode:
    """
    Node in the doubly linked list for maintaining LRU order.

    Attributes:
        key: The cache key
        value: The cached value
        expiry_time: Absolute timestamp when item expires (0 = never expires)
        prev: Previous node in the linked list
        next: Next node in the linked list
    """

    def __init__(self, key: Any = None, value: Any = None, expiry_time: float = 0):
        self.key = key
        self.value = value
        self.expiry_time = expiry_time
        self.prev: Optional[CacheNode] = None
        self.next: Optional[CacheNode] = None

    def is_expired(self) -> bool:
        """Check if this node has expired based on current time."""
        if self.expiry_time == 0:
            return False
        return time.time() > self.expiry_time


class LRUCacheWithTTL:
    """
    A thread-safe LRU cache with TTL support.

    Features:
    - O(1) average case get/put operations
    - Automatic expiration of items based on TTL
    - LRU eviction when capacity is reached
    - Thread-safe concurrent access
    - Performance statistics tracking
    """

    def __init__(self, capacity: int, default_ttl: float = 0):
        """
        Initialize the LRU cache with TTL.

        Args:
            capacity: Maximum number of items the cache can hold (must be > 0)
            default_ttl: Default TTL in seconds for all items (0 = no expiration)

        Raises:
            ValueError: If capacity is not positive
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache: Dict[Any, CacheNode] = {}

        # Create dummy head and tail nodes for easier list manipulation
        self.head = CacheNode()
        self.tail = CacheNode()
        self.head.next = self.tail
        self.tail.prev = self.head

        # Thread safety
        self.lock = threading.RLock()

        # Statistics
        self.stats = CacheStats()

    def get(self, key: Any) -> Any:
        """
        Retrieve a value from the cache.

        Args:
            key: The key to look up

        Returns:
            The cached value, or None if key not found or expired
        """
        with self.lock:
            self.stats.total_operations += 1

            if key not in self.cache:
                self.stats.misses += 1
                return None

            node = self.cache[key]

            # Check if expired
            if node.is_expired():
                self._remove_node(node)
                del self.cache[key]
                self.stats.expirations += 1
                self.stats.misses += 1
                return None

            # Move to head (mark as recently used)
            self._move_to_head(node)
            self.stats.hits += 1
            return node.value

    def put(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        """
        Store a key-value pair in the cache.

        Args:
            key: The key to store
            value: The value to store
            ttl: Time-to-live in seconds (None uses default_ttl)
        """
        with self.lock:

            # Determine expiry time
            effective_ttl = self.default_ttl if ttl is None else ttl
            expiry_time = 0 if effective_ttl <= 0 else time.time() + effective_ttl

            if key in self.cache:
                # Update existing key
                node = self.cache[key]
                node.value = value
                node.expiry_time = expiry_time
                self._move_to_head(node)
            else:
                # Add new key
                new_node = CacheNode(key, value, expiry_time)

                # Check capacity
                if len(self.cache) >= self.capacity:
                    # Evict LRU item
                    lru_node = self.tail.prev
                    if lru_node != self.head:  # Make sure it's not the dummy head
                        self._remove_node(lru_node)
                        del self.cache[lru_node.key]
                        self.stats.evictions += 1

                # Add new node
                self.cache[key] = new_node
                self._add_to_head(new_node)

    def delete(self, key: Any) -> bool:
        """
        Remove a key from the cache.

        Args:
            key: The key to remove

        Returns:
            True if key was found and removed, False otherwise
        """
        with self.lock:
            if key not in self.cache:
                return False

            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
            return True

    def clear(self) -> None:
        """Remove all items from the cache."""
        with self.lock:
            self.cache.clear()
            self.head.next = self.tail
            self.tail.prev = self.head

    def size(self) -> int:
        """Get the current number of items in the cache."""
        with self.lock:
            return len(self.cache)

    def is_empty(self) -> bool:
        """Check if the cache is empty."""
        with self.lock:
            return len(self.cache) == 0

    def get_stats(self) -> CacheStats:
        """Get a copy of current cache statistics."""
        with self.lock:
            return CacheStats(
                hits=self.stats.hits,
                misses=self.stats.misses,
                evictions=self.stats.evictions,
                expirations=self.stats.expirations,
                total_operations=self.stats.total_operations
            )

    def reset_stats(self) -> None:
        """Reset all cache statistics."""
        with self.lock:
            self.stats.reset()

    def hit_rate(self) -> float:
        """Get the current cache hit rate as a percentage."""
        with self.lock:
            return self.stats.hit_rate()

    def cleanup_expired(self) -> int:
        """
        Remove all expired items from the cache.

        Returns:
            Number of expired items removed
        """
        with self.lock:
            expired_keys = []
            current_time = time.time()

            for key, node in self.cache.items():
                if node.expiry_time > 0 and current_time > node.expiry_time:
                    expired_keys.append(key)

            for key in expired_keys:
                node = self.cache[key]
                self._remove_node(node)
                del self.cache[key]
                self.stats.expirations += 1

            return len(expired_keys)

    def set_default_ttl(self, ttl: float) -> None:
        """
        Set the default TTL for new cache entries.

        Args:
            ttl: Default TTL in seconds (0 = no expiration)
        """
        with self.lock:
            self.default_ttl = ttl

    def get_remaining_ttl(self, key: Any) -> Optional[float]:
        """
        Get the remaining TTL for a key.

        Args:
            key: The key to check

        Returns:
            Remaining TTL in seconds, 0 if no expiration, None if key not found
        """
        with self.lock:
            if key not in self.cache:
                return None

            node = self.cache[key]
            if node.expiry_time == 0:
                return 0  # No expiration

            remaining = node.expiry_time - time.time()
            return max(0, remaining)

    def _add_to_head(self, node: CacheNode) -> None:
        """Add node right after the dummy head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: CacheNode) -> None:
        """Remove node from the linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: CacheNode) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_to_head(node)

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return self.size()

    def __contains__(self, key: Any) -> bool:
        """Check if key exists and is not expired."""
        return self.get(key) is not None

    def __repr__(self) -> str:
        """String representation of the cache."""
        with self.lock:
            return f"LRUCacheWithTTL(capacity={self.capacity}, size={len(self.cache)}, hit_rate={self.hit_rate():.1f}%)"


# Example usage and demonstration
if __name__ == "__main__":
    # Create a cache with capacity 3 and default TTL of 2 seconds
    cache = LRUCacheWithTTL(capacity=3, default_ttl=2.0)

    print("=== LRU Cache with TTL Demo ===")
    print(f"Initial cache: {cache}")

    # Add some items
    print("\n1. Adding items to cache...")
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    print(f"Cache after adding 3 items: {cache}")

    # Test LRU eviction
    print("\n2. Testing LRU eviction...")
    cache.put("key4", "value4")  # Should evict key1 (least recently used)
    print(f"After adding key4: {cache}")
    print(f"key1 exists: {'key1' in cache}")  # Should be False
    print(f"key4 exists: {'key4' in cache}")  # Should be True

    # Test TTL expiration
    print("\n3. Testing TTL expiration...")
    print("Waiting 3 seconds for items to expire...")
    time.sleep(3)
    print(f"key2 after TTL: {cache.get('key2')}")  # Should be None (expired)

    # Add item with custom TTL
    print("\n4. Testing custom TTL...")
    cache.put("temp", "temporary", ttl=1.0)  # 1 second TTL
    print(f"temp value: {cache.get('temp')}")
    time.sleep(1.5)
    print(f"temp after 1.5s: {cache.get('temp')}")  # Should be None

    # Show statistics
    print("\n5. Cache statistics:")
    stats = cache.get_stats()
    print(f"Hits: {stats.hits}")
    print(f"Misses: {stats.misses}")
    print(f"Evictions: {stats.evictions}")
    print(f"Expirations: {stats.expirations}")
    print(f"Hit Rate: {stats.hit_rate():.1f}%")

    print(f"\nFinal cache state: {cache}")