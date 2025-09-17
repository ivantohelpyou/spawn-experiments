"""
Enhanced TDD Cycle 2: Advanced Unicode Search with Test Validation
Testing the tests to ensure they catch realistic search bugs
"""

import unittest
from password_entry import PasswordEntry

class TestUnicodeSearchValidated(unittest.TestCase):
    """Enhanced TDD: Unicode search with validated tests"""

    def setUp(self):
        """Set up test data with diverse Unicode content"""
        self.entries = [
            PasswordEntry("📧 Gmail Account", "user@gmail.com", "pass1"),
            PasswordEntry("🏦 Bank of América", "john.doe", "pass2"),
            PasswordEntry("💻 GitHub Repository", "developer", "pass3"),
            PasswordEntry("Café WiFi Network", "guest", "pass4"),
            PasswordEntry("München Office VPN", "admin", "pass5"),
            PasswordEntry("北京办公室", "beijing_user", "pass6"),  # Chinese
            PasswordEntry("Москва Сервер", "moscow_admin", "pass7"),  # Cyrillic
            PasswordEntry("naïve-system", "naive_user", "pass8"),  # Combining characters
        ]

    def test_emoji_tolerant_search_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that searching for "gmail" finds "📧 Gmail Account"
        even though the service name contains emoji. This requires emoji-tolerant
        search that can extract alphanumeric content.

        2. TEST VALIDATION PLAN:
        - First implement search that only does exact string matching
        - Verify test fails when emoji breaks search
        - Test with various emoji positions (start, middle, end)
        - Verify search doesn't match unrelated emoji services

        3. QUALITY CHECKLIST:
        ✅ Tests specific emoji-tolerance behavior
        ✅ Multiple emoji positions tested
        ✅ Negative cases (shouldn't match unrelated items)
        ✅ Case sensitivity handling
        """
        from password_store import PasswordStore

        store = PasswordStore()
        for entry in self.entries:
            store.add(entry)

        # Primary test: "gmail" should find "📧 Gmail Account"
        results = store.search("gmail")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "📧 Gmail Account")

        # Case insensitive: "GMAIL" should also work
        results = store.search("GMAIL")
        self.assertEqual(len(results), 1)

        # Partial match: "git" should find "💻 GitHub Repository"
        results = store.search("git")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "💻 GitHub Repository")

        # NEGATIVE TEST: "xyz" should not find anything
        results = store.search("xyz")
        self.assertEqual(len(results), 0)

        # NEGATIVE TEST: Empty query should return nothing
        results = store.search("")
        self.assertEqual(len(results), 0)

    def test_diacritic_insensitive_search_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that diacritics (accents) don't prevent matches.
        "cafe" should find "Café WiFi Network" and "america" should find
        "Bank of América". This requires diacritic removal.

        2. TEST VALIDATION PLAN:
        - First implement search without diacritic removal
        - Verify test fails when accents prevent matching
        - Test various diacritic types (acute, grave, umlaut, etc.)
        - Test composed vs decomposed diacritics

        3. QUALITY CHECKLIST:
        ✅ Multiple diacritic types (á, é, ü, ñ, etc.)
        ✅ Both composed and decomposed forms
        ✅ Case insensitive with diacritics
        ✅ Partial matching with diacritics
        """
        from password_store import PasswordStore

        store = PasswordStore()
        for entry in self.entries:
            store.add(entry)

        # Diacritic removal: "cafe" should find "Café WiFi Network"
        results = store.search("cafe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "Café WiFi Network")

        # Diacritic removal: "america" should find "Bank of América"
        results = store.search("america")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "🏦 Bank of América")

        # Diacritic removal: "munchen" should find "München Office VPN"
        results = store.search("munchen")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "München Office VPN")

        # Complex case: "naive" should find "naïve-system"
        results = store.search("naive")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "naïve-system")

        # REVERSE TEST: Searching with diacritics should work too
        results = store.search("café")
        self.assertEqual(len(results), 1)

    def test_script_aware_search_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that search works across different writing systems
        (Latin, Cyrillic, Chinese) and can handle transliteration or
        script-specific search behavior.

        2. TEST VALIDATION PLAN:
        - First implement search that only handles ASCII
        - Verify test fails with non-Latin scripts
        - Test exact script matching works
        - Consider transliteration needs

        3. QUALITY CHECKLIST:
        ✅ Multiple writing systems (Latin, Cyrillic, CJK)
        ✅ Exact matching within scripts
        ✅ Case handling for non-Latin scripts
        ✅ Mixed script content handling
        """
        from password_store import PasswordStore

        store = PasswordStore()
        for entry in self.entries:
            store.add(entry)

        # Chinese search: exact match should work
        results = store.search("北京")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "北京办公室")

        # Cyrillic search: exact match should work
        results = store.search("Москва")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].service, "Москва Сервер")

        # Partial Cyrillic search
        results = store.search("Сервер")
        self.assertEqual(len(results), 1)

        # NEGATIVE TEST: Latin "moscow" should not find Cyrillic "Москва"
        # (unless transliteration is implemented)
        results = store.search("moscow")
        self.assertEqual(len(results), 0)

    def test_search_ranking_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that search results are ranked by relevance:
        exact matches first, then starts-with, then contains.

        2. TEST VALIDATION PLAN:
        - First implement search with random result order
        - Verify test fails when ranking is wrong
        - Test tie-breaking behavior
        - Test ranking with Unicode normalization

        3. QUALITY CHECKLIST:
        ✅ Multiple services that match the same query
        ✅ Clear ranking criteria (exact > starts-with > contains)
        ✅ Consistent ordering
        ✅ Unicode-aware ranking
        """
        from password_store import PasswordStore

        store = PasswordStore()

        # Add entries that will match "office" in different ways
        office_entries = [
            PasswordEntry("office", "exact_match", "pass1"),  # Exact match - should be first
            PasswordEntry("Office Building", "starts_with", "pass2"),  # Starts with - should be second
            PasswordEntry("München Office VPN", "contains", "pass3"),  # Contains - should be third
        ]

        for entry in office_entries:
            store.add(entry)

        results = store.search("office")

        # Should find all three
        self.assertEqual(len(results), 3)

        # Check ranking order
        services = [result.service for result in results]
        self.assertEqual(services[0], "office")  # Exact match first
        self.assertTrue("Office Building" in services[:2])  # Starts-with in top 2
        self.assertEqual(services[2], "München Office VPN")  # Contains last

    def test_fuzzy_search_validated(self):
        """
        ENHANCED TDD TEST with VALIDATION

        1. EXPLAIN:
        This test verifies that fuzzy search can find matches even with
        typos, using edit distance or similar algorithms.

        2. TEST VALIDATION PLAN:
        - First implement exact-match-only search
        - Verify test fails with typos
        - Test various typo types (substitution, insertion, deletion)
        - Test edit distance limits

        3. QUALITY CHECKLIST:
        ✅ Common typo patterns
        ✅ Edit distance limits (1-2 character differences)
        ✅ Unicode-aware fuzzy matching
        ✅ Performance with fuzzy search
        """
        from password_store import PasswordStore

        store = PasswordStore()
        for entry in self.entries:
            store.add(entry)

        # Typo tolerance: "gmial" should find "Gmail"
        results = store.fuzzy_search("gmial", max_distance=2)
        self.assertGreater(len(results), 0)
        gmail_found = any("Gmail" in result.service for result in results)
        self.assertTrue(gmail_found)

        # Single character substitution: "Githib" -> "GitHub"
        results = store.fuzzy_search("githib", max_distance=1)
        github_found = any("GitHub" in result.service for result in results)
        self.assertTrue(github_found)

        # Insertion error: "Bnak" -> "Bank"
        results = store.fuzzy_search("bnak", max_distance=2)
        bank_found = any("Bank" in result.service for result in results)
        self.assertTrue(bank_found)

if __name__ == '__main__':
    unittest.main()