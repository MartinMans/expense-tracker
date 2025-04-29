from app.expense_utils import get_expense_details, save_expense_entry
from visuals.visualize import main as visualize_menu
from tools.manual_backup import create_manual_backup
from tools.delete_data import delete_main_expense_tracker
import pandas as pd
from pathlib import Path

def load_data():
    project_root = Path(__file__).resolve().parent
    filepath = project_root / 'data' / 'Expense_Tracker.xlsx'
    
    try:
        df = pd.read_excel(filepath)
    except FileNotFoundError:
        print("⚠️ No expense tracker file found. Creating a new one...")
        df = pd.DataFrame({
            'Date': pd.Series(dtype='str'),
            'Category': pd.Series(dtype='str'),
            'Amount': pd.Series(dtype='float'),
            'Notes': pd.Series(dtype='str')
        })
        df.to_excel(filepath, index=False)
        print(f"✅ New expense tracker created at {filepath}")
    
    return df, filepath

def insert_new_expense():
    """Handles inserting a new expense into the dataset."""
    df, filepath = load_data()
    new_expense = get_expense_details()
    save_expense_entry(df, new_expense, filepath)

def main():
    while True:
        print("\n📋 Welcome to Expense Tracker")
        print("1. Add a New Expense")
        print("2. View Visualizations")
        print("3. Create a Manual Backup")
        print("4. Delete Main Data")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            insert_new_expense()
        elif choice == '2':
            visualize_menu()
        elif choice == '3':
            create_manual_backup()
        elif choice == '4':
            delete_main_expense_tracker()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()