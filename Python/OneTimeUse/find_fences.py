import re

# Read the file
with open(r"~\R\Course_Manual.md", "r", encoding="utf-8") as f:
    content = f.read()

# Count occurrences of the bad fence
bad_fence = "\\\\\\\\\\\\"  # This is six backslashes in the raw string
count = content.count(bad_fence)
print(f"Found {count} occurrences of bad code fences")

# Also check for three backslashes on their own line
import re
matches = re.findall(r"^\\\\\\\\\\\\\s*$", content, re.MULTILINE)
print(f"Found {len(matches)} standalone bad fences")

# Show some context
lines = content.split('\n')
for i, line in enumerate(lines[:1000], 1):
    if line.strip() == "\\\\\\\\\\\\":
        print(f"Line {i}: Found bad fence")
        if i > 1:
            print(f"  Previous: {lines[i-2][:50]}")
        print(f"  Current: {line}")
        if i < len(lines):
            print(f"  Next: {lines[i][:50]}")
        break
