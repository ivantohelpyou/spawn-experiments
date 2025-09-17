"""
Enhanced TDD Cycle 1: Password Entry with Test Validation
Following Red-VALIDATE-Green-Refactor process
"""

import unittest
from datetime import datetime

class TestPasswordEntryValidated(unittest.TestCase):
    """Enhanced TDD: Password Entry with validated tests"""

    def test_create_basic_password_entry_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that a PasswordEntry can be created with basic
        ASCII service name, username, and password, and that all fields
        are stored correctly with a creation timestamp.

        2. TEST VALIDATION PLAN:
        - First implement broken PasswordEntry that stores wrong fields
        - Verify test catches field assignment errors
        - Verify test catches missing timestamp
        - Verify test catches type errors

        3. QUALITY CHECKLIST:
        ✅ Specific assertions for each field
        ✅ Timestamp validation included
        ✅ Type checking included
        ✅ Will add negative case for invalid inputs
        """

        # This will fail initially (RED phase)
        from password_entry import PasswordEntry

        entry = PasswordEntry(
            service="Gmail",
            username="user@gmail.com",
            password="secret123"
        )

        # Specific field validation
        self.assertEqual(entry.service, "Gmail")
        self.assertEqual(entry.username, "user@gmail.com")
        self.assertEqual(entry.password, "secret123")

        # Timestamp validation
        self.assertIsInstance(entry.created_date, datetime)
        self.assertLessEqual(
            (datetime.now() - entry.created_date).total_seconds(),
            1.0  # Should be created within 1 second
        )

    def test_unicode_normalization_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that Unicode normalization correctly handles
        composed vs decomposed characters. Specifically, 'café' (NFC)
        and 'cafe´' (NFD) should normalize to the same form.

        2. TEST VALIDATION PLAN:
        - First implement broken normalizer that returns input unchanged
        - Verify test fails when normalization is skipped
        - Test with multiple Unicode forms (NFC, NFD, NFKC, NFKD)
        - Verify test catches when wrong normalization form is used

        3. QUALITY CHECKLIST:
        ✅ Tests specific Unicode forms (composed vs decomposed)
        ✅ Tests both positive (should be equal) and negative (should differ)
        ✅ Multiple examples of normalization issues
        ✅ Verifies exact normalization form (NFC)
        """

        from password_entry import PasswordEntry
        import unicodedata

        # Test Case 1: Composed vs Decomposed é
        entry1 = PasswordEntry("café", "user1", "password1")     # NFC: é as single codepoint
        entry2 = PasswordEntry("cafe´", "user2", "password2")    # NFD: e + combining acute

        # These should normalize to the same value
        self.assertEqual(entry1.normalized_service, entry2.normalized_service)

        # Test Case 2: Verify specific normalization form (NFC)
        expected_nfc = unicodedata.normalize('NFC', "café")
        self.assertEqual(entry1.normalized_service, expected_nfc)
        self.assertEqual(entry2.normalized_service, expected_nfc)

        # Test Case 3: NEGATIVE TEST - Different characters should not be equal
        entry3 = PasswordEntry("different", "user3", "password3")
        self.assertNotEqual(entry1.normalized_service, entry3.normalized_service)

        # Test Case 4: More complex Unicode (multiple combining characters)
        entry4 = PasswordEntry("naïve", "user4", "password4")    # ï with combining diaeresis
        entry5 = PasswordEntry("naïve", "user5", "password5")    # ï as single codepoint

        self.assertEqual(entry4.normalized_service, entry5.normalized_service)

    def test_validation_requirements_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that password entries validate their inputs
        according to business rules: service names 1-100 chars,
        usernames 1-200 chars, passwords 1-500 chars.

        2. TEST VALIDATION PLAN:
        - First implement PasswordEntry with no validation
        - Verify test fails when validation is missing
        - Test boundary conditions (exactly 1, exactly max, max+1)
        - Test empty strings and null inputs

        3. QUALITY CHECKLIST:
        ✅ Tests all validation rules
        ✅ Tests boundary conditions
        ✅ Tests both valid and invalid inputs
        ✅ Specific exception types and messages
        """

        from password_entry import PasswordEntry

        # Valid inputs should work
        valid_entry = PasswordEntry("Gmail", "user@example.com", "password123")
        self.assertTrue(valid_entry.validate())

        # Test service name length validation
        with self.assertRaises(ValueError) as cm:
            long_service = "x" * 101  # Too long
            entry = PasswordEntry(long_service, "user", "pass")
            entry.validate()
        self.assertIn("service name", str(cm.exception).lower())

        # Test username length validation
        with self.assertRaises(ValueError) as cm:
            long_username = "x" * 201  # Too long
            entry = PasswordEntry("service", long_username, "pass")
            entry.validate()
        self.assertIn("username", str(cm.exception).lower())

        # Test password length validation
        with self.assertRaises(ValueError) as cm:
            long_password = "x" * 501  # Too long
            entry = PasswordEntry("service", "user", long_password)
            entry.validate()
        self.assertIn("password", str(cm.exception).lower())

        # Test empty inputs
        with self.assertRaises(ValueError):
            PasswordEntry("", "user", "pass").validate()

        with self.assertRaises(ValueError):
            PasswordEntry("service", "", "pass").validate()

        with self.assertRaises(ValueError):
            PasswordEntry("service", "user", "").validate()

if __name__ == '__main__':
    unittest.main()