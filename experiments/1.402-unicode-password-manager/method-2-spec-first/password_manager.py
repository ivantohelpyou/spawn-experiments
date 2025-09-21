"""
Main password manager application
Implements SPEC requirements with proper Unicode support
"""

from datetime import datetime
from getpass import getpass
import sys
from typing import Optional

from password_entry import PasswordEntry
from password_store import PasswordStore
from password_generator import PasswordGenerator, CharacterSet
from search_engine import SearchEngine

class UnicodePasswordManager:
    """
    Main password manager class implementing all specifications
    Follows SPEC-4.1 API design
    """

    def __init__(self, file_path: str = "passwords_secure.json"):
        self.store = PasswordStore(file_path)
        self.generator = PasswordGenerator()
        self.search_engine = SearchEngine()
        self.is_authenticated = False

    def initialize(self) -> bool:
        """
        Initialize the password manager
        Handle first-time setup or existing database
        """
        try:
            # Try to load existing database
            if self.store.load_from_file():
                print("📁 Existing password database found.")
                return self._authenticate()
            else:
                print("🆕 No existing database found. Setting up new password manager.")
                return self._setup_new_database()

        except Exception as e:
            print(f"❌ Error initializing: {e}")
            return False

    def _setup_new_database(self) -> bool:
        """Set up a new password database"""
        print("\n🔐 Setting up your secure password manager")
        print("Your master password will encrypt all stored passwords.")

        while True:
            master_password = getpass("Enter master password: ")
            confirm_password = getpass("Confirm master password: ")

            if master_password != confirm_password:
                print("❌ Passwords don't match. Try again.")
                continue

            try:
                self.store.set_master_password(master_password)
                self.store.save_to_file()
                self.is_authenticated = True
                print("✅ Password manager initialized successfully!")
                return True

            except ValueError as e:
                print(f"❌ {e}")
                continue

    def _authenticate(self) -> bool:
        """Authenticate with existing database"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            master_password = getpass("Enter master password: ")

            try:
                if self.store.unlock_and_load_entries(master_password):
                    self.search_engine.set_entries(self.store.entries)
                    self.is_authenticated = True
                    print("✅ Successfully unlocked password manager!")
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    print(f"❌ Incorrect password. {remaining} attempts remaining.")

            except Exception as e:
                print(f"❌ Error: {e}")
                return False

        print("🔒 Too many failed attempts. Exiting.")
        return False

    def add_password(self, service: str, username: str, password: str) -> bool:
        """
        Add a new password entry
        Implements SPEC-4.1 add_password
        """
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return False

        try:
            now = datetime.now()
            entry = PasswordEntry(
                service_name=service,
                username=username,
                password=password,
                created_date=now,
                modified_date=now
            )

            if self.store.add_entry(entry):
                self.store.save_to_file()
                self.search_engine.set_entries(self.store.entries)
                print(f"✅ Password for {service} saved!")

                # Show password strength
                strength = self.generator.get_password_strength_indicator(password)
                print(f"Password strength: {strength}")
                return True

        except ValueError as e:
            print(f"❌ {e}")
            return False

    def get_password(self, service: str) -> Optional[PasswordEntry]:
        """
        Retrieve password entry
        Implements SPEC-4.1 get_password
        """
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return None

        entry = self.store.get_entry(service)
        if entry:
            print(f"\n🔍 Found: {service}")
            print(f"Username: {entry.username}")
            print(f"Password: {entry.password}")
            print(f"Created: {entry.created_date.strftime('%Y-%m-%d %H:%M')}")
            if entry.category:
                print(f"Category: {entry.category}")

            # Copy to clipboard if available
            try:
                import pyperclip
                pyperclip.copy(entry.password)
                print("📋 Password copied to clipboard!")
            except ImportError:
                print("💡 Install pyperclip to enable clipboard copying")

            return entry
        else:
            print(f"❌ No password found for {service}")
            return None

    def update_password(self, service: str, new_password: str) -> bool:
        """
        Update existing password
        Implements SPEC-4.1 update_password
        """
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return False

        entry = self.store.get_entry(service)
        if not entry:
            print(f"❌ No entry found for {service}")
            return False

        entry.password = new_password
        entry.modified_date = datetime.now()

        if self.store.update_entry(service, entry):
            self.store.save_to_file()
            print(f"✅ Password for {service} updated!")

            # Show new password strength
            strength = self.generator.get_password_strength_indicator(new_password)
            print(f"New password strength: {strength}")
            return True

        return False

    def delete_password(self, service: str) -> bool:
        """
        Delete password entry
        Implements SPEC-4.1 delete_password
        """
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return False

        if self.store.delete_entry(service):
            self.store.save_to_file()
            self.search_engine.set_entries(self.store.entries)
            print(f"🗑️ Password for {service} deleted!")
            return True
        else:
            print(f"❌ No password found for {service}")
            return False

    def list_services(self) -> list:
        """
        List all services
        Implements SPEC-4.1 list_services
        """
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return []

        services = self.store.list_services()
        if services:
            print(f"\n📋 {len(services)} stored passwords:")
            for service in sorted(services):
                print(f"🔐 {service}")
        else:
            print("📭 No passwords stored yet")

        return services

    def search_services(self, query: str) -> list:
        """
        Search services
        Implements SPEC-4.1 search_services with Unicode awareness
        """
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return []

        results = self.search_engine.search(query)
        if results:
            print(f"\n🔍 Found {len(results)} matches for '{query}':")
            for service in results:
                print(f"📌 {service}")
        else:
            print(f"❌ No matches found for '{query}'")

            # Offer fuzzy search
            fuzzy_results = self.search_engine.fuzzy_search(query)
            if fuzzy_results:
                print(f"💡 Did you mean:")
                for service in fuzzy_results[:3]:  # Show top 3
                    print(f"   {service}")

        return results

    def generate_password(
        self,
        length: int = 16,
        charset: CharacterSet = CharacterSet.UNICODE_MIXED,
        exclude_similar: bool = True
    ) -> str:
        """
        Generate secure password
        Implements SPEC-4.2 password generation
        """
        try:
            password = self.generator.generate_password(length, charset, exclude_similar)
            print(f"🔑 Generated password: {password}")

            # Show strength and entropy
            strength = self.generator.get_password_strength_indicator(password)
            entropy = self.generator.analyze_password_entropy(password)
            print(f"Strength: {strength}")
            print(f"Entropy: {entropy:.1f} bits")

            return password

        except ValueError as e:
            print(f"❌ {e}")
            return ""

    def show_statistics(self):
        """Show password database statistics"""
        if not self.is_authenticated:
            print("❌ Not authenticated")
            return

        stats = self.store.get_statistics()
        print(f"\n📊 Password Database Statistics:")
        print(f"Total entries: {stats['total_entries']}")
        print(f"Categories: {stats['categories']}")
        if stats['oldest_entry']:
            print(f"Oldest entry: {stats['oldest_entry'].strftime('%Y-%m-%d')}")
        if stats['newest_entry']:
            print(f"Newest entry: {stats['newest_entry'].strftime('%Y-%m-%d')}")

def main():
    """Main application loop"""
    print("🔐 Unicode Password Manager")
    print("Supports international characters, emoji, and symbols!\n")

    manager = UnicodePasswordManager()

    if not manager.initialize():
        sys.exit(1)

    while True:
        print("\n" + "="*50)
        print("🔐 Unicode Password Manager Menu")
        print("1. Add password")
        print("2. Get password")
        print("3. List all services")
        print("4. Search passwords")
        print("5. Generate password")
        print("6. Update password")
        print("7. Delete password")
        print("8. Show statistics")
        print("9. Exit")

        choice = input("\nChoose an option (1-9): ").strip()

        try:
            if choice == '1':
                service = input("Service name (🔗 emojis supported): ")
                username = input("Username: ")
                password = getpass("Password (or press Enter to generate): ")

                if not password:
                    print("\nGenerate password:")
                    print("1. ASCII only")
                    print("2. ASCII + symbols")
                    print("3. Unicode mixed (recommended)")
                    print("4. Emoji only (fun!)")

                    gen_choice = input("Generator type (1-4, default 3): ").strip() or "3"
                    length = input("Length (8-128, default 16): ").strip()
                    length = int(length) if length.isdigit() else 16

                    charset_map = {
                        "1": CharacterSet.ASCII_BASIC,
                        "2": CharacterSet.ASCII_EXTENDED,
                        "3": CharacterSet.UNICODE_MIXED,
                        "4": CharacterSet.EMOJI_ONLY
                    }

                    charset = charset_map.get(gen_choice, CharacterSet.UNICODE_MIXED)
                    password = manager.generate_password(length, charset)

                if password:
                    manager.add_password(service, username, password)

            elif choice == '2':
                service = input("Service name: ")
                manager.get_password(service)

            elif choice == '3':
                manager.list_services()

            elif choice == '4':
                query = input("Search for: ")
                manager.search_services(query)

            elif choice == '5':
                print("\nPassword Generator Options:")
                print("1. ASCII only")
                print("2. ASCII + symbols")
                print("3. Unicode mixed (recommended)")
                print("4. Unicode symbols")
                print("5. Emoji only")

                gen_choice = input("Choose type (1-5, default 3): ").strip() or "3"
                length = input("Length (8-128, default 16): ").strip()
                length = int(length) if length.isdigit() else 16

                charset_map = {
                    "1": CharacterSet.ASCII_BASIC,
                    "2": CharacterSet.ASCII_EXTENDED,
                    "3": CharacterSet.UNICODE_MIXED,
                    "4": CharacterSet.UNICODE_SYMBOLS,
                    "5": CharacterSet.EMOJI_ONLY
                }

                charset = charset_map.get(gen_choice, CharacterSet.UNICODE_MIXED)
                manager.generate_password(length, charset)

            elif choice == '6':
                service = input("Service name to update: ")
                new_password = getpass("New password (or press Enter to generate): ")

                if not new_password:
                    new_password = manager.generate_password()

                if new_password:
                    manager.update_password(service, new_password)

            elif choice == '7':
                service = input("Service name to delete: ")
                confirm = input(f"Are you sure you want to delete '{service}'? (y/N): ")
                if confirm.lower() == 'y':
                    manager.delete_password(service)

            elif choice == '8':
                manager.show_statistics()

            elif choice == '9':
                print("👋 Goodbye! Your passwords are safely encrypted.")
                manager.store.lock()  # Clear sensitive data
                break

            else:
                print("❌ Invalid option. Please choose 1-9.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            manager.store.lock()
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()