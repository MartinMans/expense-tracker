import pandas as pd
from pathlib import Path
from .plot_utils import plot_monthly_spending, plot_spending_per_category, plot_cumulative_spending

def load_data():
    project_root = Path(__file__).resolve().parents[1]
    filepath = project_root / 'data' / 'Expense_Tracker.xlsx'
    df = pd.read_excel(filepath)
    return df

def main():
    df = load_data()

    while True:
        print("\n📊 What would you like to visualize?")
        print("1. Monthly Spending")
        print("2. Spending per Category")
        print("3. Cumulative Spending Over Time")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            try:
                month = int(input("Enter the month (1-12): "))
                year = int(input("Enter the year (e.g., 2025): "))
                if 1 <= month <= 12:
                    plot_monthly_spending(df, month, year)
                else:
                    print("❌ Invalid month. Please enter between 1 and 12.")
            except ValueError:
                print("❌ Invalid input. Please enter numeric values.")
        elif choice == '2':
            plot_spending_per_category(df)
        elif choice == '3':
            plot_cumulative_spending(df)
        elif choice == '4':
            print("👋 Exiting Visualization. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()