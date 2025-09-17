"""
Unicode-aware search engine for password entries
Implements SPEC-1.4 search requirements
"""

import unicodedata
from typing import List, Dict
import re
from password_entry import PasswordEntry

class SearchEngine:
    """
    Unicode-aware search functionality for password entries
    Implements SPEC-1.4.1 through SPEC-1.4.4
    """

    def __init__(self):
        self.entries: Dict[str, PasswordEntry] = {}

    def set_entries(self, entries: Dict[str, PasswordEntry]):
        """Set the entries to search through"""
        self.entries = entries

    def search(self, query: str) -> List[str]:
        """
        Search password entries with Unicode-aware matching
        Implements SPEC-1.4 requirements
        """
        if not query.strip():
            return []

        # Normalize query for consistent comparison (SPEC-1.4.4)
        normalized_query = self._normalize_for_search(query)

        results = []

        for service_name, entry in self.entries.items():
            if self._matches_service(normalized_query, service_name, entry):
                results.append(service_name)

        # Sort results by relevance
        return self._sort_by_relevance(results, query)

    def _normalize_for_search(self, text: str) -> str:
        """
        Normalize text for search comparison
        Implements SPEC-1.4.4 Unicode-aware search
        """
        # Normalize to NFC first
        normalized = unicodedata.normalize('NFC', text)

        # Case fold for case-insensitive search (SPEC-1.4.3)
        # This handles Unicode case folding properly
        case_folded = normalized.casefold()

        # Remove diacritics for broader matching
        # This allows "cafe" to match "café"
        without_diacritics = self._remove_diacritics(case_folded)

        return without_diacritics

    def _remove_diacritics(self, text: str) -> str:
        """
        Remove diacritical marks for broader search matching
        Allows "cafe" to match "café"
        """
        # Decompose to separate base characters from combining marks
        decomposed = unicodedata.normalize('NFD', text)

        # Remove combining marks (diacritics)
        without_marks = ''.join(
            char for char in decomposed
            if unicodedata.category(char) != 'Mn'  # Mn = Nonspacing_Mark
        )

        return without_marks

    def _matches_service(self, normalized_query: str, service_name: str, entry: PasswordEntry) -> bool:
        """
        Check if an entry matches the search query
        Implements partial string matching (SPEC-1.4.2)
        """
        # Normalize service name for comparison
        normalized_service = self._normalize_for_search(service_name)

        # Basic substring match
        if normalized_query in normalized_service:
            return True

        # Also search in username (bonus feature)
        normalized_username = self._normalize_for_search(entry.username)
        if normalized_query in normalized_username:
            return True

        # Search in category if present
        if entry.category:
            normalized_category = self._normalize_for_search(entry.category)
            if normalized_query in normalized_category:
                return True

        # Handle emoji/symbol removal for broader matching
        # Remove emoji and symbols from both query and service name
        query_alphanumeric = self._extract_alphanumeric(normalized_query)
        service_alphanumeric = self._extract_alphanumeric(normalized_service)

        if query_alphanumeric and service_alphanumeric:
            if query_alphanumeric in service_alphanumeric:
                return True

        return False

    def _extract_alphanumeric(self, text: str) -> str:
        """
        Extract only alphanumeric characters for emoji-tolerant search
        Allows "gmail" to match "📧 Gmail"
        """
        # Keep only letters and numbers
        alphanumeric = ''.join(
            char for char in text
            if unicodedata.category(char)[0] in 'LN'  # Letter or Number
        )
        return alphanumeric.lower()

    def _sort_by_relevance(self, results: List[str], original_query: str) -> List[str]:
        """
        Sort search results by relevance
        Exact matches first, then partial matches
        """
        if not results:
            return results

        normalized_query = self._normalize_for_search(original_query)

        def relevance_score(service_name: str) -> tuple:
            normalized_service = self._normalize_for_search(service_name)

            # Exact match gets highest score
            if normalized_query == normalized_service:
                return (0, 0)

            # Starts with query gets second highest
            if normalized_service.startswith(normalized_query):
                return (1, len(service_name))

            # Contains query gets third
            if normalized_query in normalized_service:
                return (2, len(service_name))

            # Alphanumeric match gets lowest
            return (3, len(service_name))

        return sorted(results, key=relevance_score)

    def fuzzy_search(self, query: str, max_distance: int = 2) -> List[str]:
        """
        Fuzzy search using edit distance
        Bonus feature for typo tolerance
        """
        if not query.strip():
            return []

        normalized_query = self._normalize_for_search(query)
        results = []

        for service_name in self.entries.keys():
            normalized_service = self._normalize_for_search(service_name)

            # Calculate Levenshtein distance
            distance = self._levenshtein_distance(normalized_query, normalized_service)

            # Also check alphanumeric version
            query_alpha = self._extract_alphanumeric(normalized_query)
            service_alpha = self._extract_alphanumeric(normalized_service)

            if query_alpha and service_alpha:
                alpha_distance = self._levenshtein_distance(query_alpha, service_alpha)
                distance = min(distance, alpha_distance)

            if distance <= max_distance:
                results.append((service_name, distance))

        # Sort by distance (closer matches first)
        results.sort(key=lambda x: x[1])
        return [service_name for service_name, _ in results]

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein (edit) distance between two strings
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """
        Get search suggestions based on partial input
        Useful for autocomplete functionality
        """
        if not partial_query.strip():
            return []

        normalized_partial = self._normalize_for_search(partial_query)
        suggestions = []

        for service_name in self.entries.keys():
            normalized_service = self._normalize_for_search(service_name)

            if normalized_service.startswith(normalized_partial):
                suggestions.append(service_name)

        # Also check alphanumeric matching
        partial_alpha = self._extract_alphanumeric(normalized_partial)
        if partial_alpha:
            for service_name in self.entries.keys():
                service_alpha = self._extract_alphanumeric(service_name)
                if service_alpha.startswith(partial_alpha) and service_name not in suggestions:
                    suggestions.append(service_name)

        return sorted(suggestions, key=len)  # Shorter names first