"""
Test validation script to demonstrate our tests catch real bugs
This runs our tests against the deliberately broken implementation
"""

import sys
import traceback
from lru_cache_ttl import LRUCacheWithTTL


def test_cache_initialization_with_capacity():
    """Should FAIL: Implementation returns wrong capacity"""
    try:
        cache = LRUCacheWithTTL(capacity=10)
        assert cache.capacity == 10
        print("❌ UNEXPECTED PASS: test_cache_initialization_with_capacity")
        return False
    except AssertionError:
        print("✅ EXPECTED FAIL: test_cache_initialization_with_capacity - caught capacity bug")
        return True
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: test_cache_initialization_with_capacity - {e}")
        return False


def test_cache_starts_empty():
    """Should FAIL: Implementation starts with wrong size"""
    try:
        cache = LRUCacheWithTTL(capacity=5)
        assert len(cache) == 0
        assert cache.size() == 0
        print("❌ UNEXPECTED PASS: test_cache_starts_empty")
        return False
    except AssertionError:
        print("✅ EXPECTED FAIL: test_cache_starts_empty - caught size initialization bug")
        return True
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: test_cache_starts_empty - {e}")
        return False


def test_invalid_capacity_raises_error():
    """Should FAIL: Implementation doesn't validate negative capacity"""
    try:
        # This should pass (implementation does check for 0)
        try:
            LRUCacheWithTTL(capacity=0)
            print("❌ UNEXPECTED PASS: test_invalid_capacity_raises_error (capacity=0)")
            return False
        except ValueError:
            pass  # Expected

        # This should fail (implementation doesn't check negative)
        try:
            LRUCacheWithTTL(capacity=-1)
            print("✅ EXPECTED FAIL: test_invalid_capacity_raises_error - caught negative capacity bug")
            return True
        except ValueError:
            print("❌ UNEXPECTED PASS: test_invalid_capacity_raises_error (capacity=-1)")
            return False

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: test_invalid_capacity_raises_error - {e}")
        return False


def test_invalid_ttl_raises_error():
    """Should FAIL: Implementation doesn't validate TTL at all"""
    try:
        LRUCacheWithTTL(capacity=10, default_ttl=-1)
        print("✅ EXPECTED FAIL: test_invalid_ttl_raises_error - caught TTL validation bug")
        return True
    except ValueError:
        print("❌ UNEXPECTED PASS: test_invalid_ttl_raises_error")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: test_invalid_ttl_raises_error - {e}")
        return False


def test_can_determine_if_key_exists():
    """Should FAIL: Implementation has inverted containment logic"""
    try:
        cache = LRUCacheWithTTL(capacity=10)
        assert "key1" not in cache
        print("❌ UNEXPECTED PASS: test_can_determine_if_key_exists")
        return False
    except AssertionError:
        print("✅ EXPECTED FAIL: test_can_determine_if_key_exists - caught containment bug")
        return True
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: test_can_determine_if_key_exists - {e}")
        return False


def test_basic_key_value_storage():
    """Should FAIL: Implementation doesn't store values and returns wrong values"""
    try:
        cache = LRUCacheWithTTL(capacity=10)
        cache.set("key1", "value1")
        result = cache.get("key1")
        assert result == "value1"
        print("❌ UNEXPECTED PASS: test_basic_key_value_storage")
        return False
    except AssertionError:
        print("✅ EXPECTED FAIL: test_basic_key_value_storage - caught storage/retrieval bug")
        return True
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: test_basic_key_value_storage - {e}")
        return False


def main():
    """Run all test validations and report results"""
    print("=== TEST VALIDATION: Verifying our tests catch real bugs ===\n")

    tests = [
        test_cache_initialization_with_capacity,
        test_cache_starts_empty,
        test_invalid_capacity_raises_error,
        test_invalid_ttl_raises_error,
        test_can_determine_if_key_exists,
        test_basic_key_value_storage,
    ]

    passed_validations = 0
    total_tests = len(tests)

    for test_func in tests:
        if test_func():
            passed_validations += 1
        print()

    print(f"=== VALIDATION SUMMARY ===")
    print(f"Tests that correctly caught bugs: {passed_validations}/{total_tests}")

    if passed_validations == total_tests:
        print("✅ ALL TESTS VALIDATED: Our tests correctly catch the intended bugs!")
        print("✅ Tests are well-designed and will catch real implementation errors.")
    else:
        print("❌ SOME TESTS FAILED VALIDATION: Some tests may not be testing what they claim.")
        print("❌ Review and improve test design before proceeding.")

    return passed_validations == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)