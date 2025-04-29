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
        self.hide_dropdown()

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

        current = self.listbox.curselection()
        if event.keysym == "Down":
            if not current:
                self.listbox.selection_set(0)
            elif current[0] < self.listbox.size() - 1:
                self.listbox.selection_clear(current)
                self.listbox.selection_set(current[0] + 1)

        elif event.keysym == "Up":
            if not current:
                self.listbox.selection_set(tk.END)
            elif current[0] > 0:
                self.listbox.selection_clear(current)
                self.listbox.selection_set(current[0] - 1)

        elif event.keysym == "Return":
            self.select_suggestion(None)

        elif event.keysym == "Escape":
            self.hide_dropdown()

def launch_gui():
    root = tk.Tk()
    root.title("Expense Tracker")
    window_width, window_height = 825, 350
    x = (root.winfo_screenwidth() // 2) - (window_width // 2)
    y = (root.winfo_screenheight() // 2) - (window_height // 2) - 75
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    HEADER_FONT = ("Segoe UI", 14, "bold")
    LABEL_FONT = ("Segoe UI", 10)
    BUTTON_FONT = ("Segoe UI", 10)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    container = tk.Frame(root)
    container.pack(expand=True, fill="both")
    for i in range(3):
        container.columnconfigure(i, weight=1)

    # LEFT PANEL: Visualize Data
    visualize_panel = tk.Frame(container, padx=10, pady=10, bd=1, relief="groove")
    visualize_panel.grid(row=0, column=0, padx=20, sticky="nsew")
    tk.Label(visualize_panel, text="📊 Visualize Data", font=HEADER_FONT).pack(pady=10)

    def show_monthly():
        try:
            year = simpledialog.askinteger("Year", "Enter Year (e.g., 2025):", parent=root)
            month = simpledialog.askinteger("Month", "Enter Month (1-12):", parent=root)
            if None in (month, year): return
            root.after(50, lambda: plot_monthly_spending(load_data()[0], month, year))
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to plot monthly spending.\n\n{str(e)}", parent=root)

    def show_category():
        try: plot_spending_per_category(load_data()[0])
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to plot category spending.\n\n{str(e)}", parent=root)

    def show_cumulative():
        try: plot_cumulative_spending(load_data()[0])
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to plot cumulative spending.\n\n{str(e)}", parent=root)

    def view_data():
        try:
            df, _ = load_data()
            if df.empty:
                messagebox.showinfo("Info", "No data available.", parent=root)
                return

            win = tk.Toplevel(root)
            win.title("View All Expenses")
            win.geometry("800x400")

            style = ttk.Style(win)
            style.configure("Treeview", rowheight=25)
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

            frame = tk.Frame(win)
            frame.pack(expand=True, fill="both")

            vsb = ttk.Scrollbar(frame, orient="vertical")
            hsb = ttk.Scrollbar(frame, orient="horizontal")
            tree = ttk.Treeview(frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            vsb.pack(side="right", fill="y")
            hsb.pack(side="bottom", fill="x")
            tree.pack(expand=True, fill="both")
            vsb.config(command=tree.yview)
            hsb.config(command=tree.xview)

            tree["columns"] = list(df.columns)
            tree["show"] = "headings"

            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=100)

            for _, row in df.iterrows():
                tree.insert("", tk.END, values=list(row))

            tree.see(tree.get_children()[-1])

        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to load data.\n\n{str(e)}", parent=root)

    for label, func in [
        ("Monthly Spending", show_monthly),
        ("Spending by Category", show_category),
        ("Cumulative Spending", show_cumulative),
        ("View Data", view_data)
    ]:
        tk.Button(visualize_panel, text=label, font=BUTTON_FONT, command=func).pack(pady=5, fill="x")

    # CENTER PANEL: Insert New Entry
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

    # RIGHT PANEL: Additional Tools
    tools_panel = tk.Frame(container, padx=10, pady=10, bd=1, relief="groove")
    tools_panel.grid(row=0, column=2, padx=20, sticky="nsew")
    tk.Label(tools_panel, text="🔧 Additional Tools", font=HEADER_FONT).pack(pady=10)

    for label, func in [
        ("Create Backup", lambda: (create_manual_backup(), messagebox.showinfo("Backup", "✅ Backup created!", parent=root))),
        ("Delete Data", lambda: delete_main_expense_tracker() if messagebox.askyesno("⚠️ Confirm", "Delete Excel file?", parent=root) else None),
        ("Exit", root.quit)
    ]:
        tk.Button(tools_panel, text=label, font=BUTTON_FONT, command=func).pack(pady=5, fill="x")

    root.mainloop()

if __name__ == "__main__":
    launch_gui()