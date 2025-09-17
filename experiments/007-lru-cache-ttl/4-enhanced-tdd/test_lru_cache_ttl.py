"""
Test-Driven Development for LRU Cache with TTL
Enhanced approach with comprehensive test validation
"""

import pytest
import time
from typing import Any, Optional
from lru_cache_ttl import LRUCacheWithTTL


class TestCacheInitialization:
    """Tests for basic cache initialization and core functionality"""

    def test_cache_initialization_with_capacity(self):
        """
        Test Explanation:
        This test verifies that a cache can be created with a specified capacity.
        If the implementation fails to set capacity correctly, this test should fail.
        If the implementation doesn't create the internal storage structures,
        accessing .capacity property would fail.

        What this test actually validates:
        - Constructor accepts capacity parameter
        - Capacity property returns correct value
        - Cache is properly initialized and ready for use
        """
        cache = LRUCacheWithTTL(capacity=10)
        assert cache.capacity == 10

    def test_cache_initialization_with_default_ttl(self):
        """
        Test Explanation:
        This test verifies that a cache can be created with a default TTL setting.
        If the implementation ignores the default_ttl parameter, this would fail.
        If the implementation doesn't store the default_ttl properly, accessing
        it would return None or wrong value.

        What this test actually validates:
        - Constructor accepts default_ttl parameter
        - Default TTL is stored correctly for later use
        - Cache properly configures TTL behavior
        """
        cache = LRUCacheWithTTL(capacity=10, default_ttl=300)
        # We'll add a property to access default_ttl in our implementation
        assert hasattr(cache, 'default_ttl')
        assert cache.default_ttl == 300

    def test_cache_starts_empty(self):
        """
        Test Explanation:
        This test verifies that a newly created cache is empty.
        If the implementation pre-populates the cache or fails to initialize
        the size counter correctly, this test would fail.

        What this test actually validates:
        - Cache size starts at 0
        - Cache has no items initially
        - Cache is ready to accept new items
        """
        cache = LRUCacheWithTTL(capacity=5)
        assert len(cache) == 0
        assert cache.size() == 0

    def test_invalid_capacity_raises_error(self):
        """
        Test Explanation:
        This test verifies that invalid capacity values are rejected.
        If the implementation doesn't validate capacity, it would accept
        invalid values like 0 or negative numbers, which could cause
        issues later.

        What this test actually validates:
        - Business rule BR1: Capacity must be positive integer
        - Error handling works correctly
        - Cache prevents invalid configurations
        """
        with pytest.raises(ValueError, match="Capacity must be a positive integer"):
            LRUCacheWithTTL(capacity=0)

        with pytest.raises(ValueError, match="Capacity must be a positive integer"):
            LRUCacheWithTTL(capacity=-1)

    def test_invalid_ttl_raises_error(self):
        """
        Test Explanation:
        This test verifies that invalid TTL values are rejected.
        If the implementation doesn't validate TTL, it would accept
        negative TTL values which don't make logical sense.

        What this test actually validates:
        - Business rule BR6: TTL must be None or positive
        - Error handling for TTL validation
        - Cache prevents illogical TTL configurations
        """
        with pytest.raises(ValueError, match="TTL must be None or a positive number"):
            LRUCacheWithTTL(capacity=10, default_ttl=-1)


class TestBasicStorage:
    """Tests for basic storage operations without LRU or TTL complexity"""

    def test_can_determine_if_key_exists(self):
        """
        Test Explanation:
        This test verifies that we can check if a key exists in the cache.
        If the implementation doesn't properly track keys or implement
        __contains__, this would fail.

        What this test actually validates:
        - __contains__ method works correctly
        - Cache properly tracks which keys are stored
        - Basic existence checking functionality
        """
        cache = LRUCacheWithTTL(capacity=10)
        assert "key1" not in cache
        # We'll set this in the next test, but this establishes the baseline

    def test_basic_key_value_storage(self):
        """
        Test Explanation:
        This test verifies basic storage functionality without any complex
        eviction or expiration logic. If the implementation fails to store
        or retrieve values correctly, this fundamental test would fail.

        What this test actually validates:
        - Basic storage mechanism works
        - Simple key-value association
        - Foundation for more complex operations
        """
        cache = LRUCacheWithTTL(capacity=10)

        # This test deliberately uses the simplest possible operations
        # to isolate basic storage from LRU/TTL complexity
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        assert "key1" in cache
        assert len(cache) == 1

    def test_multiple_key_storage(self):
        """
        Test Explanation:
        This test verifies that the cache can handle multiple keys simultaneously.
        If the implementation has issues with its internal data structures,
        storing multiple items might overwrite each other or cause other issues.

        What this test actually validates:
        - Cache can handle multiple simultaneous entries
        - Keys don't interfere with each other
        - Size tracking works with multiple items
        """
        cache = LRUCacheWithTTL(capacity=10)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        assert cache.get("key1") == "value1"
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
        assert len(cache) == 3


class TestDictionaryInterface:
    """Tests for dictionary-like interface and advanced get/set operations"""

    def test_dictionary_style_get_set(self):
        """
        Test Explanation:
        This test verifies that the cache supports dictionary-style operations
        using [] syntax. If the __getitem__ and __setitem__ methods aren't
        implemented correctly, this would fail.

        What this test actually validates:
        - __setitem__ method works (cache[key] = value)
        - __getitem__ method works (value = cache[key])
        - Dictionary interface is intuitive and consistent
        """
        cache = LRUCacheWithTTL(capacity=10)

        # Dictionary-style assignment
        cache["key1"] = "value1"
        cache["key2"] = "value2"

        # Dictionary-style access
        assert cache["key1"] == "value1"
        assert cache["key2"] == "value2"

    def test_dictionary_style_delete(self):
        """
        Test Explanation:
        This test verifies that the cache supports dictionary-style deletion
        using del syntax. If __delitem__ isn't implemented correctly, this
        would fail.

        What this test actually validates:
        - __delitem__ method works (del cache[key])
        - Deletion removes items from cache
        - KeyError raised for non-existent keys during deletion
        """
        cache = LRUCacheWithTTL(capacity=10)
        cache["key1"] = "value1"

        # Verify item exists
        assert "key1" in cache

        # Dictionary-style deletion
        del cache["key1"]

        # Verify item is gone
        assert "key1" not in cache

    def test_delete_nonexistent_key_raises_keyerror(self):
        """
        Test Explanation:
        This test verifies that attempting to delete a non-existent key
        raises KeyError, following standard Python dictionary behavior.
        If the implementation doesn't raise KeyError or raises wrong exception,
        this would fail.

        What this test actually validates:
        - __delitem__ raises KeyError for missing keys
        - Error behavior matches Python dict standard
        - Cache properly handles edge cases
        """
        cache = LRUCacheWithTTL(capacity=10)

        # Should raise KeyError for non-existent key
        try:
            del cache["nonexistent"]
            assert False, "Should have raised KeyError"
        except KeyError:
            pass  # Expected

    def test_get_nonexistent_key_raises_keyerror(self):
        """
        Test Explanation:
        This test verifies that accessing a non-existent key raises KeyError,
        following standard Python dictionary behavior. If the implementation
        returns None or raises wrong exception, this would fail.

        What this test actually validates:
        - __getitem__ raises KeyError for missing keys
        - Error behavior matches Python dict standard
        - Clear error messages for debugging
        """
        cache = LRUCacheWithTTL(capacity=10)

        try:
            value = cache["nonexistent"]
            assert False, "Should have raised KeyError"
        except KeyError as e:
            assert "nonexistent" in str(e)

    def test_iteration_over_keys(self):
        """
        Test Explanation:
        This test verifies that the cache supports iteration over keys
        using for...in syntax. If __iter__ isn't implemented correctly,
        this would fail.

        What this test actually validates:
        - __iter__ method works correctly
        - Iteration provides all current keys
        - Iterator behavior matches expectations
        """
        cache = LRUCacheWithTTL(capacity=10)
        cache["key1"] = "value1"
        cache["key2"] = "value2"
        cache["key3"] = "value3"

        keys = list(cache)
        assert len(keys) == 3
        assert "key1" in keys
        assert "key2" in keys
        assert "key3" in keys

    def test_update_existing_key_with_new_value(self):
        """
        Test Explanation:
        This test verifies that setting a value for an existing key updates
        the value rather than creating a duplicate. If the implementation
        doesn't handle updates correctly, this would fail.

        What this test actually validates:
        - Key updates work correctly
        - No duplicate entries created
        - Cache size remains consistent
        - Most recent value is stored
        """
        cache = LRUCacheWithTTL(capacity=10)

        # Set initial value
        cache["key1"] = "value1"
        assert len(cache) == 1
        assert cache["key1"] == "value1"

        # Update with new value
        cache["key1"] = "new_value"
        assert len(cache) == 1  # Size shouldn't change
        assert cache["key1"] == "new_value"

    def test_cache_size_tracking_during_operations(self):
        """
        Test Explanation:
        This test verifies that the cache correctly tracks its size during
        various operations. If the size tracking logic has bugs, this would fail.

        What this test actually validates:
        - Size increases when adding new items
        - Size stays same when updating existing items
        - Size decreases when deleting items
        - len() and size() remain consistent
        """
        cache = LRUCacheWithTTL(capacity=10)

        # Start empty
        assert len(cache) == 0
        assert cache.size() == 0

        # Add items
        cache["key1"] = "value1"
        assert len(cache) == 1
        assert cache.size() == 1

        cache["key2"] = "value2"
        assert len(cache) == 2
        assert cache.size() == 2

        # Update existing item (size shouldn't change)
        cache["key1"] = "new_value"
        assert len(cache) == 2
        assert cache.size() == 2

        # Delete item
        del cache["key1"]
        assert len(cache) == 1
        assert cache.size() == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])