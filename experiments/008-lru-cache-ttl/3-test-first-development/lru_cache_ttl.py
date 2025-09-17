class LRUCacheWithTTL:
    """LRU Cache with Time-To-Live functionality"""

    def __init__(self, capacity):
        self._capacity = capacity
        self._size = 0

    def capacity(self):
        """Return the maximum capacity of the cache"""
        return self._capacity

    def size(self):
        """Return the current size of the cache"""
        return self._size