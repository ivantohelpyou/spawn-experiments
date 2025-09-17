"""
Simple test runner for our cache implementation
"""

import sys
import traceback
from lru_cache_ttl import LRUCacheWithTTL


def run_test(test_func, test_name):
    """Run a single test and report results"""
    try:
        test_func()
        print(f"✅ PASS: {test_name}")
        return True
    except Exception as e:
        print(f"❌ FAIL: {test_name}")
        print(f"   Error: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False


def test_cache_initialization_with_capacity():
    cache = LRUCacheWithTTL(capacity=10)
    assert cache.capacity == 10


def test_cache_initialization_with_default_ttl():
    cache = LRUCacheWithTTL(capacity=10, default_ttl=300)
    assert hasattr(cache, 'default_ttl')
    assert cache.default_ttl == 300


def test_cache_starts_empty():
    cache = LRUCacheWithTTL(capacity=5)
    assert len(cache) == 0
    assert cache.size() == 0


def test_invalid_capacity_raises_error():
    try:
        LRUCacheWithTTL(capacity=0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Capacity must be a positive integer" in str(e)

    try:
        LRUCacheWithTTL(capacity=-1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Capacity must be a positive integer" in str(e)


def test_invalid_ttl_raises_error():
    try:
        LRUCacheWithTTL(capacity=10, default_ttl=-1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "TTL must be None or a positive number" in str(e)


def test_can_determine_if_key_exists():
    cache = LRUCacheWithTTL(capacity=10)
    assert "key1" not in cache


def test_basic_key_value_storage():
    cache = LRUCacheWithTTL(capacity=10)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    assert "key1" in cache
    assert len(cache) == 1


def test_multiple_key_storage():
    cache = LRUCacheWithTTL(capacity=10)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert len(cache) == 3


# Dictionary Interface Tests
def test_dictionary_style_get_set():
    cache = LRUCacheWithTTL(capacity=10)
    cache["key1"] = "value1"
    cache["key2"] = "value2"
    assert cache["key1"] == "value1"
    assert cache["key2"] == "value2"


def test_dictionary_style_delete():
    cache = LRUCacheWithTTL(capacity=10)
    cache["key1"] = "value1"
    assert "key1" in cache
    del cache["key1"]
    assert "key1" not in cache


def test_delete_nonexistent_key_raises_keyerror():
    cache = LRUCacheWithTTL(capacity=10)
    try:
        del cache["nonexistent"]
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_get_nonexistent_key_raises_keyerror():
    cache = LRUCacheWithTTL(capacity=10)
    try:
        value = cache["nonexistent"]
        assert False, "Should have raised KeyError"
    except KeyError as e:
        assert "nonexistent" in str(e)


def test_iteration_over_keys():
    cache = LRUCacheWithTTL(capacity=10)
    cache["key1"] = "value1"
    cache["key2"] = "value2"
    cache["key3"] = "value3"

    keys = list(cache)
    assert len(keys) == 3
    assert "key1" in keys
    assert "key2" in keys
    assert "key3" in keys


def test_update_existing_key_with_new_value():
    cache = LRUCacheWithTTL(capacity=10)
    cache["key1"] = "value1"
    assert len(cache) == 1
    assert cache["key1"] == "value1"

    cache["key1"] = "new_value"
    assert len(cache) == 1
    assert cache["key1"] == "new_value"


def test_cache_size_tracking_during_operations():
    cache = LRUCacheWithTTL(capacity=10)
    assert len(cache) == 0
    assert cache.size() == 0

    cache["key1"] = "value1"
    assert len(cache) == 1
    assert cache.size() == 1

    cache["key2"] = "value2"
    assert len(cache) == 2
    assert cache.size() == 2

    cache["key1"] = "new_value"
    assert len(cache) == 2
    assert cache.size() == 2

    del cache["key1"]
    assert len(cache) == 1
    assert cache.size() == 1


def main():
    """Run all tests"""
    print("=== Running Enhanced TDD Tests for Basic Cache Features ===\n")

    tests = [
        (test_cache_initialization_with_capacity, "test_cache_initialization_with_capacity"),
        (test_cache_initialization_with_default_ttl, "test_cache_initialization_with_default_ttl"),
        (test_cache_starts_empty, "test_cache_starts_empty"),
        (test_invalid_capacity_raises_error, "test_invalid_capacity_raises_error"),
        (test_invalid_ttl_raises_error, "test_invalid_ttl_raises_error"),
        (test_can_determine_if_key_exists, "test_can_determine_if_key_exists"),
        (test_basic_key_value_storage, "test_basic_key_value_storage"),
        (test_multiple_key_storage, "test_multiple_key_storage"),
        (test_dictionary_style_get_set, "test_dictionary_style_get_set"),
        (test_dictionary_style_delete, "test_dictionary_style_delete"),
        (test_delete_nonexistent_key_raises_keyerror, "test_delete_nonexistent_key_raises_keyerror"),
        (test_get_nonexistent_key_raises_keyerror, "test_get_nonexistent_key_raises_keyerror"),
        (test_iteration_over_keys, "test_iteration_over_keys"),
        (test_update_existing_key_with_new_value, "test_update_existing_key_with_new_value"),
        (test_cache_size_tracking_during_operations, "test_cache_size_tracking_during_operations"),
    ]

    passed = 0
    total = len(tests)

    for test_func, test_name in tests:
        if run_test(test_func, test_name):
            passed += 1
        print()

    print(f"=== TEST RESULTS ===")
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✅ ALL TESTS PASSED! Ready to proceed to next feature.")
    else:
        print("❌ SOME TESTS FAILED! Fix implementation before proceeding.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)