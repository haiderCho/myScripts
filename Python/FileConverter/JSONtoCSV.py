import json
import csv

# Specify file paths
input_json_file = 'input.json'
output_csv_file = 'output.csv'

try:
    # Load JSON data from file
    with open(input_json_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    if not data:
        raise ValueError("JSON file is empty!")

    # Write CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Use DictWriter for safe header handling
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Conversion successful! The output file is saved as: {output_csv_file}")

except FileNotFoundError:
    print(f"Error: File '{input_json_file}' not found.")
except json.JSONDecodeError:
    print(f"Error: File '{input_json_file}' is not a valid JSON.")
except Exception as e:
    print(f"Unexpected error: {e}")

