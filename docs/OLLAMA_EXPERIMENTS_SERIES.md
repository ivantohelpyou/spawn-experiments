# Ollama Experiments Series (1.6XX)

**Date**: 2025-09-30
**Purpose**: Explore local LLM integration using Ollama across 4 development methodologies
**Status**: Active - 1 experiment complete with 2 validated findings

---

## Series Overview

The 1.6XX series explores **local AI model integration** using Ollama, demonstrating how methodology choices affect AI-augmented development patterns. These experiments combine traditional programming with local LLM capabilities.

**Key Research Questions**:
- How do methodologies handle AI service integration? ✅ **ANSWERED**
- What testing approaches work for non-deterministic outputs? ✅ **ANSWERED**
- How do developers structure prompts and model interactions? ✅ **ANSWERED**
- What error handling patterns emerge for local AI services?
- **NEW**: How does prompt quality affect development process? ✅ **DISCOVERED**

---

## Completed Experiments

### ⭐ **1.608 - Story-to-Haiku Converter** (4 Runs Complete)
**Status**: ✅ Complete | **Findings**: 2 validated discoveries

**Summary**: Revolutionary 4-run study exploring LLM integration with creative outputs. Discovered that prompt engineering acts as a universal force multiplier and that multiple methodology samples can be used for Monte Carlo quality filtering.

**Runs**:
- Run 1: Initial baseline (unstructured output)
- Run 2: Structured JSON output
- Run 3: Clean room (5 methodologies tested)
- Run 4: Optimized prompts (exploratory pivot)

**Key Discoveries**:

#### Finding 09: Prompt Engineering as Force Multiplier
- Optimized prompts improved development speed by 22-36%
- Quality improved by +1 to +7 points across all methodologies
- TDD benefits most from clear examples (+7 points)
- **Status**: Moderate-High confidence (needs proper controlled validation)

#### Finding 10: Monte Carlo Methodology Sampling
- Generate N samples → Judge → Pick best = 20% quality improvement
- Validated with Olympic judging system (3 LLM judges)
- Immediately applicable production technique
- **Status**: Validated

**Innovations**:
- Working CLI tool (`tools/generate-haiku`)
- Olympic judging system (3 models, drop high/low)
- Mock strategy for parallel execution
- Prompt quality validation tests (Method 4 only)

**Research Integrity**:
- Rejected Finding 11 (Creative Simplicity Paradox) as likely random variation (N=1)
- Transparent about Run 4 being exploratory pivot, not controlled experiment

**Read More**: [Complete 1.608 Summary](../experiments/1.608-story-to-haiku/EXPERIMENT_1608_COMPLETE_SUMMARY.md)

---

## Prerequisites

### Required Setup
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve &

# Pull required models (see individual experiments)
```

### Model Requirements by Experiment
Each experiment specifies which models to pull before starting.

---

## Proposed Experiments

### 1.601 - Sentiment Analyzer
**Description**: Function that analyzes text sentiment (positive/negative/neutral) using local LLM
**Complexity**: Simple - single-turn prompt, clear output format
**Demo Value**: Shows basic Ollama integration, prompt engineering
**Time Estimate**: 3-4 minutes

**Required Models**:
```bash
ollama pull llama3.2:latest  # 2GB - fast, efficient
```

**Input**: Text string
**Output**: Sentiment label + confidence score
**Key Challenges**: Prompt design, output parsing, error handling

---

### 1.602 - Code Comment Generator
**Description**: Function that generates docstring comments for Python functions
**Complexity**: Simple - code understanding, structured output
**Demo Value**: Practical developer tool, shows code analysis
**Time Estimate**: 3-4 minutes

**Required Models**:
```bash
ollama pull codellama:7b  # 3.8GB - code-specialized
# OR
ollama pull qwen2.5-coder:7b  # 4.7GB - excellent for code
```

**Input**: Python function source code
**Output**: Formatted docstring with description, params, returns
**Key Challenges**: Code parsing, docstring formatting, edge cases

---

### 1.603 - Smart Text Summarizer
**Description**: Function that summarizes text to specified length with quality metrics
**Complexity**: Moderate - length control, quality assessment
**Demo Value**: Shows constraint handling, multi-step processing
**Time Estimate**: 4-5 minutes

**Required Models**:
```bash
ollama pull llama3.2:latest  # 2GB
```

**Input**: Long text + target length (words/sentences)
**Output**: Summary + metrics (compression ratio, key points preserved)
**Key Challenges**: Length constraints, quality measurement, testing

---

### 1.604 - Multi-Language Translator
**Description**: Function that translates text between languages with confidence scoring
**Complexity**: Moderate - language detection, quality validation
**Demo Value**: Shows practical utility, testing non-deterministic outputs
**Time Estimate**: 4-5 minutes

**Required Models**:
```bash
ollama pull llama3.2:latest  # 2GB - good multilingual support
```

**Input**: Text + target language
**Output**: Translation + confidence score + detected source language
**Key Challenges**: Quality validation, language detection, error cases

---

### 1.605 - Image Caption Generator
**Description**: Function that generates descriptive captions for images
**Complexity**: Moderate - vision model integration, multi-modal processing
**Demo Value**: **EXCELLENT for AI Tinkerers** - visual, multi-modal, impressive
**Time Estimate**: 4-5 minutes

**Required Models**:
```bash
ollama pull llava:7b  # 4.7GB - vision-language model
```

**Input**: Image file path
**Output**: Descriptive caption + detected objects/themes
**Key Challenges**: Image loading, vision model integration, quality assessment
**Demo Appeal**: Visual results are engaging and immediately understandable

---

### 1.606 - JSON Schema Generator
**Description**: Function that generates JSON schemas from example data
**Complexity**: Moderate - structured output, schema validation
**Demo Value**: Developer tool, shows structured generation
**Time Estimate**: 4-5 minutes

**Required Models**:
```bash
ollama pull qwen2.5-coder:7b  # 4.7GB - excellent for structured output
# OR
ollama pull llama3.2:latest  # 2GB - lighter alternative
```

**Input**: JSON example data
**Output**: Valid JSON Schema with types, constraints
**Key Challenges**: Schema correctness, validation, edge cases

---

### 1.607 - Regex Pattern Generator
**Description**: Function that generates regex patterns from natural language descriptions
**Complexity**: Moderate - pattern validation, test case generation
**Demo Value**: Practical utility, shows technical pattern generation
**Time Estimate**: 3-4 minutes

**Required Models**:
```bash
ollama pull codellama:7b  # 3.8GB - good for technical patterns
```

**Input**: Natural language description of pattern to match
**Output**: Regex pattern + test cases + explanation
**Key Challenges**: Pattern correctness, testing, complexity management

---

### 1.608 - Story-to-Haiku Converter
**Description**: Function that distills a story/paragraph into a haiku poem
**Complexity**: Simple - creative transformation, syllable counting
**Demo Value**: **EXCELLENT for AI Tinkerers** - creative, poetic, impressive output
**Time Estimate**: 3-4 minutes

**Required Models**:
```bash
ollama pull llama3.2:latest  # 2GB
```

**Input**: Story text (any length)
**Output**: Haiku (5-7-5 syllables) + syllable count validation
**Key Challenges**: Syllable counting accuracy, poetic quality, testing creativity
**Demo Appeal**: Beautiful output, shows AI creativity, easy to evaluate

---

### 1.609 - Intent Classifier
**Description**: Function that classifies user intent from natural language queries
**Complexity**: Moderate - classification taxonomy, confidence scoring
**Demo Value**: Shows practical chatbot/CLI component
**Time Estimate**: 4-5 minutes

**Required Models**:
```bash
ollama pull llama3.2:latest  # 2GB
```

**Input**: User query string + list of possible intents
**Output**: Classified intent + confidence + extracted entities
**Key Challenges**: Taxonomy design, accuracy testing, edge cases

---

### 1.610 - Fact Checker with Citations
**Description**: Function that verifies claims and identifies potential issues
**Complexity**: Complex - reasoning, citation format, uncertainty handling
**Demo Value**: Shows advanced reasoning capabilities
**Time Estimate**: 5-6 minutes

**Required Models**:
```bash
ollama pull llama3.2:latest  # 2GB
# OR for better reasoning
ollama pull llama3.1:8b  # 4.7GB
```

**Input**: Factual claim
**Output**: Verification result + reasoning + confidence + caveats
**Key Challenges**: Hallucination handling, confidence calibration, testing

---

## Recommended First Experiments for AI Tinkerers Demo

### Best Options (meets all criteria):

1. **1.608 - Story-to-Haiku Converter** ⭐ TOP PICK
   - ✅ Completes in 3-4 minutes
   - ✅ Small model (2GB) - quick to pull
   - ✅ Beautiful, creative output
   - ✅ Easy to understand and evaluate
   - ✅ Shows AI creativity
   - ✅ Audience will enjoy the poetry

2. **1.605 - Image Caption Generator** ⭐ RUNNER-UP
   - ✅ Completes in 4-5 minutes
   - ✅ Visual and engaging
   - ✅ Multi-modal (impressive)
   - ⚠️ Requires 4.7GB model (longer pull time)
   - ✅ Immediately understandable results

3. **1.601 - Sentiment Analyzer**
   - ✅ Fastest (3-4 minutes)
   - ✅ Smallest model (2GB)
   - ✅ Practical and clear
   - ⚠️ Less exciting than haiku/images

---

## Testing Strategies for Ollama Experiments

### CRITICAL INSIGHT: Mock During Development, Real at Demo End

**The Performance Breakthrough**: Local LLM calls are slow (~20-30s each), which would serialize the entire 4-method parallel execution. But we don't need real Ollama calls during development!

**Strategy**:
1. **Development Phase** (parallel, fast): All 4 methods use mocked LLM responses
2. **Demo Phase** (sequential, slow): Run comparison script with real Ollama once

**Why This Works**:
- ✅ Parallel methodology execution completes in 3-5 minutes
- ✅ Tests run instantly with mocks (no Ollama bottleneck)
- ✅ Real Ollama integration proven at the end
- ✅ Fits perfectly in 5-minute live demo window

### Implementation Pattern

**Design for dependency injection**:
```python
def story_to_haiku(text: str, llm_client=None) -> Haiku:
    """Convert story to haiku using LLM"""
    if llm_client is None:
        llm_client = ollama  # Real client

    response = llm_client.generate(
        model='llama3.2',
        prompt=f"Convert to haiku:\n{text}"
    )
    return parse_haiku(response['response'])
```

**Tests use mocks**:
```python
def test_story_to_haiku():
    mock_llm = Mock()
    mock_llm.generate.return_value = {
        'response': 'Cherry blossoms fall\nSoftly on the quiet pond\nSpring whispers arrive'
    }

    result = story_to_haiku("A story about spring...", llm_client=mock_llm)

    assert len(result.lines) == 3
    assert result.syllable_counts == [5, 7, 5]
```

**Comparison script uses real Ollama**:
```python
# methodology_comparison_demo.py
# Runs ONCE at the end, sequentially, with real Ollama
for method in [1, 2, 3, 4]:
    impl = import_method(method)
    # No mock - uses real ollama (slow but only runs once)
    result = impl.story_to_haiku(test_story)
    print(f"Method {method}: {result}")
```

### Testing Strategies

**1. Format Validation** (mock-friendly)
```python
assert len(haiku.lines) == 3
assert haiku.syllable_counts == [5, 7, 5]
assert all(isinstance(line, str) for line in haiku.lines)
```

**2. Edge Cases** (mock-friendly)
```python
assert story_to_haiku("") raises ValueError
assert story_to_haiku("x" * 10000) handles long input
```

**3. Quality Metrics** (real Ollama, comparison script only)
```python
# In comparison script, not in tests
haiku = story_to_haiku(test_story)  # Real Ollama call
quality_score = evaluate_poetic_quality(haiku)
print(f"Syllable accuracy: {quality_score.syllable_match}")
```

### Demo Timeline (Under 5 Minutes)

**Minute 0-3**: Parallel methodology execution
- All 4 methods develop simultaneously
- Tests run with mocks (instant)
- No Ollama calls yet

**Minute 3-4**: Code review
- Show implementation differences
- Highlight methodology patterns

**Minute 4-5**: Real Ollama demo
- Run comparison script once
- Show 4 different haiku outputs
- Discuss methodology impact on results

**Result**: Audience sees full parallel execution + real AI output, all under 5 minutes!

---

## Model Selection Guide

### For Quick Demos (<5 min total):
- **llama3.2:latest** (2GB) - Fast, capable, good balance
- Pre-pull before presentation!

### For Code Tasks:
- **qwen2.5-coder:7b** (4.7GB) - Best for code generation
- **codellama:7b** (3.8GB) - Good alternative

### For Vision Tasks:
- **llava:7b** (4.7GB) - Vision-language model
- **llava:13b** (8GB) - Better quality, slower

### For Reasoning Tasks:
- **llama3.1:8b** (4.7GB) - Better reasoning
- **mixtral:8x7b** (26GB) - Highest quality (too large for quick demo)

---

## Integration Notes

### Ollama Python Library
```bash
pip install ollama
```

### Basic Usage Pattern
```python
import ollama

response = ollama.generate(
    model='llama3.2',
    prompt='Your prompt here',
    options={'temperature': 0.7}
)

print(response['response'])
```

### Error Handling
```python
try:
    response = ollama.generate(model='llama3.2', prompt=text)
except ollama.ResponseError as e:
    # Handle model not found, service down, etc.
    pass
```

---

## Research Value

These experiments provide insights into:
- **Methodology adaptation** for AI service integration
- **Testing strategies** for non-deterministic systems
- **Prompt engineering** patterns across methodologies
- **Error handling** for external AI services
- **Quality assessment** without ground truth

**Expected Pattern**: Specification-driven approaches may over-engineer error handling while immediate implementation may under-test edge cases. Adaptive TDD should balance robustness with simplicity.

---

## Next Steps

1. **Choose experiment** based on demo constraints
2. **Pull required model** before starting (can take 5-10 minutes)
3. **Run spawn-experiments** with chosen experiment number
4. **Compare methodology approaches** to Ollama integration
5. **Share findings** with AI Tinkerers community

---

## Related Documents
- [Experiment Numbering System](EXPERIMENT_NUMBERING_SYSTEM.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Experiment Standards](../EXPERIMENT_STANDARDS.md)