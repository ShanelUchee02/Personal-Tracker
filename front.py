import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

# --- Theme Colors ---
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
canvas = None  # for pie chart

# --- Update Pie Chart in Overview ---
def update_pie_chart(frame):
    global canvas

    # Clear old chart if it exists
    if canvas:
        canvas.get_tk_widget().destroy()

    expense_data = [t for t in transactions if t[0] == "Expense"]

    if not expense_data:
        lbl_no_data = tk.Label(frame, text="No expenses yet", font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR)
        lbl_no_data.pack()
        return

    category_totals = {}
    for _, amount, category in expense_data:
        category_totals[category] = category_totals.get(category, 0) + amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    ax.set_title("Expenses by Category")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# --- Transactions ---
def add_income(category):
    global balance
    try:
        amount = float(entry_income.get())
        balance += amount
        transactions.append(("Income", amount, category))
        entry_income.delete(0, tk.END)
        update_ui()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for income")

def add_expense(category):
    global balance
    try:
        amount = float(entry_expense.get())
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

    # Update overview
    total_income = sum(t[1] for t in transactions if t[0] == "Income")
    total_expenses = sum(t[1] for t in transactions if t[0] == "Expense")
    num_transactions = len(transactions)

    lbl_overview_balance.config(text=f"Balance: R{balance:.2f}")
    lbl_overview_income.config(text=f"Total Income: R{total_income:.2f}")
    lbl_overview_expense.config(text=f"Total Expenses: R{total_expenses:.2f}")
    lbl_overview_count.config(text=f"Transactions: {num_transactions}")

    save_user_data(username, balance, transactions)

    # Refresh pie chart
    for widget in chart_frame.winfo_children():
        widget.destroy()
    update_pie_chart(chart_frame)

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

# --- Main App with Tabs ---
def show_main_app():
    global lbl_balance, entry_income, entry_expense, listbox
    global lbl_overview_balance, lbl_overview_income, lbl_overview_expense, lbl_overview_count, chart_frame

    # Notebook (Tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # --- Overview Tab ---
    overview_tab = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(overview_tab, text="Overview")

    lbl_overview_title = tk.Label(overview_tab, text="📊 Overview", font=("Helvetica", 16, "bold"),
                                  fg=FG_COLOR, bg=BG_COLOR)
    lbl_overview_title.pack(pady=10)

    lbl_overview_balance = tk.Label(overview_tab, text="Balance: R0.00",
                                    font=("Helvetica", 14), fg=FG_COLOR, bg=BG_COLOR)
    lbl_overview_balance.pack(pady=5)

    lbl_overview_income = tk.Label(overview_tab, text="Total Income: R0.00",
                                   font=("Helvetica", 12), fg=FG_COLOR, bg=BG_COLOR)
    lbl_overview_income.pack(pady=5)

    lbl_overview_expense = tk.Label(overview_tab, text="Total Expenses: R0.00",
                                    font=("Helvetica", 12), fg=FG_COLOR, bg=BG_COLOR)
    lbl_overview_expense.pack(pady=5)

    lbl_overview_count = tk.Label(overview_tab, text="Transactions: 0",
                                  font=("Helvetica", 12), fg=FG_COLOR, bg=BG_COLOR)
    lbl_overview_count.pack(pady=5)

    # Chart area
    chart_frame = tk.Frame(overview_tab, bg=BG_COLOR)
    chart_frame.pack(pady=10)

    # --- Income Tab ---
    income_tab = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(income_tab, text="Income")

    lbl_income = tk.Label(income_tab, text="Enter Income:", font=("Helvetica", 12),
                          fg=FG_COLOR, bg=BG_COLOR)
    lbl_income.pack(pady=5)
    entry_income = tk.Entry(income_tab, font=("Helvetica", 12), bg=ENTRY_BG)
    entry_income.pack(pady=5)

    lbl_income_cat = tk.Label(income_tab, text="Choose Category:", font=("Helvetica", 12),
                              fg=FG_COLOR, bg=BG_COLOR)
    lbl_income_cat.pack(pady=5)

    income_categories = ["Salary", "Bonus", "Gift", "Other"]
    for cat in income_categories:
        btn = tk.Button(income_tab, text=cat, command=lambda c=cat: add_income(c),
                        width=15, bg=BTN_COLOR, fg=BTN_TEXT, font=("Helvetica", 12, "bold"))
        btn.pack(pady=3)

    # --- Expense Tab ---
    expense_tab = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(expense_tab, text="Expenses")

    lbl_expense = tk.Label(expense_tab, text="Enter Expense:", font=("Helvetica", 12),
                           fg=FG_COLOR, bg=BG_COLOR)
    lbl_expense.pack(pady=5)
    entry_expense = tk.Entry(expense_tab, font=("Helvetica", 12), bg=ENTRY_BG)
    entry_expense.pack(pady=5)

    lbl_expense_cat = tk.Label(expense_tab, text="Choose Category:", font=("Helvetica", 12),
                               fg=FG_COLOR, bg=BG_COLOR)
    lbl_expense_cat.pack(pady=5)

    expense_categories = ["Food", "Transport", "Rent", "Entertainment", "Other"]
    for cat in expense_categories:
        btn = tk.Button(expense_tab, text=cat, command=lambda c=cat: add_expense(c),
                        width=15, bg="#f44336", fg=BTN_TEXT, font=("Helvetica", 12, "bold"))
        btn.pack(pady=3)

    # --- Transactions Tab ---
    transactions_tab = tk.Frame(notebook, bg=BG_COLOR)
    notebook.add(transactions_tab, text="Transactions")

    lbl_balance = tk.Label(transactions_tab, text=f"Balance: R{balance:.2f}",
                           font=("Helvetica", 16, "bold"), fg=FG_COLOR, bg=BG_COLOR)
    lbl_balance.pack(pady=10)

    listbox = tk.Listbox(transactions_tab, width=50, height=12, font=("Helvetica", 11),
                         bg="#ffffff", fg="#333333", highlightbackground="#ccc")
    listbox.pack(pady=10)

    update_ui()

# --- Root Window ---
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg=BG_COLOR)
root.geometry("500x600")

# --- Login Frame ---
login_frame = tk.Frame(root, bg=BG_COLOR, pady=20)
login_frame.pack(expand=True)

lbl_username = tk.Label(login_frame, text="Enter your username:", font=("Helvetica", 12),
                        fg=FG_COLOR, bg=BG_COLOR)
lbl_username.pack(pady=5)

entry_username = tk.Entry(login_frame, font=("Helvetica", 12), bg=ENTRY_BG)
entry_username.pack(pady=5)

btn_login = tk.Button(login_frame, text="Login", command=login,
                      bg=BTN_COLOR, fg=BTN_TEXT, font=("Helvetica", 12, "bold"))
btn_login.pack(pady=10)

root.mainloop()