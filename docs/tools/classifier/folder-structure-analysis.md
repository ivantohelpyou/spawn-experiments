# Folder Structure Analysis for Documentation Classification

**Purpose**: Leverage directory hierarchy as primary classification signal

**Context**: QRCards repository has intentional organizational patterns
**Key Insight**: Folder structure reflects creator intent more reliably than content analysis

---

## QRCards Folder Structure Patterns

### Observed Organizational Intelligence

From the QRCards repository scan, clear organizational patterns emerge:

```
~/qrcards/
├── /docs/ (95M - 963 files)                    # Primary documentation hub
│   ├── /business/ (10 subdirs)                 # Business strategy and planning
│   ├── /marketing/ (15 subdirs)                # Sales and promotional materials
│   ├── /technical/ (18 subdirs)                # Technical implementation docs
│   ├── /ai-collaboration/                      # AI-assisted development logs
│   ├── /methodology/                           # Development methodology docs
│   └── /training/                              # Onboarding and education
├── /project/ (2,225 files)                     # Project management and execution
│   ├── /mvp/phase5/ (timestamped reports)      # Development phase tracking
│   ├── /development-guides/                    # Implementation guidance
│   ├── /demo-content-library/                  # Customer-facing materials
│   └── /z_archive/ (historical decisions)      # Archived decision records
├── /packages/ (per-package docs)               # Technical component documentation
│   ├── /flasklayer/docs/ (948K)               # Web application documentation
│   ├── /dap-processor/docs/ (288K)            # Card generation documentation
│   └── /dashboard/docs/ (212K)                # Admin interface documentation
└── /scripts/ (35 subdirs)                     # Operational procedure documentation
```

### Classification Signals from Structure

#### Strong Category Indicators

**Business Intent**:
- `/docs/business/` → High confidence business classification
- `/project/planning/` → Business/strategy content
- `/docs/sales/` → Marketing/business hybrid

**Technical Intent**:
- `/packages/*/docs/` → Technical implementation documentation
- `/docs/technical/` → Technical reference materials
- `/docs/api/` → Technical interface documentation

**Operational Intent**:
- `/scripts/*/` → Operational procedures and deployment
- `/docs/deployment/` → Operational guidance
- `/docs/operations/` → System management

**Historical Intent**:
- `/z_archive/` → Explicit archival designation
- `/legacy-docs/` → Historical reference materials
- `/completed/` → Finished project documentation

#### Ambiguous Patterns

**Mixed Context Directories**:
- `/docs/ai-collaboration/` → Could be technical or methodology
- `/project/action/` → Could be business or operational
- `/docs/workflows/` → Could be technical or operational

**Timestamped Directories**:
- `/project/mvp/phase5/2025-05-*` → Date suggests historical, but may be active
- `/sessions/` → Could be meeting notes (business) or debug sessions (technical)

## Folder Analysis Algorithm

### Hierarchical Weight Assignment

#### Primary Classification (Weight: 10)
```python
def analyze_primary_folder(path_parts):
    """Extract primary intent from top-level organization."""
    if 'docs' in path_parts:
        if 'business' in path_parts: return 'business'
        if 'technical' in path_parts: return 'technical'
        if 'marketing' in path_parts: return 'marketing'
        if 'sales' in path_parts: return 'marketing'
        if 'operations' in path_parts: return 'operational'
        if 'deployment' in path_parts: return 'operational'

    if 'packages' in path_parts and 'docs' in path_parts:
        return 'technical'

    if 'scripts' in path_parts:
        return 'operational'

    if any(archive in path_parts for archive in ['z_archive', 'legacy', 'completed']):
        return 'historical'

    return None
```

#### Secondary Classification (Weight: 5)
```python
def analyze_secondary_folder(path_parts):
    """Extract secondary intent from deeper hierarchy."""
    # Look for intent keywords in any level
    for part in path_parts:
        if part in ['api', 'schema', 'database', 'deployment']:
            return 'technical'
        if part in ['strategy', 'planning', 'requirements']:
            return 'business'
        if part in ['demo', 'showcase', 'presentation']:
            return 'marketing'
        if part in ['logs', 'monitoring', 'backup']:
            return 'operational'

    return None
```

#### Temporal Analysis (Weight: 3)
```python
def analyze_temporal_patterns(path_parts):
    """Detect temporal organization patterns."""
    # Look for date patterns in folder names
    date_pattern = re.compile(r'20\d{2}-\d{2}-\d{2}')
    phase_pattern = re.compile(r'phase\d+')

    has_dates = any(date_pattern.search(part) for part in path_parts)
    has_phases = any(phase_pattern.search(part) for part in path_parts)

    if has_dates or has_phases:
        # Recent dates suggest active development
        # Old dates suggest historical
        return analyze_date_recency(path_parts)

    return None
```

### Content-Structure Validation

#### Cross-Validation Strategy
1. **Structure Suggests**: Folder analysis provides primary classification
2. **Content Confirms**: Content analysis validates or challenges folder classification
3. **Confidence Adjustment**: High agreement = high confidence, disagreement = lower confidence

#### Disagreement Resolution
```python
def resolve_classification_conflict(folder_classification, content_classification):
    """Handle cases where folder and content suggest different categories."""

    # High confidence folder classification overrides content
    if folder_confidence > 0.8:
        return folder_classification, folder_confidence * 0.9

    # Strong content signals can override weak folder signals
    if content_confidence > 0.7 and folder_confidence < 0.5:
        return content_classification, content_confidence * 0.8

    # Hybrid classification for genuine mixed content
    if abs(folder_confidence - content_confidence) < 0.2:
        return create_hybrid_classification(folder_classification, content_classification)

    # Default to folder classification with reduced confidence
    return folder_classification, min(folder_confidence, content_confidence)
```

## Implementation Strategy

### Phase 1: Folder Pattern Discovery
1. **Scan Directory Structure**: Map all folder hierarchies
2. **Identify Patterns**: Extract common organizational patterns
3. **Weight Assignment**: Assign classification weights to folder patterns
4. **Validation**: Test against known file classifications

### Phase 2: Hybrid Classification
1. **Folder Analysis**: Primary classification from directory structure
2. **Content Analysis**: Secondary validation from file content
3. **Confidence Scoring**: Combine signals with appropriate weighting
4. **Conflict Resolution**: Handle disagreements between signals

### Phase 3: Pattern Learning
1. **Success Analysis**: Identify most reliable folder patterns
2. **Pattern Extraction**: Create reusable folder classification rules
3. **Community Patterns**: Document patterns for other repositories
4. **Methodology Integration**: Include folder analysis in classification methodology

## Expected Benefits

### Improved Accuracy
- **Creator Intent**: Folder structure reflects how creator organized information
- **Organizational Logic**: Directory hierarchy shows intended relationships
- **Context Preservation**: Spatial organization provides semantic context

### Reduced False Positives
- **Business vs Technical**: Clear separation in well-organized repositories
- **Active vs Historical**: Archive folders clearly marked
- **Operational vs Development**: Scripts vs docs clearly separated

### Scalability
- **Quick Classification**: Folder analysis faster than content analysis
- **Bulk Processing**: Directory patterns apply to many files simultaneously
- **Hierarchy Leverage**: Parent folder classification inherits to children

## Integration with Content Analysis

### Complementary Approaches
- **Folder Structure**: Provides organizational intent
- **Content Analysis**: Provides semantic validation
- **Combined Signal**: Higher confidence than either alone

### Quality Assurance
- **Agreement Validation**: High confidence when both approaches agree
- **Disagreement Investigation**: Lower confidence triggers manual review
- **Pattern Refinement**: Disagreements improve classification rules

---

## Related Documents
- [Classifier README](README.md) - Main classifier documentation
- [Implementation Guide](classifier-implementation.md) - Technical implementation details
- [QRCards Documentation Archaeology](../../notes/034-qrcards-documentation-archaeology.md) - Overall strategy