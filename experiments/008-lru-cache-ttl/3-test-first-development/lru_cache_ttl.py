class LRUCacheWithTTL:
    """LRU Cache with Time-To-Live functionality"""

    def __init__(self, capacity):
        self._capacity = capacity
        self._data = {}

    def capacity(self):
        """Return the maximum capacity of the cache"""
        return self._capacity

    def size(self):
        """Return the current size of the cache"""
        return len(self._data)

    def put(self, key, value):
        """Store a key-value pair in the cache"""
        self._data[key] = value

    def get(self, key):
        """Retrieve a value by key, return None if not found"""
        return self._data.get(key)