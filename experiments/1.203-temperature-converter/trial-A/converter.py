import sys

def get_unit(unit):
    unit = unit.lower()
    if unit in ['c', 'celsius']:
        return 'c'
    elif unit in ['f', 'fahrenheit']:
        return 'f'
    elif unit in ['k', 'kelvin']:
        return 'k'
    return None

def to_celsius(value, unit):
    if unit == 'c':
        return value
    elif unit == 'f':
        return (value - 32) * 5/9
    elif unit == 'k':
        return value - 273.15

def from_celsius(value, unit):
    if unit == 'c':
        return value
    elif unit == 'f':
        return (value * 9/5) + 32
    elif unit == 'k':
        return value + 273.15

def convert(value, source_unit, target_unit):
    s_unit = get_unit(source_unit)
    t_unit = get_unit(target_unit)
    if s_unit is None or t_unit is None:
        raise ValueError("Invalid unit")
    celsius_value = to_celsius(value, s_unit)
    return from_celsius(celsius_value, t_unit)

if __name__ == "__main__":
    # ./converter.py 32 f c
    if len(sys.argv) != 4:
        print("Usage: converter.py <value> <source_unit> <target_unit>", file=sys.stderr)
        sys.exit(1)

    try:
        value = float(sys.argv[1])
        source_unit = sys.argv[2]
        target_unit = sys.argv[3]

        result = convert(value, source_unit, target_unit)
        print(result)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
