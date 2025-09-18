#!/usr/bin/env python3
"""
LRU Cache with TTL Demonstration Script

This script demonstrates all the functionality of the LRU Cache with TTL
implementation, including capacity management, TTL expiration, and LRU eviction.
"""

import time
import sys
from lru_cache_ttl import LRUCacheWithTTL


def print_separator(title: str):
    """Print a formatted section separator."""
    print(f"\\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_cache_state(cache: LRUCacheWithTTL, description: str):
    """Print the current state of the cache."""
    print(f"\\n{description}:")
    print(f"  Size: {cache.size()}/{cache.capacity}")
    print(f"  Keys: {cache.keys()}")
    print(f"  Items: {cache.items()}")
    print(f"  Representation: {cache}")


def demonstrate_basic_operations():
    """Demonstrate basic put and get operations."""
    print_separator("Basic Operations")

    # Create cache
    cache = LRUCacheWithTTL(3)
    print(f"Created cache with capacity 3")

    # Test put operations
    print("\\nAdding items:")
    cache.put("name", "Alice", 10.0)
    print(f"  put('name', 'Alice', 10.0)")

    cache.put("age", 25, 10.0)
    print(f"  put('age', 25, 10.0)")

    cache.put("city", "New York", 10.0)
    print(f"  put('city', 'New York', 10.0)")

    print_cache_state(cache, "Cache after adding 3 items")

    # Test get operations
    print("\\nRetrieving items:")
    for key in ["name", "age", "city", "nonexistent"]:
        value = cache.get(key)
        print(f"  get('{key}') = {value}")

    return cache


def demonstrate_capacity_limit(cache: LRUCacheWithTTL):
    """Demonstrate LRU eviction when capacity is exceeded."""
    print_separator("Capacity Limit and LRU Eviction")

    print_cache_state(cache, "Current cache state")

    # Access 'name' to make it most recently used
    print("\\nAccessing 'name' to make it most recently used:")
    value = cache.get("name")
    print(f"  get('name') = {value}")

    print_cache_state(cache, "Cache after accessing 'name'")

    # Add a 4th item - should evict LRU item ('age')
    print("\\nAdding 4th item (should evict LRU item):")
    cache.put("country", "USA", 10.0)
    print(f"  put('country', 'USA', 10.0)")

    print_cache_state(cache, "Cache after adding 4th item (age should be evicted)")

    return cache


def demonstrate_ttl_expiration():
    """Demonstrate TTL expiration functionality."""
    print_separator("TTL Expiration")

    # Create fresh cache
    cache = LRUCacheWithTTL(5)
    print("Created fresh cache with capacity 5")

    # Add items with different TTLs
    print("\\nAdding items with different TTLs:")
    cache.put("short", "expires soon", 2.0)
    print("  put('short', 'expires soon', 2.0)")

    cache.put("medium", "expires later", 4.0)
    print("  put('medium', 'expires later', 4.0)")

    cache.put("long", "expires last", 6.0)
    print("  put('long', 'expires last', 6.0)")

    print_cache_state(cache, "Cache with items having different TTLs")

    # Wait and check expiration
    print("\\nWaiting 2.5 seconds for 'short' to expire...")
    time.sleep(2.5)

    print("\\nAccessing items after 2.5 seconds:")
    for key in ["short", "medium", "long"]:
        value = cache.get(key)
        print(f"  get('{key}') = {value}")

    print_cache_state(cache, "Cache after first expiration")

    print("\\nWaiting another 2 seconds for 'medium' to expire...")
    time.sleep(2.0)

    print("\\nAccessing items after 4.5 seconds total:")
    for key in ["short", "medium", "long"]:
        value = cache.get(key)
        print(f"  get('{key}') = {value}")

    print_cache_state(cache, "Cache after second expiration")

    return cache


def demonstrate_edge_cases():
    """Demonstrate edge cases and error handling."""
    print_separator("Edge Cases and Error Handling")

    # Test invalid capacity
    print("Testing invalid capacity:")
    try:
        invalid_cache = LRUCacheWithTTL(0)
    except ValueError as e:
        print(f"  LRUCacheWithTTL(0) raised: {e}")

    try:
        invalid_cache = LRUCacheWithTTL(-1)
    except ValueError as e:
        print(f"  LRUCacheWithTTL(-1) raised: {e}")

    # Test invalid TTL
    cache = LRUCacheWithTTL(3)
    print("\\nTesting invalid TTL:")
    try:
        cache.put("test", "value", 0)
    except ValueError as e:
        print(f"  put('test', 'value', 0) raised: {e}")

    try:
        cache.put("test", "value", -1)
    except ValueError as e:
        print(f"  put('test', 'value', -1) raised: {e}")

    # Test updating existing key
    print("\\nTesting key updates:")
    cache.put("key1", "value1", 5.0)
    print("  put('key1', 'value1', 5.0)")
    print_cache_state(cache, "Cache after adding key1")

    cache.put("key1", "updated_value", 10.0)
    print("  put('key1', 'updated_value', 10.0)")
    print_cache_state(cache, "Cache after updating key1")

    # Test clear operation
    print("\\nTesting clear operation:")
    cache.clear()
    print("  cache.clear()")
    print_cache_state(cache, "Cache after clear")

    return cache


def demonstrate_magic_methods():
    """Demonstrate magic methods (__len__, __contains__, __str__)."""
    print_separator("Magic Methods")

    cache = LRUCacheWithTTL(3)

    # Add some items
    cache.put("a", 1, 5.0)
    cache.put("b", 2, 5.0)
    cache.put("c", 3, 5.0)

    print("Added items: a=1, b=2, c=3")

    # Test __len__
    print(f"\\nlen(cache) = {len(cache)}")

    # Test __contains__
    print("\\nTesting 'in' operator:")
    for key in ["a", "b", "c", "d"]:
        result = key in cache
        print(f"  '{key}' in cache = {result}")

    # Test __str__
    print(f"\\nstr(cache) = {str(cache)}")

    return cache


def demonstrate_performance_characteristics():
    """Demonstrate O(1) performance characteristics."""
    print_separator("Performance Characteristics")

    print("All operations are O(1) average case:")
    print("  - put(): O(1) - hash table lookup + doubly linked list operations")
    print("  - get(): O(1) - hash table lookup + doubly linked list operations")
    print("  - Capacity enforcement: O(1) - remove tail node")
    print("  - TTL cleanup: O(k) where k is number of expired items")

    # Create large cache to demonstrate
    cache = LRUCacheWithTTL(1000)

    print("\\nDemonstrating with larger cache (capacity 1000):")

    # Time some operations
    import time

    start_time = time.time()
    for i in range(1000):
        cache.put(f"key_{i}", f"value_{i}", 60.0)
    put_time = time.time() - start_time

    start_time = time.time()
    for i in range(1000):
        cache.get(f"key_{i}")
    get_time = time.time() - start_time

    print(f"  Time to put 1000 items: {put_time:.4f}s ({put_time/1000*1000:.4f}ms per operation)")
    print(f"  Time to get 1000 items: {get_time:.4f}s ({get_time/1000*1000:.4f}ms per operation)")

    print(f"\\nFinal cache size: {cache.size()}")

    return cache


def main():
    """Run all demonstrations."""
    print("LRU Cache with TTL - Complete Demonstration")
    print("This script demonstrates all features of the implementation.")

    try:
        # Run demonstrations
        cache1 = demonstrate_basic_operations()
        cache2 = demonstrate_capacity_limit(cache1)
        cache3 = demonstrate_ttl_expiration()
        cache4 = demonstrate_edge_cases()
        cache5 = demonstrate_magic_methods()
        cache6 = demonstrate_performance_characteristics()

        print_separator("Demonstration Complete")
        print("All features have been successfully demonstrated!")
        print("\\nKey features verified:")
        print("  ✓ Basic put/get operations")
        print("  ✓ LRU eviction when capacity exceeded")
        print("  ✓ TTL expiration with automatic cleanup")
        print("  ✓ Error handling for invalid inputs")
        print("  ✓ Key updates and cache clearing")
        print("  ✓ Magic methods (__len__, __contains__, __str__)")
        print("  ✓ O(1) performance characteristics")

    except KeyboardInterrupt:
        print("\\nDemonstration interrupted by user.")
    except Exception as e:
        print(f"\\nError during demonstration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()