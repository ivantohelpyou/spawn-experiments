"""
TDD Cycle 3: Password Storage
RED phase - write failing tests first
"""

import unittest
from password_entry import PasswordEntry

class TestPasswordStore(unittest.TestCase):
    """TDD Cycle 3: Basic password storage"""

    def test_store_and_retrieve_password(self):
        """RED: Store and retrieve a password entry"""
        from password_store import PasswordStore

        store = PasswordStore()
        entry = PasswordEntry(
            service="Gmail",
            username="user@gmail.com",
            password="secret123"
        )

        store.add(entry)
        retrieved = store.get("Gmail")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.service, "Gmail")
        self.assertEqual(retrieved.username, "user@gmail.com")

    def test_store_unicode_service_names(self):
        """RED: Store entries with Unicode service names"""
        from password_store import PasswordStore

        store = PasswordStore()
        entry = PasswordEntry(
            service="📧 Gmail",
            username="user@gmail.com",
            password="café🔐123"
        )

        store.add(entry)
        retrieved = store.get("📧 Gmail")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.service, "📧 Gmail")
        self.assertEqual(retrieved.password, "café🔐123")

    def test_normalize_service_lookup(self):
        """RED: Find entry using normalized service name"""
        from password_store import PasswordStore

        store = PasswordStore()

        # Store with composed é
        entry = PasswordEntry(
            service="café",
            username="user",
            password="password"
        )
        store.add(entry)

        # Retrieve with decomposed e + ´
        retrieved = store.get_normalized("cafe´")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.normalized_service, "café")

if __name__ == '__main__':
    unittest.main()