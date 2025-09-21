#!/usr/bin/env python3
"""
TDD demonstration for Unicode password manager
Following Red-Green-Refactor cycles
"""

# TDD Cycle 2: Test Unicode normalization (RED)
def test_unicode_normalization():
    """Test that should fail - PasswordEntry doesn't have normalized_service yet"""
    try:
        from password_entry import PasswordEntry

        # café with composed é
        entry1 = PasswordEntry(
            service="café",
            username="user1",
            password="password1"
        )

        # café with decomposed e + ´
        entry2 = PasswordEntry(
            service="cafe´",  # This is e + combining acute accent
            username="user2",
            password="password2"
        )

        # This should fail because normalized_service doesn't exist yet
        assert entry1.normalized_service == entry2.normalized_service
        print("❌ Test should have failed but passed!")

    except AttributeError as e:
        print(f"✅ RED: Test failed as expected - {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

    return True

# Run RED phase
print("=== TDD Cycle 2: Unicode Normalization ===")
print("RED Phase: Running failing test...")
test_unicode_normalization()

print("\nNow implementing GREEN phase...")

# GREEN: Add minimal code to make test pass
print("Adding normalized_service property to PasswordEntry...")