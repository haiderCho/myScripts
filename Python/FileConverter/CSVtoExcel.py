
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import openpyxl
import sys
from openpyxl import Workbook

def main():
    print("This program writes data from a CSV (or similarly formatted file) into an Excel file.")
    print("Input and output files must be in the same directory as this script.\n")

    csv_name = input("Name of the CSV file for input (with extension): ").strip()
    sep = input("Separator used in the CSV file: ").strip()
    excel_name = input("Name of the Excel file for output (with extension): ").strip()
    sheet_name = input("Name of the Excel sheet for output: ").strip()

    # -----------------------------
    # Load or create workbook
    # -----------------------------
    try:
        try:
            wb = openpyxl.load_workbook(excel_name)
            print(f"Loaded existing Excel file: {excel_name}")
        except FileNotFoundError:
            wb = Workbook()
            print(f"Created new Excel file: {excel_name}")

        # Create or select sheet
        if sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
        else:
            sheet = wb.create_sheet(title=sheet_name)
    except Exception as e:
        print(f"Excel file error: {e}")
        sys.exit(1)

    # -----------------------------
    # Read CSV and write to Excel
    # -----------------------------
    try:
        with open(csv_name, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=sep)

            for row_index, row_data in enumerate(reader, start=1):
                for col_index, value in enumerate(row_data, start=1):
                    sheet.cell(row=row_index, column=col_index, value=value)

        wb.save(excel_name)
        print(f"Data successfully written to {excel_name} in sheet '{sheet_name}'.")
    except Exception as e:
        print(f"CSV read/write error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
