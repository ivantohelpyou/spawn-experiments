# Potential TDD in the AI Era Experiments

## Criteria for Good Experiments

A good experiment should:
- ✅ Be complex enough that naive approaches fail
- ✅ Have no established solutions to copy from training data
- ✅ Demonstrate clear methodology differences
- ✅ Be implementable in 15 minutes to 4 hours
- ✅ Have visual/demonstrable results
- ✅ Contain realistic edge cases

## Tier 1: Excellent Experiment Candidates

### 1. Multi-Language Code Documentation Generator
**Domain**: Generate documentation from code comments in multiple programming languages
**Complexity**: Language parsing, syntax highlighting, cross-references, multiple output formats
**Why Good**: No standard solution, complex parsing rules, many edge cases
**Demo Value**: Visual diff between naive (broken parsing) vs TDD (robust parsing)

### 2. Smart Calendar Conflict Resolver
**Domain**: Resolve scheduling conflicts across time zones with recurring events
**Complexity**: Time zone math, recurring event algorithms, conflict detection
**Why Good**: Extremely complex domain with many edge cases (DST, leap years, etc.)
**Demo Value**: Show calendar with conflicts, demonstrate resolution

### 3. Markdown-to-Slides Converter with Animations
**Domain**: Convert markdown to presentation slides with transition animations
**Complexity**: Markdown parsing, slide layout, animation timing, responsive design
**Why Good**: Creative domain with no standard approach, visual output
**Demo Value**: Live conversion showing layout and animations

### 4. Git Merge Conflict Resolver with Context Analysis
**Domain**: Intelligent git merge conflict resolution using code context
**Complexity**: Git internals, AST parsing, semantic analysis, conflict strategies
**Why Good**: Highly technical, no perfect solutions exist, many edge cases
**Demo Value**: Show merge conflicts being resolved intelligently

### 5. Real-Time Collaborative Text Editor with Operational Transform
**Domain**: Build Google Docs-like collaborative editing with conflict resolution
**Complexity**: Operational transforms, concurrent editing, network synchronization
**Why Good**: Notoriously difficult algorithm, no simple solutions
**Demo Value**: Multiple users editing simultaneously

## Tier 2: Good Experiment Candidates

### 6. Smart Recipe Scaler with Unit Conversion
**Domain**: Scale recipes for different serving sizes with intelligent unit conversion
**Complexity**: Unit parsing, fraction math, ingredient categorization, scaling rules
**Why Good**: Deceptively complex (1.5 cups scaled by 0.67 = ?), many edge cases
**Demo Value**: Show scaling failures vs successes

### 7. Unicode Text Normalizer with Language Detection
**Domain**: Normalize text across different Unicode forms and languages
**Complexity**: Unicode normalization, language detection, character encoding
**Why Good**: Unicode is notoriously complex, many subtle edge cases
**Demo Value**: Show text rendering correctly vs incorrectly

### 8. Smart Log Parser with Pattern Recognition
**Domain**: Parse and analyze log files with intelligent pattern recognition
**Complexity**: Regex generation, pattern learning, anomaly detection, time series
**Why Good**: No standard approach, highly domain-specific
**Demo Value**: Show insights extracted from messy log data

### 9. Dependency Graph Analyzer with Circular Detection
**Domain**: Analyze project dependencies and detect circular references
**Complexity**: Graph algorithms, dependency resolution, cycle detection
**Why Good**: Graph algorithms are complex, many edge cases
**Demo Value**: Visual dependency graphs with problems highlighted

### 10. Smart Configuration Merger with Conflict Resolution
**Domain**: Merge configuration files from multiple sources with intelligent conflict resolution
**Complexity**: YAML/JSON parsing, semantic merging, precedence rules
**Why Good**: No standard approach, many edge cases with nested structures
**Demo Value**: Show configuration conflicts being resolved

## Tier 3: Moderate Experiment Candidates

### 11. Cron Expression Parser and Scheduler
**Domain**: Parse cron expressions and calculate next execution times
**Complexity**: Cron syntax, date/time math, timezone handling
**Why Good**: Well-defined but complex syntax, many edge cases
**Demo Value**: Show schedule calculations

### 12. CSV Data Cleaner with Type Inference
**Domain**: Clean messy CSV data with automatic type detection and correction
**Complexity**: Data type inference, outlier detection, format standardization
**Why Good**: Real-world messiness, no perfect solutions
**Demo Value**: Before/after data visualization

### 13. URL Router with Pattern Matching
**Domain**: Build a flexible URL routing system with parameter extraction
**Complexity**: Pattern matching, parameter parsing, route precedence
**Why Good**: Many edge cases, performance considerations
**Demo Value**: Show routing decisions in real-time

### 14. Template Engine with Inheritance
**Domain**: Build a template engine supporting template inheritance and includes
**Complexity**: Parsing, inheritance resolution, context management
**Why Good**: Complex parsing and resolution logic
**Demo Value**: Show template compilation and rendering

### 15. Simple Database Query Optimizer
**Domain**: Optimize simple SQL-like queries for better performance
**Complexity**: Query parsing, optimization rules, cost estimation
**Why Good**: Complex algorithms, many optimization strategies
**Demo Value**: Show query plans and performance improvements

## Experiment Selection Criteria

### For Live Demos (PuPPy Meetup)
**Prioritize**:
- Visual/interactive results
- Clear failure modes in naive approach
- Demonstrable quality differences
- Familiar problem domains
- 15-30 minute implementation time

**Recommended**: Smart Recipe Scaler, Unicode Text Normalizer, or CSV Data Cleaner

### For Deep Analysis
**Prioritize**:
- Complex algorithmic challenges
- Multiple valid approaches
- Rich edge case scenarios
- Measurable quality metrics
- 2-4 hour implementation time

**Recommended**: Calendar Conflict Resolver, Git Merge Resolver, or Collaborative Text Editor

### For Framework Comparison
**Prioritize**:
- Well-defined testing scenarios
- Clear test structure requirements
- Measurable test coverage
- Framework-agnostic problem domain

**Recommended**: Expression Evaluator (already implemented), Cron Parser, or URL Router

## Implementation Notes

### Testing Framework Considerations
- **unittest**: Better for complex test hierarchies and setup/teardown
- **pytest**: Better for parametrized tests and simple assertions
- **doctest**: Good for documentation-driven development examples

### Complexity Scaling
- Start with core functionality
- Add edge cases progressively
- Include performance requirements
- Consider internationalization needs

### Demo Preparation
- Prepare failure examples for naive approaches
- Have visual comparisons ready
- Include metrics and measurements
- Show real-world applicability

---

**Next Steps**: Select 1-2 experiments for immediate implementation and 2-3 for future exploration based on meetup feedback and time constraints.
