def validate_date(date_string, format_type="auto", min_year=1900, max_year=2100):
    """
    Validate date string in MM/DD/YYYY or DD/MM/YYYY format.

    Args:
        date_string (str): Date string to validate
        format_type (str): "us" (MM/DD), "eu" (DD/MM), or "auto" for detection
        min_year (int): Minimum valid year (default: 1900)
        max_year (int): Maximum valid year (default: 2100)

    Returns:
        bool: True if valid date, False otherwise
    """
    if not date_string:
        return False

    # Split by forward slash
    parts = date_string.split('/')
    if len(parts) != 3:
        return False

    # Try to convert to integers
    try:
        part1, part2, year = [int(part) for part in parts]
    except ValueError:
        return False

    # Validate year range
    if year < min_year or year > max_year:
        return False

    # Determine month and day based on format
    if format_type == "us":
        month, day = part1, part2
    elif format_type == "eu":
        day, month = part1, part2
    elif format_type == "auto":
        # Auto-detection logic
        month, day = _detect_format_and_extract(part1, part2)
        if month is None:  # Invalid in both formats
            return False
    else:
        return False  # Invalid format_type

    # Validate month range
    if month < 1 or month > 12:
        return False

    # Validate day range
    if day < 1:
        return False

    # Get days in month
    days_in_month = _get_days_in_month(month, year)
    if day > days_in_month:
        return False

    return True


def _detect_format_and_extract(part1, part2):
    """
    Detect format and extract month/day from ambiguous input.
    Returns (month, day) or (None, None) if invalid in both formats.
    """
    # If part1 > 12, must be DD/MM format
    if part1 > 12:
        if part2 >= 1 and part2 <= 12:
            return part2, part1  # month, day
        else:
            return None, None

    # If part2 > 12, must be MM/DD format
    if part2 > 12:
        if part1 >= 1 and part1 <= 12:
            return part1, part2  # month, day
        else:
            return None, None

    # Both parts <= 12, ambiguous - default to US format (MM/DD)
    if part1 >= 1 and part1 <= 12 and part2 >= 1 and part2 <= 12:
        return part1, part2  # month, day (US format)

    return None, None


def _get_days_in_month(month, year):
    """Get number of days in a given month/year."""
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if month == 2 and _is_leap_year(year):
        return 29

    return days_per_month[month - 1]


def _is_leap_year(year):
    """Check if year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)