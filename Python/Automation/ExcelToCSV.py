import pandas as pd
from pathlib import Path

input_file = Path("data.xlsx")
output_file = Path("data.csv")

if not input_file.exists():
    raise FileNotFoundError(f"Input file not found: {input_file}")

df = pd.read_excel(input_file)
df.to_csv(output_file, index=False)

print(f"Converted {input_file} → {output_file}")
