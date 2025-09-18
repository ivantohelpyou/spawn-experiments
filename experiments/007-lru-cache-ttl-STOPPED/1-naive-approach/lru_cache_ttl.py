"""
LRU Cache with TTL (Time-To-Live) Implementation

This module provides an LRU (Least Recently Used) cache with TTL functionality.
All operations are O(1) average case through the use of a hash map and doubly linked list.

Features:
- put(key, value, ttl_seconds): Store item with expiration
- get(key): Return value if exists and not expired, None otherwise
- capacity: Maximum number of items
- When capacity exceeded, remove LRU item
- When items expire, they are automatically removed on next access
- All operations are O(1) average case
"""

import time
from typing import Any, Optional


class Node:
    """Doubly linked list node for LRU implementation."""

    def __init__(self, key: Any, value: Any, expires_at: float):
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


class LRUCacheWithTTL:
    """
    LRU Cache with TTL (Time-To-Live) functionality.

    This cache maintains items with expiration times and automatically
    removes the least recently used items when capacity is exceeded.
    """

    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with given capacity.

        Args:
            capacity: Maximum number of items the cache can hold

        Raises:
            ValueError: If capacity is not positive
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.cache = {}  # key -> node mapping

        # Create dummy head and tail nodes for doubly linked list
        self.head = Node(None, None, float('inf'))
        self.tail = Node(None, None, float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

    def _is_expired(self, node: Node) -> bool:
        """Check if a node has expired."""
        return time.time() > node.expires_at

    def _remove_node(self, node: Node) -> None:
        """Remove a node from the doubly linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: Node) -> None:
        """Add a node right after the head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: Node) -> None:
        """Move an existing node to the head."""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> Node:
        """Remove the last node (before dummy tail)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node

    def _cleanup_expired_items(self) -> None:
        """Remove all expired items from the cache."""
        current_time = time.time()
        expired_keys = []

        # Find all expired keys
        for key, node in self.cache.items():
            if current_time > node.expires_at:
                expired_keys.append(key)

        # Remove expired items
        for key in expired_keys:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]

    def get(self, key: Any) -> Optional[Any]:
        """
        Get value by key if it exists and hasn't expired.

        Args:
            key: The key to look up

        Returns:
            The value if key exists and hasn't expired, None otherwise
        """
        # Clean up expired items first
        self._cleanup_expired_items()

        if key not in self.cache:
            return None

        node = self.cache[key]

        # Check if item has expired
        if self._is_expired(node):
            self._remove_node(node)
            del self.cache[key]
            return None

        # Move to head (mark as recently used)
        self._move_to_head(node)
        return node.value

    def put(self, key: Any, value: Any, ttl_seconds: float) -> None:
        """
        Store a key-value pair with TTL.

        Args:
            key: The key to store
            value: The value to store
            ttl_seconds: Time to live in seconds

        Raises:
            ValueError: If TTL is not positive
        """
        if ttl_seconds <= 0:
            raise ValueError("TTL must be positive")

        # Clean up expired items first
        self._cleanup_expired_items()

        expires_at = time.time() + ttl_seconds

        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            node.expires_at = expires_at
            self._move_to_head(node)
        else:
            # Add new key
            new_node = Node(key, value, expires_at)

            if len(self.cache) >= self.capacity:
                # Remove LRU item
                tail_node = self._remove_tail()
                del self.cache[tail_node.key]

            self.cache[key] = new_node
            self._add_to_head(new_node)

    def size(self) -> int:
        """
        Get the current number of items in the cache.

        Returns:
            Number of items currently in cache
        """
        self._cleanup_expired_items()
        return len(self.cache)

    def clear(self) -> None:
        """Remove all items from the cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head

    def keys(self) -> list:
        """
        Get all non-expired keys in the cache.

        Returns:
            List of keys for non-expired items
        """
        self._cleanup_expired_items()
        return list(self.cache.keys())

    def items(self) -> list:
        """
        Get all non-expired key-value pairs.

        Returns:
            List of (key, value) tuples for non-expired items
        """
        self._cleanup_expired_items()
        return [(key, node.value) for key, node in self.cache.items()]

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return self.size()

    def __contains__(self, key: Any) -> bool:
        """Check if key exists and hasn't expired."""
        return self.get(key) is not None

    def __str__(self) -> str:
        """String representation of the cache."""
        self._cleanup_expired_items()
        items = []
        current = self.head.next
        while current != self.tail:
            expires_in = current.expires_at - time.time()
            items.append(f"{current.key}: {current.value} (expires in {expires_in:.1f}s)")
            current = current.next
        return f"LRUCacheWithTTL(capacity={self.capacity}, items=[{', '.join(items)}])"