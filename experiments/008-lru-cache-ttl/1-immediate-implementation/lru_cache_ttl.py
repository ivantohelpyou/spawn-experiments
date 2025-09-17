"""
LRU Cache with TTL (Time-To-Live) Implementation

This module provides a thread-safe LRU cache with TTL functionality.
Features:
- Least Recently Used (LRU) eviction policy
- Time-To-Live (TTL) expiration for entries
- Thread-safe operations with proper locking
- Configurable maximum capacity
- Statistics tracking (hits, misses, evictions)
- Optional persistence and configuration
"""

import time
import threading
from typing import Any, Optional, Dict, Tuple, Iterator
from collections import OrderedDict
import json
import os
from datetime import datetime, timedelta


class CacheEntry:
    """Represents a single cache entry with value and expiration time."""

    def __init__(self, value: Any, ttl_seconds: Optional[float] = None):
        self.value = value
        self.created_at = time.time()
        self.last_accessed = self.created_at
        self.expires_at = self.created_at + ttl_seconds if ttl_seconds else None
        self.access_count = 1

    def is_expired(self) -> bool:
        """Check if this entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def touch(self) -> None:
        """Update the last accessed time and increment access count."""
        self.last_accessed = time.time()
        self.access_count += 1

    def time_to_live(self) -> Optional[float]:
        """Get remaining TTL in seconds, or None if no expiration."""
        if self.expires_at is None:
            return None
        remaining = self.expires_at - time.time()
        return max(0, remaining)


class LRUCacheWithTTL:
    """
    A thread-safe LRU Cache with TTL (Time-To-Live) functionality.

    This cache maintains a maximum capacity and evicts the least recently used
    items when full. Items also automatically expire after their TTL.
    """

    def __init__(self, max_size: int = 128, default_ttl: Optional[float] = None):
        """
        Initialize the LRU Cache with TTL.

        Args:
            max_size: Maximum number of items to store in cache
            default_ttl: Default TTL in seconds for new entries (None = no expiration)
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()

        # Statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'expirations': 0,
            'sets': 0,
            'deletes': 0
        }

        # Background cleanup
        self._cleanup_interval = 60  # seconds
        self._cleanup_thread = None
        self._stop_cleanup = threading.Event()
        self._start_cleanup_thread()

    def _start_cleanup_thread(self) -> None:
        """Start the background cleanup thread."""
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_expired_entries,
            daemon=True
        )
        self._cleanup_thread.start()

    def _cleanup_expired_entries(self) -> None:
        """Background thread to clean up expired entries."""
        while not self._stop_cleanup.wait(self._cleanup_interval):
            with self._lock:
                expired_keys = [
                    key for key, entry in self._cache.items()
                    if entry.is_expired()
                ]
                for key in expired_keys:
                    del self._cache[key]
                    self._stats['expirations'] += 1

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
            key: The cache key

        Returns:
            The cached value, or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                self._stats['misses'] += 1
                return None

            entry = self._cache[key]

            # Check if expired
            if entry.is_expired():
                del self._cache[key]
                self._stats['misses'] += 1
                self._stats['expirations'] += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            entry.touch()
            self._stats['hits'] += 1

            return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        Set a value in the cache.

        Args:
            key: The cache key
            value: The value to cache
            ttl: TTL in seconds (uses default_ttl if None)
        """
        with self._lock:
            ttl_to_use = ttl if ttl is not None else self.default_ttl

            if key in self._cache:
                # Update existing entry
                self._cache[key] = CacheEntry(value, ttl_to_use)
                self._cache.move_to_end(key)
            else:
                # Add new entry
                if len(self._cache) >= self.max_size:
                    # Evict least recently used item
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                    self._stats['evictions'] += 1

                self._cache[key] = CacheEntry(value, ttl_to_use)

            self._stats['sets'] += 1

    def delete(self, key: str) -> bool:
        """
        Delete a key from the cache.

        Args:
            key: The cache key to delete

        Returns:
            True if the key was found and deleted, False otherwise
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._stats['deletes'] += 1
                return True
            return False

    def clear(self) -> None:
        """Clear all items from the cache."""
        with self._lock:
            self._cache.clear()

    def exists(self, key: str) -> bool:
        """Check if a key exists and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False

            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                self._stats['expirations'] += 1
                return False

            return True

    def ttl(self, key: str) -> Optional[float]:
        """Get the remaining TTL for a key in seconds."""
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                self._stats['expirations'] += 1
                return None

            return entry.time_to_live()

    def size(self) -> int:
        """Get the current number of items in the cache."""
        with self._lock:
            return len(self._cache)

    def capacity(self) -> int:
        """Get the maximum capacity of the cache."""
        return self.max_size

    def is_full(self) -> bool:
        """Check if the cache is at maximum capacity."""
        return self.size() >= self.max_size

    def keys(self) -> Iterator[str]:
        """Get an iterator over all non-expired keys."""
        with self._lock:
            # Clean up expired entries first
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._cache[key]
                self._stats['expirations'] += 1

            return iter(list(self._cache.keys()))

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Get an iterator over all non-expired key-value pairs."""
        with self._lock:
            # Clean up expired entries first
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._cache[key]
                self._stats['expirations'] += 1

            return iter([(key, entry.value) for key, entry in self._cache.items()])

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            stats = self._stats.copy()
            stats.update({
                'size': len(self._cache),
                'capacity': self.max_size,
                'hit_rate': stats['hits'] / (stats['hits'] + stats['misses']) if (stats['hits'] + stats['misses']) > 0 else 0,
                'load_factor': len(self._cache) / self.max_size
            })
            return stats

    def reset_stats(self) -> None:
        """Reset all statistics counters."""
        with self._lock:
            for key in self._stats:
                self._stats[key] = 0

    def save_to_file(self, filepath: str) -> None:
        """Save cache contents to a JSON file."""
        with self._lock:
            data = {
                'max_size': self.max_size,
                'default_ttl': self.default_ttl,
                'timestamp': time.time(),
                'entries': {}
            }

            for key, entry in self._cache.items():
                if not entry.is_expired():
                    data['entries'][key] = {
                        'value': entry.value,
                        'created_at': entry.created_at,
                        'expires_at': entry.expires_at,
                        'access_count': entry.access_count
                    }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str) -> bool:
        """Load cache contents from a JSON file."""
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            with self._lock:
                self.clear()
                self.max_size = data.get('max_size', self.max_size)
                self.default_ttl = data.get('default_ttl', self.default_ttl)

                current_time = time.time()
                for key, entry_data in data.get('entries', {}).items():
                    # Only load non-expired entries
                    expires_at = entry_data.get('expires_at')
                    if expires_at is None or current_time <= expires_at:
                        entry = CacheEntry(entry_data['value'])
                        entry.created_at = entry_data.get('created_at', current_time)
                        entry.expires_at = expires_at
                        entry.access_count = entry_data.get('access_count', 1)
                        entry.last_accessed = current_time
                        self._cache[key] = entry

            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            return False

    def __len__(self) -> int:
        """Get the current size of the cache."""
        return self.size()

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        return self.exists(key)

    def __getitem__(self, key: str) -> Any:
        """Get an item from the cache (raises KeyError if not found)."""
        value = self.get(key)
        if value is None and key not in self._cache:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an item in the cache."""
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Delete an item from the cache (raises KeyError if not found)."""
        if not self.delete(key):
            raise KeyError(key)

    def __repr__(self) -> str:
        """String representation of the cache."""
        with self._lock:
            return f"LRUCacheWithTTL(size={len(self._cache)}, capacity={self.max_size}, default_ttl={self.default_ttl})"

    def close(self) -> None:
        """Clean up resources and stop background threads."""
        self._stop_cleanup.set()
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=1)

    def __del__(self) -> None:
        """Cleanup when object is destroyed."""
        try:
            self.close()
        except:
            pass


# Factory function for easy creation
def create_cache(max_size: int = 128, default_ttl: Optional[float] = None) -> LRUCacheWithTTL:
    """
    Factory function to create an LRU Cache with TTL.

    Args:
        max_size: Maximum number of items to store
        default_ttl: Default TTL in seconds for new entries

    Returns:
        A new LRUCacheWithTTL instance
    """
    return LRUCacheWithTTL(max_size=max_size, default_ttl=default_ttl)


if __name__ == "__main__":
    # Demo usage
    print("LRU Cache with TTL Demo")
    print("=" * 50)

    # Create cache with max 5 items and 10-second default TTL
    cache = create_cache(max_size=5, default_ttl=10.0)

    # Add some items
    cache.set("user:1", {"name": "Alice", "age": 30})
    cache.set("user:2", {"name": "Bob", "age": 25})
    cache.set("config", {"theme": "dark", "lang": "en"})

    print(f"Cache size: {cache.size()}")
    print(f"Stats: {cache.get_stats()}")

    # Access items
    print(f"user:1 = {cache.get('user:1')}")
    print(f"user:2 = {cache.get('user:2')}")

    # Check TTL
    print(f"TTL for user:1: {cache.ttl('user:1'):.2f} seconds")

    # Add item with custom TTL
    cache.set("temp", "temporary data", ttl=2.0)
    print(f"Added temp item with 2-second TTL")

    print(f"Final stats: {cache.get_stats()}")

    # Cleanup
    cache.close()