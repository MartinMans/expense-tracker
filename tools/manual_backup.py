import shutil
from pathlib import Path
from datetime import datetime
import sys

def get_base_path():
    """Returns correct base path whether running from script or PyInstaller .exe"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]

def create_manual_backup():
    """Create a manual backup of the expense tracker file."""
    base_path = get_base_path()
    data_dir = base_path / 'data'
    filepath = data_dir / 'Expense_Tracker.xlsx'

    if not filepath.exists():
        print("⚠️ No expense tracker file found to backup.")
        return

    # Delete existing backup for today
    for file in data_dir.glob('Expense_Tracker_backup_*.xlsx'):
        file.unlink()

    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
    backup_filename = f'Expense_Tracker_backup_{today_str}.xlsx'
    backup_path = data_dir / backup_filename

    shutil.copy(filepath, backup_path)
    print(f"✅ Manual backup created: {backup_filename}")
    print(f"🕒 Backup creation time: {timestamp_str}")

if __name__ == "__main__":
    create_manual_backup()