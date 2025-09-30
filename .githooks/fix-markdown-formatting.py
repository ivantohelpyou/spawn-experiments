#!/usr/bin/env python3
"""
Fix markdown formatting issues by adding blank lines between
consecutive bold metadata lines (**Key**: value format).

Usage: python3 .githooks/fix-markdown-formatting.py [file1.md file2.md ...]
       If no files specified, fixes all *.md files in repo.
"""

import re
import sys
import glob
from pathlib import Path

def fix_markdown_formatting(file_path):
    """Fix consecutive bold metadata lines by adding blank lines between them."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return 0

    fixed_lines = []
    fixed_count = 0

    for i in range(len(lines)):
        fixed_lines.append(lines[i])

        # Check if current line is bold metadata and next line is also bold metadata
        if i < len(lines) - 1:
            current_is_bold = re.match(r'^\*\*[A-Za-z]+\*\*:', lines[i])
            next_is_bold = re.match(r'^\*\*[A-Za-z]+\*\*:', lines[i+1])

            if current_is_bold and next_is_bold:
                # Add blank line between them
                fixed_lines.append('\n')
                fixed_count += 1

    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        return fixed_count
    return 0

def main():
    # Get files to fix
    if len(sys.argv) > 1:
        files_to_fix = sys.argv[1:]
    else:
        # Fix all markdown files in repo
        files_to_fix = glob.glob('**/*.md', recursive=True)
        files_to_fix = [f for f in files_to_fix
                       if not f.startswith('.venv/')
                       and not f.startswith('archive/')
                       and not f.startswith('.git/')]

    total_fixed = 0
    files_fixed = []

    for md_file in files_to_fix:
        if not Path(md_file).exists():
            continue

        try:
            count = fix_markdown_formatting(md_file)
            if count > 0:
                total_fixed += count
                files_fixed.append((md_file, count))
        except Exception as e:
            print(f"Error fixing {md_file}: {e}")

    if total_fixed > 0:
        print(f"✅ Fixed {total_fixed} formatting issues in {len(files_fixed)} files:\n")
        for file, count in files_fixed[:15]:
            print(f"   {file}: {count} fixes")
        if len(files_fixed) > 15:
            print(f"   ... and {len(files_fixed) - 15} more files")
        print("\n💡 Run 'git add' to stage the changes")
    else:
        print("✅ No formatting issues found!")

    return 0

if __name__ == '__main__':
    sys.exit(main())
