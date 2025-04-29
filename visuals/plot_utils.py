import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_monthly_spending(df, month, year):
    """
    Plot daily spending for a given month and year.
    """
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
    filtered_df = df[(df['Date'].dt.month == month) & (df['Date'].dt.year == year)]

    if filtered_df.empty:
        print(f"No expenses found for {month:02d}/{year}.")
        return

    daily_spending = filtered_df.groupby(filtered_df['Date'].dt.day)['Amount'].sum()

    plt.figure(figsize=(10, 6))
    plt.plot(daily_spending.index, daily_spending.values, marker='o')

    plt.title(f"Daily Spending - {month:02d}/{year}")
    plt.xlabel("Day of Month")
    plt.ylabel("Amount Spent (USD)")
    plt.xticks(daily_spending.index, rotation=45)  # ✅ only show actual days, tilted
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_spending_per_category(df):
    """
    Plot total spending per category.
    """
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

    spending_by_category = df.groupby('Category')['Amount'].sum().sort_values()

    if spending_by_category.empty:
        print("❌ No spending data available.")
        return

    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab20.colors  # vibrant color palette
    spending_by_category.plot(kind='barh', color=colors)
    plt.title("Total Spending per Category")
    plt.xlabel("Amount Spent (USD)")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.show()

def plot_cumulative_spending(df):
    """
    Plot cumulative spending over time (line + filled area).
    """
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
    df = df.sort_values(by='Date')

    df['Cumulative'] = df['Amount'].cumsum()

    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Cumulative'], color='royalblue', linewidth=2)
    plt.fill_between(df['Date'], df['Cumulative'], color='lightblue', alpha=0.3)

    plt.title("Cumulative Spending Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Amount Spent (USD)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()