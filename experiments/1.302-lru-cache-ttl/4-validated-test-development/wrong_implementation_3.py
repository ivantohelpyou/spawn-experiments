"""
Test Validation: Wrong Implementation #3
Cache that starts with pre-existing data
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
    """WRONG IMPLEMENTATION: Starts with pre-existing data"""

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        self.capacity = capacity
        self.default_ttl = default_ttl
        # BUG: Start with pre-existing data
        self.data = {"preloaded": "value"}  # INTENTIONAL BUG

    def size(self):
        return len(self.data)

    def keys(self):
        return list(self.data.keys())


class TestCacheInitialization(unittest.TestCase):

    def test_cache_starts_empty(self):
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        # These SHOULD FAIL because cache starts with data
        assert cache.size() == 0  # SHOULD FAIL
        assert len(cache.keys()) == 0  # SHOULD FAIL


if __name__ == "__main__":
    unittest.main()