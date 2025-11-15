from datetime import date

def calculate_age(birthday: date) -> str:
    today = date.today()

    # Check if the birthdate is in the future
    if birthday > today:
        return "Invalid birthdate. Please enter a valid date."

    # Calculate age
    years = today.year - birthday.year
    months = today.month - birthday.month
    days = today.day - birthday.day

    # Adjust for negative month/day differences
    if days < 0:
        months -= 1
        # Get days in the previous month
        prev_month = (today.month - 1) or 12
        prev_year = today.year - (1 if today.month == 1 else 0)
        days += (date(prev_year, prev_month + 1, 1) - date(prev_year, prev_month, 1)).days

    if months < 0:
        years -= 1
        months += 12

    return f"Age: {years} years, {months} months, and {days} days"


if __name__ == "__main__":
    print("Age Calculator (Python)")

    try:
        birth_year = int(input("Enter birth year: "))
        birth_month = int(input("Enter birth month: "))
        birth_day = int(input("Enter birth day: "))
        date_of_birth = date(birth_year, birth_month, birth_day)
        print(calculate_age(date_of_birth))
    except ValueError:
        print("Invalid input. Please enter valid integers for year, month, and day.")

