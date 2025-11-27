from datetime import date
import argparse
import sys

def calculate_age(birthday: date, reference_date: date = None) -> dict:
    """Calculate age from birthday to reference date (default: today)"""
    if reference_date is None:
        reference_date = date.today()

    # Check if the birthdate is in the future
    if birthday > reference_date:
        return None

    # Calculate age
    years = reference_date.year - birthday.year
    months = reference_date.month - birthday.month
    days = reference_date.day - birthday.day

    # Adjust for negative day difference
    if days < 0:
        months -= 1
        # Get the number of days in the previous month
        if reference_date.month == 1:
            prev_month = 12
            prev_year = reference_date.year - 1
        else:
            prev_month = reference_date.month - 1
            prev_year = reference_date.year
        
        # Calculate days in previous month
        if prev_month == 12:
            next_month_year = prev_year + 1
            next_month = 1
        else:
            next_month_year = prev_year
            next_month = prev_month + 1
        
        from calendar import monthrange
        days_in_prev_month = monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month

    # Adjust for negative month difference
    if months < 0:
        years -= 1
        months += 12

    # Calculate total days
    total_days = (reference_date - birthday).days

    return {
        'years': years,
        'months': months,
        'days': days,
        'total_days': total_days
    }


def format_age(age_data: dict, format_type: str = 'full') -> str:
    """Format age data in different ways"""
    if age_data is None:
        return "Invalid birthdate. Please enter a valid date in the past."
    
    if format_type == 'full':
        return f"Age: {age_data['years']} years, {age_data['months']} months, and {age_data['days']} days"
    elif format_type == 'years':
        return f"Age: {age_data['years']} years"
    elif format_type == 'total_days':
        return f"Age: {age_data['total_days']} days"
    elif format_type == 'all':
        return (f"Age: {age_data['years']} years, {age_data['months']} months, and {age_data['days']} days\n"
                f"Total days: {age_data['total_days']}")
    else:
        return f"Age: {age_data['years']} years, {age_data['months']} months, and {age_data['days']} days"


def parse_date_string(date_str: str) -> date:
    """Parse date string in various formats"""
    from datetime import datetime
    
    formats = [
        '%Y-%m-%d',      # 2000-01-15
        '%d/%m/%Y',      # 15/01/2000
        '%m/%d/%Y',      # 01/15/2000
        '%d-%m-%Y',      # 15-01-2000
        '%Y/%m/%d',      # 2000/01/15
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse date: {date_str}. Supported formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, DD-MM-YYYY, YYYY/MM/DD")


def main():
    parser = argparse.ArgumentParser(
        description='Calculate age from birthdate',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                           # Interactive mode
  %(prog)s 2000-01-15                # Calculate age from date
  %(prog)s 2000-01-15 --format years # Show only years
  %(prog)s 2000-01-15 --at 2025-01-01  # Age at specific date
        '''
    )
    
    parser.add_argument('birthdate', nargs='?', help='Birthdate (YYYY-MM-DD, DD/MM/YYYY, etc.)')
    parser.add_argument('--at', '--reference', dest='reference_date', 
                       help='Calculate age at this date instead of today (YYYY-MM-DD)')
    parser.add_argument('--format', '-f', choices=['full', 'years', 'total_days', 'all'],
                       default='full', help='Output format (default: full)')
    
    args = parser.parse_args()

    try:
        # Interactive mode
        if not args.birthdate:
            print("Age Calculator (Python)")
            print("=" * 40)
            
            birth_year = int(input("Enter birth year: "))
            birth_month = int(input("Enter birth month (1-12): "))
            birth_day = int(input("Enter birth day: "))
            birthday = date(birth_year, birth_month, birth_day)
            
            reference_date = None
            if input("Calculate age at specific date? (y/n): ").lower() == 'y':
                ref_year = int(input("Enter reference year: "))
                ref_month = int(input("Enter reference month (1-12): "))
                ref_day = int(input("Enter reference day: "))
                reference_date = date(ref_year, ref_month, ref_day)
            
            age_data = calculate_age(birthday, reference_date)
            print("\n" + format_age(age_data, 'all'))
        
        # CLI mode
        else:
            birthday = parse_date_string(args.birthdate)
            
            reference_date = None
            if args.reference_date:
                reference_date = parse_date_string(args.reference_date)
            
            age_data = calculate_age(birthday, reference_date)
            print(format_age(age_data, args.format))
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

