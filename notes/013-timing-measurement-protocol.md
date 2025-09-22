# Timing Measurement Protocol for Spawn Experiments

## Primary Timing Source: Task Tool Execution

The Task tool provides the most accurate timing measurement because it:
- Captures complete development workflow
- Includes tool usage overhead
- Reflects real development time including thinking/planning
- Measures from prompt start to completion

## Implementation Guidelines

### 1. Experiment Execution
```bash
# Always launch methods in parallel for fair comparison
Task(method1) + Task(method2) + Task(method3) + Task(method4)
```

### 2. Timing Collection
Record Task execution times from output:
```
● Task(Execute Method 1: Immediate Implementation)
  ⎿  Done (12 tool uses · 16.6k tokens · 1m 17.4s)  ← USE THIS TIME
```

### 3. Report Template
```markdown
### Development Speed
1. **Method 1**: 1m 17s (Task execution)
2. **Method 2**: 4m 49s (Task execution)
3. **Method 3**: 8m 33s (Task execution)
4. **Method 4**: 9m 20s (Task execution)
```

### 4. File Timestamp Usage
- Use only for validation/sanity checking
- Should align with Task execution order
- Not primary timing source

## Quality Assurance

1. **Timing Consistency Check**: Task times should follow logical progression based on methodology complexity
2. **Sanity Validation**: File timestamps should not conflict with Task execution order
3. **Documentation**: Always specify "Task execution time" in reports

## Future Automation Ideas

1. **Timing Parser**: Script to extract Task times from experiment output
2. **Report Generator**: Auto-populate timing sections from Task data
3. **Validation Checker**: Verify Task times vs file timestamps for anomalies

## Standard Phrases for Reports

- "Development time measured by Task tool execution"
- "Task execution time: Xm Xs"
- "Primary timing source: Task tool measurement"
- "File timestamps used for validation only"