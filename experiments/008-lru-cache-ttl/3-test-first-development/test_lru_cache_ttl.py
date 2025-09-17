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


if __name__ == '__main__':
    unittest.main()