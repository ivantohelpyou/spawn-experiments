"""
Comprehensive tests for LRU Cache with TTL implementation.

Tests cover all functional requirements, edge cases, thread safety,
and performance characteristics specified in the requirements.
"""

import pytest
import time
import threading
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor, as_completed

from lru_cache_ttl import LRUCacheWithTTL, CacheStats, CacheNode


class TestCacheNode:
    """Test the CacheNode class."""

    def test_node_creation(self):
        """Test basic node creation."""
        node = CacheNode("key1", "value1", time.time() + 10)
        assert node.key == "key1"
        assert node.value == "value1"
        assert node.expiry_time > time.time()
        assert node.prev is None
        assert node.next is None

    def test_node_expiration(self):
        """Test node expiration logic."""
        # Non-expiring node
        node1 = CacheNode("key1", "value1", 0)
        assert not node1.is_expired()

        # Expired node
        node2 = CacheNode("key2", "value2", time.time() - 1)
        assert node2.is_expired()

        # Not yet expired node
        node3 = CacheNode("key3", "value3", time.time() + 10)
        assert not node3.is_expired()


class TestCacheStats:
    """Test the CacheStats class."""

    def test_initial_stats(self):
        """Test initial statistics values."""
        stats = CacheStats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.evictions == 0
        assert stats.expirations == 0
        assert stats.total_operations == 0
        assert stats.hit_rate() == 0.0

    def test_hit_rate_calculation(self):
        """Test hit rate calculation."""
        stats = CacheStats()

        # Test with zero operations
        assert stats.hit_rate() == 0.0

        # Test with some operations
        stats.hits = 7
        stats.misses = 3
        stats.total_operations = 10
        assert stats.hit_rate() == 70.0

    def test_stats_reset(self):
        """Test statistics reset functionality."""
        stats = CacheStats()
        stats.hits = 5
        stats.misses = 3
        stats.evictions = 2
        stats.expirations = 1
        stats.total_operations = 8

        stats.reset()

        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.evictions == 0
        assert stats.expirations == 0
        assert stats.total_operations == 0


class TestLRUCacheWithTTL:
    """Test the main LRU cache implementation."""

    def test_cache_creation(self):
        """Test cache creation with valid parameters."""
        cache = LRUCacheWithTTL(capacity=5, default_ttl=10.0)
        assert cache.capacity == 5
        assert cache.default_ttl == 10.0
        assert cache.size() == 0
        assert cache.is_empty()

    def test_invalid_capacity(self):
        """Test cache creation with invalid capacity."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            LRUCacheWithTTL(capacity=0)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            LRUCacheWithTTL(capacity=-1)

    def test_basic_put_get(self):
        """Test basic put and get operations."""
        cache = LRUCacheWithTTL(capacity=3)

        # Test put and get
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache.size() == 1
        assert not cache.is_empty()

        # Test overwrite
        cache.put("key1", "new_value1")
        assert cache.get("key1") == "new_value1"
        assert cache.size() == 1

    def test_cache_miss(self):
        """Test cache miss scenarios."""
        cache = LRUCacheWithTTL(capacity=3)

        # Get from empty cache
        assert cache.get("nonexistent") is None

        # Get after putting different key
        cache.put("key1", "value1")
        assert cache.get("key2") is None

    def test_lru_eviction(self):
        """Test LRU eviction when capacity is reached."""
        cache = LRUCacheWithTTL(capacity=2)

        # Fill cache to capacity
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        assert cache.size() == 2

        # Add third item - should evict key1 (LRU)
        cache.put("key3", "value3")
        assert cache.size() == 2
        assert cache.get("key1") is None  # Evicted
        assert cache.get("key2") == "value2"  # Still there
        assert cache.get("key3") == "value3"  # Newly added

    def test_lru_ordering(self):
        """Test that access updates LRU ordering."""
        cache = LRUCacheWithTTL(capacity=2)

        cache.put("key1", "value1")
        cache.put("key2", "value2")

        # Access key1 to make it recently used
        cache.get("key1")

        # Add key3 - should evict key2 (now LRU)
        cache.put("key3", "value3")
        assert cache.get("key1") == "value1"  # Still there
        assert cache.get("key2") is None     # Evicted
        assert cache.get("key3") == "value3"  # Newly added

    def test_ttl_expiration(self):
        """Test TTL expiration functionality."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=0.1)  # 100ms TTL

        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"

        # Wait for expiration
        time.sleep(0.15)
        assert cache.get("key1") is None
        assert cache.size() == 0  # Should be removed automatically

    def test_custom_ttl(self):
        """Test custom TTL override."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=10.0)

        # Add item with custom short TTL
        cache.put("temp", "temporary", ttl=0.1)
        cache.put("permanent", "permanent")  # Uses default TTL

        assert cache.get("temp") == "temporary"
        assert cache.get("permanent") == "permanent"

        # Wait for custom TTL to expire
        time.sleep(0.15)
        assert cache.get("temp") is None
        assert cache.get("permanent") == "permanent"  # Still there

    def test_no_ttl(self):
        """Test items with no expiration (TTL=0)."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=0)

        cache.put("key1", "value1", ttl=0)
        time.sleep(0.1)  # Wait a bit
        assert cache.get("key1") == "value1"  # Should not expire

    def test_delete_operation(self):
        """Test delete operation."""
        cache = LRUCacheWithTTL(capacity=3)

        cache.put("key1", "value1")
        cache.put("key2", "value2")

        # Delete existing key
        assert cache.delete("key1") is True
        assert cache.get("key1") is None
        assert cache.size() == 1

        # Delete non-existent key
        assert cache.delete("nonexistent") is False
        assert cache.size() == 1

    def test_clear_operation(self):
        """Test clear operation."""
        cache = LRUCacheWithTTL(capacity=3)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        assert cache.size() == 3

        cache.clear()
        assert cache.size() == 0
        assert cache.is_empty()
        assert cache.get("key1") is None

    def test_cleanup_expired(self):
        """Test manual cleanup of expired items."""
        cache = LRUCacheWithTTL(capacity=5, default_ttl=0.1)

        # Add items that will expire
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3", ttl=0)  # No expiration

        assert cache.size() == 3

        # Wait for expiration
        time.sleep(0.15)

        # Manual cleanup
        expired_count = cache.cleanup_expired()
        assert expired_count == 2  # key1 and key2 expired
        assert cache.size() == 1   # Only key3 remains
        assert cache.get("key3") == "value3"

    def test_remaining_ttl(self):
        """Test remaining TTL functionality."""
        cache = LRUCacheWithTTL(capacity=3)

        # Non-existent key
        assert cache.get_remaining_ttl("nonexistent") is None

        # Key with no expiration
        cache.put("permanent", "value", ttl=0)
        assert cache.get_remaining_ttl("permanent") == 0

        # Key with TTL
        cache.put("temporary", "value", ttl=1.0)
        remaining = cache.get_remaining_ttl("temporary")
        assert 0.9 <= remaining <= 1.0  # Should be close to 1 second

    def test_set_default_ttl(self):
        """Test setting default TTL."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=1.0)

        cache.set_default_ttl(2.0)
        assert cache.default_ttl == 2.0

    def test_statistics_tracking(self):
        """Test cache statistics tracking."""
        cache = LRUCacheWithTTL(capacity=2)

        # Initial stats
        stats = cache.get_stats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.evictions == 0
        assert stats.expirations == 0
        assert stats.total_operations == 0

        # Test operations and stats
        cache.put("key1", "value1")  # Operation 1
        cache.get("key1")           # Operation 2 - hit
        cache.get("key2")           # Operation 3 - miss

        stats = cache.get_stats()
        assert stats.hits == 1
        assert stats.misses == 1
        assert stats.total_operations == 2  # Only get operations count
        assert stats.hit_rate() == 50.0

        # Test eviction stats
        cache.put("key2", "value2")  # Operation 4
        cache.put("key3", "value3")  # Operation 5 - causes eviction

        stats = cache.get_stats()
        assert stats.evictions == 1

    def test_reset_statistics(self):
        """Test resetting statistics."""
        cache = LRUCacheWithTTL(capacity=2)

        # Generate some stats
        cache.put("key1", "value1")
        cache.get("key1")
        cache.get("key2")

        # Reset stats
        cache.reset_stats()
        stats = cache.get_stats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.total_operations == 0

    def test_contains_operator(self):
        """Test 'in' operator."""
        cache = LRUCacheWithTTL(capacity=3, default_ttl=0.1)

        cache.put("key1", "value1")
        assert "key1" in cache
        assert "key2" not in cache

        # Test with expired item
        time.sleep(0.15)
        assert "key1" not in cache

    def test_len_operator(self):
        """Test len() function."""
        cache = LRUCacheWithTTL(capacity=3)

        assert len(cache) == 0

        cache.put("key1", "value1")
        assert len(cache) == 1

        cache.put("key2", "value2")
        assert len(cache) == 2

    def test_repr(self):
        """Test string representation."""
        cache = LRUCacheWithTTL(capacity=5)
        repr_str = repr(cache)
        assert "LRUCacheWithTTL" in repr_str
        assert "capacity=5" in repr_str
        assert "size=0" in repr_str

    def test_edge_case_single_capacity(self):
        """Test cache with capacity of 1."""
        cache = LRUCacheWithTTL(capacity=1)

        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache.size() == 1

        # Adding second item should evict first
        cache.put("key2", "value2")
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.size() == 1

    def test_edge_case_large_capacity(self):
        """Test cache with large capacity."""
        cache = LRUCacheWithTTL(capacity=1000)

        # Add many items
        for i in range(500):
            cache.put(f"key{i}", f"value{i}")

        assert cache.size() == 500

        # Verify all items are accessible
        for i in range(500):
            assert cache.get(f"key{i}") == f"value{i}"

    def test_different_key_types(self):
        """Test cache with different key types."""
        cache = LRUCacheWithTTL(capacity=5)

        # String keys
        cache.put("string_key", "string_value")

        # Integer keys
        cache.put(42, "int_value")

        # Tuple keys
        cache.put((1, 2), "tuple_value")

        # Boolean keys
        cache.put(True, "bool_value")

        assert cache.get("string_key") == "string_value"
        assert cache.get(42) == "int_value"
        assert cache.get((1, 2)) == "tuple_value"
        assert cache.get(True) == "bool_value"

    def test_different_value_types(self):
        """Test cache with different value types."""
        cache = LRUCacheWithTTL(capacity=5)

        # Different value types
        cache.put("string", "string_value")
        cache.put("int", 42)
        cache.put("list", [1, 2, 3])
        cache.put("dict", {"a": 1, "b": 2})
        cache.put("none", None)

        assert cache.get("string") == "string_value"
        assert cache.get("int") == 42
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"a": 1, "b": 2}
        assert cache.get("none") is None


class TestThreadSafety:
    """Test thread safety of the cache."""

    def test_concurrent_access(self):
        """Test concurrent read/write operations."""
        cache = LRUCacheWithTTL(capacity=100)
        results = []

        def worker(thread_id):
            """Worker function for concurrent testing."""
            local_results = []
            for i in range(50):
                key = f"key_{thread_id}_{i}"
                value = f"value_{thread_id}_{i}"

                # Put operation
                cache.put(key, value)

                # Get operation
                retrieved = cache.get(key)
                local_results.append(retrieved == value)

                # Some random gets
                cache.get(f"key_{(thread_id + 1) % 5}_{i % 10}")

            return local_results

        # Run concurrent workers
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(worker, i) for i in range(5)]

            for future in as_completed(futures):
                thread_results = future.result()
                results.extend(thread_results)

        # All operations should have succeeded
        assert all(results), f"Some operations failed: {results.count(False)} out of {len(results)}"

    def test_concurrent_eviction(self):
        """Test that eviction works correctly under concurrent load."""
        cache = LRUCacheWithTTL(capacity=10)

        def writer(start_key):
            """Write many items to trigger evictions."""
            for i in range(50):
                cache.put(f"key_{start_key}_{i}", f"value_{start_key}_{i}")

        # Run concurrent writers
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(writer, i) for i in range(3)]

            for future in as_completed(futures):
                future.result()

        # Cache should never exceed capacity
        assert cache.size() <= 10

    def test_concurrent_statistics(self):
        """Test that statistics remain consistent under concurrent access."""
        cache = LRUCacheWithTTL(capacity=50)

        def operations(thread_id):
            """Perform various cache operations."""
            for i in range(100):
                key = f"key_{thread_id}_{i}"

                # Put
                cache.put(key, f"value_{i}")

                # Get (hit)
                cache.get(key)

                # Get (miss)
                cache.get(f"nonexistent_{thread_id}_{i}")

        # Run concurrent operations
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(operations, i) for i in range(3)]

            for future in as_completed(futures):
                future.result()

        stats = cache.get_stats()

        # Basic sanity checks
        assert stats.total_operations > 0
        assert stats.hits > 0
        assert stats.misses > 0
        assert stats.hits + stats.misses == stats.total_operations


class TestPerformance:
    """Test performance characteristics."""

    def test_get_performance(self):
        """Test that get operations are reasonably fast."""
        cache = LRUCacheWithTTL(capacity=1000)

        # Fill cache
        for i in range(1000):
            cache.put(f"key{i}", f"value{i}")

        # Time get operations
        start_time = time.time()
        for i in range(1000):
            cache.get(f"key{i}")
        end_time = time.time()

        # Should be very fast (less than 0.1 seconds for 1000 operations)
        assert (end_time - start_time) < 0.1

    def test_put_performance(self):
        """Test that put operations are reasonably fast."""
        cache = LRUCacheWithTTL(capacity=1000)

        # Time put operations
        start_time = time.time()
        for i in range(1000):
            cache.put(f"key{i}", f"value{i}")
        end_time = time.time()

        # Should be very fast (less than 0.1 seconds for 1000 operations)
        assert (end_time - start_time) < 0.1


if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"])