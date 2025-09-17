import unittest
import time
from lru_cache_ttl import LRUCacheWithTTL


class TestLRUCacheWithTTL(unittest.TestCase):

    def test_cache_can_be_created_with_default_capacity(self):
        """Test that cache can be instantiated with default capacity"""
        cache = LRUCacheWithTTL()
        self.assertEqual(cache.capacity(), 100)

    def test_cache_can_be_created_with_custom_capacity(self):
        """Test that cache can be instantiated with custom capacity"""
        cache = LRUCacheWithTTL(50)
        self.assertEqual(cache.capacity(), 50)

    def test_cache_initial_size_is_zero(self):
        """Test that new cache has size 0"""
        cache = LRUCacheWithTTL()
        self.assertEqual(cache.size(), 0)

    def test_put_and_get_single_item(self):
        """Test storing and retrieving a single item"""
        cache = LRUCacheWithTTL()
        cache.put("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.size(), 1)

    def test_get_nonexistent_key_returns_none(self):
        """Test that getting a non-existent key returns None"""
        cache = LRUCacheWithTTL()
        self.assertIsNone(cache.get("nonexistent"))

    def test_delete_existing_key(self):
        """Test deleting an existing key"""
        cache = LRUCacheWithTTL()
        cache.put("key1", "value1")
        self.assertTrue(cache.delete("key1"))
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.size(), 0)

    def test_delete_nonexistent_key(self):
        """Test deleting a non-existent key returns False"""
        cache = LRUCacheWithTTL()
        self.assertFalse(cache.delete("nonexistent"))

    def test_clear_cache(self):
        """Test clearing all items from cache"""
        cache = LRUCacheWithTTL()
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.clear()
        self.assertEqual(cache.size(), 0)
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))

    def test_item_with_ttl_expires(self):
        """Test that item with TTL expires after specified time"""
        cache = LRUCacheWithTTL()
        cache.put("key1", "value1", ttl=0.5)  # 0.5 second TTL
        self.assertEqual(cache.get("key1"), "value1")

        # Sleep for 0.6 seconds to ensure expiration
        time.sleep(0.6)
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.size(), 0)

    def test_item_without_ttl_does_not_expire(self):
        """Test that item without TTL doesn't expire"""
        cache = LRUCacheWithTTL()
        cache.put("key1", "value1")  # No TTL

        # Sleep for a short time
        time.sleep(0.1)
        self.assertEqual(cache.get("key1"), "value1")

    def test_expired_item_removed_from_cache(self):
        """Test that expired items are removed from cache on access"""
        cache = LRUCacheWithTTL()
        cache.put("key1", "value1", ttl=0.5)
        cache.put("key2", "value2")  # No TTL

        time.sleep(0.6)

        # Getting expired key should return None and remove it
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.size(), 1)

    def test_capacity_limit_evicts_lru_item(self):
        """Test that cache evicts least recently used item when at capacity"""
        cache = LRUCacheWithTTL(2)  # Small capacity
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        # Cache is now full

        # Add third item, should evict key1 (LRU)
        cache.put("key3", "value3")

        self.assertEqual(cache.size(), 2)
        self.assertIsNone(cache.get("key1"))  # Should be evicted
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")

    def test_access_updates_lru_order(self):
        """Test that accessing an item updates its LRU position"""
        cache = LRUCacheWithTTL(2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")

        # Access key1 to make it most recently used
        cache.get("key1")

        # Add third item, should evict key2 (now LRU)
        cache.put("key3", "value3")

        self.assertEqual(cache.size(), 2)
        self.assertEqual(cache.get("key1"), "value1")  # Should still be there
        self.assertIsNone(cache.get("key2"))  # Should be evicted
        self.assertEqual(cache.get("key3"), "value3")

    def test_put_updates_lru_order(self):
        """Test that putting an existing key updates its LRU position"""
        cache = LRUCacheWithTTL(2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")

        # Update key1 to make it most recently used
        cache.put("key1", "new_value1")

        # Add third item, should evict key2 (now LRU)
        cache.put("key3", "value3")

        self.assertEqual(cache.size(), 2)
        self.assertEqual(cache.get("key1"), "new_value1")  # Updated and still there
        self.assertIsNone(cache.get("key2"))  # Should be evicted
        self.assertEqual(cache.get("key3"), "value3")


if __name__ == '__main__':
    unittest.main()