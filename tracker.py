import json
import os

DATA_FILE = "data.json"

def show_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Balance")
    print("4. View Transactions")
    print("5. Exit")

def add_income(balance, transactions):
    amount = float(input("Enter income amount: "))
    balance += amount
    transactions.append(("Income", amount))
    print(f"Added income: {amount}")
    return balance, transactions

def add_expense(balance, transactions):
    amount = float(input("Enter expense amount: "))
    balance -= amount
    transactions.append(("Expense", amount))
    print(f"Added expense: {amount}")
    return balance, transactions

def save_data(balance, transactions):
    with open(DATA_FILE, "w") as f:
        json.dump({"balance": balance, "transactions": transactions}, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data["balance"], data["transactions"]
    return 0, []

def award_badges(balance, transactions):
    badges = []

    # Badge 1: Saver (balance > 1000)
    if balance >= 1000:
        badges.append("💰 Saver Badge")

    # Badge 2: Budget Keeper (10+ transactions)
    if len(transactions) >= 10:
        badges.append("📊 Budget Keeper")

    # Badge 3: Balanced Life (more income than expenses)
    income = sum(t[1] for t in transactions if t[0] == "Income")
    expenses = sum(t[1] for t in transactions if t[0] == "Expense")
    if income > expenses:
        badges.append("⚖️ Balanced Life")

    return badges

def save_data(balance, transactions):
    data = {
        "balance": balance,
        "transactions": transactions,
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("balance", 0), data.get("transactions", [])
    return 0, []

def main():
    balance, transactions = load_data()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            balance, transactions = add_income(balance, transactions)
        elif choice == "2":
            balance, transactions = add_expense(balance, transactions)
        elif choice == "3":
            print(f"Your balance is: {balance}")
            badges = award_badges(balance, transactions)
            if badges:
                print("🎉 You earned these badges:")
                for b in badges:
                    print(f"- {b}")
                else:
                    print("No badges yet. Keep going!")

        elif choice == "4":
            print("Transactions:")
            for t in transactions:
                print(f"- {t[0]}: {t[1]}")
        elif choice == "5":
            save_data(balance, transactions)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
