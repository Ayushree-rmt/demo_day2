import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

FILE_NAME = "expenses.csv"


# -----------------------------
# Create CSV file if not exists
# -----------------------------
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])


# -----------------------------
# Load expenses
# -----------------------------
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    total = 0

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        row["Date"],
                        row["Category"],
                        row["Description"],
                        row["Amount"]
                    )
                )

                total += float(row["Amount"])

        total_label.config(text=f"Total Expenses: ₹{total:.2f}")

    except FileNotFoundError:
        create_file()


# -----------------------------
# Add expense
# -----------------------------
def add_expense():

    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if not date or not category or not description or not amount:
        messagebox.showwarning(
            "Missing Data",
            "Please fill all fields."
        )
        return

    try:
        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            date,
            category,
            description,
            amount
        ])

    messagebox.showinfo(
        "Success",
        "Expense added successfully!"
    )

    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    load_expenses()


# -----------------------------
# Delete expense
# -----------------------------
def delete_expense():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Select Expense",
            "Please select an expense to delete."
        )
        return

    values = tree.item(selected[0], "values")

    date = values[0]
    category = values[1]
    description = values[2]
    amount = values[3]

    rows = []

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row != [date, category, description, amount]:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    load_expenses()


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x550")
root.resizable(False, False)

create_file()

# Title
title_label = tk.Label(
    root,
    text="Expense Tracker",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=15)


# -----------------------------
# Input Frame
# -----------------------------
input_frame = tk.Frame(root)
input_frame.pack(pady=10)


# Date
tk.Label(
    input_frame,
    text="Date:"
).grid(row=0, column=0, padx=5, pady=5)

date_entry = tk.Entry(input_frame, width=18)
date_entry.grid(row=0, column=1, padx=5, pady=5)

date_entry.insert(
    0,
    datetime.now().strftime("%Y-%m-%d")
)


# Category
tk.Label(
    input_frame,
    text="Category:"
).grid(row=0, column=2, padx=5, pady=5)

category_entry = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Education",
        "Health",
        "Other"
    ],
    width=16
)

category_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# Description
tk.Label(
    input_frame,
    text="Description:"
).grid(row=1, column=0, padx=5, pady=5)

description_entry = tk.Entry(
    input_frame,
    width=18
)

description_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# Amount
tk.Label(
    input_frame,
    text="Amount:"
).grid(row=1, column=2, padx=5, pady=5)

amount_entry = tk.Entry(
    input_frame,
    width=18
)

amount_entry.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)


# Add button
add_button = tk.Button(
    input_frame,
    text="Add Expense",
    command=add_expense,
    width=15
)

add_button.grid(
    row=2,
    column=1,
    columnspan=2,
    pady=15
)


# -----------------------------
# Expense Table
# -----------------------------
columns = (
    "Date",
    "Category",
    "Description",
    "Amount"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:
    tree.heading(column, text=column)

tree.column("Date", width=120)
tree.column("Category", width=150)
tree.column("Description", width=250)
tree.column("Amount", width=120)

tree.pack(pady=10)


# -----------------------------
# Delete Button
# -----------------------------
delete_button = tk.Button(
    root,
    text="Delete Selected Expense",
    command=delete_expense,
    width=25
)

delete_button.pack(pady=5)


# -----------------------------
# Total
# -----------------------------
total_label = tk.Label(
    root,
    text="Total Expenses: ₹0.00",
    font=("Arial", 16, "bold")
)

total_label.pack(pady=10)


# Load existing data
load_expenses()

# Start application
root.mainloop()