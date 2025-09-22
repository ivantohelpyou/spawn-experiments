# Date Format Validator - Implementation Specifications

## Overview
A Python date format validator that accepts MM/DD/YYYY and DD/MM/YYYY formats with comprehensive validation logic.

## API Specification

### Primary Function
```python
def validate_date(date_string, format_type="auto", min_year=1900, max_year=2100) -> bool
```

### Parameters
- `date_string` (str): Date string to validate
- `format_type` (str): Format interpretation ("auto", "us", "eu")
  - "auto": Attempt both US and EU formats
  - "us": MM/DD/YYYY interpretation
  - "eu": DD/MM/YYYY interpretation
- `min_year` (int): Minimum valid year (default: 1900)
- `max_year` (int): Maximum valid year (default: 2100)

### Return Value
- `bool`: True if date is valid, False otherwise

## Input Format Requirements

### Accepted Formats
1. **US Format (MM/DD/YYYY)**:
   - MM/DD/YYYY (e.g., "12/25/2023")
   - M/DD/YYYY (e.g., "1/25/2023")
   - MM/D/YYYY (e.g., "12/5/2023")
   - M/D/YYYY (e.g., "1/5/2023")

2. **EU Format (DD/MM/YYYY)**:
   - DD/MM/YYYY (e.g., "25/12/2023")
   - D/MM/YYYY (e.g., "5/12/2023")
   - DD/M/YYYY (e.g., "25/1/2023")
   - D/M/YYYY (e.g., "5/1/2023")

### Separator Requirements
- Only forward slash (/) separators accepted
- No other separators (dash, dot, space) supported

## Validation Logic

### Structure Validation
1. **Component Count**: Must have exactly 3 components separated by "/"
2. **Numeric Validation**: All components must be valid integers
3. **Range Validation**: Each component must be within logical ranges

### Date Logic Validation
1. **Month Validation**: 1-12 range
2. **Day Validation**: 1-31 range based on month
3. **Year Validation**: Within specified min_year to max_year range
4. **Leap Year Handling**: February 29th only valid in leap years
5. **Month-Day Constraints**:
   - January: 1-31 days
   - February: 1-28 days (1-29 in leap years)
   - March: 1-31 days
   - April: 1-30 days
   - May: 1-31 days
   - June: 1-30 days
   - July: 1-31 days
   - August: 1-31 days
   - September: 1-30 days
   - October: 1-31 days
   - November: 1-30 days
   - December: 1-31 days

### Leap Year Logic
A year is a leap year if:
- Divisible by 4 AND
- If divisible by 100, must also be divisible by 400

## Format Type Behavior

### "auto" Mode
1. Try US format (MM/DD/YYYY) interpretation first
2. If invalid, try EU format (DD/MM/YYYY) interpretation
3. Return True if either interpretation is valid
4. Handle ambiguous dates (e.g., "01/02/2023" could be Jan 2 or Feb 1)

### "us" Mode
- Only interpret as MM/DD/YYYY
- Return False if interpretation is invalid

### "eu" Mode
- Only interpret as DD/MM/YYYY
- Return False if interpretation is invalid

## Error Handling

### Invalid Input Cases
1. **Empty or None input**: Return False
2. **Non-string input**: Return False
3. **Malformed structure**: Wrong number of components, non-numeric components
4. **Out of range components**: Month > 12, day > 31, year outside range
5. **Invalid date logic**: Feb 30, Apr 31, Feb 29 in non-leap years

### Edge Cases
1. **Leading zeros**: "01/02/2023" should be valid
2. **Single digits**: "1/2/2023" should be valid
3. **Boundary years**: Test min_year and max_year boundaries
4. **Leap year boundaries**: Test Feb 29 in leap/non-leap years
5. **Month boundaries**: Test last day of each month

## Implementation Structure

### Core Components
1. **Input Parser**: Extract and validate numeric components
2. **Format Interpreter**: Determine month/day based on format_type
3. **Range Validator**: Check component ranges
4. **Date Logic Validator**: Validate actual date existence
5. **Leap Year Calculator**: Determine leap year status

### Helper Functions
```python
def _parse_date_components(date_string) -> tuple[int, int, int] | None
def _is_leap_year(year: int) -> bool
def _get_days_in_month(month: int, year: int) -> int
def _validate_us_format(month: int, day: int, year: int, min_year: int, max_year: int) -> bool
def _validate_eu_format(day: int, month: int, year: int, min_year: int, max_year: int) -> bool
def _validate_date_logic(month: int, day: int, year: int) -> bool
```

## Test Coverage Requirements

### Basic Functionality Tests
- Valid dates in both formats
- Invalid dates (structure and logic)
- Edge cases (leap years, month boundaries)

### Format Type Tests
- "auto" mode with unambiguous dates
- "auto" mode with ambiguous dates
- "us" mode specific behavior
- "eu" mode specific behavior

### Parameter Tests
- Custom year ranges
- Boundary testing for min_year/max_year
- Invalid parameter values

### Error Handling Tests
- Empty strings, None values
- Non-string inputs
- Malformed date strings
- Out of range values

## Performance Considerations
- Single pass parsing where possible
- Early exit on obviously invalid input
- Minimal regex usage (prefer string operations)
- No external dependencies

## Implementation Dependencies
- Python standard library only
- No third-party packages
- Compatible with Python 3.8+