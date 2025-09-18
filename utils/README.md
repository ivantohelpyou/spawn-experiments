# Utils Directory

## Purpose

Collection of utility functions and tools for general use in development projects.

## Structure

### `functions/`
Utility functions for common programming tasks:
- Text processing and string manipulation
- Data structure operations
- Mathematical and algorithmic helpers
- File and I/O utilities

### `tools/`
Command-line utilities and development tools:
- Text processing tools
- File manipulation utilities
- Data formatting helpers
- Development workflow tools

## Usage

Import functions directly into your projects:
```python
from utils.functions.text_processor import normalize_text
from utils.functions.data_helper import merge_dictionaries
```

Use tools from command line:
```bash
python utils/tools/formatter.py input.csv --output json
python utils/tools/analyzer.py --input data.txt --stats
```

## Organization

Components are organized by functionality and complexity:
- **functions/**: Reusable function libraries
- **tools/**: Standalone command-line utilities

Each component includes basic documentation and usage examples.