# Temperature Converter

This is a command-line utility to convert temperatures between Celsius, Fahrenheit, and Kelvin.

## Usage

```bash
python converter.py <value> <source_unit> <target_unit>
```

### Arguments

*   `<value>`: The temperature value to convert (float).
*   `<source_unit>`: The source unit. Supported units (case-insensitive):
    *   Celsius (c, celsius)
    *   Fahrenheit (f, fahrenheit)
    *   Kelvin (k, kelvin)
*   `<target_unit>`: The target unit. Supported units are the same as the source unit.

### Example

```bash
python converter.py 32 f c
```

Output:

```
0.0
```

## Error Handling

*   If an invalid unit is provided, an error message is printed to standard error.
*   If the number of arguments is incorrect, a usage message is printed to standard error.
