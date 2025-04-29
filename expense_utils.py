import pandas as pd
import os

# Path to your Excel file
filepath = './data/Expense_Tracker.xlsx'

# Fixed list of categories
categories = [
    'Restaurant', 'Toters', 'Entertainment', 'Groceries', 'Snacks', 
    'Barber', 'Laundry', 'Transportation', 'Shopping', 'Phone'
]

def validate_date(date_str):
    """Validate input in DD/MM/YYYY format, return a string in YY/MM/DD format."""
    try:
        date = pd.to_datetime(date_str, format='%d/%m/%Y')
        return date.strftime('%Y/%m/%d')
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return None

def get_expense_details():
    """Prompt user for expense details and return as a dictionary."""
    date_input = input("Enter the date (DD/MM/YYYY) or type 'exit' to quit: ").strip()
    if date_input.lower() == 'exit':
        return 'exit'
    
    date = validate_date(date_input)
    if date is None:
        return None

    print("\nSelect a category:")
    for i, category in enumerate(categories):
        print(f"{i + 1}. {category}")
    category_index = int(input("Enter the number corresponding to the category: ")) - 1
    category = categories[category_index]

    amount = float(input("Enter the amount spent (USD): "))
    notes = input("Any notes? (optional): ")

    return {
        'Date': date,
        'Category': category,
        'Amount': amount,
        'Notes': notes
    }

def save_expense_entry(df, entry):
    """Append a new expense entry and save the Excel file."""
    new_row = pd.DataFrame([entry])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(filepath, index=False)
    return df