import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from app.expense_utils import load_data, save_expense_entry
from visuals.plot_utils import plot_monthly_spending, plot_spending_per_category, plot_cumulative_spending
from tools.manual_backup import create_manual_backup
from tools.delete_data import delete_main_expense_tracker

class AutocompleteDropdown:
    def __init__(self, entry, suggestions):
        self.entry = entry
        self.suggestions = suggestions
        self.listbox = None
        self.entry.bind("<KeyRelease>", self.on_keyrelease)

    def on_keyrelease(self, event):
        if event.keysym in ["Up", "Down", "Return", "Escape"]:
            if self.listbox:
                self.navigate_listbox(event)
            return

        typed = self.entry.get()
        if typed == "":
            self.hide_dropdown()
            return

        matches = [s for s in self.suggestions if s.lower().startswith(typed.lower())]
        if matches:
            self.show_dropdown(matches)
        else:
            self.hide_dropdown()

    def show_dropdown(self, suggestions):
        self.hide_dropdown()  # Always clear previous one

        self.listbox = tk.Listbox(self.entry.master, height=min(5, len(suggestions)), bg="white", relief="solid", borderwidth=1)
        for item in suggestions:
            self.listbox.insert(tk.END, item)

        x_offset = self.entry.winfo_rootx() - self.entry.master.winfo_rootx() - 12
        y_offset = self.entry.winfo_y() + self.entry.winfo_height() - 8
        self.listbox.place(x=x_offset, y=y_offset)

        self.listbox.bind("<ButtonRelease-1>", self.select_suggestion)

    def hide_dropdown(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

    def select_suggestion(self, event):
        if self.listbox:
            index = self.listbox.curselection()
            if index:
                value = self.listbox.get(index)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, value)
            self.hide_dropdown()

    def navigate_listbox(self, event):
        if not self.listbox:
            return

        if event.keysym == "Down":
            if self.listbox.curselection() == ():
                self.listbox.selection_set(0)
            else:
                current = self.listbox.curselection()[0]
                if current < self.listbox.size() - 1:
                    self.listbox.selection_clear(current)
                    self.listbox.selection_set(current + 1)

        elif event.keysym == "Up":
            if self.listbox.curselection() == ():
                self.listbox.selection_set(tk.END)
            else:
                current = self.listbox.curselection()[0]
                if current > 0:
                    self.listbox.selection_clear(current)
                    self.listbox.selection_set(current - 1)

        elif event.keysym == "Return":
            self.select_suggestion(None)

        elif event.keysym == "Escape":
            self.hide_dropdown()

def launch_gui():
    root = tk.Tk()
    root.title("Expense Tracker")

    # Set desired size
    window_width = 825
    window_height = 350

    # Center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2) - 75 # I find setting this to -75 makes it eye level

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Fonts
    HEADER_FONT = ("Segoe UI", 14, "bold")
    LABEL_FONT = ("Segoe UI", 10)
    BUTTON_FONT = ("Segoe UI", 10)

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

    tk.Label(visualize_panel, text="📊 Visualize Data", font=HEADER_FONT).pack(pady=10)

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
            messagebox.showerror("Error", f"❌ Failed to plot monthly spending.\n\n{str(e)}", parent=root)

    def show_spending_by_category():
        try:
            df, _ = load_data()
            plot_spending_per_category(df)
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to plot spending by category.\n\n{str(e)}", parent=root)

    def show_cumulative_spending():
        try:
            df, _ = load_data()
            plot_cumulative_spending(df)
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to plot cumulative spending.\n\n{str(e)}", parent=root)

    tk.Button(visualize_panel, text="Monthly Spending", font=BUTTON_FONT, command=show_monthly_spending).pack(pady=5, fill="x")
    tk.Button(visualize_panel, text="Spending by Category", font=BUTTON_FONT, command=show_spending_by_category).pack(pady=5, fill="x")
    tk.Button(visualize_panel, text="Cumulative Spending", font=BUTTON_FONT, command=show_cumulative_spending).pack(pady=5, fill="x")

    # ====== CENTER PANEL: Insert New Entry ======
    insert_panel = tk.Frame(container, width=100, padx=10, pady=10, bd=1, relief="groove")
    insert_panel.grid(row=0, column=1, padx=20, sticky="nsew")
    insert_panel.grid_propagate(False)

    tk.Label(insert_panel, text="📟 Insert New Entry", font=HEADER_FONT).pack(pady=10)

    tk.Label(insert_panel, text="Date (DD/MM/YYYY):", font=LABEL_FONT).pack(anchor="w")
    date_entry = tk.Entry(insert_panel)
    date_entry.pack(pady=2, fill="x")
    date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    tk.Label(insert_panel, text="Category:", font=LABEL_FONT).pack(anchor="w")
    category_combo = ttk.Combobox(insert_panel, values=[
        "Restaurant", "Toters", "Entertainment", "Groceries", "Snacks",
        "Barber", "Laundry", "Transportation", "Shopping", "Phone"
    ], state="readonly")
    category_combo.pack(pady=2, fill="x")
    category_combo.set("Restaurant")

    tk.Label(insert_panel, text="Amount (USD):", font=LABEL_FONT).pack(anchor="w")
    amount_entry = tk.Entry(insert_panel)
    amount_entry.pack(pady=2, fill="x")

    tk.Label(insert_panel, text="Notes (optional):", font=LABEL_FONT).pack(anchor="w")
    notes_entry = tk.Entry(insert_panel)
    notes_entry.pack(pady=2, fill="x")

    df, _ = load_data()
    restaurant_notes = df[df["Category"] == "Restaurant"]["Notes"].dropna().unique().tolist()
    AutocompleteDropdown(notes_entry, restaurant_notes)

    def submit_expense():
        date_str = date_entry.get().strip()
        category = category_combo.get().strip()
        amount_str = amount_entry.get().strip()
        notes = notes_entry.get().strip()

        try:
            pd.to_datetime(date_str, format='%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Date format must be DD/MM/YYYY.", parent=root)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Amount must be a number.", parent=root)
            return

        df, filepath = load_data()
        entry = {
            "Date": pd.to_datetime(date_str, format='%d/%m/%Y').strftime('%Y/%m/%d'),
            "Category": category,
            "Amount": amount,
            "Notes": notes
        }

        save_expense_entry(df, entry, filepath)
        messagebox.showinfo("Success", "✅ Expense entry saved!", parent=root)

        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        notes_entry.delete(0, tk.END)
        category_combo.set("Restaurant")

    tk.Button(insert_panel, text="Submit", font=BUTTON_FONT, command=submit_expense).pack(pady=10)

    # ====== RIGHT PANEL: Additional Tools ======
    tools_panel = tk.Frame(container, padx=10, pady=10, bd=1, relief="groove")
    tools_panel.grid(row=0, column=2, padx=20, sticky="nsew")

    tk.Label(tools_panel, text="🔧 Additional Tools", font=HEADER_FONT).pack(pady=10)

    def handle_backup():
        try:
            create_manual_backup()
            messagebox.showinfo("Backup Created", "✅ Backup file created successfully!", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to create backup.\n\n{str(e)}", parent=root)

    def handle_delete():
        confirm = messagebox.askyesno("⚠️ Confirm Deletion", "Are you sure you want to delete the main Excel file?", parent=root)
        if confirm:
            try:
                delete_main_expense_tracker()
                messagebox.showinfo("Deleted", "🗑️ Main Excel file deleted.", parent=root)
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to delete file.\n\n{str(e)}", parent=root)

    def handle_exit():
        root.quit()

    tk.Button(tools_panel, text="Create Backup", font=BUTTON_FONT, command=handle_backup).pack(pady=5, fill="x")
    tk.Button(tools_panel, text="Delete Data", font=BUTTON_FONT, command=handle_delete).pack(pady=5, fill="x")
    tk.Button(tools_panel, text="Exit", font=BUTTON_FONT, command=handle_exit).pack(pady=5, fill="x")

    root.mainloop()

if __name__ == "__main__":
    launch_gui()