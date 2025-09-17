"""
Test Validation: Wrong Implementation #2
Cache that doesn't validate input parameters
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
    """WRONG IMPLEMENTATION: No input validation"""

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        # BUG: Accept ANY capacity, even invalid ones
        self.capacity = capacity  # NO VALIDATION
        self.default_ttl = default_ttl  # NO VALIDATION
        self.data = {}

    def size(self):
        return len(self.data)

    def keys(self):
        return list(self.data.keys())


class TestCacheInitialization(unittest.TestCase):

    def test_cache_init_zero_capacity_raises_error(self):
        # This SHOULD FAIL because implementation doesn't validate
        with self.assertRaises(CacheCapacityError):
            LRUCacheWithTTL(capacity=0, default_ttl=60.0)

    def test_cache_init_negative_ttl_raises_error(self):
        # This SHOULD FAIL because implementation doesn't validate TTL
        with self.assertRaises(CacheTTLError):
            LRUCacheWithTTL(capacity=3, default_ttl=-10.0)


if __name__ == "__main__":
    unittest.main()