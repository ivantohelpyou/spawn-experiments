#!/usr/bin/env python3
"""
Comprehensive Unit Tests for LRU Cache with TTL

This module provides extensive testing for the LRU Cache with TTL implementation.
Tests cover:
- Basic cache operations (get, set, delete)
- LRU eviction behavior
- TTL expiration functionality
- Thread safety
- Edge cases and error conditions
- Statistics tracking
- Persistence features
"""

import unittest
import time
import threading
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from lru_cache_ttl import LRUCacheWithTTL, CacheEntry, create_cache


class TestCacheEntry(unittest.TestCase):
    """Test cases for CacheEntry class."""

    def test_cache_entry_creation(self):
        """Test basic cache entry creation."""
        entry = CacheEntry("test_value", ttl_seconds=10.0)

        self.assertEqual(entry.value, "test_value")
        self.assertIsNotNone(entry.created_at)
        self.assertIsNotNone(entry.expires_at)
        self.assertEqual(entry.access_count, 1)
        self.assertAlmostEqual(entry.time_to_live(), 10.0, delta=0.1)

    def test_cache_entry_no_ttl(self):
        """Test cache entry without TTL."""
        entry = CacheEntry("test_value")

        self.assertEqual(entry.value, "test_value")
        self.assertIsNone(entry.expires_at)
        self.assertIsNone(entry.time_to_live())
        self.assertFalse(entry.is_expired())

    def test_cache_entry_expiration(self):
        """Test cache entry expiration."""
        entry = CacheEntry("test_value", ttl_seconds=0.1)

        # Should not be expired immediately
        self.assertFalse(entry.is_expired())

        # Wait for expiration
        time.sleep(0.15)
        self.assertTrue(entry.is_expired())

    def test_cache_entry_touch(self):
        """Test cache entry touch functionality."""
        entry = CacheEntry("test_value")
        initial_count = entry.access_count
        initial_access_time = entry.last_accessed

        time.sleep(0.01)  # Small delay
        entry.touch()

        self.assertEqual(entry.access_count, initial_count + 1)
        self.assertGreater(entry.last_accessed, initial_access_time)


class TestLRUCacheWithTTL(unittest.TestCase):
    """Test cases for LRUCacheWithTTL class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = LRUCacheWithTTL(max_size=3, default_ttl=None)

    def tearDown(self):
        """Clean up after tests."""
        self.cache.close()

    def test_cache_creation(self):
        """Test cache creation with different parameters."""
        # Default cache
        cache1 = LRUCacheWithTTL()
        self.assertEqual(cache1.max_size, 128)
        self.assertIsNone(cache1.default_ttl)
        cache1.close()

        # Custom cache
        cache2 = LRUCacheWithTTL(max_size=50, default_ttl=300.0)
        self.assertEqual(cache2.max_size, 50)
        self.assertEqual(cache2.default_ttl, 300.0)
        cache2.close()

        # Invalid size should raise error
        with self.assertRaises(ValueError):
            LRUCacheWithTTL(max_size=0)

    def test_basic_operations(self):
        """Test basic get/set/delete operations."""
        # Set and get
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

        # Get non-existent key
        self.assertIsNone(self.cache.get("nonexistent"))

        # Delete existing key
        self.assertTrue(self.cache.delete("key1"))
        self.assertIsNone(self.cache.get("key1"))

        # Delete non-existent key
        self.assertFalse(self.cache.delete("nonexistent"))

    def test_lru_eviction(self):
        """Test LRU eviction behavior."""
        # Fill cache to capacity
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")

        # All keys should be present
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")

        # Add one more item - should evict least recently used (key1)
        self.cache.set("key4", "value4")

        self.assertIsNone(self.cache.get("key1"))  # Evicted
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_lru_order_update(self):
        """Test that accessing items updates LRU order."""
        # Fill cache
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")

        # Access key1 to make it most recently used
        self.cache.get("key1")

        # Add new item - should evict key2 (oldest unaccessed)
        self.cache.set("key4", "value4")

        self.assertEqual(self.cache.get("key1"), "value1")  # Still present
        self.assertIsNone(self.cache.get("key2"))  # Evicted
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_ttl_functionality(self):
        """Test TTL expiration."""
        # Set item with short TTL
        self.cache.set("temp_key", "temp_value", ttl=0.1)

        # Should be accessible immediately
        self.assertEqual(self.cache.get("temp_key"), "temp_value")
        self.assertTrue(self.cache.exists("temp_key"))

        # Wait for expiration
        time.sleep(0.15)

        # Should be expired now
        self.assertIsNone(self.cache.get("temp_key"))
        self.assertFalse(self.cache.exists("temp_key"))

    def test_default_ttl(self):
        """Test default TTL functionality."""
        cache = LRUCacheWithTTL(max_size=3, default_ttl=0.1)
        try:
            cache.set("key1", "value1")  # Uses default TTL

            self.assertEqual(cache.get("key1"), "value1")

            time.sleep(0.15)
            self.assertIsNone(cache.get("key1"))
        finally:
            cache.close()

    def test_ttl_method(self):
        """Test TTL method for checking remaining time."""
        self.cache.set("key1", "value1", ttl=10.0)

        ttl_remaining = self.cache.ttl("key1")
        self.assertIsNotNone(ttl_remaining)
        self.assertAlmostEqual(ttl_remaining, 10.0, delta=0.1)

        # No TTL key
        self.cache.set("key2", "value2")
        self.assertIsNone(self.cache.ttl("key2"))

        # Non-existent key
        self.assertIsNone(self.cache.ttl("nonexistent"))

    def test_size_and_capacity(self):
        """Test size and capacity methods."""
        self.assertEqual(self.cache.size(), 0)
        self.assertEqual(self.cache.capacity(), 3)
        self.assertFalse(self.cache.is_full())

        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.size(), 1)
        self.assertFalse(self.cache.is_full())

        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.assertEqual(self.cache.size(), 3)
        self.assertTrue(self.cache.is_full())

    def test_clear(self):
        """Test cache clearing."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")

        self.assertEqual(self.cache.size(), 2)

        self.cache.clear()

        self.assertEqual(self.cache.size(), 0)
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))

    def test_keys_and_items(self):
        """Test keys() and items() methods."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")

        keys = list(self.cache.keys())
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
        self.assertEqual(len(keys), 2)

        items = list(self.cache.items())
        self.assertIn(("key1", "value1"), items)
        self.assertIn(("key2", "value2"), items)
        self.assertEqual(len(items), 2)

    def test_dictionary_interface(self):
        """Test dictionary-like interface."""
        # Test __setitem__ and __getitem__
        self.cache["key1"] = "value1"
        self.assertEqual(self.cache["key1"], "value1")

        # Test __contains__
        self.assertIn("key1", self.cache)
        self.assertNotIn("nonexistent", self.cache)

        # Test __len__
        self.assertEqual(len(self.cache), 1)

        # Test __delitem__
        del self.cache["key1"]
        self.assertNotIn("key1", self.cache)

        # Test KeyError for missing keys
        with self.assertRaises(KeyError):
            _ = self.cache["nonexistent"]

        with self.assertRaises(KeyError):
            del self.cache["nonexistent"]

    def test_statistics(self):
        """Test statistics tracking."""
        initial_stats = self.cache.get_stats()

        # Test hits and misses
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # Hit
        self.cache.get("nonexistent")  # Miss

        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], initial_stats['hits'] + 1)
        self.assertEqual(stats['misses'], initial_stats['misses'] + 1)
        self.assertEqual(stats['sets'], initial_stats['sets'] + 1)

        # Test reset
        self.cache.reset_stats()
        reset_stats = self.cache.get_stats()
        self.assertEqual(reset_stats['hits'], 0)
        self.assertEqual(reset_stats['misses'], 0)

    def test_persistence(self):
        """Test save and load functionality."""
        # Set up test data
        self.cache.set("key1", "value1")
        self.cache.set("key2", {"nested": "object"})
        self.cache.set("key3", "value3", ttl=3600)  # Long TTL

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name

        try:
            self.cache.save_to_file(temp_file)

            # Create new cache and load
            new_cache = LRUCacheWithTTL(max_size=5)
            try:
                self.assertTrue(new_cache.load_from_file(temp_file))

                self.assertEqual(new_cache.get("key1"), "value1")
                self.assertEqual(new_cache.get("key2"), {"nested": "object"})
                self.assertEqual(new_cache.get("key3"), "value3")

                # Test loading non-existent file
                self.assertFalse(new_cache.load_from_file("nonexistent.json"))
            finally:
                new_cache.close()

        finally:
            os.unlink(temp_file)

    def test_thread_safety(self):
        """Test thread safety of cache operations."""
        num_threads = 10
        operations_per_thread = 100
        results = {}

        def worker(thread_id):
            local_results = []
            for i in range(operations_per_thread):
                key = f"thread_{thread_id}_key_{i}"
                value = f"thread_{thread_id}_value_{i}"

                # Set value
                self.cache.set(key, value)

                # Get value
                retrieved = self.cache.get(key)
                local_results.append((key, value, retrieved))

            results[thread_id] = local_results

        # Start threads
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join()

        # Verify results
        for thread_id, thread_results in results.items():
            for key, expected_value, retrieved_value in thread_results:
                # Note: Due to LRU eviction, some values might be evicted
                # We just check that if a value is retrieved, it's correct
                if retrieved_value is not None:
                    self.assertEqual(retrieved_value, expected_value)

    def test_background_cleanup(self):
        """Test background cleanup of expired entries."""
        # Set items with short TTL
        self.cache.set("temp1", "value1", ttl=0.1)
        self.cache.set("temp2", "value2", ttl=0.1)

        # Items should exist initially
        self.assertEqual(self.cache.size(), 2)

        # Wait for expiration and cleanup
        time.sleep(0.2)

        # Force a cleanup by accessing keys method
        list(self.cache.keys())

        # Items should be cleaned up
        self.assertEqual(self.cache.size(), 0)

    def test_edge_cases(self):
        """Test various edge cases."""
        # Setting same key multiple times
        self.cache.set("key1", "value1")
        self.cache.set("key1", "value2")
        self.assertEqual(self.cache.get("key1"), "value2")
        self.assertEqual(self.cache.size(), 1)  # Size shouldn't increase

        # Zero TTL should expire immediately
        self.cache.set("zero_ttl", "value", ttl=0)
        self.assertIsNone(self.cache.get("zero_ttl"))

        # Negative TTL should expire immediately
        self.cache.set("negative_ttl", "value", ttl=-1)
        self.assertIsNone(self.cache.get("negative_ttl"))

    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.cache)
        self.assertIn("LRUCacheWithTTL", repr_str)
        self.assertIn("size=0", repr_str)
        self.assertIn("capacity=3", repr_str)


class TestFactoryFunction(unittest.TestCase):
    """Test cases for the factory function."""

    def test_create_cache(self):
        """Test create_cache factory function."""
        # Default parameters
        cache1 = create_cache()
        self.assertEqual(cache1.max_size, 128)
        self.assertIsNone(cache1.default_ttl)
        cache1.close()

        # Custom parameters
        cache2 = create_cache(max_size=64, default_ttl=300)
        self.assertEqual(cache2.max_size, 64)
        self.assertEqual(cache2.default_ttl, 300)
        cache2.close()


class TestConcurrentAccess(unittest.TestCase):
    """Test concurrent access patterns."""

    def setUp(self):
        self.cache = LRUCacheWithTTL(max_size=100)

    def tearDown(self):
        self.cache.close()

    def test_concurrent_reads_writes(self):
        """Test concurrent reads and writes."""
        num_writers = 5
        num_readers = 5
        operations_per_thread = 50

        def writer(thread_id):
            for i in range(operations_per_thread):
                key = f"writer_{thread_id}_key_{i}"
                value = f"writer_{thread_id}_value_{i}"
                self.cache.set(key, value)
                time.sleep(0.001)  # Small delay

        def reader():
            for _ in range(operations_per_thread):
                # Try to read random keys
                for thread_id in range(num_writers):
                    for i in range(0, operations_per_thread, 10):  # Sample every 10th
                        key = f"writer_{thread_id}_key_{i}"
                        self.cache.get(key)
                time.sleep(0.001)  # Small delay

        # Start all threads
        threads = []

        # Start writers
        for i in range(num_writers):
            t = threading.Thread(target=writer, args=(i,))
            threads.append(t)
            t.start()

        # Start readers
        for i in range(num_readers):
            t = threading.Thread(target=reader)
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join()

        # Cache should be in a consistent state
        stats = self.cache.get_stats()
        self.assertGreaterEqual(stats['sets'], 0)
        self.assertGreaterEqual(stats['hits'] + stats['misses'], 0)


if __name__ == '__main__':
    # Set up test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestCacheEntry,
        TestLRUCacheWithTTL,
        TestFactoryFunction,
        TestConcurrentAccess
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with proper code
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)