#!/usr/bin/env python3
"""
Simple password manager with Unicode support
"""

import json
import random
import string
import os
from getpass import getpass

class PasswordManager:
    def __init__(self, file_path="passwords.json"):
        self.file_path = file_path
        self.passwords = {}
        self.load_passwords()

    def load_passwords(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.passwords = json.load(f)

    def save_passwords(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.passwords, f, indent=2)

    def add_password(self, service, username, password):
        self.passwords[service] = {
            'username': username,
            'password': password
        }
        self.save_passwords()
        print(f"✅ Password for {service} saved!")

    def get_password(self, service):
        if service in self.passwords:
            entry = self.passwords[service]
            print(f"Service: {service}")
            print(f"Username: {entry['username']}")
            print(f"Password: {entry['password']}")
        else:
            print(f"❌ No password found for {service}")

    def list_services(self):
        if not self.passwords:
            print("No passwords stored")
            return

        print("Stored passwords:")
        for service in self.passwords:
            print(f"🔐 {service}")

    def generate_password(self, length=12):
        # Basic character sets
        chars = string.ascii_letters + string.digits + "!@#$%^&*"

        # Add some Unicode characters for fun
        unicode_chars = "🔐🗝️🔒🔓💪⚡🎯"
        chars += unicode_chars

        password = ''.join(random.choice(chars) for _ in range(length))
        return password

    def search(self, query):
        results = []
        for service in self.passwords:
            if query.lower() in service.lower():
                results.append(service)

        if results:
            print(f"Found {len(results)} matches:")
            for service in results:
                print(f"🔍 {service}")
        else:
            print("No matches found")

    def delete_password(self, service):
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
            print(f"🗑️ Password for {service} deleted!")
        else:
            print(f"❌ No password found for {service}")

def main():
    pm = PasswordManager()

    while True:
        print("\n🔐 Unicode Password Manager")
        print("1. Add password")
        print("2. Get password")
        print("3. List all services")
        print("4. Generate password")
        print("5. Search")
        print("6. Delete password")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            service = input("Service name: ")
            username = input("Username: ")
            password = getpass("Password (or press Enter to generate): ")
            if not password:
                password = pm.generate_password()
                print(f"Generated password: {password}")
            pm.add_password(service, username, password)

        elif choice == '2':
            service = input("Service name: ")
            pm.get_password(service)

        elif choice == '3':
            pm.list_services()

        elif choice == '4':
            length = input("Password length (default 12): ")
            length = int(length) if length else 12
            password = pm.generate_password(length)
            print(f"Generated password: {password}")

        elif choice == '5':
            query = input("Search for: ")
            pm.search(query)

        elif choice == '6':
            service = input("Service to delete: ")
            pm.delete_password(service)

        elif choice == '7':
            print("👋 Goodbye!")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()