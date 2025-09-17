import unittest
import time
from lru_cache_ttl import LRUCacheWithTTL


class TestLRUCacheWithTTL(unittest.TestCase):

    def test_constructor_creates_cache_with_capacity(self):
        """Test that cache can be created with specified capacity"""
        cache = LRUCacheWithTTL(capacity=5)
        self.assertEqual(cache.capacity(), 5)
        self.assertEqual(cache.size(), 0)

    def test_put_and_get_single_item(self):
        """Test basic put and get operations with single item"""
        cache = LRUCacheWithTTL(capacity=5)
        cache.put("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.size(), 1)

    def test_get_nonexistent_key_returns_none(self):
        """Test that getting a non-existent key returns None"""
        cache = LRUCacheWithTTL(capacity=5)
        self.assertIsNone(cache.get("nonexistent"))

    def test_lru_eviction_when_capacity_exceeded(self):
        """Test that least recently used item is evicted when capacity is exceeded"""
        cache = LRUCacheWithTTL(capacity=2)

        # Fill cache to capacity
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        self.assertEqual(cache.size(), 2)

        # Add third item - should evict key1 (least recently used)
        cache.put("key3", "value3")
        self.assertEqual(cache.size(), 2)
        self.assertIsNone(cache.get("key1"))  # key1 should be evicted
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")

    def test_lru_updates_on_get(self):
        """Test that getting an item updates its position in LRU order"""
        cache = LRUCacheWithTTL(capacity=2)

        cache.put("key1", "value1")
        cache.put("key2", "value2")

        # Access key1 to make it recently used
        cache.get("key1")

        # Add third item - should now evict key2 (least recently used)
        cache.put("key3", "value3")
        self.assertEqual(cache.size(), 2)
        self.assertEqual(cache.get("key1"), "value1")  # key1 should still exist
        self.assertIsNone(cache.get("key2"))  # key2 should be evicted
        self.assertEqual(cache.get("key3"), "value3")


if __name__ == '__main__':
    unittest.main()