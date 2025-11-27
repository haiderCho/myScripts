import os
import argparse
import sys
import re
import json
from datetime import datetime
from pathlib import Path


def get_files_in_folder(folder, extensions=None, recursive=False):
    """Get all files in folder, optionally filtered by extension"""
    folder_path = Path(folder)
    
    if not folder_path.exists():
        raise ValueError(f"Folder does not exist: {folder}")
    
    if not folder_path.is_dir():
        raise ValueError(f"Path is not a directory: {folder}")
    
    files = []
    
    if recursive:
        pattern = "**/*"
        all_items = folder_path.glob(pattern)
    else:
        all_items = folder_path.iterdir()
    
    for item in all_items:
        if item.is_file():
            if extensions:
                if item.suffix.lower() in [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]:
                    files.append(item)
            else:
                files.append(item)
    
    return sorted(files)


def generate_new_name(filename, pattern_type, pattern_value, index=None, total=None):
    """Generate new filename based on pattern type"""
    stem = Path(filename).stem
    ext = Path(filename).suffix
    
    if pattern_type == 'sequential':
        # Sequential numbering: file_1.txt, file_2.txt
        padding = len(str(total)) if total else 3
        new_stem = pattern_value.format(i=str(index).zfill(padding), name=stem)
        
    elif pattern_type == 'prefix':
        # Add prefix: prefix_originalname.txt
        new_stem = f"{pattern_value}{stem}"
        
    elif pattern_type == 'suffix':
        # Add suffix: originalname_suffix.txt
        new_stem = f"{stem}{pattern_value}"
        
    elif pattern_type == 'replace':
        # Replace text: old -> new
        old, new = pattern_value.split(':', 1)
        new_stem = stem.replace(old, new)
        
    elif pattern_type == 'regex':
        # Regex replacement: pattern:replacement
        pattern, replacement = pattern_value.split(':', 1)
        new_stem = re.sub(pattern, replacement, stem)
        
    elif pattern_type == 'lowercase':
        new_stem = stem.lower()
        
    elif pattern_type == 'uppercase':
        new_stem = stem.upper()
        
    elif pattern_type == 'title':
        new_stem = stem.title()
        
    else:
        raise ValueError(f"Unknown pattern type: {pattern_type}")
    
    return f"{new_stem}{ext}"


def preview_rename(files, pattern_type, pattern_value):
    """Show preview of what files will be renamed to"""
    changes = []
    total = len(files)
    
    for idx, filepath in enumerate(files, start=1):
        old_name = filepath.name
        new_name = generate_new_name(old_name, pattern_type, pattern_value, idx, total)
        
        if old_name != new_name:
            changes.append({
                'old': old_name,
                'new': new_name,
                'path': filepath.parent,
                'full_old': str(filepath),
                'full_new': str(filepath.parent / new_name)
            })
    
    return changes


def execute_rename(changes, log_file=None):
    """Execute the rename operations"""
    success_count = 0
    error_count = 0
    log_data = []
    
    for change in changes:
        old_path = Path(change['full_old'])
        new_path = Path(change['full_new'])
        
        # Check if target already exists
        if new_path.exists():
            print(f"⚠️  Skipping {change['old']}: {change['new']} already exists")
            error_count += 1
            log_data.append({
                'status': 'skipped',
                'old': change['full_old'],
                'new': change['full_new'],
                'reason': 'target exists'
            })
            continue
        
        try:
            old_path.rename(new_path)
            print(f"✓ Renamed: {change['old']} → {change['new']}")
            success_count += 1
            log_data.append({
                'status': 'success',
                'old': change['full_old'],
                'new': change['full_new'],
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"✗ Error renaming {change['old']}: {e}")
            error_count += 1
            log_data.append({
                'status': 'error',
                'old': change['full_old'],
                'new': change['full_new'],
                'error': str(e)
            })
    
    # Save log if requested
    if log_file:
        log_path = Path(log_file)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total': len(changes),
                'success': success_count,
                'errors': error_count,
                'operations': log_data
            }, f, indent=2)
        print(f"\n📄 Log saved to: {log_path}")
    
    return success_count, error_count


def undo_rename(log_file):
    """Undo renames from a log file"""
    log_path = Path(log_file)
    
    if not log_path.exists():
        print(f"Error: Log file not found: {log_file}")
        return
    
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    print(f"Undoing {log_data['success']} operations from {log_data['timestamp']}...")
    
    success_count = 0
    error_count = 0
    
    for op in log_data['operations']:
        if op['status'] != 'success':
            continue
        
        # Reverse: new -> old
        current_path = Path(op['new'])
        original_path = Path(op['old'])
        
        if not current_path.exists():
            print(f"⚠️  Skipping: {current_path.name} no longer exists")
            error_count += 1
            continue
        
        try:
            current_path.rename(original_path)
            print(f"✓ Restored: {current_path.name} → {original_path.name}")
            success_count += 1
        except Exception as e:
            print(f"✗ Error restoring {current_path.name}: {e}")
            error_count += 1
    
    print(f"\nUndo complete: {success_count} restored, {error_count} errors")


def main():
    parser = argparse.ArgumentParser(
        description='Bulk file renamer with preview and multiple pattern options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Pattern Types and Examples:
  sequential    - Rename with numbers: --pattern sequential --value "file_{i}"
                  Creates: file_001.txt, file_002.txt, etc.
  
  prefix        - Add prefix: --pattern prefix --value "backup_"
                  Creates: backup_document.txt
  
  suffix        - Add suffix: --pattern suffix --value "_v2"
                  Creates: document_v2.txt
  
  replace       - Replace text: --pattern replace --value "old:new"
                  Replaces all "old" with "new"
  
  regex         - Regex replace: --pattern regex --value "\\d+:NUM"
                  Replaces numbers with "NUM"
  
  lowercase     - Convert to lowercase: --pattern lowercase
  uppercase     - Convert to UPPERCASE: --pattern uppercase
  title         - Convert To Title Case: --pattern title

Examples:
  %(prog)s /path/to/folder --pattern sequential --value "photo_{i}" --preview
  %(prog)s /path/to/folder --pattern prefix --value "2024_" --ext jpg png
  %(prog)s /path/to/folder --pattern replace --value "IMG:Photo" --execute
  %(prog)s --undo rename_log_20241127.json
        '''
    )
    
    parser.add_argument('folder', nargs='?', help='Folder containing files to rename')
    parser.add_argument('--pattern', '-p', 
                       choices=['sequential', 'prefix', 'suffix', 'replace', 'regex', 'lowercase', 'uppercase', 'title'],
                       help='Rename pattern type')
    parser.add_argument('--value', '-v', help='Pattern value (format depends on pattern type)')
    parser.add_argument('--ext', '-e', nargs='+', help='Filter by file extensions (e.g., jpg png txt)')
    parser.add_argument('--recursive', '-r', action='store_true', help='Include files in subdirectories')
    parser.add_argument('--preview', action='store_true', help='Preview changes without executing (default)')
    parser.add_argument('--execute', action='store_true', help='Execute the rename operations')
    parser.add_argument('--log', help='Save operation log to file (for undo capability)')
    parser.add_argument('--undo', help='Undo operations from a log file')
    
    args = parser.parse_args()
    
    # Undo mode
    if args.undo:
        undo_rename(args.undo)
        return
    
    # Validate arguments for rename mode
    if not args.folder:
        parser.error("Folder path is required (or use --undo to undo previous operation)")
    
    if not args.pattern:
        parser.error("--pattern is required")
    
    if args.pattern in ['sequential', 'prefix', 'suffix', 'replace', 'regex'] and not args.value:
        parser.error(f"--value is required for pattern type '{args.pattern}'")
    
    try:
        # Get files
        files = get_files_in_folder(args.folder, args.ext, args.recursive)
        
        if not files:
            print(f"No files found in {args.folder}")
            if args.ext:
                print(f"Filters: extensions={args.ext}")
            return
        
        print(f"Found {len(files)} file(s)")
        if args.ext:
            print(f"Filtered by extensions: {', '.join(args.ext)}")
        print()
        
        # Generate preview
        changes = preview_rename(files, args.pattern, args.value or '')
        
        if not changes:
            print("No files need to be renamed (all names already match pattern)")
            return
        
        # Show preview
        print(f"Preview of {len(changes)} change(s):")
        print("=" * 80)
        for i, change in enumerate(changes[:20], 1):  # Show first 20
            print(f"{i:3}. {change['old']:40} → {change['new']}")
        
        if len(changes) > 20:
            print(f"... and {len(changes) - 20} more")
        print("=" * 80)
        
        # Execute if requested
        if args.execute:
            print()
            confirm = input(f"Execute {len(changes)} rename operations? (yes/no): ").strip().lower()
            if confirm in ('yes', 'y'):
                success, errors = execute_rename(changes, args.log)
                print(f"\n✓ Rename complete: {success} successful, {errors} errors")
                if args.log:
                    print(f"💡 To undo, run: {sys.argv[0]} --undo {args.log}")
            else:
                print("Operation cancelled")
        else:
            print("\n💡 This is a preview. Use --execute to actually rename files")
            print(f"💡 Recommended: use --log to enable undo capability")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

