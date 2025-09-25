import tkinter as tk
from tkinter import messagebox

#adding theme
Bkg_color = "#cfe2f5"
fg_color = "#0C0B0B"
btn_color = "#3B75F1"
btn_text_color = "#ffffff"
entry_box = "#ffffff"

balance = 0
transactions = []

def add_income():
    global balance
    try:
        amount = float(entry_income.get()) 
        category = income_var.get()  # use entry_income
        balance += amount
        transactions.append(("Income", amount, category))
        entry_income.delete(0, tk.END)  # clear income input
        update_ui()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for income")

def add_expense():
    global balance
    try:
        amount = float(entry_expense.get())   # use entry_expense
        category = expense_var.get()
        balance -= amount
        transactions.append(("Expense", amount, category))
        entry_expense.delete(0, tk.END)  # clear expense input
        update_ui()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for expense")

def update_ui():
    # Update balance display
    lbl_balance.config(text=f"Balance: R{balance:.2f}")

    # Update transactions list
    listbox.delete(0, tk.END)
    for t in transactions:
        listbox.insert(tk.END, f"{t[0]}: R{t[1]:.2f}")

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg=Bkg_color)

# Balance label
lbl_balance = tk.Label(root, text=f"Balance: R{balance:.2f}", font=("Arial", 16, "bold"))
lbl_balance.pack(pady=10)

# Income section
lbl_income = tk.Label(root, text="Enter Income:", font=("Arial", 12))
lbl_income.pack()
entry_income = tk.Entry(root, font=("Arial", 12))   # define entry_income
entry_income.pack(pady=5)

income_var = tk.StringVar(value="Salary")
income_categories = ["Salary", "Bonus", "Gift", "Other"]
dropdown_income = tk.OptionMenu(root, income_var, *income_categories)
dropdown_income.pack(pady=5)

btn_income = tk.Button(root, text="Add Income", command=add_income, width=15, bg=btn_color, fg=btn_text_color)
btn_income.pack(pady=5)

# Expense section
lbl_expense = tk.Label(root, text="Enter Expense:", font=("Arial", 12))
lbl_expense.pack()
entry_expense = tk.Entry(root, font=("Arial", 12))   # define entry_expense
entry_expense.pack(pady=5)

expense_var = tk.StringVar(value="Food")
expense_categories = ["Food", "Transport", "Entertainment", "Bills", "Other"]
dropdown_expense = tk.OptionMenu(root, expense_var, *expense_categories)
dropdown_expense.pack(pady=5)

btn_expense = tk.Button(root, text="Add Expense", command=add_expense, width=15,  bg=btn_color, fg=btn_text_color)
btn_expense.pack(pady=5)

# Transactions list
listbox = tk.Listbox(root, width=40, height=10, font=("Arial", 10))
listbox.pack(pady=10)

root.mainloop()