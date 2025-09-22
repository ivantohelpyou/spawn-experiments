#!/usr/bin/env python3
"""
Simple Email Validator Robustness Comparison

This script demonstrates robustness differences by testing edge cases that reveal
which validators are more permissive or strict than others.

Key Question: Which implementation accepts emails that others reject?
"""

import sys
import os

def find_experiment_directory():
    """Find the experiment directory, whether running from project root or experiment dir."""
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Try script directory first (when running from experiment directory)
    if os.path.basename(script_dir) == "1.501-email-validator":
        return script_dir

    # Try from current working directory (when running from project root)
    experiment_path = os.path.join(current_dir, "experiments", "1.501-email-validator")
    if os.path.exists(experiment_path):
        return experiment_path

    # Try relative to script location
    return script_dir

# Set base experiment directory
EXPERIMENT_DIR = find_experiment_directory()

def test_method1():
    """Test Method 1 - Multi-level validator"""
    try:
        method1_dir = os.path.join(EXPERIMENT_DIR, "1-immediate-implementation")
        if not os.path.exists(method1_dir):
            print(f"❌ Method 1 directory not found: {method1_dir}")
            return None
        sys.path.insert(0, method1_dir)
        from email_validator import EmailValidator, ValidationLevel

        validator_basic = EmailValidator(ValidationLevel.BASIC)
        validator_standard = EmailValidator(ValidationLevel.STANDARD)

        def method1_test(email):
            try:
                basic_result, _ = validator_basic.validate(email)
                standard_result, _ = validator_standard.validate(email)
                return {"basic": basic_result, "standard": standard_result}
            except:
                return {"basic": False, "standard": False}

        return method1_test
    except ImportError:
        return None

def test_method2():
    """Test Method 2 - Specification-driven"""
    try:
        method2_dir = os.path.join(EXPERIMENT_DIR, "2-specification-driven")
        if not os.path.exists(method2_dir):
            print(f"❌ Method 2 directory not found: {method2_dir}")
            return None
        sys.path.insert(0, method2_dir)
        from email_validator import validate_email

        def method2_test(email):
            try:
                result = validate_email(email)
                # Handle tuple returns (result, errors)
                if isinstance(result, tuple):
                    return result[0]
                return result
            except:
                return False

        return method2_test
    except ImportError:
        return None

def test_method3():
    """Test Method 3 - TDD"""
    try:
        method3_dir = os.path.join(EXPERIMENT_DIR, "3-test-first-development")
        if not os.path.exists(method3_dir):
            print(f"❌ Method 3 directory not found: {method3_dir}")
            return None
        sys.path.insert(0, method3_dir)
        from email_validator import is_valid_email

        def method3_test(email):
            try:
                return is_valid_email(email)
            except:
                return False

        return method3_test
    except ImportError:
        return None

def test_method4():
    """Test Method 4 - Validated test development"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        method4_dir = os.path.join(script_dir, "4-validated-test-development")
        sys.path.insert(0, method4_dir)
        from email_validator import validate_email

        def method4_test(email):
            try:
                result = validate_email(email)
                # Handle tuple returns (result, errors)
                if isinstance(result, tuple):
                    return result[0]
                return result
            except:
                return False

        return method4_test
    except ImportError:
        return None

def main():
    print("🧪 Email Validator Robustness Comparison")
    print("=" * 50)

    # Load validators
    validators = {
        "Method 1": test_method1(),
        "Method 2": test_method2(),
        "Method 3": test_method3(),
        "Method 4": test_method4()
    }

    loaded_validators = {k: v for k, v in validators.items() if v is not None}

    if not loaded_validators:
        print("❌ No validators could be loaded!")
        return

    print(f"✅ Loaded {len(loaded_validators)} validators: {', '.join(loaded_validators.keys())}")
    print()

    # Test cases designed to show robustness differences
    test_cases = [
        # Basic cases (should all pass)
        ("user@domain.com", "Basic valid email"),
        ("test@example.org", "Another valid email"),

        # Edge cases that might differ
        ("a@b.co", "Minimal valid email"),
        ("user@domain", "Missing TLD"),
        ("user..name@domain.com", "Consecutive dots in local"),
        (".user@domain.com", "Leading dot in local"),
        ("user.@domain.com", "Trailing dot in local"),
        ("user@domain..com", "Consecutive dots in domain"),
        ("user@.domain.com", "Leading dot in domain"),

        # Length cases
        ("a" * 65 + "@domain.com", "Local part too long (65 chars)"),
        ("user@" + "a" * 250 + ".com", "Domain too long"),

        # Special characters
        ("user@domain.c", "Single char TLD"),
        ("user name@domain.com", "Space in local part"),
        ("user@domain .com", "Space in domain"),

        # Advanced cases (Method 1 might accept)
        ("user@[192.168.1.1]", "IP address domain"),
        ('"user name"@domain.com', "Quoted local part"),

        # Obviously invalid
        ("", "Empty string"),
        ("plaintext", "No @ symbol"),
        ("user@@domain.com", "Double @ symbol"),
        ("user@", "Missing domain"),
        ("@domain.com", "Missing local"),
    ]

    print("ROBUSTNESS TEST RESULTS")
    print("-" * 30)
    print()

    disagreements = []

    for email, description in test_cases:
        print(f"📧 {description}: '{email}'")

        results = {}
        for name, validator in loaded_validators.items():
            if name == "Method 1" and validator:
                # Method 1 has multiple levels
                result = validator(email)
                if isinstance(result, dict):
                    # Show individual levels and overall result
                    basic = result.get("basic", False)
                    standard = result.get("standard", False)
                    overall = basic or standard
                    results[name] = overall
                    print(f"   {name}: {overall} (basic:{basic}, standard:{standard})")
                else:
                    results[name] = result
                    print(f"   {name}: {result}")
            else:
                result = validator(email)
                # Ensure result is boolean
                if isinstance(result, tuple):
                    result = result[0]
                results[name] = bool(result)
                print(f"   {name}: {result}")

        # Check for disagreements
        unique_results = set(results.values())
        if len(unique_results) > 1:
            disagreements.append((email, description, results))
            print("   ⚠️  DISAGREEMENT DETECTED!")

        print()

    # Summary analysis
    print("ROBUSTNESS ANALYSIS")
    print("=" * 30)
    print()

    if disagreements:
        print(f"🔍 Found {len(disagreements)} cases where validators disagree:")
        print()

        for email, description, results in disagreements:
            print(f"📧 {description}: '{email}'")
            accepts = [name for name, result in results.items() if result]
            rejects = [name for name, result in results.items() if not result]

            if accepts:
                print(f"   ✅ ACCEPTS: {', '.join(accepts)}")
            if rejects:
                print(f"   ❌ REJECTS: {', '.join(rejects)}")
            print()

        # Calculate permissiveness ranking
        print("PERMISSIVENESS RANKING:")
        print("(Higher acceptance rate = more permissive = potentially less robust)")
        print()

        validator_stats = {}
        for name in loaded_validators.keys():
            accepts = sum(1 for _, _, results in disagreements if results.get(name, False))
            total_disagreements = len(disagreements)
            validator_stats[name] = accepts / total_disagreements if total_disagreements > 0 else 0

        sorted_validators = sorted(validator_stats.items(), key=lambda x: x[1], reverse=True)

        for i, (name, acceptance_rate) in enumerate(sorted_validators, 1):
            print(f"{i}. {name}: {acceptance_rate:.1%} acceptance on disputed cases")

        print()
        print("🎯 ROBUSTNESS ORDERING (most to least robust):")
        for i, (name, _) in enumerate(reversed(sorted_validators), 1):
            robustness = "🛡️" if i == 1 else "⚠️" if i == len(sorted_validators) else "🔶"
            print(f"{i}. {robustness} {name}")

    else:
        print("✅ All validators agree on all test cases!")
        print("   This suggests similar robustness levels.")

    print()
    print("KEY INSIGHTS:")
    print("• More permissive validators may be easier to use but less secure")
    print("• More strict validators may reject valid emails but are more secure")
    print("• Choice depends on your security vs. usability requirements")
    print()
    print("🔒 For high security: Choose stricter validators")
    print("👥 For user-facing apps: Balance security with usability")

if __name__ == "__main__":
    main()