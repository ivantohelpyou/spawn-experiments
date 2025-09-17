import time


class CacheNode:
    """Node for doubly linked list used in LRU implementation"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCacheWithTTL:
    """LRU Cache with Time-To-Live support"""

    def __init__(self, capacity=100):
        """Initialize cache with given capacity"""
        self._capacity = capacity
        self._size = 0
        self._cache = {}  # key -> CacheNode
        self._expiry = {}  # key -> expiry_time

        # Create dummy head and tail nodes for doubly linked list
        self._head = CacheNode(None, None)
        self._tail = CacheNode(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    def capacity(self):
        """Return maximum capacity of cache"""
        return self._capacity

    def size(self):
        """Return current number of items in cache"""
        return self._size

    def _add_to_head(self, node):
        """Add node right after head"""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node):
        """Remove an existing node from linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node):
        """Move existing node to head (most recently used)"""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self):
        """Remove last node before tail (least recently used)"""
        last_node = self._tail.prev
        if last_node != self._head:
            self._remove_node(last_node)
            return last_node
        return None

    def put(self, key, value, ttl=None):
        """Store a key-value pair with optional TTL"""
        if key in self._cache:
            # Key already exists, update value and move to head
            node = self._cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # New key
            node = CacheNode(key, value)

            if self._size >= self._capacity:
                # Remove LRU item
                tail_node = self._remove_tail()
                if tail_node:
                    del self._cache[tail_node.key]
                    if tail_node.key in self._expiry:
                        del self._expiry[tail_node.key]
                    self._size -= 1

            # Add new node
            self._cache[key] = node
            self._add_to_head(node)
            self._size += 1

        # Handle TTL
        if ttl is not None:
            self._expiry[key] = time.time() + ttl
        elif key in self._expiry:
            # Remove expiry if key had TTL before but doesn't now
            del self._expiry[key]

    def get(self, key):
        """Retrieve value by key"""
        if key not in self._cache:
            return None

        node = self._cache[key]

        # Check if key has expired
        if key in self._expiry and time.time() > self._expiry[key]:
            # Key has expired, remove it
            self._remove_node(node)
            del self._cache[key]
            del self._expiry[key]
            self._size -= 1
            return None

        # Move to head (most recently used)
        self._move_to_head(node)
        return node.value

    def delete(self, key):
        """Delete a key-value pair"""
        if key in self._cache:
            node = self._cache[key]
            self._remove_node(node)
            del self._cache[key]
            if key in self._expiry:
                del self._expiry[key]
            self._size -= 1
            return True
        return False

    def clear(self):
        """Remove all cached items"""
        self._cache.clear()
        self._expiry.clear()
        self._size = 0
        # Reset linked list
        self._head.next = self._tail
        self._tail.prev = self._head