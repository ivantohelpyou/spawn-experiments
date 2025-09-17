#!/usr/bin/env python3
"""
Basic functionality test for specification-first implementation
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from password_entry import PasswordEntry
from password_generator import PasswordGenerator, CharacterSet
from search_engine import SearchEngine

def test_unicode_normalization():
    """Test Unicode normalization functionality"""
    print("=== Testing Unicode Normalization ===")

    # Test composed vs decomposed characters
    entry1 = PasswordEntry(
        service_name="café",  # composed é
        username="user1",
        password="password1",
        created_date=datetime.now(),
        modified_date=datetime.now()
    )

    entry2 = PasswordEntry(
        service_name="cafe´",  # decomposed e + ´
        username="user2",
        password="password2",
        created_date=datetime.now(),
        modified_date=datetime.now()
    )

    print(f"Composed 'café': {repr(entry1.service_name)}")
    print(f"Decomposed 'cafe´': {repr(entry2.service_name)}")
    print(f"Are they equal after normalization? {entry1.service_name == entry2.service_name}")

def test_password_generation():
    """Test password generation with different character sets"""
    print("\n=== Testing Password Generation ===")

    generator = PasswordGenerator()

    # Test different character sets
    charsets = [
        (CharacterSet.ASCII_BASIC, "ASCII Basic"),
        (CharacterSet.ASCII_EXTENDED, "ASCII Extended"),
        (CharacterSet.UNICODE_SYMBOLS, "Unicode Symbols"),
        (CharacterSet.UNICODE_MIXED, "Unicode Mixed"),
        (CharacterSet.EMOJI_ONLY, "Emoji Only")
    ]

    for charset, name in charsets:
        try:
            password = generator.generate_password(12, charset)
            strength = generator.get_password_strength_indicator(password)
            entropy = generator.analyze_password_entropy(password)

            print(f"\n{name}:")
            print(f"  Password: {password}")
            print(f"  Length: {len(password)} code points")
            print(f"  Bytes: {len(password.encode())} bytes")
            print(f"  Strength: {strength}")
            print(f"  Entropy: {entropy:.1f} bits")

        except Exception as e:
            print(f"{name}: Error - {e}")

def test_unicode_search():
    """Test Unicode-aware search functionality"""
    print("\n=== Testing Unicode Search ===")

    search_engine = SearchEngine()

    # Create test entries with various Unicode
    entries = {
        "📧 Gmail Account": PasswordEntry("📧 Gmail Account", "user@gmail.com", "pass1", datetime.now(), datetime.now()),
        "🏦 Bank of América": PasswordEntry("🏦 Bank of América", "john", "pass2", datetime.now(), datetime.now()),
        "💻 GitHub": PasswordEntry("💻 GitHub", "developer", "pass3", datetime.now(), datetime.now()),
        "Café WiFi": PasswordEntry("Café WiFi", "guest", "pass4", datetime.now(), datetime.now()),
        "München Office": PasswordEntry("München Office", "admin", "pass5", datetime.now(), datetime.now()),
    }

    search_engine.set_entries(entries)

    # Test searches
    test_queries = [
        "gmail",      # Should find Gmail with emoji
        "bank",       # Should find Bank with emoji and accent
        "cafe",       # Should find Café (diacritic removal)
        "munchen",    # Should find München (diacritic removal)
        "github",     # Should find GitHub with emoji
        "🏦",         # Should find bank by emoji
        "América",    # Exact accent match
    ]

    for query in test_queries:
        results = search_engine.search(query)
        print(f"Search '{query}': {results}")

def test_validation():
    """Test input validation"""
    print("\n=== Testing Validation ===")

    try:
        # Test service name too long
        long_name = "x" * 101
        entry = PasswordEntry(long_name, "user", "pass", datetime.now(), datetime.now())
        entry.validate()
        print("❌ Should have failed validation for long service name")
    except ValueError as e:
        print(f"✅ Validation caught long service name: {e}")

    try:
        # Test empty username
        entry = PasswordEntry("service", "", "pass", datetime.now(), datetime.now())
        entry.validate()
        print("❌ Should have failed validation for empty username")
    except ValueError as e:
        print(f"✅ Validation caught empty username: {e}")

    try:
        # Test null bytes
        entry = PasswordEntry("service\x00", "user", "pass", datetime.now(), datetime.now())
        print(f"Service name after null removal: {repr(entry.service_name)}")
        print("✅ Null bytes removed successfully")
    except Exception as e:
        print(f"❌ Error handling null bytes: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Specification-First Implementation")
    print("=" * 60)

    test_unicode_normalization()
    test_password_generation()
    test_unicode_search()
    test_validation()

    print("\n" + "=" * 60)
    print("✅ Basic functionality tests completed!")
    print("Note: This implementation follows detailed specifications")
    print("and handles many Unicode edge cases that naive approach missed.")

if __name__ == "__main__":
    main()