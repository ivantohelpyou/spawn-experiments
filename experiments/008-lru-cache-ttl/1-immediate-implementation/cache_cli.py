#!/usr/bin/env python3
"""
Command-Line Interface for LRU Cache with TTL

This module provides a comprehensive CLI for interacting with the LRU Cache with TTL.
Features:
- Interactive shell mode
- Single command execution
- Configuration management
- Import/export functionality
- Real-time statistics and monitoring
- Batch operations
- Help system
"""

import argparse
import cmd
import json
import sys
import time
import threading
from typing import Any, Dict, List, Optional
import readline  # For better CLI experience
from lru_cache_ttl import LRUCacheWithTTL, create_cache


class CacheCLI(cmd.Cmd):
    """Interactive command-line interface for the LRU Cache with TTL."""

    intro = '''
LRU Cache with TTL - Interactive Shell
======================================
Type 'help' for available commands.
Type 'help <command>' for detailed help on a specific command.
Type 'quit' or 'exit' to leave.
'''
    prompt = 'cache> '

    def __init__(self, cache: Optional[LRUCacheWithTTL] = None):
        super().__init__()
        self.cache = cache or create_cache()
        self.monitoring = False
        self.monitor_thread = None
        self.stop_monitor = threading.Event()

    def default(self, line: str):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' for available commands.")

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_set(self, args: str):
        """
        Set a key-value pair in the cache.
        Usage: set <key> <value> [ttl_seconds]

        Examples:
            set user:1 "{'name': 'Alice'}"
            set temp_data "some value" 10
            set config {"theme": "dark"} 300
        """
        parts = args.split(None, 2)
        if len(parts) < 2:
            print("Usage: set <key> <value> [ttl_seconds]")
            return

        key = parts[0]
        value_str = parts[1]
        ttl = None

        if len(parts) == 3:
            try:
                ttl = float(parts[2])
            except ValueError:
                print("TTL must be a number (seconds)")
                return

        # Try to parse value as JSON, fall back to string
        try:
            value = json.loads(value_str)
        except json.JSONDecodeError:
            value = value_str

        self.cache.set(key, value, ttl)
        ttl_info = f" (TTL: {ttl}s)" if ttl else ""
        print(f"Set '{key}' = {value}{ttl_info}")

    def do_get(self, args: str):
        """
        Get a value from the cache.
        Usage: get <key>

        Example:
            get user:1
        """
        if not args.strip():
            print("Usage: get <key>")
            return

        key = args.strip()
        value = self.cache.get(key)

        if value is None:
            print(f"Key '{key}' not found or expired")
        else:
            print(f"'{key}' = {json.dumps(value) if isinstance(value, (dict, list)) else value}")

    def do_delete(self, args: str):
        """
        Delete a key from the cache.
        Usage: delete <key>

        Example:
            delete user:1
        """
        if not args.strip():
            print("Usage: delete <key>")
            return

        key = args.strip()
        if self.cache.delete(key):
            print(f"Deleted '{key}'")
        else:
            print(f"Key '{key}' not found")

    def do_exists(self, args: str):
        """
        Check if a key exists in the cache.
        Usage: exists <key>

        Example:
            exists user:1
        """
        if not args.strip():
            print("Usage: exists <key>")
            return

        key = args.strip()
        exists = self.cache.exists(key)
        print(f"Key '{key}' {'exists' if exists else 'does not exist'}")

    def do_ttl(self, args: str):
        """
        Get the remaining TTL for a key.
        Usage: ttl <key>

        Example:
            ttl user:1
        """
        if not args.strip():
            print("Usage: ttl <key>")
            return

        key = args.strip()
        ttl_remaining = self.cache.ttl(key)

        if ttl_remaining is None:
            if self.cache.exists(key):
                print(f"Key '{key}' has no expiration")
            else:
                print(f"Key '{key}' not found")
        else:
            print(f"Key '{key}' expires in {ttl_remaining:.2f} seconds")

    def do_keys(self, args: str):
        """
        List all keys in the cache.
        Usage: keys [pattern]

        Examples:
            keys
            keys user:*
        """
        pattern = args.strip() if args.strip() else None
        keys_list = list(self.cache.keys())

        if pattern:
            import fnmatch
            keys_list = [k for k in keys_list if fnmatch.fnmatch(k, pattern)]

        if keys_list:
            print(f"Keys ({len(keys_list)}):")
            for key in sorted(keys_list):
                ttl_info = ""
                ttl_remaining = self.cache.ttl(key)
                if ttl_remaining is not None:
                    ttl_info = f" (TTL: {ttl_remaining:.1f}s)"
                print(f"  {key}{ttl_info}")
        else:
            print("No keys found")

    def do_size(self, args: str):
        """
        Show cache size information.
        Usage: size
        """
        size = self.cache.size()
        capacity = self.cache.capacity()
        load_factor = (size / capacity) * 100 if capacity > 0 else 0

        print(f"Cache size: {size}/{capacity} ({load_factor:.1f}% full)")

    def do_clear(self, args: str):
        """
        Clear all items from the cache.
        Usage: clear
        """
        confirm = input("Are you sure you want to clear the cache? (y/N): ")
        if confirm.lower() in ('y', 'yes'):
            self.cache.clear()
            print("Cache cleared")
        else:
            print("Operation cancelled")

    def do_stats(self, args: str):
        """
        Show cache statistics.
        Usage: stats [reset]

        Examples:
            stats
            stats reset
        """
        if args.strip() == 'reset':
            self.cache.reset_stats()
            print("Statistics reset")
            return

        stats = self.cache.get_stats()
        print("\nCache Statistics:")
        print("=" * 40)
        print(f"Size: {stats['size']}/{stats['capacity']} ({stats['load_factor']:.1%} full)")
        print(f"Hit Rate: {stats['hit_rate']:.1%}")
        print(f"Operations:")
        print(f"  Hits: {stats['hits']}")
        print(f"  Misses: {stats['misses']}")
        print(f"  Sets: {stats['sets']}")
        print(f"  Deletes: {stats['deletes']}")
        print(f"  Evictions: {stats['evictions']}")
        print(f"  Expirations: {stats['expirations']}")

    def do_save(self, args: str):
        """
        Save cache to a file.
        Usage: save <filepath>

        Example:
            save cache_backup.json
        """
        if not args.strip():
            print("Usage: save <filepath>")
            return

        filepath = args.strip()
        try:
            self.cache.save_to_file(filepath)
            print(f"Cache saved to '{filepath}'")
        except Exception as e:
            print(f"Error saving cache: {e}")

    def do_load(self, args: str):
        """
        Load cache from a file.
        Usage: load <filepath>

        Example:
            load cache_backup.json
        """
        if not args.strip():
            print("Usage: load <filepath>")
            return

        filepath = args.strip()
        try:
            if self.cache.load_from_file(filepath):
                print(f"Cache loaded from '{filepath}'")
            else:
                print(f"Failed to load cache from '{filepath}'")
        except Exception as e:
            print(f"Error loading cache: {e}")

    def do_config(self, args: str):
        """
        Show or modify cache configuration.
        Usage: config [set <property> <value>]

        Examples:
            config
            config set max_size 256
            config set default_ttl 600
        """
        parts = args.split()

        if not parts:
            # Show current config
            print("\nCache Configuration:")
            print("=" * 30)
            print(f"Max Size: {self.cache.max_size}")
            print(f"Default TTL: {self.cache.default_ttl}")
            print(f"Current Size: {self.cache.size()}")
            return

        if len(parts) >= 3 and parts[0] == 'set':
            prop = parts[1]
            value = parts[2]

            if prop == 'max_size':
                try:
                    new_size = int(value)
                    if new_size > 0:
                        self.cache.max_size = new_size
                        print(f"Max size set to {new_size}")
                    else:
                        print("Max size must be positive")
                except ValueError:
                    print("Max size must be an integer")

            elif prop == 'default_ttl':
                try:
                    new_ttl = float(value) if value != 'None' else None
                    self.cache.default_ttl = new_ttl
                    print(f"Default TTL set to {new_ttl}")
                except ValueError:
                    print("TTL must be a number or 'None'")

            else:
                print(f"Unknown property: {prop}")
        else:
            print("Usage: config [set <property> <value>]")

    def do_monitor(self, args: str):
        """
        Start/stop real-time monitoring.
        Usage: monitor [start|stop|status]

        Examples:
            monitor start
            monitor stop
        """
        command = args.strip().lower()

        if command == 'start':
            if not self.monitoring:
                self.monitoring = True
                self.stop_monitor.clear()
                self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
                self.monitor_thread.start()
                print("Monitoring started. Type 'monitor stop' to stop.")
            else:
                print("Monitoring is already running")

        elif command == 'stop':
            if self.monitoring:
                self.monitoring = False
                self.stop_monitor.set()
                print("Monitoring stopped")
            else:
                print("Monitoring is not running")

        elif command == 'status' or not command:
            status = "running" if self.monitoring else "stopped"
            print(f"Monitoring is {status}")

        else:
            print("Usage: monitor [start|stop|status]")

    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.monitoring and not self.stop_monitor.wait(5):
            stats = self.cache.get_stats()
            print(f"\n[MONITOR] Size: {stats['size']}/{stats['capacity']}, "
                  f"Hit Rate: {stats['hit_rate']:.1%}, "
                  f"Operations: {stats['hits'] + stats['misses'] + stats['sets']}")

    def do_batch(self, args: str):
        """
        Execute batch operations from a file.
        Usage: batch <filepath>

        File format: One command per line
        Example:
            set key1 value1
            set key2 value2 10
            get key1
        """
        if not args.strip():
            print("Usage: batch <filepath>")
            return

        filepath = args.strip()
        try:
            with open(filepath, 'r') as f:
                commands = f.readlines()

            print(f"Executing {len(commands)} commands from '{filepath}'...")

            for i, command in enumerate(commands, 1):
                command = command.strip()
                if command and not command.startswith('#'):
                    print(f"[{i}] {command}")
                    self.onecmd(command)

            print("Batch execution completed")

        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except Exception as e:
            print(f"Error executing batch: {e}")

    def do_export(self, args: str):
        """
        Export cache contents in various formats.
        Usage: export <format> <filepath>

        Formats: json, csv, txt
        Examples:
            export json cache_data.json
            export csv cache_data.csv
            export txt cache_data.txt
        """
        parts = args.split()
        if len(parts) != 2:
            print("Usage: export <format> <filepath>")
            return

        format_type, filepath = parts

        try:
            if format_type.lower() == 'json':
                data = {key: value for key, value in self.cache.items()}
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)

            elif format_type.lower() == 'csv':
                import csv
                with open(filepath, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Key', 'Value', 'TTL'])
                    for key in self.cache.keys():
                        value = self.cache.get(key)
                        ttl = self.cache.ttl(key)
                        writer.writerow([key, json.dumps(value), ttl or 'None'])

            elif format_type.lower() == 'txt':
                with open(filepath, 'w') as f:
                    for key in self.cache.keys():
                        value = self.cache.get(key)
                        ttl = self.cache.ttl(key)
                        f.write(f"{key}: {value} (TTL: {ttl or 'None'})\n")

            else:
                print("Supported formats: json, csv, txt")
                return

            print(f"Cache exported to '{filepath}' in {format_type.upper()} format")

        except Exception as e:
            print(f"Error exporting cache: {e}")

    def do_info(self, args: str):
        """
        Show detailed cache information.
        Usage: info
        """
        stats = self.cache.get_stats()
        print("\nCache Information:")
        print("=" * 50)
        print(f"Type: LRU Cache with TTL")
        print(f"Max Size: {stats['capacity']}")
        print(f"Current Size: {stats['size']}")
        print(f"Load Factor: {stats['load_factor']:.1%}")
        print(f"Default TTL: {self.cache.default_ttl} seconds")
        print(f"Hit Rate: {stats['hit_rate']:.1%}")
        print(f"Total Operations: {stats['hits'] + stats['misses'] + stats['sets']}")
        print(f"Background Cleanup: Active")

    def do_quit(self, args: str):
        """Exit the CLI."""
        return self.do_exit(args)

    def do_exit(self, args: str):
        """Exit the CLI."""
        if self.monitoring:
            self.monitoring = False
            self.stop_monitor.set()
        print("Goodbye!")
        return True


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="LRU Cache with TTL - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Start interactive shell
  %(prog)s --max-size 256 --ttl 300     # Start with custom settings
  %(prog)s --load cache.json            # Load saved cache
  %(prog)s --command "set key value"    # Execute single command
  %(prog)s --batch commands.txt         # Execute batch commands
        """
    )

    parser.add_argument('--max-size', type=int, default=128,
                        help='Maximum cache size (default: 128)')
    parser.add_argument('--ttl', type=float, default=None,
                        help='Default TTL in seconds (default: no expiration)')
    parser.add_argument('--load', metavar='FILE',
                        help='Load cache from file on startup')
    parser.add_argument('--command', metavar='CMD',
                        help='Execute a single command and exit')
    parser.add_argument('--batch', metavar='FILE',
                        help='Execute commands from file and exit')
    parser.add_argument('--save-on-exit', metavar='FILE',
                        help='Save cache to file on exit')

    args = parser.parse_args()

    # Create cache with specified parameters
    cache = create_cache(max_size=args.max_size, default_ttl=args.ttl)

    # Load cache if specified
    if args.load:
        if cache.load_from_file(args.load):
            print(f"Loaded cache from '{args.load}'")
        else:
            print(f"Failed to load cache from '{args.load}'")

    # Create CLI instance
    cli = CacheCLI(cache)

    try:
        if args.command:
            # Execute single command
            cli.onecmd(args.command)
        elif args.batch:
            # Execute batch commands
            cli.onecmd(f"batch {args.batch}")
        else:
            # Start interactive shell
            cli.cmdloop()

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # Save cache if specified
        if args.save_on_exit:
            try:
                cache.save_to_file(args.save_on_exit)
                print(f"Saved cache to '{args.save_on_exit}'")
            except Exception as e:
                print(f"Failed to save cache: {e}")

        # Cleanup
        cache.close()


if __name__ == "__main__":
    main()