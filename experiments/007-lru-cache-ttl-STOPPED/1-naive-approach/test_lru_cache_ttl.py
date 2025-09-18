#!/usr/bin/env python3
"""
Unit Tests for LRU Cache with TTL

Comprehensive test suite covering all functionality of the LRU Cache with TTL
implementation, including edge cases, error conditions, and performance characteristics.
"""

import unittest
import time
from lru_cache_ttl import LRUCacheWithTTL, Node


class TestNode(unittest.TestCase):
    """Test cases for the Node class."""

    def test_node_creation(self):
        """Test basic node creation."""
        expires_at = time.time() + 10
        node = Node("key1", "value1", expires_at)

        self.assertEqual(node.key, "key1")
        self.assertEqual(node.value, "value1")
        self.assertEqual(node.expires_at, expires_at)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)


class TestLRUCacheWithTTL(unittest.TestCase):
    """Test cases for the LRU Cache with TTL."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.cache = LRUCacheWithTTL(3)

    def test_cache_initialization(self):
        """Test cache initialization."""
        cache = LRUCacheWithTTL(5)
        self.assertEqual(cache.capacity, 5)
        self.assertEqual(len(cache.cache), 0)
        self.assertEqual(cache.size(), 0)

        # Test dummy nodes are properly connected
        self.assertEqual(cache.head.next, cache.tail)
        self.assertEqual(cache.tail.prev, cache.head)

    def test_invalid_capacity(self):
        """Test error handling for invalid capacity."""
        with self.assertRaises(ValueError):
            LRUCacheWithTTL(0)

        with self.assertRaises(ValueError):
            LRUCacheWithTTL(-1)

    def test_basic_put_get(self):
        """Test basic put and get operations."""
        # Test put and get
        self.cache.put("key1", "value1", 10.0)
        self.assertEqual(self.cache.get("key1"), "value1")

        # Test non-existent key
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_invalid_ttl(self):
        """Test error handling for invalid TTL values."""
        with self.assertRaises(ValueError):
            self.cache.put("key", "value", 0)

        with self.assertRaises(ValueError):
            self.cache.put("key", "value", -1)

    def test_key_update(self):
        """Test updating an existing key."""
        self.cache.put("key1", "value1", 10.0)
        self.cache.put("key1", "updated_value", 15.0)

        self.assertEqual(self.cache.get("key1"), "updated_value")
        self.assertEqual(self.cache.size(), 1)

    def test_capacity_limit_lru_eviction(self):
        """Test LRU eviction when capacity is exceeded."""
        # Fill cache to capacity
        self.cache.put("key1", "value1", 10.0)
        self.cache.put("key2", "value2", 10.0)
        self.cache.put("key3", "value3", 10.0)
        self.assertEqual(self.cache.size(), 3)

        # Access key1 to make it most recently used
        self.cache.get("key1")

        # Add 4th item - should evict key2 (LRU)
        self.cache.put("key4", "value4", 10.0)
        self.assertEqual(self.cache.size(), 3)

        # key2 should be evicted, others should remain
        self.assertIsNone(self.cache.get("key2"))
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_ttl_expiration(self):
        """Test TTL expiration functionality."""
        # Add item with short TTL
        self.cache.put("short", "expires_soon", 0.1)
        self.assertEqual(self.cache.get("short"), "expires_soon")

        # Wait for expiration
        time.sleep(0.2)

        # Item should be expired and removed
        self.assertIsNone(self.cache.get("short"))
        self.assertEqual(self.cache.size(), 0)

    def test_ttl_cleanup_on_operations(self):
        """Test that expired items are cleaned up during operations."""
        # Add items with different TTLs
        self.cache.put("short1", "value1", 0.1)
        self.cache.put("short2", "value2", 0.1)
        self.cache.put("long", "value3", 10.0)

        self.assertEqual(self.cache.size(), 3)

        # Wait for short TTL items to expire
        time.sleep(0.2)

        # Access long-lived item - should trigger cleanup
        self.assertEqual(self.cache.get("long"), "value3")
        self.assertEqual(self.cache.size(), 1)

    def test_size_method(self):
        """Test size method accuracy."""
        self.assertEqual(self.cache.size(), 0)

        self.cache.put("key1", "value1", 10.0)
        self.assertEqual(self.cache.size(), 1)

        self.cache.put("key2", "value2", 10.0)
        self.assertEqual(self.cache.size(), 2)

        self.cache.put("key1", "updated", 10.0)  # Update existing
        self.assertEqual(self.cache.size(), 2)

    def test_clear_method(self):
        """Test cache clearing."""
        # Add some items
        self.cache.put("key1", "value1", 10.0)
        self.cache.put("key2", "value2", 10.0)
        self.assertEqual(self.cache.size(), 2)

        # Clear cache
        self.cache.clear()
        self.assertEqual(self.cache.size(), 0)
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))

    def test_keys_method(self):
        """Test keys method."""
        # Empty cache
        self.assertEqual(self.cache.keys(), [])

        # Add items
        self.cache.put("key1", "value1", 10.0)
        self.cache.put("key2", "value2", 10.0)

        keys = self.cache.keys()
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
        self.assertEqual(len(keys), 2)

        # Test with expired items
        self.cache.put("short", "expires", 0.1)
        time.sleep(0.2)

        keys = self.cache.keys()
        self.assertNotIn("short", keys)

    def test_items_method(self):
        """Test items method."""
        # Empty cache
        self.assertEqual(self.cache.items(), [])

        # Add items
        self.cache.put("key1", "value1", 10.0)
        self.cache.put("key2", "value2", 10.0)

        items = self.cache.items()
        self.assertIn(("key1", "value1"), items)
        self.assertIn(("key2", "value2"), items)
        self.assertEqual(len(items), 2)

    def test_magic_methods(self):
        """Test magic methods (__len__, __contains__, __str__)."""
        # Test __len__
        self.assertEqual(len(self.cache), 0)
        self.cache.put("key1", "value1", 10.0)
        self.assertEqual(len(self.cache), 1)

        # Test __contains__
        self.assertTrue("key1" in self.cache)
        self.assertFalse("nonexistent" in self.cache)

        # Test with expired item
        self.cache.put("short", "expires", 0.1)
        time.sleep(0.2)
        self.assertFalse("short" in self.cache)

        # Test __str__
        str_repr = str(self.cache)
        self.assertIn("LRUCacheWithTTL", str_repr)
        self.assertIn("capacity=3", str_repr)

    def test_lru_ordering(self):
        """Test that LRU ordering is maintained correctly."""
        # Fill cache
        self.cache.put("first", 1, 10.0)
        self.cache.put("second", 2, 10.0)
        self.cache.put("third", 3, 10.0)

        # Access first item to make it most recent
        self.cache.get("first")

        # Access second item to make it most recent
        self.cache.get("second")

        # Add new item - should evict "third" (least recently used)
        self.cache.put("fourth", 4, 10.0)

        # Check that third was evicted
        self.assertIsNone(self.cache.get("third"))
        self.assertEqual(self.cache.get("first"), 1)
        self.assertEqual(self.cache.get("second"), 2)
        self.assertEqual(self.cache.get("fourth"), 4)

    def test_mixed_data_types(self):
        """Test cache with mixed data types."""
        # Test different value types
        self.cache.put("string", "hello", 10.0)
        self.cache.put("int", 42, 10.0)
        self.cache.put("float", 3.14, 10.0)

        self.assertEqual(self.cache.get("string"), "hello")
        self.assertEqual(self.cache.get("int"), 42)
        self.assertEqual(self.cache.get("float"), 3.14)

        # Test different key types
        cache = LRUCacheWithTTL(5)
        cache.put(1, "one", 10.0)
        cache.put("two", 2, 10.0)
        cache.put((3, 3), "tuple_key", 10.0)

        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get("two"), 2)
        self.assertEqual(cache.get((3, 3)), "tuple_key")

    def test_concurrent_expiration_and_access(self):
        """Test behavior when items expire during access patterns."""
        # Add items with staggered expiration times
        self.cache.put("expires_first", "value1", 0.1)
        time.sleep(0.05)
        self.cache.put("expires_second", "value2", 0.1)
        time.sleep(0.05)
        self.cache.put("expires_third", "value3", 0.1)

        # At this point, first item should be about to expire
        time.sleep(0.05)  # Total sleep: 0.15s

        # First item should be expired
        self.assertIsNone(self.cache.get("expires_first"))

        # Others might still be valid depending on timing
        # Just check that cache handles this gracefully
        self.cache.get("expires_second")
        self.cache.get("expires_third")

    def test_edge_case_single_capacity(self):
        """Test cache with capacity of 1."""
        cache = LRUCacheWithTTL(1)

        cache.put("first", "value1", 10.0)
        self.assertEqual(cache.get("first"), "value1")

        # Adding second item should evict first
        cache.put("second", "value2", 10.0)
        self.assertIsNone(cache.get("first"))
        self.assertEqual(cache.get("second"), "value2")

    def test_large_capacity(self):
        """Test cache with large capacity."""
        cache = LRUCacheWithTTL(1000)

        # Add many items
        for i in range(1000):
            cache.put(f"key_{i}", f"value_{i}", 10.0)

        self.assertEqual(cache.size(), 1000)

        # Verify all items are accessible
        for i in range(0, 1000, 100):  # Sample every 100th item
            self.assertEqual(cache.get(f"key_{i}"), f"value_{i}")

    def test_performance_characteristics(self):
        """Test that operations are reasonably fast (O(1) behavior)."""
        cache = LRUCacheWithTTL(1000)

        # Time put operations
        start_time = time.time()
        for i in range(1000):
            cache.put(f"key_{i}", f"value_{i}", 60.0)
        put_time = time.time() - start_time

        # Time get operations
        start_time = time.time()
        for i in range(1000):
            cache.get(f"key_{i}")
        get_time = time.time() - start_time

        # Operations should be fast (this is a rough test)
        self.assertLess(put_time, 1.0, "Put operations took too long")
        self.assertLess(get_time, 1.0, "Get operations took too long")


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple features."""

    def test_complex_scenario(self):
        """Test complex scenario with mixed operations."""
        cache = LRUCacheWithTTL(3)

        # Add items with different TTLs
        cache.put("session_1", "user_data_1", 1.0)
        cache.put("session_2", "user_data_2", 2.0)
        cache.put("config", "app_settings", 10.0)

        # Access items to change LRU order
        cache.get("session_1")
        cache.get("config")

        # Wait for first session to expire
        time.sleep(1.1)

        # Add new item - should not evict anything due to expiration
        cache.put("session_3", "user_data_3", 5.0)

        # Check state
        self.assertIsNone(cache.get("session_1"))  # Expired
        self.assertEqual(cache.get("session_2"), "user_data_2")
        self.assertEqual(cache.get("config"), "app_settings")
        self.assertEqual(cache.get("session_3"), "user_data_3")

        # Wait for second session to expire
        time.sleep(1.5)

        # Check final state
        self.assertIsNone(cache.get("session_2"))  # Expired
        self.assertEqual(cache.get("config"), "app_settings")
        self.assertEqual(cache.get("session_3"), "user_data_3")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNode))
    suite.addTests(loader.loadTestsFromTestCase(TestLRUCacheWithTTL))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("Running comprehensive test suite for LRU Cache with TTL...")
    print("=" * 70)

    result = run_tests()

    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print("\\nAll tests passed! 🎉")
    else:
        print("\\nSome tests failed. 😞")