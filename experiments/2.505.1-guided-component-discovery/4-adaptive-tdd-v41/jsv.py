#!/usr/bin/env python3
"""
JSON Schema Validator CLI Tool
Main entry point for the jsv command-line tool.
"""

import sys
import os

# Add the jsv module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'jsv'))

from jsv.cli import main

if __name__ == '__main__':
    sys.exit(main())