import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import json
import os

# --- Theme Colors (CSS-like) ---
BG_COLOR = "#f0f4f8"
FG_COLOR = "#333333"
BTN_COLOR = "#4CAF50"
BTN_TEXT = "#ffffff"
ENTRY_BG = "#ffffff"

# --- User data storage ---
def get_user_file(username):
    return f"user_{username}.json"

def save_user_data(username, balance, transactions):
    data = {
        "balance": balance,
        "transactions": transactions
    }
    with open(get_user_file(username), "w") as f:
        json.dump(data, f, indent=4)

def load_user_data(username):
    filename = get_user_file(username)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return data["balance"], data["transactions"]
    else:
        return 0, []  # default for new users

# --- Global variables ---
username = None
balance = 0
transactions = []

# --- Expense Report ---
def view_report():
    expense_data = [t for t in transactions if t[0] == "Expense"]

    if not expense_data:
        messagebox.showinfo("Report", "No expenses to show!")
        return

    category_totals = {}
    for _, amount, category in expense_data:
        category_totals[category] = category_totals.get(category, 0) + amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Expenses by Category")
    plt.show()

# --- Transactions ---
def add_income():
    global balance
    try:
        amount = float(entry_income.get())
        category = income_var.get()
        balance += amount
        transactions.append(("Income", amount, category))
        entry_income.delete(0, tk.END)
        update_ui()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for income")

def add_expense():
    global balance
    try:
        amount = float(entry_expense.get())
        category = expense_var.get()
        balance -= amount
        transactions.append(("Expense", amount, category))
        entry_expense.delete(0, tk.END)
        update_ui()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for expense")

def update_ui():
    lbl_balance.config(text=f"Balance: R{balance:.2f}")

    listbox.delete(0, tk.END)
    for t in transactions:
        listbox.insert(tk.END, f"{t[0]} ({t[2]}): R{t[1]:.2f}")

    save_user_data(username, balance, transactions)

# --- Login ---
def login():
    global username, balance, transactions
    username = entry_username.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter a username")
        return

    balance, transactions = load_user_data(username)

    login_frame.destroy()
    show_main_app()

# --- Main App ---
def show_main_app():
    global lbl_balance, entry_income, entry_expense, listbox, income_var, expense_var

    # Balance label
    lbl_balance = tk.Label(root, text=f"Balance: R{balance:.2f}",
                           font=("Helvetica", 18, "bold"), fg=FG_COLOR, bg=BG_COLOR)
    lbl_balance.pack(pady=10)

    # Income section
    lbl_income = tk.Label(root, text="Enter Income:", font=("Helvetica", 12),
                          fg=FG_COLOR, bg=BG_COLOR)
    lbl_income.pack()
    entry_income = tk.Entry(root, font=("Helvetica", 12), bg=ENTRY_BG)
    entry_income.pack(pady=5)

    income_var = tk.StringVar(value="Salary")
    income_categories = ["Salary", "Bonus", "Gift", "Other"]
    income_menu = tk.OptionMenu(root, income_var, *income_categories)
    income_menu.pack(pady=5)

    btn_income = tk.Button(root, text="Add Income", command=add_income,
                           width=15, bg=BTN_COLOR, fg=BTN_TEXT, font=("Helvetica", 12, "bold"))
    btn_income.pack(pady=5)

    # Expense section
    lbl_expense = tk.Label(root, text="Enter Expense:", font=("Helvetica", 12),
                           fg=FG_COLOR, bg=BG_COLOR)
    lbl_expense.pack()
    entry_expense = tk.Entry(root, font=("Helvetica", 12), bg=ENTRY_BG)
    entry_expense.pack(pady=5)

    expense_var = tk.StringVar(value="Food")
    expense_categories = ["Food", "Transport", "Rent", "Entertainment", "Other"]
    expense_menu = tk.OptionMenu(root, expense_var, *expense_categories)
    expense_menu.pack(pady=5)

    btn_expense = tk.Button(root, text="Add Expense", command=add_expense,
                            width=15, bg="#f44336", fg=BTN_TEXT, font=("Helvetica", 12, "bold"))
    btn_expense.pack(pady=5)

    # Transactions list
    listbox = tk.Listbox(root, width=50, height=12, font=("Helvetica", 11),
                         bg="#ffffff", fg="#333333", highlightbackground="#ccc")
    listbox.pack(pady=10)

    # Report button
    btn_report = tk.Button(root, text="View Expense Report", command=view_report,
                           width=20, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
    btn_report.pack(pady=5)

    update_ui()

# --- Root Window ---
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg=BG_COLOR)

# --- Login Frame ---
login_frame = tk.Frame(root, bg=BG_COLOR, pady=20)
login_frame.pack()

lbl_username = tk.Label(login_frame, text="Enter your username:", font=("Helvetica", 12),
                        fg=FG_COLOR, bg=BG_COLOR)
lbl_username.pack(pady=5)

entry_username = tk.Entry(login_frame, font=("Helvetica", 12), bg=ENTRY_BG)
entry_username.pack(pady=5)

btn_login = tk.Button(login_frame, text="Login", command=login,
                      bg=BTN_COLOR, fg=BTN_TEXT, font=("Helvetica", 12, "bold"))
btn_login.pack(pady=10)

root.mainloop()