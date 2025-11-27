import csv
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime


def convert_value(value, preserve_strings=False, parse_dates=False):
    """Convert string values to appropriate Python types"""
    if preserve_strings:
        return value
    
    if not value:
        return None
    
    # Try date parsing if enabled
    if parse_dates:
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']
        for fmt in date_formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.isoformat()
            except ValueError:
                pass
    
    # Try numeric conversion
    if value.isdigit():
        return int(value)
    
    try:
        float_val = float(value)
        return float_val
    except ValueError:
        pass
    
    # Boolean conversion
    if value.lower() in ('true', 'yes', '1'):
        return True
    if value.lower() in ('false', 'no', '0'):
        return False
    
    return value


def csv_to_json(csv_file, json_file, preserve_strings=False, parse_dates=False, pretty=True, encoding='utf-8'):
    """Convert CSV to JSON with auto-detection of delimiter"""
    csv_path = Path(csv_file)
    json_path = Path(json_file)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    # Detect CSV dialect automatically
    with open(csv_path, 'r', encoding=encoding) as file:
        sample = file.read(8192)  # Read larger sample
        file.seek(0)
        
        try:
            dialect = csv.Sniffer().sniff(sample)
            print(f"Detected delimiter: '{dialect.delimiter}'")
        except csv.Error:
            print("Could not auto-detect delimiter, using comma")
            dialect = 'excel'
        
        reader = csv.DictReader(file, dialect=dialect)
        
        data = []
        for row in reader:
            # Convert values to appropriate data types
            parsed_row = {
                key: convert_value(value, preserve_strings, parse_dates) 
                for key, value in row.items()
            }
            data.append(parsed_row)
    
    # Write JSON output
    indent = 4 if pretty else None
    with open(json_path, 'w', encoding=encoding) as outfile:
        json.dump(data, outfile, indent=indent, ensure_ascii=False)
    
    print(f"✓ Converted {len(data)} rows from '{csv_file}' to '{json_file}'")


def batch_csv_to_json(csv_files, output_dir=None, **kwargs):
    """Convert multiple CSV files to JSON"""
    for csv_file in csv_files:
        csv_path = Path(csv_file)
        
        if not csv_path.exists():
            print(f"⚠️  Skipping {csv_file}: File not found")
            continue
        
        # Determine output path
        if output_dir:
            out_dir = Path(output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            json_file = out_dir / f"{csv_path.stem}.json"
        else:
            json_file = csv_path.with_suffix('.json')
        
        try:
            print(f"\nProcessing: {csv_path.name}")
            csv_to_json(csv_file, json_file, **kwargs)
        except Exception as e:
            print(f"✗ Error processing {csv_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert CSV files to JSON format with type conversion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic conversion
  %(prog)s input.csv -o output.json
  
  # Preserve all values as strings
  %(prog)s input.csv -o output.json --preserve-strings
  
  # Parse dates to ISO format
  %(prog)s input.csv -o output.json --parse-dates
  
  # Compact output (no pretty printing)
  %(prog)s input.csv -o output.json --no-pretty
  
  # Batch conversion
  %(prog)s file1.csv file2.csv file3.csv --batch --output-dir json_files
        '''
    )
    
    parser.add_argument('input', nargs='*', help='CSV file(s) to convert')
    parser.add_argument('-o', '--output', help='Output JSON file path')
    parser.add_argument('--preserve-strings', action='store_true', 
                       help='Keep all values as strings (no type conversion)')
    parser.add_argument('--parse-dates', action='store_true',
                       help='Attempt to parse and convert date fields')
    parser.add_argument('--no-pretty', action='store_false', dest='pretty',
                       help='Compact JSON output (no indentation)')
    parser.add_argument('--encoding', default='utf-8',
                       help='File encoding (default: utf-8)')
    parser.add_argument('--batch', action='store_true',
                       help='Batch mode: convert multiple CSV files')
    parser.add_argument('--output-dir', help='Output directory for batch mode')
    
    args = parser.parse_args()
    
    try:
        # Interactive mode
        if not args.input:
            print("CSV to JSON Converter")
            print("=" * 50)
            
            csv_file = input("CSV file for input: ").strip() or "input.csv"
            json_file = input("JSON file for output: ").strip() or "output.json"
            
            csv_to_json(csv_file, json_file, pretty=True, encoding=args.encoding)
        
        # Batch mode
        elif args.batch:
            batch_csv_to_json(
                args.input,
                output_dir=args.output_dir,
                preserve_strings=args.preserve_strings,
                parse_dates=args.parse_dates,
                pretty=args.pretty,
                encoding=args.encoding
            )
        
        # Single file mode
        else:
            if len(args.input) > 1:
                print("Error: Specify only one input file, or use --batch for multiple files")
                sys.exit(1)
            
            csv_file = args.input[0]
            json_file = args.output or Path(csv_file).with_suffix('.json')
            
            csv_to_json(
                csv_file,
                json_file,
                preserve_strings=args.preserve_strings,
                parse_dates=args.parse_dates,
                pretty=args.pretty,
                encoding=args.encoding
            )
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except csv.Error as e:
        print(f"CSV parsing error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
