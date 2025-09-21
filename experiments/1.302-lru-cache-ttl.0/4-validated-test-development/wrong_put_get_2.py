"""
Test Validation: Wrong Put/Get Implementation #2
Cache that doesn't handle overwriting correctly
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
    """WRONG IMPLEMENTATION: Doesn't overwrite existing keys properly"""

    def __init__(self, capacity: int, default_ttl: Optional[float] = None):
        if capacity <= 0:
            raise CacheCapacityError(f"Capacity must be positive, got {capacity}")
        if default_ttl is not None and default_ttl < 0:
            raise CacheTTLError(f"TTL must be non-negative, got {default_ttl}")

        self.capacity = capacity
        self.default_ttl = default_ttl
        self._data = {}

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """BUG: Only stores if key doesn't exist, ignores overwrites."""
        if key not in self._data:  # INTENTIONAL BUG
            self._data[key] = value

    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)

    def size(self) -> int:
        return len(self._data)

    def keys(self) -> list:
        return list(self._data.keys())


class TestBasicPutGetOperations(unittest.TestCase):

    def test_put_overwrites_existing_key(self):
        cache = LRUCacheWithTTL(capacity=3, default_ttl=60.0)

        cache.put("key1", "value1")
        cache.put("key1", "new_value")  # This should overwrite

        # This SHOULD FAIL because overwrite is ignored
        self.assertEqual(cache.get("key1"), "new_value")  # SHOULD FAIL


if __name__ == "__main__":
    unittest.main()