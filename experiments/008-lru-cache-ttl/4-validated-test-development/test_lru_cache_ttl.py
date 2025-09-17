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


class CacheNode:
    """Node for doubly-linked list used in LRU implementation."""

    def __init__(self, key: str, value: Any, expiry_time: Optional[float] = None):
        self.key = key
        self.value = value
        self.expiry_time = expiry_time
        self.prev: Optional['CacheNode'] = None
        self.next: Optional['CacheNode'] = None


class LRUCacheWithTTL:
    """
    LRU Cache with TTL - A cache that evicts least recently used items
    and automatically expires items after their time-to-live period.

    Complete implementation with LRU eviction and TTL expiration.
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

        # LRU data structures
        self._data = {}  # key -> node mapping

        # Dummy head and tail for doubly-linked list
        self._head = CacheNode("", "")
        self._tail = CacheNode("", "")
        self._head.next = self._tail
        self._tail.prev = self._head

    def _validate_capacity(self, capacity: int) -> None:
        """Validate that capacity is a positive integer."""
        if not isinstance(capacity, int) or capacity <= 0:
            raise CacheCapacityError(f"Capacity must be a positive integer, got {capacity}")

    def _validate_ttl(self, ttl: Optional[float]) -> None:
        """Validate that TTL is non-negative if provided."""
        if ttl is not None and ttl < 0:
            raise CacheTTLError(f"TTL must be non-negative, got {ttl}")

    def _remove_node(self, node: CacheNode) -> None:
        """Remove node from doubly-linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: CacheNode) -> None:
        """Add node right after head (most recent position)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _move_to_head(self, node: CacheNode) -> None:
        """Move existing node to head (mark as most recent)."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> CacheNode:
        """Remove and return the least recently used node."""
        lru_node = self._tail.prev
        self._remove_node(lru_node)
        return lru_node

    def _is_expired(self, node: CacheNode) -> bool:
        """Check if a node has expired."""
        if node.expiry_time is None:
            return False
        return time.time() > node.expiry_time

    def _cleanup_expired(self, key: str, node: CacheNode) -> bool:
        """Remove expired node if expired. Returns True if removed."""
        if self._is_expired(node):
            self._remove_node(node)
            del self._data[key]
            return True
        return False

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
        """
        # Calculate expiry time
        effective_ttl = ttl if ttl is not None else self.default_ttl
        expiry_time = None if effective_ttl is None else time.time() + effective_ttl

        if key in self._data:
            # Update existing key
            node = self._data[key]
            node.value = value
            node.expiry_time = expiry_time
            self._move_to_head(node)
        else:
            # Add new key
            new_node = CacheNode(key, value, expiry_time)

            if len(self._data) >= self.capacity:
                # Remove LRU item
                lru_node = self._pop_tail()
                del self._data[lru_node.key]

            self._data[key] = new_node
            self._add_to_head(new_node)

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value by key from the cache.

        Args:
            key: The key to look up

        Returns:
            The value associated with the key, or None if key doesn't exist or expired.
        """
        if key not in self._data:
            return None

        node = self._data[key]

        # Check if expired
        if self._cleanup_expired(key, node):
            return None

        # Move to head (mark as most recent)
        self._move_to_head(node)
        return node.value


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


class TestLRUEviction(unittest.TestCase):
    """Test LRU eviction logic with comprehensive validation."""

    def test_eviction_when_capacity_exceeded(self):
        """
        Test: LRU item is evicted when capacity is exceeded.

        Purpose: Verify core LRU eviction functionality.
        What could go wrong: Wrong item evicted, no eviction, or crash.
        """
        cache = LRUCacheWithTTL(capacity=2, default_ttl=60.0)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")  # Should evict key1

        self.assertIsNone(cache.get("key1"))  # Should be evicted
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")
        self.assertEqual(cache.size(), 2)

    def test_get_updates_lru_order(self):
        """
        Test: Getting an item makes it most recently used.

        Purpose: Verify LRU order updates on access.
        What could go wrong: Access doesn't update order.
        """
        cache = LRUCacheWithTTL(capacity=2, default_ttl=60.0)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.get("key1")  # Make key1 most recent
        cache.put("key3", "value3")  # Should evict key2, not key1

        self.assertEqual(cache.get("key1"), "value1")  # Should still exist
        self.assertIsNone(cache.get("key2"))  # Should be evicted
        self.assertEqual(cache.get("key3"), "value3")

    def test_put_updates_lru_order(self):
        """
        Test: Updating existing key makes it most recently used.

        Purpose: Verify put on existing key updates LRU order.
        What could go wrong: Update doesn't change LRU position.
        """
        cache = LRUCacheWithTTL(capacity=2, default_ttl=60.0)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key1", "new_value1")  # Update key1, make it most recent
        cache.put("key3", "value3")  # Should evict key2

        self.assertEqual(cache.get("key1"), "new_value1")  # Should still exist
        self.assertIsNone(cache.get("key2"))  # Should be evicted
        self.assertEqual(cache.get("key3"), "value3")


class TestTTLExpiration(unittest.TestCase):
    """Test TTL expiration logic with comprehensive validation."""

    def test_item_expires_after_ttl(self):
        """
        Test: Item expires and returns None after TTL elapses.

        Purpose: Verify TTL expiration works.
        What could go wrong: Item doesn't expire or expires too early.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=0.1)  # 100ms TTL

        cache.put("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")  # Should exist

        time.sleep(0.15)  # Wait for expiration

        self.assertIsNone(cache.get("key1"))  # Should be expired
        self.assertEqual(cache.size(), 0)  # Should be removed

    def test_custom_ttl_overrides_default(self):
        """
        Test: Custom TTL takes precedence over default TTL.

        Purpose: Verify per-item TTL customization.
        What could go wrong: Default TTL used instead of custom.
        """
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1", ttl=0.1)  # Short TTL
        cache.put("key2", "value2")  # Uses default TTL

        time.sleep(0.15)

        self.assertIsNone(cache.get("key1"))  # Should be expired
        self.assertEqual(cache.get("key2"), "value2")  # Should still exist


class TestEdgeCasesAndIntegration(unittest.TestCase):
    """Test edge cases and integration scenarios."""

    def test_capacity_one_cache(self):
        """Test: Cache with capacity 1 works correctly."""
        cache = LRUCacheWithTTL(capacity=1, default_ttl=60.0)

        cache.put("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")

        cache.put("key2", "value2")  # Should evict key1
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.size(), 1)

    def test_lru_and_ttl_interaction(self):
        """Test: LRU and TTL work together correctly."""
        cache = LRUCacheWithTTL(capacity=2, default_ttl=0.1)

        cache.put("key1", "value1")
        cache.put("key2", "value2")

        # Access key1 to make it most recent
        cache.get("key1")

        # Add key3, should evict key2 (not key1)
        cache.put("key3", "value3")
        self.assertEqual(cache.get("key1"), "value1")
        self.assertIsNone(cache.get("key2"))
        self.assertEqual(cache.get("key3"), "value3")

        # Wait for TTL expiration
        time.sleep(0.15)

        # Both remaining items should be expired
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key3"))
        self.assertEqual(cache.size(), 0)

    def test_zero_ttl_immediate_expiration(self):
        """Test: TTL of 0 causes immediate expiration."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1", ttl=0.0)
        # Item should expire immediately or very quickly
        time.sleep(0.01)
        self.assertIsNone(cache.get("key1"))

    def test_none_ttl_never_expires(self):
        """Test: TTL of None means items never expire."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=None)

        cache.put("key1", "value1")
        # Even after a reasonable wait, item should still exist
        time.sleep(0.1)
        self.assertEqual(cache.get("key1"), "value1")


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