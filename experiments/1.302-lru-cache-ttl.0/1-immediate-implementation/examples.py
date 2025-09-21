#!/usr/bin/env python3
"""
Usage Examples for LRU Cache with TTL

This module demonstrates various usage patterns and features of the
LRU Cache with TTL implementation.
"""

import time
import threading
import json
from lru_cache_ttl import create_cache


def example_basic_usage():
    """Demonstrate basic cache operations."""
    print("=" * 50)
    print("Basic Usage Example")
    print("=" * 50)

    # Create cache with 5 items max, 10-second default TTL
    cache = create_cache(max_size=5, default_ttl=10.0)

    try:
        # Set some values
        cache.set("user:1", {"name": "Alice", "age": 30})
        cache.set("user:2", {"name": "Bob", "age": 25})
        cache.set("config", {"theme": "dark", "notifications": True})

        print(f"Cache size: {cache.size()}")

        # Get values
        user1 = cache.get("user:1")
        print(f"User 1: {user1}")

        # Dictionary-like access
        cache["settings"] = {"language": "en", "timezone": "UTC"}
        settings = cache["settings"]
        print(f"Settings: {settings}")

        # Check existence
        if "user:1" in cache:
            print("User 1 exists in cache")

        # Show all keys
        print(f"All keys: {list(cache.keys())}")

        # Get statistics
        stats = cache.get_stats()
        print(f"Hit rate: {stats['hit_rate']:.1%}")

    finally:
        cache.close()


def example_ttl_functionality():
    """Demonstrate TTL (Time-To-Live) functionality."""
    print("\n" + "=" * 50)
    print("TTL Functionality Example")
    print("=" * 50)

    cache = create_cache(max_size=10)

    try:
        # Set items with different TTL values
        cache.set("permanent", "This never expires")  # No TTL
        cache.set("short_lived", "This expires in 2 seconds", ttl=2.0)
        cache.set("medium_lived", "This expires in 5 seconds", ttl=5.0)

        print("Initial state:")
        for key in cache.keys():
            ttl_remaining = cache.ttl(key)
            ttl_str = f"{ttl_remaining:.1f}s" if ttl_remaining else "never"
            print(f"  {key}: expires in {ttl_str}")

        # Wait and check expiration
        print("\nAfter 3 seconds:")
        time.sleep(3)

        for key in ["permanent", "short_lived", "medium_lived"]:
            value = cache.get(key)
            status = "exists" if value else "expired"
            print(f"  {key}: {status}")

        print("\nAfter 6 seconds total:")
        time.sleep(3)

        for key in ["permanent", "short_lived", "medium_lived"]:
            value = cache.get(key)
            status = "exists" if value else "expired"
            print(f"  {key}: {status}")

    finally:
        cache.close()


def example_lru_eviction():
    """Demonstrate LRU eviction behavior."""
    print("\n" + "=" * 50)
    print("LRU Eviction Example")
    print("=" * 50)

    # Small cache to demonstrate eviction
    cache = create_cache(max_size=3)

    try:
        # Fill cache to capacity
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        print(f"Cache after filling to capacity: {list(cache.keys())}")

        # Access key1 to make it most recently used
        cache.get("key1")
        print("Accessed key1 to make it most recently used")

        # Add another item - should evict least recently used (key2)
        cache.set("key4", "value4")
        print(f"After adding key4: {list(cache.keys())}")

        # Verify key2 was evicted
        if cache.get("key2") is None:
            print("key2 was evicted (least recently used)")

        # Show eviction statistics
        stats = cache.get_stats()
        print(f"Evictions: {stats['evictions']}")

    finally:
        cache.close()


def example_thread_safety():
    """Demonstrate thread safety."""
    print("\n" + "=" * 50)
    print("Thread Safety Example")
    print("=" * 50)

    cache = create_cache(max_size=100)
    results = {"successful_operations": 0, "errors": 0}
    lock = threading.Lock()

    def worker(thread_id, operations=100):
        """Worker function for threading test."""
        for i in range(operations):
            try:
                key = f"thread_{thread_id}_key_{i}"
                value = f"thread_{thread_id}_value_{i}"

                # Set value
                cache.set(key, value)

                # Get value
                retrieved = cache.get(key)

                # Verify correctness
                if retrieved == value:
                    with lock:
                        results["successful_operations"] += 1
                else:
                    with lock:
                        results["errors"] += 1

            except Exception:
                with lock:
                    results["errors"] += 1

    try:
        # Start multiple threads
        threads = []
        num_threads = 5

        print(f"Starting {num_threads} threads...")

        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i, 50))
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join()

        print(f"Successful operations: {results['successful_operations']}")
        print(f"Errors: {results['errors']}")
        print(f"Final cache size: {cache.size()}")

        stats = cache.get_stats()
        print(f"Cache statistics: {stats}")

    finally:
        cache.close()


def example_persistence():
    """Demonstrate save/load functionality."""
    print("\n" + "=" * 50)
    print("Persistence Example")
    print("=" * 50)

    # Create and populate cache
    cache1 = create_cache(max_size=50, default_ttl=3600)

    try:
        # Add various data types
        cache1.set("string_data", "Hello, World!")
        cache1.set("number_data", 42)
        cache1.set("list_data", [1, 2, 3, "four", 5.0])
        cache1.set("dict_data", {
            "name": "Example",
            "count": 100,
            "nested": {"flag": True}
        })

        print("Original cache contents:")
        for key, value in cache1.items():
            print(f"  {key}: {value}")

        # Save to file
        save_file = "cache_example.json"
        cache1.save_to_file(save_file)
        print(f"\nSaved cache to {save_file}")

    finally:
        cache1.close()

    # Load into new cache
    cache2 = create_cache()

    try:
        if cache2.load_from_file(save_file):
            print(f"\nLoaded cache from {save_file}")

            print("Restored cache contents:")
            for key, value in cache2.items():
                print(f"  {key}: {value}")

            # Verify data integrity
            original_dict = {"name": "Example", "count": 100, "nested": {"flag": True}}
            restored_dict = cache2.get("dict_data")

            if restored_dict == original_dict:
                print("\nData integrity verified!")
            else:
                print("\nData integrity check failed!")

        else:
            print(f"Failed to load cache from {save_file}")

    finally:
        cache2.close()

    # Cleanup
    import os
    if os.path.exists(save_file):
        os.remove(save_file)


def example_advanced_features():
    """Demonstrate advanced features."""
    print("\n" + "=" * 50)
    print("Advanced Features Example")
    print("=" * 50)

    cache = create_cache(max_size=20, default_ttl=300)

    try:
        # Demonstrate various features
        print("1. Complex data structures:")
        user_session = {
            "user_id": 12345,
            "permissions": ["read", "write", "admin"],
            "metadata": {
                "login_time": time.time(),
                "ip_address": "192.168.1.1",
                "user_agent": "Python Example"
            }
        }
        cache.set("session:abc123", user_session, ttl=1800)  # 30 minutes

        print("2. Conditional operations:")
        # Check before setting
        if not cache.exists("config:theme"):
            cache.set("config:theme", "dark")
            print("Set default theme")

        print("3. Batch operations:")
        # Multiple sets
        data_batch = {
            "metric:cpu": 45.2,
            "metric:memory": 67.8,
            "metric:disk": 23.1
        }

        for key, value in data_batch.items():
            cache.set(key, value, ttl=60)  # 1 minute

        print("4. Statistics monitoring:")
        # Perform various operations
        for i in range(10):
            cache.get(f"metric:cpu")  # Hits
            cache.get(f"nonexistent_{i}")  # Misses

        stats = cache.get_stats()
        print(f"Hit rate: {stats['hit_rate']:.1%}")
        print(f"Total operations: {stats['hits'] + stats['misses']}")

        print("5. Key pattern matching:")
        # Get all metric keys
        metric_keys = [key for key in cache.keys() if key.startswith("metric:")]
        print(f"Metric keys: {metric_keys}")

        print("6. Memory efficiency:")
        print(f"Cache size: {cache.size()}/{cache.capacity()}")
        print(f"Load factor: {cache.size() / cache.capacity() * 100:.1f}%")

    finally:
        cache.close()


def example_real_world_use_case():
    """Demonstrate a real-world use case: Web API response caching."""
    print("\n" + "=" * 50)
    print("Real-World Use Case: API Response Caching")
    print("=" * 50)

    # Simulate an API response cache
    api_cache = create_cache(max_size=1000, default_ttl=300)  # 5 minutes default

    def simulate_api_call(endpoint, params=None):
        """Simulate an expensive API call."""
        time.sleep(0.1)  # Simulate network delay
        return {
            "endpoint": endpoint,
            "params": params,
            "data": f"Response data for {endpoint}",
            "timestamp": time.time()
        }

    def cached_api_call(endpoint, params=None, ttl=None):
        """API call with caching."""
        # Create cache key
        cache_key = f"api:{endpoint}"
        if params:
            import hashlib
            param_hash = hashlib.md5(str(sorted(params.items())).encode()).hexdigest()[:8]
            cache_key += f":{param_hash}"

        # Try cache first
        cached_response = api_cache.get(cache_key)
        if cached_response:
            print(f"Cache HIT for {endpoint}")
            return cached_response

        # Cache miss - make actual API call
        print(f"Cache MISS for {endpoint} - making API call")
        response = simulate_api_call(endpoint, params)

        # Cache the response
        cache_ttl = ttl or 300  # 5 minutes default
        api_cache.set(cache_key, response, ttl=cache_ttl)

        return response

    try:
        print("Simulating API calls with caching:")

        # First calls (cache misses)
        cached_api_call("/users", {"page": 1})
        cached_api_call("/posts", {"user_id": 123})
        cached_api_call("/comments", {"post_id": 456})

        print("\nRepeating same calls (should be cache hits):")
        cached_api_call("/users", {"page": 1})
        cached_api_call("/posts", {"user_id": 123})
        cached_api_call("/comments", {"post_id": 456})

        print("\nCalls with different parameters (cache misses):")
        cached_api_call("/users", {"page": 2})
        cached_api_call("/posts", {"user_id": 124})

        # Show cache statistics
        stats = api_cache.get_stats()
        print(f"\nCache Statistics:")
        print(f"Hit rate: {stats['hit_rate']:.1%}")
        print(f"Total requests: {stats['hits'] + stats['misses']}")
        print(f"Cache size: {api_cache.size()}")

        # Demonstrate TTL for different endpoints
        print(f"\nUsing different TTL for different endpoints:")
        cached_api_call("/config", ttl=3600)  # Config cached for 1 hour
        cached_api_call("/realtime", ttl=10)  # Realtime data cached for 10 seconds

        print(f"Cache keys: {list(api_cache.keys())}")

    finally:
        api_cache.close()


def main():
    """Run all examples."""
    print("LRU Cache with TTL - Usage Examples")
    print("=" * 60)

    try:
        example_basic_usage()
        example_ttl_functionality()
        example_lru_eviction()
        example_thread_safety()
        example_persistence()
        example_advanced_features()
        example_real_world_use_case()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")

    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"\nExample failed with error: {e}")
        raise


if __name__ == "__main__":
    main()