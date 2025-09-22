#!/bin/bash
# JSON Schema Validator CLI Tool - Method 1E External Library Variant
# Comprehensive demonstration script

echo "=== JSON Schema Validator CLI Tool - External Library Variant ==="
echo "Method: 1E - Immediate Implementation + External Libraries"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "1. Testing help output:"
python json_validator.py --help
echo ""

echo "2. Testing with valid data (file input):"
python json_validator.py test_schema.json --data-file test_data_valid.json
echo ""

echo "3. Testing with invalid data (rich text output):"
python json_validator.py test_schema.json --data-file test_data_invalid.json
echo ""

echo "4. Testing JSON output format:"
python json_validator.py test_schema.json --data-file test_data_invalid.json -o json
echo ""

echo "5. Testing string input:"
python json_validator.py test_schema.json --data-string '{"name": "Test User", "email": "test@gmail.com", "age": 25, "preferences": {"theme": "light"}}'
echo ""

echo "6. Testing stdin input:"
echo '{"name": "Stdin User", "email": "stdin@test.com", "age": 30, "preferences": {"theme": "dark"}}' | python json_validator.py test_schema.json --stdin
echo ""

echo "7. Testing quiet mode (exit codes only):"
echo "Valid data:"
python json_validator.py test_schema.json --data-string '{"name": "Test", "email": "test@gmail.com", "age": 25, "preferences": {"theme": "dark"}}' -o quiet
echo "Exit code: $?"

echo "Invalid data:"
python json_validator.py test_schema.json --data-file test_data_invalid.json -o quiet
echo "Exit code: $?"

echo ""
echo "=== External Libraries Used ==="
pip list | grep -E "(click|rich|jsonschema|email-validator|validators|colorama)"

echo ""
echo "=== Demo Complete ==="