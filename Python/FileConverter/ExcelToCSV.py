import pandas as pd
import argparse
import sys
from pathlib import Path


def excel_to_csv(excel_file, output_csv=None, sheet_name=None, sheet_index=0, encoding='utf-8', delimiter=',', all_sheets=False):
    """
    Convert Excel file to CSV
    
    Args:
        excel_file: Path to Excel input file
        output_csv: Path to CSV output file (optional)
        sheet_name: Name of sheet to convert
        sheet_index: Index of sheet to convert (0-based)
        encoding: Output encoding
        delimiter: CSV delimiter
        all_sheets: Convert all sheets to separate CSV files
    """
    excel_path = Path(excel_file)
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_file}")
    
    # Read Excel file
    if all_sheets:
        # Read all sheets
        excel_data = pd.read_excel(excel_path, sheet_name=None, engine='openpyxl')
        
        print(f"Found {len(excel_data)} sheet(s) in {excel_file}")
        
        for sheet_name, df in excel_data.items():
            # Generate output filename
            safe_sheet_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in sheet_name)
            csv_output = excel_path.parent / f"{excel_path.stem}_{safe_sheet_name}.csv"
            
            df.to_csv(csv_output, index=False, encoding=encoding, sep=delimiter)
            print(f"✓ Converted sheet '{sheet_name}' ({len(df)} rows) → {csv_output.name}")
        
        return
    
    # Read specific sheet
    if sheet_name:
        df = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')
        print(f"Reading sheet: {sheet_name}")
    else:
        df = pd.read_excel(excel_path, sheet_name=sheet_index, engine='openpyxl')
        print(f"Reading sheet at index: {sheet_index}")
    
    # Determine output path
    if output_csv:
        csv_path = Path(output_csv)
    else:
        csv_path = excel_path.with_suffix('.csv')
    
    # Export to CSV
    df.to_csv(csv_path, index=False, encoding=encoding, sep=delimiter)
    
    print(f"✓ Converted {len(df)} rows → {csv_path}")


def batch_excel_to_csv(excel_files, output_dir=None, **kwargs):
    """Convert multiple Excel files to CSV"""
    for excel_file in excel_files:
        excel_path = Path(excel_file)
        
        if not excel_path.exists():
            print(f"⚠️  Skipping {excel_file}: File not found")
            continue
        
        try:
            print(f"\nProcessing: {excel_path.name}")
            
            # Override output path for batch mode
            if output_dir and not kwargs.get('all_sheets'):
                out_dir = Path(output_dir)
                out_dir.mkdir(parents=True, exist_ok=True)
                csv_file = out_dir / f"{excel_path.stem}.csv"
                excel_to_csv(excel_file, output_csv=csv_file, **kwargs)
            else:
                excel_to_csv(excel_file, **kwargs)
                
        except Exception as e:
            print(f"✗ Error processing {excel_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Excel files to CSV format with sheet selection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Convert first sheet
  %(prog)s data.xlsx -o output.csv
  
  # Convert specific sheet by name
  %(prog)s data.xlsx -o output.csv --sheet "Sales Data"
  
  # Convert specific sheet by index
  %(prog)s data.xlsx --sheet-index 2
  
  # Convert all sheets to separate CSV files
  %(prog)s data.xlsx --all-sheets
  
  # Custom delimiter (tab-separated)
  %(prog)s data.xlsx -o output.tsv --delimiter "\\t"
  
  # Batch conversion
  %(prog)s file1.xlsx file2.xlsx --batch --output-dir csv_files
        '''
    )
    
    parser.add_argument('input', nargs='*', help='Excel file(s) to convert')
    parser.add_argument('-o', '--output', help='Output CSV file path')
    parser.add_argument('--sheet', dest='sheet_name', help='Sheet name to convert')
    parser.add_argument('--sheet-index', type=int, default=0, help='Sheet index to convert (0-based, default: 0)')
    parser.add_argument('--all-sheets', action='store_true', help='Convert all sheets to separate CSV files')
    parser.add_argument('--delimiter', '--sep', default=',', help='CSV delimiter (default: comma)')
    parser.add_argument('--encoding', default='utf-8', help='Output encoding (default: utf-8)')
    parser.add_argument('--batch', action='store_true', help='Batch mode: convert multiple Excel files')
    parser.add_argument('--output-dir', help='Output directory for batch mode')
    
    args = parser.parse_args()
    
    try:
        # Interactive mode
        if not args.input:
            print("Excel to CSV Converter")
            print("=" * 50)
            
            excel_file = input("Excel file for input: ").strip() or "data.xlsx"
            
            # Check if file exists
            if not Path(excel_file).exists():
                print(f"Error: File not found: {excel_file}")
                sys.exit(1)
            
            # Ask about sheets
            try:
                import openpyxl
                wb = openpyxl.load_workbook(excel_file, read_only=True)
                sheet_names = wb.sheetnames
                wb.close()
                
                print(f"\nAvailable sheets:")
                for i, name in enumerate(sheet_names):
                    print(f"  {i}: {name}")
                
                choice = input("\nConvert (a)ll sheets or (s)pecific sheet? [a/s]: ").strip().lower()
                
                if choice == 'a':
                    excel_to_csv(excel_file, all_sheets=True)
                else:
                    sheet_input = input("Sheet name or index: ").strip()
                    
                    # Check if input is a number (index) or name
                    if sheet_input.isdigit():
                        sheet_index = int(sheet_input)
                        csv_file = input("Output CSV file: ").strip() or None
                        excel_to_csv(excel_file, output_csv=csv_file, sheet_index=sheet_index)
                    else:
                        csv_file = input("Output CSV file: ").strip() or None
                        excel_to_csv(excel_file, output_csv=csv_file, sheet_name=sheet_input)
            
            except ImportError:
                print("Note: openpyxl not available for sheet listing")
                csv_file = input("Output CSV file: ").strip() or None
                excel_to_csv(excel_file, output_csv=csv_file)
        
        # Batch mode
        elif args.batch:
            batch_excel_to_csv(
                args.input,
                output_dir=args.output_dir,
                sheet_name=args.sheet_name,
                sheet_index=args.sheet_index,
                encoding=args.encoding,
                delimiter=args.delimiter,
                all_sheets=args.all_sheets
            )
        
        # Single file mode
        else:
            if len(args.input) > 1 and not args.batch:
                print("Error: Specify only one input file, or use --batch for multiple files")
                sys.exit(1)
            
            excel_to_csv(
                args.input[0],
                output_csv=args.output,
                sheet_name=args.sheet_name,
                sheet_index=args.sheet_index,
                encoding=args.encoding,
                delimiter=args.delimiter,
                all_sheets=args.all_sheets
            )
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
