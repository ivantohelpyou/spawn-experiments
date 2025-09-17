#!/usr/bin/env python3
"""
Main entry point for LRU Cache with TTL implementation.

This script provides a simple command-line interface to choose between:
1. Interactive cache interface
2. Demonstration script
3. Unit tests
"""

import sys
import subprocess
import os


def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("    LRU Cache with TTL - Method 1: Direct Implementation")
    print("=" * 60)
    print()


def print_menu():
    """Print main menu options."""
    print("Choose an option:")
    print("1. Interactive Cache Interface")
    print("2. Run Demonstration")
    print("3. Run Unit Tests")
    print("4. Quick Example")
    print("5. Exit")
    print()


def run_interactive():
    """Run the interactive cache interface."""
    print("Starting interactive cache interface...")
    print("Type 'help' for commands or 'demo' for a built-in demonstration.")
    print("-" * 50)

    try:
        from cache_ui import main
        main()
    except ImportError as e:
        print(f"Error importing cache_ui: {e}")
    except KeyboardInterrupt:
        print("\\nReturning to main menu...")


def run_demo():
    """Run the demonstration script."""
    print("Running comprehensive demonstration...")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running demo: {e}")
    except KeyboardInterrupt:
        print("\\nDemo interrupted.")

    input("\\nPress Enter to continue...")


def run_tests():
    """Run the unit test suite."""
    print("Running unit test suite...")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, "test_lru_cache_ttl.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
    except KeyboardInterrupt:
        print("\\nTests interrupted.")

    input("\\nPress Enter to continue...")


def run_quick_example():
    """Run a quick example to show basic functionality."""
    print("Running quick example...")
    print("-" * 50)

    try:
        from lru_cache_ttl import LRUCacheWithTTL
        import time

        # Create cache
        cache = LRUCacheWithTTL(3)
        print("Created cache with capacity 3")

        # Add some items
        print("\\nAdding items:")
        cache.put("name", "Alice", 5.0)
        print("  put('name', 'Alice', 5.0)")

        cache.put("age", 30, 5.0)
        print("  put('age', 30, 5.0)")

        cache.put("city", "New York", 2.0)
        print("  put('city', 'New York', 2.0) - shorter TTL")

        # Show current state
        print(f"\\nCurrent cache state: {cache}")

        # Access items
        print("\\nAccessing items:")
        print(f"  get('name') = {cache.get('name')}")
        print(f"  get('age') = {cache.get('age')}")
        print(f"  get('city') = {cache.get('city')}")

        # Test capacity limit
        print("\\nTesting capacity limit:")
        cache.put("country", "USA", 5.0)
        print("  put('country', 'USA', 5.0)")
        print(f"  Cache after adding 4th item: {cache}")

        # Test TTL expiration
        print("\\nWaiting 2.5 seconds for 'city' to expire...")
        time.sleep(2.5)

        print("Accessing items after wait:")
        print(f"  get('city') = {cache.get('city')} (should be None - expired)")
        print(f"  get('name') = {cache.get('name')}")
        print(f"  get('country') = {cache.get('country')}")

        print(f"\\nFinal cache state: {cache}")
        print("\\nQuick example complete!")

    except ImportError as e:
        print(f"Error importing lru_cache_ttl: {e}")
    except Exception as e:
        print(f"Error in quick example: {e}")

    input("\\nPress Enter to continue...")


def main():
    """Main program loop."""
    print_banner()

    while True:
        print_menu()

        try:
            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                run_interactive()
            elif choice == '2':
                run_demo()
            elif choice == '3':
                run_tests()
            elif choice == '4':
                run_quick_example()
            elif choice == '5':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1-5.")

        except KeyboardInterrupt:
            print("\\nGoodbye!")
            sys.exit(0)
        except EOFError:
            print("\\nGoodbye!")
            sys.exit(0)

        print()  # Add blank line between iterations


if __name__ == "__main__":
    main()