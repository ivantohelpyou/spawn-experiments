#!/usr/bin/env python3
"""
Live Demo Script for TDD in the AI Era Presentation
Minimal implementation showing the cycle with practical Unicode input
"""

import os
import sys

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def demo_header(title):
    """Show demo section header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def show_unicode_picker():
    """Show available Unicode characters for easy copy-paste"""
    print("\n📋 Unicode Character Picker (copy-paste these):")
    print("-" * 50)

    categories = {
        "Email & Communication": ["📧", "📨", "📩", "✉️", "📬", "📭"],
        "Financial & Banking": ["🏦", "💳", "💰", "💸", "💎", "🪙"],
        "Work & Productivity": ["💻", "⌨️", "🖥️", "📊", "📈", "📉"],
        "Security & Access": ["🔐", "🗝️", "🔒", "🔓", "🔑", "🛡️"],
        "Social & Entertainment": ["📱", "🎮", "🎬", "🎵", "📺", "🎯"],
        "Travel & Location": ["✈️", "🚗", "🏨", "🗺️", "📍", "🌍"],
        "Common Accented": ["café", "naïve", "résumé", "México", "München", "Москва"]
    }

    for category, chars in categories.items():
        print(f"{category:25}: {' '.join(chars)}")

    print("\n💡 Tip: Copy-paste these characters into service names!")
    input("\nPress Enter to continue...")

def demo_method_comparison():
    """Show the four methods with realistic examples"""
    clear_screen()
    demo_header("Method Comparison with Real Examples")

    print("We'll test each method with the same challenging input:")
    print("  Service: 📧 Gmail (with emoji)")
    print("  Search: 'gmail' (without emoji)")
    print("  Expected: Should find the entry")

    methods = [
        ("Method 1: Naive", "❌ Fails - exact match only"),
        ("Method 2: Spec-First", "✅ Works - planned Unicode support"),
        ("Method 3: TDD", "✅ Works - test-driven Unicode handling"),
        ("Method 4: Enhanced TDD", "✅ Works - proven Unicode handling")
    ]

    print(f"\n{'Method':20} {'Result':30}")
    print("-" * 55)
    for method, result in methods:
        print(f"{method:20} {result:30}")

    input("\nPress Enter to see live demonstration...")

def demo_unicode_edge_cases():
    """Demonstrate Unicode complexity"""
    clear_screen()
    demo_header("Unicode Complexity Demonstration")

    print("Why Unicode is challenging for password managers:")
    print()

    # Example 1: Normalization
    print("1. Unicode Normalization:")
    composed = "café"      # NFC form
    decomposed = "cafe´"   # NFD form (e + combining acute)

    print(f"   Composed:   '{composed}' (looks like café)")
    print(f"   Decomposed: '{decomposed}' (also looks like café)")
    print(f"   Equal?      {composed == decomposed}")
    print(f"   Bytes:      {len(composed.encode())} vs {len(decomposed.encode())}")
    print()

    # Example 2: Emoji sequences
    print("2. Complex Emoji:")
    family = "👨‍👩‍👧‍👦"
    print(f"   Family emoji: '{family}'")
    print(f"   Visual chars: 1")
    print(f"   Code points:  {len(family)}")
    print(f"   Bytes:        {len(family.encode())}")
    print()

    # Example 3: Homograph attack
    print("3. Homograph Attack Potential:")
    cyrillic = "раssword"  # Cyrillic р and а
    latin = "password"     # Latin p and a
    print(f"   Cyrillic: '{cyrillic}' (contains Cyrillic chars)")
    print(f"   Latin:    '{latin}' (all Latin chars)")
    print(f"   Look same? Yes, but Equal? {cyrillic == latin}")

    input("\nPress Enter to continue...")

def demo_live_password_manager():
    """Interactive demo with realistic Unicode input"""
    clear_screen()
    demo_header("Live Password Manager Demo (Method 4)")

    # Simulated password store
    passwords = {}

    print("Let's add some realistic Unicode password entries:")
    print()

    # Pre-populate with realistic examples
    demo_entries = [
        ("📧 Gmail Account", "user@gmail.com"),
        ("🏦 Bank of América", "john.doe@email.com"),
        ("💻 GitHub Projects", "developer@company.com"),
        ("Café René WiFi", "guest"),
        ("München Office VPN", "admin@company.de"),
    ]

    print("Adding entries:")
    for service, username in demo_entries:
        passwords[service] = {
            'username': username,
            'password': f"secure_{len(passwords)+1}@123"
        }
        print(f"✅ Added: {service}")

    print(f"\nTotal entries: {len(passwords)}")

    # Interactive search demo
    print("\n" + "-" * 40)
    print("Now let's test Unicode-aware search:")

    while True:
        print(f"\nCurrent entries:")
        for i, service in enumerate(passwords.keys(), 1):
            print(f"  {i}. {service}")

        search_query = input(f"\nEnter search term (or 'quit'): ").strip()

        if search_query.lower() == 'quit':
            break

        if not search_query:
            continue

        # Simulate enhanced search
        matches = simulate_enhanced_search(search_query, passwords)

        if matches:
            print(f"\n🔍 Found {len(matches)} match(es):")
            for service, data in matches:
                print(f"  ✅ {service}")
                print(f"      Username: {data['username']}")
                print(f"      Password: {data['password']}")
        else:
            print("❌ No matches found")

            # Show what would work
            print("\n💡 Try searching for:")
            suggestions = ["gmail", "bank", "github", "cafe", "munchen"]
            for suggestion in suggestions:
                if suggestion not in search_query.lower():
                    print(f"   - '{suggestion}'")
                    break

def simulate_enhanced_search(query, passwords):
    """Simulate the enhanced Unicode search"""
    import unicodedata

    def normalize_for_search(text):
        # Simplified version of our enhanced search
        normalized = unicodedata.normalize('NFC', text.lower())
        # Remove diacritics
        decomposed = unicodedata.normalize('NFD', normalized)
        without_marks = ''.join(c for c in decomposed if unicodedata.category(c) != 'Mn')
        # Extract alphanumeric for emoji tolerance
        alphanumeric = ''.join(c for c in without_marks if c.isalnum())
        return without_marks, alphanumeric

    query_norm, query_alpha = normalize_for_search(query)
    matches = []

    for service, data in passwords.items():
        service_norm, service_alpha = normalize_for_search(service)

        # Check for matches at different levels
        if (query_norm in service_norm or
            query_alpha in service_alpha or
            query.lower() in service.lower()):
            matches.append((service, data))

    return matches

def demo_test_validation_concept():
    """Demonstrate the test validation concept"""
    clear_screen()
    demo_header("Test Validation Demonstration")

    print("Enhanced TDD's key innovation: Test the Tests!")
    print()

    print("Traditional TDD:")
    print("  1. ❌ RED: Write failing test")
    print("  2. ✅ GREEN: Make test pass")
    print("  3. 🔄 REFACTOR: Clean up code")
    print()

    print("Enhanced TDD adds validation:")
    print("  1. ❌ RED: Write failing test")
    print("  2. 🧪 VALIDATE: Prove test catches bugs")
    print("     a) Write broken implementation")
    print("     b) Verify test fails for right reason")
    print("     c) Check test quality")
    print("  3. ✅ GREEN: Write correct implementation")
    print("  4. 🔄 REFACTOR: Clean up code")
    print()

    print("Example validation process:")
    print("  Test: 'gmail' should find '📧 Gmail Account'")
    print("  Broken impl: exact string matching only")
    print("  Validation: ✅ Test fails (proves test works)")
    print("  Correct impl: Unicode-aware search")
    print("  Result: ✅ Test passes (implementation works)")

    input("\nPress Enter to continue...")

def demo_methodology_impact():
    """Show the impact of methodology choice"""
    clear_screen()
    demo_header("Methodology Impact Summary")

    print("Same task, different approaches, different outcomes:")
    print()

    results = [
        ("Method 1: Naive", "15 min", "15+ bugs", "0%", "❌ Broken"),
        ("Method 2: Spec-First", "195 min", "5 bugs", "20%", "⚠️ Gaps"),
        ("Method 3: TDD", "150 min", "1-2 bugs", "90%", "✅ Good"),
        ("Method 4: Enhanced TDD", "240 min", "0 bugs", "98%", "🏆 Excellent")
    ]

    print(f"{'Method':20} {'Time':8} {'Bugs':8} {'Coverage':8} {'Result':12}")
    print("-" * 70)
    for method, time, bugs, coverage, result in results:
        print(f"{method:20} {time:8} {bugs:8} {coverage:8} {result:12}")

    print()
    print("Key Insight: 16x time investment → 100% bug reduction")
    print("             Methodology choice determines quality")

    input("\nPress Enter to see conclusion...")

def demo_conclusion():
    """Wrap up the demonstration"""
    clear_screen()
    demo_header("Conclusion: TDD in the AI Era")

    print("What we've demonstrated:")
    print("  ✅ AI amplifies your methodology (good or bad)")
    print("  ✅ Unicode provides perfect complexity test case")
    print("  ✅ TDD dramatically improves AI-generated code")
    print("  ✅ Test validation catches issues TDD alone misses")
    print("  ✅ Time investment in methodology pays massive dividends")
    print()

    print("For your AI development:")
    print("  🎯 Choose methodology deliberately")
    print("  🧪 Write tests first, especially for complex domains")
    print("  🔍 Validate your tests catch real bugs")
    print("  📈 Invest in quality - it compounds")
    print()

    print("Questions?")
    print("  📧 GitHub: https://github.com/anthropics/claude-code")
    print("  💬 Discussion: Let's talk about your TDD experiences!")

def main():
    """Run the complete demo"""
    clear_screen()
    print("🎯 TDD in the AI Era: Live Demonstration")
    print("Puget Sound Python Meetup")
    print("="*50)

    demos = [
        ("Show Unicode Picker", show_unicode_picker),
        ("Method Comparison", demo_method_comparison),
        ("Unicode Complexity", demo_unicode_edge_cases),
        ("Live Password Manager", demo_live_password_manager),
        ("Test Validation Concept", demo_test_validation_concept),
        ("Methodology Impact", demo_methodology_impact),
        ("Conclusion", demo_conclusion)
    ]

    print("\nDemo sections:")
    for i, (title, _) in enumerate(demos, 1):
        print(f"  {i}. {title}")

    input("\nPress Enter to start demo...")

    for title, demo_func in demos:
        demo_func()

    clear_screen()
    print("🎉 Demo Complete!")
    print("Thank you Puget Sound Python!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo ended early. Thanks for watching!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("But the methodology still works! 😄")