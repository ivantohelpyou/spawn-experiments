"""
Date Format Validator - Test-First Development Implementation
Pure TDD approach with Red-Green-Refactor cycles.
"""

import re


def validate_date(date_string, format_type="auto", min_year=1900, max_year=2100):
    """
    Validate date strings in MM/DD/YYYY or DD/MM/YYYY formats.

    Args:
        date_string (str): Date string to validate
        format_type (str): "us" for MM/DD, "eu" for DD/MM, "auto" for both
        min_year (int): Minimum valid year (default: 1900)
        max_year (int): Maximum valid year (default: 2100)

    Returns:
        bool: True if valid date, False otherwise
    """
    if not date_string or not isinstance(date_string, str):
        return False

    # Basic pattern: 1-2 digits / 1-2 digits / 4 digits
    pattern = r'^(\d{1,2})/(\d{1,2})/(\d{4})$'
    match = re.match(pattern, date_string.strip())

    if not match:
        return False

    part1, part2, year = map(int, match.groups())

    # Year range check
    if year < min_year or year > max_year:
        return False

    # Try different format interpretations
    formats_to_try = []
    if format_type == "us":
        formats_to_try = [(part1, part2)]  # MM/DD
    elif format_type == "eu":
        formats_to_try = [(part2, part1)]  # DD/MM
    else:  # auto
        # For auto-detection, try both formats
        formats_to_try = [(part1, part2), (part2, part1)]

    # Test each format
    for month, day in formats_to_try:
        if _is_valid_date(month, day, year):
            return True

    return False


def _is_valid_date(month, day, year):
    """Check if the given month/day/year combination is valid."""
    # Basic range checks
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False

    # Days in each month
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Leap year adjustment
    if _is_leap_year(year):
        days_in_month[1] = 29

    # Check if day is valid for the month
    return day <= days_in_month[month - 1]


def _is_leap_year(year):
    """Check if a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


if __name__ == "__main__":
    # Test cases driven by TDD
    test_cases = [
        ("02/29/2020", True),   # Valid leap year
        ("02/29/2021", False),  # Invalid leap year
        ("13/01/2020", True),   # Auto-detects as EU format
        ("01/13/2020", True),   # Auto-detects as US format
        ("31/12/2020", True),   # Valid EU format
        ("12/31/2020", True),   # Valid US format
        ("2/5/2020", True),     # Valid single digits
        ("", False),            # Empty string
        ("abc", False),         # Invalid format
        ("32/01/2020", False),  # Invalid day
        ("02/30/2020", False),  # Feb 30 never valid
    ]

    print("Testing TDD date validator:")
    all_passed = True
    for test_input, expected in test_cases:
        result = validate_date(test_input)
        status = "" if result == expected else ""
        if result != expected:
            all_passed = False
        print(f"{status} '{test_input}' -> {result} (expected {expected})")

    print(f"\nAll tests {'PASSED' if all_passed else 'FAILED'}")