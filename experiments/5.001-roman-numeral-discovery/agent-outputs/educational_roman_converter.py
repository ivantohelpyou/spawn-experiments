"""
Educational Roman Numeral Converter
Designed specifically for middle school students to understand the conversion process.

This implementation prioritizes clarity and educational value over performance,
showing step-by-step how Roman numeral conversion works.
"""

def int_to_roman_educational(num, show_steps=True):
    """
    Convert integer to Roman numeral with educational step-by-step explanation.

    Args:
        num (int): Number to convert (1-3999)
        show_steps (bool): Whether to print conversion steps

    Returns:
        str: Roman numeral representation
    """
    if not isinstance(num, int) or num < 1 or num > 3999:
        raise ValueError("Number must be an integer between 1 and 3999")

    if show_steps:
        print(f"\n=== Converting {num} to Roman Numerals ===")
        print("We'll break down the number using Roman numeral values from largest to smallest:")
        print("1000=M, 900=CM, 500=D, 400=CD, 100=C, 90=XC, 50=L, 40=XL, 10=X, 9=IX, 5=V, 4=IV, 1=I")
        print()

    # Roman numeral mapping from largest to smallest (including subtractive cases)
    roman_map = [
        (1000, 'M'),   # 1000 = M
        (900, 'CM'),   # 900 = CM (1000-100)
        (500, 'D'),    # 500 = D
        (400, 'CD'),   # 400 = CD (500-100)
        (100, 'C'),    # 100 = C
        (90, 'XC'),    # 90 = XC (100-10)
        (50, 'L'),     # 50 = L
        (40, 'XL'),    # 40 = XL (50-10)
        (10, 'X'),     # 10 = X
        (9, 'IX'),     # 9 = IX (10-1)
        (5, 'V'),      # 5 = V
        (4, 'IV'),     # 4 = IV (5-1)
        (1, 'I')       # 1 = I
    ]

    result = ""
    remaining = num

    for value, numeral in roman_map:
        # How many times does this value fit into our remaining number?
        count = remaining // value

        if count > 0:
            # Add this numeral the appropriate number of times
            roman_part = numeral * count
            result += roman_part

            if show_steps:
                print(f"Step: {remaining} ÷ {value} = {count} remainder {remaining % value}")
                print(f"      Add '{roman_part}' to result")
                print(f"      Result so far: '{result}'")
                print(f"      Remaining to convert: {remaining % value}")
                print()

            # Subtract what we've used
            remaining = remaining % value

    if show_steps:
        print(f"Final result: {num} = {result}")
        print("=" * 40)

    return result


def roman_to_int_educational(roman, show_steps=True):
    """
    Convert Roman numeral to integer with educational step-by-step explanation.

    Args:
        roman (str): Roman numeral to convert
        show_steps (bool): Whether to print conversion steps

    Returns:
        int: Integer value
    """
    if not isinstance(roman, str) or not roman.strip():
        raise ValueError("Roman numeral must be a non-empty string")

    # Clean up input
    roman = roman.upper().strip()

    if show_steps:
        print(f"\n=== Converting '{roman}' to Integer ===")
        print("Roman numeral values: I=1, V=5, X=10, L=50, C=100, D=500, M=1000")
        print("Rule: If a smaller numeral comes before a larger one, subtract it.")
        print("      Otherwise, add it.")
        print()

    # Roman numeral values
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    # Validate all characters are valid Roman numerals
    for char in roman:
        if char not in roman_values:
            raise ValueError(f"Invalid character '{char}' in Roman numeral")

    total = 0
    i = 0

    while i < len(roman):
        current_char = roman[i]
        current_value = roman_values[current_char]

        # Look ahead to see if we need to subtract (subtractive notation)
        if i + 1 < len(roman):
            next_char = roman[i + 1]
            next_value = roman_values[next_char]

            if current_value < next_value:
                # Subtractive case: IV, IX, XL, XC, CD, CM
                subtract_value = next_value - current_value
                total += subtract_value

                if show_steps:
                    print(f"Step: Found '{current_char}{next_char}' = {next_value} - {current_value} = {subtract_value}")
                    print(f"      Add {subtract_value} to total")
                    print(f"      Running total: {total}")
                    print()

                i += 2  # Skip both characters
                continue

        # Regular case: just add the value
        total += current_value

        if show_steps:
            print(f"Step: Found '{current_char}' = {current_value}")
            print(f"      Add {current_value} to total")
            print(f"      Running total: {total}")
            print()

        i += 1

    if show_steps:
        print(f"Final result: '{roman}' = {total}")
        print("=" * 40)

    return total


def demonstrate_roman_numerals():
    """Demonstrate the educational Roman numeral converter with examples."""
    print("EDUCATIONAL ROMAN NUMERAL CONVERTER")
    print("=" * 50)

    # Example numbers that show different conversion patterns
    demo_numbers = [4, 9, 27, 58, 194, 421, 1984]

    print("\nDEMONSTRATION: Integer to Roman")
    print("=" * 50)

    for num in demo_numbers:
        try:
            roman = int_to_roman_educational(num, show_steps=True)
            print()
        except Exception as e:
            print(f"Error converting {num}: {e}")

    print("\nDEMONSTRATION: Roman to Integer")
    print("=" * 50)

    demo_romans = ['IV', 'IX', 'XXVII', 'LVIII', 'CXCIV', 'CDXXI', 'MCMLXXXIV']

    for roman in demo_romans:
        try:
            num = roman_to_int_educational(roman, show_steps=True)
            print()
        except Exception as e:
            print(f"Error converting {roman}: {e}")

    # Show that conversion is bidirectional
    print("\nBIDIRECTIONAL CONVERSION TEST")
    print("=" * 30)
    test_number = 1776
    print(f"Original number: {test_number}")
    roman_result = int_to_roman_educational(test_number, show_steps=False)
    print(f"To Roman: {roman_result}")
    back_to_int = roman_to_int_educational(roman_result, show_steps=False)
    print(f"Back to integer: {back_to_int}")
    print(f"Conversion successful: {test_number == back_to_int}")


if __name__ == "__main__":
    demonstrate_roman_numerals()