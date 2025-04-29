import os
from pathlib import Path

def delete_main_expense_tracker():
    """Delete the main expense tracker Excel file after user confirmation."""
    project_root = Path(__file__).resolve().parents[1]
    filepath = project_root / 'data' / 'Expense_Tracker.xlsx'

    if not filepath.exists():
        print("⚠️ No expense tracker file found to delete.")
        return

    os.remove(filepath)
    print(f"✅ Deleted the main expense tracker file: {filepath}")

if __name__ == "__main__":
    delete_main_expense_tracker()