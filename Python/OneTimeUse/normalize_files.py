#!/usr/bin/env python3
# Normalize line endings and clean up all markdown files

import os
import glob

# Get all markdown files in the directory
md_files = glob.glob(r"~\R\*.md")

print(f"Found {len(md_files)} markdown files")

for filepath in md_files:
    filename = os.path.basename(filepath)
    
    # Read file
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Convert to string
    text = content.decode('utf-8', errors='ignore')
    
    # Normalize line endings to LF
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove trailing whitespace from lines
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    
    # Remove multiple consecutive blank lines (keep max 2)
    cleaned_lines = []
    blank_count = 0
    for line in lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                cleaned_lines.append(line)
        else:
            blank_count = 0
            cleaned_lines.append(line)
    
    # Rejoin
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Ensure file ends with single newline
    if not cleaned_text.endswith('\n'):
        cleaned_text += '\n'
    
    # Write back with LF endings
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(cleaned_text)
    
    print(f"✓ Cleaned: {filename}")

print(f"\nAll {len(md_files)} files cleaned successfully!")
