# Expense Tracker

A lightweight Python script to log personal expenses directly into an Excel file.  
Designed for fast, command-line usage with simple manual tools for backup and data management.

Built with clean project organization, absolute path handling, and OS-independent structure.

---

## 📦 Project Structure

expense-tracker/
├── expense_tracker.py         # Main expense logging script
├── expense_utils.py            # Helper functions (input validation, saving)
├── tools/                      # Utility scripts
│   ├── manual_backup.py        # Manually create a backup of current data (absolute path handling)
│   ├── delete_data.py          # Delete the main expense tracker (confirmation required, absolute path handling)
├── data/                       # Contains active data and backups
│   ├── Expense_Tracker.xlsx
│   ├── Expense_Tracker_backup_YYYY-MM-DD.xlsx
├── requirements.txt
├── README.md
├── .gitignore

---

## 🚀 How to Use

### 1. Log Expenses
```bash
python expense_tracker.py
```
- Input date, category, amount, notes.
- Continue adding expenses or exit.

### 2. Create a Backup (Manually)
```bash
python tools/manual_backup.py
```
- Creates a backup of the current `Expense_Tracker.xlsx`.
- Deletes previous backup for the day if it exists.
- Displays the time when backup was created.

### 3. Delete Main Data (Careful!)
```bash
python tools/delete_data.py
```
- Prompts for confirmation before deleting `Expense_Tracker.xlsx`.
- Backup files are NOT affected.

---

## 🛠 Requirements

- Python 3.8+
- pandas
- openpyxl

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Design Highlights

- ✅ Absolute path handling using `pathlib` (robust to different working directories)
- ✅ OS-independent file structure (works on Windows, macOS, Linux)
- ✅ Lightweight and fast
- ✅ Designed for future expansion (visualization, summaries)

---

## 🧠 Future Plans

- Add spending visualizations.
- Monthly spending summaries.
- Optional category customization.