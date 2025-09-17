from collections import OrderedDict


class LRUCacheWithTTL:
    """LRU Cache with Time-To-Live functionality"""

    def __init__(self, capacity):
        self._capacity = capacity
        self._data = OrderedDict()

    def capacity(self):
        """Return the maximum capacity of the cache"""
        return self._capacity

    def size(self):
        """Return the current size of the cache"""
        return len(self._data)

    def put(self, key, value):
        """Store a key-value pair in the cache"""
        if key in self._data:
            # Move to end (most recently used)
            self._data.move_to_end(key)
        else:
            # Check if we need to evict
            if len(self._data) >= self._capacity:
                # Remove least recently used (first item)
                self._data.popitem(last=False)

        self._data[key] = value

    def get(self, key):
        """Retrieve a value by key, return None if not found"""
        if key in self._data:
            # Move to end (most recently used)
            self._data.move_to_end(key)
            return self._data[key]
        return None