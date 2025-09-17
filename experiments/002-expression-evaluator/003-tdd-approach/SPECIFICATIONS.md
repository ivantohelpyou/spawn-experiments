# Expression Evaluator - Detailed Specifications

## 1. Core Functional Requirements

### 1.1 Primary Functionality
- Evaluate mathematical expressions provided as strings
- Support basic arithmetic operations: addition (+), subtraction (-), multiplication (*), division (/)
- Handle parentheses for expression grouping and precedence override
- Return numeric results for valid expressions
- Provide meaningful error messages for invalid expressions

### 1.2 Supported Operations
- **Addition**: `2 + 3` → `5`
- **Subtraction**: `5 - 2` → `3`
- **Multiplication**: `3 * 4` → `12`
- **Division**: `8 / 2` → `4.0`
- **Parentheses**: `(2 + 3) * 4` → `20`
- **Nested Parentheses**: `((2 + 3) * 4) / 2` → `10.0`

### 1.3 Number Support
- Integer numbers: `1`, `42`, `100`
- Floating-point numbers: `3.14`, `0.5`, `123.456`
- Negative numbers: `-5`, `-3.14`

## 2. User Stories with Acceptance Criteria

### Story 1: Basic Arithmetic Evaluation
**As a** user
**I want to** evaluate simple arithmetic expressions
**So that** I can perform calculations programmatically

**Acceptance Criteria:**
- Given a string "2 + 3", the evaluator returns 5
- Given a string "10 - 4", the evaluator returns 6
- Given a string "3 * 7", the evaluator returns 21
- Given a string "15 / 3", the evaluator returns 5.0

### Story 2: Operator Precedence
**As a** user
**I want** operators to follow mathematical precedence rules
**So that** expressions are evaluated correctly

**Acceptance Criteria:**
- Given "2 + 3 * 4", the evaluator returns 14 (not 20)
- Given "10 - 6 / 2", the evaluator returns 7.0 (not 2.0)
- Given "2 * 3 + 4", the evaluator returns 10

### Story 3: Parentheses Support
**As a** user
**I want to** use parentheses to override operator precedence
**So that** I can control the order of operations

**Acceptance Criteria:**
- Given "(2 + 3) * 4", the evaluator returns 20
- Given "2 * (3 + 4)", the evaluator returns 14
- Given "((2 + 3) * 4) / 2", the evaluator returns 10.0

### Story 4: Error Handling
**As a** user
**I want** clear error messages for invalid expressions
**So that** I can understand and fix input problems

**Acceptance Criteria:**
- Given "2 +", the evaluator raises a meaningful error
- Given "2 + + 3", the evaluator raises a meaningful error
- Given "(2 + 3", the evaluator raises an error about unmatched parentheses
- Given "2 / 0", the evaluator raises a division by zero error

## 3. Technical Architecture Overview

### 3.1 Component Design
```
ExpressionEvaluator
├── Tokenizer
│   ├── Token (data class)
│   └── tokenize(expression: str) -> List[Token]
├── Parser
│   ├── ASTNode (abstract base)
│   ├── NumberNode(ASTNode)
│   ├── BinaryOpNode(ASTNode)
│   └── parse(tokens: List[Token]) -> ASTNode
└── Evaluator
    └── evaluate(node: ASTNode) -> float
```

### 3.2 Processing Pipeline
1. **Input**: String expression (e.g., "2 + 3 * 4")
2. **Tokenization**: Convert string to list of tokens
3. **Parsing**: Convert tokens to Abstract Syntax Tree (AST)
4. **Evaluation**: Traverse AST to compute result
5. **Output**: Numeric result or error message

### 3.3 Design Patterns
- **Abstract Syntax Tree**: For representing parsed expressions
- **Recursive Descent Parser**: For parsing expressions with precedence
- **Visitor Pattern**: For AST evaluation

## 4. Data Models and Relationships

### 4.1 Token Class
```python
@dataclass
class Token:
    type: TokenType
    value: str
    position: int
```

### 4.2 TokenType Enum
```python
class TokenType(Enum):
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    EOF = "EOF"
```

### 4.3 AST Node Hierarchy
```python
class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator: Token, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right
```

## 5. API Design

### 5.1 Public Interface
```python
class ExpressionEvaluator:
    def evaluate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression string.

        Args:
            expression: String containing mathematical expression

        Returns:
            float: Numeric result of the expression

        Raises:
            SyntaxError: If expression has invalid syntax
            ValueError: If expression contains invalid values
            ZeroDivisionError: If expression contains division by zero
        """
```

### 5.2 Usage Examples
```python
evaluator = ExpressionEvaluator()

# Basic operations
result = evaluator.evaluate("2 + 3")  # Returns 5.0
result = evaluator.evaluate("2 * 3 + 4")  # Returns 10.0

# Parentheses
result = evaluator.evaluate("(2 + 3) * 4")  # Returns 20.0

# Error handling
try:
    result = evaluator.evaluate("2 + ")
except SyntaxError as e:
    print(f"Syntax error: {e}")
```

## 6. Business Rules and Validation Requirements

### 6.1 Expression Validation Rules
- Expressions must contain only valid tokens (numbers, operators, parentheses)
- Operators must have operands on both sides (except unary minus)
- Parentheses must be balanced
- Division by zero is not allowed
- Empty expressions are not allowed

### 6.2 Operator Precedence Rules
1. Parentheses (highest precedence)
2. Multiplication and Division (left-to-right)
3. Addition and Subtraction (lowest precedence, left-to-right)

### 6.3 Number Format Rules
- Integer numbers: sequence of digits (0-9)
- Floating-point: digits with single decimal point
- Negative numbers: minus sign immediately before number
- No leading zeros except for decimal numbers (0.5 is valid, 05 is invalid)

## 7. Error Handling and Edge Cases

### 7.1 Syntax Errors
- **Incomplete expression**: "2 +" → "Unexpected end of expression"
- **Invalid operator sequence**: "2 + + 3" → "Unexpected operator '+'"
- **Unmatched parentheses**: "(2 + 3" → "Unmatched opening parenthesis"
- **Empty parentheses**: "()" → "Empty parentheses not allowed"

### 7.2 Runtime Errors
- **Division by zero**: "5 / 0" → "Division by zero"
- **Invalid number format**: "2.3.4" → "Invalid number format"

### 7.3 Edge Cases
- **Whitespace handling**: " 2 + 3 " should work
- **Single number**: "42" should return 42.0
- **Negative numbers**: "-5 + 3" should return -2.0
- **Complex expressions**: "(((1 + 2) * 3) - 4) / 2" should work

### 7.4 Error Message Format
```python
class ExpressionError(Exception):
    def __init__(self, message: str, position: int = None):
        self.message = message
        self.position = position
        super().__init__(self.format_message())

    def format_message(self) -> str:
        if self.position is not None:
            return f"{self.message} at position {self.position}"
        return self.message
```

## 8. Performance Requirements
- Expressions up to 1000 characters should evaluate in < 100ms
- Memory usage should be proportional to expression complexity
- No memory leaks for repeated evaluations

## 9. Testing Strategy
- **Unit Tests**: Each component tested in isolation
- **Integration Tests**: End-to-end expression evaluation
- **Edge Case Tests**: Error conditions and boundary cases
- **Performance Tests**: Large and complex expressions
- **Property-Based Tests**: Generated expressions with known properties