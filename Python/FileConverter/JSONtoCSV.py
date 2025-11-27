import json
import csv
import argparse
import sys
from pathlib import Path


def flatten_dict(d, parent_key='', sep='_'):
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Convert list to string representation
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_csv(json_file, csv_file, flatten=False, fields=None, encoding='utf-8', delimiter=','):
    """
    Convert JSON to CSV
    
    Args:
        json_file: Path to JSON input file
        csv_file: Path to CSV output file
        flatten: Flatten nested JSON objects
        fields: List of fields to include (None = all fields)
        encoding: File encoding
        delimiter: CSV delimiter
    """
    json_path = Path(json_file)
    csv_path = Path(csv_file)
    
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")
    
    # Load JSON data
    with open(json_path, 'r', encoding=encoding) as f:
        data = json.load(f)
    
    # Validate data structure
    if not data:
        raise ValueError("JSON file is empty!")
    
    if not isinstance(data, list):
        # If root is a dict, try to find a list inside
        if isinstance(data, dict):
            # Look for list values
            list_values = [v for v in data.values() if isinstance(v, list)]
            if list_values:
                print(f"Warning: Root is a dict. Using first list value ({len(list_values[0])} items)")
                data = list_values[0]
            else:
                print("Warning: Root is a dict, not a list. Wrapping in list.")
                data = [data]
        else:
            raise ValueError("JSON root must be a list of objects or a dict containing a list")
    
    # Flatten if requested
    if flatten:
        print("Flattening nested JSON structures...")
        data = [flatten_dict(item) if isinstance(item, dict) else item for item in data]
    
    # Handle nested objects by converting to strings
    processed_data = []
    for item in data:
        if not isinstance(item, dict):
            print(f"Warning: Skipping non-dict item: {type(item)}")
            continue
        
        processed_item = {}
        for key, value in item.items():
            if isinstance(value, (dict, list)):
                # Convert complex types to JSON string
                processed_item[key] = json.dumps(value, ensure_ascii=False)
            else:
                processed_item[key] = value
        processed_data.append(processed_item)
    
    if not processed_data:
        raise ValueError("No valid data rows to export")
    
    # Determine fieldnames
    all_fields = set()
    for item in processed_data:
        all_fields.update(item.keys())
    
    if fields:
        # Use specified fields only
        fieldnames = [f for f in fields if f in all_fields]
        if not fieldnames:
            raise ValueError(f"None of the specified fields exist in data: {fields}")
        print(f"Exporting fields: {', '.join(fieldnames)}")
    else:
        fieldnames = sorted(all_fields)
    
    # Write CSV
    with open(csv_path, 'w', newline='', encoding=encoding) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(processed_data)
    
    print(f"✓ Converted {len(processed_data)} rows with {len(fieldnames)} fields → {csv_path}")


def batch_json_to_csv(json_files, output_dir=None, **kwargs):
    """Convert multiple JSON files to CSV"""
    for json_file in json_files:
        json_path = Path(json_file)
        
        if not json_path.exists():
            print(f"⚠️  Skipping {json_file}: File not found")
            continue
        
        # Determine output path
        if output_dir:
            out_dir = Path(output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            csv_file = out_dir / f"{json_path.stem}.csv"
        else:
            csv_file = json_path.with_suffix('.csv')
        
        try:
            print(f"\nProcessing: {json_path.name}")
            json_to_csv(json_file, csv_file, **kwargs)
        except Exception as e:
            print(f"✗ Error processing {json_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert JSON files to CSV format with nested object support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic conversion
  %(prog)s input.json -o output.csv
  
  # Flatten nested objects
  %(prog)s input.json -o output.csv --flatten
  
  # Export specific fields only
  %(prog)s input.json -o output.csv --fields name email age
  
  # Custom delimiter (tab-separated)
  %(prog)s input.json -o output.tsv --delimiter "\\t"
  
  # Batch conversion
  %(prog)s file1.json file2.json file3.json --batch --output-dir csv_files

Notes:
  - JSON root should be a list of objects
  - Nested objects will be converted to JSON strings (or flattened with --flatten)
  - Arrays within objects will be converted to strings
        '''
    )
    
    parser.add_argument('input', nargs='*', help='JSON file(s) to convert')
    parser.add_argument('-o', '--output', help='Output CSV file path')
    parser.add_argument('--flatten', action='store_true', help='Flatten nested JSON objects')
    parser.add_argument('--fields', nargs='+', help='Specific fields to export')
    parser.add_argument('--delimiter', '--sep', default=',', help='CSV delimiter (default: comma)')
    parser.add_argument('--encoding', default='utf-8', help='File encoding (default: utf-8)')
    parser.add_argument('--batch', action='store_true', help='Batch mode: convert multiple JSON files')
    parser.add_argument('--output-dir', help='Output directory for batch mode')
    
    args = parser.parse_args()
    
    try:
        # Interactive mode
        if not args.input:
            print("JSON to CSV Converter")
            print("=" * 50)
            
            json_file = input("JSON file for input: ").strip() or "input.json"
            csv_file = input("CSV file for output: ").strip() or "output.csv"
            
            json_to_csv(json_file, csv_file, encoding=args.encoding)
        
        # Batch mode
        elif args.batch:
            batch_json_to_csv(
                args.input,
                output_dir=args.output_dir,
                flatten=args.flatten,
                fields=args.fields,
                encoding=args.encoding,
                delimiter=args.delimiter
            )
        
        # Single file mode
        else:
            if len(args.input) > 1:
                print("Error: Specify only one input file, or use --batch for multiple files")
                sys.exit(1)
            
            json_file = args.input[0]
            csv_file = args.output or Path(json_file).with_suffix('.csv')
            
            json_to_csv(
                json_file,
                csv_file,
                flatten=args.flatten,
                fields=args.fields,
                encoding=args.encoding,
                delimiter=args.delimiter
            )
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
