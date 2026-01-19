#!/usr/bin/env python3
# Replace bad code fences with proper markdown

import re

# Read the file
with open(r"~\R\Course_Manual.md", "r", encoding="utf-8") as f:
    content = f.read()

# Track changes
original_content = content
changes = 0

# Replace lines that are only backslashes (3 or more) with proper code fences
lines = content.split('\n')
new_lines = []
in_code_block = False

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Check if this line is only backslashes (3 backslashes specifically based on what we found)
    if stripped == '\\\\\\':
        if not in_code_block:
            # Start of code block
            new_lines.append('```r')
            in_code_block = True
            changes += 1
        else:
            # End of code block
            new_lines.append('```')
            in_code_block = False
            changes += 1
    else:
        new_lines.append(line)

result = '\n'.join(new_lines)

# Write the fixed content
with open(r"~\R\Course_Manual.md", "w", encoding="utf-8") as f:
    f.write(result)

print(f"Fixed {changes} bad code fences")
print(f"File updated successfully")
