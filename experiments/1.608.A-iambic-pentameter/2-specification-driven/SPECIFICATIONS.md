# Story-to-Iambic-Pentameter Converter
## Technical Specifications

### 1. Overview

**Purpose**: Convert prose stories into Shakespearean verse (iambic pentameter)

**Method**: Specification-Driven Development
- Design first, implement second
- Clear interfaces and contracts
- Quality-focused implementation

### 2. Requirements

#### 2.1 Functional Requirements
- **FR-1**: Accept prose text as input (stories, paragraphs, sentences)
- **FR-2**: Convert text to iambic pentameter format
- **FR-3**: Maintain semantic meaning during conversion
- **FR-4**: Output properly formatted verse (10 syllables per line)
- **FR-5**: Follow iambic meter (unstressed-stressed syllable alternation)

#### 2.2 Technical Requirements
- **TR-1**: Use llama3.2 model via Ollama for LLM processing
- **TR-2**: Use only Python standard library + Ollama
- **TR-3**: No external web access required
- **TR-4**: Include comprehensive test suite
- **TR-5**: Handle errors gracefully (Ollama unavailable, invalid input)

#### 2.3 Non-Functional Requirements
- **NFR-1**: Modular, maintainable code structure
- **NFR-2**: Clear separation of concerns
- **NFR-3**: Comprehensive error handling
- **NFR-4**: Well-documented code and usage

### 3. Architecture Design

#### 3.1 System Components

```
┌─────────────────────────────────────────────────┐
│              Main Application                   │
│           (iambic_converter.py)                 │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌──────────────┐           ┌──────────────────┐
│   Input      │           │    LLM Client    │
│  Processor   │           │   (Ollama)       │
└──────────────┘           └──────────────────┘
        │                           │
        └─────────────┬─────────────┘
                      ▼
              ┌──────────────┐
              │   Converter  │
              │    Engine    │
              └──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │   Validator  │
              │   (Meter)    │
              └──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │    Output    │
              │  Formatter   │
              └──────────────┘
```

#### 3.2 Core Classes

**IambicConverter** (Main Class)
- Responsibilities: Orchestrate conversion process
- Methods:
  - `__init__(model: str = "llama3.2")`: Initialize with model
  - `convert(text: str) -> str`: Convert prose to iambic pentameter
  - `_validate_ollama() -> bool`: Check Ollama availability

**SyllableCounter**
- Responsibilities: Count syllables in words/lines
- Methods:
  - `count_syllables(word: str) -> int`: Count syllables in word
  - `count_line_syllables(line: str) -> int`: Count syllables in line

**MeterValidator**
- Responsibilities: Validate iambic pentameter structure
- Methods:
  - `is_valid_line(line: str) -> bool`: Check if line has 10 syllables
  - `validate_poem(text: str) -> dict`: Validate entire poem

**OllamaClient**
- Responsibilities: Handle LLM communication
- Methods:
  - `generate(prompt: str) -> str`: Generate text via Ollama
  - `is_available() -> bool`: Check if Ollama is running

### 4. Interface Specifications

#### 4.1 Main Interface

```python
class IambicConverter:
    """Convert prose to iambic pentameter using LLM."""

    def convert(self, text: str) -> str:
        """
        Convert prose text to iambic pentameter.

        Args:
            text: Input prose text

        Returns:
            Text in iambic pentameter format

        Raises:
            ValueError: If input is empty or invalid
            ConnectionError: If Ollama is unavailable
        """
```

#### 4.2 Data Flow

1. **Input**: Prose text string
2. **Preprocessing**: Clean and prepare text
3. **LLM Generation**: Send to Ollama with structured prompt
4. **Validation**: Check syllable count and meter
5. **Refinement**: Retry if validation fails (max 3 attempts)
6. **Output**: Formatted iambic pentameter

### 5. Prompt Engineering

#### 5.1 Core Prompt Template

```
You are a Shakespearean poetry expert. Convert the following prose into iambic pentameter.

RULES:
- Each line must have exactly 10 syllables
- Follow iambic meter: unstressed-STRESSED pattern (da-DUM)
- Maintain the original meaning and story
- Use poetic language but keep it comprehensible
- Output only the converted poem, no explanations

PROSE:
{input_text}

IAMBIC PENTAMETER:
```

#### 5.2 Refinement Prompt (if validation fails)

```
The previous attempt had lines with incorrect syllable counts.

Lines with issues: {problem_lines}

Please revise to ensure EVERY line has exactly 10 syllables in iambic meter.

REVISED IAMBIC PENTAMETER:
```

### 6. Syllable Counting Algorithm

#### 6.1 Heuristic Rules
1. Count vowel groups (consecutive vowels = 1 syllable)
2. Silent 'e' at end doesn't count (unless word ends in 'le')
3. 'y' at end counts as vowel
4. Common exceptions dictionary for accuracy
5. Minimum 1 syllable per word

#### 6.2 Exception Dictionary
- Common words with non-standard patterns
- Contractions (don't, can't, etc.)
- Proper nouns if needed

### 7. Error Handling

#### 7.1 Error Categories
1. **Connection Errors**: Ollama unavailable
2. **Validation Errors**: Invalid input (empty, too long)
3. **Generation Errors**: LLM fails to generate valid output
4. **Timeout Errors**: LLM takes too long

#### 7.2 Recovery Strategies
- Retry with refined prompts (max 3 attempts)
- Graceful degradation (return best attempt)
- Clear error messages for users

### 8. Testing Strategy

#### 8.1 Unit Tests
- Syllable counter accuracy
- Meter validation logic
- Input preprocessing
- Error handling

#### 8.2 Integration Tests
- Full conversion pipeline
- Ollama integration (if available)
- Retry logic
- Output formatting

#### 8.3 Test Cases
1. Simple sentences
2. Complex narratives
3. Edge cases (empty input, very long text)
4. Special characters and punctuation
5. Already-poetic text

### 9. Performance Considerations

- **Latency**: LLM calls are slowest component (5-30 seconds)
- **Retries**: Limit to 3 attempts to balance quality/speed
- **Caching**: Not implemented in v1 (future enhancement)
- **Batch Processing**: Process paragraphs separately for better results

### 10. File Structure

```
2-specification-driven/
├── SPECIFICATIONS.md          # This file
├── ARCHITECTURE.md            # Detailed design
├── README.md                  # User guide
├── requirements.txt           # Dependencies
├── iambic_converter.py        # Main implementation
└── test_iambic_converter.py   # Test suite
```

### 11. Dependencies

```
ollama (Python package) - NOT REQUIRED, using subprocess instead
```

Standard library modules:
- `re` - Regular expressions for text processing
- `subprocess` - Calling Ollama CLI
- `typing` - Type hints
- `unittest` - Testing framework

### 12. Success Criteria

- ✓ Converts prose to iambic pentameter format
- ✓ Most lines have exactly 10 syllables
- ✓ Maintains semantic meaning
- ✓ Handles errors gracefully
- ✓ Comprehensive test coverage (>80%)
- ✓ Clear documentation
