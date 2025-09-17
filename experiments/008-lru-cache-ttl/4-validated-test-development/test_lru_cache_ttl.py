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