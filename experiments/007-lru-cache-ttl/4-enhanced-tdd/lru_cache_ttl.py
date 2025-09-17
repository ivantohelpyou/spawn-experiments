"""
LRU Cache with TTL Implementation
Correct implementation following Enhanced Test-Driven Development
"""

import time
import threading
from typing import Any, Optional, Hashable, Dict, List, Tuple, Iterator
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """Represents a single cache entry with metadata"""
    key: Hashable
    value: Any
    timestamp: float
    ttl: Optional[float]
    access_time: float
    prev: Optional['CacheEntry'] = None
    next: Optional['CacheEntry'] = None

    def is_expired(self) -> bool:
        """Check if this entry has expired based on TTL"""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl


@dataclass
class CacheStats:
    """Statistics for cache performance monitoring"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    current_size: int = 0
    capacity: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate hit rate as percentage"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0

    @property
    def miss_rate(self) -> float:
        """Calculate miss rate as percentage"""
        return 100.0 - self.hit_rate


class LRUCacheWithTTL:
    """
    LRU Cache with Time-To-Live support

    Features:
    - O(1) get/set operations
    - Automatic LRU eviction when capacity exceeded
    - TTL-based expiration
    - Thread-safe operations
    - Performance statistics
    """

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        """
        Initialize the cache with given capacity and default TTL

        Args:
            capacity: Maximum number of items (must be positive)
            default_ttl: Default TTL in seconds (None for no expiration)

        Raises:
            ValueError: If capacity <= 0 or default_ttl < 0
        """
        # Validate capacity
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        # Validate TTL
        if default_ttl is not None and default_ttl < 0:
            raise ValueError("TTL must be None or a positive number")

        self._capacity = capacity
        self.default_ttl = default_ttl

        # Storage: Dict for O(1) access, doubly-linked list for LRU ordering
        self._storage: Dict[Hashable, CacheEntry] = {}

        # Doubly-linked list sentinels for LRU ordering
        self._head = CacheEntry(key=None, value=None, timestamp=0, access_time=0, ttl=None)
        self._tail = CacheEntry(key=None, value=None, timestamp=0, access_time=0, ttl=None)
        self._head.next = self._tail
        self._tail.prev = self._head

        # Statistics and thread safety
        self._stats = CacheStats(capacity=capacity)
        self._lock = threading.RLock()

    @property
    def capacity(self) -> int:
        """Return the maximum capacity of the cache"""
        return self._capacity

    def size(self) -> int:
        """Return the current number of items in the cache"""
        with self._lock:
            return len(self._storage)

    def __len__(self) -> int:
        """Return the current number of items in the cache"""
        return self.size()

    def __contains__(self, key: Hashable) -> bool:
        """Check if key exists in cache and is not expired"""
        with self._lock:
            if key not in self._storage:
                return False

            entry = self._storage[key]
            if entry.is_expired():
                # Remove expired entry
                self._remove_entry(entry)
                return False

            return True

    def _remove_entry(self, entry: CacheEntry) -> None:
        """Remove entry from both storage and LRU list (internal use)"""
        # Remove from storage
        if entry.key in self._storage:
            del self._storage[entry.key]

        # Remove from LRU list
        if entry.prev:
            entry.prev.next = entry.next
        if entry.next:
            entry.next.prev = entry.prev

    def _move_to_front(self, entry: CacheEntry) -> None:
        """Move entry to front of LRU list (most recently used)"""
        # Remove from current position
        if entry.prev:
            entry.prev.next = entry.next
        if entry.next:
            entry.next.prev = entry.prev

        # Insert at front (after head sentinel)
        entry.prev = self._head
        entry.next = self._head.next
        self._head.next.prev = entry
        self._head.next = entry

    def _add_to_front(self, entry: CacheEntry) -> None:
        """Add new entry to front of LRU list"""
        entry.prev = self._head
        entry.next = self._head.next
        self._head.next.prev = entry
        self._head.next = entry

    def _remove_tail(self) -> Optional[CacheEntry]:
        """Remove and return the least recently used entry"""
        if self._tail.prev == self._head:
            return None  # Empty list

        lru_entry = self._tail.prev
        self._remove_entry(lru_entry)
        return lru_entry

    def set(self, key: Hashable, value: Any, ttl: Optional[float] = None) -> None:
        """
        Store a key-value pair in the cache

        Args:
            key: The key to store (must be hashable)
            value: The value to store
            ttl: TTL in seconds (None uses default_ttl)
        """
        if key is None:
            raise ValueError("Key cannot be None")

        with self._lock:
            current_time = time.time()
            effective_ttl = ttl if ttl is not None else self.default_ttl

            if key in self._storage:
                # Update existing entry
                entry = self._storage[key]
                entry.value = value
                entry.timestamp = current_time
                entry.access_time = current_time
                entry.ttl = effective_ttl
                self._move_to_front(entry)
            else:
                # Create new entry
                entry = CacheEntry(
                    key=key,
                    value=value,
                    timestamp=current_time,
                    access_time=current_time,
                    ttl=effective_ttl
                )

                # Check if we need to evict
                while len(self._storage) >= self._capacity:
                    evicted = self._remove_tail()
                    if evicted:
                        self._stats.evictions += 1

                # Add new entry
                self._storage[key] = entry
                self._add_to_front(entry)

            # Update statistics
            self._stats.current_size = len(self._storage)

    def get(self, key: Hashable) -> Any:
        """
        Retrieve a value from the cache

        Args:
            key: The key to retrieve

        Returns:
            The stored value

        Raises:
            KeyError: If key doesn't exist or has expired
        """
        with self._lock:
            if key not in self._storage:
                self._stats.misses += 1
                raise KeyError(f"Key '{key}' not found in cache")

            entry = self._storage[key]

            # Check expiration
            if entry.is_expired():
                self._remove_entry(entry)
                self._stats.misses += 1
                self._stats.current_size = len(self._storage)
                raise KeyError(f"Key '{key}' has expired")

            # Update access time and move to front
            entry.access_time = time.time()
            self._move_to_front(entry)

            self._stats.hits += 1
            return entry.value

    def delete(self, key: Hashable) -> bool:
        """
        Delete a key from the cache

        Args:
            key: The key to delete

        Returns:
            True if key was deleted, False if key didn't exist
        """
        with self._lock:
            if key not in self._storage:
                return False

            entry = self._storage[key]
            self._remove_entry(entry)
            self._stats.current_size = len(self._storage)
            return True

    def clear(self) -> None:
        """Remove all items from the cache"""
        with self._lock:
            self._storage.clear()
            self._head.next = self._tail
            self._tail.prev = self._head
            self._stats.current_size = 0

    def keys(self) -> List[Hashable]:
        """Return list of all keys (excludes expired items)"""
        with self._lock:
            self._cleanup_expired()
            return list(self._storage.keys())

    def values(self) -> List[Any]:
        """Return list of all values (excludes expired items)"""
        with self._lock:
            self._cleanup_expired()
            return [entry.value for entry in self._storage.values()]

    def items(self) -> List[Tuple[Hashable, Any]]:
        """Return list of all key-value pairs (excludes expired items)"""
        with self._lock:
            self._cleanup_expired()
            return [(key, entry.value) for key, entry in self._storage.items()]

    def stats(self) -> CacheStats:
        """Return current cache statistics"""
        with self._lock:
            self._stats.current_size = len(self._storage)
            # Return a copy to prevent external modification
            return CacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
                current_size=self._stats.current_size,
                capacity=self._stats.capacity
            )

    def cleanup_expired(self) -> int:
        """Remove all expired entries and return count removed"""
        with self._lock:
            return self._cleanup_expired()

    def _cleanup_expired(self) -> int:
        """Internal method to cleanup expired entries"""
        expired_keys = []
        current_time = time.time()

        for key, entry in self._storage.items():
            if entry.is_expired():
                expired_keys.append(key)

        for key in expired_keys:
            entry = self._storage[key]
            self._remove_entry(entry)

        self._stats.current_size = len(self._storage)
        return len(expired_keys)

    def resize(self, new_capacity: int) -> None:
        """
        Resize the cache capacity

        Args:
            new_capacity: New maximum capacity (must be positive)

        Raises:
            ValueError: If new_capacity <= 0
        """
        if not isinstance(new_capacity, int) or new_capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        with self._lock:
            self._capacity = new_capacity
            self._stats.capacity = new_capacity

            # Evict items if necessary
            while len(self._storage) > new_capacity:
                evicted = self._remove_tail()
                if evicted:
                    self._stats.evictions += 1

            self._stats.current_size = len(self._storage)

    def is_expired(self, key: Hashable) -> bool:
        """
        Check if a key has expired

        Args:
            key: The key to check

        Returns:
            True if key exists and is expired, False otherwise
        """
        with self._lock:
            if key not in self._storage:
                return False
            return self._storage[key].is_expired()

    def __getitem__(self, key: Hashable) -> Any:
        """Dictionary-style get"""
        return self.get(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Dictionary-style set"""
        self.set(key, value)

    def __delitem__(self, key: Hashable) -> None:
        """Dictionary-style delete"""
        if not self.delete(key):
            raise KeyError(f"Key '{key}' not found in cache")

    def __iter__(self) -> Iterator[Hashable]:
        """Iterate over keys"""
        return iter(self.keys())