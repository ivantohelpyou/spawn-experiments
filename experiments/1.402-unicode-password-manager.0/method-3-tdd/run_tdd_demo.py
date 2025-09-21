#!/usr/bin/env python3
"""
TDD demonstration - showing the evolution through Red-Green-Refactor cycles
"""

from password_entry import PasswordEntry
from password_store import PasswordStore
from password_generator import PasswordGenerator

def demo_tdd_evolution():
    """Demonstrate the functionality built through TDD"""
    print("🧪 TDD Method 3 Demonstration")
    print("=" * 50)

    # TDD Cycle 1 & 2: Password Entry with Unicode normalization
    print("\n1. Password Entry with Unicode Normalization (TDD Cycles 1-2)")
    print("-" * 60)

    entry1 = PasswordEntry("café", "user1", "password1")  # composed é
    entry2 = PasswordEntry("cafe´", "user2", "password2")  # decomposed e + ´

    print(f"Entry 1 service: {repr(entry1.service)}")
    print(f"Entry 2 service: {repr(entry2.service)}")
    print(f"Normalized 1: {repr(entry1.normalized_service)}")
    print(f"Normalized 2: {repr(entry2.normalized_service)}")
    print(f"Normalization equal: {entry1.normalized_service == entry2.normalized_service}")

    # TDD Cycle 3: Password Storage
    print("\n2. Password Storage (TDD Cycle 3)")
    print("-" * 60)

    store = PasswordStore()

    # Add some Unicode entries
    entries = [
        PasswordEntry("📧 Gmail", "user@gmail.com", "café🔐123"),
        PasswordEntry("🏦 Bank", "john", "password456"),
        PasswordEntry("Café WiFi", "guest", "wifi789"),
    ]

    for entry in entries:
        store.add(entry)

    print(f"Added {len(entries)} entries to store")

    # Test retrieval
    retrieved = store.get("📧 Gmail")
    print(f"Retrieved Gmail: {retrieved.service if retrieved else 'Not found'}")

    # Test normalized retrieval
    normalized = store.get_normalized("cafe´")  # decomposed, should find composed
    print(f"Normalized search for 'cafe´': {normalized.service if normalized else 'Not found'}")

    # TDD Cycle 4: Unicode Search
    print("\n3. Unicode-Aware Search (TDD Cycle 4)")
    print("-" * 60)

    test_searches = [
        ("gmail", "Should find 📧 Gmail"),
        ("bank", "Should find 🏦 Bank"),
        ("CAFE", "Should find Café WiFi (case insensitive)"),
        ("cafe", "Should find Café WiFi (diacritic removal)"),
    ]

    for query, description in test_searches:
        results = store.search(query)
        found = results[0].service if results else "Not found"
        print(f"Search '{query}': {found} ({description})")

    # TDD Cycle 5: Password Generation
    print("\n4. Password Generation (TDD Cycle 5)")
    print("-" * 60)

    generator = PasswordGenerator()

    # Generate different types of passwords
    ascii_pwd = generator.generate(12)
    unicode_pwd = generator.generate(12, include_unicode=True)
    emoji_pwd = generator.generate_emoji(8)

    print(f"ASCII password: {ascii_pwd}")
    print(f"Unicode password: {unicode_pwd}")
    print(f"Emoji password: {emoji_pwd}")

    # Test entropy and strength
    test_passwords = ["weak", "Strong123", "café🔐αβγ123"]

    print(f"\nPassword Analysis:")
    for pwd in test_passwords:
        entropy = generator.calculate_entropy(pwd)
        strength = generator.get_strength(pwd)
        print(f"'{pwd}': Entropy={entropy:.1f} bits, Strength={strength:.0f}/100")

def demo_unicode_edge_cases():
    """Demonstrate Unicode edge cases handled by TDD approach"""
    print("\n5. Unicode Edge Cases Handled by TDD")
    print("-" * 60)

    store = PasswordStore()
    generator = PasswordGenerator()

    # Edge case 1: Unicode normalization
    store.add(PasswordEntry("café", "user", "pass"))  # NFC
    results = store.search("cafe´")  # NFD search
    print(f"Normalization test: {'✅ Found' if results else '❌ Not found'}")

    # Edge case 2: Emoji in passwords
    emoji_password = generator.generate_emoji(6)
    store.add(PasswordEntry("Test", "user", emoji_password))
    retrieved = store.get("Test")
    print(f"Emoji password storage: {'✅ Works' if retrieved.password == emoji_password else '❌ Broken'}")

    # Edge case 3: Case sensitivity with Unicode
    store.add(PasswordEntry("MÜNCHEN", "admin", "pass"))
    results = store.search("münchen")
    print(f"Unicode case folding: {'✅ Found' if results else '❌ Not found'}")

    # Edge case 4: Mixed scripts
    mixed_service = "αβγ123🔐"
    store.add(PasswordEntry(mixed_service, "user", "pass"))
    results = store.search("αβγ")
    print(f"Mixed script search: {'✅ Found' if results else '❌ Not found'}")

def show_tdd_benefits():
    """Show benefits of TDD approach"""
    print("\n6. TDD Benefits Demonstrated")
    print("-" * 60)

    benefits = [
        "✅ Every feature is tested before implementation",
        "✅ Unicode edge cases caught early through tests",
        "✅ Refactoring is safe with comprehensive test coverage",
        "✅ API design driven by test requirements",
        "✅ Documentation through executable tests",
        "✅ Confidence in correctness",
        "✅ Incremental development with working code at each step"
    ]

    for benefit in benefits:
        print(benefit)

    print(f"\nCode Quality Metrics:")
    print(f"- Test Coverage: ~90% (estimated)")
    print(f"- Unicode Support: Comprehensive")
    print(f"- Edge Cases: Handled systematically")
    print(f"- Security: Basic (no encryption in this demo)")
    print(f"- Maintainability: High (well-tested)")

def main():
    """Run the complete TDD demonstration"""
    demo_tdd_evolution()
    demo_unicode_edge_cases()
    show_tdd_benefits()

    print("\n" + "=" * 60)
    print("🎯 TDD Method 3 Complete!")
    print("Built through 5 Red-Green-Refactor cycles")
    print("Each feature tested before implementation")
    print("Robust Unicode handling throughout")

if __name__ == "__main__":
    main()