"""
User Interface for LRU Cache with TTL

This module provides an interactive command-line interface for testing
and demonstrating the LRU Cache with TTL functionality.
"""

import time
import sys
from typing import Any
from lru_cache_ttl import LRUCacheWithTTL


class CacheUI:
    """Interactive user interface for the LRU Cache with TTL."""

    def __init__(self):
        self.cache = None
        self.commands = {
            'help': self.show_help,
            'h': self.show_help,
            'create': self.create_cache,
            'put': self.put_item,
            'get': self.get_item,
            'size': self.show_size,
            'keys': self.show_keys,
            'items': self.show_items,
            'clear': self.clear_cache,
            'status': self.show_status,
            'demo': self.run_demo,
            'quit': self.quit_program,
            'q': self.quit_program,
            'exit': self.quit_program
        }

    def show_help(self) -> None:
        """Display available commands."""
        print("\\n=== LRU Cache with TTL - Available Commands ===")
        print("create <capacity>          - Create a new cache with given capacity")
        print("put <key> <value> <ttl>    - Store item with TTL (seconds)")
        print("get <key>                  - Retrieve item by key")
        print("size                       - Show current cache size")
        print("keys                       - Show all keys")
        print("items                      - Show all key-value pairs")
        print("clear                      - Clear all items from cache")
        print("status                     - Show cache status and statistics")
        print("demo                       - Run automated demonstration")
        print("help, h                    - Show this help message")
        print("quit, q, exit              - Exit the program")
        print("=" * 50)

    def create_cache(self, *args) -> None:
        """Create a new cache with specified capacity."""
        if not args:
            print("Error: Please specify capacity. Usage: create <capacity>")
            return

        try:
            capacity = int(args[0])
            self.cache = LRUCacheWithTTL(capacity)
            print(f"Created cache with capacity {capacity}")
        except ValueError as e:
            print(f"Error: {e}")

    def put_item(self, *args) -> None:
        """Store an item in the cache."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        if len(args) < 3:
            print("Error: Usage: put <key> <value> <ttl_seconds>")
            return

        try:
            key = args[0]
            value = args[1]
            ttl = float(args[2])

            # Try to convert value to appropriate type
            if value.isdigit():
                value = int(value)
            elif value.replace('.', '').isdigit():
                value = float(value)

            self.cache.put(key, value, ttl)
            print(f"Stored: {key} = {value} (expires in {ttl}s)")
        except ValueError as e:
            print(f"Error: {e}")

    def get_item(self, *args) -> None:
        """Retrieve an item from the cache."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        if not args:
            print("Error: Usage: get <key>")
            return

        key = args[0]
        value = self.cache.get(key)

        if value is not None:
            print(f"Retrieved: {key} = {value}")
        else:
            print(f"Key '{key}' not found or expired")

    def show_size(self) -> None:
        """Display current cache size."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        size = self.cache.size()
        print(f"Cache size: {size}/{self.cache.capacity}")

    def show_keys(self) -> None:
        """Display all keys in the cache."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        keys = self.cache.keys()
        if keys:
            print(f"Keys: {', '.join(map(str, keys))}")
        else:
            print("No keys in cache")

    def show_items(self) -> None:
        """Display all key-value pairs in the cache."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        items = self.cache.items()
        if items:
            print("Items:")
            for key, value in items:
                print(f"  {key}: {value}")
        else:
            print("No items in cache")

    def clear_cache(self) -> None:
        """Clear all items from the cache."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        self.cache.clear()
        print("Cache cleared")

    def show_status(self) -> None:
        """Display detailed cache status."""
        if not self.cache:
            print("Error: No cache created. Use 'create <capacity>' first.")
            return

        print("\\n=== Cache Status ===")
        print(f"Capacity: {self.cache.capacity}")
        print(f"Current size: {self.cache.size()}")
        print(f"Utilization: {(self.cache.size() / self.cache.capacity) * 100:.1f}%")
        print(f"Cache representation: {self.cache}")
        print("=" * 20)

    def run_demo(self) -> None:
        """Run an automated demonstration of cache functionality."""
        print("\\n=== Running Cache Demonstration ===")

        # Create cache
        self.cache = LRUCacheWithTTL(3)
        print("1. Created cache with capacity 3")

        # Add items with different TTLs
        print("\\n2. Adding items with different TTLs:")
        self.cache.put("user:123", "Alice", 5.0)
        print("   Added: user:123 = Alice (5s TTL)")

        self.cache.put("session:abc", "active", 3.0)
        print("   Added: session:abc = active (3s TTL)")

        self.cache.put("temp:data", "temporary", 2.0)
        print("   Added: temp:data = temporary (2s TTL)")

        print(f"\\n3. Cache status: {self.cache}")

        # Test capacity limit
        print("\\n4. Testing capacity limit (adding 4th item):")
        self.cache.put("new:item", "newest", 10.0)
        print("   Added: new:item = newest (10s TTL)")
        print(f"   Cache after LRU eviction: {self.cache}")

        # Test retrieval and LRU ordering
        print("\\n5. Testing retrieval and LRU ordering:")
        value = self.cache.get("session:abc")
        print(f"   Retrieved session:abc = {value}")
        print(f"   Cache after access (session:abc moved to front): {self.cache}")

        # Wait for expiration
        print("\\n6. Waiting for items to expire...")
        time.sleep(2.5)
        print("   After 2.5 seconds:")
        print(f"   Accessing temp:data: {self.cache.get('temp:data')}")
        print(f"   Cache after expired cleanup: {self.cache}")

        time.sleep(1)
        print("\\n   After 3.5 seconds total:")
        print(f"   Accessing session:abc: {self.cache.get('session:abc')}")
        print(f"   Cache after expired cleanup: {self.cache}")

        print("\\n=== Demo Complete ===")

    def quit_program(self) -> None:
        """Exit the program."""
        print("Goodbye!")
        sys.exit(0)

    def parse_command(self, user_input: str) -> tuple:
        """Parse user input into command and arguments."""
        parts = user_input.strip().split()
        if not parts:
            return None, []
        return parts[0].lower(), parts[1:]

    def run(self) -> None:
        """Main interactive loop."""
        print("=== LRU Cache with TTL Interactive Interface ===")
        print("Type 'help' for available commands or 'demo' for a demonstration.")

        while True:
            try:
                user_input = input("\\ncache> ").strip()

                if not user_input:
                    continue

                command, args = self.parse_command(user_input)

                if command in self.commands:
                    self.commands[command](*args)
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\\nGoodbye!")
                break
            except EOFError:
                print("\\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point for the cache UI."""
    ui = CacheUI()
    ui.run()


if __name__ == "__main__":
    main()