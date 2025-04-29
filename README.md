# Expense Tracker CLI Application

A lightweight personal expense tracking tool built in Python.

This project started as a basic CLI expense tracker and has now evolved into a modular, fully functioning application. It allows you to track expenses, generate visualizations, back up data, and manage your expense dataset seamlessly.

---

## 📅 Features

- **Add New Expenses** through a simple CLI flow
- **Visualize Your Spending**:
  - Monthly spending trends
  - Spending per category
  - Cumulative all-time spending
- **Create Manual Backups** of your expense data
- **Delete** your main dataset when needed (with confirmation)
- **Auto-sorted by date** after every new entry
- **Dummy data generator** for testing

---

## 📂 Project Structure

```
expense-tracker/
├── app/                # Core logic (adding expenses, saving, utils)
│   ├── __init__.py
│   ├── expense_tracker.py
│   ├── expense_utils.py
├── visuals/            # Visualizations (plots and visualization menu)
│   ├── __init__.py
│   ├── visualize.py
│   ├── plot_utils.py
├── tools/              # Maintenance tools (backup, delete, dummy data)
│   ├── __init__.py
│   ├── manual_backup.py
│   ├── delete_data.py
│   ├── generate_dummy_data.py
├── data/               # Stored Excel files
│   ├── Expense_Tracker.xlsx
├── main.py             # ✨ Unified CLI Application Entry Point
├── run_tracker.bat     # Quick launcher script
├── README.md
├── requirements.txt
├── .gitignore
```

---

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

2. (Optional) Create and activate a virtual environment.

3. Install required libraries:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

Run the main CLI app:

```bash
python main.py
```

Or double-click `run_tracker.bat` if you prefer a one-click launch.

Follow the on-screen menu to:
- Add new expenses
- View visualizations
- Create backups
- Delete your main dataset
- Exit

---

## 📊 Future Development

- Phase 4: Migrate the CLI app into a full GUI (Tkinter)
- Add richer statistics and filters (e.g., monthly reports)
- Build in export options (CSV, PDF reports)

---

## 🌟 Notes

- Dummy data is currently provided for demonstration and testing.
- Expense Tracker automatically sorts entries by date after every new addition.
- Real expense tracking usage is intended to begin after GUI development.

---

💼 Built with care for practical everyday use.
