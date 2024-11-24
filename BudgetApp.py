import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

columns = ["Date", "Category", "Description", "Amount"]
data = pd.DataFrame(columns=columns)

def add_transaction():
    global data
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number!")
        return

    new_row = {"Date": date, "Category": category, "Description": description, "Amount": amount}
    data.loc[len(data)] = new_row
    update_table()
    clear_entries()
    messagebox.showinfo("Success", "Transaction added successfully!")

def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def update_table():
    for row in table.get_children():
        table.delete(row)
    for index, row in data.iterrows():
        table.insert("", "end", values=(row["Date"], row["Category"], row["Description"], row["Amount"]))

def view_summary():
    global data
    if data.empty:
        messagebox.showinfo("Summary", "No transactions recorded.")
        return

    income = data[data["Amount"] > 0]["Amount"].sum()
    expenses = data[data["Amount"] < 0]["Amount"].sum()
    balance = income + expenses
    summary_message = f"Total Income: {income:.2f}\nTotal Expenses: {expenses:.2f}\nBalance: {balance:.2f}"
    messagebox.showinfo("Summary", summary_message)

def save_to_csv():
    global data
    file_name = "budget_tracker.csv"
    data.to_csv(file_name, index=False)
    messagebox.showinfo("Save", f"Data saved to {file_name}.")

def load_from_csv():
    global data
    file_name = "budget_tracker.csv"
    try:
        data = pd.read_csv(file_name)
        update_table()
        messagebox.showinfo("Load", f"Data loaded from {file_name}.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"No file named {file_name} found.")

root = tk.Tk()
root.title("Budget Tracker")

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=5)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Amount (positive for income, negative for expense):").grid(row=3, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Add Transaction", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="View Summary", command=view_summary).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(root, text="Save to CSV", command=save_to_csv).grid(row=6, column=0, pady=5)
tk.Button(root, text="Load from CSV", command=load_from_csv).grid(row=6, column=1, pady=5)

table = ttk.Treeview(root, columns=("Date", "Category", "Description", "Amount"), show="headings", height=10)
table.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

root.mainloop()
