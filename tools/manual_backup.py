import shutil
from pathlib import Path
from datetime import datetime

def create_manual_backup():
    """Create a manual backup of the expense tracker file."""
    project_root = Path(__file__).resolve().parents[1]
    filepath = project_root / 'data' / 'Expense_Tracker.xlsx'
    backup_dir = project_root / 'data'

    if not filepath.exists():
        print("⚠️ No expense tracker file found to backup.")
        return

    # Delete existing backup for today
    for file in backup_dir.glob('Expense_Tracker_backup_*.xlsx'):
        file.unlink()

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