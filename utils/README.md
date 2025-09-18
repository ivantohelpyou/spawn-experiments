# Utils Directory - Discovered Components System

## Purpose

This directory contains proven components from completed experiments, available for **organic discovery** by future experimental agents.

## Structure

### `functions/` - Tier 1 Components
Contains well-tested function implementations from Tier 1 experiments:
- Single functions with clear interfaces
- Comprehensive test coverage
- Standard library dependencies only
- Ready for import and reuse

### `tools/` - Tier 2 Components
Contains CLI tools and utilities from Tier 2 experiments:
- Command-line interfaces
- File processing utilities
- Composable tool components
- May depend on Tier 1 functions

## Discovered Components Protocol

### **No Explicit Guidance**
- Components are **not mentioned** in experiment prompts
- Agents discover them naturally through codebase exploration
- Research measures organic discovery and utilization patterns

### **Research Questions**
1. **Which methodologies naturally explore existing codebases?**
2. **How do different approaches evaluate found components?**
3. **What drives reuse vs. rebuild decisions?**
4. **How does component availability influence system architecture?**

### **Component Quality Standards**
- **Functional correctness**: All components must work as documented
- **Clear interfaces**: Obvious usage patterns and parameters
- **Test coverage**: Comprehensive validation included
- **Documentation**: Basic docstrings explaining purpose and usage

## Population Process

### After Tier 1 Completion
Best function implementations are copied to `functions/` with:
- Original filename preserved
- Tests included where applicable
- Basic documentation maintained
- Import paths clearly defined

### After Tier 2 Completion
Best tool implementations are copied to `tools/` with:
- CLI interfaces documented
- Usage examples provided
- Dependencies noted
- Integration patterns demonstrated

## Research Value

This system enables study of **authentic development behavior** in environments with existing codebases, revealing:
- Natural component discovery patterns
- Methodology-specific evaluation criteria
- Integration strategy differences
- Architecture emergence with available building blocks

The discovered components approach preserves experimental validity while studying realistic development scenarios where developers must navigate existing project assets.