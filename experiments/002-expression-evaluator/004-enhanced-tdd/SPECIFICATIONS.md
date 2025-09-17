# Expression Evaluator - Enhanced TDD with Test Validation
## Detailed Specifications

### 1. Core Functional Requirements

**Primary Objective**: Create a robust expression evaluator that can parse and evaluate mathematical expressions with proper error handling.

**Core Features**:
- Basic arithmetic operations: addition (+), subtraction (-), multiplication (*), division (/)
- Operator precedence (PEMDAS/BODMAS)
- Parentheses support for grouping
- Decimal number support
- Negative number support
- Whitespace handling (ignore spaces)
- Error handling for invalid expressions

**Input/Output Requirements**:
- Input: String representation of mathematical expression
- Output: Numeric result (float/int) or appropriate error message
- Examples:
  - "2 + 3" → 5
  - "2 * (3 + 4)" → 14
  - "10 / 2" → 5.0
  - "invalid" → Error

### 2. User Stories with Acceptance Criteria

**Story 1: Basic Arithmetic Operations**
```
As a user
I want to evaluate basic arithmetic expressions
So that I can perform simple calculations

Acceptance Criteria:
- Given expression "2 + 3", when evaluated, then returns 5
- Given expression "10 - 4", when evaluated, then returns 6
- Given expression "3 * 7", when evaluated, then returns 21
- Given expression "15 / 3", when evaluated, then returns 5.0
```

**Story 2: Operator Precedence**
```
As a user
I want expressions to follow standard mathematical precedence
So that complex calculations are evaluated correctly

Acceptance Criteria:
- Given expression "2 + 3 * 4", when evaluated, then returns 14 (not 20)
- Given expression "10 - 6 / 2", when evaluated, then returns 7.0 (not 2.0)
- Given expression "2 * 3 + 4 * 5", when evaluated, then returns 26
```

**Story 3: Parentheses Support**
```
As a user
I want to use parentheses to override precedence
So that I can control the order of operations

Acceptance Criteria:
- Given expression "(2 + 3) * 4", when evaluated, then returns 20
- Given expression "2 * (3 + 4)", when evaluated, then returns 14
- Given expression "((2 + 3) * 4) - 5", when evaluated, then returns 15
```

**Story 4: Decimal and Negative Numbers**
```
As a user
I want to work with decimal and negative numbers
So that I can perform real-world calculations

Acceptance Criteria:
- Given expression "2.5 + 1.5", when evaluated, then returns 4.0
- Given expression "-5 + 3", when evaluated, then returns -2
- Given expression "(-2) * 3", when evaluated, then returns -6
```

**Story 5: Error Handling**
```
As a user
I want clear error messages for invalid expressions
So that I understand what went wrong

Acceptance Criteria:
- Given expression "2 + ", when evaluated, then raises appropriate error
- Given expression "2 + * 3", when evaluated, then raises appropriate error
- Given expression "2 / 0", when evaluated, then raises division by zero error
- Given expression "(2 + 3", when evaluated, then raises unmatched parentheses error
```

### 3. Technical Architecture Overview

**Architecture Pattern**: Clean Architecture with clear separation of concerns

**Core Components**:

1. **Tokenizer** (`tokenizer.py`)
   - Converts string input into tokens (numbers, operators, parentheses)
   - Handles whitespace removal and basic validation

2. **Parser** (`parser.py`)
   - Implements recursive descent parser
   - Builds Abstract Syntax Tree (AST) respecting operator precedence
   - Handles parentheses and associativity

3. **Evaluator** (`evaluator.py`)
   - Traverses AST to compute final result
   - Handles arithmetic operations and error conditions

4. **Expression Calculator** (`expression_calculator.py`)
   - Main interface that orchestrates tokenizer, parser, and evaluator
   - Provides clean API for expression evaluation

**Error Handling Strategy**:
- Custom exception hierarchy for different error types
- Graceful degradation with meaningful error messages
- Input validation at each stage

### 4. Data Models and Relationships

**Token Class**:
```python
@dataclass
class Token:
    type: TokenType  # NUMBER, OPERATOR, LPAREN, RPAREN, EOF
    value: Union[float, str]
    position: int  # For error reporting
```

**TokenType Enumeration**:
```python
class TokenType(Enum):
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"
```

**AST Node Classes**:
```python
@dataclass
class NumberNode:
    value: float

@dataclass
class BinaryOpNode:
    left: ASTNode
    operator: Token
    right: ASTNode

@dataclass
class UnaryOpNode:
    operator: Token
    operand: ASTNode
```

### 5. API Design

**Primary Interface**:
```python
class ExpressionCalculator:
    def evaluate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression string.

        Args:
            expression: String containing mathematical expression

        Returns:
            float: Numerical result of the expression

        Raises:
            ParseError: If expression has syntax errors
            EvaluationError: If evaluation fails (e.g., division by zero)
            TokenizeError: If expression contains invalid characters
        """
```

**Usage Examples**:
```python
calculator = ExpressionCalculator()
result = calculator.evaluate("2 + 3 * 4")  # Returns 14.0
result = calculator.evaluate("(2 + 3) * 4")  # Returns 20.0
```

### 6. Business Rules and Validation Requirements

**Operator Precedence Rules** (highest to lowest):
1. Parentheses `()`
2. Unary minus `-`
3. Multiplication `*` and Division `/` (left-to-right associative)
4. Addition `+` and Subtraction `-` (left-to-right associative)

**Number Format Rules**:
- Integers: `123`, `-45`
- Decimals: `12.34`, `-5.67`, `0.5`
- No scientific notation in initial version
- No leading zeros except for `0.x` decimals

**Expression Validation Rules**:
- Must contain at least one number
- Operators must be between operands
- Parentheses must be balanced
- No empty expressions
- No consecutive operators (except unary minus)

**Whitespace Handling**:
- Leading and trailing whitespace ignored
- Internal whitespace ignored
- Tabs and spaces treated equally

### 7. Error Handling and Edge Cases

**Exception Hierarchy**:
```python
class ExpressionError(Exception):
    """Base exception for expression evaluation errors"""

class TokenizeError(ExpressionError):
    """Raised when tokenization fails"""

class ParseError(ExpressionError):
    """Raised when parsing fails"""

class EvaluationError(ExpressionError):
    """Raised when evaluation fails"""
```

**Edge Cases to Handle**:

1. **Division by Zero**:
   - `"5 / 0"` → EvaluationError("Division by zero")
   - `"5 / (3 - 3)"` → EvaluationError("Division by zero")

2. **Malformed Expressions**:
   - `"2 +"` → ParseError("Unexpected end of expression")
   - `"+ 2"` → ParseError("Unexpected operator at start")
   - `"2 3"` → ParseError("Missing operator between numbers")

3. **Parentheses Issues**:
   - `"(2 + 3"` → ParseError("Unmatched opening parenthesis")
   - `"2 + 3)"` → ParseError("Unmatched closing parenthesis")
   - `"((2 + 3)"` → ParseError("Unmatched opening parenthesis")

4. **Invalid Characters**:
   - `"2 + a"` → TokenizeError("Invalid character 'a'")
   - `"2 + #"` → TokenizeError("Invalid character '#'")

5. **Empty or Whitespace-only**:
   - `""` → ParseError("Empty expression")
   - `"   "` → ParseError("Empty expression")

6. **Number Format Issues**:
   - `"2.3.4"` → TokenizeError("Invalid number format")
   - `"2."` → TokenizeError("Invalid number format")
   - `".5"` → Should work (0.5)

**Error Message Requirements**:
- Include position information when possible
- Be user-friendly and actionable
- Distinguish between syntax and runtime errors
- Provide suggestions for common mistakes

**Performance Considerations**:
- Handle expressions up to 1000 characters
- Recursive parser should handle nesting up to 50 levels
- Memory usage should be linear with input size
- Evaluation should complete in under 100ms for typical expressions

**Testing Strategy**:
- Unit tests for each component (tokenizer, parser, evaluator)
- Integration tests for complete expression evaluation
- Edge case testing for error conditions
- Property-based testing for mathematical correctness
- Performance testing for large expressions