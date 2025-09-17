# Experimental Attribution and Documentation

## Primary Research Question
**How does methodology guidance affect AI-generated code quality?**

Comparing four development approaches:
1. **Naive**: "Just build it" with minimal guidance
2. **Spec-First**: Detailed specifications before implementation
3. **TDD**: Test-driven development with red-green-refactor cycles
4. **Enhanced TDD**: TDD plus rigorous test validation

## Experiment Attribution Log

### Completed Experiments

**Experiment 001: Unicode Password Manager**
- **AI Agent**: Claude 3.5 Sonnet (Anthropic)
- **Date**: September 2024
- **Methods Completed**: All 4 methods (Naive, Spec-First, TDD, Enhanced TDD)
- **Testing Framework**: Python `unittest` (Methods 3 & 4)
- **Status**: Complete baseline experiment

**Experiment 002: Expression Evaluator**
- **AI Agent**: Claude 3.5 Sonnet (Anthropic)
- **Date**: September 2024
- **Methods Completed**: All 4 methods (Naive, Spec-First, TDD, Enhanced TDD)
- **Testing Framework**: Python `unittest` (Methods 3 & 4)
- **Status**: Complete

**Experiment 003: Simple Interest Calculator**
- **AI Agent**: Claude 3.5 Sonnet (Anthropic)  
- **Date**: September 2024
- **Methods Completed**: Method 1 (Naive) only
- **Testing Framework**: None (print statements)
- **Status**: Incomplete

## Key Findings

### Methodology Progression Shows Clear Value
- **Method 1 (Naive)**: Basic functionality, minimal error handling, no systematic testing
- **Method 2 (Spec-First)**: Better structure and planning, some validation, improved documentation
- **Method 3 (TDD)**: Comprehensive test suites, robust error handling, clean refactored code
- **Method 4 (Enhanced TDD)**: Highest test quality, thorough edge case coverage, maximum confidence

### Main Insights
- **AI amplifies methodology**: Good practices become better, poor practices become more obvious
- **TDD with AI is powerful**: AI can write tests faster than humans, making TDD more accessible
- **Test quality matters**: Method 4's validation catches issues that Method 3 misses

## Secondary Research: Framework Bias Testing (Optional)

### Research Question
Does the choice of testing framework (unittest vs pytest) significantly impact the effectiveness or outcomes of TDD-based methodologies?

### Experimental Design

**Control Group**: Experiment 002 (Expression Evaluator with unittest)
**Test Group**: Experiment 002b (Expression Evaluator with pytest)

**Variables to Control**:
- Same problem domain (expression evaluation)
- Same AI agent (Claude 3.5 Sonnet)
- Same methodology prompts (TDD and Enhanced TDD)
- Same evaluation criteria

**Variables to Measure**:
- Development time/iterations
- Test coverage achieved
- Code quality metrics (complexity, readability)
- Bug detection effectiveness
- Final feature completeness
- Developer experience (subjective assessment)

### Framework Comparison Criteria

**Technical Metrics**:
- Lines of test code required
- Test execution speed
- Test readability/maintainability
- Assertion clarity and expressiveness
- Setup/teardown complexity

**Methodology Impact**:
- Ease of TDD red-green-refactor cycles
- Test organization and structure
- Debugging and failure reporting quality
- Integration with enhanced validation practices

**Cognitive Load**:
- Boilerplate code requirements
- Learning curve for framework-specific features
- Mental overhead for test structure

### Expected Outcomes

**Null Hypothesis**: Testing framework choice has no significant impact on TDD methodology effectiveness.

**Alternative Hypotheses**:
1. **pytest advantage**: More concise syntax leads to faster TDD cycles and better test coverage
2. **unittest advantage**: More explicit structure leads to better organized, more maintainable tests
3. **Context dependency**: Framework effectiveness varies by problem complexity or developer experience

### Framework Selection Rationale

**unittest (Standard Library)**:
- ✅ No external dependencies
- ✅ Familiar to Java/C# developers
- ✅ Explicit test structure
- ❌ More verbose syntax
- ❌ Less flexible assertions

**pytest (Third-party)**:
- ✅ Concise, Pythonic syntax
- ✅ Powerful fixtures and parametrization
- ✅ Better failure reporting
- ❌ External dependency
- ❌ More "magic" behavior

## Bias Mitigation Strategies

### 1. Prompt Neutrality
- Use identical methodology descriptions for both framework experiments
- Avoid language suggesting one framework is "better" or "preferred"
- Focus prompts on methodology goals, not framework-specific features

### 2. Evaluation Consistency
- Apply identical code quality metrics to both experiments
- Use same bug injection tests for validation
- Measure same performance and maintainability criteria

### 3. Documentation Standards
- Record identical level of detail for both experiments
- Note any framework-specific advantages or disadvantages objectively
- Document unexpected outcomes without bias toward either framework

## Dependency Management Policy

### Current Approach: No External Dependencies
**Rationale**: 
- Keeps focus on methodology rather than tooling
- Prevents "best library wins" bias
- Maintains experimental control across methods
- Reduces setup complexity for demo purposes

**Exception for Framework Testing**:
- pytest experiment will require external dependency
- This is acceptable because we're explicitly testing framework impact
- Will document installation requirements clearly
- Will note this as limitation for pure methodology comparison

### Future Experiment Considerations
**Potential "Libraries Allowed" Experiment**:
- Could test: "Given access to rich ecosystem, which methodology leverages it best?"
- Would require careful library selection to avoid bias
- Should provide identical library recommendations to all methods
- Focus on methodology's ability to integrate and utilize external tools

## Attribution Requirements

### For Each Experiment
**Must Document**:
- AI agent name and version
- Date/time of execution  
- Human operator (if different from AI agent)
- Computing environment details
- Any external tools or libraries used
- Methodology prompt versions used

### For Comparative Analysis
**Must Specify**:
- Which experiments are being compared
- Whether same AI agent was used
- Time gap between experiments (model evolution consideration)
- Any environmental differences that might affect results

### For Publication/Presentation
**Must Acknowledge**:
- AI agents as co-authors/contributors
- Specific model versions and capabilities
- Limitations of AI-generated code
- Human oversight and validation role

## Quality Assurance

### Experiment Validation
- All code must be executable and tested
- Results must be reproducible by independent parties
- Methodology adherence must be verifiable
- Outcomes must be measurable and objective

### Bias Detection
- Regular review of experimental assumptions
- Peer review of methodology and results
- Documentation of unexpected or contradictory findings
- Willingness to revise hypotheses based on evidence

---

**Next Steps**:
1. Complete Experiment 002b (pytest version)
2. Conduct comparative analysis of framework impact
3. Update experimental design based on findings
4. Document lessons learned for future experiments
