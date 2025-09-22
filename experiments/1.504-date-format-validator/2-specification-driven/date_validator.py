"""
Date Format Validator - Specification-Driven Implementation

A Python date format validator that accepts MM/DD/YYYY and DD/MM/YYYY formats
with comprehensive validation logic. Follows specification-driven design.
"""

from typing import Optional, Tuple


def _parse_date_components(date_string: str) -> Optional[Tuple[int, int, int]]:
    """
    Parse date string into numeric components.

    Args:
        date_string: Date string to parse

    Returns:
        tuple[int, int, int]: (component1, component2, year) or None if invalid

    Handles:
    - Input validation (string type, not empty)
    - Component splitting on '/'
    - Numeric conversion with error handling
    - Basic range checks (positive integers)
    """
    if not isinstance(date_string, str) or not date_string.strip():
        return None

    parts = date_string.strip().split('/')
    if len(parts) != 3:
        return None

    try:
        components = [int(part) for part in parts]
        # Basic positive integer check
        if any(comp <= 0 for comp in components):
            return None
        return tuple(components)
    except ValueError:
        return None


def _is_leap_year(year: int) -> bool:
    """
    Determine if year is a leap year.

    Logic: divisible by 4, except century years must be divisible by 400

    Args:
        year: Year to check

    Returns:
        bool: True if leap year, False otherwise
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _get_days_in_month(month: int, year: int) -> int:
    """
    Get number of days in specified month/year.

    Handles leap year logic for February.

    Args:
        month: Month (1-12)
        year: Year

    Returns:
        int: Number of days in the month
    """
    if not (1 <= month <= 12):
        return 0

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if month == 2 and _is_leap_year(year):
        return 29

    return days_in_month[month - 1]


def _validate_date_logic(month: int, day: int, year: int) -> bool:
    """
    Validate that the month/day/year combination represents a real date.

    Args:
        month: Month (1-12)
        day: Day (1-31)
        year: Year

    Returns:
        bool: True if valid date, False otherwise
    """
    # Month range check
    if not (1 <= month <= 12):
        return False

    # Day range check based on month
    max_days = _get_days_in_month(month, year)
    if not (1 <= day <= max_days):
        return False

    return True


def _validate_us_format(month: int, day: int, year: int, min_year: int, max_year: int) -> bool:
    """
    Validate date assuming US format (MM/DD/YYYY).

    Args:
        month: Month component (1-12)
        day: Day component (1-31)
        year: Year component
        min_year: Minimum valid year
        max_year: Maximum valid year

    Returns:
        bool: True if valid US format date, False otherwise
    """
    # Year range check
    if not (min_year <= year <= max_year):
        return False

    # Validate date logic
    return _validate_date_logic(month, day, year)


def _validate_eu_format(day: int, month: int, year: int, min_year: int, max_year: int) -> bool:
    """
    Validate date assuming EU format (DD/MM/YYYY).

    Args:
        day: Day component (1-31)
        month: Month component (1-12)
        year: Year component
        min_year: Minimum valid year
        max_year: Maximum valid year

    Returns:
        bool: True if valid EU format date, False otherwise
    """
    # Year range check
    if not (min_year <= year <= max_year):
        return False

    # Validate date logic (note: month and day are swapped compared to US)
    return _validate_date_logic(month, day, year)


def validate_date(date_string, format_type="auto", min_year=1900, max_year=2100) -> bool:
    """
    Main validation function with format interpretation logic.

    Args:
        date_string (str): Date string to validate
        format_type (str): Format interpretation ("auto", "us", "eu")
            - "auto": Attempt both US and EU formats
            - "us": MM/DD/YYYY interpretation
            - "eu": DD/MM/YYYY interpretation
        min_year (int): Minimum valid year (default: 1900)
        max_year (int): Maximum valid year (default: 2100)

    Returns:
        bool: True if date is valid, False otherwise

    Flow:
    1. Parse components
    2. Apply format-specific validation based on format_type
    3. Return boolean result
    """
    # Parse input into components
    components = _parse_date_components(date_string)
    if components is None:
        return False

    comp1, comp2, comp3 = components
    year = comp3  # Year is always the third component

    # Validate based on format type
    if format_type == "us":
        # US format: MM/DD/YYYY
        return _validate_us_format(comp1, comp2, year, min_year, max_year)

    elif format_type == "eu":
        # EU format: DD/MM/YYYY
        return _validate_eu_format(comp1, comp2, year, min_year, max_year)

    elif format_type == "auto":
        # Try US format first
        if _validate_us_format(comp1, comp2, year, min_year, max_year):
            return True

        # Fallback to EU format
        return _validate_eu_format(comp1, comp2, year, min_year, max_year)

    else:
        # Invalid format_type
        return False