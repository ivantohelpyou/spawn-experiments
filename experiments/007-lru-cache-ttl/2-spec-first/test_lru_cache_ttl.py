"""
Comprehensive test suite for LRU Cache with TTL implementation.

This test suite verifies all specifications defined in SPECIFICATIONS.md including:
- Core functionality (LRU eviction, TTL expiration)
- Edge cases and error conditions
- Thread safety
- Performance characteristics
- All user stories and acceptance criteria
"""

import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lru_cache_ttl import LRUCacheWithTTL, CacheNode, CacheStats, create_cache


class TestCacheNode:
    """Test the CacheNode class."""

    def test_node_creation(self):
        """Test basic node creation."""
        node = CacheNode("key1", "value1")
        assert node.key == "key1"
        assert node.value == "value1"
        assert node.expiration_time is None
        assert node.prev is None
        assert node.next is None

    def test_node_with_expiration(self):
        """Test node creation with expiration time."""
        exp_time = time.time() + 60
        node = CacheNode("key1", "value1", exp_time)
        assert node.expiration_time == exp_time

    def test_is_expired_no_expiration(self):
        """Test is_expired with no expiration set."""
        node = CacheNode("key1", "value1")
        assert not node.is_expired()

    def test_is_expired_not_expired(self):
        """Test is_expired with future expiration."""
        exp_time = time.time() + 60
        node = CacheNode("key1", "value1", exp_time)
        assert not node.is_expired()

    def test_is_expired_expired(self):
        """Test is_expired with past expiration."""
        exp_time = time.time() - 1
        node = CacheNode("key1", "value1", exp_time)
        assert node.is_expired()


class TestCacheStats:
    """Test the CacheStats class."""

    def test_stats_initialization(self):
        """Test initial stats values."""
        stats = CacheStats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.evictions == 0
        assert stats.expirations == 0
        assert stats.puts == 0
        assert stats.deletes == 0

    def test_stats_to_dict(self):
        """Test stats dictionary conversion."""
        stats = CacheStats()
        stats.hits = 10
        stats.misses = 5

        result = stats.to_dict()
        assert result['hits'] == 10
        assert result['misses'] == 5
        assert result['hit_ratio'] == 10 / 15


class TestLRUCacheWithTTLConstruction:
    """Test cache construction and validation."""

    def test_valid_capacity(self):
        """Test creation with valid capacity."""
        cache = LRUCacheWithTTL(10)
        assert cache.capacity() == 10
        assert cache.size() == 0

    def test_minimum_capacity(self):
        """Test creation with minimum capacity."""
        cache = LRUCacheWithTTL(1)
        assert cache.capacity() == 1

    def test_invalid_capacity_zero(self):
        """Test creation with zero capacity raises error."""
        with pytest.raises(ValueError, match="Capacity must be at least 1"):
            LRUCacheWithTTL(0)

    def test_invalid_capacity_negative(self):
        """Test creation with negative capacity raises error."""
        with pytest.raises(ValueError, match="Capacity must be at least 1"):
            LRUCacheWithTTL(-1)


class TestBasicOperations:
    """Test basic cache operations."""

    def test_put_and_get(self):
        """Test basic put and get operations."""
        cache = LRUCacheWithTTL(3)

        assert cache.put("key1", "value1") is True
        assert cache.get("key1") == "value1"
        assert cache.size() == 1

    def test_get_nonexistent_key(self):
        """Test getting non-existent key returns None."""
        cache = LRUCacheWithTTL(3)
        assert cache.get("nonexistent") is None

    def test_put_duplicate_key(self):
        """Test putting duplicate key updates value."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1")
        cache.put("key1", "value2")

        assert cache.get("key1") == "value2"
        assert cache.size() == 1

    def test_delete_existing_key(self):
        """Test deleting existing key."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1")
        assert cache.delete("key1") is True
        assert cache.get("key1") is None
        assert cache.size() == 0

    def test_delete_nonexistent_key(self):
        """Test deleting non-existent key."""
        cache = LRUCacheWithTTL(3)
        assert cache.delete("nonexistent") is False

    def test_clear(self):
        """Test clearing cache."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.clear()

        assert cache.size() == 0
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_contains_operator(self):
        """Test __contains__ operator."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1")
        assert "key1" in cache
        assert "nonexistent" not in cache

    def test_len_operator(self):
        """Test __len__ operator."""
        cache = LRUCacheWithTTL(3)

        assert len(cache) == 0
        cache.put("key1", "value1")
        assert len(cache) == 1

    def test_repr(self):
        """Test string representation."""
        cache = LRUCacheWithTTL(5)
        cache.put("key1", "value1")

        repr_str = repr(cache)
        assert "LRUCacheWithTTL" in repr_str
        assert "capacity=5" in repr_str
        assert "size=1" in repr_str


class TestLRUEviction:
    """Test LRU eviction policy."""

    def test_lru_eviction_on_capacity_exceeded(self):
        """Test LRU eviction when capacity is exceeded."""
        cache = LRUCacheWithTTL(2)

        cache.put("a", "value_a")
        cache.put("b", "value_b")
        cache.put("c", "value_c")  # Should evict 'a'

        assert cache.get("a") is None  # Evicted
        assert cache.get("b") == "value_b"
        assert cache.get("c") == "value_c"
        assert cache.size() == 2

    def test_lru_order_by_access(self):
        """Test LRU order is updated by access."""
        cache = LRUCacheWithTTL(2)

        cache.put("a", "value_a")
        cache.put("b", "value_b")

        # Access 'a' to make it recently used
        cache.get("a")

        # Add 'c', should evict 'b' (least recently used)
        cache.put("c", "value_c")

        assert cache.get("a") == "value_a"  # Still there
        assert cache.get("b") is None       # Evicted
        assert cache.get("c") == "value_c"

    def test_lru_order_by_update(self):
        """Test LRU order is updated by putting to existing key."""
        cache = LRUCacheWithTTL(2)

        cache.put("a", "value_a")
        cache.put("b", "value_b")

        # Update 'a' to make it recently used
        cache.put("a", "value_a_updated")

        # Add 'c', should evict 'b'
        cache.put("c", "value_c")

        assert cache.get("a") == "value_a_updated"
        assert cache.get("b") is None
        assert cache.get("c") == "value_c"

    def test_single_capacity_eviction(self):
        """Test eviction with capacity of 1."""
        cache = LRUCacheWithTTL(1)

        cache.put("a", "value_a")
        cache.put("b", "value_b")  # Should evict 'a'

        assert cache.get("a") is None
        assert cache.get("b") == "value_b"
        assert cache.size() == 1


class TestTTLExpiration:
    """Test TTL expiration functionality."""

    def test_put_with_ttl(self):
        """Test putting item with TTL."""
        cache = LRUCacheWithTTL(3)

        assert cache.put("key1", "value1", ttl_seconds=1) is True
        assert cache.get("key1") == "value1"

    def test_ttl_expiration(self):
        """Test item expires after TTL."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1", ttl_seconds=0.1)
        time.sleep(0.15)

        assert cache.get("key1") is None
        assert cache.size() == 0  # Expired item should be removed

    def test_ttl_not_expired(self):
        """Test item doesn't expire before TTL."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1", ttl_seconds=1)
        time.sleep(0.1)

        assert cache.get("key1") == "value1"

    def test_mixed_ttl_and_no_ttl(self):
        """Test mixing items with and without TTL."""
        cache = LRUCacheWithTTL(3)

        cache.put("permanent", "value1")  # No TTL
        cache.put("temporary", "value2", ttl_seconds=0.1)

        time.sleep(0.15)

        assert cache.get("permanent") == "value1"
        assert cache.get("temporary") is None

    def test_ttl_update_existing_key(self):
        """Test updating TTL for existing key."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1", ttl_seconds=10)
        cache.put("key1", "value2", ttl_seconds=0.1)

        time.sleep(0.15)
        assert cache.get("key1") is None

    def test_cleanup_expired(self):
        """Test manual cleanup of expired items."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1", ttl_seconds=0.1)
        cache.put("key2", "value2", ttl_seconds=0.1)
        cache.put("key3", "value3")  # No expiration

        time.sleep(0.15)

        # Items are expired but not yet cleaned up
        assert cache.size() == 3

        # Manual cleanup
        cleaned = cache.cleanup_expired()
        assert cleaned == 2
        assert cache.size() == 1
        assert cache.get("key3") == "value3"


class TestErrorHandling:
    """Test error handling and validation."""

    def test_unhashable_key(self):
        """Test error with unhashable key."""
        cache = LRUCacheWithTTL(3)

        with pytest.raises(TypeError, match="Cache keys must be hashable"):
            cache.put(["list", "key"], "value")

    def test_negative_ttl(self):
        """Test error with negative TTL."""
        cache = LRUCacheWithTTL(3)

        with pytest.raises(ValueError, match="TTL cannot be negative"):
            cache.put("key1", "value1", ttl_seconds=-1)

    def test_zero_ttl(self):
        """Test zero TTL (should be allowed)."""
        cache = LRUCacheWithTTL(3)

        # Zero TTL should expire immediately
        cache.put("key1", "value1", ttl_seconds=0)
        time.sleep(0.01)
        assert cache.get("key1") is None

    def test_various_key_types(self):
        """Test various hashable key types."""
        cache = LRUCacheWithTTL(10)

        # Test different hashable types
        test_keys = [
            "string_key",
            42,
            (1, 2, 3),
            frozenset([1, 2, 3]),
            True,
            None
        ]

        for key in test_keys:
            cache.put(key, f"value_for_{key}")
            assert cache.get(key) == f"value_for_{key}"


class TestThreadSafety:
    """Test thread safety of cache operations."""

    def test_concurrent_puts(self):
        """Test concurrent put operations."""
        cache = LRUCacheWithTTL(1000)

        def put_items(start, end):
            for i in range(start, end):
                cache.put(f"key_{i}", f"value_{i}")

        # Run concurrent puts
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(10):
                future = executor.submit(put_items, i * 10, (i + 1) * 10)
                futures.append(future)

            for future in futures:
                future.result()

        # Verify all items were stored
        assert cache.size() == 100
        for i in range(100):
            assert cache.get(f"key_{i}") == f"value_{i}"

    def test_concurrent_gets(self):
        """Test concurrent get operations."""
        cache = LRUCacheWithTTL(100)

        # Pre-populate cache
        for i in range(50):
            cache.put(f"key_{i}", f"value_{i}")

        results = []

        def get_items():
            local_results = []
            for i in range(50):
                result = cache.get(f"key_{i}")
                local_results.append(result)
            results.append(local_results)

        # Run concurrent gets
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(get_items) for _ in range(10)]
            for future in futures:
                future.result()

        # Verify all gets returned correct values
        for result_set in results:
            for i, value in enumerate(result_set):
                assert value == f"value_{i}"

    def test_concurrent_mixed_operations(self):
        """Test concurrent mixed operations."""
        cache = LRUCacheWithTTL(200)

        def mixed_operations(thread_id):
            for i in range(20):
                key = f"key_{thread_id}_{i}"
                cache.put(key, f"value_{thread_id}_{i}")
                assert cache.get(key) == f"value_{thread_id}_{i}"

                if i % 3 == 0:
                    cache.delete(key)

        # Run concurrent mixed operations
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(mixed_operations, i) for i in range(5)]
            for future in futures:
                future.result()

        # Cache should be in a consistent state
        assert cache.size() <= 200


class TestPerformance:
    """Test performance characteristics."""

    def test_get_performance(self):
        """Test get operation performance (should be O(1))."""
        cache = LRUCacheWithTTL(10000)

        # Populate cache
        for i in range(1000):
            cache.put(f"key_{i}", f"value_{i}")

        # Time multiple gets
        start_time = time.time()
        for _ in range(1000):
            cache.get("key_500")  # Get same key repeatedly
        end_time = time.time()

        # Should be very fast (less than 0.1 seconds for 1000 operations)
        assert end_time - start_time < 0.1

    def test_put_performance(self):
        """Test put operation performance (should be O(1))."""
        cache = LRUCacheWithTTL(10000)

        # Time multiple puts
        start_time = time.time()
        for i in range(1000):
            cache.put(f"perf_key_{i}", f"perf_value_{i}")
        end_time = time.time()

        # Should be very fast (less than 0.1 seconds for 1000 operations)
        assert end_time - start_time < 0.1


class TestStatistics:
    """Test cache statistics functionality."""

    def test_hit_miss_stats(self):
        """Test hit and miss statistics."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1")

        # Generate hits and misses
        cache.get("key1")  # Hit
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        cache.get("key3")  # Miss

        stats = cache.stats()
        assert stats['hits'] == 2
        assert stats['misses'] == 2
        assert stats['hit_ratio'] == 0.5

    def test_eviction_stats(self):
        """Test eviction statistics."""
        cache = LRUCacheWithTTL(2)

        cache.put("a", "value_a")
        cache.put("b", "value_b")
        cache.put("c", "value_c")  # Should cause eviction

        stats = cache.stats()
        assert stats['evictions'] == 1

    def test_expiration_stats(self):
        """Test expiration statistics."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1", ttl_seconds=0.1)
        time.sleep(0.15)
        cache.get("key1")  # Should register expiration

        stats = cache.stats()
        assert stats['expirations'] == 1

    def test_put_delete_stats(self):
        """Test put and delete statistics."""
        cache = LRUCacheWithTTL(3)

        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.delete("key1")

        stats = cache.stats()
        assert stats['puts'] == 2
        assert stats['deletes'] == 1


class TestUserStories:
    """Test implementation of user stories from specifications."""

    def test_basic_cache_operations_story(self):
        """Test US1: Basic Cache Operations."""
        cache = LRUCacheWithTTL(10)

        # Store a value with a key
        result = cache.put("user_123", {"name": "John", "role": "admin"})
        assert result is True

        # Retrieve a value by key
        user_data = cache.get("user_123")
        assert user_data == {"name": "John", "role": "admin"}

        # Handle cache miss gracefully
        missing_data = cache.get("user_999")
        assert missing_data is None

    def test_automatic_expiration_story(self):
        """Test US2: Automatic Expiration."""
        cache = LRUCacheWithTTL(10)

        # Set TTL when storing items
        cache.put("session_abc", "session_data", ttl_seconds=0.2)

        # Access before expiration
        data = cache.get("session_abc")
        assert data == "session_data"

        # Access after expiration (should return miss)
        time.sleep(0.25)
        expired_data = cache.get("session_abc")
        assert expired_data is None

        # Verify expired items are cleaned up
        assert cache.size() == 0

    def test_memory_management_story(self):
        """Test US3: Memory Management."""
        cache = LRUCacheWithTTL(2)  # Small capacity

        # Fill cache to capacity
        cache.put("item1", "data1")
        cache.put("item2", "data2")
        assert cache.size() == 2

        # Cache reaches maximum capacity
        cache.put("item3", "data3")  # Should evict item1

        # Least recently used items are evicted
        assert cache.get("item1") is None  # Evicted
        assert cache.get("item2") == "data2"
        assert cache.get("item3") == "data3"

        # Cache size remains within limits
        assert cache.size() == 2


class TestUseCases:
    """Test real-world use cases from specifications."""

    def test_web_session_cache_use_case(self):
        """Test UC1: Web Application Session Cache."""
        cache = LRUCacheWithTTL(1000)

        # User logs in, session data stored with 30-minute TTL
        session_data = {
            "user_id": 123,
            "username": "john_doe",
            "permissions": ["read", "write"]
        }
        cache.put("session_xyz789", session_data, ttl_seconds=0.2)  # Shortened for test

        # Subsequent requests retrieve session from cache
        retrieved_session = cache.get("session_xyz789")
        assert retrieved_session == session_data

        # Session automatically expires
        time.sleep(0.25)
        expired_session = cache.get("session_xyz789")
        assert expired_session is None

    def test_api_response_cache_use_case(self):
        """Test UC2: API Response Cache."""
        cache = LRUCacheWithTTL(500)

        # API response cached for 5 minutes
        api_response = {"data": [1, 2, 3], "status": "success"}
        cache.put("api:/users?page=1", api_response, ttl_seconds=0.1)

        # Subsequent identical requests served from cache
        cached_response = cache.get("api:/users?page=1")
        assert cached_response == api_response

        # Response expires and is refreshed
        time.sleep(0.15)
        expired_response = cache.get("api:/users?page=1")
        assert expired_response is None

    def test_database_query_cache_use_case(self):
        """Test UC3: Database Query Cache."""
        cache = LRUCacheWithTTL(100)

        # Expensive query result cached
        query_key = "SELECT * FROM users WHERE active=1"
        query_result = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        cache.put(query_key, query_result, ttl_seconds=0.1)

        # Identical queries served from cache
        cached_result = cache.get(query_key)
        assert cached_result == query_result

        # Cache manages space using LRU eviction
        # Fill cache to demonstrate LRU behavior
        for i in range(100):
            cache.put(f"query_{i}", f"result_{i}")

        # Original query should be evicted
        assert cache.get(query_key) is None


class TestConvenienceFunction:
    """Test the convenience create_cache function."""

    def test_create_cache_default(self):
        """Test create_cache with default capacity."""
        cache = create_cache()
        assert cache.capacity() == 128
        assert isinstance(cache, LRUCacheWithTTL)

    def test_create_cache_custom_capacity(self):
        """Test create_cache with custom capacity."""
        cache = create_cache(50)
        assert cache.capacity() == 50


# Integration tests
class TestIntegration:
    """Integration tests for complex scenarios."""

    def test_lru_and_ttl_interaction(self):
        """Test interaction between LRU eviction and TTL expiration."""
        cache = LRUCacheWithTTL(3)

        # Add items with different TTLs
        cache.put("short", "value1", ttl_seconds=0.1)    # Expires first
        cache.put("medium", "value2", ttl_seconds=0.2)   # Expires second
        cache.put("long", "value3", ttl_seconds=1.0)     # Long TTL

        # Cache is full, add another item to trigger LRU
        # But first, access "short" to make it recently used
        cache.get("short")

        # Add new item - should evict "medium" (least recently used)
        cache.put("new", "value4")

        # Verify "medium" was evicted, not expired items
        assert cache.get("short") == "value1"
        assert cache.get("medium") is None  # Evicted
        assert cache.get("long") == "value3"
        assert cache.get("new") == "value4"

        # Wait for "short" to expire
        time.sleep(0.15)
        assert cache.get("short") is None  # Expired

    def test_stress_test(self):
        """Stress test with many operations."""
        cache = LRUCacheWithTTL(100)

        # Add many items
        for i in range(200):  # More than capacity
            ttl = 0.5 if i % 2 == 0 else None  # Half with TTL
            cache.put(f"key_{i}", f"value_{i}", ttl_seconds=ttl)

        # Cache should maintain capacity
        assert cache.size() == 100

        # Access patterns should affect LRU order
        for i in range(150, 200):  # Access recent items
            cache.get(f"key_{i}")

        # Add more items to trigger more evictions
        for i in range(200, 220):
            cache.put(f"new_key_{i}", f"new_value_{i}")

        # Cache should still maintain capacity and consistency
        assert cache.size() == 100

        # Wait for TTL expirations
        time.sleep(0.6)

        # Access cache to trigger cleanup
        cache.cleanup_expired()

        # Some items should have expired
        stats = cache.stats()
        assert stats['expirations'] > 0


if __name__ == "__main__":
    # Run basic test suite
    pytest.main([__file__, "-v"])