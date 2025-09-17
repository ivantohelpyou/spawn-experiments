import unittest
import time
from lru_cache_ttl import LRUCacheWithTTL


class TestLRUCacheWithTTL(unittest.TestCase):

    def test_constructor_creates_cache_with_capacity(self):
        """Test that cache can be created with specified capacity"""
        cache = LRUCacheWithTTL(capacity=5)
        self.assertEqual(cache.capacity(), 5)
        self.assertEqual(cache.size(), 0)


if __name__ == '__main__':
    unittest.main()