"""
Test Validation: Wrong Put/Get Implementation #1
Cache that doesn't properly store values
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
    """WRONG IMPLEMENTATION: Always returns None from get()"""

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        if capacity <= 0:
            raise CacheCapacityError(f"Capacity must be positive, got {capacity}")
        if default_ttl is not None and default_ttl < 0:
            raise CacheTTLError(f"TTL must be non-negative, got {default_ttl}")

        self.capacity = capacity
        self.default_ttl = default_ttl
        self._data = {}

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Store appears to work but actually doesn't save values."""
        # BUG: Store key but always with None value
        self._data[key] = None  # INTENTIONAL BUG

    def get(self, key: str) -> Optional[Any]:
        """Always returns None regardless of what was stored."""
        # BUG: Always return None
        return None  # INTENTIONAL BUG

    def size(self) -> int:
        return len(self._data)

    def keys(self) -> list:
        return list(self._data.keys())


class TestBasicPutGetOperations(unittest.TestCase):

    def test_put_and_get_single_item(self):
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1")
        result = cache.get("key1")

        # This SHOULD FAIL because get always returns None
        self.assertEqual(result, "value1")  # SHOULD FAIL


if __name__ == "__main__":
    unittest.main()