import pandas as pd
from app.expense_utils import load_data, get_expense_details, save_expense_entry

def main():
    print("Welcome to the Expense Tracker! 📋")

    while True:
        expense_entry = get_expense_details()
        if expense_entry == 'exit':
            print("\nExiting without adding an expense. 👋")
            break
        if expense_entry is None:
            print("Invalid date. Please try again.\n")
            continue

        global df
        df = save_expense_entry(df, expense_entry, filepath)

        done = input("\nAre you done? (Y/N): ").strip().upper()
        if done == 'Y':
            break
        elif done != 'N':
            print("Invalid input. Please enter 'Y' or 'N'.")

    print("\nThanks for using Expense Tracker! 👋")

if __name__ == "__main__":
    df, filepath = load_data()
    main()