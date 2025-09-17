"""
Comprehensive test suite for LRU Cache with TTL using Test-Driven Development
with rigorous test validation methodology.
"""

import unittest
import time
from typing import Any, Optional


class CacheError(Exception):
    """Base exception for cache-related errors."""
    pass


class CacheCapacityError(CacheError):
    """Raised when invalid capacity is provided."""
    pass


class CacheTTLError(CacheError):
    """Raised when invalid TTL is provided."""
    pass


class LRUCacheWithTTL:
    """
    LRU Cache with TTL - A cache that evicts least recently used items
    and automatically expires items after their time-to-live period.

    This implementation focuses on cache initialization and basic structure.
    Additional features (put/get/eviction) will be added in subsequent TDD cycles.
    """

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        """
        Initialize the LRU Cache with TTL.

        Args:
            capacity: Maximum number of items the cache can hold (must be > 0)
            default_ttl: Default time-to-live in seconds for cache items.
                        None means no expiration. Must be >= 0 if provided.

        Raises:
            CacheCapacityError: If capacity <= 0
            CacheTTLError: If default_ttl < 0
        """
        self._validate_capacity(capacity)
        self._validate_ttl(default_ttl)

        # Cache configuration
        self.capacity = capacity
        self.default_ttl = default_ttl

        # Cache storage (will be enhanced for LRU + TTL in later iterations)
        self._data = {}

    def _validate_capacity(self, capacity: int) -> None:
        """Validate that capacity is a positive integer."""
        if not isinstance(capacity, int) or capacity <= 0:
            raise CacheCapacityError(f"Capacity must be a positive integer, got {capacity}")

    def _validate_ttl(self, ttl: Optional[float]) -> None:
        """Validate that TTL is non-negative if provided."""
        if ttl is not None and ttl < 0:
            raise CacheTTLError(f"TTL must be non-negative, got {ttl}")

    def size(self) -> int:
        """Return the current number of items in cache."""
        return len(self._data)

    def keys(self) -> list:
        """Return list of all keys currently in cache."""
        return list(self._data.keys())

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        Store a key-value pair in the cache.

        Args:
            key: The key to store
            value: The value to associate with the key
            ttl: Time-to-live for this specific item. If None, uses default_ttl.

        Note: This basic implementation doesn't yet handle LRU eviction or TTL expiration.
        Those features will be added in subsequent TDD cycles.
        """
        # Basic storage - will be enhanced for TTL and LRU in later iterations
        self._data[key] = value

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value by key from the cache.

        Args:
            key: The key to look up

        Returns:
            The value associated with the key, or None if key doesn't exist.

        Note: This basic implementation doesn't yet handle TTL expiration or LRU updates.
        Those features will be added in subsequent TDD cycles.
        """
        return self._data.get(key)


class TestBasicPutGetOperations(unittest.TestCase):
    """Test basic put and get operations with comprehensive validation."""

    def test_put_and_get_single_item(self):
        """
        Test: Store and retrieve a single item.

        Purpose: Verify basic put/get functionality works.
        What could go wrong: Item might not be stored, or wrong value returned.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1")
        result = cache.get("key1")

        self.assertEqual(result, "value1")
        self.assertEqual(cache.size(), 1)

    def test_put_multiple_items_and_get_each(self):
        """
        Test: Store multiple items and retrieve each one.

        Purpose: Verify cache handles multiple items correctly.
        What could go wrong: Items might overwrite each other or be lost.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")

        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")
        self.assertEqual(cache.size(), 3)

    def test_put_overwrites_existing_key(self):
        """
        Test: Putting same key twice overwrites the value.

        Purpose: Verify put operations update existing keys.
        What could go wrong: Duplicate keys might create multiple entries.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1")
        cache.put("key1", "new_value")

        self.assertEqual(cache.get("key1"), "new_value")
        self.assertEqual(cache.size(), 1)  # Should still be 1 item

    def test_get_nonexistent_key_returns_none(self):
        """
        Test: Getting non-existent key returns None.

        Purpose: Verify proper handling of missing keys.
        What could go wrong: Might raise exception or return wrong value.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        result = cache.get("nonexistent")

        self.assertIsNone(result)

    def test_get_from_empty_cache_returns_none(self):
        """
        Test: Getting from empty cache returns None.

        Purpose: Verify empty cache handling.
        What could go wrong: Might raise exception or return wrong value.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        result = cache.get("any_key")

        self.assertIsNone(result)

    def test_put_with_custom_ttl(self):
        """
        Test: Put item with custom TTL different from default.

        Purpose: Verify per-item TTL customization works.
        What could go wrong: Custom TTL might be ignored or applied incorrectly.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1", ttl=30.0)
        result = cache.get("key1")

        self.assertEqual(result, "value1")

    def test_put_various_value_types(self):
        """
        Test: Put and get various data types as values.

        Purpose: Verify cache handles different Python objects.
        What could go wrong: Certain types might not be stored correctly.
        """
        cache = LRUCacheWithTTL(capacity=5, default_ttl=60.0)

        test_values = {
            "string": "hello",
            "integer": 42,
            "float": 3.14,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }

        # Put all values
        for key, value in test_values.items():
            cache.put(key, value)

        # Get and verify all values
        for key, expected_value in test_values.items():
            result = cache.get(key)
            self.assertEqual(result, expected_value)

    def test_keys_method_reflects_put_operations(self):
        """
        Test: keys() method returns correct keys after put operations.

        Purpose: Verify keys() stays synchronized with put operations.
        What could go wrong: keys() might not update or return wrong keys.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        # Initially empty
        self.assertEqual(set(cache.keys()), set())

        # After adding items
        cache.put("key1", "value1")
        cache.put("key2", "value2")

        self.assertEqual(set(cache.keys()), {"key1", "key2"})


class TestCacheInitialization(unittest.TestCase):
    """Test cache initialization with comprehensive validation."""

    def test_cache_init_with_valid_capacity_and_default_ttl(self):
        """
        Test: Cache initializes correctly with valid capacity and default TTL.

        Purpose: Verify basic cache creation with standard parameters.
        What could go wrong: Cache might not store parameters correctly,
        or might reject valid inputs.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        # Cache should be created and accessible
        assert cache is not None
        assert hasattr(cache, 'capacity')
        assert hasattr(cache, 'default_ttl')
        assert cache.capacity == 3
        assert cache.default_ttl == 60.0

    def test_cache_init_with_capacity_only_no_default_ttl(self):
        """
        Test: Cache initializes with capacity but no default TTL.

        Purpose: Verify cache works when TTL is optional (None).
        What could go wrong: Cache might require TTL or fail with None.
        """
        cache = LRUCacheWithTTL(capacity=5)

        assert cache is not None
        assert cache.capacity == 5
        assert cache.default_ttl is None

    def test_cache_init_with_minimum_capacity(self):
        """
        Test: Cache initializes with minimum valid capacity (1).

        Purpose: Verify edge case of single-item cache.
        What could go wrong: Logic might fail with capacity 1.
        """
        cache = LRUCacheWithTTL(capacity=1, default_ttl=30.0)

        assert cache.capacity == 1
        assert cache.default_ttl == 30.0

    def test_cache_starts_empty(self):
        """
        Test: Newly created cache is empty.

        Purpose: Verify initial state is clean.
        What could go wrong: Cache might have pre-existing data.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        # Cache should start with size 0
        assert cache.size() == 0
        assert len(cache.keys()) == 0

    def test_cache_init_zero_capacity_raises_error(self):
        """
        Test: Cache initialization fails with zero capacity.

        Purpose: Verify input validation for invalid capacity.
        What could go wrong: Cache might accept invalid capacity or
        raise wrong exception type.
        """
        with self.assertRaises(CacheCapacityError):
            LRUCacheWithTTL(capacity=0, default_ttl=60.0)

    def test_cache_init_negative_capacity_raises_error(self):
        """
        Test: Cache initialization fails with negative capacity.

        Purpose: Verify input validation rejects negative values.
        What could go wrong: Cache might accept negative values.
        """
        with self.assertRaises(CacheCapacityError):
            LRUCacheWithTTL(capacity=-1, default_ttl=60.0)

    def test_cache_init_negative_ttl_raises_error(self):
        """
        Test: Cache initialization fails with negative TTL.

        Purpose: Verify TTL validation rejects negative values.
        What could go wrong: Cache might accept negative TTL.
        """
        with self.assertRaises(CacheTTLError):
            LRUCacheWithTTL(capacity=3, default_ttl=-10.0)

    def test_cache_init_zero_ttl_is_valid(self):
        """
        Test: Cache accepts TTL of zero (immediate expiration).

        Purpose: Verify edge case where items expire immediately.
        What could go wrong: Zero TTL might be rejected as invalid.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=0.0)

        assert cache.default_ttl == 0.0

    def test_cache_init_large_capacity(self):
        """
        Test: Cache handles large capacity values.

        Purpose: Verify scalability for large caches.
        What could go wrong: Large numbers might cause overflow or rejection.
        """
        cache = LRUCacheWithTTL(capacity=10000, default_ttl=3600.0)

        assert cache.capacity == 10000
        assert cache.default_ttl == 3600.0


if __name__ == "__main__":
    unittest.main()