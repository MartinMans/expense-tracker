import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.expense_utils import load_data, save_expense_entry
from visuals.plot_utils import plot_monthly_spending, plot_spending_per_category, plot_cumulative_spending
from tools.manual_backup import create_manual_backup
from tools.delete_data import delete_main_expense_tracker

def launch_gui():
    root = tk.Tk()
    root.title("Expense Tracker")

    # Set desired size
    window_width = 810
    window_height = 350

    # Center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2) - 75  # adjust for eye level

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


    # Allow the root window to expand cleanly
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # ====== CONTAINER FRAME ======
    container = tk.Frame(root)
    container.pack(expand=True, fill="both")
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)

    # ====== LEFT PANEL: Visualize Data ======
    visualize_panel = tk.Frame(container, padx=10, pady=10, bd=1, relief="groove")
    visualize_panel.grid(row=0, column=0, padx=20, sticky="nsew")

    tk.Label(visualize_panel, text="\ud83d\udcca Visualize Data", font=("Arial", 14)).pack(pady=10)

    def show_monthly_spending():
        try:
            year = simpledialog.askinteger("Year", "Enter Year (e.g., 2025):", parent=root)
            if year is None:
                return
            month = simpledialog.askinteger("Month", "Enter Month (1-12):", parent=root)
            if month is None:
                return

            def run_plot():
                df, _ = load_data()
                plot_monthly_spending(df, month, year)

            root.after(50, run_plot)

        except Exception as e:
            messagebox.showerror("Error", f"\u274c Failed to plot monthly spending.\n\n{str(e)}", parent=root)

    def show_spending_by_category():
        try:
            df, _ = load_data()
            plot_spending_per_category(df)
        except Exception as e:
            messagebox.showerror("Error", f"\u274c Failed to plot spending by category.\n\n{str(e)}", parent=root)

    def show_cumulative_spending():
        try:
            df, _ = load_data()
            plot_cumulative_spending(df)
        except Exception as e:
            messagebox.showerror("Error", f"\u274c Failed to plot cumulative spending.\n\n{str(e)}", parent=root)

    tk.Button(visualize_panel, text="Monthly Spending", command=show_monthly_spending).pack(pady=5, fill="x")
    tk.Button(visualize_panel, text="Spending by Category", command=show_spending_by_category).pack(pady=5, fill="x")
    tk.Button(visualize_panel, text="Cumulative Spending", command=show_cumulative_spending).pack(pady=5, fill="x")

    # ====== CENTER PANEL: Insert New Entry ======
    insert_panel = tk.Frame(container, width=100, padx=10, pady=10, bd=1, relief="groove")
    insert_panel.grid(row=0, column=1, padx=20, sticky="nsew")
    insert_panel.grid_propagate(False)

    tk.Label(insert_panel, text="\ud83d\udcdf Insert New Entry", font=("Arial", 14)).pack(pady=10)

    tk.Label(insert_panel, text="Date (DD/MM/YYYY):").pack(anchor="w")
    date_entry = tk.Entry(insert_panel)
    date_entry.pack(pady=2, fill="x")

    tk.Label(insert_panel, text="Category:").pack(anchor="w")
    category_combo = ttk.Combobox(insert_panel, values=[
        "Restaurant", "Toters", "Entertainment", "Groceries", "Snacks",
        "Barber", "Laundry", "Transportation", "Shopping", "Phone"
    ])
    category_combo.pack(pady=2, fill="x")
    category_combo.set("Restaurant")

    tk.Label(insert_panel, text="Amount (USD):").pack(anchor="w")
    amount_entry = tk.Entry(insert_panel)
    amount_entry.pack(pady=2, fill="x")

    tk.Label(insert_panel, text="Notes (optional):").pack(anchor="w")
    notes_entry = tk.Text(insert_panel, height=3, width=40)
    notes_entry.pack(pady=2)

    def submit_expense():
        date_str = date_entry.get().strip()
        category = category_combo.get().strip()
        amount_str = amount_entry.get().strip()
        notes = notes_entry.get("1.0", tk.END).strip()

        try:
            pd.to_datetime(date_str, format='%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Invalid Input", "\u274c Date format must be DD/MM/YYYY.", parent=root)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "\u274c Amount must be a number.", parent=root)
            return

        df, filepath = load_data()
        entry = {
            "Date": pd.to_datetime(date_str, format='%d/%m/%Y').strftime('%Y/%m/%d'),
            "Category": category,
            "Amount": amount,
            "Notes": notes
        }

        save_expense_entry(df, entry, filepath)
        messagebox.showinfo("Success", "\u2705 Expense entry saved!", parent=root)

        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        notes_entry.delete("1.0", tk.END)
        category_combo.set("Restaurant")

    tk.Button(insert_panel, text="Submit", command=submit_expense).pack(pady=10)

    # ====== RIGHT PANEL: Additional Tools ======
    tools_panel = tk.Frame(container, padx=10, pady=10, bd=1, relief="groove")
    tools_panel.grid(row=0, column=2, padx=20, sticky="nsew")

    tk.Label(tools_panel, text="\ud83d\udd27 Additional Tools", font=("Arial", 14)).pack(pady=10)

    def handle_backup():
        try:
            create_manual_backup()
            messagebox.showinfo("Backup Created", "\u2705 Backup file created successfully!", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"\u274c Failed to create backup.\n\n{str(e)}", parent=root)

    def handle_delete():
        confirm = messagebox.askyesno("\u26a0\ufe0f Confirm Deletion", "Are you sure you want to delete the main Excel file?", parent=root)
        if confirm:
            try:
                delete_main_expense_tracker()
                messagebox.showinfo("Deleted", "\ud83d\uddd1\ufe0f Main Excel file deleted.", parent=root)
            except Exception as e:
                messagebox.showerror("Error", f"\u274c Failed to delete file.\n\n{str(e)}", parent=root)

    def handle_exit():
        root.quit()

    tk.Button(tools_panel, text="Create Backup", command=handle_backup).pack(pady=5, fill="x")
    tk.Button(tools_panel, text="Delete Data", command=handle_delete).pack(pady=5, fill="x")
    tk.Button(tools_panel, text="Exit", command=handle_exit).pack(pady=5, fill="x")

    root.mainloop()

if __name__ == "__main__":
    launch_gui()