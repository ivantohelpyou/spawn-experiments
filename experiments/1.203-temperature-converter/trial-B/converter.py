
import sys

def convert_temperature(value, source_unit, target_unit):
    """Converts temperature from source_unit to target_unit."""
    source_unit = source_unit.lower()
    target_unit = target_unit.lower()

    # Convert source to Celsius first
    if source_unit in ('c', 'celsius'):
        celsius = value
    elif source_unit in ('f', 'fahrenheit'):
        celsius = (value - 32) * 5/9
    elif source_unit in ('k', 'kelvin'):
        celsius = value - 273.15
    else:
        raise ValueError("Invalid source unit")

    # Convert Celsius to target
    if target_unit in ('c', 'celsius'):
        return celsius
    elif target_unit in ('f', 'fahrenheit'):
        return celsius * 9/5 + 32
    elif target_unit in ('k', 'kelvin'):
        return celsius + 273.15
    else:
        raise ValueError("Invalid target unit")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python converter.py <value> <source_unit> <target_unit>", file=sys.stderr)
        sys.exit(1)

    try:
        value = float(sys.argv[1])
        source_unit = sys.argv[2]
        target_unit = sys.argv[3]
        result = convert_temperature(value, source_unit, target_unit)
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
