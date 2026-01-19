#!/usr/bin/env python3
# Check the actual character pattern in the file

with open(r"~\R\Course_Manual.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("\nChecking line 817 (index 816):")
if len(lines) > 816:
    line = lines[816]
    print(f"Line content: {repr(line)}")
    print(f"Line stripped: '{line.strip()}'")
    print(f"Line bytes: {line.encode('utf-8')}")
    
print("\nLooking for lines with only backslashes:")
for i, line in enumerate(lines[:1500], 1):
    stripped = line.strip()
    if stripped and all(c == '\\' for c in stripped):
        print(f"Line {i}: {repr(line)} (length={len(stripped)})")
        if i < 10:  # Show first few
            if i > 1:
                print(f"  Before: {lines[i-2].strip()[:60]}")
            print(f"  After: {lines[i].strip()[:60]}")
