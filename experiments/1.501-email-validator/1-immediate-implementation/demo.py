"""
Interactive demonstration and CLI tool for the Email Validator.

This module provides both an interactive CLI and practical usage examples
for the EmailValidator functionality.
"""

import sys
import json
from typing import List, Dict, Any

from email_validator import (
    EmailValidator, ValidationLevel, create_validator,
    is_valid_email, validate_email
)


class EmailValidatorCLI:
    """Interactive command-line interface for email validation."""

    def __init__(self):
        """Initialize the CLI."""
        self.validator = EmailValidator(ValidationLevel.STANDARD)
        self.validation_level = "standard"

    def run(self):
        """Run the interactive CLI."""
        print("=" * 60)
        print("INTERACTIVE EMAIL VALIDATOR")
        print("=" * 60)
        print("\nCommands:")
        print("  validate <email>     - Validate a single email")
        print("  batch <email1,email2,...> - Validate multiple emails")
        print("  level <basic|standard|strict|rfc> - Set validation level")
        print("  details <email>      - Get detailed analysis")
        print("  demo                 - Run demonstration")
        print("  help                 - Show this help")
        print("  quit                 - Exit")
        print("\nCurrent validation level: " + self.validation_level)
        print("-" * 60)

        while True:
            try:
                command = input("\n> ").strip()
                if not command:
                    continue

                parts = command.split(' ', 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if cmd == 'quit' or cmd == 'exit':
                    print("Goodbye!")
                    break
                elif cmd == 'help':
                    self._show_help()
                elif cmd == 'validate':
                    self._validate_email(args)
                elif cmd == 'batch':
                    self._validate_batch(args)
                elif cmd == 'level':
                    self._set_level(args)
                elif cmd == 'details':
                    self._show_details(args)
                elif cmd == 'demo':
                    self._run_demo()
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _show_help(self):
        """Show help information."""
        print("\nEmail Validator CLI Help")
        print("-" * 30)
        print("Commands:")
        print("  validate <email>")
        print("    Example: validate user@example.com")
        print("\n  batch <email1,email2,...>")
        print("    Example: batch user@test.com,invalid@,good@example.org")
        print("\n  level <basic|standard|strict|rfc>")
        print("    Example: level strict")
        print("\n  details <email>")
        print("    Example: details test.user+tag@example.co.uk")
        print("\n  demo")
        print("    Run a comprehensive demonstration")
        print("\nValidation Levels:")
        print("  basic       - Simple regex validation")
        print("  standard    - Standard validation with common rules")
        print("  strict      - Strict validation with TLD checking")
        print("  rfc         - RFC 5321/5322 compliant validation")

    def _validate_email(self, email: str):
        """Validate a single email."""
        if not email:
            print("Please provide an email address.")
            return

        email = email.strip()
        is_valid, errors = self.validator.validate(email)

        print(f"\nEmail: {email}")
        print(f"Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
        print(f"Level: {self.validation_level}")

        if errors:
            print("Errors:")
            for error in errors:
                print(f"  • {error}")

    def _validate_batch(self, emails_str: str):
        """Validate multiple emails."""
        if not emails_str:
            print("Please provide comma-separated email addresses.")
            return

        emails = [email.strip() for email in emails_str.split(',')]
        results = self.validator.validate_batch(emails)

        print(f"\nBatch Validation Results ({self.validation_level} level):")
        print("-" * 50)

        valid_count = 0
        for email, (is_valid, errors) in results.items():
            status = "✓ VALID" if is_valid else "✗ INVALID"
            print(f"{status:12} {email}")

            if errors:
                for error in errors:
                    print(f"             └─ {error}")

            if is_valid:
                valid_count += 1

        print(f"\nSummary: {valid_count}/{len(emails)} emails are valid")

    def _set_level(self, level: str):
        """Set the validation level."""
        if not level:
            print(f"Current level: {self.validation_level}")
            print("Available levels: basic, standard, strict, rfc")
            return

        level = level.lower().strip()
        level_map = {
            "basic": ValidationLevel.BASIC,
            "standard": ValidationLevel.STANDARD,
            "strict": ValidationLevel.STRICT,
            "rfc": ValidationLevel.RFC_COMPLIANT,
            "rfc_compliant": ValidationLevel.RFC_COMPLIANT
        }

        if level in level_map:
            self.validation_level = level
            self.validator = EmailValidator(level_map[level])
            print(f"Validation level set to: {level}")
        else:
            print(f"Invalid level: {level}")
            print("Available levels: basic, standard, strict, rfc")

    def _show_details(self, email: str):
        """Show detailed analysis of an email."""
        if not email:
            print("Please provide an email address.")
            return

        email = email.strip()
        details = self.validator.get_validation_details(email)

        print(f"\nDetailed Analysis for: {email}")
        print("-" * 50)
        print(f"Valid: {details['is_valid']}")
        print(f"Local Part: {details['local_part']}")
        print(f"Domain Part: {details['domain_part']}")

        if details['domain_labels']:
            print(f"Domain Labels: {' → '.join(details['domain_labels'])}")

        if details['tld']:
            print(f"TLD: {details['tld']}")

        length_info = details['length_info']
        print(f"\nLength Information:")
        print(f"  Total Length: {length_info['total_length']}")
        print(f"  Local Length: {length_info['local_length']}")
        print(f"  Domain Length: {length_info['domain_length']}")
        print(f"  Within Limits: {length_info['within_limits']}")

        if details['warnings']:
            print(f"\nWarnings:")
            for warning in details['warnings']:
                print(f"  ⚠ {warning}")

        if details['errors']:
            print(f"\nErrors:")
            for error in details['errors']:
                print(f"  • {error}")

    def _run_demo(self):
        """Run the demonstration."""
        run_comprehensive_demo()


def run_comprehensive_demo():
    """Run a comprehensive demonstration of all features."""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE EMAIL VALIDATOR DEMONSTRATION")
    print("=" * 60)

    # Example 1: Basic validation
    print("\n1. BASIC VALIDATION EXAMPLES")
    print("-" * 30)

    basic_examples = [
        ("user@example.com", "Simple valid email"),
        ("test.email+tag@domain.co.uk", "Email with tags and subdomains"),
        ("invalid.email", "Missing @ symbol"),
        ("user@domain", "Missing TLD"),
        ("user..double@example.com", "Double dots in local part")
    ]

    for email, description in basic_examples:
        is_valid = is_valid_email(email)
        status = "✓" if is_valid else "✗"
        print(f"{status} {email:30} ({description})")

    # Example 2: Validation levels comparison
    print(f"\n2. VALIDATION LEVELS COMPARISON")
    print("-" * 30)

    test_emails = [
        "user@example.com",
        "test@unknown.tld",
        "user.with.many.dots@example.com",
        '"quoted.string"@example.com'
    ]

    levels = ["basic", "standard", "strict", "rfc_compliant"]

    for email in test_emails:
        print(f"\nEmail: {email}")
        for level in levels:
            validator = create_validator(level)
            is_valid = validator.is_valid(email)
            status = "✓" if is_valid else "✗"
            print(f"  {level:12}: {status}")

    # Example 3: Detailed analysis
    print(f"\n3. DETAILED ANALYSIS EXAMPLE")
    print("-" * 30)

    validator = EmailValidator(ValidationLevel.STANDARD)
    sample_email = "john.doe+newsletter@company.co.uk"
    details = validator.get_validation_details(sample_email)

    print(f"Analyzing: {sample_email}")
    print(f"  Valid: {details['is_valid']}")
    print(f"  Local Part: '{details['local_part']}'")
    print(f"  Domain: '{details['domain_part']}'")
    print(f"  TLD: '{details['tld']}'")
    print(f"  Labels: {' → '.join(details['domain_labels'])}")

    # Example 4: Error handling
    print(f"\n4. ERROR HANDLING EXAMPLES")
    print("-" * 30)

    error_examples = [
        "user@domain",
        "user..double@example.com",
        "@missing-local.com",
        "missing-at-symbol.com",
        "a" * 70 + "@example.com"  # Too long local part
    ]

    for email in error_examples:
        is_valid, errors = validate_email(email)
        print(f"\n✗ {email}")
        for error in errors:
            print(f"   └─ {error}")

    # Example 5: Batch validation
    print(f"\n5. BATCH VALIDATION EXAMPLE")
    print("-" * 30)

    batch_emails = [
        "user1@example.com",
        "user2@test.org",
        "invalid@",
        "user3@company.co.uk",
        "bad..email@domain.com"
    ]

    validator = EmailValidator(ValidationLevel.STANDARD)
    results = validator.validate_batch(batch_emails)

    valid_count = 0
    for email, (is_valid, errors) in results.items():
        status = "✓" if is_valid else "✗"
        print(f"{status} {email}")
        if errors:
            print(f"   Errors: {'; '.join(errors)}")
        if is_valid:
            valid_count += 1

    print(f"\nResult: {valid_count}/{len(batch_emails)} emails are valid")

    # Example 6: Real-world scenarios
    print(f"\n6. REAL-WORLD SCENARIOS")
    print("-" * 30)

    scenarios = [
        ("admin@company.com", "Corporate email"),
        ("user+spam@gmail.com", "Gmail with tag"),
        ("firstname.lastname@university.edu", "Academic email"),
        ("user@subdomain.example.org", "Subdomain email"),
        ("contact@startup.io", "Modern TLD"),
        ("support@e-commerce-site.co.uk", "Hyphenated domain"),
        ("user@[192.168.1.1]", "IP address domain"),
        ("test@localhost", "Local domain (invalid)")
    ]

    for email, scenario in scenarios:
        is_valid, errors = validate_email(email, "standard")
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:10} {email:30} ({scenario})")

    print(f"\n7. PERFORMANCE TEST")
    print("-" * 30)

    import time

    # Test with many emails
    test_count = 1000
    test_emails_cycle = [
        "user@example.com",
        "test@domain.org",
        "invalid@",
        "user.name@company.co.uk"
    ]

    start_time = time.time()
    validator = EmailValidator(ValidationLevel.STANDARD)

    for i in range(test_count):
        email = test_emails_cycle[i % len(test_emails_cycle)]
        validator.is_valid(email)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Validated {test_count} emails in {duration:.3f} seconds")
    print(f"Rate: {test_count/duration:.0f} emails/second")


def main():
    """Main entry point for the demo script."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "cli":
            cli = EmailValidatorCLI()
            cli.run()
        elif command == "demo":
            run_comprehensive_demo()
        elif command == "test":
            # Quick test mode
            test_emails = sys.argv[2:] if len(sys.argv) > 2 else [
                "user@example.com",
                "invalid@",
                "test.email+tag@domain.co.uk"
            ]

            print("Quick Email Validation Test")
            print("-" * 30)

            for email in test_emails:
                is_valid, errors = validate_email(email)
                status = "✓ VALID" if is_valid else "✗ INVALID"
                print(f"{status} {email}")
                if errors:
                    for error in errors:
                        print(f"   └─ {error}")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python demo.py [cli|demo|test] [emails...]")
    else:
        print("Email Validator Demo")
        print("=" * 20)
        print("Usage:")
        print("  python demo.py cli     - Interactive CLI")
        print("  python demo.py demo    - Run demonstration")
        print("  python demo.py test [emails...] - Quick test")
        print("\nExample:")
        print("  python demo.py test user@example.com invalid@")


if __name__ == "__main__":
    main()