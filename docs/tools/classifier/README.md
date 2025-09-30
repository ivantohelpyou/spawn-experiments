# Documentation Classification System

**Purpose**: Automated categorization and concept extraction for large documentation repositories

**Context**: Phase 1.1 of QRCards documentation archaeology

**Status**: Development - Documentation First Approach

---

## Overview

The Documentation Classification System is designed to process thousands of markdown files and automatically:
1. **Categorize** documents by content type (technical, business, marketing, etc.)
2. **Extract concepts** related to architectural decisions and system evolution
3. **Generate timelines** of documentation evolution
4. **Identify hotspots** where documentation clusters

This tool addresses the challenge of managing 3,000+ documentation files scattered across business, technical, and marketing contexts in unruly monorepos.

## Problem Statement

### The QRCards Documentation Challenge
- **Scale**: 3,000+ markdown files across multiple hierarchies
- **Complexity**: Mixed business, technical, marketing, and operational content
- **Evolution**: Documents created over months without systematic organization
- **Intent Discovery**: Need to surface architectural decisions and rationale buried in files

### Why Automated Classification?
Manual categorization of 3,000+ files is impractical. The classifier provides:
- **Speed**: Process entire repository in minutes vs. weeks manually
- **Consistency**: Objective categorization criteria applied uniformly
- **Concept Mining**: Extract key concepts that might be missed manually
- **Timeline Analysis**: Understand documentation evolution patterns

## Architecture

### Core Components

#### 1. Document Classifier (`DocumentClassifier` class)
**Purpose**: Main classification engine

**Responsibilities**:
- File content analysis and categorization
- Confidence scoring for classifications
- Concept extraction from content patterns
- Timeline and hotspot analysis

#### 2. Category System
**Categories Defined**:
- **Technical**: API docs, database schemas, deployment guides, architecture
- **Business**: Strategy, requirements, planning, customer needs
- **Marketing**: Sales materials, demos, showcases, presentations
- **Operational**: Deployment logs, monitoring, maintenance procedures
- **Development**: Implementation guides, testing, debugging, refactoring
- **Decisions**: Decision analysis, approaches, recommendations
- **Historical**: Archives, legacy docs, deprecated materials

#### 3. Concept Extraction Engine
**Target Concepts**:
- **Convention City**: Primary customer/use case references
- **Environment Matrix**: 3x3 environment architecture mentions
- **Database Architecture**: Admin/runtime separation decisions
- **Decisions**: Problem/solution pairs and rationale
- **Problems/Solutions**: Issue identification and resolution patterns

### Classification Methodology

#### Multi-Signal Hierarchical Approach
1. **Folder Structure Analysis**: Directory hierarchy provides primary categorization signals
2. **Path Pattern Recognition**: File location within organizational structure
3. **Content Keyword Matching**: Document content scanned for category-specific terms
4. **Content Pattern Recognition**: Regex patterns for technical and business concepts
5. **Cross-Validation**: Multiple signals combined for reliability assessment

#### Scoring Algorithm
```python
# For each category:
folder_score = analyze_folder_hierarchy(file_path)  # Primary signal
path_score = analyze_path_patterns(file_path)       # Secondary signal
content_score = (keyword_matches * 2) + (pattern_matches * 3)

total_score = (folder_score * 10) + (path_score * 5) + content_score
confidence = category_score / total_all_scores
```

**Rationale**: Folder structure weighted highest (intentional organization), followed by path patterns, then content analysis. This acknowledges that documentation organization reflects intended categorization.

## Usage Patterns

### Primary Use Cases

#### 1. Repository Archaeology
**Scenario**: Understanding large, organically grown documentation

**Process**:
1. Run classifier on entire repository
2. Review category distribution for organizational insights
3. Extract concept timeline to understand evolution
4. Identify documentation hotspots for focused review

#### 2. Intent Discovery
**Scenario**: Finding architectural decisions buried in documentation

**Process**:
1. Extract files mentioning "Convention City" for requirements context
2. Find "environment matrix" references for infrastructure decisions
3. Locate "database architecture" discussions for data design rationale
4. Map decision timeline for architectural evolution understanding

#### 3. Documentation Consolidation
**Scenario**: Reducing 3,000 files to manageable structure

**Process**:
1. Classify all files by content type
2. Identify high-confidence technical vs. business content
3. Find duplicate/overlapping concepts across files
4. Create consolidation strategy based on classification results

### Integration with Modernization Process

#### Phase 1.1: Automated Scanning (Current)
- **Input**: Raw repository with 3,000+ markdown files
- **Output**: Classified inventory with concept extraction
- **Purpose**: Foundation for manual review and synthesis

#### Phase 1.2: Manual Review (Next)
- **Input**: Classification results and concept maps
- **Output**: Validated concepts and decision timeline
- **Purpose**: Human validation of automated insights

#### Phase 2: Target Architecture (Future)
- **Input**: Intent understanding from archaeology
- **Output**: Architecture design informed by discovered rationale
- **Purpose**: Preserve intelligent decisions while eliminating chaos

## Output Formats

### 1. Classification Results (`classification_results.json`)
**Structure**:
```json
{
  "scan_date": "2025-09-26T...",
  "total_files": 3000,
  "categories": {
    "technical": {
      "files": [...],
      "count": 500,
      "avg_confidence": 0.75
    }
  },
  "concepts": {
    "convention_city": ["file1.md", "file2.md"],
    "environment_matrix": ["file3.md"]
  },
  "timeline": [...],
  "hotspots": {...}
}
```

### 2. Human-Readable Report (`classification_report.md`)
**Contents**:
- Category distribution with confidence levels
- Key concepts discovered with file references
- Documentation hotspots (directories with most files)
- Timeline insights (recent activity patterns)

### 3. Processing Logs
**Real-time feedback**:
- Progress indicators during processing
- Error handling for corrupted files
- Summary statistics upon completion

## Design Decisions

### Why Python?
- **Rich text processing**: Excellent regex and file handling libraries
- **JSON output**: Native support for structured data export
- **Cross-platform**: Runs consistently across development environments
- **Extensible**: Easy to add new classification categories and patterns

### Why Confidence Scoring?
- **Quality assessment**: Distinguishes clear categorizations from ambiguous ones
- **Review prioritization**: Focus human review on high-confidence results first
- **Iterative improvement**: Identify patterns that need refinement

### Why Multiple Output Formats?
- **JSON**: Machine-readable for further processing and analysis
- **Markdown**: Human-readable for immediate review and documentation
- **Logs**: Real-time feedback during processing

## Limitations and Future Enhancements

### Current Limitations
1. **English-only**: Designed for English markdown content
2. **Static categories**: Categories hardcoded, not dynamically discovered
3. **Content-only**: Doesn't analyze file relationships or dependencies
4. **No semantic analysis**: Keyword/pattern matching, not deep content understanding

### Planned Enhancements
1. **Machine Learning**: Train models on classified results for improved accuracy
2. **Relationship Analysis**: Map dependencies and references between documents
3. **Duplicate Detection**: Identify similar content across multiple files
4. **Version Analysis**: Track how documents evolved over time

## Integration Points

### With Augment
- **Input**: Classifier results inform Augment's architectural analysis
- **Output**: Augment validates classifier insights against full system context
- **Feedback**: Augment findings refine classifier patterns

### With Claude Code
- **Input**: Claude Code experiments validate extracted concepts
- **Output**: Experiment results improve classifier accuracy
- **Iteration**: Continuous refinement of classification patterns

### With Community Education
- **Pattern Library**: Successful classifications become reusable patterns
- **Documentation Strategy**: Classification approach informs methodology framework
- **Case Studies**: QRCards classification becomes community education example

---

## Implementation Guide

See [classifier-implementation.md](classifier-implementation.md) for detailed implementation instructions and code documentation.

## Related Documents
- [QRCards Documentation Archaeology Strategy](../../notes/034-qrcards-documentation-archaeology.md)
- [Parallel Tracks Strategy](../../notes/036-parallel-tracks-strategy.md)
- [Phase 1 Review and Next Steps](../../notes/035-phase1-review-and-next-steps.md)