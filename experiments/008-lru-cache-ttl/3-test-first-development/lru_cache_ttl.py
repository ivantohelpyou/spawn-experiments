from collections import OrderedDict
import time


class CacheItem:
    """Represents an item in the cache with value and expiration info"""
    def __init__(self, value, ttl=None):
        self.value = value
        self.expiry_time = time.time() + ttl if ttl is not None else None

    def is_expired(self):
        """Check if the item has expired"""
        if self.expiry_time is None:
            return False
        return time.time() > self.expiry_time


class LRUCacheWithTTL:
    """LRU Cache with Time-To-Live functionality"""

    def __init__(self, capacity, default_ttl=None):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer (>= 1)")

        if default_ttl is not None and default_ttl < 0:
            raise ValueError("Default TTL must be non-negative")

        self._capacity = capacity
        self._default_ttl = default_ttl
        self._data = OrderedDict()

    def capacity(self):
        """Return the maximum capacity of the cache"""
        return self._capacity

    def size(self):
        """Return the current size of the cache"""
        # Clean expired items and return size
        self._clean_expired()
        return len(self._data)

    def put(self, key, value, ttl=None):
        """Store a key-value pair in the cache"""
        self._validate_key(key)

        if ttl is not None and ttl < 0:
            raise ValueError("TTL must be non-negative")

        # Use provided TTL or default TTL
        effective_ttl = ttl if ttl is not None else self._default_ttl

        if key in self._data:
            # Move to end (most recently used)
            self._data.move_to_end(key)
        else:
            # Check if we need to evict
            if len(self._data) >= self._capacity:
                # Remove least recently used (first item)
                self._data.popitem(last=False)

        self._data[key] = CacheItem(value, effective_ttl)

    def get(self, key):
        """Retrieve a value by key, return None if not found or expired"""
        self._validate_key(key)

        if key in self._data:
            item = self._data[key]
            if item.is_expired():
                # Remove expired item
                del self._data[key]
                return None
            else:
                # Move to end (most recently used)
                self._data.move_to_end(key)
                return item.value
        return None

    def delete(self, key):
        """Delete a specific key from cache, return True if deleted, False if not found"""
        self._validate_key(key)

        if key in self._data:
            del self._data[key]
            return True
        return False

    def _validate_key(self, key):
        """Validate that key is a non-empty string"""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if key == "":
            raise ValueError("Key cannot be an empty string")

    def clear(self):
        """Remove all items from the cache"""
        self._data.clear()

    def _clean_expired(self):
        """Remove all expired items from cache"""
        expired_keys = []
        for key, item in self._data.items():
            if item.is_expired():
                expired_keys.append(key)

        for key in expired_keys:
            del self._data[key]