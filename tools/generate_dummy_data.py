import pandas as pd
import random
from pathlib import Path

def generate_dummy_data():
    project_root = Path(__file__).resolve().parents[1]
    filepath = project_root / 'data' / 'Expense_Tracker.xlsx'

    categories = [
        'Restaurant', 'Toters', 'Entertainment', 'Groceries', 'Snacks',
        'Barber', 'Laundry', 'Transportation', 'Shopping', 'Phone'
    ]

    # Prepare date range once
    dates = pd.date_range(start="2025-01-01", end="2025-04-30", freq='D')

    # Generate 200 random entries
    expenses = [
        {
            'Date': random.choice(dates),
            'Category': random.choice(categories),
            'Amount': round(random.uniform(5, 200), 2),
            'Notes': ""
        }
        for _ in range(200)
    ]

    # Create DataFrame
    df = pd.DataFrame(expenses)

    # Sort by date
    df = df.sort_values(by='Date').reset_index(drop=True)

    # Format date nicely
    df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')

    # Save
    filepath.parent.mkdir(parents=True, exist_ok=True)  # Make sure the directory exists
    df.to_excel(filepath, index=False)
    print(f"✅ Dummy data generated and saved to {filepath}")

if __name__ == "__main__":
    generate_dummy_data()