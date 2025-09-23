from tkinter import messagebox
import tkinter as tk

balance = 0
transactions = []

def add_income():
    global balance
    try:
        amount = float(entry_amount.get())
        balance += amount
        transactions.append(("Income", amount))
        update_ui()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

def add_expense():
    global balance
    try:
        amount = float(entry_amount.get())
        balance -= amount
        transactions.append(("Expense", amount))
        update_ui()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

def update_ui():
    lbl_balance.config(text=f"Balance: {balance}")
    listbox.delete(0, tk.END)
    for t in transactions:
        listbox.insert(tk.END, f"{t[0]}: {t[1]}")

#GUI Setup
root = tk.Tk()
root.title("Expense Tracker")

lbl_balance = tk.Label(root, text=f"Balance: {balance}", font=("Arial", 14))
lbl_balance.pack(pady=5)

entry_amount = tk.Entry(root)
entry_amount.pack(pady=5)

btn_add_income = tk.Button(root, text="Add Income", command=add_income)
btn_add_income.pack(pady=5)

btn_add_expense = tk.Button(root, text="Add Expense", command=add_expense)
btn_add_expense.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=5)

root.mainloop()