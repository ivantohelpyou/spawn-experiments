#!/usr/bin/env python3
"""
Demo Script for 1.501.1: Email Validator Severed Branch Timing
"""
import subprocess
import sys
from pathlib import Path

def test_method(method_dir, name):
    print(f"\n=== Testing {name} ===")

    validator_file = method_dir / "email_validator.py"
    if not validator_file.exists():
        print(f"ERROR: No email_validator.py in {method_dir}")
        return False

    # Test cases
    valid_emails = [
        "user@domain.com",
        "user.name@domain.co.uk",
        "user+tag@subdomain.domain.com",
        "user_name@domain-name.org"
    ]

    invalid_emails = [
        "user@domain",  # no TLD
        "user@@domain.com",  # double @
        "user@domain..com",  # consecutive dots
        "user.@domain.com",  # local part ends with dot
        ".user@domain.com",  # local part starts with dot
        "",  # empty string
        "invalid"  # no @
    ]

    try:
        # Import the validation function
        import importlib.util
        spec = importlib.util.spec_from_file_location("email_validator", validator_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        validate_email = getattr(module, 'validate_email')

        # Test valid emails
        for email in valid_emails:
            if not validate_email(email):
                print(f"FAIL: Valid email rejected: {email}")
                return False
        print(f"PASS: All {len(valid_emails)} valid emails accepted")

        # Test invalid emails
        for email in invalid_emails:
            if validate_email(email):
                print(f"FAIL: Invalid email accepted: {email}")
                return False
        print(f"PASS: All {len(invalid_emails)} invalid emails rejected")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("=== Demo for 1.501.1: Email Validator Severed Branch ===")

    base_dir = Path(__file__).parent
    methods = [
        ("1-immediate-implementation", "Method 1: Immediate"),
        ("2-specification-driven", "Method 2: Spec-driven"),
        ("3-test-first-development", "Method 3: TDD"),
        ("4-adaptive-tdd-v4.1", "Method 4: Adaptive TDD")
    ]

    results = {}
    for folder, name in methods:
        method_dir = base_dir / folder
        if method_dir.exists():
            results[name] = test_method(method_dir, name)
        else:
            print(f"\nERROR: {method_dir} not found")
            results[name] = False

    print(f"\n=== SUMMARY ===")
    working = 0
    for name, status in results.items():
        print(f"{name}: {'✅ WORKING' if status else '❌ FAILED'}")
        if status:
            working += 1

    print(f"\nResult: {working}/{len(results)} implementations working")
    return 0 if working == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())