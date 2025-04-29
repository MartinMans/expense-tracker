# Expense Tracker 🧾

A lightweight personal expense tracking app with both a command-line and GUI interface. Easily log expenses, view visualizations, and manage local data via Excel.

Now available as a standalone `.exe` — no Python installation required!

---

## 💡 Features

- Add expenses with date, category, amount, and optional notes
- Autocomplete suggestions for notes based on past entries
- View full dataset inside the app
- Visualize:
  - Monthly spending (line graph)
  - Spending per category (bar chart)
  - Cumulative all-time spending (line + fill)
- Create backup files manually
- Delete all data via confirmation prompt
- Auto-creates `data/` folder and Excel file if missing
- Local data stored in `data/Expense_Tracker.xlsx`
- GUI built with Tkinter (centered, responsive layout)
- Available as a Python script **or** standalone `.exe`

---

## 📁 Folder Structure

```
expense-tracker/
├── app/
│   ├── expense_tracker.py
│   ├── expense_utils.py
│   └── __init__.py
├── visuals/
│   ├── plot_utils.py
│   ├── visualize.py
│   └── __init__.py
├── tools/
│   ├── manual_backup.py
│   ├── delete_data.py
│   ├── generate_dummy_data.py
│   └── __init__.py
├── data/
│   └── Expense_Tracker.xlsx (auto-generated)
├── gui.exe              # ✅ Standalone executable
├── gui.py               # GUI launcher (Python version)
├── main.py              # CLI menu system
├── run_tracker.bat      # Optional .bat launcher
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How to Use

### 🟢 Standalone .exe

Just double-click `gui.exe` — no need to install Python!

> ℹ️ If `Expense_Tracker.xlsx` is missing, it will be created automatically in `data/`

---

### 🧪 Python CLI Mode

```bash
python main.py
```

---

### 🧪 Python GUI Mode (Dev)

```bash
python gui.py
```

---

## 📦 Requirements (for devs)

```bash
pip install -r requirements.txt
```

- pandas
- matplotlib
- openpyxl
- pillow
- tkinter (bundled with Python)

---

## 👤 Author

Developed by [Martin Mansour](https://github.com/MartinMans)