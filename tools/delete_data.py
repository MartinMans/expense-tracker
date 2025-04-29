import os
from pathlib import Path
import sys

def get_base_path():
    """Returns correct base path whether running from script or PyInstaller .exe"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]

def delete_main_expense_tracker():
    """Delete the main expense tracker Excel file after user confirmation."""
    base_path = get_base_path()
    filepath = base_path / 'data' / 'Expense_Tracker.xlsx'

    if not filepath.exists():
        print("⚠️ No expense tracker file found to delete.")
        return

    os.remove(filepath)
    print(f"✅ Deleted the main expense tracker file: {filepath}")

if __name__ == "__main__":
    delete_main_expense_tracker()