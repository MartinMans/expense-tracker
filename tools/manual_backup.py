import shutil
import os
from pathlib import Path
from datetime import datetime

# Dynamically find project root
project_root = Path(__file__).resolve().parents[1]
filepath = project_root / 'data' / 'Expense_Tracker.xlsx'
backup_dir = project_root / 'data'

def create_manual_backup():
    """Create a single backup file with today's date, overwriting old backup if it exists."""
    if not filepath.exists():
        print("⚠️ No expense tracker file found to backup.")
        return

    # Delete any existing backup
    for file in os.listdir(backup_dir):
        if file.startswith('Expense_Tracker_backup_') and file.endswith('.xlsx'):
            os.remove(backup_dir / file)
            print(f"🗑️ Deleted old backup: {file}")

    # Create new backup
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
    backup_filename = f'Expense_Tracker_backup_{today_str}.xlsx'
    backup_path = backup_dir / backup_filename

    shutil.copy(filepath, backup_path)
    print(f"✅ Manual backup created: {backup_filename}")
    print(f"🕒 Backup creation time: {timestamp_str}")

if __name__ == "__main__":
    create_manual_backup()