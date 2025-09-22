# Date Format Validator - Requirements Analysis

## Core Requirements
- **API**: `validate_date(date_string, format_type="auto", min_year=1900, max_year=2100)`
- **Formats**: MM/DD/YYYY, DD/MM/YYYY, M/D/YYYY, D/M/YYYY
- **Separator**: Forward slashes (/) only
- **Date Logic**: Validate actual dates (no Feb 30, proper leap years)
- **Return**: Boolean (True/False)
- **Dependencies**: Python standard library only

## Format Types
1. **"auto"**: Attempt to detect format automatically
2. **"us"**: MM/DD/YYYY interpretation
3. **"eu"**: DD/MM/YYYY interpretation

## Key Test Scenarios

### Valid Dates
- MM/DD/YYYY: "12/25/2023", "01/15/2000"
- M/D/YYYY: "1/5/2023", "12/5/2023"
- DD/MM/YYYY: "25/12/2023", "15/01/2000"
- D/M/YYYY: "5/1/2023", "5/12/2023"

### Invalid Dates
- Feb 30: "02/30/2023", "30/02/2023"
- Feb 29 non-leap year: "02/29/2023", "29/02/2023"
- Month > 12: "13/01/2023", "01/13/2023" (ambiguous)
- Day > 31: "32/01/2023", "01/32/2023"
- Month 0: "00/01/2023", "01/00/2023"
- Day 0: "01/00/2023", "00/01/2023"

### Leap Year Logic
- Valid: "02/29/2024", "29/02/2024" (2024 is leap year)
- Invalid: "02/29/2023", "29/02/2023" (2023 is not leap year)
- Century years: "02/29/2000" (valid), "02/29/1900" (invalid)

### Edge Cases
- Empty string: ""
- None input: None
- Wrong separator: "12-25-2023", "12.25.2023"
- Non-numeric: "ab/cd/efgh"
- Incomplete: "12/25", "12/25/"
- Extra parts: "12/25/2023/extra"
- Year out of range: "12/25/1899", "12/25/2101"

### Format Detection (Auto Mode)
- Unambiguous dates: "25/12/2023" (must be DD/MM), "12/25/2023" (could be either)
- Ambiguous dates: "01/02/2023" (could be Jan 2 or Feb 1)

## Implementation Strategy
1. Input validation and parsing
2. Format detection logic
3. Date component validation
4. Leap year calculation
5. Date existence validation