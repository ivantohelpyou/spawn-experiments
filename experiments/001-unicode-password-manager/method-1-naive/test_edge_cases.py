#!/usr/bin/env python3
"""
Test edge cases that will break the naive implementation
"""

from password_manager import PasswordManager
import os

print("=== Testing Edge Cases That Break Naive Approach ===")

pm = PasswordManager()

# Test 1: Unicode normalization issues
print("\n1. Unicode Normalization Issues:")
print("Adding 'café' (precomposed)")
pm.add_password("café test", "user1", "password1")

print("Searching for 'cafe´' (decomposed - same visual, different encoding)")
# This should find the café entry but won't due to naive string matching
pm.search("cafe´")

print("Searching for 'café' (exact match)")
pm.search("café")

# Test 2: Case sensitivity with Unicode
print("\n2. Case Sensitivity Issues:")
pm.add_password("ĞMÁIL", "user2", "password2")  # Turkish/accented caps
pm.search("ğmáil")  # lowercase version - should match but won't

# Test 3: Emoji sequence issues
print("\n3. Emoji Sequence Issues:")
family_emoji = "👨‍👩‍👧‍👦"  # Family emoji (compound)
pm.add_password(f"Family {family_emoji}", "user3", "password3")

print(f"Length of family emoji: {len(family_emoji)} (code points)")
print(f"Bytes: {len(family_emoji.encode())} bytes")
print("This is actually 1 visual character but 11 code points!")

# Test 4: Homograph attack
print("\n4. Homograph Attack Vulnerability:")
pm.add_password("раssword", "user4", "real_password")  # Cyrillic 'р' and 'а'
pm.add_password("password", "user5", "fake_password")   # Latin chars

print("Two entries that look identical but are different:")
pm.get_password("раssword")  # Cyrillic
pm.get_password("password")   # Latin

# Test 5: Password generation issues
print("\n5. Password Generation Issues:")
for i in range(5):
    pwd = pm.generate_password(10)
    print(f"Generated: {pwd} (Length: {len(pwd)} code points, {len(pwd.encode())} bytes)")

# Test 6: Search with Unicode
print("\n6. Unicode Search Issues:")
pm.add_password("🎯 Target Account", "archer", "bullseye123")
pm.search("target")  # Won't find emoji version
pm.search("🎯")      # Only finds exact emoji match

print("\n=== Edge Case Testing Complete ===")
print("Notice how many searches fail due to naive string matching!")

# Test 7: JSON encoding issues
print("\n7. JSON Storage Issues:")
print("Look at the raw JSON - all Unicode is escaped to ASCII")
if os.path.exists("passwords.json"):
    with open("passwords.json", 'r') as f:
        content = f.read()
        print("Raw JSON (notice \\u escapes):")
        print(content[:200] + "..." if len(content) > 200 else content)