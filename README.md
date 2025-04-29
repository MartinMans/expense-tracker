# Expense Tracker 🧾

A lightweight, personal expense tracking app with both a command-line and GUI interface. Easily log your daily expenses, view visualizations, and manage your data locally via Excel.

---

## 💡 Features

- Insert new expenses by date, category, amount, and optional notes
- Autocomplete Notes field using dropdown suggestions from past entries
- View full dataset inside the app via a "View Data" button
- Visualize:
  - Monthly spending (line graph)
  - Spending per category (bar chart)
  - Cumulative all-time spending (line+fill)
- Create backup files manually
- Delete all data via confirmation prompt
- Automatically creates the `data/` folder and Excel file if missing
- Persistent local data stored in `data/Expense_Tracker.xlsx`
- Runs via Python or executable `.bat` file
- GUI built with Tkinter — centered, responsive layout

---

## 📁 Project Structure

```
expense-tracker/
├── app/                # Core logic (data handling, saving, validation)
│   ├── expense_tracker.py
│   ├── expense_utils.py
│   └── __init__.py
├── visuals/            # Visualization logic
│   ├── plot_utils.py
│   ├── visualize.py
│   └── __init__.py
├── tools/              # Developer tools (backup, delete, dummy data)
│   ├── manual_backup.py
│   ├── delete_data.py
│   ├── generate_dummy_data.py
│   └── __init__.py
├── data/               # Stores `Expense_Tracker.xlsx` and backup
│   └── (auto-created on first run)
├── gui.py              # GUI launcher (Tkinter-based)
├── main.py             # CLI menu system
├── run_tracker.bat     # One-click launcher (for Windows)
├── README.md
├── .gitignore
└── requirements.txt
```

---

## 🚀 How to Run

### 🔹 GUI App

```bash
python gui.py
```
Or double-click `run_tracker.bat` to launch with no terminal.

### 🔹 CLI Mode

```bash
python main.py
```

---

## 🛠 Requirements

```bash
pip install -r requirements.txt
```

- pandas
- openpyxl
- tkinter (built into Python standard library)

---

## 📦 Future Plans

- Package `.exe` with PyInstaller (no console pop-up)
- Optional data import/export
- Add column sorting and filtering to the data viewer

---

## 👤 Author

Developed by [Martin Mansour](https://github.com/MartinMans).
