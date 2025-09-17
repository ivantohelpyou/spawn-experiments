"""
TDD Cycle 4: Unicode Search
RED phase - write failing tests for search functionality
"""

import unittest
from password_entry import PasswordEntry
from password_store import PasswordStore

class TestUnicodeSearch(unittest.TestCase):
    """TDD Cycle 4: Unicode-aware search"""

    def setUp(self):
        """Set up test data"""
        self.store = PasswordStore()

        # Add test entries with various Unicode
        entries = [
            PasswordEntry("📧 Gmail", "user@gmail.com", "pass1"),
            PasswordEntry("🏦 Bank of América", "john", "pass2"),
            PasswordEntry("💻 GitHub", "developer", "pass3"),
            PasswordEntry("Café WiFi", "guest", "pass4"),
            PasswordEntry("München Office", "admin", "pass5"),
        ]

        for entry in entries:
            self.store.add(entry)

    def test_search_emoji_tolerant(self):
        """RED: Search 'gmail' should find '📧 Gmail'"""
        results = self.store.search("gmail")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "📧 Gmail")

    def test_search_diacritic_tolerant(self):
        """RED: Search 'cafe' should find 'Café WiFi'"""
        results = self.store.search("cafe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "Café WiFi")

    def test_search_case_insensitive(self):
        """RED: Search 'GITHUB' should find '💻 GitHub'"""
        results = self.store.search("GITHUB")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "💻 GitHub")

    def test_search_partial_match(self):
        """RED: Search 'bank' should find 'Bank of América'"""
        results = self.store.search("bank")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "🏦 Bank of América")

    def test_search_unicode_normalization(self):
        """RED: Search with different Unicode forms should work"""
        # Search with decomposed characters
        results = self.store.search("munchen")  # should find München
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "München Office")

if __name__ == '__main__':
    unittest.main()