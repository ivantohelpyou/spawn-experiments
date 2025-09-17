#!/usr/bin/env python3
"""
Demo script for LRU Cache with TTL implementation.
Demonstrates all key features developed using Test-Driven Development.
"""

import time
from lru_cache_ttl import LRUCacheWithTTL

def main():
    print("=== LRU Cache with TTL Demo ===")
    print("Implementation built using strict Test-Driven Development\n")

    # Demo 1: Basic Operations
    print("1. Basic Cache Operations:")
    cache = LRUCacheWithTTL(capacity=3)

    cache.put("user:1", {"name": "Alice", "age": 30})
    cache.put("user:2", {"name": "Bob", "age": 25})
    cache.put("user:3", {"name": "Charlie", "age": 35})

    print(f"Cache size: {cache.size()}")
    print(f"Get user:1: {cache.get('user:1')}")
    print(f"Get user:2: {cache.get('user:2')}")
    print()

    # Demo 2: LRU Eviction
    print("2. LRU Eviction (capacity=3):")
    print("Adding user:4 should evict user:3 (least recently used)")

    cache.put("user:4", {"name": "David", "age": 28})
    print(f"Cache size: {cache.size()}")
    print(f"Get user:3 (should be None): {cache.get('user:3')}")
    print(f"Get user:4: {cache.get('user:4')}")
    print()

    # Demo 3: TTL Functionality
    print("3. TTL (Time-To-Live) Functionality:")
    ttl_cache = LRUCacheWithTTL(capacity=5)

    ttl_cache.put("session:abc", "user_data_here", ttl=2.0)  # 2 seconds TTL
    ttl_cache.put("temp:xyz", "temporary_data", ttl=1.0)      # 1 second TTL

    print(f"Immediately after putting: session:abc = {ttl_cache.get('session:abc')}")
    print(f"Immediately after putting: temp:xyz = {ttl_cache.get('temp:xyz')}")

    print("Waiting 1.5 seconds...")
    time.sleep(1.5)

    print(f"After 1.5s: session:abc = {ttl_cache.get('session:abc')}")  # Should exist
    print(f"After 1.5s: temp:xyz = {ttl_cache.get('temp:xyz')}")        # Should be None (expired)
    print(f"Cache size after expiration: {ttl_cache.size()}")
    print()

    # Demo 4: Default TTL
    print("4. Default TTL:")
    default_ttl_cache = LRUCacheWithTTL(capacity=3, default_ttl=0.5)

    default_ttl_cache.put("auto_expire", "this will expire in 0.5s")
    print(f"Immediately: auto_expire = {default_ttl_cache.get('auto_expire')}")

    time.sleep(0.6)
    print(f"After 0.6s: auto_expire = {default_ttl_cache.get('auto_expire')}")
    print()

    # Demo 5: Cache Management
    print("5. Cache Management:")
    mgmt_cache = LRUCacheWithTTL(capacity=3)
    mgmt_cache.put("key1", "value1")
    mgmt_cache.put("key2", "value2")
    mgmt_cache.put("key3", "value3")

    print(f"Before delete: size = {mgmt_cache.size()}")
    deleted = mgmt_cache.delete("key2")
    print(f"Deleted key2: {deleted}")
    print(f"After delete: size = {mgmt_cache.size()}")

    mgmt_cache.clear()
    print(f"After clear: size = {mgmt_cache.size()}")
    print()

    # Demo 6: Error Handling
    print("6. Error Handling:")
    try:
        LRUCacheWithTTL(capacity=0)
    except ValueError as e:
        print(f"Invalid capacity error: {e}")

    try:
        test_cache = LRUCacheWithTTL(capacity=1)
        test_cache.put(123, "value")
    except TypeError as e:
        print(f"Invalid key type error: {e}")

    try:
        test_cache = LRUCacheWithTTL(capacity=1)
        test_cache.put("key", "value", ttl=-1)
    except ValueError as e:
        print(f"Invalid TTL error: {e}")
    print()

    print("=== Demo Complete ===")
    print("All features implemented using Red-Green-Refactor TDD cycles")
    print("✓ Basic get/put operations")
    print("✓ LRU eviction policy")
    print("✓ TTL expiration")
    print("✓ Cache management (delete/clear)")
    print("✓ Comprehensive error handling")

if __name__ == "__main__":
    main()