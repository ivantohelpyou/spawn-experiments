"""
Test Validation: Wrong Implementation #1
Cache that stores wrong capacity value
"""

import unittest
import time
from typing import Any, Optional


class CacheError(Exception):
    pass


class CacheCapacityError(CacheError):
    pass


class CacheTTLError(CacheError):
    pass


class LRUCacheWithTTL:
    """WRONG IMPLEMENTATION: Stores capacity + 1 instead of actual capacity"""

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        # BUG: Store wrong capacity value
        self.capacity = capacity + 1  # INTENTIONAL BUG
        self.default_ttl = default_ttl
        self.data = {}

    def size(self):
        return len(self.data)

    def keys(self):
        return list(self.data.keys())


class TestCacheInitialization(unittest.TestCase):

    def test_cache_init_with_valid_capacity_and_default_ttl(self):
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        # This SHOULD FAIL because cache.capacity will be 4, not 3
        assert cache.capacity == 3  # SHOULD FAIL
        assert cache.default_ttl == 60.0


if __name__ == "__main__":
    unittest.main()