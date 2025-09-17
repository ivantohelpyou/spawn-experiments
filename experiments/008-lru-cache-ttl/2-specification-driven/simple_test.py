#!/usr/bin/env python3
"""
Simple test runner for LRU Cache with TTL implementation.
Tests the core functionality without external dependencies.
"""

import time
import threading
from lru_cache_ttl import LRUCacheWithTTL, CacheStats, CacheNode


def test_basic_functionality():
    """Test basic cache operations."""
    print("Testing basic functionality...")

    cache = LRUCacheWithTTL(capacity=3)

    # Test put and get
    cache.put("key1", "value1")
    assert cache.get("key1") == "value1", "Basic get/put failed"

    # Test cache miss
    assert cache.get("nonexistent") is None, "Cache miss should return None"

    # Test size
    assert cache.size() == 1, "Size should be 1"
    assert not cache.is_empty(), "Cache should not be empty"

    print("✓ Basic functionality tests passed")


def test_lru_eviction():
    """Test LRU eviction policy."""
    print("Testing LRU eviction...")

    cache = LRUCacheWithTTL(capacity=2)

    # Fill to capacity
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    assert cache.size() == 2, "Size should be 2"

    # Add third item (should evict key1)
    cache.put("key3", "value3")
    assert cache.size() == 2, "Size should still be 2"
    assert cache.get("key1") is None, "key1 should be evicted"
    assert cache.get("key2") == "value2", "key2 should still exist"
    assert cache.get("key3") == "value3", "key3 should exist"

    print("✓ LRU eviction tests passed")


def test_ttl_expiration():
    """Test TTL expiration."""
    print("Testing TTL expiration...")

    cache = LRUCacheWithTTL(capacity=3, default_ttl=0.1)  # 100ms TTL

    cache.put("key1", "value1")
    assert cache.get("key1") == "value1", "Should get value before expiration"

    # Wait for expiration
    time.sleep(0.15)
    assert cache.get("key1") is None, "Should return None after expiration"
    assert cache.size() == 0, "Size should be 0 after expiration cleanup"

    print("✓ TTL expiration tests passed")


def test_custom_ttl():
    """Test custom TTL override."""
    print("Testing custom TTL...")

    cache = LRUCacheWithTTL(capacity=3, default_ttl=10.0)

    # Add item with custom short TTL
    cache.put("temp", "temporary", ttl=0.1)
    cache.put("permanent", "permanent", ttl=0)  # No expiration

    assert cache.get("temp") == "temporary", "Should get temp value"
    assert cache.get("permanent") == "permanent", "Should get permanent value"

    # Wait for custom TTL expiration
    time.sleep(0.15)
    assert cache.get("temp") is None, "Temp should expire"
    assert cache.get("permanent") == "permanent", "Permanent should remain"

    print("✓ Custom TTL tests passed")


def test_statistics():
    """Test statistics tracking."""
    print("Testing statistics...")

    cache = LRUCacheWithTTL(capacity=3)

    # Initial stats
    stats = cache.get_stats()
    assert stats.hits == 0, "Initial hits should be 0"
    assert stats.misses == 0, "Initial misses should be 0"

    # Generate some operations
    cache.put("key1", "value1")
    cache.get("key1")  # Hit
    cache.get("key2")  # Miss

    stats = cache.get_stats()
    assert stats.hits == 1, "Should have 1 hit"
    assert stats.misses == 1, "Should have 1 miss"
    assert stats.total_operations == 2, "Should have 2 total operations"
    assert stats.hit_rate() == 50.0, "Hit rate should be 50%"

    print("✓ Statistics tests passed")


def test_thread_safety():
    """Test basic thread safety."""
    print("Testing thread safety...")

    cache = LRUCacheWithTTL(capacity=50)
    results = []

    def worker():
        """Worker function for threading test."""
        for i in range(10):
            key = f"key_{threading.current_thread().ident}_{i}"
            value = f"value_{i}"
            cache.put(key, value)
            retrieved = cache.get(key)
            results.append(retrieved == value)

    # Run multiple threads
    threads = []
    for _ in range(3):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # All operations should succeed
    assert all(results), f"Some thread operations failed: {results.count(False)} failures"

    print("✓ Thread safety tests passed")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")

    # Test single capacity
    cache = LRUCacheWithTTL(capacity=1)
    cache.put("key1", "value1")
    cache.put("key2", "value2")  # Should evict key1
    assert cache.get("key1") is None, "key1 should be evicted"
    assert cache.get("key2") == "value2", "key2 should exist"

    # Test zero TTL (no expiration)
    cache = LRUCacheWithTTL(capacity=3, default_ttl=0)
    cache.put("permanent", "value")
    time.sleep(0.1)
    assert cache.get("permanent") == "value", "Should not expire with TTL=0"

    # Test invalid capacity
    try:
        LRUCacheWithTTL(capacity=0)
        assert False, "Should raise ValueError for invalid capacity"
    except ValueError:
        pass  # Expected

    print("✓ Edge case tests passed")


def test_advanced_features():
    """Test advanced features."""
    print("Testing advanced features...")

    cache = LRUCacheWithTTL(capacity=5, default_ttl=1.0)

    # Test delete
    cache.put("key1", "value1")
    assert cache.delete("key1") is True, "Should successfully delete existing key"
    assert cache.delete("nonexistent") is False, "Should fail to delete non-existent key"

    # Test clear
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.clear()
    assert cache.size() == 0, "Cache should be empty after clear"

    # Test cleanup_expired
    cache.put("temp1", "value1", ttl=0.1)
    cache.put("temp2", "value2", ttl=0.1)
    cache.put("permanent", "value3", ttl=0)

    time.sleep(0.15)
    expired_count = cache.cleanup_expired()
    assert expired_count == 2, "Should clean up 2 expired items"
    assert cache.size() == 1, "Should have 1 item remaining"

    # Test remaining TTL
    cache.put("test", "value", ttl=1.0)
    remaining = cache.get_remaining_ttl("test")
    assert 0.9 <= remaining <= 1.0, "Remaining TTL should be close to 1.0"
    assert cache.get_remaining_ttl("nonexistent") is None, "Should return None for non-existent key"

    # Test container operations
    cache.put("container_test", "value")
    assert "container_test" in cache, "Should find key using 'in' operator"
    assert len(cache) == cache.size(), "len() should match size()"

    print("✓ Advanced feature tests passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Running LRU Cache with TTL Tests")
    print("=" * 60)

    test_functions = [
        test_basic_functionality,
        test_lru_eviction,
        test_ttl_expiration,
        test_custom_ttl,
        test_statistics,
        test_thread_safety,
        test_edge_cases,
        test_advanced_features
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("🎉 All tests passed! Implementation is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)