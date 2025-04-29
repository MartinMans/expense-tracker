import os
from pathlib import Path

# Automatically find the root directory
project_root = Path(__file__).resolve().parents[1]
filepath = project_root / 'data' / 'Expense_Tracker.xlsx'

def delete_expense_tracker():
    """Delete the main expense tracker Excel file after user confirmation."""
    print(f"Checking for file at: {filepath}")
    print(f"File exists? {filepath.exists()}")

    if not filepath.exists():
        print("⚠️ No expense tracker file found to delete.")
        return

    confirmation = input("⚠️ Are you sure you want to delete the main Expense Tracker file? (Y/N): ").strip().upper()
    if confirmation == 'Y':
        os.remove(filepath)
        print(f"🗑️ Deleted main expense tracker file: {filepath}")
    else:
        print("❌ Deletion canceled. File is safe.")

if __name__ == "__main__":
    delete_expense_tracker()