# Glossary: TDD in the AI Era

## Technical Terms

### Unicode and Character Encoding

**NFC (Normalization Form Composed)**
- Unicode normalization where characters like `é` are stored as single codepoints
- Example: `café` has `é` as one character (U+00E9)

**NFD (Normalization Form Decomposed)**
- Unicode normalization where accented characters are split into base + combining marks
- Example: `café` has `e` + combining acute accent (U+0065 + U+0301)

**Unicode Normalization**
- Process of converting text to a standard form for consistent comparison
- Prevents `café` (NFC) and `cafe´` (NFD) from being treated as different

**Diacritics**
- Accent marks added to letters (á, é, ñ, ü, etc.)
- Can cause search failures if not handled properly

**Homograph Attack**
- Security exploit using visually similar characters from different scripts
- Example: `раssword` (Cyrillic р,а) vs `password` (Latin p,a)

**Combining Characters**
- Unicode characters that modify the preceding character
- Example: e + ´ = é when properly rendered

**Grapheme Cluster**
- What users perceive as a single character
- Example: `👨‍👩‍👧‍👦` (family emoji) is 1 grapheme but 11 codepoints

**Case Folding**
- Unicode-aware case conversion for comparison
- Handles non-Latin scripts properly (unlike simple .lower())

### Development Methodologies

**TDD (Test-Driven Development)**
- Software development process: write tests first, then implement
- Red-Green-Refactor cycle

**Red-Green-Refactor**
- TDD cycle: Red (failing test) → Green (minimal code) → Refactor (improve)

**Enhanced TDD**
- TDD with added test validation step
- Process: Red-Validate-Green-Refactor

**Test Validation**
- Proving tests catch bugs by implementing broken code first
- Ensures test quality and eliminates false confidence

**Specification-First Development**
- Write detailed requirements before implementation
- Top-down approach from specs to code

**Naive Implementation**
- Direct coding without planning or testing
- "Just build it" approach

### Testing Concepts

**Test Coverage**
- Percentage of code lines executed by tests
- Higher coverage generally indicates better testing

**False Positive (Testing)**
- Test that passes when it should fail
- Indicates weak or incorrect test

**Assertion**
- Statement in test that must be true for test to pass
- Example: `self.assertEqual(result, expected)`

**Edge Case**
- Unusual or extreme input that might break the system
- Example: empty strings, maximum length inputs

**Boundary Testing**
- Testing at the limits of acceptable input ranges
- Example: testing with exactly maximum allowed length

**Fuzzy Search**
- Search that tolerates typos and approximate matches
- Uses algorithms like edit distance

**Edit Distance (Levenshtein Distance)**
- Number of single-character changes needed to transform one string into another
- Used for typo tolerance in search

### Software Quality Metrics

**Cyclomatic Complexity**
- Measure of code complexity based on decision points
- Lower is generally better for maintainability

**Code Duplication**
- Repeated code blocks that should be consolidated
- Increases maintenance burden

**Technical Debt**
- Accumulated shortcuts that need future cleanup
- Results from choosing quick fixes over proper solutions

**Maintainability**
- How easily code can be modified and extended
- Affected by testing, documentation, and code quality

### AI and Development Terms

**Prompt Engineering**
- Crafting AI instructions to get desired outcomes
- Critical skill for AI-assisted development

**Methodology Amplification**
- How AI magnifies the effects of development practices
- Good practices → excellent results, poor practices → broken software

**Implementation Gap**
- Difference between specifications and actual code
- Common issue in spec-first development

**Test-Driven API Design**
- Using tests to drive the design of interfaces
- Results in more usable APIs

### Search and Information Retrieval

**Emoji-Tolerant Search**
- Search that finds text even when service names contain emoji
- Example: "gmail" finds "📧 Gmail Account"

**Diacritic-Insensitive Search**
- Search that ignores accent marks
- Example: "cafe" finds "Café WiFi"

**Result Ranking**
- Ordering search results by relevance
- Typically: exact match > starts-with > contains

**Alphanumeric Extraction**
- Removing non-letter, non-number characters for comparison
- Enables emoji-tolerant matching

**Script-Aware Search**
- Search that handles different writing systems (Latin, Cyrillic, CJK)
- May include transliteration capabilities

### Security Terms

**Input Validation**
- Checking user input for correctness and safety
- Prevents malformed data attacks

**Attack Surface**
- Points where system can be exploited
- Unicode handling increases attack surface if not done properly

**Security Vulnerability**
- Weakness that can be exploited by attackers
- Example: accepting malformed Unicode input

### Performance and Scalability

**Time Complexity**
- How algorithm performance scales with input size
- O(n) means linear scaling with input

**Memory Footprint**
- Amount of memory used by program
- Important for handling large Unicode strings

**Optimization**
- Improving performance while maintaining functionality
- Trade-off between speed and code complexity

### Development Process

**Incremental Development**
- Building software in small, working pieces
- Reduces risk and enables early feedback

**Refactoring**
- Improving code structure without changing behavior
- Safer when comprehensive tests exist

**Code Review**
- Peer examination of code for quality and correctness
- Critical for catching issues

**Regression**
- Previously working feature that breaks due to changes
- Prevented by comprehensive test suites

**Technical Specification**
- Detailed document describing system requirements
- Bridge between business needs and implementation

### Quality Assurance

**Acceptance Criteria**
- Conditions that must be met for feature to be considered complete
- Often written as testable statements

**User Story**
- Feature description from user perspective
- Format: "As a [user], I want [goal] so that [benefit]"

**Quality Gate**
- Checkpoint where code must meet standards before proceeding
- May include test coverage, performance, security checks

**Production-Ready**
- Code quality suitable for live user environment
- Implies comprehensive testing, error handling, and security

### Modern Development Practices

**Continuous Integration**
- Automatically testing code changes when submitted
- Catches integration issues early

**DevOps**
- Practices bridging development and operations
- Emphasizes automation and monitoring

**Pair Programming**
- Two developers working together on same code
- Knowledge sharing and real-time code review

**Agile Development**
- Iterative development methodology
- Emphasizes working software and customer collaboration

### Data and Storage

**Serialization**
- Converting objects to storable format (JSON, etc.)
- Must preserve Unicode correctly

**Data Persistence**
- Storing data between program runs
- Unicode encoding critical for international data

**Database Collation**
- Rules for comparing and sorting text in databases
- Affects Unicode string comparison behavior

**Character Set**
- Collection of characters available for use
- ASCII (128 chars) vs Unicode (1M+ chars)