"""
Password store implementation - evolved through TDD cycles
TDD Cycle 3: Basic storage
TDD Cycle 4: Unicode search
"""

import unicodedata
from typing import Dict, Optional, List
from password_entry import PasswordEntry

class PasswordStore:
    """Password store with Unicode-aware search (TDD Cycles 3-4)"""

    def __init__(self):
        self.entries: Dict[str, PasswordEntry] = {}

    def add(self, entry: PasswordEntry):
        """Add a password entry using service name as key"""
        self.entries[entry.service] = entry

    def get(self, service_name: str) -> Optional[PasswordEntry]:
        """Get password entry by exact service name match"""
        return self.entries.get(service_name)

    def get_normalized(self, service_name: str) -> Optional[PasswordEntry]:
        """Get password entry using Unicode normalization"""
        normalized_search = unicodedata.normalize('NFC', service_name)

        for entry in self.entries.values():
            if entry.normalized_service == normalized_search:
                return entry

        return None

    def search(self, query: str) -> List[PasswordEntry]:
        """
        Unicode-aware search (TDD Cycle 4)
        Handles emoji, diacritics, and case sensitivity
        """
        if not query.strip():
            return []

        # Normalize and prepare query for matching
        normalized_query = self._normalize_for_search(query)
        results = []

        for entry in self.entries.values():
            if self._matches_entry(normalized_query, entry):
                results.append(entry)

        return results

    def _normalize_for_search(self, text: str) -> str:
        """Normalize text for search comparison"""
        # Step 1: Unicode normalization
        normalized = unicodedata.normalize('NFC', text)

        # Step 2: Case folding for case-insensitive search
        case_folded = normalized.casefold()

        # Step 3: Remove diacritics for broader matching
        without_diacritics = self._remove_diacritics(case_folded)

        return without_diacritics

    def _remove_diacritics(self, text: str) -> str:
        """Remove diacritical marks for broader search matching"""
        # Decompose to separate base characters from combining marks
        decomposed = unicodedata.normalize('NFD', text)

        # Remove combining marks (diacritics)
        without_marks = ''.join(
            char for char in decomposed
            if unicodedata.category(char) != 'Mn'  # Mn = Nonspacing_Mark
        )

        return without_marks

    def _matches_entry(self, normalized_query: str, entry: PasswordEntry) -> bool:
        """Check if an entry matches the search query"""
        # Normalize service name for comparison
        normalized_service = self._normalize_for_search(entry.service)

        # Basic substring match
        if normalized_query in normalized_service:
            return True

        # Also check alphanumeric-only version for emoji tolerance
        query_alpha = self._extract_alphanumeric(normalized_query)
        service_alpha = self._extract_alphanumeric(normalized_service)

        if query_alpha and service_alpha and query_alpha in service_alpha:
            return True

        return False

    def _extract_alphanumeric(self, text: str) -> str:
        """Extract only alphanumeric characters for emoji-tolerant search"""
        # Keep only letters and numbers
        alphanumeric = ''.join(
            char for char in text
            if unicodedata.category(char)[0] in 'LN'  # Letter or Number
        )
        return alphanumeric.lower()