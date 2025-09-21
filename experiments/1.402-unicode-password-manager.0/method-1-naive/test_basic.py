#!/usr/bin/env python3
"""
Quick test of the naive password manager
"""

from password_manager import PasswordManager
import os

# Clean start
if os.path.exists("passwords.json"):
    os.remove("passwords.json")

pm = PasswordManager()

# Test basic functionality
print("=== Testing Naive Password Manager ===")

# Add some passwords with Unicode
print("\n1. Adding passwords with Unicode characters...")
pm.add_password("📧 Gmail", "user@gmail.com", "café@123")
pm.add_password("🏦 Bank", "john_doe", "password🔐123")
pm.add_password("💻 GitHub", "developer", "🎯coding⚡pwd")

# List services
print("\n2. Listing all services...")
pm.list_services()

# Generate a password
print("\n3. Generating Unicode password...")
generated = pm.generate_password(15)
print(f"Generated: {generated}")

# Search functionality
print("\n4. Testing search...")
pm.search("gmail")
pm.search("Bank")

# Retrieve a password
print("\n5. Retrieving password...")
pm.get_password("📧 Gmail")

print("\n=== Basic Test Complete ===")

# Show the raw JSON to see encoding issues
print("\n6. Raw JSON content:")
if os.path.exists("passwords.json"):
    with open("passwords.json", 'r') as f:
        content = f.read()
        print(content)