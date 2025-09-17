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

    def test_put_with_ttl(self):
        """Test storing items with TTL"""
        cache = LRUCacheWithTTL(capacity=5)
        cache.put("key1", "value1", ttl=1.0)  # 1 second TTL
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.size(), 1)

    def test_ttl_expiration(self):
        """Test that items expire after TTL seconds"""
        cache = LRUCacheWithTTL(capacity=5)
        cache.put("key1", "value1", ttl=0.1)  # 0.1 second TTL

        # Item should exist immediately
        self.assertEqual(cache.get("key1"), "value1")

        # Wait for expiration
        time.sleep(0.2)

        # Item should be expired and return None
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.size(), 0)  # Should be removed from cache

    def test_ttl_with_default_ttl(self):
        """Test using default TTL from constructor"""
        cache = LRUCacheWithTTL(capacity=5, default_ttl=0.1)
        cache.put("key1", "value1")  # Should use default TTL

        self.assertEqual(cache.get("key1"), "value1")
        time.sleep(0.2)
        self.assertIsNone(cache.get("key1"))

    def test_delete_existing_key(self):
        """Test deleting an existing key"""
        cache = LRUCacheWithTTL(capacity=5)
        cache.put("key1", "value1")
        cache.put("key2", "value2")

        self.assertTrue(cache.delete("key1"))
        self.assertEqual(cache.size(), 1)
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")

    def test_delete_nonexistent_key(self):
        """Test deleting a non-existent key returns False"""
        cache = LRUCacheWithTTL(capacity=5)
        self.assertFalse(cache.delete("nonexistent"))

    def test_clear_cache(self):
        """Test clearing all cache contents"""
        cache = LRUCacheWithTTL(capacity=5)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")

        self.assertEqual(cache.size(), 3)
        cache.clear()
        self.assertEqual(cache.size(), 0)
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))
        self.assertIsNone(cache.get("key3"))

    def test_invalid_capacity_raises_error(self):
        """Test that invalid capacity values raise ValueError"""
        with self.assertRaises(ValueError):
            LRUCacheWithTTL(capacity=0)

        with self.assertRaises(ValueError):
            LRUCacheWithTTL(capacity=-1)

    def test_invalid_ttl_raises_error(self):
        """Test that negative TTL values raise ValueError"""
        cache = LRUCacheWithTTL(capacity=5)

        with self.assertRaises(ValueError):
            cache.put("key1", "value1", ttl=-1)

    def test_invalid_key_types_raise_error(self):
        """Test that non-string keys raise TypeError"""
        cache = LRUCacheWithTTL(capacity=5)

        with self.assertRaises(TypeError):
            cache.put(123, "value1")

        with self.assertRaises(TypeError):
            cache.get(123)

        with self.assertRaises(TypeError):
            cache.delete(123)

    def test_empty_string_key_raises_error(self):
        """Test that empty string keys raise ValueError"""
        cache = LRUCacheWithTTL(capacity=5)

        with self.assertRaises(ValueError):
            cache.put("", "value1")

        with self.assertRaises(ValueError):
            cache.get("")

        with self.assertRaises(ValueError):
            cache.delete("")


if __name__ == '__main__':
    unittest.main()