"""
Test-driven development for Unicode password manager
Starting with the most basic functionality
"""

import unittest
from datetime import datetime

class TestPasswordEntry(unittest.TestCase):
    """Test password entry basic functionality"""

    def test_create_basic_password_entry(self):
        """RED: Create a basic password entry with Unicode"""
        # This test will fail because PasswordEntry doesn't exist yet
        from password_entry import PasswordEntry

        entry = PasswordEntry(
            service="Gmail",
            username="user@gmail.com",
            password="secret123"
        )

        self.assertEqual(entry.service, "Gmail")
        self.assertEqual(entry.username, "user@gmail.com")
        self.assertEqual(entry.password, "secret123")
        self.assertIsInstance(entry.created_date, datetime)

    def test_create_unicode_password_entry(self):
        """RED: Unicode characters in service name"""
        from password_entry import PasswordEntry

        entry = PasswordEntry(
            service="📧 Gmail",
            username="user@gmail.com",
            password="café🔐123"
        )

        self.assertEqual(entry.service, "📧 Gmail")
        self.assertEqual(entry.password, "café🔐123")

    def test_unicode_normalization(self):
        """RED: Unicode normalization should make composed and decomposed equal"""
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

        # After normalization, these should be equal
        self.assertEqual(entry1.normalized_service, entry2.normalized_service)

if __name__ == '__main__':
    unittest.main()