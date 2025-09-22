# JSON Schema Validator - Implementation Specifications

## Project Overview
Build a JSON Schema Validator using Python with jsonschema library that validates JSON data against JSON Schema Draft 7 specifications.

## Core Requirements

### 1. Validation Functionality
- **Primary Function**: Validate JSON data against provided JSON schema
- **Schema Support**: JSON Schema Draft 7 subset only
- **Return Format**: Boolean valid/invalid result with detailed error information
- **Error Handling**: Graceful handling of malformed JSON and invalid schemas

### 2. Supported Data Types
- `string` - Text data with optional format validation
- `number` - Numeric values (integer or float)
- `integer` - Whole numbers only
- `boolean` - True/false values
- `object` - Key-value pairs with property validation
- `array` - Ordered lists with item validation

### 3. Supported Schema Keywords
- `type` - Data type specification
- `properties` - Object property definitions
- `required` - Required property array for objects
- `format` - String format validation (email, date, uri)
- `minimum`/`maximum` - Numeric range validation
- `minLength`/`maxLength` - String length validation
- `items` - Array item schema
- `minItems`/`maxItems` - Array length validation

### 4. Format Validation Support
- `email` - Valid email address format
- `date` - ISO 8601 date format (YYYY-MM-DD)
- `uri` - Valid URI format

## Technical Specifications

### 1. Architecture
```
JSONSchemaValidator
├── Core Validator Class
│   ├── validate(data, schema) -> ValidationResult
│   ├── _parse_json(json_string) -> dict/list
│   ├── _validate_schema(schema) -> bool
│   └── _format_errors(errors) -> list
├── ValidationResult Class
│   ├── is_valid: bool
│   ├── errors: list
│   └── __str__() -> str
└── Utility Functions
    ├── is_valid_json(json_string) -> bool
    └── validate_simple(data, schema) -> bool
```

### 2. Input/Output Specifications

#### Input Types
1. **JSON Data**: String (JSON), dict, list, or primitive types
2. **Schema**: Dictionary containing JSON Schema Draft 7 specification

#### Output Format
```python
ValidationResult:
    is_valid: bool
    errors: List[str]  # Detailed error descriptions
```

#### Error Categories
1. **JSON Parse Errors**: Malformed JSON input
2. **Schema Validation Errors**: Invalid schema structure
3. **Data Validation Errors**: Data doesn't match schema requirements

### 3. Expected Behaviors

#### Valid Cases
```python
# Valid string
validate('{"name": "John"}', {"type": "object", "properties": {"name": {"type": "string"}}})
# Result: ValidationResult(is_valid=True, errors=[])

# Valid array
validate('[1, 2, 3]', {"type": "array", "items": {"type": "integer"}})
# Result: ValidationResult(is_valid=True, errors=[])
```

#### Invalid Cases
```python
# Type mismatch
validate('{"age": "25"}', {"type": "object", "properties": {"age": {"type": "integer"}}})
# Result: ValidationResult(is_valid=False, errors=["'25' is not of type 'integer'"])

# Missing required property
validate('{}', {"type": "object", "required": ["name"]})
# Result: ValidationResult(is_valid=False, errors=["'name' is a required property"])
```

#### Error Cases
```python
# Malformed JSON
validate('{"invalid": json}', {})
# Result: ValidationResult(is_valid=False, errors=["Invalid JSON: Expecting value: line 1 column 13"])

# Invalid schema
validate('{}', {"type": "invalid_type"})
# Result: ValidationResult(is_valid=False, errors=["Invalid schema: 'invalid_type' is not a valid type"])
```

## Implementation Strategy

### Phase 1: Core Structure
1. Create `ValidationResult` class for structured output
2. Create main `JSONSchemaValidator` class
3. Implement basic JSON parsing with error handling
4. Set up jsonschema library integration

### Phase 2: Basic Validation
1. Implement type validation for all supported types
2. Add property validation for objects
3. Add required field validation
4. Add basic array validation

### Phase 3: Advanced Features
1. Implement format validation (email, date, uri)
2. Add numeric range validation
3. Add string length validation
4. Add array length validation

### Phase 4: Error Handling & Polish
1. Comprehensive error message formatting
2. Edge case handling (null, empty inputs)
3. Schema validation before use
4. Performance considerations

## Constraints & Exclusions

### Explicitly NOT Supported
- Schema composition (`allOf`, `oneOf`, `anyOf`)
- Conditional logic (`if`/`then`/`else`)
- Remote schema references (`$ref` URLs)
- Custom keyword extensions
- Schema transformation or modification
- Performance optimization for large datasets

### Library Dependencies
- Python standard library
- `jsonschema` package (if available)
- No external web dependencies
- No custom format validators beyond standard ones

## Testing Strategy

### Test Categories
1. **Basic Type Validation**: Each supported type with valid/invalid data
2. **Object Validation**: Properties, required fields, nested objects
3. **Array Validation**: Items, length constraints
4. **Format Validation**: Email, date, URI patterns
5. **Error Handling**: Malformed JSON, invalid schemas, edge cases
6. **Integration Tests**: Complex schemas combining multiple features

### Test Data Sets
- Valid JSON examples for each type
- Invalid JSON examples with expected errors
- Edge cases (empty objects, null values, boundary conditions)
- Complex nested structures
- Format validation test cases

## Success Criteria

### Functional Requirements
✓ Validates all supported data types correctly
✓ Handles object properties and required fields
✓ Validates array items and constraints
✓ Supports email, date, and URI format validation
✓ Returns structured results with clear error messages
✓ Gracefully handles malformed JSON and invalid schemas

### Quality Requirements
✓ Clean, readable code with proper error handling
✓ Comprehensive test coverage
✓ Clear documentation and usage examples
✓ Follows Python best practices
✓ Proper separation of concerns

### Performance Requirements
✓ Reasonable performance for typical JSON documents
✓ Memory efficient for moderately sized data
✓ No performance optimization required for large datasets