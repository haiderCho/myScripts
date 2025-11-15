import csv
import json


def convert_value(value):
    """Convert numeric strings to int or float when possible."""
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value  # leave as string


def csv_to_json(csv_file, json_file):
    try:
        # Detect CSV dialect automatically
        with open(csv_file, 'r', encoding='utf-8') as file:
            sample = file.read(1024)
            file.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            reader = csv.DictReader(file, dialect=dialect)

            data = []
            for row in reader:
                # Convert values to appropriate data types
                parsed_row = {key: convert_value(value) for key, value in row.items()}
                data.append(parsed_row)

        # Write JSON output
        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

        print(f"CSV file '{csv_file}' has been converted to JSON file '{json_file}'.")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except csv.Error as e:
        print(f"CSV parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Example usage
if __name__ == "__main__":
    csv_file = "input.csv"
    json_file = "output.json"
    csv_to_json(csv_file, json_file)

