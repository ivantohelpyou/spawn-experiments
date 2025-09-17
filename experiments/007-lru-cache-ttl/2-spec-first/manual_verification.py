#!/usr/bin/env python3
"""
Manual verification of LRU Cache with TTL implementation.
This script tests key functionality without requiring pytest.
"""

import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from lru_cache_ttl import LRUCacheWithTTL, create_cache


def test_basic_functionality():
    """Test basic put/get/delete operations."""
    print("=== Testing Basic Functionality ===")

    cache = LRUCacheWithTTL(5)

    # Test basic put/get
    assert cache.put("key1", "value1") == True
    assert cache.get("key1") == "value1"
    assert cache.size() == 1

    # Test missing key
    assert cache.get("missing") is None

    # Test delete
    assert cache.delete("key1") == True
    assert cache.get("key1") is None
    assert cache.size() == 0

    print("✅ Basic functionality tests passed")


def test_lru_eviction():
    """Test LRU eviction policy."""
    print("\n=== Testing LRU Eviction ===")

    cache = LRUCacheWithTTL(3)

    # Fill cache
    cache.put("a", "value_a")
    cache.put("b", "value_b")
    cache.put("c", "value_c")

    # Access 'a' to make it recently used
    cache.get("a")

    # Add 'd' - should evict 'b' (least recently used)
    cache.put("d", "value_d")

    assert cache.get("a") == "value_a"  # Still there
    assert cache.get("b") is None       # Evicted
    assert cache.get("c") == "value_c"  # Still there
    assert cache.get("d") == "value_d"  # New item
    assert cache.size() == 3

    print("✅ LRU eviction tests passed")


def test_ttl_expiration():
    """Test TTL expiration functionality."""
    print("\n=== Testing TTL Expiration ===")

    cache = LRUCacheWithTTL(5)

    # Test item with TTL
    cache.put("temp", "temporary_value", ttl_seconds=0.2)
    assert cache.get("temp") == "temporary_value"

    # Wait for expiration
    time.sleep(0.25)
    assert cache.get("temp") is None
    assert cache.size() == 0  # Expired item cleaned up

    # Test mixed TTL and permanent items
    cache.put("permanent", "permanent_value")
    cache.put("temp", "temp_value", ttl_seconds=0.1)

    time.sleep(0.15)
    assert cache.get("permanent") == "permanent_value"
    assert cache.get("temp") is None
    assert cache.size() == 1

    print("✅ TTL expiration tests passed")


def test_thread_safety():
    """Test thread safety with concurrent operations."""
    print("\n=== Testing Thread Safety ===")

    cache = LRUCacheWithTTL(1000)
    results = []

    def worker(thread_id):
        """Worker function for concurrent testing."""
        local_results = []
        for i in range(100):
            key = f"thread_{thread_id}_key_{i}"
            value = f"thread_{thread_id}_value_{i}"

            # Put and get
            cache.put(key, value)
            retrieved = cache.get(key)
            local_results.append(retrieved == value)

        results.append(all(local_results))

    # Run concurrent operations
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(worker, i) for i in range(5)]
        for future in futures:
            future.result()

    # All workers should have succeeded
    assert all(results)
    assert cache.size() <= 1000  # Should not exceed capacity

    print("✅ Thread safety tests passed")


def test_error_handling():
    """Test error handling and validation."""
    print("\n=== Testing Error Handling ===")

    # Test invalid capacity
    try:
        LRUCacheWithTTL(0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Capacity must be at least 1" in str(e)

    cache = LRUCacheWithTTL(5)

    # Test unhashable key
    try:
        cache.put([1, 2, 3], "value")  # List is not hashable
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert "hashable" in str(e)

    # Test negative TTL
    try:
        cache.put("key", "value", ttl_seconds=-1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "TTL cannot be negative" in str(e)

    print("✅ Error handling tests passed")


def test_statistics():
    """Test statistics functionality."""
    print("\n=== Testing Statistics ===")

    cache = LRUCacheWithTTL(3)

    # Generate some activity
    cache.put("key1", "value1")
    cache.put("key2", "value2", ttl_seconds=0.1)

    cache.get("key1")  # Hit
    cache.get("key1")  # Hit
    cache.get("missing")  # Miss

    # Trigger eviction
    cache.put("key3", "value3")
    cache.put("key4", "value4")  # Should evict key2 or cause expiration

    # Wait for expiration
    time.sleep(0.15)
    cache.get("key2")  # Should be expired

    stats = cache.stats()

    assert stats['hits'] >= 2
    assert stats['misses'] >= 1
    assert stats['puts'] >= 4
    assert 'hit_ratio' in stats

    print("✅ Statistics tests passed")


def test_user_scenarios():
    """Test real-world user scenarios."""
    print("\n=== Testing User Scenarios ===")

    # Web session cache scenario
    session_cache = LRUCacheWithTTL(1000)

    session_data = {
        "user_id": 123,
        "username": "john_doe",
        "permissions": ["read", "write"]
    }

    # Store session with TTL
    session_cache.put("session_abc123", session_data, ttl_seconds=0.2)

    # Retrieve session
    retrieved = session_cache.get("session_abc123")
    assert retrieved == session_data

    # Session expires
    time.sleep(0.25)
    expired = session_cache.get("session_abc123")
    assert expired is None

    # API cache scenario
    api_cache = LRUCacheWithTTL(500)

    response_data = {"users": [{"id": 1, "name": "Alice"}], "total": 1}
    api_cache.put("GET:/api/users?page=1", response_data, ttl_seconds=0.1)

    # Cache hit
    cached_response = api_cache.get("GET:/api/users?page=1")
    assert cached_response == response_data

    # Cache expires
    time.sleep(0.15)
    expired_response = api_cache.get("GET:/api/users?page=1")
    assert expired_response is None

    print("✅ User scenario tests passed")


def test_convenience_function():
    """Test the convenience create_cache function."""
    print("\n=== Testing Convenience Function ===")

    # Default capacity
    cache1 = create_cache()
    assert cache1.capacity() == 128

    # Custom capacity
    cache2 = create_cache(50)
    assert cache2.capacity() == 50

    # Verify it works
    cache2.put("test", "value")
    assert cache2.get("test") == "value"

    print("✅ Convenience function tests passed")


def main():
    """Run all verification tests."""
    print("Running manual verification of LRU Cache with TTL implementation...")
    print("=" * 60)

    try:
        test_basic_functionality()
        test_lru_eviction()
        test_ttl_expiration()
        test_thread_safety()
        test_error_handling()
        test_statistics()
        test_user_scenarios()
        test_convenience_function()

        print("\n" + "=" * 60)
        print("🎉 ALL VERIFICATION TESTS PASSED! 🎉")
        print("The LRU Cache with TTL implementation is working correctly.")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)